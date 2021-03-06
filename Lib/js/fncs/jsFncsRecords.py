#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DSC = {'eng': '''
:dsc:
This module get all the functions related to the transformation of the recordset on the Javascript part.
Each of those functions are in charge of transforming a recordSet in the front end (which means that this cannot be 
seen on the Python side in the scripting interface). The best way to test those changes is to use a report and set the DEBUG flag.

## 

'''}


class JsRecFunc(object):
  """
  :category: Javascript Record Function
  :rubric: JS
  :type: Record Function Interface
  :dsc:
    This class cannot be used directly to format a record as the mandatory parameters are not defined and are set to None.
    Anyway as an interface this will give you the different information which have to be defined to create a new js function.
    The objective in this logic is to centralise all the js functions used in the front end in this folder in order
    to limit the use and standardise the implementation.

    ## The main parameters ##

    - alias, The alias name used in the Python layer to point to this function
    - params, The parameters name available in the Javascript function (data is always passed)
    - value, The content of the function.

    ## Javascript function ##

    A javascript function, represented as a class in the framework, is always trying to transform a data variable
    which is defined as a recordSet to a result variable which should be also a recordSet. The purpose of having this
    will ensure that functions can:

      1. Transform the recordSet in a specific manner
      2. Be shared in the different components
      3. Be put together sum(count(...))

  """
  alias = None
  params = None
  value = None

  @staticmethod
  def extendArgs(category, originParams, newCols): return originParams

  @staticmethod
  def extendColumns(jsSchema, params):
    raise Exception("Method extendColumns should be overriden")


class JsRowBuckets(JsRecFunc):
  """
  :category: Javascript Record Function
  :rubric: JS
  :type:
  :dsc:


  """
  @staticmethod
  def extendArgs(category, originParams, newCols):
    originParams[1] += newCols
    return originParams

  @staticmethod
  def extendColumns(jsSchema, params):
    pass

  alias = "row-buckets"
  params = ("allGroups", "seriesNames")
  value = '''
    var groupRowsIds = {}; var groupRows = {};
    data.forEach(function(rec, i){
      var inBuckets = {}; for(var g in allGroups){inBuckets[g] = null};
      for(var g in allGroups){
        for(var col in allGroups[g]){if(allGroups[g][col].indexOf(rec[col]) >= 0){
          inBuckets[g] = true} else {inBuckets[g] = false; break}}}
      for(var g in inBuckets){
        if (inBuckets[g]) { 
            if (g in groupRowsIds) {groupRowsIds[g].push(i);groupRows[g].push(rec)} 
            else {groupRowsIds[g] = [i];groupRows[g] = [rec]}}
      }; result.push(rec)
    });
    for(var g in groupRows){
      var row = {'_system': true}; var text = g;
      for(var col in allGroups[g]){row[col] = text; text=''}; seriesNames.forEach(function(v){row[v] = 0}); 
      groupRows[g].forEach(function(rec){ seriesNames.forEach(function(v){row[v] += rec[v]})});
      result.push(row)}'''


class JsRowTotal(JsRecFunc):
  """
  :category: Javascript Record Function
  :rubric: JS
  :type: RecordSet Function
  :dsc:

  """
  @staticmethod
  def extendArgs(category, originParams, newCols):
    originParams[0] += newCols
    return originParams

  @staticmethod
  def extendColumns(jsSchema, params):
    pass

  alias = "row-total"
  params = ("seriesNames", "rowDefinition")
  value = '''
    seriesNames.forEach(function(v){rowDefinition[v] = 0});
    data.forEach(function(rec){
      if(!rec['_system']){seriesNames.forEach(function(v){rowDefinition[v] += rec[v]})};
      result.push(rec);
    }); result.push(rowDefinition);
    '''


class JsSum(JsRecFunc):
  """
  :category: Javascript Record Function
  :rubric: JS
  :type:
  :dsc:


  """

  @staticmethod
  def extendColumns(jsSchema, params):
    if params[0] is not None and params[1] is not None:
      jsSchema['keys'] |= set(params[0])
      jsSchema['values'] |= set(params[1])

  alias = "sum"
  params = ("keys", "values")
  value = '''
    if ((keys == null) || (values == null)){result = data}
    else{
      var temp = {};
      var order = [];
      data.forEach( function(rec) { 
        var aggKey = []; keys.forEach(function(k){ aggKey.push(rec[k])}); var newKey = aggKey.join("#"); order.push(newKey);
        if (!(newKey in temp)) {temp[newKey] = {}};
        values.forEach(function(v) {if (!(v in temp[newKey])) {temp[newKey][v] = rec[v]} else {temp[newKey][v] += rec[v]}}) ;}); 
      order.forEach(function(label) {
        var rec = {}; var splitKey = label.split("#");
        keys.forEach(function(k, i) {rec[k] = splitKey[i];});
        for(var v in temp[label]) {rec[v] = temp[label][v]};
        result.push(rec)})}'''


class JsOperations(JsRecFunc):
  """
  :category: Count
  :rubric: JS
  :type:
  :dsc:
    This function will aggregate the different values for each series according to a shcema defined in a Python
    dictionary in the last position of the tuple.
  :example: aggFnc=('aggregation', ['direction'], values, {'dn': 'sum', 'Date': 'count'}),
  :return:
  """

  @staticmethod
  def extendArgs(category, originParams, newCols):
    """
    :category: Update Arguments
    :rubric: JS
    :type:
    :dsc:
      This function will update the function argument accoding to the mode defined by the user. Indeed some properties can be received to validate the accuracy of the data.
      Those data should be added to the different transformation functions and the columns should be passed to the final object.
      This function will ensure that by activating the mode the columns will be automatically added to the aggregated data.
    :return: The update set of columns to be considered in the Javascript function
    """
    if category == 'age':
      originParams[1] = originParams[1] + newCols
      for c in newCols:
        originParams[2][c] = 'sum'
    return originParams

  @staticmethod
  def extendColumns(jsSchema, params):
    """

    """
    if params[0] is not None and params[1] is not None:
      jsSchema['keys'] |= set(params[0])
      jsSchema['values'] |= set(params[1])

  alias = "aggregation"
  params = ("keys", "values", "operations")
  value = '''
    var temp = {};
    var order = [];
    data.forEach( function(rec) { 
      var aggKey = []; keys.forEach(function(k){ aggKey.push( rec[k])}); var newKey = aggKey.join("#"); order.push(newKey);
      if (!(newKey in temp)) {temp[newKey] = {}};
      values.forEach(function(v) {
        if (operations[v] === undefined){ if (!(v in temp[newKey])) {temp[newKey][v] = 1} else {temp[newKey][v] += 1} }
        else if (operations[v] == 'sum') {if (!(v in temp[newKey])) {temp[newKey][v] = rec[v]} else {temp[newKey][v] += rec[v]}}
        else if (operations[v] == 'count') {if (!(v in temp[newKey])) {temp[newKey][v] = 1} else {temp[newKey][v] += 1}}
      })}); 
    order.forEach(function(label) {
      var rec = {}; var splitKey = label.split("#");
      keys.forEach(function(k, i) {rec[k] = splitKey[i];});
      for(var v in temp[label]) {rec[v] = temp[label][v]};
      result.push(rec)})'''


class JsCount(JsRecFunc):
  """
  :category: Count
  :rubric: JS
  :type:
  :dsc:

  """

  @staticmethod
  def extendColumns(jsSchema, params):
    if params[0] is not None and params[1] is not None:
      jsSchema['keys'] |= set(params[0])
      jsSchema['values'] |= set(params[1])

  alias = "count"
  params = ("keys", "values")
  value = '''
    var temp = {};
    var order = [];
    data.forEach( function(rec) { 
      var aggKey = []; keys.forEach(function(k){ aggKey.push( rec[k])}); var newKey = aggKey.join("#"); order.push(newKey);
      if (!(newKey in temp)) {temp[newKey] = {}};
      values.forEach(function(v) {if (!(v in temp[newKey])) {temp[newKey][v] = 1} else {temp[newKey][v] += 1}}) ;}); 
    order.forEach(function(label) {
      var rec = {}; var splitKey = label.split("#");
      keys.forEach(function(k, i) {rec[k] = splitKey[i];});
      for(var v in temp[label]) {rec[v] = temp[label][v]};
      result.push(rec)})'''


class JsTop(object):
  """
  :category: Count
  :rubric: JS
  :type:
  :dsc:

  """

  @staticmethod
  def extendColumns(jsSchema, params): pass

  alias = "top"
  params = ("countItems", "value", "sortType")
  value = '''
    var tmpRec = {};
    data.forEach(function(rec){
      if(tmpRec[rec[value]] === undefined){ tmpRec[rec[value]] = [rec] } else {tmpRec[rec[value]].push(rec)}});
    
    var result = []; 
    Object.keys(tmpRec).sort().forEach(function(key) {
      tmpRec[key].forEach(function(rec){result.push(rec)})});
    
    if (sortType == 'descending'){ result = result.slice(-countItems)}
    else {result = result.slice(0, countItems)}
    '''


class JsCountDistinct(object):
  """
  :category: Distinct Count
  :rubric: JS
  :type:
  :dsc:
    Return the distinct counts of element in a list of columns. This function will return a list of dictionaries
    with the following structure {'column': '', 'count_distinct': 0}
  :return: A new recordSet with the properties of the requested keys
  """
  alias = "count(Distinct)"
  params = ("keys", )
  value = '''
    var temp = {}; var t0 = performance.now(); keys.forEach(function(k){temp[k] = {}});
    data.forEach(function(rec) {keys.forEach(function(k){temp[k][rec[k]] = 1})}); 
    for(var col in temp){
      var dCount = Object.keys(temp[col]).length; result.push({'column': col, 'count_distinct': dCount})}'''


class JsCountAll(object):
  """
  :category: Count all
  :rubric: JS
  :type:
  :dsc:
    Function to produce KPI on an original recordSet. This function will create a new recordSet based on the selected
    columns of the original data source.
  :return: A new recordSet with the properties of the requested keys
  """
  alias = "count(All)"
  params = ("keys", )
  value = '''
    var temp = {}; var order= []; var t0 = performance.now();
    data.forEach(function(rec) { 
      keys.forEach(function(k){
        var aggKey = k + "#" + rec[k]; order.push(aggKey); if (!(aggKey in temp)) {temp[aggKey] = 1} else {temp[aggKey] += 1}});}); 
    order.forEach(function(label) {{
      var keys = label.split("#"); var rec = {'column': keys[0], 'value': keys[1], 'count': temp[label]};
      result.push(rec);})'''


class JsRename(object):
  """
  :category: Column Renaming
  :rubric: JS
  :type:
  :dsc:
    Function to remap some columns in the recordSet. The renaming is done based on the input parameter.
    The parameter passed in this function is a dictionary with as keys the existing column names and value the new column.
  :return: The Js recordSet with the new columns in each record. The original keys will be removed
  """
  alias = "rename"
  params = ("colsWithName", )
  value = '''
    var t0 = performance.now();
    data.forEach( function(rec) { 
      for (var col in colsWithName) {rec[colsWithName[col]] = rec[col]; delete rec[col]; result.push(rec); } })'''


class JsExtend(object):
  """
  :category:
  :rubric: JS
  :type:
  :dsc:
    Function to add some predefined entries to each records in the RecordSet
    The parameter passed in the function call should be a dictionary with as keys the columns to be added to the original record
    and the value {'static': {}, 'dynamic': {}}
    In case of key clashes the values will be replaced.
  :return: A new Js recordSet with the extra columns
  """
  alias = "extend"
  params = ('values', 'recKey')
  value = '''
    if (Array.isArray(data)){
      if(recKey == undefined){
        data.forEach(function(rec, i) { 
          var newRec = Object.assign(rec, values.static);
          if (i in values.dynamic) {newRec = Object.assign(newRec, values.dynamic[i])};
          result.push(newRec)})}
      else{
        data.forEach(function(rec, i) { 
          var newRec = Object.assign(rec, values.static);
          if (i in values.dynamic) {newRec = Object.assign(newRec, values.dynamic[i])};
          result.push(newRec);
          var subValues = rec[recKey]; result[recKey] = [];
          subValues.forEach(function(row, j) { 
            var newRec = Object.assign(row, values.static);
            if (i in values.dynamic) {newRec = Object.assign(newRec, values.dynamic[i])};
            result[recKey].push(newRec)})  
        })
      }} 
    else {result = data}
  '''


class JsExtendDataSet(object):
  """
  :category:
  :rubric: JS
  :type:
  :dsc:

  :return: A new Js recordSet with the extra columns in the datasets section
  """
  alias = "extend-dataset"
  params = ("values", 'recKey')
  value = '''
    var records; var recResults; 
    if(recKey == undefined){records = data;recResults = result} 
    else {records = data[recKey];result[recKey] = [];recResults = result[recKey];
      for(var k in data) {if (k != recKey) {result[k] = data[k]}}};
    records.forEach(function(rec, i) { 
      var newRec = Object.assign(rec, values.static);
      if (i in values.dynamic) {newRec = Object.assign(newRec, values.dynamic[i])};
      recResults.push(newRec)})'''


class JsFilter(object):
  """
  :category: Records Filter
  :rubric: JS
  :type:
  :dsc:
    Filter the different records in a recordSet from the definition given as a parameter.
    The filters definition is based on a dictionary as keys the column names. Each records should have the given columns.
    All records which do not match the rules will not be considered
  :return: A new JS dictionary with only the selected lines
  """
  alias = "filter"
  params = ("filterCols", )
  value = '''
    filters = {};
    for (var k in filterCols){if((k !== 'allIfEmpty') && (k !== '_colsMaps') ){filters[k] = filterCols[k]}};
    if(filterCols.allIfEmpty !== undefined){
      filterCols.allIfEmpty.forEach(function(col){
        if(Array.isArray(filters[col])){ if(filters[col].length == 0){ delete filters[col]}}
        else {if((filters[col] === null) || (filters[col].replace(/(<br ?\/?>)*/g,"") == '')) { delete filters[col]}}}
    )}; ;
    data.forEach( function(rec) {  
      var isValid = true; for (var col in filters) {
        var mapCol = col;
        if(filterCols['_colsMaps'] !== undefined){mapCol = filterCols['_colsMaps'][col]};
        if (Array.isArray(filters[col])){if (filters[col].indexOf(rec[mapCol]) < 0) { isValid = false; break }}
        else {if (rec[mapCol] != filters[col]) { isValid = false; break }} };
      if (isValid) {result.push(rec)}})'''


class JsIntensity(object):
  """

  """
  alias = "intensity"
  params = ("cols",)
  value = '''
    stats = {};
    cols.forEach(function(col){stats[col] = {min: null, max: null}});
    data.forEach(function(rec){
      cols.forEach(function(col){
        if((stats[col].max == null) || (rec[col] > stats[col].max) ) { stats[col].max = rec[col]};
        if((stats[col].min == null) || (rec[col] < stats[col].min) ) { stats[col].min = rec[col]}})});
    data.forEach(function(rec){
      cols.forEach(function(col){rec[col + ".intensity.min"] = stats[col].min; rec[col + ".intensity.max"] = stats[col].max});
      result.push(rec)});
    '''

  @staticmethod
  def extendColumns(jsSchema, params):
    pass