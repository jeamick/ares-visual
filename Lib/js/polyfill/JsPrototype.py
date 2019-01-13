#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


class JsArray(object):
  """

  """
  primitive = "Array"
  fncs = {'unique': '''function() {var result = [];this.forEach(function(item) {
     if(result.indexOf(item) < 0) {result.push(item)} }); return result;}''',
          'contains': 'function(obj) {var i = this.length; while (i--) {if (this[i] === obj) {return true;}}; return false;}'}


class JsString(object):
  """

  """
  primitive = "String"
  fncs = {
    'leftTrim': 'function() { return this.replace(/^\s+/, ""); }',
    'startsWith': 'function(searchString, position){return this.substr(position || 0, searchString.length) === searchString;}',
    'formatMoney': '''function(decPlaces, thouSeparator, decSeparator) {
       var n = parseFloat(this); return n.formatMoney(decPlaces, thouSeparator, decSeparator) ;} ;'''}


class JsNumber(object):
  """

  """
  primitive = "Number"
  fncs = {'formatMoney': '''
    function(decPlaces, thouSeparator, decSeparator) {
    var n = this, decPlaces = isNaN(decPlaces = Math.abs(decPlaces)) ? 2 : decPlaces,
        decSeparator = decSeparator == undefined ? "." : decSeparator,
        thouSeparator = thouSeparator == undefined ? "," : thouSeparator,
        sign = n < 0 ? "-" : "",
        i = parseInt(n = Math.abs(+n || 0).toFixed(decPlaces)) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return sign + (j ? i.substr(0, j) + thouSeparator : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thouSeparator) + (decPlaces ? decSeparator + Math.abs(n - i).toFixed(decPlaces).slice(2) : "")} '''}


if __name__ == "__main__":
  obj = JsArray()
  for fncName, fncDef in obj.fncs.items():
    print("if (!%s.prototype.%s) { %s.prototype.%s = %s}" % (obj.primitive, fncName, obj.primitive, fncName, fncDef) )

