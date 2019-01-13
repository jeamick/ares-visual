#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


class JsD3Bubble(object):
  """
  :dsc:
    aggData = {datasets: [], labels: [], stats: {} } ;
  """
  alias = "D3"
  chartTypes = ['bubble']
  params = ("seriesNames", "xAxis")
  value = '''
    var temp = {} ; var labels = {};
    data.forEach(function(rec) { 
      if (!(rec[xAxis] in temp)) {temp[rec[xAxis]] = {}};
      seriesNames.forEach(function(name){
        labels[name] = true; if(rec[name] !== undefined) {if (!(name in temp[rec[xAxis]])) {temp[rec[xAxis]][name] = rec[name]} else {temp[rec[xAxis]][name] += rec[name]}}  }) ;
    });
    var labels = Object.keys(labels);
    for(var series in temp) {
      var values = {text: "", size: 0};
      labels.forEach(function(label) { if(temp[series][label] !== undefined ) { values.text = label; values.size = temp[series][label] }});
      result.push(values);};
    '''
