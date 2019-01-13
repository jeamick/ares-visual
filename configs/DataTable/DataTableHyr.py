#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.configs.DataTable import DataTableBase


class TableHyr(DataTableBase.TableBasic):
  """
  :category: Datatable
  :rubric: PY
  :type: Configuration
  :dsc:
    Table with a tree view.
    The structure of the expected records will be a bit specific in order to produce automatically this tree view
  :return:
  """
  name, tableCall = 'Table Hierarchy', 'hierarchy'

  @staticmethod
  def mocks():
    mocks = [
      {'lang': 'Python', 'rank': -2, 'value': -34, 'level': 0, '_id': 'A'},
      {'lang': 'R', 'rank': 2, 'value': -99, 'level': 1, '_leaf': True, '_id': 'A_B' },
      {'lang': 'C', 'rank': 2, 'value': -99, 'level': 0, '_id': 'C' },
      {'lang': 'C++', 'rank': 3, 'value': 98, 'level': 1, '_id': 'C_D'},
      {'lang': 'C#', 'rank': 3, 'value': 98, 'level': 2, '_leaf': True, '_id': 'C_D_E_F'},
      {'lang': 'Java', 'rank': -4, 'value': 0, 'level': 0, '_id': 'F', '_leaf': True},
    ]

    header = [{'data': 'lang', 'title': 'Programming Languages', "width": "50px"},
              {'data': 'rank', 'title': '2017 Ranking', 'display': 'override'},
              {'data': 'value', 'title': 'Ranking', 'display': 'button'}]
    return mocks, header

  def levelStyle(self, level, cssStyle):
    """

    """
    if not 'createdRowParts' in self:
      self['createdRowParts'] = []
    self['createdRowParts'].append( "if ( data.level == %s ) { $(row).css( %s ) } " % (level, cssStyle) )

  def config(self):
    """

    """
    self.ordering([])

  def js(self):
    """

    """
    ctx = []
    self.aresObj.jsGlobal.fnc('ExpandTable(e)', '''
       if ( $(e).attr('src') == '/static/images/grey-minus.png') { 
          $(e).attr('src', '/static/images/grey-plus.png'); 
          var firstTd = $(e).parent(); var tr = firstTd.parent(); var loop = true ;
          while( tr.next().is('tr') && loop ) {
            tr = tr.next() ; if ( tr.find('td').first().data('id').startsWith( firstTd.data('id') ) ) { 
                tr.hide() ; if ( !tr.find('td').first().data('leaf')) { tr.find('td').first().find('img').attr('src', '/static/images/grey-plus.png') }
            } else { loop = false ;}  } }
       else {
          $(e).attr('src', '/static/images/grey-minus.png'); 
          var firstTd = $(e).parent(); var tr = firstTd.parent() ; var loop = true ;
          while( tr.next().is('tr') && loop ) {
            tr = tr.next() ; 
              if ( tr.find('td').first().data('id').startsWith( firstTd.data('id') ) ) { 
              if ( tr.find('td').first().data('level')-1 == firstTd.data('level') ) { tr.show() ; }
            } else { loop = false ;}  } } ''')

    if 'createdRowParts' in self:
      self['createdRow'] = "function ( row, data, index ) { %s }" % ";".join(self['createdRowParts'])
      del self['createdRowParts']

    if self.expanded:
      self['rowCallback'] = '''
        function ( row, data, index ) { 
          if ( !data['_leaf'] ) { $('td:eq(0)', row).data('leaf', false) ; $('td:eq(0)', row).html( '<img onclick="ExpandTable(this)" style="margin-top:-3px" src="/static/images/grey-minus.png"/>' + data['%s'] ) ; } ;
          if ( data.level > 0) { $('td:eq(0)', row).data('leaf', true) ; $('td:eq(0)', $(row)).css('padding-left', 25 * data.level + 'px') ;} 
          $('td:eq(0)', row).data('id', data['_id']); $('td:eq(0)', row).data('level', data['level']); }
        ''' % self.header[0]['data']
    else:
      self['rowCallback'] = '''
        function ( row, data, index ) { 
          if ( !data['_leaf'] ) { $('td:eq(0)', row).html( '<img onclick="ExpandTable(this)" style="margin-top:-3px" src="/static/images/grey-plus.png"/>' + data['%s'] ) ; } ;
          if ( data.level > 0) { $('td:eq(0)', $(row)).css('padding-left', 25 * data.level + 'px') ; $(row).hide() ;} 
        $('td:eq(0)', row).data('id', data['_id']); $('td:eq(0)', row).data('level', data['level']); }
        ''' % self.header[0]['data']

    if self.footerType == 'sum':
      self['footerCallback'] = ''' function ( row, data, start, end, display ) { 
          var api = this.api();
          api.columns('.sum', { page: 'current' } ).every(function (el) {
              var sum = this.data().reduce(function (a, b) {var x = parseFloat(a) || 0; var y = parseFloat(b) || 0;return x + y; }, 0);
              $(this.footer()).html( sum.formatMoney(0, ',', '.') ); } );}
        '''
    self.resolveDict(self, ctx)
    return ctx