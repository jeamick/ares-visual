#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json

from ares.Lib.js import AresJsEncoder


class ChartJs(dict):
  """

  """
  name, chartCall, jsCls = 'Default configuration', None, 'Chart'
  listAttributes = ['yAxes', 'xAxes', 'datasets']
  points = ['circle', 'triangle', 'rect', 'rectRounded', 'rectRot', 'cross', 'crossRot', 'star', 'line', 'dash']
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {
    'options': {'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
                'scales': {
                  'yAxes': [{
                    'ticks': {'display': True, 'beginAtZero': True}
                  }],
                  'xAxes': [{'ticks': {'display': True}}]}
                }
  }

  def __init__(self, aresObj, data, seriesProperties):
    self.aresObj, self.seriesProperties = aresObj, seriesProperties
    resolvedAttrs = {}
    self.rAttr(self._attrs, resolvedAttrs)
    self.update(resolvedAttrs)
    self['type'] = json.dumps(self.chartObj)
    self.data = self.transformation(data)
    self.config()

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
      if isinstance(srcVals, tuple):
        srcVals = json.dumps(srcVals[0]) if srcVals[1] else srcVals[0]

      if srcKey is not None:
        if isinstance(srcVals, str):
          # TODO: To be tested in Python 3
          dstVals[srcKey] = srcVals
        else:
          dstVals[srcKey] = json.dumps(srcVals)
      elif isinstance(dstVals, list):
        dstVals.append(json.dumps(srcVals))

  def config(self):
    """
    :category: Chart Series Properties
    :rubric: JS
    :type: Configuration
    :dsc:
      Extra configuration function to change the data options. Those parameters will be used on the javascript part
      when the final Javascript chart object will be passed to the charting library.
    """
    pass

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
    if isPyData:
      val = json.dumps(val, cls=AresJsEncoder.AresEncoder)

    if tree is not None:
      if not category in self:
        self[category] = {}
      chartLocation = self[category]
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

  def dataSetType(self, chartType, seriesId):
    """

    """
    self.addAttr('type', chartType)