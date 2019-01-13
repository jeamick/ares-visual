#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import os
import time
import inspect
import json
import importlib

import ares.Lib.js.fncs
import ares.Lib.js.objects
import ares.utils.AresSiphash


# Factory wii all the javascript information
factory = None


DSC = {
  'eng': '''
:dsc:
The Ares Js object is the object in charge of defining the functions to apply to the different recordSets once they are 
defined on the Javascript side. This object will not be in charge of encoding the data (this is done as part of the 
pandas DataFrame in the module **AresFilePandas.py**), it will be on charge of ensuring that all your containers using the same 
data will rely on the same javascript variable. The only differences will be the javascript transformation to end up 
to an object definition which will fit the containers.
__
Each chart and table containers will have specific requirements and this specific transformation is done in objects/ conversion folder. 
Those conversion are defined based on the output function in the Js Object and each chart family will use it to type the data.
__
For example for the **ChartJs object** you get the below data conversion

```python
def plotChartJs(self, chartType, data=None, width=100, widthUnit="%", height=300, heightUnit='px', title='', chartOptions=None, toolsbar=None, htmlCode=None, globalFilter=None):
                  
params = (list(data._schema['values']), list(data._schema['keys']))
return self.add(graph.AresHtmlGraphChartJs.Chart(self, chartType, data.output('ChartJs', chartType, params), width, widthUnit, height, heightUnit, title, chartOptions, toolsbar, htmlCode, globalFilter), sys._getframe().f_code.co_name)
```

The data.output() function in this case will type the object to be a ChartJs one. The definition of the conversion from a recordSet to a ChartJs object is done in the module **jsCharts.py** specific to the ChartJs framework.
The Javascript part used to convert the data to this container is then defined in a static and generic manner in the value string variable.

```javascript
var temp = {}; var labels = []; var uniqLabels = {};
seriesNames.forEach(function(series){temp[series] = {}}) ;
data.forEach(function(rec) { 
  seriesNames.forEach(function(name){
    if(rec[name] !== undefined) {
      if (!(rec[xAxis] in uniqLabels)){labels.push(rec[xAxis]); uniqLabels[rec[xAxis]] = true};
      temp[name][rec[xAxis]] = rec[name]}})
});
result = {datasets: [], labels: labels};
seriesNames.forEach(function(series){
  dataSet = {label: series, data: []};
  labels.forEach(function(x){
    if (temp[series][x] == undefined) {dataSet.data.push(null)} else {dataSet.data.push(temp[series][x])}
  }); result.datasets.push(dataSet)})
```

## How to add Javascript transformations


## How to use the debug flag


## Use and Create a regression test  

This part is still in progress (do not hesitate to help), but the idea is quite simple to add various tests to your javascript functions.
Indeed any changes in the Javascript is quite painful and difficult to test / debug, the idea with this is to store all the relevant input and output in a text file automatically leveraging on the AReS architecture to make this easier.

A possible extension to this model could be to create specificity per type of browser in order to have a font end code which can adapt according to the browser.

'''}


def load(forceReload=False):
  """
  :category: Javascript
  :rubric: JS
  :type: Factory
  :dsc:
    Load the factory with the all the different Javascript functions defined in the framework.
    It will store all the different Javascript function used to transform the recordSet or the ones in charge
    of changing the recordSet to fit the different containers in the AReS components.
  :return: The factory data
  """
  global factory

  if factory is None or forceReload:
    tempFactory, aliasChecks = {}, {}
    jsStructures = {'fncs': ares.Lib.js.fncs, 'objs': ares.Lib.js.objects}
    for jsType, jsMod in jsStructures.items():
      for mod in os.listdir(os.path.dirname(jsMod.__file__)):
        if not mod.endswith('.py') or mod == '__init__.py':
          continue

        pyMod = importlib.import_module('%s.%s' % (jsMod.__name__, mod.replace(".py", "")))
        for name, obj in inspect.getmembers(pyMod):
          if inspect.isclass(obj) and obj.alias is not None:
            if hasattr(obj, 'alias') and hasattr(obj, 'value'):
              inst = obj()
              alias = [inst.alias] if not hasattr(inst, 'chartTypes') else ["%s_%s" % (inst.alias, cType.replace("-", "")) for cType in inst.chartTypes]
              params = "data" if getattr(inst, 'params', None) is None else "data, %s" % ", ".join(inst.params)
              for a in alias:
                if jsType == 'fncs':
                  a = "ares_%s" % a.replace("-", "")
                if a in aliasChecks:
                  raise Exception("Alias %s found two time in the framework %s and %s" % (a, obj.__name__, aliasChecks[a]))

                aliasChecks[a] = obj.__name__
                text = "".join([jsLine.strip() for jsLine in inst.value.strip().split("\n")])
                tempFactory.setdefault(jsType, {})[a] = {"text": text, 'params': params, 'module': pyMod.__name__, 'class': obj}
    factory = tempFactory
  return factory


class Js(object):
  """
  :category:
  :rubric:
  :type:
  :dsc:

  """

  def __init__(self, aresObj, pyDf, keys=None, values=None, debug=False):
    load()
    self._schema = {'fncs': [], 'out': None, 'post': [], 'keys': set() if keys is None else set(keys),
                    'values': set() if values is None else set(values), 'debug': getattr(aresObj, 'DEBUG', debug)}
    self._dataId = id(pyDf) # Store the memory ID of the original object (the one known by all the components
    if not hasattr(pyDf, 'htmlCode'):
      dataCode = None
      # For input data not defined as dataframe
      for key, dataSrc in aresObj.jsSources.items():
        if dataSrc.get('dataId') == self._dataId:
          dataCode = key
          break

      pyDf = aresObj.df(pyDf, htmlCode="ares_id_%s" % len(aresObj.jsSources) if dataCode is None else dataCode)
    self._jqId = pyDf.htmlCode # Original recordSet, this will never change
    self.aresObj, self.jqId, self._data = aresObj, pyDf.htmlCode, pyDf

  def setId(self, jqId):
    """
    :category: Javascript Object
    :rubric: JS
    :type: System
    :dsc:
      Change the Id variable name for the javascript data source.
    :return: The Python object
    """
    self.jqId = jqId if jqId is not None else self._jqId
    return self

  def attach(self, htmlObj):
    """
    :category: Javascript Object
    :rubric: JS
    :type: Front End
    :dsc:
      Attach the Dataframe to a HTML Object. This function is normally used in the different components in order
      to guarantee the link of the data. This will also ensure that the same data set will be store only once in the page
    """
    if not self._jqId in self.aresObj.jsSources:
      self.aresObj.jsSources[self._jqId] = {'dataId': self._dataId, 'containers': [], 'data': self._data}
    self.aresObj.jsSources[self._jqId]['containers'].append(htmlObj)
    self.aresObj.jsSources[self._jqId]['data'] = self._data # In case of replacements

  def output(self, outFamily, outType, args):
    """
    :category: Formatting
    :rubric: JS
    :type: Front End
    :dsc:
      Format the recordSet to a defined container.
    """
    self._schema['out'] = {"family": outFamily, 'type': outType, 'params': args}
    self._schema['out']['name'] = "%s_%s" % (outFamily, outType.replace("-", "")) if "%s_%s" % (outFamily, outType.replace("-", "")) in factory['objs'] else outFamily
    return self

  def fncs(self, fncNames, systemInfo=None):
    """
    :category: Formatting
    :rubric: JS
    :type: Front End
    :dsc:
      Post process functions on the recordSet. It will potentially enhance the columns to be processed if the systemInfo parameters are defined.
      This will allow to pass extra parameters to the different functions in the framework according to the system.
      Information can be computed in the bespoke reports or coming directly from the source system.
      In order to use this the category should be defined in the Javascript function defined in the module jsFncsRecords.
    :return: The Python Js object
    """
    if not fncNames:
      return self

    if not isinstance(fncNames, list):
      fncNames = [fncNames]
    for fncName in fncNames:
      args = None
      if isinstance(fncName, tuple):
        # This mean that some parameters are expected in the configuration
        if fncName[0] == 'order':
          countPerAxis, orderSeries = {}, []
          self._data['order'] = 0
          if fncName[1] is not None:
            for rec in self._data[fncName[1]]:
              countPerAxis[rec] = countPerAxis.get(rec, -1) + 1
              orderSeries.append(countPerAxis[rec])
            self._data['order'] = orderSeries
          continue

        args = list(fncName)[1:]
        fncName = "ares_%s" % fncName[0].replace("-", "")
        factory['fncs'][fncName]['class'].extendColumns(self._schema, args)
      if systemInfo is not None:
        for category, sysCols in systemInfo.items():
          args = factory['fncs'][fncName]['class'].extendArgs(category, args, sysCols)
      self._schema['fncs'].append({'name': fncName, 'args': args})
    return self

  def post(self, fncNames):
    """
    :category: Formatting
    :rubric: JS
    :type: Front End
    :dsc:

    :return:
    """
    if not isinstance(fncNames, list):
      fncNames = [fncNames]
    for fncName in fncNames:
      args = None
      if isinstance(fncName, tuple):
        # This mean that some parameters are expected in the configuration
        args = list(fncName)[1:]
        fncName = fncName[0].replace("-", "")
      self._schema['post'].append({'name': "ares_%s" % fncName, 'args': args})
    return self

  def getJs(self, fncs=None):
    """
    :category: Formatting
    :rubric: JS
    :type: Front End
    :dsc:

    :return:
    """
    val = self.jqId
    if fncs is not None:
      self.post(fncs)
    fncContentTemplate = ["var result = []", "if (data !== null){%s} else {data = []}", "return result"]
    if self._schema['debug']:
      fncContentTemplate = ["var t0 = performance.now()", "var result = []", "if (data !== null){%s} else {data = []}",
          "console.log('Function: '+ arguments.callee.name +', count records: '+ data.length +', time: '+ (performance.now()-t0) +' ms.')",
          "console.log('Arguments -')",
          "for(var i = 1; i < arguments.length; i++){console.log('   ' + i +': '+ JSON.stringify(arguments[i]))}",
          "console.log()",
          "console.log('Input Data -')", "console.log(arguments[0])", "console.log()",
          "console.log('Output Data -')", "console.log(result)", "console.log()", "return result"]
    fncContentTemplate = "; ".join(fncContentTemplate)
    # Add the different filtering rules
    filters, jsFncs = [],  self._schema['fncs']
    for k, v in self.aresObj.jsSources.get(self.jqId, {}).get('filters', {}).items():
      if k == 'allIfEmpty':
        v = list(v)
      filters.append("'%s': %s" % (k, v))
    if len(filters) > 0:
      jsFncs = [{'args_js': ['{%s}' % ", ".join(filters)], 'name': 'ares_filter'}] + jsFncs
    # Set all the Javascript functions
    for fnc in jsFncs:
      if fnc['name'] in factory['fncs']:
        if hasattr(self.aresObj, "jsGlobal"):
          self.aresObj.jsGlobal.fnc("%s(%s)" % (fnc['name'], factory['fncs'][fnc['name']]['params']), fncContentTemplate % factory['fncs'][fnc['name']]['text'])
        else:
          print("function %s(%s) {var result = []; %s;return result; };" % (fnc['name'], factory['fncs'][fnc['name']]['params'], factory['fncs'][fnc['name']]['text']))
      if fnc.get('args') is not None:
        val = "%s(%s, %s)" % (fnc['name'], val, ", ".join([json.dumps(a) for a in fnc['args']]))
      elif fnc.get('args_js') is not None:
        # TODO: Remove this hack done for the filter function
        val = "%s(%s, %s)" % (fnc['name'], val, ", ".join([a for a in fnc['args_js']]))
      else:
        val = "%s(%s)" % (fnc['name'], val)
    # Container formatting
    if self._schema['out'] is not None:
      if self._schema['out']['name'] in factory['objs']:
        if hasattr(self.aresObj, "jsGlobal"):
          self.aresObj.jsGlobal.fnc("Ares%s(%s)" % (self._schema['out']['name'], factory['objs'][self._schema['out']['name']]['params']), fncContentTemplate % factory['objs'][self._schema['out']['name']]['text'])
        else:
          print("function Ares%s(%s) {%s};" % (self._schema['out']['name'], fncContentTemplate % factory['objs'][self._schema['out']]['params'], factory['objs'][self._schema['out']['name']]['text']))
      params = [json.dumps(a) for a in self._schema['out']['params']]
      val = "Ares%s(%s, %s)" % (self._schema['out']['name'], val, ", ".join(params))
    # Post process function
    for fnc in self._schema['post']:
      fncName = fnc['name']
      if fncName in factory['fncs']:
        if hasattr(self.aresObj, "jsGlobal"):
          self.aresObj.jsGlobal.fnc("%s(%s)" % (fncName, factory['fncs'][fncName]['params']), fncContentTemplate % factory['fncs'][fncName]['text'])
        else:
          print("function %s(%s) {%s" % (fncName, factory['fncs'][fncName]['params'], fncContentTemplate % factory['fncs'][fncName]['text']))
      if fnc['args']:
        val = "%s(%s, %s)" % (fncName, val, ", ".join([json.dumps(a) for a in fnc['args']]))
      else:
        val = "%s(%s)" % (fncName, val)
    return val

  def toTsv(self, process='input'):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    :return: A String with the Javascript function to be used
    """
    tsv = ares.Lib.js.objects.jsText.JsTextTsv()
    self.aresObj.jsGlobal.fnc("ToTsv(data, colNames)", "%s; return result" % tsv.value)
    return "ToTsv(%s, %s)" % (self.jqId, json.dumps(list(self._schema['keys'] | self._schema['values'])))

  # --------------------------------------------------------------------------------------------------------------
  #
  #                                             Testing part
  # --------------------------------------------------------------------------------------------------------------
  def addTest(self, fncName, data, outpath=None):
    """
    :category:
    :type:
    :rubric:
    :dsc:

    """
    self.fncs(fncName)
    if outpath is None:
      outpath = os.path.join(os.path.dirname(__file__), "tests")
    fncName, module = self._fncs[0]['name'], factory['fncs'][self._fncs[0]['name']]['module'].split(".")[-1]
    testFilePath = os.path.join(outpath, "%s_%s.json" % (module, fncName))
    if os.path.exists(testFilePath):
      inFile = open(testFilePath)
      testObj = json.loads(inFile.read())
      inFile.close()
    else:
      testObj = {"fnc": fncName, "tests": {}, 'author': ''}
      for alias in self._fncs:
        testObj["def"] = "function %s(%s) {var result = []; %s ;return result; };" % (
          fncName, factory['fncs'][fncName]['params'], factory['fncs'][fncName]['text'])
        testObj['module'] = factory['fncs'][fncName]['module']
    #
    hashObj = ares.utils.AresSiphash.SipHash()
    testObj['tests'][hashObj.hashId(json.dumps(data))] = {'data': data, "time": time.time()}

    with open(r"%s\%s_%s.json" % (outpath, module, fncName), "w") as f:
      json.dump(testObj, f, indent=2)

  def doReg(self, moduleName, fncName, outpath=None):
    """
    :category:
    :type:
    :rubric:
    :dsc:

    """
    if outpath is None:
      outpath = os.path.join(os.path.dirname(__file__), "tests")
    testFilePath = os.path.join(outpath, "%s_%s.json" % (moduleName, fncName))
    inFile = open(testFilePath)
    testObj = json.loads(inFile.read())
    inFile.close()
    for testId, testDef in testObj['tests'].items():
      print("var data_%s = %s" % (testId, testDef['data']))
      print("%s(data_%s)" % (testObj['fnc'], testId))


def docEnum(aresObj, outStream, lang='eng'):
  """
  :category: Javascript
  :rubric: PY
  :type: Documentation
  """
  outStream.link("Breadcrumb definition", "")
  outStream.link("Markdown definition", "")
  outStream.link("RecordSets Functions", "")
  outStream.link("Date Functions", "")
  outStream.link("Charts Functions", "")
  outStream.link("Polyfill Functions", "")
  outStream.link("Regression Test", "")


if __name__ == "__main__":
  data = [
        {"name": "Olivier", "job": "BNP", "value": 11, "value2": 2},
        {"name": "Olivier", "job": "BNP", "value": 4, "value2": 3},
        {"name": "Aurelie", "job": "BNP", "value": 4, "value2": None},
      ]
  jsObj = Js(None, 'jsYoupi')
  jsObj.doReg('jsRecords', 'sum')
  #jsObj.addTest(('sum', ['name'], ['value']), data)
  #print( jsObj.fncs([('sum', ['name'], ['value']), ('rename', {'count': 'youpi'})]).output(('C3', [''], [''])).getJs() )

# data = [
#     {"name": "A", "job": "BNP", "value": 3, "value2": 2},
#     {"name": "A", "job": "BNP", "value": 4, "value2": 3},
#     {"name": "B", "job": "BNP", "value": 4, "value2": None},
#   ]
#
# jsObj = Js(None)
#
# # [("sum", ), "rename"])
# #jsObj.fncs( [ ("sum", ['name'], ['value']), ('rename', {"value": "label"} )] )
# #jsObj.fncs( [("count(distinct)", ['name', 'value2'] ), ('rename', {'count': 'youpi'}), ('C3', [''], ['']) ] )
# #jsObj.fncs( [("sum", ['name'], ['value', 'value2'] ) ] )
#
# print(os.path.dirname(__file__))
# outpath = r'C:\Users\olivier\Documents\youpi\ares\Lib\js\tests'
# #jsObj.fncs([("stats(Column)", 'value2')])
# jsObj.addTest("toMarkUp", data="test data **youpi**")
#
# #jsObj.output(('D3_bubble', ['value2'], 'name'))
# #jsObj.fncs( [("sum", ['name'], ['value', 'value2'] )] )
#
# # jsObj.test(outpath)
#
