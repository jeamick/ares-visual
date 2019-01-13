#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import json
from ares.Lib.html import AresHtml


class Chart(AresHtml.Html):
  """ NVD3 Venn Chart python interface """
  references = {'D3 Venn': 'https://github.com/benfred/venn.js',
                'Example': 'http://bl.ocks.org/bessiec/986e971203b4b8ddc56d3d165599f9d0'}
  __chartStyle = {}
  __svgProp, __chartProp = {}, {}
  __reqJs = ['venn']
  name, category, callFnc = 'Venn', 'Charts', 'venn'

  def mocks(self, chartType):
    return [ {'sets': ['A'], 'size': 12}, {'sets': ['C'], 'size': 4},
             {'sets': ['B'], 'size': 12}, {'sets': ['A','B'], 'size': 2}]

  def __init__(self, aresObj, chartType, data, width, widthUnit, height, heightUnit, title, chartDesc, margin):
    if data is None:
      data = self.mocks('')
    super(Chart, self).__init__(aresObj, data)
    self.height, self.width, self.title = height, width, title
    self.css({'height': '%s%s' % (height, heightUnit), 'width': '%s%s' % (width, widthUnit)})

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
    self.addGlobalFnc("D3_%s(htmlObj, data, title)" % self.htmlId, '''
      htmlObj.find("svg").remove() ; d3.select(htmlObj.get(0)).append("svg");
      var chart = venn.VennDiagram(%(colorCharts)s).width(%(width)s).height(%(height)s - 50) ;
      d3.select(htmlObj.find("svg").get(0)).datum(data).call(chart) ;
      nv.utils.windowResize(chart.update);

      var tooltip = d3.select("body").append("div").attr("class", "venntooltip");
      d3.selectAll("#" + htmlObj.attr('id') + " .venn-circle")
        .on("mouseover", function(d, i) {
            var node = d3.select(this).transition();
            node.select("path").style("fill-opacity", .2);
            node.select("text").style("font-weight", "100").style("font-size", "36px");})
            
        .on("mouseout", function(d, i) {
            var node = d3.select(this).transition();
            node.select("path").style("fill-opacity", 0);
            node.select("text").style("font-weight", "100").style("font-size", "24px");});

      var div = d3.select(htmlObj.get(0));
      div.selectAll("g")
          .on("mouseover", function(d, i) {
              venn.sortAreas(div, d);

              tooltip.transition().duration(400).style("opacity", .9);
              tooltip.text(d.size + " users");

              var selection = d3.select(this).transition("tooltip").duration(400);
              selection.select("path").style("fill-opacity", d.sets.length == 1 ? .4 : .1).style("stroke-opacity", 1);
          })

          .on("mousemove", function() {
              tooltip.style("left", (d3.event.pageX) + "px").style("top", (d3.event.pageY - 28) + "px");})

          .on("mouseout", function(d, i) {
              tooltip.transition().duration(400).style("opacity", 0);
              var selection = d3.select(this).transition("tooltip").duration(400);
              selection.select("path").style("fill-opacity", d.sets.length == 1 ? .25 : .0).style("stroke-opacity", 0); });
      
      ''' % {'width': self.width, 'height': self.height, 'colorCharts': json.dumps(self.getColorRange()[::-1]) })

  def __str__(self):
    return '<div><div %s>%s<svg></svg></div></div>' % (self.strAttr(pyClassNames=['CssDivNoBorder']), self.title)
