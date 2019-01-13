#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.js.configs import JsConfig


DSC = {

}


class JsBase(JsConfig.JsConfig):
  """ Base Class for the Plotly Charts """
  jsCls = 'Graph2d'
  reference = None  # The main link to get the documentation of this chart
  _statics = None  # Static configuration will be added to each dara set automatically
  jsType = None  # Attach the chart to a family for the data transformation
  _attrs = None
  jsQueryData = '{xaxis: event.time, column: event.value[0], src: event}'

  def __init__(self, aresObj, data, seriesProperties):
    super(JsBase, self).__init__(aresObj, data, seriesProperties)
    self.config()

  def config(self):
    if self._statics is not None:
      self.seriesProperties["static"].update(self._statics)

  @property
  def options(self):
    return self


# ---------------------------------------------------------------------------------------------------------
#                                          VIS Configurations
# ---------------------------------------------------------------------------------------------------------
class JsBar(JsBase):
  """ Configuration for a Bars Chart in Vis """
  alias = 'bar'
  name = 'Bars'
  _attrs = {'style': 'bar', 'moveable': False, 'drawPoints': True, 'stack': False, 'orientation': 'top',
            'barChart': {'align': 'center', 'sideBySide': True},
            'dataAxis': {'icons': True}}
  reference = "http://visjs.org/examples/graph2d/11_barsSideBySideGroups.html"


class JsLine(JsBase):
  """ Configuration for a Bars Chart in Vis """
  alias = 'line'
  name = 'Line Plot'
  _attrs = {'style': 'line', 'moveable': False, 'drawPoints': False}
  reference = "http://visjs.org/examples/graph2d/01_basic.html"


class JsScatter(JsBase):
  """ Configuration for a Bars Chart in Vis """
  alias = 'scatter'
  name = 'Scatter Plot'
  _attrs = {'style': 'points', 'sampling': True, 'sort': False, 'defaultGroup': 'Scatterplot', 'moveable': False}
  reference = "http://visjs.org/examples/graph2d/18_scatterplot.html"



#---------------------------------------------------------------------------------------------------------
#                           3D CHARTS
#
class JsSurface(JsBase):
  """ Configuration for a Box Chart in Vis """
  jsCls = 'Graph3d'
  alias = 'surface'
  name = 'Surface Plot'
  _attrs = {'style': 'surface', 'keepAspectRatio': True, 'verticalRatio': 0.5, 'showPerspective': True,
            'showGrid': True, 'showShadow': False, #, 'height': '100%'
            'backgroundColor': { 'strokeWidth': 0},
            }
  reference = "http://visjs.org/graph3d_examples.html"


class JsScatter3D(JsBase):
  jsCls = 'Graph3d'
  alias = 'scatter3d'
  _attrs = {'tooltip': True}
  reference = "http://visjs.org/examples/graph3d/07_dot_cloud_colors.html"


class JsBubble3D(JsBase):
  jsCls = 'Graph3d'
  alias = 'bubble'
  _attrs = {'style': 'dot-size', 'tooltip': True, 'keepAspectRatio': True, 'showPerspective': True}
  reference = "http://visjs.org/examples/graph3d/07_dot_cloud_colors.html"


class JsGroup3D(JsBase):
  alias = 'series3d'
  jsType = 'bubble'
  _attrs = {'style': 'dot-color', 'keepAspectRatio': True, 'showPerspective': True, 'verticalRatio': 0.5, 'tooltip': True,
            'showGrid': True, 'showShadow': False, 'legendLabel': 'color value', 'showLegend': False}
  reference = "http://visjs.org/examples/graph3d/07_dot_cloud_colors.html"


class JsLine3D(JsScatter3D):
  jsCls = 'Graph3d'
  alias = 'line3d'
  _attrs = {'style': 'line', 'tooltip': True}
  reference = "http://visjs.org/examples/graph3d/05_line.html"


class JsBar3D(JsScatter3D):
  jsCls = 'Graph3d'
  alias = 'bar3d'
  _attrs = {'style': 'bar', 'tooltip': True}
  reference = "http://visjs.org/examples/graph3d/12_custom_labels.html"


class JsBarColor3D(JsScatter3D):
  alias = 'barSeries3d'
  jsType = 'bubble'
  _attrs = {'style': 'bar-color', 'tooltip': True}
  reference = "http://visjs.org/examples/graph3d/12_custom_labels.html"


#---------------------------------------------------------------------------------------------------------
#                           TIMELINE CHARTS
#
class JsTimeLine(JsBase):
  alias = 'timeline'
  jsCls = 'Timeline'
  name = 'Basic Timeline'
  reference = "http://visjs.org/examples/timeline/basicUsage.html"



#---------------------------------------------------------------------------------------------------------
#                           NETWORK CHARTS
#
class JsNetwork(JsBase):
  jsCls = 'Network'
  alias = 'network'
  name = 'Basic Network'
  reference = "http://visjs.org/examples/network/basicUsage.html"