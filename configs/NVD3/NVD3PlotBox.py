#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.configs.NVD3 import NVD3Base


class NVD3PlotBox(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall = 'Box Plot', 'boxPlotChart', 'box'
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {'maxBoxWidth': 75, 'yDomain': [0, 500], 'staggerLabels': True}

  mocks = [
    {
      'label': "Sample A",
      'values': {
        'Q1': 120,
        'Q2': 150,
        'Q3': 200,
        'whisker_low': 115,
        'whisker_high': 210,
        'outliers': [50, 100, 225]
      },
    }
  ]
