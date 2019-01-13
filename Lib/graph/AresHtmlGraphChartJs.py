#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

'''
Module used as a wrapper to the Javascript NVD3 libraries
reference website: http://www.chartjs.org/docs/latest/

Main functions to know

addAttr

:example
chart.addAttr('labels', ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"], category='data')
chart.addAttr('beginAtZero', True, ["scales", 'yAxes', 'ticks'],  category='options')

'''

import time
import json
import os
import re

from ares.Lib.AresImports import requires
from ares.Lib.html import AresHtml
from ares.Lib.graph import AxisDisplay
from ares.Lib.graph import AresHtmlGraphFabric


DSC = {
  'eng': '''
'''
}


class Chart(AresHtml.Html):
  """
  :category: Chart
  :rubric: PY
  :type: Interface
  :dsc:
    ChartJs is the main javascript library used for displaying charts. This is an external javascript package and all the details about the library are available on the [website](https://www.chartjs.org/)
    In AReS it is easy to use this framework and it is set as the default one for most of the charts. You can see the priority order [here](api?enum=charts)

    ## Define a ChartJs object

    The chartJs object is created from the Python layer to then be run at the end on the Javascript side in your browser. Basically all the configurationss and properties of your charts should be already known and set in the Python layer to be then translated.
    Some generic functions are available to set the properties but do not hesitate to have a look at the Chart documentation to get more details (Not all of them have been wrapped yet).

    ## Input Data

    In most of the chart the expected data is a dc() object. dc stands for data Chart object and it is built based on a AReS Dataframe. This object will clean up the dataframe and also define some pointers for the xAxis and the seriesNames to be displayed.
    Some extra parameters are allowed to then transform the data (from the dictionary), before feeding the chart object. This design allows events and data updates hence dynamic and interactive charts.

    ## Examples


    ## Exports

    All the charts can be exported to different formats. This work is currently in progress. In static format (word, pdf and ppt), chart definitions will be converted in pictures using matplotlib.
    Each javascript charting library will be wrapped in a way that they will have a to_img() function which will be in charge of building the correct picture. Today this is in progress.
    For the HTML and Excel export, we rely on the software to display the charts. Basically we are using formulas in Excel and HTML is not at all transformed

  """
  name, category, callFnc = 'ChartJs', 'Charts', 'plotChartJs'
  references = {
    'Website': 'http://www.chartjs.org/',
    'Documentation': 'http://www.chartjs.org/docs/latest/',
    'examples': 'http://tobiasahlin.com/blog/chartjs-charts-to-get-you-started/#10-bubble-chart',
    'Repository': 'https://github.com/chartjs/Chart.js'}
  __pyStyle = ['CssDivChart']
  __reqJs, __reqCss = ['chartjs', 'datatables', 'datatables-export'], ['datatables', 'datatables-export']
  dataPmts = ["type", "fill", "showLine", "pointHoverRadius", 'pointStyle', 'pointRadius', 'steppedLine',
              'backgroundColor', 'borderColor', 'color', 'borderColor']

  def __init__(self, aresObj, chartType, data, width, widthUnit, height, heightUnit, title, chartOptions, toolsbar, htmlCode, globalFilter):
    if chartOptions is None:
      chartOptions = {}
    if AresHtmlGraphFabric.CHARTS_FACTORY is None:
      AresHtmlGraphFabric.CHARTS_FACTORY = AresHtmlGraphFabric.loadFactory() # atomic function to store all the different table mapping
    self.title, self.toolsbar, self.seriesProperties, self.height = title, toolsbar, {'static': {}, 'dynamic': {}}, height
    super(Chart, self).__init__(aresObj, [], code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.__chart = AresHtmlGraphFabric.CHARTS_FACTORY[self.name][chartType](aresObj, data, self.seriesProperties)
    if self.__chart.jsType is not None:
      # Simple remapping to be able to reuse existing transformation functions for new chart configurations
      # This will allow the creation of dynamic configurations based on existing charts
      data._schema['out']['config'] = data._schema['out']['name']
      data._schema['out']['name'] = "%s_%s" % (data._schema['out']['family'], self.__chart.jsType.replace("-", ""))
    self.__chart.data.attach(self)
    self.__chart.data.post(('extend-dataset', self.seriesProperties, 'datasets'))
    self.setSeriesColor(aresObj.cssObj._charts)
    self.css({'position': 'relative'})
    self.__chart.addAttr('position', chartOptions.get('legend', {'position': 'right'}).get('position', 'right'), ['legend'], category='options')
    self.__chart.addAttr('bottom', 20, ['layout', 'padding'], category='options')
    if title:
      self.__chart.addAttr('text', title, ['title'], category='options')
      self.__chart.addAttr('display', True, ['title'], category='options')
    if globalFilter:
      if self._code is None:
        raise Exception("ERROR: ChartJs - %s -  Please add an htmlCode to name your filter" % chartType)

      if globalFilter is True:
        self.filter(data._jqId, list(self.__chart.data._schema['keys'])[0])
      else:
        self.filter(**globalFilter)
      self.jsFrg('click', ''' 
          var activePoints = window['%(htmlId)s_chart'].getElementsAtEvent(event); var activeDataSet = window['%(htmlId)s_chart'].getDatasetAtEvent(event); 
          if(activePoints.length > 0) { 
            var clickedElementindex = activePoints[0]["_index"];
            data.event_index = clickedElementindex; data['value'] = window['%(htmlId)s_chart'].data.datasets[activeDataSet[0]["_datasetIndex"]].data[clickedElementindex] ;
            data.xaxis = window['%(htmlId)s_chart'].data.labels[clickedElementindex]; 
            data.label = window['%(htmlId)s_chart'].data.datasets[activeDataSet[0]["_datasetIndex"]].label;
            data.column = window['%(htmlId)s_chart'].data.datasets[activeDataSet[0]["_datasetIndex"]].xaxis;
            if(%(breadCrumVar)s['params']['%(htmlCode)s'] == data.xaxis) {%(breadCrumVar)s['params']['%(htmlCode)s'] = '' }
            else {%(breadCrumVar)s['params']['%(htmlCode)s'] = data.xaxis}
          } ''' % {"htmlId": self.htmlId, "htmlCode": self._code, "breadCrumVar": self.aresObj.jsGlobal.breadCrumVar})

  def filter(self, jsId, colName, allSelected=True, filterGrp=None):
    """
    :category: Data Transformation
    :rubric: JS
    :type: Filter
    :dsc:
      Link the data to the filtering function. The record will be filtered based on the composant value
    :return: The Python Html Object
    """
    self.aresObj.jsOnLoadFnc.add("%(breadCrumVar)s['params']['%(htmlCode)s'] = ''" % {'htmlCode': self._code, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar})
    val = "%(breadCrumVar)s['params']['%(htmlCode)s'] " % {'htmlCode': self._code, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar}
    colAlias = "%s_%s" % (self.htmlId, colName)
    if allSelected:
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {'allIfEmpty': []})[colAlias] = val
      self.aresObj.jsSources.setdefault(jsId, {})['filters']['allIfEmpty'].append(colAlias)
    else:
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {})[colAlias] = val
    self.aresObj.jsSources.setdefault(jsId, {})['filters'].setdefault('_colsMaps', {})[colAlias] = colName
    return self

  @property
  def jsQueryData(self): return "{}" % {"htmlId": self.htmlId}

  def onDocumentLoadVar(self): pass

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    self.ctx = []  # Just to ensure that the Structure of the chart component will not be changed in the python layer
    AresHtmlGraphFabric.Chart.resolveDict(dict([(key, val) for key, val in self.__chart.items() if val]), self.ctx)
    self.aresObj.jsOnLoadFnc.add('''window['%(htmlId)s_def'] = {%(chartDef)s}; %(jsChart)s
      ''' % {'htmlId': self.htmlId, 'chartDef': ", ".join(self.ctx), 'jsChart': self.jsGenerate(None)})

  def onDocumentLoadFnc(self): return True


  # --------------------------------------------------------------------------------------------------------------
  #                                             USER FUNCTIONS SECTION
  #
  def addSeries(self, type, label, data, options=None, color=None):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.addSerie("line", 'test', [1, 2, 3], {"borderColor": "red" })
    :dsc:
      Add a bespoke series to a chartJs chart.
      Be aware that the type might depend of the type expected by your chart at the beginning. Basically if you create a bar chart
      you will not be able to add line series. The best in this case is to create a multi chart.
    :link ChartJs Example: http://www.chartjs.org/samples/latest/scales/logarithmic/line.html
    """
    if options is None:
      options = {}
    seriesIndex = len(self.__chart.data._schema['values'])
    colors = color if color is not None else self.aresObj.cssObj._charts[seriesIndex]
    self.__chart.data._data[label] = data
    self.__chart.data._schema['values'].add(label)
    self.__chart.data._schema['fncs'][0]['args'][1].append(label)
    self.__chart.data._schema['post'][0]['args'][0]['dynamic'][seriesIndex] = options
    options.update({'backgroundColor': colors, 'type': type})
    if type == 'line':
      options['borderColor'] = colors
    return self

  def setType(self, htmlObj):
    """
    :category: Chart Type
    :rubric: JS
    :type: Configuration
    :dsc:
      Put a type based on the value of ARes component
    :return: The Python Chart object
    """
    self.addAttr("type", htmlObj.val, isPyData=False)
    return self

  def addLine(self, label, data, options=None):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.addLine('test', [1, 2, 3], {"borderColor": "red" })
    :dsc:
      Add a line series to a chartJs chart.
      Be aware that the type might depend of the type expected by your chart at the beginning. Basically if you create a bar chart
      you will not be able to add line series. The best in this case is to create a multi chart.
    :link ChartJs Example: http://www.chartjs.org/samples/latest/scales/logarithmic/line.html
    """
    extraOption = {'fill': False}
    if options is not None:
      extraOption.update(options)
    self.addSeries('line', label, data, extraOption)

  def addPoints(self, label, data, options=None):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.addPoints('test', [1, 2, 3], {"borderColor": "red" })
    :dsc:
      Add a Point series to a chartJs chart.
      Be aware that the type might depend of the type expected by your chart at the beginning. Basically if you create a bar chart
      you will not be able to add line series. The best in this case is to create a multi chart.
    :link ChartJs Example: http://www.chartjs.org/samples/latest/scales/logarithmic/scatter.html
    """
    extraOption = {'fill': False, 'showLine': False}
    if options is not None:
      extraOption.update(options)
    self.addSeries('line', label, data, extraOption)

  def addTriangles(self, label, data, options=None):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.addTriangles('test', [1, 2, 3], {"borderColor": "red" })
    :dsc:
      Add a Point series to a chartJs chart.
      Be aware that the type might depend of the type expected by your chart at the beginning. Basically if you create a bar chart
      you will not be able to add line series. The best in this case is to create a multi chart.
    :link ChartJs Example: http://www.chartjs.org/samples/latest/scales/logarithmic/scatter.html
    """
    extraOption = {'fill': False, 'pointStyle': 'triangle', 'showLine': False}
    if options is not None:
      extraOption.update(options)
    self.addSeries('scatter', label, data, extraOption)


  # --------------------------------------------------------------------------------------------------------------
  #                                             CHART PROPERTIES FUNCTIONS
  #
  def _formatAxis(self, axisName, formatFnc, label=None, options=None, isPyData=False):
    formatFnc = AxisDisplay.DISPLAYS.get(formatFnc, {'tickFormat': formatFnc} )
    if 'labelString' in formatFnc:
      label = formatFnc['labelString']
    if label is not None:
      self.addAttr('display', True, ['scales', axisName, 'scaleLabel'], category='options')
      self.addAttr('labelString', label, ['scales', axisName, 'scaleLabel'], category='options')
    if options is None:
      options = {'digits': 0}
    if 'digits' not in options:
      options['digits'] = 0
    self.addAttr('ticks', " {callback: %s} " % formatFnc['tickFormat'] % options, ['scales', axisName], category='options', isPyData=isPyData)

  def addYAxis(self, axeId, position, type='linear', options=None):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.addYAxis( "", 'right')
    :dsc:
      To attached a series to a new axis; use the option 'yAxisID': 'axeId'
    :link ChartJs Documentation: https://www.chartjs.org/docs/latest/axes/
    :link ChartJs Documentation 2: https://www.chartjs.org/docs/latest/developers/axes.html
    """
    axisName = 'xAxes' if self.__chart.chartCall in ['hbar'] else 'yAxes'
    axis = {'id': json.dumps(axeId), 'type': json.dumps(type), 'position': json.dumps(position)}
    if options is not None:
      for key, val in options.items():
        axis[key] = json.dumps(val)
    self.__chart['options'].setdefault('scales', {}).setdefault(axisName, []).append(axis)

  def yFormat(self, formatFnc, label=None, options=None, isPyData=False):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.yFormat('K')
    :example: myChart.yFormat( "function(d) { return d3.format(',.2f')(d) }" )
    :dsc:
      Function to format the y-axis. Some formats are already pre defined.
      You can also put a full Javascript function if you want to test a bespoke formatting
    :wrap AxisDisplay: DISPLAYS
    """
    axisName = 'xAxes' if self.__chart.chartCall in ['hbar'] else 'yAxes'
    self._formatAxis(axisName, formatFnc, label, options, isPyData)
    return self

  def xFormat(self, formatFnc, label=None, options=None, isPyData=False):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.xFormat('K')
    :dsc:
      Function to format the x-axis. Some formats are already pre defined
    :wrap AxisDisplay: DISPLAYS
    :link ChartJs Documentation: https://www.chartjs.org/docs/latest/axes/cartesian/time.html
    """
    axisName = 'yAxes' if self.__chart.chartCall in ['hbar'] else 'xAxes'
    self._formatAxis(axisName, formatFnc, label, options, isPyData)

  def addSeriesAttr(self, seriesId, data, dataType=None):
    """
    :category: Chartjs Series Attributes
    :rubric: JS
    :example: >>> chartObj.addSeriesAttr(0, {'label': 'Youpi', 'pointStyle': 'triangle', 'pointRadius': 10})
    :dsc:
      Add attributes to the selected series in the dataset. The series is defined by its index (number) starting from
      zeros in the dataset.
    :link ChartJs Documentation: http://www.chartjs.org/docs/latest/charts/bar.html
    :return: The Python object itself
    """
    if seriesId is None:
      # None will apply this to all the series
      typeAttrs = 'static' if dataType is None else dataType
      self.seriesProperties[typeAttrs].update(data)
    else:
      typeAttrs = 'dynamic' if dataType is None else dataType
      self.seriesProperties[typeAttrs].setdefault(seriesId, {}).update(data)
    return self

  def setSeriesColor(self, colors, seriesId=None):
    """
    :category:
    :rubric: JS
    :example:
    :dsc:

    """
    self.__chart._colors(colors, seriesId)
    return self

  def addAttr(self, key, val=None, tree=None, category=None, isPyData=True):
    """
    :category: ChartJs Attributes
    :rubric: JS
    :example: >>>
    :dsc:
      Add attributes to the javascript chart. Simple python interface to add attributes but also properties to
      all the difference object in the structure. Values can be python object but also Javascript objects like functions.
    :link ChartJs Documentation: http://www.chartjs.org/docs/latest/configuration/legend.html
    :return: The python object itself
    """
    if isinstance(key, dict):
      for k, v in key.items():
        self.__chart.addAttr(k, v, tree, category, isPyData)
    else:
      self.__chart.addAttr(key, val, tree, category, isPyData)
    return self

  def delAttr(self, keys, tree=None, category=None): self.__chart.delAttr(keys, tree, category)

  def showLabels(self, flag):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.showLabels( False )
    :dsc:
      Show or hide the legend definition
    """
    self.__chart.addAttr('display', flag, ['legend'], category='options')

  def showGrid(self, xGridFlag, yGridFlag):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.showGrid( True, True )
    :dsc:
      Display or not the x and y grids in the charts
    :link ChartJs Documentation: https://www.chartjs.org/docs/latest/axes/styling.html
    """
    self.__chart.addAttr('display', yGridFlag, ['scales', 'yAxes', 'gridLines'], category='options')
    self.__chart.addAttr('display', xGridFlag, ['scales', 'xAxes', 'gridLines'], category='options')

  def dataSetType(self, chartType, seriesId=None):
    """
    :category: Python - ChartJs
    :rubric: PY
    :example: myChart.dataSetType( "bullet", 0)
    :dsc:
      Change the type of a series in the chart.
      Make sure you are using a chart compatible with the Series you are requesting.
      For example the type multi chart will accept any type of series.
    :return:
    """
    self.__chart.dataSetType(chartType, seriesId)

  def jsRemove(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: myChart.jsRemove()
    :dsc:
      Javascript function to remove the content of a chart container. By triggering this function the chart will be
      totally removed from the page and only a F5 might restore it
    :return: The javascript string used to perform this event
    """
    return '$("#%s_container").remove()' % self.htmlId

  def jsGenerate(self, jsData='data', jsDataKey=None, isPyData=False, jsId=None):
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
      window['%(htmlId)s_def'].data = %(dc)s;
      if(window['%(htmlId)s_chart'] !== undefined){window['%(htmlId)s_chart'].destroy();};
      window['%(htmlId)s_chart'] = new %(jsCls)s($("#%(htmlId)s").get(0).getContext('2d'), window['%(htmlId)s_def']); %(time)s;
      ''' % {'htmlId': self.htmlId, 'time': AresHtmlGraphFabric.Chart.jsLastUpdate(self.htmlId),
             'dc': self.__chart.data.setId(jsData).getJs(), 'jsCls': self.__chart.jsCls}

  def jsAddSeries(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.jsAddSeries( {"data": [1, 2, 3], "label": "series 1"} )
    :dsc:
      Function to add on the Javascript side a Series to a chart on demand. This will usually be triggered thanks to a javascript event.
      If the series already exists, it will be replaced by the new one.
    :link ChartJs Documentation: https://stackoverflow.com/questions/8073673/how-can-i-add-new-array-elements-at-the-beginning-of-an-array-in-javascript
    """
    # TODO: Improve the jsAddSeries implementation for ChartJs to extebd xAxis
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
      if ( $.trim(%(jsData)s.label) != '') {
        var indexSeries = -1 ; var records = %(jsData)s; records.data = records.y;
        var chartColors = %(chartColors)s;
        %(htmlId)s_chart.data.datasets.forEach( function(rec, index) {if (rec.label == records.label) { indexSeries = index; } });
        if (indexSeries != -1) { %(htmlId)s_chart.data.datasets.shift(indexSeries); }
        if (records.backgroundColor == undefined) {records.backgroundColor = chartColors[%(htmlId)s_chart.data.datasets.length]; records.borderColor= chartColors[%(htmlId)s_chart.data.datasets.length]};
        %(htmlId)s_chart.data.datasets.unshift( records );
        %(htmlId)s_chart.update();
      } ''' % {'htmlId': self.htmlId, 'jsData': jsData, 'chartColors': json.dumps(self.aresObj.cssObj._charts)}

  def click(self, jsFncs):
    """
    :category: Javascript - ChartJs
    :rubric: JS
    :example: myChart.click( aresObj.jsConsole() )
    :dsc:
      Add a click event on the different items in a Chart. This will act like a button and might trigger some other function on the browser side.
      It might be also used to trigger some Ajax JsPost services
    :link ChartJs Documentation: https://www.chartjs.org/docs/latest/general/interactions/events.html
    """
    if isinstance(jsFncs, list):
      jsFncs = ";".join(jsFncs)
    self.jsFrg('click', '''
      var activePoints = window['%(htmlId)s_chart'].getElementsAtEvent(event); var activeDataSet = window['%(htmlId)s_chart'].getDatasetAtEvent(event); 
      if(activePoints.length > 0) {
        var clickedElementindex = activePoints[0]["_index"];
        data['event_index'] = clickedElementindex; data['value'] = window['%(htmlId)s_chart'].data.datasets[activeDataSet[0]["_datasetIndex"]].data[clickedElementindex] ;
        data['labels'] = window['%(htmlId)s_chart'].data.labels[clickedElementindex]; 
        data['label'] = window['%(htmlId)s_chart'].data.datasets[activeDataSet[0]["_datasetIndex"]].label;
        if ( '%(htmlCode)s' != 'None') { %(breadCrumVar)s['params']['%(htmlCode)s'] = data['label'] } ;
        %(jsFncs)s ;
      } ''' % {"htmlId": self.htmlId, 'jsFncs': jsFncs, "htmlCode": self.htmlCode, "breadCrumVar": self.aresObj.jsGlobal.breadCrumVar} )

  def toolTip(self, category='label', digit=0, format='%(label)s +": "+ %(value)s.formatMoney(%(digit)s, ",", ".")'):
    """
    :category: Python - ChartJs
    :rubric: PY
    :example: myChart.toolTip()
    :dsc:
      Change the tooltip feature of the chartJs.
      This will translate a python String to a Javascript valid fragment.
    :link ChartJs Documentation: https://www.chartjs.org/docs/latest/configuration/tooltip.html
    """
    formatStr = re.compile("%\(([0-9a-zA-Z_]*)\)s")
    #matches = formatStr.findall(format)
    mapCodes = {"digit": digit, "label": "data.labels[tooltipItems.index]", "value": "data.datasets[tooltipItems.datasetIndex].data[tooltipItems.index]", "y": "tooltipItems.yLabel", "x": "tooltipItems.xLabel"}
    format = format % mapCodes
    #if matches:
    #  for res in formatStr.finditer(format):
    #    format = format.replace(res.group(0), mapCodes[res.group(1)])
    self.__chart.addAttr(category, 'function(tooltipItems, data) { return %(format)s; }' % {'format':  format}, ['tooltips', 'callbacks'], category='options', isPyData=False)
    return self

  def addLayout(self, data):
    """
    """
    if 'barmode' in data:
      self.__chart.addAttr('stacked', data['barmode'] == 'stack', ['scales', 'xAxes'], category='options')
      self.__chart.addAttr('stacked', data['barmode'] == 'stack', ['scales', 'yAxes'], category='options')
    return self

  # -----------------------------------------------------------------------------------------
  #                                    CHART EXPORT FUNCTIONS
  # -----------------------------------------------------------------------------------------
  def toImg(self): return "window['%s_chart'].toBase64Image()" % self.htmlId
  def toTsv(self): return "'data:text/csv;charset=utf-8,' + encodeURIComponent(%s)" % self.__chart.data.toTsv()

  # -----------------------------------------------------------------------------------------
  #                                    CHART EXPORT OPTIONS
  # -----------------------------------------------------------------------------------------
  def __str__(self):
    strChart = '<div style="height:%spx"><canvas id="%s"></canvas></div>' % (self.height-30, self.htmlId)
    return AresHtmlGraphFabric.Chart.html(self, self.strAttr(withId=False, pyClassNames=self.pyStyle), strChart)

  def to_word(self, document):
    # Will automatically add the external library to be able to use this module
    ares_plt = requires("matplotlib.pyplot", reason='Missing Package', install='matplotlib', autoImport=True, sourceScript=__file__)

    if self.__chart['type'] == '"pie"':
      timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
      aggDf = self.data.data.groupby([self.data.xAxis])[self.data.seriesNames[0]].sum().reset_index()
      fig1, ax1 = ares_plt.subplots()
      ax1.pie(aggDf[self.data.seriesNames[0]], labels=aggDf[self.data.xAxis], autopct='%1.1f%%', shadow=True, startangle=90)
      ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
      chartPath = os.path.join(self.aresObj.run.local_path, "saved", 'pictures', '%s_%s.png' % (self.aresObj._export['id'], timestamp) )
      fig1.savefig(chartPath, format='png')
      document.add_picture(chartPath)

  def to_xls(self, workbook, worksheet, cursor):
    """

    :param workbook:
    :param worksheet:
    :param cursor:
    :return:
    :link xlsxwriter Documentation: http://xlsxwriter.readthedocs.io/working_with_charts.html
    """
    labels = list(self.data.data[self.data.xAxis])
    sizes = list(self.data.data[self.data.seriesNames[0]])
    worksheet.write(cursor['row'], cursor['col'], self.data.xAxis)
    worksheet.write(cursor['row'], cursor['col'] + 1, self.data.seriesNames[0])
    cursor['row'] += 1
    startRow = cursor['row']
    for i, label in enumerate(labels):
      worksheet.write(cursor['row'], cursor['col'], label)
      worksheet.write(cursor['row'], cursor['col'] + 1, sizes[i])
      cursor['row'] += 1
    cursor['row'] += 1

    # Map only on the charts defined in the Python library
    chartType = self.__chart['type'].replace('"', '')
    chart = workbook.add_chart({'type': {"line": "line", "bar": "bar", "pie": "pie"}.get(chartType, 'line')})
    chart.add_series({
      'name': self.title,
      'categories': '=%s!$A$%s:$A$%s' % (worksheet.get_name(), startRow + 1, startRow + len(sizes)) ,
      'values': '=%s!$B$%s:$B$%s' % (worksheet.get_name(), startRow + 1, startRow + len(sizes)),
    })

    # Insert the chart into the worksheet.
    worksheet.insert_chart(startRow, cursor['col']+3, chart)


  # -----------------------------------------------------------------------------------------
  #                                    MARKDOWN SECTION
  # -----------------------------------------------------------------------------------------
  @classmethod
  def matchMarkDownBlock(cls, data): return True if data[0].strip().startswith( "---ChartJs" ) else None

  @staticmethod
  def matchEndBlock(data): return data.endswith("---")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj=None):
    """
    :category: Markdown
    :rubric: PY
    :example: Data structure recognised
      ---ChartJs:pie
      test|val
      a|12
      b|4
      c|2
      ---
    :dsc:
      onvert the markdown text to a valid aresObj item.
      In order to include it to a report it is necessary to pass the aresObj
    """
    headers = data[1].strip().split("|")
    records = []
    for line in data[2:-1]:
      rec, attr = {}, {}
      if line.startswith("@"):
        dataAttr = line[1:].strip().split(";")
        for d in dataAttr:
          a, b = d.split(":")
          attr[a] = b
        continue

      splitLine = line.replace(",", '.').strip().split("|")
      for i, val in enumerate( splitLine ):
        if i == 0:
          rec[headers[i]] = val
        else:
          rec[headers[i]] = float(val)
      records.append(rec)

    if aresObj is not None:
      p = aresObj.chart(data[0].split(":")[1].strip(), records, seriesNames=headers[1:], xAxis=headers[0])
      p.addAttr(attr, isPyData=False)
    return []

  def jsMarkDown(self): return ""
