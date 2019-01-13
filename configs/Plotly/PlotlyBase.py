#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


class Plotly(dict):
  """

  """
  name, chartCall, jsCls = 'Default configuration', None, 'Chart'
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {}

  def __init__(self, aresObj, data, seriesProperties):
    self.aresObj, self.seriesProperties = aresObj, seriesProperties
    self.data = self.transformation(data)
    for key, val in self._attrs.items():
      self.seriesProperties['static'][key] = val
    self.config()

  def config(self): pass

  @classmethod
  def transformation(cls, data):
    return data

  def _colors(self, cList, index=None):
    """

    :param cList:
    :param index:
    :return:
    """
    if index is not None:
      if not "marker" in self.__chart.seriesProperties["static"]:
        self.seriesProperties["static"]["marker"] = {'color': [cList]}
    else:
      for i in range(len(self.data._schema['out']['params'][0])):
        self.seriesProperties["dynamic"].setdefault(i, {})["marker"] = {'color': cList[i]}