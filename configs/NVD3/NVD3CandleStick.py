#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.configs.NVD3 import NVD3Base


class NVD3CandleStick(NVD3Base.NVD3):
  """ """
  mocks = [
    {"date": 15854, "open": 165.42, "high": 165.8, "low": 164.34, "close": 165.22, "volume": 160363400, "adjusted": 164.35},
    {"date": 15855, "open": 165.35, "high": 166.59, "low": 165.22, "close": 165.83, "volume": 107793800, "adjusted": 164.96},
  ]
  name, chartObj, chartCall = 'Candles Stick', 'candlestickBarChart', 'candlestick'
  convertFnc = ['NVD3LabelsYFormat']

  def config(self):
    self.addAttr( {'x': "function(d) { return d.date }", 'y': "function(d) { return d['close'] }"}, isPyData=False)
    self.axis.setdefault('yAxis', {})['axisLabel'] = "'Stock Price'"
    self.axis['yAxis']['tickFormat'] = "function(d,i){ return '$' + d3.format(',.1f')(d); }"
    self.axis.setdefault('xAxis', {})['axisLabel'] = "'Dates'"
    self.axis['xAxis']['tickFormat'] = "function(d) { alert(d) ;return d3.time.format('%x')(new Date(new Date() - (20000 * 86400000) + (d * 86400000)));}"

