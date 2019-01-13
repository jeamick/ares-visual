#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
from ares.configs.D3 import D3Base


class D3Wheel(D3Base.D3Base):
  """

  """
  name, chartCall, chartType = 'Wheel Chart', 'wheel', 'wheel'

  def jsBuild(self):
    return ''' 
      
    var width = parseInt($('#%(htmlId)s').parent().css("width"))  ;
    var height = parseInt($('#%(htmlId)s').parent().css("height"))  ;
    var radius = Math.min(width, height) / 2;
    var innerRadius = 0.3 * radius;
  
  var pie = d3.layout.pie()
      .sort(null)
      .value(function(d) { return d.width; });
  
  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([0, 0])
    .html(function(d) {
      return d.data.label + ": <span style='color:orangered'>" + d.data.score + "</span>";
    });
  
  var arc = d3.svg.arc()
    .innerRadius(innerRadius)
    .outerRadius(function (d) { 
      return (radius - innerRadius) * (d.data.score / 100.0) + innerRadius; 
    });
  
  var outlineArc = d3.svg.arc()
          .innerRadius(innerRadius)
          .outerRadius(radius);
  
  var svg = d3.select( $('#%(htmlId)s').get(0) )
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
      .attr("preserveAspectRatio", "xMinYMin meet")
      .classed("svg-content-responsive", true); ;
  
  svg.call(tip);
  
    data = [
      {id: "FIS",order: 1.1, score: 59, weight:0.5, color: "#9E0041", label: "Fisheries"},
      {id: "MAR",order:1.3, score: 24, weight:0.5, color: "#C32F4B", label:  "Mariculture"}
    ] ;
    
    data.forEach(function(d) {
      d.id     =  d.id;
      d.order  = +d.order;
      d.color  =  d.color;
      d.weight = +d.weight;
      d.score  = +d.score;
      d.width  = +d.weight;
      d.label  =  d.label;
    });

  var path = svg.selectAll(".solidArc")
      .data(pie(data))
    .enter().append("path")
      .attr("fill", function(d) { return d.data.color; })
      .attr("class", "solidArc")
      .attr("stroke", "gray")
      .attr("d", arc)
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide);

  var outerPath = svg.selectAll(".outlineArc")
      .data(pie(data))
    .enter().append("path")
      .attr("fill", "none")
      .attr("stroke", "gray")
      .attr("class", "outlineArc")
      .attr("d", outlineArc);  

  var score = 
    data.reduce(function(a, b) {
      return a + (b.score * b.weight); 
    }, 0) / 
    data.reduce(function(a, b) { 
      return a + b.weight; 
    }, 0);

  svg.append("svg:text")
    .attr("class", "aster-score")
    .attr("dy", ".35em")
    .attr("text-anchor", "middle") // text-align: right
    .text(Math.round(score));

        
      ''' % {"htmlId": self.chartId}