#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json


class C3(dict):
  """

  """
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {}

  def __init__(self, aresObj, data, seriesProperties):
    self.aresObj, self.seriesProperties = aresObj, seriesProperties
    self.update({'data': {'x': '"x"'}, 'axis': {'x': {'type': '"category"'}}, 'grid': {}, 'regions': [], 'subchart': {},
                 'zoom': {}, 'legend': {}, 'tooltip': {}} )
    resolvedAttrs = {}
    self.rAttr(self._attrs, resolvedAttrs)
    self.update(resolvedAttrs)
    self.data = self.transformation(data)
    self.addAttr('type', self.chartType, 'data')
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

  def addAttr(self, key, val, subCategory=None, category=None, isPyData=True):
    if isPyData:
      val = json.dumps(val)
    if subCategory is not None:
      if category is not None:
        self.setdefault(category, {}).setdefault(subCategory, {})[key] = val
      else:
        self.setdefault(subCategory, {})[key] = val
    else:
      self[key] = val

  def delAttr(self, keys, subCategory=None, category=None):
    chart = self
    if subCategory is not None:
      chart = self.get(subCategory, {})
      if category is not None:
        chart = self.get(category, {}).get(subCategory, {})
    for attr in keys:
      if attr in chart:
        del chart[attr]

  @classmethod
  def transformation(cls, data):
    return data

  def donutText(self, text): pass