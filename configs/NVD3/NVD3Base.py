#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json


class NVD3(dict):
  name, chartObj, chartCall = 'Default Configuration', None, None
  convertFnc, eventObject, seriesStyle = None, 'multibar', ''
  _attrs = {} # Please do not change this object, it will impact everything as dictionaries are mutable objects
  priorities = ['color', 'showValues', 'x', 'y', 'interpolate']

  def __init__(self, aresObj, data, htmlId):
    self.aresObj, self.chartId, self.axis = aresObj, htmlId, {}
    self.data = self.transformation(data)
    for key, pyVal in self._attrs.items():
      (val, isPyData) = pyVal if isinstance(pyVal, tuple) else (pyVal, True)
      self.addAttr(key, val, isPyData=isPyData)
    self.config()

  def config(self): pass

  @classmethod
  def transformation(cls, data):
    return data

  @property
  def jsQueryData(self):
    return '''{  
      event_index: event.data.x, event_name: event.data.key, event_label: event.data.label, 
      event_val: event.data.y, event_code: '%(htmlId)s' }''' % {'htmlId': self.chartId}

  @property
  def jsQueryData(self):
    return "{'event_index': event.data.x, 'value': event.data.y, 'name': event.data.key, 'label': event.data.label}" % { 'htmlId': self.chartId}

  def jsChartDef(self):
    if self.chartObj is None:
      raise Exception("Probleme in the class, chartObj should be defined")

    return 'nv.models.%s()' % self.chartObj

  def addAttr(self, key, val=None, category=None, isPyData=True):
    if isinstance(key, dict):
      for k, v in key.items():
        if isPyData:
          v = json.dumps(v)
        if category is not None:
          self.setdefault(category, {})[k] = v
        else:
          self[k] = v
    else:
      if isPyData:
        val = json.dumps(val)
      if category is not None:
        self.setdefault(category, {})[key] = val
      else:
        self[key] = val

  def delAttr(self, keys, category=None):
    chart = self.get(category, {}) if category is not None else self
    for attr in keys:
      if attr in chart:
        del chart[attr]

  def interpolate(self, val="basis"): self.addAttr('interpolate', val)

  def style(self, seriesAttr=None, recAttr=None):
    # style( {'C': {'shape': 'triangle-up'} },  {'data': 'label', 'attr': {'January': {'shape': 'triangle-up','color': 'red'} } })
    self.seriesStyle =  '''
      values.forEach( function( rec )  { 
        var seriesAttr = %(seriesAttr)s; var recAttr = %(recAttr)s;
        if( Object.keys(seriesAttr).length > 0) {
          if( seriesAttr[rec.key] != undefined ) {
            for (var k in seriesAttr[rec.key]) { rec[k] = seriesAttr[rec.key][k]} }};
        
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
      })  ''' % {'seriesAttr': json.dumps({} if seriesAttr is None else seriesAttr),
                'recAttr': json.dumps({} if recAttr is None else recAttr)}

  def jsToTable(self):
    """ Convert the date from the chart to a table """
    return ''' '''
    # return '''
    #   var tableData = {dom: 'Bfrtip', buttons: [
    #             {'extend': 'excelHtml5', 'className': 'py_cssdivhidden', 'title': '%(htmlId)s_excel'},
    #             {'extend': 'pdfHtml5', 'className': 'py_cssdivhidden', 'title': '%(htmlId)s_pdf'}],
    #       data: [], columns: [ {data: 'row', title: 'Series'} ], scrollY: "%(height)s", paging:false, searching:true, autoWidth:true };
    #   for (var j in values[0].values[0] ) { tableData.columns.push( {data: j, title: j } ) ; } ;
    #   values.forEach( function(rec, index) { rec.values.forEach( function(i) { i.row = rec.key ; tableData.data.push( i ) ; }) ; }) ;
    #   ''' % {'height': self.height, 'htmlId': self.chartId}

  def toJs(self, options=None):
    chart = dict([(key, val) for key, val in self.items() if val])
    ctx = []  # Just to ensure that the Structure of the chart component will not be changed in the python layer
    for attrOrder in self.priorities:
      if attrOrder in chart:
        if isinstance(chart[attrOrder], dict):
          for subKey, subVal in chart[attrOrder].items():
            ctx.append("%s.%s(%s)" % (attrOrder, subKey, subVal))
        else:
          ctx.append("%s(%s)" % (attrOrder, chart[attrOrder]))
        del chart[attrOrder]
    for key, val in chart.items():
      if isinstance(val, dict):
        for subKey, subVal in val.items():
          ctx.append("%s.%s(%s)" % (key, subKey, subVal))
      else:
        ctx.append("%s(%s)" % (key, val))
    axis = []
    for key, vals in self.axis.items():
      axis.append("%s.%s.%s" % ('%s_chart' % self.chartId, key, ".".join(["%s(%s)" % (subKey, val) for subKey, val in vals.items()])))
    return '%s.%s;%s' % (self.jsChartDef(), ".".join(ctx), ";".join(axis))