#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
from ares.Lib.html import AresHtml
from ares.Lib.js.tables import JsPivotFncs


DSC = {
  'eng': '''

'''
}


class PivotTable(AresHtml.Html):
  """
  :cateogory:
  :rubric:
  :type:
  :example: aresObj.pivot(df, rows=['Date'], cols=['direction'], valCol=['AAPL.Low'], title="Pivot table title")
  :dsc:
    Do not attached entry to the Array using prototype as this might have clashed with the renderer of this object
  """
  references = {'Pivot Table': 'https://pivottable.js.org/examples/',
                'React Table': 'https://react-pivottable.js.org/',
                'Example': 'https://jsfiddle.net/nicolaskruchten/w86bgq9o/'}
  __reqJs, __reqCss = ["pivot"], ["pivot"]
  name, category, callFnc, docCategory = 'Pivot Table', 'Table', 'pivot', 'Standard'
  cssTitle = "CssTitle4"

  def __init__(self, aresObj, recordSet, rows, cols, valCol, title, width, widthUnit, height, heightUnit, aggOptions, rendererName, htmlCode):
    super(PivotTable, self).__init__(aresObj, [], width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, code=htmlCode)
    # to add all the columns in the table if nothing defined
    self.aggOptions, self.dsc = aggOptions, ''
    self.__pivot = {'cols': [] if cols is None else cols, 'rows': [] if rows is None else rows, 'vals': [] if valCol is None else valCol,
                    'aggregatorName': aggOptions['name'], 'rendererName': rendererName}
    self.__aggFncs, self.title = dict(JsPivotFncs.getAggFnc()), title
    if isinstance(recordSet, list):
      dataframe = aresObj.df(recordSet)
    self.data = recordSet
    self.data.attach(self)
    self.css({'margin': '0 auto', 'display': 'table', 'position': 'relative'})
    self.addGlobalFnc("numberWithCommas(x)", 'return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");')

  def addAggregator(self, aggCls):
    """
    :category: Pivot Aggregators
    :rubric: JS
    :type: Framework Extension
    :dsc:
      Add on the fly new aggregation logic to the pivot table. This will allow the creation of bespoke aggregation functions.
      Those functions will be structure in the way they can be added to the core framework easily.
      Aggregators should follow some rules and they should defined some mandatory parameters (name, keyAgg, push, value, format).
    :return: The HtmlObj
    :example:
      class JsPivotSumAgg(object):
        name = "New Sum Agg"
        keyAgg, key2Agg = 0, None
        push = 'this.keyAgg += parseFloat(record[attributeArray[0]]) * 2'
        value = 'return this.keyAgg'
        format = 'return numberWithCommas(x.toFixed(%(digits)s))'
    :link Aggregator Documentation: https://github.com/nicolaskruchten/pivottable/wiki/Aggregators
    """
    if not ':dsc:' in aggCls.__doc__:
      raise Exception("The new Aggregator class %s must have a doc string with a :dsc: field !" % aggCls.name)

    if aggCls.name in self.__aggFncs:
      raise Exception("Duplicated Name - Aggregator %s cannot be replaced !!!" % aggCls.name)

    self.__aggFncs[aggCls.name] = type(aggCls.__name__, (aggCls, JsPivotFncs.JsPivotAggFnc), {})()
    return self

  def jsGenerate(self, jsData='data', jsDataKey=None, isPyData=False, jsId=None):
    return """%(jqId)s.pivotUI(%(jsData)s, window['options_%(htmlId)s'])""" % {'jqId': self.jqId, 'jsData': self.data.setId(jsData).getJs(), 'htmlId': self.htmlId}

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    jsAggFncs = "{%s}" % ", ".join(["'%s': function(attributeArray) {return function(data, rowKey, colKey) {return %s}}" % (name, aggFncs.toJs(self.aggOptions)) for name, aggFncs in self.__aggFncs.items()])
    self.aresObj.jsOnLoadFnc.add("""
      var tpl = $.pivotUtilities.aggregatorTemplates;window['options_%(htmlId)s'] = %(options)s; 
      window['options_%(htmlId)s'].aggregators = %(agg)s""" % {'options': json.dumps(self.__pivot), 'agg': jsAggFncs, 'htmlId': self.htmlId})
    self.aresObj.jsOnLoadFnc.add(self.jsGenerate(None))

  def onDocumentLoadFnc(self): return True

  def setTableCss(self, cssClss):
    """
    :category: Table Definition
    :rubric: CSS
    :type: Style
    :dsc:
      Add a style to the datatable. This can be used to change some specific part of the table (for example the header)
    :example:
      class CssTableHeader(object):
        __style = [{'attr': 'background', 'value': 'grey'}]
        childrenTag = 'th'

      tb.setTableCss(CssTableHeader)
    :return: The Python Datatable object
    """
    import inspect

    if not isinstance(cssClss, list):
      cssClss = [cssClss]
    print(self.pyStyle)
    for cssCls in cssClss:
      if inspect.isclass(cssCls):
        self.aresObj.cssObj.addPy(cssCls)
        cssCls = cssCls.__name__
      clssMod = self.aresObj.cssObj.get(cssCls)
      if clssMod is not None:
        self.addPyCss(cssCls)
    return self

  def __str__(self):
    cssMod, titleCls = self.aresObj.cssObj.get(self.cssTitle), ""
    if cssMod is not None:
      self.addPyCss(self.cssTitle)
      titleCls = cssMod().classname
    if self.dsc != '':
      self.dsc = "<div style='width:100%%;padding-bottom:5px;text-align:justify'>%s</div>" % self.dsc
    return '''
    <div style="width:100%%;overflow:auto;">
      <div class="%(titleCls)s">%(title)s</div>%(dsc)s
      <div %(strAttr)s></div>
    </div>''' % {'strAttr': self.strAttr(pyClassNames=self.pyStyle), 'titleCls': titleCls, 'title': self.title, "dsc": self.dsc}


  # -----------------------------------------------------------------------------------------
  #                                    MARKDOWN SECTION
  # -----------------------------------------------------------------------------------------
  @classmethod
  def matchMarkDownBlock(cls, data):
    return True if data[0].strip().startswith("---Pivot") else None

  @staticmethod
  def matchEndBlock(data):
    return data.endswith("---")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj=None):
    return []

  def jsMarkDown(self): return ""

