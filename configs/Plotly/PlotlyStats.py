#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.AresImports import requires

# Will automatically add the external library to be able to use this module
ares_pandas = requires("pandas", reason='Missing Package', install='pandas', autoImport=True, sourceScript=__file__)
ares_numpy = requires("numpy", reason='Missing Package', install='numpy', sourceScript=__file__)

from ares.configs.Plotly import PlotlyBase
from ares.Lib import AresImports
ares_scipy_stats = AresImports.requires(name='scipy.stats', reason='Missing Package', install='scipy', sourceScript=__file__)

from ares.Lib.js import AresJs


class PlotlyKernelDensityEstimate(PlotlyBase.Plotly):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartCall, chartObj = 'Kernel Density Estimate', 'kde', 'scatter'
  step = 500
  # Please do not change this object, it will impact everything as dictionaries are mutable objects

  def transformation(self, data):
    kdeSeries = {}
    seriesNames = list(data._schema['values'])
    for series in seriesNames:
      x = ares_numpy.linspace(min(data._data[series]), max(data._data[series]), self.step)
      kdeSeries[series] = ares_scipy_stats.gaussian_kde(list(data._data[series]))(x)

    newDff = []
    for i in range(self.step):
      row = {'x': i}
      for series in seriesNames:
        row[series] = kdeSeries[series][i]
      newDff.append(row)

    data = AresJs.Js(self.aresObj, self.aresObj.df(newDff, htmlCode="%s_kde" % data._jqId), keys=['x'], values=seriesNames)
    return data.output('Plotly', self.chartCall, (seriesNames, 'x'))

