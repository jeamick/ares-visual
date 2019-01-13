#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import json

from ares.configs.NVD3 import NVD3Base


class NVD3Line(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall, eventObject = 'Lines', 'lineChart', 'line', 'interactiveLayer'
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {'showYAxis': True, 'showXAxis': True, 'useInteractiveGuideline': True, 'showLegend': True, "legendPosition": True,
            'x': ("function(d) { return d.x; }", False), 'y': ("function(d) { return d.y; }", False)
            }

  @property
  def jsQueryData(self):
    return '''{event_code: '%(htmlId)s'}''' % {'htmlId': self.chartId}


class NVD3SparkLine(NVD3Base.NVD3):
  """
  :category: Chart
  :rubric: JS
  :type: Configuration
  """
  name, chartObj, chartCall = 'Spark Line (with Focus)', 'sparklinePlus', 'sparkline'
  # Please do not change this object, it will impact everything as dictionaries are mutable objects
  _attrs = {'showLastValue': True}

  def style(self, seriesAttr=None, recAttr=None):
    self.seriesStyle = '''
      values.forEach( function( rec )  { 
        var recAttr = %(recAttr)s;
        if ( recAttr.attr[rec[recAttr.data]] != undefined ) {
          for (var k in recAttr.attr[rec[recAttr.data]]) { rec[k] = recAttr.attr[rec[recAttr.data]][k] ; }
        }
      }) ''' % {'recAttr': json.dumps({} if recAttr is None else recAttr)}

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
