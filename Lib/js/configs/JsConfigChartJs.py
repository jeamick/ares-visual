#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.js.configs import JsConfig
from ares.Lib.css import CssBaseColor


class JsBase(JsConfig.JsConfig):
  """ Base Class for the ChartJs Charts """
  listAttributes = ['yAxes', 'xAxes', 'datasets']
  jsCls = 'Chart'
  jsType = None


# ---------------------------------------------------------------------------------------------------------
#                                          CHARTJS Configurations
# ---------------------------------------------------------------------------------------------------------
class JsPie(JsBase):
  """ """
  alias = 'pie'
  name = 'Pie Chart'
  reference = 'https://www.chartjs.org/docs/latest/charts/doughnut.html'
  _attrs = {
    'type': 'pie',
    'options': {'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True}, 'scaleShowLabels': False,
                'plugins': {'labels': {'render': 'label', 'position': 'outside', 'fontColor': 'red'}},
                'scales': {
                 'yAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}],
                 'xAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}]}}}

  def config(self):
    pass
    # self.aresObj.jsImports.add('chartjs-pie-labels')

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
          self.seriesProperties['dynamic'].setdefault(i, {})['backgroundColor'] = cList
    else:
      self.seriesProperties['dynamic'].setdefault(index, {})['backgroundColor'] = cList


class JsDonut(JsPie):
  """ """
  alias = 'donut'
  name = 'Donut Chart'
  reference = 'https://www.chartjs.org/docs/latest/charts/doughnut.html'
  _attrs = {
    'type': 'doughnut',
    'options': {'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
                'scaleShowLabels': False,
                'scales': {
                  'yAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}],
                  'xAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}]}}}


class JsLine(JsBase):
  """ """
  alias = 'line'
  name = 'Basic Line Chart'
  reference = 'https://www.chartjs.org/docs/latest/charts/line.html'
  _statics = {'fill': False}
  _attrs = {
    'type': 'line',
    'options':
      {'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
          'scaleShowLabels': True,
          'scales': {
            'yAxes': [{'ticks': {'display': True, 'beginAtZero': True}, 'gridLines': {'display': True}}],
            'xAxes': [{'ticks': {'display': True, 'beginAtZero': True}, 'gridLines': {'display': True}}]}}}

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
          self.seriesProperties['dynamic'].setdefault(i, {})['borderColor'] = cList[i]
    else:
      self.seriesProperties['dynamic'].setdefault(index, {})['backgroundColor'] = cList
      self.seriesProperties['dynamic'].setdefault(index, {})['borderColor'] = cList

      
class JsArea(JsBase):
  """ """
  alias = 'area'
  name = 'Line (Fill Start)'
  reference = 'https://www.chartjs.org/docs/latest/charts/area.html'
  _statics = {'fill': True}
  _attrs = {
    'type': 'line',
    'options':
      {'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
          'scaleShowLabels': True,
          'scales': {
            'yAxes': [{'ticks': {'display': True, 'beginAtZero': True}, 'gridLines': {'display': True}}],
            'xAxes': [{'ticks': {'display': True, 'beginAtZero': True}, 'gridLines': {'display': True}}]}}}

  def _colors(self, cList, index=None):
    """
    :category: Chart Series Colors
    :rubric: JS
    :type: Configuration
    :dsc:

    """
    gbList = ["rgba(%s,%s,%s,0.3)" % tuple(CssBaseColor.CssColorMaker.getHexToRgb(val)) for val in cList]
    if index is None:
      for i in range(len(self.data._schema['out']['params'][0])):
        if len(cList) > i:
          self.seriesProperties['dynamic'].setdefault(i, {})['backgroundColor'] = gbList[i]
          self.seriesProperties['dynamic'].setdefault(i, {})['borderColor'] = cList[i]
    else:
      self.seriesProperties['dynamic'].setdefault(index, {})['backgroundColor'] = gbList
      self.seriesProperties['dynamic'].setdefault(index, {})['borderColor'] = cList


class JsAreaEnd(JsArea):
  """ """
  alias = 'area-end'
  name = 'Line (Fill End)'
  reference = 'https://www.chartjs.org/docs/latest/charts/area.html'
  _statics = {'fill': 'end'}


class JsSteppedLine(JsBase):
  """ """
  alias = 'step'
  name = 'Stepped Line Chart'
  reference = 'https://www.chartjs.org/docs/latest/charts/line.html'
  _statics = {'fill': False, 'steppedLine': True}
  _attrs = {
    'type': 'line',
    'options':
      {'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
          'scaleShowLabels': True,
          'scales': {
            'yAxes': [{'ticks': {'display': True, 'beginAtZero': True}, 'gridLines': {'display': True}}],
            'xAxes': [{'ticks': {'display': True, 'beginAtZero': True}, 'gridLines': {'display': True}}]}}}


class JsBar(JsBase):
  """ Configuration for a Bars Chart in ChartJs """
  alias = 'bar'
  name = 'Bars'
  reference = 'https://www.chartjs.org/docs/latest/charts/bar.html'
  _attrs = {
    'type': 'bar',
    'options': {
        'maintainAspectRatio': False,
        'responsive': True,
        'legend': {'display': True},
                   'scales': {
                      'yAxes': [{'ticks': {'display': True, 'beginAtZero': True}}],
                      'xAxes': [{'ticks': {'display': True}}]}}
  }


class JsHBar(JsBase):
  """ Configuration for a Horizontal Bars Chart in ChartJs """
  alias = 'hbar'
  name = 'Horizontal Bars'
  reference = 'https://www.chartjs.org/docs/latest/charts/bar.html'
  _attrs = {
      'type': 'horizontalBar',
      'options':
        {'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
            'scales': {
                'yAxes': [{'ticks': {'display': True, 'beginAtZero': True}}],
                'xAxes': [{'ticks': {'display': True, 'beginAtZero': True}}]}}}


class JsMultiBar(JsBase):
  """ """
  alias = 'multi'
  name = 'Multi Bars Chart'
  reference = ''
  _attrs = {'options': {
              'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
              'scales': {
                'yAxes': [{'ticks': {'display': True, 'beginAtZero': True}}],
                'xAxes': [{'ticks': {'display': True}}]}}}

  #def dataSetType(self, chartType, seriesId):
  #  self.seriesProperties['dynamic'][seriesId] = {'type': chartType, 'fill': False}


class JsScatter(JsBase):
  """ """
  alias = 'scatter'
  name = 'Scatter Chart'
  jsType = 'bubble'
  reference = 'https://www.chartjs.org/docs/latest/charts/scatter.html'
  _statics = {'pointStyle': 'circle'}
  _attrs = {
    'type': 'scatter',
    'options':
      {'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
       'scales': {
         'yAxes': [{'ticks': {'display': True, 'beginAtZero': True}, 'gridLines': {'display': True}}],
         'xAxes': [{'ticks': {'display': True, 'beginAtZero': True},
                    'gridLines': {'display': True}}]}}}


class JsBubble(JsBase):
  """ """
  alias = 'bubble'
  name = 'Bubble Chart'
  reference = 'https://www.chartjs.org/docs/latest/charts/bubble.html'
  _attrs = {
    'type': 'bubble',
    'options': {
      'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
      'scales': {
        'yAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}],
        'xAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}]}}}


class JsPolar(JsBase):
  """ """
  alias = 'polar'
  name = 'Polar Chart'
  reference = 'https://www.chartjs.org/docs/latest/charts/polar.html'
  _attrs = {
    'type': 'polarArea',
    'options': {
      'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
      'scales': {
        'yAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}],
        'xAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}]}}}

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
          self.seriesProperties['dynamic'].setdefault(i, {})['backgroundColor'] = cList
    else:
      self.seriesProperties['dynamic'].setdefault(index, {})['backgroundColor'] = cList


class JsRadar(JsBase):
  """ """
  alias = 'radar'
  name = 'Radar Chart'
  reference = 'https://www.chartjs.org/docs/latest/charts/radar.html'
  _attrs = {
    'type': 'radar',
    'options': {'maintainAspectRatio': False, 'responsive': True, 'legend': {'display': True},
        'scaleShowLabels': False,
        'scales': {
          'yAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}],
          'xAxes': [{'ticks': {'display': False}, 'gridLines': {'display': False}}]}}}

  def _colors(self, cList, index=None):
    """
    :category: Chart Series Colors
    :rubric: JS
    :type: Configuration
    :dsc:

    """
    rgbList = ["rgba(%s,%s,%s,0.3)" % tuple(CssBaseColor.CssColorMaker.getHexToRgb(val)) for val in cList]
    if index is None:
      for i in range(len(self.data._schema['out']['params'][0])):
        self.seriesProperties['dynamic'].setdefault(i, {})['backgroundColor'] = rgbList[i]
        self.seriesProperties['dynamic'].setdefault(i, {})['pointBackgroundColor'] = cList[i]
        self.seriesProperties['dynamic'].setdefault(i, {})['borderColor'] = cList[i]
        self.seriesProperties['dynamic'].setdefault(i, {})['borderWidth'] = 1
    else:
      self.seriesProperties['dynamic'].setdefault(index, {})['backgroundColor'] = rgbList[index]
      self.seriesProperties['dynamic'].setdefault(index, {})['pointBackgroundColor'] = cList[index]
      self.seriesProperties['dynamic'].setdefault(index, {})['borderColor'] = cList[index]
      self.seriesProperties['dynamic'].setdefault(index, {})['borderWidth'] = 1




if __name__ == "__main__":
  print (JsBar(None).toJs())