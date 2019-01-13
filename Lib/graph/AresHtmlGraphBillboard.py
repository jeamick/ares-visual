#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

'''
Module used as a wrapper to the Javascript C3 libraries
reference website: http://c3js.org/

This module is defined by a main class ** Chart **.

The constructor ::__init__
::onDocumentLoadVar
::onDocumentReady


Python / Javascript Events
::click
::mouseover
::mouseout


Pure Javascript Wrapper
Those function will be only used in **Javascript called** and they will return a piece of string which will be added in the
report to get the data later on in the Javascript layer. Python is just used here to put all the pieces together

The method to destroy the C3 chart ::jsDestroy
The method to group the different charts ::jsGroups

'''


import json

from ares.Lib.html import AresHtml
from ares.Lib.graph import AxisDisplay
from ares.Lib.graph import AresHtmlGraphFabric


DSC = {
  'eng': '''

'''
}


class Chart(AresHtml.Html):
  """
  :category: Chart Interface
  :rubric: PY
  :dsc:

  :link C3 Get Started: https://c3js.org/gettingstarted.html
  """
  name, category, callFnc = 'Billboard', 'Charts', 'plotBillboard'
  references = {'Repository': 'https://github.com/c3js/c3',
                'Pie': 'http://c3js.org/samples/chart_bar.html',
                'Donut': 'http://c3js.org/samples/chart_donut.html',
                'Area': 'http://c3js.org/samples/chart_area.html',
                'Line': 'http://c3js.org/samples/point_show.html',
                'Scatter': 'http://c3js.org/samples/chart_scatter.html',
                'Gauge': 'http://c3js.org/samples/chart_gauge.html',
                'References': 'http://c3js.org/reference.html'}
  __reqCss, __reqJs = ['billboard'], ['billboard']
  __pyStyle = ['CssDivChart']

  def __init__(self, aresObj, chartType, data, width, widthUnit, height, heightUnit, title, chartOptions, toolsbar, htmlCode, globalFilter):
    self.toolsbar, self.seriesProperties, self.__chartJsEvents, self.height = toolsbar, {'static': {}, 'dynamic': {}}, {}, height
    if AresHtmlGraphFabric.CHARTS_FACTORY is None:
      AresHtmlGraphFabric.CHARTS_FACTORY = AresHtmlGraphFabric.loadFactory() # atomic function to store all the different table mapping
    super(Chart, self).__init__(aresObj, [], code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.__chart = AresHtmlGraphFabric.CHARTS_FACTORY[self.name][chartType](aresObj, data, self.seriesProperties)
    if chartOptions is not None:
      resolvedOptions = {}
      self.__chart.rAttr(chartOptions, resolvedOptions)
      self.__chart.update(resolvedOptions)
    self.__chart.data.attach(self)
    self.__chart['bindto'] = "'#%s_div'" % self.htmlId
    self.css({'padding': '5px', 'position': 'relative'})
    if title:
      self.addAttr('text', title, 'title')
    self.setSeriesColor(aresObj.cssObj._charts)
    if globalFilter is not None:
      if self._code is None:
        raise Exception("ERROR: C3 - %s -  Please add an htmlCode to name your filter" % chartType)

      if globalFilter is True:
        self.filter(data._jqId, list(self.__chart.data._schema['keys'])[0])
      else:
        self.filter(**globalFilter)
      self.jsFrg("onclick", '''
        if(%(breadCrumVar)s['params']['%(htmlCode)s'] == data.name){%(breadCrumVar)s['params']['%(htmlCode)s'] = ''}
        else{%(breadCrumVar)s['params']['%(htmlCode)s'] = data.name}''' % {'htmlCode': self._code, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar})

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
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {'allIfEmpty': set()})[colAlias] = val
      self.aresObj.jsSources.setdefault(jsId, {})['filters']['allIfEmpty'].add(colAlias)
    else:
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {})[colAlias] = val
    self.aresObj.jsSources.setdefault(jsId, {})['filters'].setdefault('_colsMaps', {})[colAlias] = colName
    return self

  def onDocumentLoadVar(self): pass
  def onDocumentLoadFnc(self): return True

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    self.ctx = []  # Just to ensure that the Structure of the chart component will not be changed in the python layer
    for event, fnc in self.__chartJsEvents.items():
      self.addAttr(event, "function (event, i) { var data = %s; %s }" % (fnc['data'], ";".join(fnc['js'])), 'data', isPyData=False)
    AresHtmlGraphFabric.Chart.resolveDict(dict([(key, val) for key, val in self.__chart.items() if val]), self.ctx)
    self.aresObj.jsOnLoadFnc.add('''
      window['%(htmlId)s_def'] = {%(chartDef)s}; %(jsChart)s
      ''' % {'htmlId': self.htmlId, 'chartDef': ", ".join(self.ctx), 'jsChart': self.jsGenerate(jsData=None)})


  # ---------------------------------------------------------------------------------------------------------
  #                                          JAVASCRIPT EVENTS
  # ---------------------------------------------------------------------------------------------------------
  def jsGenerate(self, jsData='data', jsDataKey=None, isPyData=False, jsId=None):
    """
    :category: Chart Re Build
    :rubric: JS
    :type: System
    :dsc:
      Generate (or re build) the chart.
    :return: The Javascript event as a String
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
      if(window['%(htmlId)s_chart'] === undefined){
        window['%(htmlId)s_def'].data.columns = %(jsData)s; 
        window['%(htmlId)s_chart'] = bb.generate(window['%(htmlId)s_def'])}
      else {window['%(htmlId)s_chart'].unload();window['%(htmlId)s_chart'].load({columns: %(jsData)s})}; %(time)s
      ''' % {'htmlId': self.htmlId, 'jsData': self.__chart.data.setId(jsData).getJs(),
             'time': AresHtmlGraphFabric.Chart.jsLastUpdate(self.htmlId)}

  def jsFlow(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Chart Update
    :rubric: JS
    :type: Event
    :example: chartObj.jsFlow({"columns": [['x', 'Test'], ['value', 2000], ['value2', 4000]], 'length': 0}
    :example: chartObj.jsFlow({"columns": [['x', '2017-02-18'], ['AAPL.Open', 150], ['AAPL.Low', 150]], 'length': 0}
    :dsc:
      Add new records to the charts for the defined series
    :return: The Javascript event as a String
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return "window['%(htmlId)s_chart'].flow(%(jsData)s)" % {'htmlId': self.htmlId, 'jsData': jsData}

  def jsDelSeries(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Chart Update
    :rubric: JS
    :type: Event
    :example: chartObj.jsDelSeries(['AAPL.Open'], isPyData=True)
    :dsc:
      Delete the series in the chart. Series should be defined based on the name.
    :return: The Javascript event as a String
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
      if(%(jsData)s != null){%(jsData)s.forEach(function(series){window['%(htmlId)s_chart'].unload({ ids: series })})} 
      else {window['%(htmlId)s_chart'].load({unload: true});}''' % {'jsData': jsData, 'htmlId': self.htmlId}

  def jsAddSeries(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Chart Update
    :rubric: JS
    :type: Event
    :example: chartObj.jsAddSeries(['AAPL.Open'], isPyData=True)
    :dsc:
      Add a new series in the chart. Series should be defined based on the name.
    :link Documentation: https://c3js.org/samples/data_load.html
    :return: The Javascript event as a String
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
      var newSeries = %(series)s;
      if(Array.isArray(newSeries)){
        records = {columns: []}; newSeries.forEach(function(s){records.push([s.label].concat(newSeries.data))
        window['%(htmlId)s_chart'].load(records)})}
      else{window['%(htmlId)s_chart'].load({columns: [['x'].concat(newSeries.x), [newSeries.label].concat(newSeries.y)] })}
      ''' % { 'htmlId': self.htmlId, 'series': jsData }

  def setType(self, htmlObj):
    """
    :category: Chart Type
    :rubric: JS
    :type: Configuration
    :dsc:
      Put a type based on the value of ARes component
    :return: The Python Chart object
    """
    self.addAttr("type", htmlObj.val, category='data', isPyData=False)
    return self

  def jsDestroy(self): return "window['%s_chart'].destroy()" % self.htmlId

  def jsTranform(self, jsData='data', jsDataKey=None, isPyData=False, seriesId=None):
    """
    :category: Chart Update
    :type: JS
    :rubric: Event
    :example:
      s = aresObj.select(['pie', 'scatter'])
      aresObj.button("Button").click(chartObj.jsTranform(s.val))
    :dsc:
      Change the style of a chart
    :return: The Javascript event as a String
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    if seriesId is not None:
      return "window['%(htmlId)s_chart'].transform(%(jsChartType)s, '%(id)s')" % {'htmlId': self.htmlId, 'jsChartType': jsData, 'id': seriesId}

    return "window['%(htmlId)s_chart'].transform(%(jsChartType)s)" % {'htmlId': self.htmlId, 'jsChartType': jsData}


  # ---------------------------------------------------------------------------------------------------------
  #                                          JAVASCRIPT EVENTS
  # ---------------------------------------------------------------------------------------------------------
  def addAttr(self, key, val=None, subCategory=None, category=None, isPyData=True):
    """
    :category: Chart Bespoke Definition
    :type: PY
    :rubric: Configuration
    :dsc:
      Add attributes to the Python chart definition. Python will construct a dictionary with all the settings
      related to this charting libraries. At the end it will create the corresponding Javascript Chart object to let
      the javascript take the control.
    :return: The Python Chart object
    """
    if isinstance(key, dict):
      for k, v in key.items():
        self.__chart.addAttr(k, v, subCategory, category, isPyData)
    else:
      if key == 'regions' and not isinstance(val, list):
        val = [val]
      self.__chart.addAttr(key, val, subCategory, category, isPyData)

  def delAttr(self, keys, subCategory=None, category=None): self.__chart.delAttr(keys, subCategory, category)

  def addSeriesAttr(self, seriesId, data, dataType=None):
    """
    :category: Chart Series properties
    :rubric: PY
    :example: chartOjb.addSeriesAttr(0, {'hoverinfo': 'none', 'type': 'scatter'})
    :dsc:
      Add attributes to the selected series in the dataset. The series is defined by its index (number) starting from
      zeros in the dataset.
    :link C3 Documentation: https://plot.ly/javascript/bar-charts/
    :return: The Python Chart Object
    """
    if seriesId is not None:
      for cat, attr in data.items():
        if isinstance(attr, dict):
          for key, val in attr.items():
            self.addAttr(key, val , json.dumps(seriesId), category=cat)
        else:
          # This will ensure C3 to be compatible with ChartJs settings
          if cat == 'backgroundColor':
            self.addAttr(list(self.__chart.data._schema['values'])[seriesId], attr, 'colors', category='data')
    return self

  def setSeriesColor(self, colors, seriesId=None):
    """
    :category: Chart Series Settings
    :rubric: JS
    :type: Configuration
    :example: chartOjb.setSeriesColor('yellow', 'value2')
    :dsc:
      Change the default color of a series in the chart
    :link Billboard Example: https://c3js.org/samples/data_color.html
    :return: The Python Chart Object
    """
    if seriesId is None:
      self.addAttr('pattern', colors, 'color')
    else:
      self.addAttr(seriesId, colors, 'colors', 'data')
    return self

  def jsGroups(self, seriesId): self.addAttr("groups", seriesId)
  def groupToolTips(self, flag): self.addAttr("grouped", flag, 'tooltip')
  def seriesNames(self, namesMap):  self.addAttr("names", namesMap, 'data')
  def seriesGroups(self, groups): self.addAttr("groups", groups, 'data')
  def seriesOrder(self, order): self.addAttr("order", order, 'data')
  def showLabels(self, flag): self.addAttr("labels", flag, 'data')

  def addGridLine(self, axis, value, text, position='end', cssClass=None):
    if cssClass is not None:
      self.addPyCss(cssClass)
      cssClass = "py_%s" % cssClass.lower
    self.__chart.setdefault('grid', {}).setdefault(axis, {}).setdefault('lines', []).append(
      '{value: %s, text: "%s", position: "%s", "class": "%s"}' % (value, text, position, cssClass) )

  def addRegion(self, axis, start, end, cssClass=None):
    if cssClass is not None:
      self.addPyCss(cssClass)
      cssClass = "py_%s" % cssClass.lower
    self.__chart['regions'].append('{axis: "%s", start: %s, end: %s, "class": "%s"}' % (axis, start, end, cssClass))

  def axisFormat(self, axis, formatType, formatDefinition=None):
    if axis not in self.__chart['axis']:
      self.__chart['axis'][axis] = {}
    if formatType == 'timeseries':
      self.addAttr("type", formatType, axis, 'axis')
      # for example '%Y-%m-%d %H:%M:%S' or '%Y-%m-%d'
      self.addAttr("tick", {'format': formatDefinition}, axis, 'axis')

  def yFormat(self, formatType, options=None, isPyData=False):
    if options is None:
      options = {'digits': 0}
    if 'digits' not in options:
      options['digits'] = 0
    self.addAttr("tick", "{'format': %s}" % AxisDisplay.DISPLAYS.get(formatType, {'tickFormat': formatType})['tickFormat'] % options, 'y', 'axis', isPyData=isPyData)


  # -----------------------------------------------------------------------------------------
  #                                STANDARD CHART EVENTS
  # -----------------------------------------------------------------------------------------
  def jsFrg(self, typeEvent, jsFnc, jsData="{'event_index': event.index, 'labels': event.x, 'value': event.value, 'name': event.name, 'label': this.categories()[event.index]}"):
    if not typeEvent in self.__chartJsEvents:
      self.__chartJsEvents[typeEvent] = {"data": jsData, 'js': []}
    if isinstance(jsFnc, list):
      self.__chartJsEvents[typeEvent]['js'].extend(jsFnc)
    else:
      self.__chartJsEvents[typeEvent]['js'].append(jsFnc)

  def mouseover(self, jsFnc): self.jsFrg('onmouseover', jsFnc)
  def mouseout(self, jsFnc): self.jsFrg('onmouseout', jsFnc)

  def click(self, jsFncs):
    self.jsFrg("onclick", jsFncs)
    return self

  def __str__(self):
    strChart = '<div id="%s_div" style="height:%spx"></div>' % (self.htmlId, self.height - 30)
    return AresHtmlGraphFabric.Chart.html(self, self.strAttr(withId=False, pyClassNames=self.pyStyle), strChart)

  # -----------------------------------------------------------------------------------------
  #                                    MARKDOWN SECTION
  # -----------------------------------------------------------------------------------------
  @classmethod
  def matchMarkDownBlock(cls, data): return True if data[0].strip().startswith( "---Billboard" ) else None

  @staticmethod
  def matchEndBlock(data): return data.endswith("---")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj=None):
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
      p = aresObj.chart(data[0].split(":")[1].strip(), records, seriesNames=headers[1:], xAxis=headers[0], chartFamily='Billboard')
      p.addAttr(attr, isPyData=False)
    return ["aresObj.chart('pie', '%s', chartFamily='Billboard')" % (data[2:-1])]

  def jsMarkDown(self): return ""
