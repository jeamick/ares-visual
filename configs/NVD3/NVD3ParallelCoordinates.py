#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.configs.NVD3 import NVD3Base


class NVD3ParallelCoordinates(NVD3Base.NVD3):
  """ """
  name, chartObj, chartCall = 'Parallel Coordinates', 'parallelCoordinates', 'parallelCoordinates'
  convertFnc = ['NVD3LabelsYFormat']
  mocks = [
        {
            "name": "AMC Ambassador Brougham",
            "economy (mpg)": "13",
            "cylinders": "8",
            "displacement (cc)": "360",
            "power (hp)": "175",
            "weight (lb)": "3821",
            "0-60 mph (s)": "11",
            "year": "73"
        },
        {
          "name": "AMC Concord DL 6",
          "economy (mpg)": "20.2",
          "cylinders": "6",
          "displacement (cc)": "232",
          "power (hp)": "90",
          "weight (lb)": "3265",
          "0-60 mph (s)": "18.2",
          "year": "79"
        },
        {
          "name": "AMC Concord DL",
          "economy (mpg)": "18.1",
          "cylinders": "6",
          "displacement (cc)": "258",
          "power (hp)": "120",
          "weight (lb)": "3410",
          "0-60 mph (s)": "15.1",
          "year": "78"
        }
  ]

  def config(self):
    self.addAttr( {'lineTension': 0.8} )
    self.addAttr( 'dimensionNames', self.data.xAxis)
    #self.addAttr( 'dimensionFormats', '[d3.format("0.5f"), d3.format("e"), d3.format("g"), d3.format("d"), d3.format(""), d3.format("%"), d3.format("p")]', isPyData=False)

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