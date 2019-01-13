#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DSC = {
  'eng': '''
  '''
}


class JsTextTsv(object):
  """
  :category: RecordSet to Text
  :rubric: JS
  :type: Data Transformation
  :dsc:
    Convert the Javascript object to a string with each column delimited by a tabulation.
  """
  alias = "ToTsv"
  params = ('colNames', )
  value = '''
    var tmp = []; var row = [];
    colNames.forEach(function(col){row.push(col)}); tmp.push(row.join('\t'));
    data.forEach(function(rec){
      row = [];
      colNames.forEach(function(col){row.push(rec[col])});
      tmp.push(row.join('\t')) });
    result = tmp.join('\\n') '''