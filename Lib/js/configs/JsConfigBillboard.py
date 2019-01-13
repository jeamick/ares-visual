#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.js.configs import JsConfig


DSC = {

}


class JsBase(JsConfig.JsConfig):
  """ Base Class for the C3 Charts """
  listAttributes = []
  jsCls = 'Chart'


# ---------------------------------------------------------------------------------------------------------
#                                          C3 Configurations
# ---------------------------------------------------------------------------------------------------------
class JsBar(JsBase):
  """ Configuration for a Bars Chart in C3 """
  alias = 'bar'
  name = 'Bars'
  reference = 'https://c3js.org/samples/chart_bar.html'
  _attrs = {
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'data': {'x': 'x', 'type': 'bar'},
    'regions': [],
    'axis': {'x': {'type': '"category"'}},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': True},
    'tooltip': {}
  }


class JsHBar(JsBase):
  """ Configuration for a Horizontal Bars Chart in C3 """
  alias = 'hbar'
  name = 'Horizontal Bars'
  reference = 'https://c3js.org/samples/chart_bar.html'
  _attrs = {
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'data': {'x': 'x', 'type': 'bar'},
    'regions': [],
    'axis': {'x': {'type': 'category'}, 'rotated': True},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': True},
    'tooltip': {}
  }


class JsScatter(JsBase):
  """ Configuration for a Basic line Chart in C3 """
  alias = 'scatter'
  name = 'Scatter Chart'
  reference = 'https://c3js.org/samples/chart_scatter.html'
  _attrs = {
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'data': {'x': 'x', 'type': 'scatter'},
    'regions': [],
    'area': {},
    'axis': {'x': {'tick': {'culling': {'max': 10}}, 'type': 'category'}},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False},
    'tooltip': {},
    'point': {},
    'fill': None
  }


class JsLine(JsBase):
  """ Configuration for a Basic line Chart in C3 """
  alias = 'line'
  name = 'Line Chart'
  reference = 'https://c3js.org/samples/simple_multiple.html'
  _attrs = {
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'data': {'x': 'x'},
    'regions': [],
    'area': {},
    'axis': {'x': {'tick': {'culling': {'max': 10}}, 'type': 'category'}},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False},
    'tooltip': {},
    'fill': None
  }


class JsSpline(JsBase):
  """ Configuration for a Basic line Chart in C3 """
  alias = 'spline'
  name = 'Spline Chart'
  reference = 'https://c3js.org/samples/chart_spline.html'
  _attrs = {
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'data': {'x': 'x', 'type': 'spline'},
    'regions': [],
    'area': {},
    'axis': {'x': {'tick': {'culling': {'max': 10}}, 'type': 'category'}},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False},
    'tooltip': {},
    'fill': None
  }


class JsStep(JsBase):
  """ Configuration for a Basic line Chart in C3 """
  alias = 'step'
  name = 'Step Chart'
  reference = 'https://c3js.org/samples/chart_step.html'
  _attrs = {
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'data': {'x': 'x', 'type': 'step'},
    'regions': [],
    'area': {},
    'axis': {'x': {'tick': {'culling': {'max': 10}}, 'type': 'category'}},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False},
    'tooltip': {},
    'fill': None
  }


class JsArea(JsBase):
  """ """
  alias = 'area'
  name = 'Area Chart'
  reference = 'https://c3js.org/samples/chart_area.html'
  _attrs = {
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'data': {'x': 'x', 'type': 'area'},
    'regions': [],
    'area': {},
    'axis': {'x': {'tick': {'culling': {'max': 10}}, 'type': 'category'}},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False},
    'tooltip': {},
    'fill': None
  }


class JsAreaSpline(JsBase):
  """ """
  alias = 'area-spline'
  name = 'Area Spline Chart'
  reference = 'https://c3js.org/samples/chart_area.html'
  _attrs = {
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'data': {'x': 'x', 'type': 'area-spline'},
    'regions': [],
    'area': {},
    'axis': {'x': {'tick': {'culling': {'max': 10}}, 'type': 'category'}},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False},
    'tooltip': {},
    'fill': None
  }


class JsAreaStep(JsBase):
  """ """
  alias = 'area-step'
  name = 'Area Step Chart'
  reference = 'https://c3js.org/samples/chart_area.html'
  _attrs = {
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'data': {'x': 'x', 'type': 'area-step'},
    'regions': [],
    'area': {},
    'axis': {'x': {'tick': {'culling': {'max': 10}}, 'type': 'category'}},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False},
    'tooltip': {},
    'fill': None
  }


class JsPie(JsBase):
  """ Configuration for a Pie Chart in C3 """
  alias = 'pie'
  name = 'Pie Chart'
  reference = ''
  _attrs = {
    'data': {'x': 'x', 'type': 'pie'},
    'axis': {'x': {'type': 'category'}},
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False}
  }


class JsDonut(JsBase):
  """ Configuration for a Donut Chart in C3 """
  alias = 'donut'
  name = 'Donut Chart'
  reference = ''
  _attrs = {
    'data': {'x': 'x', 'type': 'donut'},
    'axis': {'x': {'type': 'category'}},
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False}
  }


class JsGauge(JsBase):
  """ Configuration for a Donut Chart in C3 """
  alias = 'gauge'
  name = 'Gauge Chart'
  reference = 'https://c3js.org/samples/chart_pie.html'
  _attrs = {
    'data': {'x': 'x', 'type': 'gauge'},
    'axis': {'x': {'type': 'category'}},
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False}
  }


class JsRadar(JsBase):
  """ Configuration for a Radar Chart in C3 """
  alias = 'radar'
  name = 'Radar Chart'
  reference = 'https://naver.github.io/billboard.js/demo/#Chart.RadarChart'
  _attrs = {
    'data': {'x': 'x', 'type': 'radar', 'labels': True},
    'axis': {},
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False}
  }


class JsBubble(JsBase):
  """ Configuration for a Bubble Chart in C3 """
  alias = 'bubble'
  name = 'Bubble Chart'
  reference = 'https://naver.github.io/billboard.js/demo/#Chart.BubbleChart'
  _attrs = {
    'data': {'x': 'x', 'type': 'bubble', 'labels': True},
    'axis': {'x': {'type': 'category'}},
    'bubble': {},
    'grid': {'x': {'show': True}, 'y': {'show': True}, 'enabled': True},
    'subchart': {'show': False},
    'legend': {'show': True},
    'zoom': {'enabled': False}
  }



if __name__ == "__main__":
  lineChart = JsLine(None, [], {})
  lineChart.addAttr('pattern', ['yellow'], 'color')
  print(lineChart)