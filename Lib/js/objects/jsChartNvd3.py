#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
  'eng': '''

'''
}


class JsNVD3Pie(object):
  """
  :category: RecordSet to NVD3 Object
  :rubric: JS
  :type: Data Transformation
  :dsc:
    aggData = {datasets: [], labels: [], stats: {} } ;
  """
  alias = "NVD3"
  chartTypes = ['pie']

  params = ("seriesNames", "xAxis")
  value = '''
    var temp = {} ; var labels = {};
    data.forEach(function(rec) { 
      if (!(rec[xAxis] in temp)) {temp[rec[xAxis]] = {}};
      seriesNames.forEach(function(name){
        labels[name] = true; if(rec[name] !== undefined) {if (!(name in temp[rec[xAxis]])) {temp[rec[xAxis]][name] = rec[name]} else {temp[rec[xAxis]][name] += rec[name]}}  }) ;
    });
    var labels = Object.keys(labels) ; result = [] ;
    for(var series in temp) {
      var values = {y: 0, x: series};
      labels.forEach(function(label) {
        if(temp[series][label] !== undefined ) { values.y = temp[series][label] }});
      result.push(values)}
    '''


class JsNVD3Bar(object):
  """
  :category: RecordSet to NVD3 Object
  :rubric: JS
  :type: Data Transformation
  :dsc:
    aggData = {datasets: [], labels: [], stats: {} } ;
  """
  alias = "NVD3"
  params = ("seriesNames", "xAxis")
  value = '''
    var temp = {}; var labels = []; var uniqLabels = {};
    seriesNames.forEach(function(series){temp[series] = {}}) ;
    data.forEach(function(rec) { 
      seriesNames.forEach(function(name){
        if(rec[name] !== undefined) {
          if (!(rec[xAxis] in uniqLabels)){labels.push(rec[xAxis]); uniqLabels[rec[xAxis]] = true};
          temp[name][rec[xAxis]] = rec[name]}})
    });
    seriesNames.forEach(function(series){
      dataSet = {key: series, values: [], labels: labels};
      labels.forEach(function(x, i){
        var value = temp[series][x]; 
        if (isNaN(value)) { value = null};
        if (value !== undefined) {dataSet.values.push({y: value, x: i, label: x})}
      }); result.push(dataSet)})
    '''

