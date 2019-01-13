#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json


class TableBasic(dict):
  """
  :category: Datatable
  :rubric: PY
  :type: configuration
  :dsc:
    The base table used in the framework. This configuration is forced in the aresObj.table() call.
  :example: aresObj.table([])
  :example: aresObj.datatable('base', [] )
  """
  name, tableCall = 'Table', 'base'
  _attrs = {'stateSave': False, 'searching': False, 'paginate': False, 'pageLength': 30, 'autoWidth': False,
            'colReorder': False, 'scrollX': False, 'scrollCollapse': False, 'dom': ('Bfrtip', True),
            #'bInfo': False,
            #'lengthMenu': [ [ 10, 25, 50, -1 ], [ '10 rows', '25 rows', '50 rows', 'Show all' ] ]
            }

  def __init__(self, aresObj, header, data, jsTableId):
    self.update( {'buttons': [], 'columnDefs': [] } )
    resolvedAttrs = {}
    self.rAttr(self._attrs, resolvedAttrs)
    self.update(resolvedAttrs)
    self.aresObj, self.header, self.data, self.jsTableId = aresObj, header, data, jsTableId
    cellIdx, cellNames = [], []
    for i, rec in enumerate(self.header):
      if rec.get('format', '').startswith('CELL'):
        cellIdx.append("td:eq(%s)" % i)
        cellNames.append(rec['data'])
    self.config()

    self.aresObj.jsGlobal.fnc('EditableCell(e, tableObj)', '''
          $(e).css( {'color': 'blue', 'font-weight': 'bold'}) ;
          $(e).attr('contenteditable', true) ; $(e).focus() ; ''')

    self.aresObj.jsGlobal.fnc('StopEditingCell(e, tableObj)', ''' 
          var row = tableObj.cell($(e).parent()).index().row;
          var column = tableObj.cell($(e).parent()).index().column;
          tableObj.cell(row, column).data($(e).text()) ;
          $(tableObj.cell(row, column).node()).css( {'color': 'blue', 'font-weight': 'bold'} ) ; 
          $(e).attr('contenteditable', false) ; 
          if (!(typeof window[$(e).data('table') + '_changed'] === 'undefined')) { $(tableObj.cell(row, 3).node()).find('#save').show() ; }
          '''  % {'jsTableId': self.jsTableId})

    self.aresObj.jsGlobal.fnc('UpdateCell(e, tableObj)', ''' 
              var row = tableObj.cell($(e).parent()).index().row;
              var column = tableObj.cell($(e).parent()).index().column; 
              tableObj.cell(row, column).data(e.value) ;
              if (!(typeof window[$(e).data('table') + '_changed'] === 'undefined')) { 
                var saveIndex = -1 ;
                tableObj.settings().init().columns.forEach( function(rec, index) { if (rec.data == '_save') { saveIndex = index; } }) ; 
                if ( saveIndex != -1) { $(tableObj.cell(row, saveIndex).node()).find('#save').show() ; } }
              ''' % {'jsTableId': self.jsTableId})

    self.aresObj.jsGlobal.fnc('UpdateCheckBox(e, tableObj)', ''' 
                  var row = tableObj.cell($(e).parent()).index().row;
                  var column = tableObj.cell($(e).parent()).index().column; 
                  tableObj.cell(row, column).data(e.checked) ;
                  if (!(typeof window[$(e).data('table') + '_changed'] === 'undefined')) { var saveIndex = -1 ;
                    tableObj.settings().init().columns.forEach( function(rec, index) { if (rec.data == '_save') { saveIndex = index; } }) ; 
                    if ( saveIndex != -1) { $(tableObj.cell(row, saveIndex).node()).find('#save').show() ; } }
                  ''' % {'jsTableId': self.jsTableId})

    if cellNames:
      if not 'createdRowParts' in self:
        self['createdRowParts'] = []
      for i, cellName in enumerate(cellNames):
        self['createdRowParts'].append(
          " if (  data['%(colName)s'].dsc != undefined ) { $('%(colIndex)s', row).attr( 'title', data['%(colName)s'].dsc ) }  " % {
            'colName': cellName, 'colIndex': cellIdx[i]})

  def rAttr(self, srcVals, dstVals, srcKey=None):
    """
    :category:
    :rubric: PY
    :type: System
    :dsc:

    """
    if isinstance(srcVals, dict):
      for key, val in srcVals.items():
        if isinstance(val, dict):
          dstVals[key] = {}
          self.rAttr(val, dstVals[key])
        else:
          self.rAttr(val, dstVals, key)
    elif isinstance(srcVals, list):
      dstVals[srcKey] = []
      for val in srcVals:
        dstVals[srcKey].append({})
        self.rAttr(val, dstVals[srcKey][-1])
    else:
      if isinstance(srcVals, tuple):
        srcVals = json.dumps(srcVals[0]) if srcVals[1] else srcVals[0]

      if srcKey is not None:
        if isinstance(srcVals, str):
          # TODO: To be tested in Python 3
          dstVals[srcKey] = srcVals
        else:
          dstVals[srcKey] = json.dumps(srcVals)
      elif isinstance(dstVals, list):
        dstVals.append(json.dumps(srcVals))

  def resolveList(self, currDict, currList, listResult):
    """
    """
    for item in currList:
      if isinstance(item, dict):
        subList = []
        self.resolveDict(item, subList)
        listResult.append("{ %s }" % (", ".join(subList)))
      elif isinstance(item, list):
        subList = []
        self.resolveList(currDict, item, subList)
        listResult.append("[%s]" % (",".join(subList)))
      else:
        listResult.append(item)

  def resolveDict(self, currDict, listResult):
    """
    """
    for key, item in currDict.items():
      if isinstance(item, dict):
        subList = []
        self.resolveDict(item, subList)
        listResult.append("%s: {%s}" % (key, ", ".join(subList)))
      elif isinstance(item, list):
        subList = []
        self.resolveList(currDict, item, subList)
        listResult.append("%s: [%s]" % (key, ",".join(subList)))
      else:
        listResult.append("%s: %s" % (key, item))

  def getIndices(self, cols):
    """

    """
    colIdx = []
    for i, rec in enumerate(self.header):
      if rec['data'] in cols:
        colIdx.append(i)
    return colIdx

  def addAttr(self, key, val, category=None, isPyData=True):
    """
    """
    if isPyData:
      val = json.dumps(val)
    if category is not None:
      if isinstance(category, tuple):
        category, index = category
        self[category][index][key] = val
      else:
        self.setdefault(category, {})[key] = val
    else:
      self[key] = val

  def delAttr(self, keys, category=None):
    """
    """
    chart = self.get(category, {}) if category is not None else self
    for attr in keys:
      if attr in chart:
        del chart[attr]

  def js(self):
    """
    """
    ctx = []
    if 'createdRowParts' in self:
      self['createdRow'] = "function ( row, data, index ) { %s }" % ";".join(self['createdRowParts'])
      del self['createdRowParts']

    if getattr(self, 'footerType', None) == 'sum':
      self['footerCallback'] = ''' function ( row, data, start, end, display ) { 
          var api = this.api();
          api.columns('.sum', { page: 'current' } ).every(function (el) {
              var sum = this.data().reduce(function (a, b) {var x = parseFloat(a) || 0; var y = parseFloat(b) || 0;return x + y; }, 0);
              $(this.footer()).html( sum.formatMoney(0, ',', '.') ); } );}
        '''
    self.resolveDict(self, ctx)
    return ctx

  def config(self): pass

  def ordering(self, orders):
    """
    :category:
    :rubric: JS
    :type: Configuration
    :dsc:
      Set the default ordering rule in the datatable. By default the first column is used.
      It is possible here to provide a list of column with the type of sorting rule to apply asc or desc.
    :link Datatable Documentation: https://datatables.net/examples/basic_init/table_sorting.html
    :example: tableObj.ordering(False)
    """
    if not orders:
      self['order'] = 'false'
    else:
      orderCols, orderTypes = [], []
      for colName, orderType in orders:
        orderCols.append(colName)
        orderTypes.append(orderType)
      orderColsIdx = self.getIndices(orderCols)
      self['order'] = []
      for i, j in enumerate(orderColsIdx):
        self['order'].append('[%s, "%s"]' % (j, orderTypes[i]))
