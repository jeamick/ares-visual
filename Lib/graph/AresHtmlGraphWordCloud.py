#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import re
import json

from ares.Lib.html import AresHtml
from ares.Lib.graph import AresHtmlGraphFabric


class Chart(AresHtml.Html):
  """ NVD3 Word Cloud Chart python interface """
  name, __reqCss, __reqJs = 'WordCloud', [], ['cloud']
  references = {'D3 Word Cloud': 'https://www.jasondavies.com/wordcloud/'}
  factor = 1
  name, category, callFnc = 'WordCloud', 'Charts', 'wordcloud'

  def mocks(self, chartType):
    return [	{"key": "One", "value": 29}, {"key": "Four", "value": 96}, {"key": "Other", "value": 30}]

  def __init__(self, aresObj, chartType, data, width, widthUnit, height, heightUnit, title, chartDesc, margin):
    if data is None:
      data = self.mocks('')
    super(Chart, self).__init__(aresObj, data)
    self.height, self.width, self.title = height, width, title
    self.css({'height': '%s%s' % (height, heightUnit), 'width': '%s%s' % (width, widthUnit)})

  def scaling(self, factor):
    """ Rescale the values to have fit the page

    :param factor: The scaling factor > 1
    :return:
    """
    self.factor = factor

  def autoscale(self):
    """ Rescale the values in order to get something not to big for the div size """
    vals = [rec[self.seriesGrps[0].jsVar['val']] for rec in self.seriesGrps[0].xFilter.recordSet]
    self.factor = max(vals) / 100.0

  def onDocumentLoadVar(self):
    """ Return the variable to store in the global section of the javacript part """
    self.jsVarVal = "%s_data" % self.htmlId
    self.addGlobalVar(self.jsVarVal, json.dumps(self.vals))

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    self.jsUpdateDataFnc = "D3_%(htmlId)s(%(jqId)s, %(htmlId)s_data) ; " % {'jqId': self.jqId, 'htmlId': self.htmlId}
    self.aresObj.jsOnLoadFnc.add(self.jsUpdateDataFnc)

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("D3_%s(htmlObj, data)" % self.htmlId, '''
      htmlObj.find("svg").remove() ; d3.select(htmlObj.get(0)).append("svg");
      d3.select(htmlObj.find("svg").get(0)).style("height", '%(height)spx').style("width", '%(width)s%%');
      d3.layout.cloud().size([%(width)s+200, %(height)s])
        .words(data).rotate(function() { return ~~(Math.random() * 2) * 90; })
        .font("Impact").fontSize(function(d) { return d.value / %(factor)s; })
        .on("end", draw_new).start();

      function draw_new(words) {
        d3.select(htmlObj.find("svg").get(0))
          .append("g").attr("transform", "translate(150,150)").selectAll("text")
          .data(words).enter().append("text").style("font-size", function(d) { return d.size + "px"; })
          .style("font-family", "Impact").style("fill", function(d, i) {  return %(color)s[i]; }).attr("text-anchor", "middle")
          .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; }).text(function(d) { return d.text; });
      } ; 
      ''' % {"height": self.height, "width": self.width, 'factor': self.factor, 'color': json.dumps(AresHtmlGraphFabric.chartColors) })

  def __str__(self):
    return '<div><div %s>%s<svg></svg></div></div>' % (self.strAttr(pyClassNames=['CssDivNoBorder']), self.title)