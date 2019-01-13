#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json

from ares.Lib.graph import AresHtmlGraphFabric
from ares.Lib.html import AresHtml


DSC = {
  'eng': '''

'''
}


class Chart(AresHtml.Html):
  """

  """
  name, category, callFnc = 'Vis', 'Charts', 'plotChartVis'
  references = {
    'Website': 'http://visjs.org/',
    'Documentation': 'http://visjs.org/network_examples.html'
  }
  __reqJs, __reqCss = ['vis', 'datatables', 'datatables-export'], ['vis', 'datatables', 'datatables-export']
  __pyStyle = ['CssDivChart']

  def __init__(self, aresObj, chartType, data, width, widthUnit, height, heightUnit, title, chartOptions, toolsbar, htmlCode, globalFilter):
    self.seriesProperties, self.height, self._groups, self.__edges = {'static': {}, 'dynamic': {}}, height, None, None
    if AresHtmlGraphFabric.CHARTS_FACTORY is None:
      AresHtmlGraphFabric.CHARTS_FACTORY = AresHtmlGraphFabric.loadFactory()  # atomic function to store all the different table mapping
    super(Chart, self).__init__(aresObj, data, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, code=htmlCode)
    self.__chart = AresHtmlGraphFabric.CHARTS_FACTORY[self.name][chartType](aresObj, data, self.seriesProperties)
    if self.__chart.jsType is not None:
      # Simple remapping to be able to reuse existing transformation functions for new chart configurations
      # This will allow the creation of dynamic configurations based on existing charts
      self.__chart.jsCls = AresHtmlGraphFabric.CHARTS_FACTORY[self.name][self.__chart.jsType].jsCls
      self.__chart.data._schema['out']['config'] = self.__chart.data._schema['out']['name']
      self.__chart.data._schema['out']['name'] = "%s_%s" % (self.__chart.data._schema['out']['family'], self.__chart.jsType.replace("-", ""))
    self.__chart.data.attach(self)
    self.toolsbar, self.title = toolsbar, title
    self.__chart["height"] = "'%spx'" % (self.height - 50 if title else self.height - 30)

  @property
  def jsQueryData(self): return self.__chart.jsQueryData
  @property
  def eventId(self): return "window['%s_chart']" % self.htmlId

  def onDocumentLoadVar(self): pass
  def onDocumentLoadFnc(self): return True

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    self.ctx = []  # Just to ensure that the Structure of the chart component will not be changed in the python layer
    AresHtmlGraphFabric.Chart.resolveDict(dict([(key, val) for key, val in self.__chart.items() if val]), self.ctx)
    self.aresObj.jsOnLoadFnc.add('''
      window['%(htmlId)s_options'] = {%(options)s}; %(jsChart)s;
      ''' % {'jsChart': self.jsGenerate(jsData=None), 'htmlId': self.htmlId, 'options': ", ".join(self.ctx)})


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
      window['%(htmlId)s_data'] = new vis.DataSet(%(chartData)s);
      if(window['%(htmlId)s_chart'] === undefined){
        window['%(htmlId)s_edges'] = %(edges)s;
        if (window['%(htmlId)s_edges'] == undefined){
          window['%(htmlId)s_chart'] = new vis.%(chartObj)s($("#%(htmlId)s").get(0), window['%(htmlId)s_data'], window['%(htmlId)s_options'])}
        else{
          window['%(htmlId)s_chart'] = new vis.%(chartObj)s($("#%(htmlId)s").get(0), {nodes: window['%(htmlId)s_data'], edges: window['%(htmlId)s_edges']}, window['%(htmlId)s_options'])
        };
        %(groups)s}
      else {window['%(htmlId)s_chart'].setItems(window['%(htmlId)s_data'])}
      ''' % {'htmlId': self.htmlId,
             'groups': "window['%s_chart'].setGroups(%s)" % (self.htmlId, json.dumps(self._groups)) if self._groups is not None else '',
             'chartData': self.__chart.data.setId(jsData).getJs([('extend', self.seriesProperties)]),
             'chartObj': self.__chart.jsCls, 'edges': json.dumps(self.__edges)}

  def addAttr(self, key, val=None, tree=None, category=None, isPyData=True):
    """
    :category:
    :rubric: JS
    :type: Configuration
    :example: chartObj.addAttr('style', 'circle', category='drawPoints')
    :example: chartObj.addAttr('visible', False, category='dataAxis')
    :dsc:
      Update the Chart Options.
      All the details of the possible parameters are defined in the docs in the Vis.js official website.
      Please have a look to check the properties.
      For example for a 2D charts the below options are defined [here](http://visjs.org/docs/graph2d/)
    :return: The Python Chart Object
    """
    if category is not None:
      if not category in self.__chart._attrs:
        self.__chart[category] = {}
      if isinstance(key, dict):
        self.__chart[category].update(key)
      else:
        self.__chart[category][key] = val
    else:
      if isinstance(key, dict):
        self.__chart.update(key)
      else:
        self.__chart[key] = val
    return self

  def jsAddPoints(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Chart Series Update
    :rubric: JS
    :type: Configuration
    :example: htmlObj.click( ["data = [{x:'2014-06-14', y: 34}]", c.jsAddPoints()])
    :dsc:

    :return: The String of the Javascript event
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return "window['%(htmlId)s_data'].add(%(jsData)s)" % {'htmlId': self.htmlId,
        'jsData': self.__chart.data.setId(jsData).getJs([('extend', self.seriesProperties)])}

  def jsAddSeries(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Chart Series Update
    :rubric: JS
    :type: Configuration
    :example: click( ["data = [{x:'2014-06-14', y: 34, group: 3}, {x:'2014-06-11', y: 34, group: 3}]", c.jsAddSeries()])
    :dsc:
      Add a brand new series to the chart.
      The data structure of this new series should directly fit the Vis chart requirement to be correctly added
    :return: The String of the Javascript event
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return "window['%(htmlId)s_data'].add(%(jsData)s)" % {'htmlId': self.htmlId, 'jsData': jsData}

  def setType(self, htmlObj):
    """
    :category: Chart Type
    :rubric: JS
    :type: Configuration
    :dsc:
      Put a type based on the value of ARes component
    :return: The Python Chart object
    """
    self.addAttr("style", htmlObj.val, isPyData=False)
    return self

  def groups(self, groupInfo):
    """
    :category: Chart Groups Definition
    :rubric: JS
    :type: Configuration
    :dsc:
      For some charts this function will allow the creation of groups.
      This does not work with all type of charts, please have a look at the Vis online documentation for more details
      about this option
    :return: The Python Chart object
    """
    self._groups = groupInfo
    return self

  def edges(self, edgesInfo):
    """
    :category: Chart Groups Definition
    :rubric: JS
    :type: Configuration
    :dsc:
      only available for network charts.
    :return: The Python Chart object
    """
    if self.__chart.jsCls != 'Network':
      raise Exception("This property is only available for Network Charts to set the edges between nodes")

    self.__edges = edgesInfo
    return self

  # ---------------------------------------------------------------------------------------------------------
  #                                          PYTHON CONFIGURATION
  # ---------------------------------------------------------------------------------------------------------
  def axis(self, typeAxis, title=None, type=None): pass
  def yFormat(self, formatFnc, label=None, options=None, isPyData=False): pass
  def xormat(self, formatFnc, label=None, options=None, isPyData=False): pass

  def addSeriesAttr(self, seriesId, data, dataType="dynamic"):
    if dataType == 'static':
      self.__chart.seriesProperties[dataType].update(data)
    else:
      self.__chart.seriesProperties[dataType].setdefault(seriesId, {}).update(data)
    return self

  def click(self, jsFncs):
    """
    :category:
    :rubric: JS
    :type: Events
    :dsc:

    :link Plotly Documentation: https://plot.ly/javascript/plotlyjs-events/
    """
    self.jsFrg('click', jsFncs)
    return self

  def __str__(self):
    if self.title:
      strChart = '<div style="width:100%%;text-align:center;font-size:16px">%s</div><div id="%s" style="height:%spx"></div>' % ( self.title, self.htmlId, self.height - 50)
    else:
      strChart = '<div id="%s" style="height:%spx"></div>' % (self.htmlId, self.height - 30)
    return AresHtmlGraphFabric.Chart.html(self, self.strAttr(withId=False, pyClassNames=self.pyStyle), strChart)


  # ---------------------------------------------------------------------------------------------------------
  #                                          MARKDOWN SECTION
  # ---------------------------------------------------------------------------------------------------------
  @classmethod
  def matchMarkDownBlock(cls, data):
    return True if data[0].strip().startswith("---Vis") else None

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
      p = aresObj.chart(data[0].split(":")[1].strip(), records, seriesNames=headers[1:], xAxis=headers[0], chartFamily='Vis')
      p.addAttr(attr, isPyData=False)
    return []

