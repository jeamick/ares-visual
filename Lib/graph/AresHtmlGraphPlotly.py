#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json

from ares.Lib.html import AresHtml
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
    Standard Charting interface to wrap the Plotly.js module.
  :link Plotly Documentation: https://plot.ly/javascript/plotlyjs-function-reference/#common-parameters

  chartOptions = {'showGrid': False, 'showLabels': True, 'zoom': False, 'legend': {'position': 'bottom'} }
  """
  name, category, callFnc = 'Plotly', 'Charts', 'plotly'
  __reqJs = ['plotly']
  __pyStyle = ['CssDivChart']

  def __init__(self, aresObj, chartType, data, width, widthUnit, height, heightUnit, title, chartOptions, toolsbar, htmlCode, globalFilter):
    if chartOptions is None:
      chartOptions = {}
    super(Chart, self).__init__(aresObj, [], width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, code=htmlCode)
    self._layout, self.options, self.seriesProperties = {}, {"displaylogo": False, 'responsive': True, 'autosize': True}, {'static': {}, 'dynamic': {}}
    self.toolsbar, self.height = toolsbar, height
    if AresHtmlGraphFabric.CHARTS_FACTORY is None:
      AresHtmlGraphFabric.CHARTS_FACTORY = AresHtmlGraphFabric.loadFactory()  # atomic function to store all the different table mapping
    self.__chart = AresHtmlGraphFabric.CHARTS_FACTORY[self.name][chartType](aresObj, data, self.seriesProperties)
    if self.__chart.jsType is not None:
      # Simple remapping to be able to reuse existing transformation functions for new chart configurations
      # This will allow the creation of dynamic configurations based on existing charts
      data._schema['out']['config'] = data._schema['out']['name']
      data._schema['out']['name'] = "%s_%s" % (data._schema['out']['family'], self.__chart.jsType.replace("-", ""))
    self.__chart.data.attach(self)
    if not 'type' in self.seriesProperties['static']:
      self.seriesProperties['static']['type'] = self.__chart._attrs.get('type', getattr(self.__chart, 'chartObj', None))
    self.addLayout({"xaxis": {"showgrid": chartOptions.get("showGrid", False), 'showline': chartOptions.get("showGrid", False)},
                    "yaxis": {"showgrid": chartOptions.get("showGrid", False), 'showline': chartOptions.get("showGrid", False)}} )
    self.addLayout({"showlegend": chartOptions.get("showLabels", True)})
    self.setSeriesColor(aresObj.cssObj._charts)
    if title is not None:
      self.addLayout({"title": title})
    if self.__chart._layout is not None:
      self.addLayout(self.__chart._layout)
    if chartOptions is not None and 'legend' in chartOptions:
      if chartOptions['legend'].get('position') == 'bottom':
        self.addLayout({"legend": {"orientation": "h"}})
    self.addLayout({"xaxis": {"fixedrange": chartOptions.get("zoom", False)}, "yaxis": {"fixedrange": chartOptions.get("zoom", False)}})
    if htmlCode is not None and globalFilter is not None:
      if globalFilter is True:
        self.filter(data._jqId, list(self.__chart.data._schema['keys'])[0])
      else:
        self.filter(**globalFilter)
      self.click('''
        if(%(breadCrumVar)s['params']['%(htmlCode)s'] == data.name){%(breadCrumVar)s['params']['%(htmlCode)s'] = ''}
        else{%(breadCrumVar)s['params']['%(htmlCode)s'] = data.name}
        ''' % {'htmlCode': self._code, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar})

  def onDocumentLoadFnc(self): return True
  def onDocumentReady(self):
    self.aresObj.jsOnLoadFnc.add(
    ''' 
    %(jsChart)s; 
    ''' % {'jsChart': self.jsGenerate(jsData=None), 'htmlId': self.htmlId} )

  @property
  def eventId(self): return "document.getElementById('%s')" % self.htmlId

  @property
  def jsQueryData(self): return "{event_val: event.points[0].value, name: event.points[0].label, event_code: '%s' }" % self.htmlId

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
    if allSelected:
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {'allIfEmpty': []})[colName] = val
      self.aresObj.jsSources.setdefault(jsId, {})['filters']['allIfEmpty'].append(colName)
    else:
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {})[colName] = val
    return self

  # ---------------------------------------------------------------------------------------------------------
  #                                          JAVASCRIPT EVENTS
  # ---------------------------------------------------------------------------------------------------------
  def jsUpdateChart(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Chart Update
    :rubric: JS
    :type: Event
    :dsc:
      Update the chart following an event
    :link Plotly Documentation: https://plot.ly/javascript/plotlyjs-function-reference/#plotlyupdate
    :return:
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return "Plotly.update('%(htmlId)s', %(jsData)s, {});" % {'htmlId': self.htmlId,
                    'jsData': self.__chart.data.setId(jsData).getJs([('extend', self.seriesProperties)])}

  def jsDestroy(self): return "Plotly.purge('%s')" % self.htmlId

  def jsRefreshSeries(self, jsData='data', jsDataSeriesNames=None, jsDataKey=None, isPyData=False):
    """
    :cqtegory:
    :rubric:
    :type:
    :dsc:

    """
    a = self.jsDelSeries(jsData=jsData, jsDataKey=jsDataSeriesNames, isPyData=isPyData)
    b = self.jsAddSeries(jsData=jsData, jsDataKey=jsDataKey, isPyData=isPyData)
    return ";".join([a, b])

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

  def jsDelSeries(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Chart Series
    :rubric: JS
    :type: Event
    :dsc:
      Remove the new series to the chart.
    :return: The Javascript string to remove the selected series (based on the ID)
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
      var seriesIds = [] ;
      %(seriesNames)s.forEach(function(series, i){if(%(jsData)s.indexOf(series) > -1 ){seriesIds.push(i)}});
      Plotly.deleteTraces('%(htmlId)s', seriesIds);''' % {'htmlId': self.htmlId, "jsData": jsData,
        'seriesNames': json.dumps(self.__chart.data._schema['out']['params'][0])}

  def jsAddSeries(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Chart Series
    :rubric: JS
    :type: Event
    :example: chartObj.jsAddSeries( {y: [5000, null], x: ['Serie1', 'Serie2'], type: 'bar'} )
    :dsc:
      Add the new series to the chart.
    :return: The Javascript string to add the new series
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
      var newSeries = %(jsData)s;
      if(Array.isArray(newSeries)){}
      else{newSeries.name = newSeries.label; Plotly.addTraces('%(htmlId)s', [newSeries])}
      ''' % {'htmlId': self.htmlId, "jsData": jsData}

  def jsFlow(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Chart Series
    :type: Update
    :rubric: JS
    :example: chartObj.jsFlow({"columns": [['x', 'Test'], ['value', 2000], ['value2', 4000]], 'length': 0}
    :dsc:

    :return: The Javascript event as a String
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return "Plotly.extendTraces('%(htmlId)s', %(jsData)s, [0]);" % {'htmlId': self.htmlId, "jsData": jsData}

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
        window['%(htmlId)s_chart'] = Plotly.newPlot('%(htmlId)s', %(jsData)s, %(jsLayout)s, %(options)s)}
      else { window['%(htmlId)s_chart'] = Plotly.react('%(htmlId)s', %(jsData)s, %(jsLayout)s, %(options)s) } ; %(time)s
      ''' % {'htmlId': self.htmlId, 'jsData': self.__chart.data.setId(jsData).getJs([('extend', self.seriesProperties)]),
             'jsLayout': json.dumps(self._layout), 'options': json.dumps(self.options),
             'time': AresHtmlGraphFabric.Chart.jsLastUpdate(self.htmlId)}


  # ---------------------------------------------------------------------------------------------------------
  #                                          PYTHON CONFIGURATION
  # ---------------------------------------------------------------------------------------------------------
  def axis(self, typeAxis, title=None, type=None):
    """
    :category: Chart Re Build
    :rubric: JS
    :type: Configuration
    :dsc:
        Change the usual axis parameters of the chart.
    :link Plotly Documentation: https://plot.ly/javascript/reference/#layout-xaxis-type
    :return: The Python Chart Object
    """
    if title is not None:
      self.addLayout({"%saxis" % typeAxis: {"title": title}})
    if type is not None:
      self.addLayout({"%saxis" % typeAxis: {"type": type}})
    return self

  def yFormat(self, formatFnc, label=None, options=None, isPyData=False):
    """ No need to use this function plotly will format automatically the axis """
    return self

  def xFormat(self, formatFnc, label=None, options=None, isPyData=False):
    """ No need to use this function plotly will format automatically the axis """
    return self

  def addSeries(self, type, label, data, options=None, color=None):
    """
    :category:
    :rubric: JS
    :example:
    :dsc:

      Plotly.addTraces(graphDiv, {y: [1, 5, 7]}, 0);
    :return: The Python Chart Object
    """
    if options is None:
      options = {}
    seriesIndex = len(self.__chart.data._schema['values'])
    self.__chart.data._data[label] = data
    self.__chart.data._schema['values'].add(label)
    self.__chart.data._schema['fncs'][0]['args'][1].append(label)
    self.seriesProperties['dynamic'][seriesIndex] = options
    return self

  def addAttr(self, key, val=None, tree=None, category=None, isPyData=True):
    """
    :category:
    :rubric: JS
    :type: Configuration
    :example:
    :dsc:

    :return: The Python Chart Object
    """
    return self

  def addSeriesAttr(self, seriesId, data, dataType="dynamic"):
    """
    :category: Chart Series properties
    :rubric: PY
    :example: chartOjb.addSeriesAttr(0, {'hoverinfo': 'none', 'type': 'scatter'})
    :dsc:
      Add attributes to the selected series in the dataset. The series is defined by its index (number) starting from
      zeros in the dataset.
    :link Plotly Documentation: https://plot.ly/javascript/bar-charts/
    :return: The Python Chart Object
    """
    self.__chart.seriesProperties[dataType].setdefault(seriesId, {}).update(data)
    return self

  def setSeriesColor(self, colors, seriesIds=None):
    """
    :category: Chart Series colors
    :rubric: PY
    :type: Configuration
    :example: aresObj.cssObj.colorObj.getColors('#FFFFFF', '#008000', 10)
    :return: The Python Chart Object
    """
    self.__chart._colors(colors, seriesIds)
    return self

  def addLayout(self, data):
    """

    :example: chartOjb.addLayout( {'barmode': 'stack'} )
    """
    self._layout.update(data)
    return self

  def click(self, jsFncs):
    """
    :category:
    :rubric: JS
    :type: Events
    :dsc:

    :link Plotly Documentation: https://plot.ly/javascript/plotlyjs-events/
    """
    self.jsFrg('plotly_click', jsFncs)
    return self

  def __str__(self):
    """
    :category: Container Representation
    :rubric: HTML
    :type: Output
    :dsc:
      Return the component HTML display. No use of the features in the function htmlContainer() for this Chart as Plotly is providing
      already most of the features. So for those charts the display of the events might slightly different from the other charts.
    :return: The HTML string to be added to the template.
    """
    strChart = '<div id="%(htmlId)s" style="height:%(height)spx"></div>' % {'height': self.height - 30, 'htmlId': self.htmlId}
    return AresHtmlGraphFabric.Chart.html(self, self.strAttr(withId=False, pyClassNames=self.pyStyle), strChart)


  # ---------------------------------------------------------------------------------------------------------
  #                                          MARKDOWN SECTION
  # ---------------------------------------------------------------------------------------------------------
  @classmethod
  def matchMarkDownBlock(cls, data):
    return True if data[0].strip().startswith("---Plotly") else None

  @staticmethod
  def matchEndBlock(data):
    return data.endswith("---")

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
      for i, val in enumerate(splitLine):
        if i == 0:
          rec[headers[i]] = val
        else:
          rec[headers[i]] = float(val)
      records.append(rec)

    if aresObj is not None:
      p = aresObj.chart(data[0].split(":")[1].strip(), records, seriesNames=headers[1:], xAxis=headers[0], chartFamily='Plottly')
      p.addAttr(attr, isPyData=False)
    return []
