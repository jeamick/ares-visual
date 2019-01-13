#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
from ares.configs.NVD3 import NVD3Base


class NVD3MultiBar(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall = 'Multi Bars', 'multiBarChart', 'multi-bar'
  _attrs = {'reduceXTicks': True, 'showControls': True, 'groupSpacing': 0.1, 'rotateLabels': -15, 'showLegend': True}

  #def xAxisSort(self, htmlId):
  #  return "%(htmlId)s_data[0].values = %(htmlId)s_data[0].values.sort(keysrt('x', false)); ;" % {'htmlId': htmlId}


class NVD3MultiBarStacked(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall = 'Multi Bars', 'multiBarChart', 'multi-bar-stacked'
  _attrs = {'reduceXTicks': True, 'showControls': True, 'groupSpacing': 0.1, 'rotateLabels': -15, 'showLegend': True, 'stacked': True}

  def xAxisSort(self, htmlId):
    return "%(htmlId)s_data[0].values = %(htmlId)s_data[0].values.sort(keysrt('x', false)); ;" % {'htmlId': htmlId}


class NVD3MultiChart(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall = 'MultiCharts', 'multiChart', 'multi'
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {'showLegend': False}

  def style(self, seriesAttr=None, recAttr=None):
    self.seriesStyle = '''
      values.forEach( function( rec )  { 
        var seriesAttr = %(seriesAttr)s; var recAttr = %(recAttr)s;
        if( Object.keys(seriesAttr).length > 0) {
          if( seriesAttr[rec.key] != undefined ) {
            if ( seriesAttr[rec.key].type == undefined) { rec.type = 'line';} else { rec.type = seriesAttr[rec.key].type } ;
            if ( seriesAttr[rec.key].yAxis  == undefined) { rec.yAxis  = 1;} else { rec.yAxis = seriesAttr[rec.key].yAxis }; 
        
            for (var k in seriesAttr[rec.key]) { rec[k] = seriesAttr[rec.key][k]} }
          else { rec.type = 'line' ; rec.yAxis  = 1; }}
        else { rec.type = 'line' ; rec.yAxis  = 1;}
        
        if( Object.keys(recAttr).length > 0) {
          if ((recAttr.data == 'key') && ( rec.key in recAttr.attr) ) {
            rec.values.forEach( function(i) { 
              for (var k in recAttr.attr[rec.key]) { i[k] = recAttr.attr[rec.key][k] ; }
            })
          } else {
            rec.values.forEach( function(i) { 
              if ( recAttr.attr[i[recAttr.data]] != undefined ) {
                for (var k in recAttr.attr[i[recAttr.data]]) { i[k] = recAttr.attr[i[recAttr.data]][k] ; }
              }
            })
          }
        }
      })  ''' % {'seriesAttr': json.dumps({} if seriesAttr is None else seriesAttr), 'recAttr': json.dumps({} if recAttr is None else recAttr)}


class NVD3Scatter(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall, eventObject = 'Scatter', 'scatterChart', 'scatter', 'scatter'
  shapes = ['thin-x', 'circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square']
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {'showDistX': True, 'showDistY': True, 'duration': 300}

  @property
  def jsQueryData(self):
    return '''{  
          event_index: event.point.x, event_label: event.point.label, 
          event_val: event.point.y, event_code: '%(htmlId)s' }''' % {'htmlId': self.chartId}


class NVD3Area(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall = 'Stacked Area', 'stackedAreaChart', 'area'
  eventObject = 'stacked'
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {'duration': 300, 'showLegend': True}

  @property
  def jsQueryData(self):
    return '''{  
        event_index: event.point.x, event_label: event.point.label, 
        event_val: event.point.y, event_code: '%(htmlId)s' }''' % {'htmlId': self.chartId}

