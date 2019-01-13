#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {

}


class JsBillboard(object):
  """
  :category: RecordSet to Billboard Object
  :rubric: JS
  :type: Data Transformation
  :dsc:
    Function to convert an AReS recordSet to a valid object for Billboard.
  """
  alias = "Billboard"
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
    result = [];
    result.push(['x'].concat(labels));
    seriesNames.forEach(function(series){
      dataSet = [series];
      labels.forEach(function(x){
        if (temp[series][x] == undefined) {dataSet.push(null)} else {dataSet.push(temp[series][x])}
      }); result.push(dataSet)}); '''


class JsC3Pie(object):
  """
  :category: RecordSet to Billboard Object
  :rubric: JS
  :type: Data Transformation
  :dsc:

  """
  alias = "Billboard"
  chartTypes = ['pie', 'donut']
  params = ("seriesNames", "xAxis")
  value = '''
    var temp = {} ; var labels = {};
    data.forEach(function(rec) { 
      if (!(rec[xAxis] in temp)) {temp[rec[xAxis]] = {}};
      seriesNames.forEach(function(name){
        labels[name] = true; if(rec[name] !== undefined) {if (!(name in temp[rec[xAxis]])) {temp[rec[xAxis]][name] = rec[name]} else {temp[rec[xAxis]][name] += rec[name]}}  }) ;
    });
    result = [];
    result.push(['x'].concat(labels));
    var labels = Object.keys(labels);
    for(var series in temp) {
      var values = [series];
      labels.forEach(function(label) {
        if(temp[series][label] !== undefined ) { values.push(temp[series][label]) } else { values.push(null) }});
      result.push(values);};
    '''

