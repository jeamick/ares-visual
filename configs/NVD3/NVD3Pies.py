#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.configs.NVD3 import NVD3Base


class NVD3Pie(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall, eventObject = 'Pie', 'pieChart', 'pie', 'pie'
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {'showLabels': True, 'labelsOutside': True, 'showLegend': True, "legendPosition": True,
            #'title': {'enable': True, 'text': "yfytfytf", 'css': {'color': 'black'}},
            'x': ("function(d) { return d.x; }", False), 'y': ("function(d) { return d.y; }", False)}

  @property
  def jsQueryData(self):
    return '''{  
        event_index: event.data.x, event_label: event.data.label, event_val: event.data.y, event_code: '%(htmlId)s' }''' % {'htmlId': self.chartId}

  def jsToTable(self):
    """ Convert the date from the chart to a table """
    return ''' 
      var tableData = {dom: 'Bfrtip', buttons: [
                {'extend': 'excelHtml5', 'className': 'py_cssdivhidden', 'title': '%(htmlId)s_excel'},
                {'extend': 'pdfHtml5', 'className': 'py_cssdivhidden', 'title': '%(htmlId)s_pdf'}], 
          data: [], columns: [], scrollY: "%(height)s", paging:false, searching:true, autoWidth:true };
      for (var j in values[0] ) { tableData.columns.push( {data: j, title: j } ) ; } ;
        values.forEach( function(rec, index) { tableData.data.push( rec ); }) ;
      ''' % {'height': self.height, 'htmlId': self.chartId}


class NVD3Donut(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall, eventObject = 'Donut', 'pieChart', 'donut', 'pie'
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {'showLabels': True, 'labelThreshold': .05, 'labelType': "percent", 'donut': True, 'donutRatio': 0.35,
           'labelsOutside': True, 'showLegend': True, "legendPosition": True,
           'x': ("function(d) { return d.x; }", False), 'y': ("function(d) { return d.y; }", False)
           }

  @property
  def jsQueryData(self):
    return '''{  
          event_index: event.data.x, event_label: event.data.label, event_val: event.data.y, event_code: '%(htmlId)s' }''' % { 'htmlId': self.chartId}

  def jsToTable(self):
    """ Convert the date from the chart to a table """
    return ''' 
      var tableData = {dom: 'Bfrtip', buttons: [
                {'extend': 'excelHtml5', 'className': 'py_cssdivhidden', 'title': '%(htmlId)s_excel'},
                {'extend': 'pdfHtml5', 'className': 'py_cssdivhidden', 'title': '%(htmlId)s_pdf'}], 
          data: [], columns: [], scrollY: "%(height)s", paging:false, searching:true, autoWidth:true };
      console.log(values) ; 
      for (var j in values[0] ) { tableData.columns.push( {data: j, title: j } ) ; } ;
        values.forEach( function(rec, index) { tableData.data.push( rec ); }) ;
      ''' % {'height': self.height, 'htmlId': self.chartId}


class NVD3Meter(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall, eventObject = 'Meter', 'pieChart', 'meter', 'pie'

  def config(self):
    self.addAttr({'showLabels': True, 'labelThreshold': .05, 'labelType': "percent", 'donut': True, 'donutRatio': 0.35, 'labelsOutside': True,
                  'showLegend': self.showLegend, "legendPosition": self.legendPosition})
    self.addAttr('x', "function(d) { return d.label; }", isPyData=False)
    self.addAttr('y', "function(d) { return d.y; }", isPyData=False)
    self.addAttr('startAngle', "function(d) { return d.startAngle/2 -Math.PI/2 }", isPyData=False)
    self.addAttr('endAngle', "function(d) { return d.endAngle/2 -Math.PI/2 }", isPyData=False)

  @property
  def jsQueryData(self):
    return '''{  
            event_index: event.data.x, event_label: event.data.label, event_val: event.data.y, event_code: '%(htmlId)s' }''' % { 'htmlId': self.chartId}

  def jsToTable(self):
    """ Convert the date from the chart to a table """
    return ''' 
      var tableData = {dom: 'Bfrtip', buttons: [
                {'extend': 'excelHtml5', 'className': 'py_cssdivhidden', 'title': '%(htmlId)s_excel'},
                {'extend': 'pdfHtml5', 'className': 'py_cssdivhidden', 'title': '%(htmlId)s_pdf'}], 
          data: [], columns: [], scrollY: "%(height)s", paging:false, searching:true, autoWidth:true };
      console.log(values) ; 
      for (var j in values[0] ) { tableData.columns.push( {data: j, title: j } ) ; } ;
        values.forEach( function(rec, index) { tableData.data.push( rec ); }) ;
      ''' % {'height': self.height, 'htmlId': self.chartId}


class NVD3Sunburst(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  mocks = [{
    "name": "Category1",
    "children": [
      {"name": "AgglomerativeCluster", "size": 3938},
      {"name": "AgglomerativeCluster", "size": 3812}
    ],
    "name": "Category2",
    "children": [
      {"name": "AgglomerativeCluster", "size": 3938},
      {"name": "AgglomerativeCluster", "size": 3812}
    ],
  }]
  name, chartObj, chartCall = 'Sunburst', 'sunburstChart', 'sunburst'
  convertFnc = ["NVD3XYFormat"]

  def config(self): pass