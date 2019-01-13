#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.configs.NVD3 import NVD3Base


class NVD3Bar(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall, eventObject = 'Bars', 'discreteBarChart', 'bar', 'discretebar'
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {
    'staggerLabels': True
  }


class NVD3HorizontalBar(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall = 'Horizontal Bars', 'multiBarHorizontalChart', 'hbar'


