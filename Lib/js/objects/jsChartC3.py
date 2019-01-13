#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
  'eng': '''

'''
}


class JsC3(object):
  """
  :category: RecordSet to C3 Object
  :rubric: JS
  :type: Data Transformation
  :dsc:

  """
  alias = "C3"
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
  :category: RecordSet to C3 Object
  :rubric: JS
  :type: Data Transformation
  :dsc:

  """
  alias = "C3"
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


if __name__ == "__main__":
  # It is possible to test the result of the function
  import json

  path = r'C:\Users\olivier\Documents\test\test.html'
  with open(path, 'w') as f:
    f.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<script language="javascript" type="text/javascript">\n')
    jsFnc = 'function %s(%s) {%s; return result};' % (JsC3Pie.__name__, ", ".join(['data', *list(JsC3Pie.params)]), JsC3Pie.value)
    f.write("%s\n" % jsFnc)
    f.write("</script>\n</head>\n<body>\n<script>")
    data = [
      {'a': 1, 'b': 'A'}, {'a': 3, 'b': 'B'},]
    f.write("console.log(%s(%s, ['a'], 'b'))" % (JsC3Pie.__name__, json.dumps(data)))
    f.write('</script>\n</body>\n</html>')