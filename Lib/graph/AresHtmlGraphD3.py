#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

# https://bl.ocks.org/ctufts/f38ef0187f98c537d791d24fda4a6ef9

from ares.Lib.html import AresHtml
from ares.Lib.graph import AresHtmlGraphFabric


DSC = {
  'eng': '''

'''
}


class Chart(AresHtml.Html):
  """

  """
  name, category, callFnc = 'D3', 'Charts', 'plotChartD3'
  __reqJs = ['d3']
  references = {
    'Website': 'https://d3js.org/',
    'Website2': 'https://d3plus.org/examples/',
  }

  def __init__(self, aresObj, chartType, data, width, widthUnit, height, heightUnit, title, chartDesc, subChart, zoom,
               legendPosition, order, showGrid, groupTooltips, showLabels, refresh, comment, download, pdf, excel, magnify,
               scriptSrc, htmlCode, globalFilter):

    if AresHtmlGraphFabric.CHARTS_FACTORY is None:
      AresHtmlGraphFabric.CHARTS_FACTORY = AresHtmlGraphFabric.loadFactory()  # atomic function to store all the different table mapping

    super(Chart, self).__init__(aresObj, [], code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.__chart = AresHtmlGraphFabric.CHARTS_FACTORY[self.name][chartType](aresObj, data, self.htmlId)

  def onDocumentLoadFnc(self): return True

  def onDocumentReady(self):
    self.aresObj.jsOnLoadFnc.add( self.__chart.jsBuild() )

  def __str__(self):
    return '<div %s><svg id="%s"></svg></div>' % (self.strAttr(withId=False, pyClassNames=['CssDivNoBorder']), self.htmlId)











  #
  #   if FACTORY is None:
  #     FACTORY = loadFactory()  # atomic function to store all the different table mapping
  #   if data is None:
  #     if chartType == 'treemap':
  #       data = aresObj.dc(FACTORY[chartType].mocks, ['value'], 'name')
  #     if chartType == 'radar':
  #       data = aresObj.dc(FACTORY[chartType].mocks, ['value'], ['name', 'skill'])
  #     if chartType == 'sankey':
  #       data = aresObj.df(FACTORY[chartType].mocks)
  #       nodes = data.filters(" category == 'nodes' ", inplace=False).dropCol(['category']).attr( {'selectCols': False, 'dropna': True} )
  #       edges = data.filters(" category == 'edges' ", inplace=False).dropCol(['category']).attr( {'selectCols': False, 'dropna': True} )
  #       data = [nodes, edges]
  #
  #   if FACTORY[chartType].convertFnc is not None:
  #     for fnc in FACTORY[chartType].convertFnc:
  #       if fnc not in data.dataFncs:
  #         data.dataFncs.append(fnc)
  #
  #   super(Chart, self).__init__(aresObj, data, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
  #   self.__chart = FACTORY[chartType](aresObj, data, self.htmlId, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
  #   self.refresh, self.comment, self.download, self.pdf, self.excel, self.magnify = refresh, comment, download, pdf, excel, magnify
  #
  # @classmethod
  # def charts(cls, chartType=None):
  #   factory = loadFactory()
  #   if chartType is not None:
  #     return factory[chartType]
  #
  #   return sorted(factory.keys())
  #
  # def onDocumentLoadVar(self): pass
  # def onDocumentLoadFnc(self): return True
  #
  # def onDocumentReady(self):
  #   self.aresObj.jsOnLoadFnc.add("var %(htmlId)s_chart = %(jsBuild)s;" % {'htmlId': self.htmlId, 'jsBuild': self.__chart.jsBuild()})
  #
  # def __str__(self):
  #   return '<div %s><div id="%s"></div></div>' % (self.strAttr(withId=False, pyClassNames=['CssDivNoBorder']), self.htmlId)