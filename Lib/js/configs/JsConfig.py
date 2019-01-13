#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import json
import importlib
import inspect
import sys

from ares.Lib.js import AresJsEncoder

factory = None


def getConfigs(libraries):
  """
  :category: Factory
  :rubric: JS
  :type: Configuration
  :dsc:
    Load the factory with all the different javascript configuration for the different HTML components.
    Some components like charts, tables, pivot and lists are bespoke and would require extra tuning according to the need.
    This module in the framework will segregate all the different official configurations. Some bespoke ones can be
    added in the reports using the available hooks for each type of components
  :return: The content of the factory
  """
  global factory

  if factory is None:
    tmpFactory = {}
    for libConfig in libraries:
      chartMod = importlib.import_module('ares.Lib.js.configs.JsConfig%s' % libConfig)
      for name, chartCls in inspect.getmembers(sys.modules[chartMod.__name__]):
        chartAlias = getattr(chartCls, 'alias', None)
        if chartAlias is not None:
          if chartAlias in tmpFactory.get(libConfig, {}):
            raise Exception("Duplicated Name - Chart %s in %s cannot be replaced !!!" % (chartAlias, libConfig))

          tmpFactory.setdefault(libConfig, {})[chartAlias] = chartCls
    factory = tmpFactory
  return factory


def getConfig(pyCls, chartFam):
  """
  :category: Chart Bespoke Configuration
  :rubric: JS
  :type: Framework Extension
  :example: aresObj.addChartConfig(JsTestHBar, 'ChartJs')
  :dsc:
    Entry point to allow the add of bespoke configurations. Those configurations should be linked to an alias which has
    to be unique. From this entry point it is not possible to update existing configurations.
    Those configurations should follow the defined class structure in order to be then easily added to the framework in the
    next release.
    The entry point of this function in the framework is in the function aresObj.addChartConfig in the framework
  """
  chartMod = importlib.import_module('ares.Lib.js.configs.JsConfig%s' % chartFam)

  return type(pyCls.__name__, (pyCls, chartMod.JsBase), {})


class JsConfig(dict):
  """
  :category: Javascript Wrapper
  :rubric: JS
  :type: System
  :dsc:
    Base class in charge of the conversion of Python configurations to Javascript ones.
    Those configurations defined on the Python side will only be used and visible on the Javascript.
    This class will build a dictionary of valid parameters for the Javascript layer.

    ## Class Parameters

      - aresObj: The uniq AReS object, shared with all the different objects in the framework
      - seriesProperties: Dictionary with configuration to be added after the Javascript data transformation to the object
      - data: The Python data structure which will be added to the data section of the Javascript chart

    ## Special static class variables

    Those variable are properties of the class and should not be changed directly. Some methods are available
    in order to add bespoke configuration to the chart or to the series like addAttr() and addSeriesAttr().
    If something seems to be missing, please never change those variable and either create a new bespoke configuration
    or talk to your IT team.

      - _attrs, Chart properties and styles
      - _statics, parameters added to each series at the end of the data build

    The different Javascript structure are defined by the charting libraries
  """

  def __init__(self, aresObj, data, seriesProperties):
    self.aresObj, self.seriesProperties = aresObj, seriesProperties
    resolvedAttrs = {}
    self.rAttr(self._attrs, resolvedAttrs)
    if getattr(self, '_statics', None) is not None:
      seriesProperties.setdefault('static', {}).update(self._statics)
    self.update(resolvedAttrs)
    self.data = self.transformation(data)
    self.config()

  def config(self): pass

  def rAttr(self, srcVals, dstVals, srcKey=None):
    """
    :category:
    :rubric: PY
    :type: System
    :dsc:

    """
    if isinstance(srcVals, dict):
      for key, val in srcVals.items():
        if isinstance(val, dict):
          dstVals[key] = {}
          self.rAttr(val, dstVals[key])
        else:
          self.rAttr(val, dstVals, key)
    elif isinstance(srcVals, list):
      dstVals[srcKey] = []
      for val in srcVals:
        dstVals[srcKey].append({})
        self.rAttr(val, dstVals[srcKey][-1])
    else:
      if srcKey is not None:
        if isinstance(srcVals, str):
          if srcVals.startswith("function") or srcVals.startswith("JSON.stringify"):
            dstVals[srcKey] = srcVals
          else:
            dstVals[srcKey] = json.dumps(srcVals)
        else:
          dstVals[srcKey] = json.dumps(srcVals)
      elif isinstance(dstVals, list):
        dstVals.append(json.dumps(srcVals))

  def toJs(self, options=None): return self

  @classmethod
  def transformation(cls, data):
    """
    :category: Data Transformation
    :rubric: PY
    :type: Transformation
    :dsc:
      Data transformation for the DataFrame. Using this function might create a new DataFrame. Thus a new Javascript
      object will be created and the logic within the global filters might not work correctly.
      If you use this, please make it obvious to ensure other users might not be surprised
    """
    return data

  def addAttr(self, key, val, tree=None, category=None, isPyData=True):
    if isinstance(key, dict):
      for k, v in key.items():
        self.addAttr.addAttr(k, v, category=category, isPyData=isPyData)

    if isPyData:
      val = json.dumps(val, cls=AresJsEncoder.AresEncoder)
    if category is None and tree is not None:
      category, tree = tree, None
    if tree is not None:
      chartLocation = self[category]
      if not isinstance(tree, list):
        tree = [tree]
      for subCategory in tree:
        if isinstance(subCategory, tuple):
          subCategory, subCategoryIndex = subCategory
        else:
          subCategory, subCategoryIndex = subCategory, 0
        if subCategory in self.listAttributes:
          if not subCategory in chartLocation:
            chartLocation[subCategory] = []
            for i in range(subCategoryIndex + 1):
              chartLocation[subCategory].append({})
          if len(chartLocation[subCategory]) < subCategoryIndex + 1:
            for i in range(subCategoryIndex + 1):
              if i not in chartLocation[subCategory]:
                chartLocation[subCategory].append({})
          chartLocation = chartLocation[subCategory][subCategoryIndex]
        else:
          if not subCategory in chartLocation:
            chartLocation[subCategory] = {}
          chartLocation = chartLocation[subCategory]
      if isinstance(chartLocation, list):
        chartLocation[0][key] = val
      else:
        chartLocation[key] = val
    elif category is not None:
      self.setdefault(category, {})[key] = val
    else:
      self[key] = val

  def delAttr(self, keys, tree=None, category=None):
    """ """
    chart = self
    if tree is not None:
      chartLocation = self.get(category, {})
      for subCategory in tree:
        chartLocation = chartLocation.get(subCategory, {})
      chart = chartLocation
    if category is not None:
      chart = self.get(category, {})
    for attr in keys:
      if attr in chart:
        del chart[attr]

  def _colors(self, cList, index=None):
    """
    :category: Chart Series Colors
    :rubric: JS
    :type: Configuration
    :dsc:

    """
    if index is None:
      for i in range(len(self.data._schema['values'])):
        if len(cList) > i:
          self.seriesProperties['dynamic'].setdefault(i, {})['backgroundColor'] = cList[i]
    else:
      self.seriesProperties['dynamic'].setdefault(index, {})['backgroundColor'] = cList



if __name__ == "__main__":
  print(getConfigs(['ChartJs']))