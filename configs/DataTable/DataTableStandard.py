#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import json
from ares.configs.DataTable import DataTableBase


class TableFloat(DataTableBase.TableBasic):
  """
  :category: Datatable
  :rubric: PY
  :type: Configuration
  :dsc:

  :return:
  :example: aresObj.datatable('color', data)
  """
  name, tableCall = 'Table Color', 'color'

  @staticmethod
  def mocks():
    mocks = [
            {'lang': 'Python', 'rank': -2, 'value': -34}, {'lang': 'C', 'rank': 2, 'value': -99},
            {'lang': 'C++', 'rank': 3, 'value': 98}, {'lang': 'Java', 'rank': -4, 'value': 0},
          ]

    header = [ {'data': 'lang', 'title': 'Programming Languages', "width": "50px"},
               {'data': 'rank', 'title': '2017 Ranking', 'format': 'float'},
               {'data': 'value', 'title': 'Ranking', 'format': 'float'}]
    return mocks, header

  def config(self):
    """ """
    colsIdx, colsNames = [], []
    for i, rec in enumerate(self.header):
      if rec.get('type') == 'number':
        colsIdx.append(i)
        colsNames.append(rec['data'])
    for i, colsName in enumerate(colsNames):
      self.row(colsName, 0, [colsName], {"background-color": 'rgb(255, 199, 206)', 'color': 'rgb(156, 0, 6)'}, '<')
      self.row(colsName, 0, [colsName], {"background-color": 'rgb(198, 239, 206)', 'color': 'rgb(0, 97, 0)'}, '>')
      self.row(colsName, 0, [colsName], {"background-color": 'rgb(255, 235, 156)', 'color': 'rgb(156, 87, 0)'}, '==')


class TableAge(DataTableBase.TableBasic):
  """
  :category: Datatable
  :rubric: PY
  :type: Configuration
  :dsc:

  :return:
  """
  name, tableCall = 'Table', 'cellage'
  rangeColor = 30
  color = 'red'

  @staticmethod
  def mocks():
    mocks = [
            {'lang': 'Python', 'rank': {'val': -2, 'age': 29}, 'value': {'val': -34, 'age': 2}},
            {'lang': 'C', 'rank': {'val': 2, 'age': 5}, 'value': {'val': -99, 'age': 0}},
          ]

    header = [ {'data': 'lang', 'title': 'Programming Languages', "width": "50px"},
               {'data': 'rank', 'title': '2017 Ranking', 'format': 'float', 'type': 'cell'},
               {'data': 'value', 'title': 'Ranking', 'format': 'float', 'type': 'cell'}]
    return mocks, header

  def config(self):
    """ """
    self.aresObj.jsImports.add('d3')
    self.aresObj.jsGlobal.add('colorAge', '''
          d3.scale.linear().domain( [1, %s] ).range( [ d3.rgb('white'), d3.rgb('%s')] );''' % (self.rangeColor, self.color))

    colsIdx, colsNames = [], []
    for i, rec in enumerate(self.header):
      if rec.get('type') == 'tuple':
        colsIdx.append(i)
        colsNames.append(rec['data'])
    for i, colsName in enumerate(colsNames):
      if not 'createdRowParts' in self:
        self['createdRowParts'] = []
      self['createdRowParts'].append("if (data['%s'][1] != 0) { $('td:eq(%s)', row).css( {'background': colorAge(Math.min(data['%s'][1], %s)) } ) } " % (colsName, colsIdx[i], colsName, self.rangeColor))


class TableIntensity(DataTableBase.TableBasic):
  """
  :category: Datatable
  :rubric: PY
  :type: Configuration
  :dsc:

  :return:
  """
  name, tableCall = 'Table Color', 'intensity'

  @staticmethod
  def mocks():
    mocks = [
            {'lang': {'val': 'Python', 'dsc': 'youpi'}, 'rank': -2, 'value': -34},
            {'lang': {'val': 'C', 'dsc': 'youpi2'}, 'rank': 2, 'value': -99},
            {'lang': {'val': 'C++', 'dsc': 'youpi3'}, 'rank': 63, 'value': 198},
            {'lang': {'val': 'Java', 'dsc': 'youpi4'}, 'rank': -4, 'value': 0},
          ]

    header = [ {'data': 'lang', 'title': 'Programming Languages', "width": "50px", "type": 'cell'},
               {'data': 'rank', 'title': '2017 Ranking', 'format': 'float', "display": "override", '_intensity': True},
               {'data': 'value', 'title': 'Ranking', 'format': 'float', 'digits': 1, '_intensity': True, 'factor': 'K', 'display': 'euro'}]
    return mocks, header
  colorMin, colorMax = '#FFC7CE', '#AABBEE'
  min, max = -200, 200

  def config(self):
    """ """
    self.aresObj.jsGlobal.fnc('ColorIntensity(point, max)', '''return Math.round(100 * point / max); ''')
    colsIdx, colsNames, intensityMinMax = [], [], {}
    for i, rec in enumerate(self.header):
      if rec.get('format') in ['float', 'int', 'percentage'] and rec.get('_intensity'):
        colsIdx.append("td:eq(%s)" % i)
        colsNames.append(rec['data'])
        if '_min' in rec and '_max' in rec:
          intensityMinMax[rec['data']] = {'min': rec['_min'], 'max': rec['_max'] }
    self['createdRowParts'] = []
    self.htmlId = id(self)
    for name in colsNames:
      if name not in intensityMinMax:
        intensityMinMax[name] = {'min': self.vals.min(name), 'max': self.vals.max(name)}

    self.aresObj.jsGlobal.add('intensity_%s' % self.htmlId, json.dumps(intensityMinMax))
    for i, colsName in enumerate(colsNames):
      self['createdRowParts'].append('''
        if ( data['%(colName)s'] < 0 ) { 
          $('%(colIndex)s', row).css( 'background', 'linear-gradient(to right, %(colorMin)s, white ' + ColorIntensity(data['%(colName)s'], intensity_%(htmlId)s['%(colName)s'].min) + '%%)' );
          if ( Math.abs(data['%(colName)s']) > Math.abs(intensity_%(htmlId)s['%(colName)s'].min) / 3) { $('%(colIndex)s', row).css( 'color', '#C00000'); }
        } ''' % {'colName': colsName, 'colIndex': colsIdx[i], 'htmlId': self.htmlId, 'colorMin': self.colorMin})

      self['createdRowParts'].append('''
        if ( data['%(colName)s'] > 0 ) {
          $('%(colIndex)s', row).css( 'background', 'linear-gradient(to right, %(colorMax)s, white ' + ColorIntensity(data['%(colName)s'], intensity_%(htmlId)s['%(colName)s'].max) + '%%)' );
          if ( data['%(colName)s'] > intensity_%(htmlId)s['%(colName)s'].max / 3) { $('%(colIndex)s', row).css( 'color', '#293846') ; }
        } ''' % {'colName': colsName, 'colIndex': colsIdx[i], 'htmlId': self.htmlId, 'colorMax': self.colorMax})


class TableHeatMap(DataTableBase.TableBasic):
  """
  :category: Datatable
  :rubric: PY
  :type: Configuration
  :dsc:

  :return:
  """
  name, tableCall = 'Table Color', 'heatmap'

  @staticmethod
  def mocks():
    mocks = [
            {'lang': {'val': 'Python', 'dsc': 'youpi'}, 'rank': -2, 'value': -34},
            {'lang': {'val': 'C', 'dsc': 'youpi2'}, 'rank': 2, 'value': -99},
            {'lang': {'val': 'C++', 'dsc': 'youpi3'}, 'rank': 63, 'value': 198},
            {'lang': {'val': 'Java', 'dsc': 'youpi4'}, 'rank': -4, 'value': 0},
          ]

    header = [ {'data': 'lang', 'title': 'Programming Languages', "width": "50px", "format": 'CELL'},
               {'data': 'rank', 'title': '2017 Ranking', 'type': 'number'},
               {'data': 'value', 'title': 'Ranking', 'type': 'number'}]
    return mocks, header

  def config(self):
    """ """
    self.aresObj.jsGlobal.fnc('HeatMapColor(start, stop, point)', '''
      return Math.round(stop - start) * point / 100 + start;
      ''')

    colsIdx, colsNames = [], []
    for i, rec in enumerate(self.header):
      if rec.get('format') in ['float', 'int', 'percentage']:
        colsIdx.append("td:eq(%s)" % i)
        colsNames.append(rec['data'])
    self['createdRowParts'] = []
    for i, colsName in enumerate(colsNames):
      self['createdRowParts'].append( "if ( data['%(colName)s'] < 0 ) { $('%(colIndex)s', row).css( 'background-color',  'rgb(' + HeatMapColor(255,100,-data['%(colName)s']) + ',' + HeatMapColor(255,0,-data['%(colName)s']) + ',' + HeatMapColor(255,0,-data['%(colName)s']) +')') } " % { 'colName': colsName, 'colIndex': colsIdx[i] } )
      self['createdRowParts'].append( "if ( data['%(colName)s'] > 0 ) { $('%(colIndex)s', row).css( 'background-color',  'rgb(' + HeatMapColor(255,0,data['%(colName)s']) + ',' + HeatMapColor(255,50,data['%(colName)s']) + ',' + HeatMapColor(255,0,data['%(colName)s']) +')') } " % {'colName': colsName, 'colIndex': colsIdx[i]})
      self['createdRowParts'].append( "if ( Math.abs(data['%(colName)s']) > 40 ) { $('%(colIndex)s', row).css( 'color', 'white') } " % {'colName': colsName, 'colIndex': colsIdx[i]})


class TableDeltaSigned(DataTableBase.TableBasic):
  """
  :category: Datatable
  :rubric: PY
  :type: Configuration
  :dsc:

  :return:
  """
  name, tableCall = 'Table Delta (Signed)', 'delta_signed'
  rangeColor = 100
  colorPlus, colorMinus = 'red', 'green'

  @staticmethod
  def mocks():
    mocks = [
      {'lang': {'val': 'Python', 'dsc': 'youpi', 'delta': 90}, 'rank': -2, 'value': -34},
      {'lang': {'val': 'C', 'dsc': 'youpi2', 'delta': 50}, 'rank': 2, 'value': -99},
      {'lang': {'val': 'C++', 'dsc': 'youpi3', 'delta': -20}, 'rank': 63, 'value': 198},
      {'lang': {'val': 'Java', 'dsc': 'youpi4', 'delta': 5}, 'rank': -4, 'value': 0},
    ]

    header = [{'data': 'lang', 'title': 'Programming Languages', "width": "50px", 'type': 'cell', 'display': 'tooltip'},
              {'data': 'rank', 'title': '2017 Ranking', 'type': 'number'},
              {'data': 'value', 'title': 'Ranking', 'type': 'number'}]
    return mocks, header

  def config(self):
    """ """
    self.aresObj.jsImports.add('d3')
    self.aresObj.jsGlobal.add('colorDeltaPlus', '''
          d3.scale.linear().domain( [1, %s] ).range( [ d3.rgb('white'), d3.rgb('%s')] );''' % (self.rangeColor, self.colorPlus))
    self.aresObj.jsGlobal.add('colorDeltaMinus', '''
              d3.scale.linear().domain( [1, %s] ).range( [ d3.rgb('white'), d3.rgb('%s')] );''' % (
    self.rangeColor, self.colorMinus))

    colsIdx, colsNames = [], []
    for i, rec in enumerate(self.header):
      if rec.get('type') == 'cell':
        colsIdx.append(i)
        colsNames.append(rec['data'])
    for i, colsName in enumerate(colsNames):
      if not 'createdRowParts' in self:
        self['createdRowParts'] = []
      self['createdRowParts'].append("if (data['%s'].delta > 0) { $('td:eq(%s)', row).css( {'background': colorDeltaPlus(Math.min(data['%s'].delta, %s)) } ) } " % (colsName, colsIdx[i], colsName, self.rangeColor))
      self['createdRowParts'].append("if (data['%s'].delta < 0) { $('td:eq(%s)', row).css( {'background': colorDeltaMinus(Math.min(-data['%s'].delta, %s)) } ) } " % (colsName, colsIdx[i], colsName, self.rangeColor))


class TableDeltaAbs(TableDeltaSigned):
  """
  :category: Datatable
  :rubric: PY
  :type: Configuration
  :dsc:

  :return:
  """
  name, tableCall = 'Table Delta (Absolute)', 'delta_abs'

  def config(self):
    """ """
    self.aresObj.jsImports.add('d3')
    self.aresObj.jsGlobal.add('colorDeltaPlus', '''
          d3.scale.linear().domain( [1, %s] ).range( [ d3.rgb('white'), d3.rgb('%s')] );''' % (self.rangeColor, self.colorPlus))

    colsIdx, colsNames = [], []
    for i, rec in enumerate(self.header):
      if rec.get('type') == 'cell':
        colsIdx.append(i)
        colsNames.append(rec['data'])
    for i, colsName in enumerate(colsNames):
      if not 'createdRowParts' in self:
        self['createdRowParts'] = []
      self['createdRowParts'].append("if (Math.abs(data['%s'].delta) > 0) { $('td:eq(%s)', row).css( {'background': colorDeltaPlus(Math.abs(Math.min(data['%s'].delta), %s)) } ) } " % (colsName, colsIdx[i], colsName, self.rangeColor))


class TableComments(DataTableBase.TableBasic):
  """
  :category: Datatable
  :rubric: PY
  :type: Configuration
  :dsc:

  :return:
  """
  name, tableCall = 'Table Comments', 'comment'

  def config(self):
    self.aresObj.cssObj.add('CssCellComment')
    pyCssClsComment = self.aresObj.cssObj.pyRef('CssCellComment')
    self.aresObj.cssObj.add('CssCellSave')
    self.vals.jsColsUsed.add('comment')
    self.vals.df['comment'] = self.vals.df['comment'].fillna('')
    pyCssClsSave = self.aresObj.cssObj.pyRef('CssCellSave')
    self.header.append({'data': 'comment', 'className': pyCssClsComment, 'title': 'Comment', 'width': '200px'})
    self.header.append({'data': 'save', 'className': pyCssClsSave, 'title': '', 'format': "'<div name=\"%s\" id=\"add\" title=\"Save\" style=\"cursor:pointer;font-size:14px\" class=\"fas fa-save\"></div>'" % self.jsTableId, 'width': '5px'})
    self['createdRowParts'] = []
    self['createdRowParts'].append('''
      $('td:eq(%(commId)s)', row).html('<div spellcheck=false contenteditable=true style=\"width:200px;line-height:0.8;height:15px;overflow:auto;margin:0;text-align:left\">'+ data['comment'] +'</div>');
      ''' % {'commId': len(self.header) - 2 } )
    self.aresObj.jsOnLoadFnc.add('''
                  $( document ).on('click', '.%(saveCls)s', function() {
                      var jsTableId = window[$(this).find('svg').attr('name')];
                      var cells = $(this).parents()[0].cells;
                      var comment = cells[ cells.length - 2].innerText ;
                      var data = jsTableId.row( $(this).parents() ).data(); data['comment'] = comment ;                      
                  }) ''' % {"saveCls": pyCssClsSave, 'commCls': pyCssClsComment})

