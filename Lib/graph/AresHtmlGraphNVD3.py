#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


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

  chartOptions = {'showLegend': True, 'showLabels': True}
  """
  name, category, callFnc = 'NVD3', 'Charts', 'plotNVD3'
  references = {
    'WebSite': 'http://nvd3.org/',
    'Example': 'http://nvd3.org/examples/index.html',
    'NVD3 DiscreteBar': 'http://nvd3.org/examples/discreteBar.html',
    'NVD3 Event': 'https://stackoverflow.com/questions/17598694/how-to-add-a-click-event-on-nvd3-js-graph',
    'NVD3 Force Directed': 'http://krispo.github.io/angular-nvd3/#/forceDirectedGraph',
    'NVD3 Candle Chart': 'http://krispo.github.io/angular-nvd3/#/candlestickBarChart',
    'NVD3 Horizontal Bars': 'http://nvd3.org/examples/multiBarHorizontal.html',
    'NVD3 Example': 'http://python-nvd3.readthedocs.io/en/latest/classes-doc/multi-bar-horizontal-chart.html',
    'NVD3 Line': 'http://nvd3.org/examples/line.html',
    'NVD3 Multi Bars': 'http://nvd3.org/examples/multiBar.html',
    'NVD3 Pie': 'http://nvd3.org/examples/pie.html',
    'NVD3 Scatter': 'http://nvd3.org/examples/scatter.html',
    'NVD3 Stacked Area': 'http://nvd3.org/examples/stackedArea.html',
    'Repository': 'https://github.com/novus/nvd3',
    'Tips': 'https://www.webcomponents.org/element/saeidzebardast/nvd3-elements/elements/nvd3-pie#property-labelsOutside',
    'Application': 'https://bridge360blog.com/2016/03/07/adding-and-handling-click-events-for-nvd3-graph-elements-in-angular-applications/'
  }

  # Required external modules (javascript and CSS
  __reqCss, __reqJs = ['nvd3', 'datatables', 'datatables-export'], ['nvd3', 'datatables', 'datatables-export']
  __pyStyle = ['CssDivChart']

  def __init__(self, aresObj, chartType, data, width, widthUnit, height, heightUnit, title, chartOptions, toolsbar, htmlCode, globalFilter):
    if chartOptions is None:
      chartOptions = {}
    if chartType == 'bar' and len(data._schema['out']['params'][0]) > 1:
      chartType = 'multi-bar'
    super(Chart, self).__init__(aresObj, [], code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    if AresHtmlGraphFabric.CHARTS_FACTORY is None:
      AresHtmlGraphFabric.CHARTS_FACTORY = AresHtmlGraphFabric.loadFactory()  # atomic function to store all the different table mapping
    self.__chart = AresHtmlGraphFabric.CHARTS_FACTORY[self.name][chartType](aresObj, data, self.htmlId)
    self.__chart.data.attach(self)
    self.__chartJsEvents, self.chartType, self.jsDataFnc = {}, chartType, []
    self.setSeriesColor(aresObj.cssObj._charts)
    for label, val in chartOptions.items():
      if label == 'legend':
        if 'position' in val:
          self.addAttr("legendPosition", val['position'])
          del val['position']
          continue

      self.addAttr(label, val)
    self.css({'position': 'relative'})
    self.toolsbar, self.seriesProperties, self.title = toolsbar, {'static': {}, 'dynamic': {}}, title
    if htmlCode is not None and globalFilter is not None:
      self.aresObj.htmlCodes[htmlCode] = self
      if globalFilter is True:
        self.filter()
      else:
        self.filter(**globalFilter)


  # ---------------------------------------------------------------------------------------------------------
  #                                          PYTHON CONFIGURATION
  # ---------------------------------------------------------------------------------------------------------
  def addSeriesAttr(self, seriesId, data, dataType="dynamic"):
    """
    :category: Chart Series properties
    :rubric: PY
    :example: chartOjb.addSeriesAttr(0, {'shape': 'triangle-up', 'color': 'green', 'size': 4})
    :dsc:
      Add attributes to the selected series in the dataset. The series is defined by its index (number) starting from
      zeros in the dataset.
    :link NVD3 Example: http://nvd3.org/examples/scatter.html
    :return: The Python Chart Object
    """
    if 'shape' in data:
      shapes = ['circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square']
      if not data['shape'] in shapes:
        raise Exception("NVD3: %s does not exist" % data['shape'])

    self.seriesProperties[dataType].setdefault(seriesId, {}).update(data)
    self.__chart.data.post([('extend', self.seriesProperties, 'values')])
    return self

  def addAttr(self, key, val=None, category=None, isPyData=True):
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
        self.__chart.addAttr(k, v, category, isPyData=isPyData)
    else:
      self.__chart.addAttr(key, val, category, isPyData=isPyData)

  def delAttr(self, keys, category=None): self.__chart.delAttr(keys, category)

  def setSeriesColor(self, colors, seriesId=None):
    """
    :category: Chart Series colors
    :rubric: PY
    :type: Configuration
    :example: aresObj.cssObj.colorObj.getColors('#FFFFFF', '#008000', 10)
    :return: The Python Chart Object
    """
    if seriesId is None:
      self.addAttr({'color': colors})
    else:
      self.seriesProperties['dynamic'][seriesId] = {'color': colors}
      self.__chart.data.post([('extend', self.seriesProperties, 'values')])
    return self

  def addSeries(self, type, label, data, options=None, color=None):
    return self

  # -----------------------------------------------------------------------------------------
  #                                AXIS TRANSFORMATION
  # -----------------------------------------------------------------------------------------
  def format(self, formatType, axis, options=None, isPyData=False):
    format = dict(AxisDisplay.DISPLAYS[formatType] if formatType in AxisDisplay.DISPLAYS else formatType)
    if 'labelString' in format:
      del format['labelString']
    if options is None:
      options = {'digits': 0}
    if 'digits' not in options:
      options['digits'] = 0
    for key, val in format.items():
      val = val % options
      self.__chart.axis.setdefault(axis, {})[key] = val
    if formatType == 'MONTH':
      self.addGlobalVar("months", "['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']")
    if formatType == 'DAY':
      self.addGlobalVar("days", '["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]')
    return self

  def yFormat(self, formatType, options=None, isPyData=False): return self.format(formatType, 'yAxis', options, isPyData)
  def xFormat(self, formatType, options=None, isPyData=False): return self.format(formatType, 'xAxis', options, isPyData)
  def xAxisSort(self): self.jsDataFnc.append(self.__chart.xAxisSort(self.htmlId))


  # -----------------------------------------------------------------------------------------
  #                                STANDARD HTML METHODS
  # -----------------------------------------------------------------------------------------
  def onDocumentLoadVar(self): pass # Data should be registered externally
  def onDocumentLoadFnc(self): return True
  def onDocumentReady(self): self.aresObj.jsOnLoadFnc.add(self.jsGenerate(jsData=None))

  def style(self, seriesAttr=None, recAttr=None): self.__chart.style(seriesAttr, recAttr)

  def click(self, jsFnc):
    """
    :category: Chart Series
    :rubric: PY
    :type: Event
    :dsc:

    :return: The Python Chart Object
    """
    self.jsFrg('elementClick', jsFnc)
    return self


  # ---------------------------------------------------------------------------------------------------------
  #                                          JAVASCRIPT EVENTS
  # ---------------------------------------------------------------------------------------------------------
  def jsEvents(self):
    """
    :category: Chart Events
    :rubric: PY
    :type: System
    :dsc:

    """
    for eventKey, fnc in self.__chartJsEvents.items():
      self.aresObj.jsOnLoadEvtsFnc.add('''
        window['%(htmlId)s_chart'].%(eventObject)s.dispatch.on("%(eventKey)s", function (event) {
          if ( typeof event === 'undefined' ) { event = {data: {x: null, key: null, label: null, y: null} } ; } 
          var useAsync = false; var data = %(data)s ; var returnVal = undefined;
          if (!$('#body_loading').length){ 
            var bodyLoading2 = $('<div id="body_loading" name="ares_loading" style="bottom:20px;left:70px;position:fixed;background-color:#F4F4F4;padding:5px"><i class="fas fa-spinner fa-spin" style="margin-left:10px;margin-right:10px"></i><div style="display:inline" id="loading_count">0</div> process running...</div>') ; 
          } ;
          $('body').append(bodyLoading2) ;
          $('#loading_count').html( parseInt($('#loading_count').html()) + 1) ;
          %(jsFnc)s ; 
          if (!useAsync) {
            $('#loading_count').html( parseInt($('#loading_count').html()) - 1) ;
            if ($('#loading_count').html() == '0') { $('#body_loading').remove() ;} }
          if (returnVal != undefined) { return returnVal } ; 
        }) ;''' % {'htmlId': self.htmlId, 'htmlCode': self._code, 'eventObject': self.__chart.eventObject, 'eventKey': eventKey,
                   'data': self.__chart.jsQueryData, 'jsFnc': ";".join([f for f in fnc if f is not None]), "breadCrumVar": self.aresObj.jsGlobal.breadCrumVar})

  def jsFrg(self, typeEvent, jsFnc):
    if isinstance(jsFnc, list):
      self.__chartJsEvents.setdefault(typeEvent, []).extend(jsFnc)
    else:
      self.__chartJsEvents.setdefault(typeEvent, []).append(jsFnc)

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
      window['%(htmlId)s_chart'] = %(chartDef)s; var chartData = %(jsData)s;
      if (chartData[0].labels !== undefined) {
        window['%(htmlId)s_chart'].xAxis.tickFormat(function(d){return chartData[0].labels[d]});};
      d3.select($('#%(htmlId)s').get(0)).datum( chartData ).call(window['%(htmlId)s_chart']);
      d3.select($('#%(htmlId)s').get(0)).append("text").attr("x", $('#%(htmlId)s').width() /2).attr("y", 10).attr("text-anchor", "middle").style("font-weight", "bold").text("%(title)s"); 
      nv.utils.windowResize(window['%(htmlId)s_chart'].update); %(time)s    
      ''' % {'htmlId': self.htmlId, 'chartDef': self.__chart.toJs(), 'jsData': self.__chart.data.setId(jsData).getJs(),
             'time': AresHtmlGraphFabric.Chart.jsLastUpdate(self.htmlId), 'title': self.title}

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
    # TODO: Do the jsAddSeries implementation for NVD3
    print("!!!!!!!!!!!!!!!! Does not work for this chart yet !!!!!!!!!!!!!!!!")
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
      d3.select($('#%(htmlId)s').get(0)).datum( [ { key: "point", values: [{x:1, y:1}], color: "#334D6B" }] ).call(window['%(htmlId)s_chart']);nv.utils.windowResize(window['%(htmlId)s_chart'].update)
      ''' % {'htmlId': self.htmlId, 'jsData': jsData}

  def jsFlow(self, jsData='data', jsDataKey=None, isPyData=False):
    print("JsFLow not available with NVD3, please have a look at C3 instead")
    return ''

  def __str__(self):
    strChart = '<svg id="%s"></svg>' % self.htmlId
    return AresHtmlGraphFabric.Chart.html(self, self.strAttr(withId=False, pyClassNames=self.pyStyle), strChart)

  # -----------------------------------------------------------------------------------------
  #                                    MARKDOWN SECTION
  # -----------------------------------------------------------------------------------------
  @classmethod
  def matchMarkDownBlock(cls, data): return True if data[0].strip().startswith( "---NVD3" ) else None

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
      records.append( rec )

    if aresObj is not None:
      p = aresObj.chart(data[0].split(":")[1].strip(), records, seriesNames=headers[1:], xAxis=headers[0], chartFamily='NVD3')
      p.addAttr(attr, isPyData=False)
    return []

  def jsMarkDown(self): return ""


  def filter(self, aresDf=None, colName=None, caseSensitive=False, multiVals=False, exactMath=False, allSelected=True, filterGrp=None):
    if self._code is None:
      self._code = "default_data_%s" % id(self)
      self.aresObj.htmlCodes[self._code] = self
    self.click('''
      if ( '%(htmlCode)s' != 'None' ) {
        if(%(breadCrumVar)s['params']['%(htmlCode)s'] == data['label']) { %(breadCrumVar)s['params']['%(htmlCode)s'] = null ; }
        else {  %(breadCrumVar)s['params']['%(htmlCode)s'] = data['label']; } }
      ''' % {"htmlId": self.htmlId, "htmlCode": self._code, "breadCrumVar": self.aresObj.jsGlobal.breadCrumVar})
    if aresDf is None:
      aresDf = self.data.data
    if colName is None:
      colName = self.data.xAxis
    strFilter = ["( aresObj('%s') == rec['%s'] )" % (self._code, colName)]
    if allSelected:
      strFilter.append("( aresObj('%s') == null)" % self._code)
    aresDf.link("elementClick", self._code, " || ".join(strFilter), filterGrp if filterGrp is not None else "filter_%s" % aresDf.htmlCode, colNames=[colName])
    return self