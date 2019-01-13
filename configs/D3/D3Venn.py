#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
from ares.configs.D3 import D3Base


class D3Venn(D3Base.D3Base):
  name, chartCall, chartType = 'Venn Chart', 'venn', 'venn'
  mocks = [
    {'sets': ['A'], 'size': 12},
    {'sets': ['C'], 'size': 4},
    {'sets': ['B'], 'size': 12},
    {'sets': ['A','B'], 'size': 2}
  ]

  def config(self): self.aresObj.jsImports.add('venn')

  def jsBuild(self):
    return '''
      var width = parseInt($('#%(htmlId)s').parent().css("width"))  ;
      var height = parseInt($('#%(htmlId)s').parent().css("height"))  ;
      var color = d3.scale.ordinal().range(["#334D6B", "#bbeeee"]);
      data =  [
        {'sets': ['A'], 'size': 12},
        {'sets': ['C'], 'size': 4},
        {'sets': ['B'], 'size': 17},
        {'sets': ['D'], 'size': 6},
        {'sets': ['A','B'], 'size': 7},
        {'sets': ['A','C'], 'size': 7},
      ];
      var chart = venn.VennDiagram(color).width(width).height(height) ;
      d3.select( $('#%(htmlId)s').parent().get(0) ).datum(data).call(chart) ;

      var tooltip = d3.select( $('#%(htmlId)s').parent().get(0) ).append("div").attr("class", "venntooltip");
   
      d3.selectAll(".venn-circle")
        .on("mouseover", function(d, i) {
            var node = d3.select(this).transition();
            node.select("path").style("fill-opacity", .2);
            node.select("text").style("font-weight", "100").style("font-size", "36px");})
            
        .on("mouseout", function(d, i) {
            var node = d3.select(this).transition();
            node.select("path").style("fill-opacity", 0);
            node.select("text").style("font-weight", "100").style("font-size", "24px");});
  
      var div = d3.select( $('#%(htmlId)s').parent().get(0) );
      console.log(color(10)) ;
      div.selectAll("g")
          .on("mouseover", function(d, i) {
              venn.sortAreas(div, d);
              tooltip.transition().duration(400).style("opacity", .9);
              tooltip.text(d.size + " users");
              var selection = d3.select(this).transition("tooltip").duration(400);
              selection.select("path").style("fill-opacity", d.sets.length == 1 ? .4 : .1).style("stroke-opacity", 1);
          })

          .on("mousemove", function() {tooltip.style("left", (d3.event.pageX) + "px").style("top", (d3.event.pageY - 28) + "px");})

          .on("mouseout", function(d, i) {
              tooltip.transition().duration(400).style("opacity", 0);
              var selection = d3.select(this).transition("tooltip").duration(400);
              selection.select("path").style("fill-opacity", d.sets.length == 1 ? .25 : .0).style("stroke-opacity", 0); });
      
      ''' % {'htmlId': self.chartId, "jsData": json.dumps(self.data) }
