#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import os
import json
import inspect
import importlib
import logging

from ares.Lib.html import AresHtml
from ares.Lib.js.tables import JsTableCols

import ares.configs.DataTable


# The object with all the different configurations available for the table interface
# This factory will pick up automatically when the server is restarted all the new configurations
FACTORY = None


DSC = {
    'eng':
'''
:category: Table
:rubric: PY
:type: Factory
:dsc: 
  Different configuration avaiable for the table object. Those configuration will drive the kind of expected recordset.
  Indeed for some configurations some specific keys are expected to correctly display the data.
'''
}

# External Datatable extensions added on demand to add some extra features
# Details of the different extensions are available on the different websites
# https://datatables.net/extensions/
extensions = {
  'rowsGroup': {'jsImports': ['datatables-rows-group']},
  'rowGroup': {'jsImports': ['datatables-row-group'], 'cssImport': ['datatables-row-group']},
  'fixedHeader': {'jsImports': ['datatables-fixed-header'], 'cssImport': ['datatables-fixed-header']},
  'colReorder': {'jsImports': ['datatables-col-order'], 'cssImport': ['datatables-col-order'] },
  'colResize': {'jsImports': ['datatables-col-resizable'], 'cssImport': ['datatables-col-resizable']},
  'fixedColumns': {'jsImports': ['datatables-fixed-columns'], 'cssImport': ['datatables-fixed-columns']}
}


def loadFactory():
  """
  :category: Table
  :rubric: PY
  :type: configuration
  :dsc:
    This will read the table configuration table and it will create a mapping table between the names and the corresponding class.
    Thus when a specific type of table is requested, this will be automatically mapped to the right class with the defined configuration.
    The data expected for any table is a AReS dataframe.
  :return: The factory with all the table configuration
  """
  tmp = {}
  for script in os.listdir(os.path.dirname(ares.configs.DataTable.__file__)):
    if script.startswith('DataTable') and not script.endswith('pyc'):
      try:
        for name, obj in inspect.getmembers(importlib.import_module("ares.configs.DataTable.%s" % script.replace(".py", "")), inspect.isclass):
          if hasattr(obj, 'tableCall'):
            tmp[getattr(obj, 'tableCall')] = obj
      except Exception as err:
        logging.warning( "%s, error %s" % (script, err) )
  return tmp


class DataTable(AresHtml.Html):
  """
  :category: Javascript - Datatable
  :rubric: JS
  :dsc:
    The python interface to the javascript Datatable framework. Not all the functions have been wrapped here but you should be able to
    do the most frequent events and interactions with this component from the available function.
    Please keep in mind that the javascript is only trigger on the web browser (namely not with the Python code)
  :link Datatable website: https://datatables.net/
  :link Datatable column legacy: http://legacy.datatables.net/usage/columns
  :link Datatable column legacy: https://datatables.net/upgrade/1.10-convert
  :link Datatable Column Definition: https://datatables.net/reference/option/columnDefs
  """
  name, category, callFnc, docCategory = 'Table', 'Table', 'table', 'Standard'
  references = {'DataTable': 'https://datatables.net/reference/index',
                'DataTable Options': 'https://datatables.net/reference/option/',
                'DataTable Ajax': 'https://datatables.net/reference/option/ajax.data',
                'DataTable Callbacks': 'https://datatables.net/reference/option/drawCallback',
                'DataTable Buttons': 'https://datatables.net/extensions/buttons/examples/initialisation/custom.html', }
  __reqCss, __reqJs = ['datatables', 'datatables-export'], ['d3', 'datatables', 'datatables-export']
  __pyStyle = ['CssDivLoading']

  # The javascript layer is not supposed to cast the data
  # By doing this here it will be a huge loss in term of efficiency in the borwser renderer
  __type = {'cell': 'data.val', 'tuple': 'data[0]'}

  # Variable dedicated to the documentation of this class
  # This cannot and should not be using or accessing by other classes derived from this one
  __doc__enums = {
    'help': {"eng": "Get the list of enumerable items generated automatically from factories"},
  }

  def __init__(self, aresObj, tableTypes, recordSet, header, title, width, widthUnit, height,
               heightUnit, tableOptions, toolsbar, htmlCode):
    global FACTORY
    super(DataTable, self).__init__(aresObj, [], code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.jsTableId, self.extraHeaders, self.tableOptions, self.header, self.footer = "%s_table" % self.htmlId, None, tableOptions, '', ''
    self._systemOptions = dict(tableOptions.get('system', {}))
    self._cols = JsTableCols.TableCols(aresObj)
    if 'system' in tableOptions:
      del tableOptions['system']

    self.extraJsInitFnc, self.dsc_comment, self.tableWidth, self.toolsbar = set(), '', "100%", toolsbar
    if FACTORY is None:
      FACTORY = loadFactory() # atomic function to store all the different table mapping
    self.columns = header.get('_order', list(recordSet._schema['keys']) + list(recordSet._schema['values']))
    headers, colValues, self._jsRowFncs, self._jsColFncs, self._eventFrgs, self.tableStyle = [], [], [], {}, {}, []
    for i, column in enumerate(self.columns):
      if column in recordSet._schema['values']:
        colValues.append(i)
        recordSet._data[column].fillna(0, inplace=True)
        # TODO: replace this replacement by moving to list of lists
        colDef = {'data': column.replace(".", "\\.").replace("[", "\\[").replace("]", "\\]"), 'title': column, 'format': 'float', 'digits': self.tableOptions.get("digits", 0)}
      else:
        colDef = {'data': column.replace(".", "\\."), 'title': column}
      if column in header and isinstance(header[column], dict):
        colDef.update(header[column])
      headers.append(colDef)

    if tableTypes == 'hierarchy':
      pyDetailCls = self.addPyCss('CssTdDetails')
      pyShownDetailCls = self.addPyCss('CssTdDetailsShown')
      headers[0]['visible'] = False
      headers[1]['visible'] = False
      headers = [{'data': None, 'title': '', 'width': 20, "className": pyDetailCls, 'orderable': False, 'defaultContent': ''}] + headers
      self.aresObj.jsOnLoadFnc.add('''
        $('#%(htmlId)s table').on('click', 'td.%(pyDetailCls)s, td.%(pyShownDetailCls)s', function () {
          var tr = $(this).closest('tr'); var row = %(jsTableId)s.row(tr);
          if (row.child.isShown()) {
            $(this).removeClass('%(pyShownDetailCls)s').addClass('%(pyDetailCls)s');
            row.child.hide(); tr.removeClass('shown')} 
          else {
            $(this).removeClass('%(pyDetailCls)s').addClass('%(pyShownDetailCls)s');
            row.child( "<div>gbgbg</div>" ).show(); tr.addClass('shown');
          }})''' % {'pyDetailCls': pyDetailCls, 'htmlId': self.htmlId, 'jsTableId': self.jsTableId, 'pyShownDetailCls': pyShownDetailCls})

    self.__table = FACTORY['base'](aresObj, headers, recordSet, self.jsTableId)
    self.__table.data.attach(self)
    if len(colValues) > 0:
      tableStyles = tableOptions.get('style', {})
      valsDef = tableStyles.get('values', {}).get('attr', {})
      valsDef['table'] = headers
      self.styleCols(colValues, tableOptions.get('style', {}).get('values', {'name': 'number'}).get('name', 'number'), attr=valsDef)
      for systemCell, flag in self._systemOptions.items():
        if flag:
          valsDef = tableStyles.get(systemCell, {}).get('attr', {})
          valsDef['table'] = headers
          self.styleCols(colValues, tableOptions.get('style', {}).get(systemCell, {'name': systemCell}).get('name', systemCell), attr=valsDef)

    # else: # Add the different export possible from a table
    #   self.addAttr('lengthMenu', [ [ 10, 25, 50, -1 ], [ '10 rows', '25 rows', '50 rows', 'Show all' ] ])
    #   self.__table['buttons'].append('"pageLength"')

    #self.__table.footerType = footerType
    self.addAttr(tableOptions)
    self.addGlobalVar("DATATABLES_STATE", "{}")
    if tableOptions.get('rowsGroup', False):
       self.aresObj.jsImports.add('datatables-rows-group')
       self.addAttr('rowsGroup', tableOptions['rows-group'])
    if tableOptions.get('rowGroup', False):
       self.aresObj.jsImports.add('datatables-row-group')
       self.aresObj.cssImport.add('datatables-row-group')
       self.addAttr('rowGroup', tableOptions['rowGroup'])
    if tableOptions.get('fixedHeader', False):
       self.aresObj.jsImports.add('datatables-fixed-header')
       self.aresObj.cssImport.add('datatables-fixed-header')
       #self.addAttr('headerOffset', 50, 'fixedHeader')
    if tableOptions.get('colsOrdering', False):
      self.aresObj.cssImport.add('datatables-col-order')
      self.aresObj.jsImports.add('datatables-col-order')
      self.addAttr('colReorder', True)
    if tableOptions.get('fixedLeftColumnId', None) is not None:
      self.aresObj.jsImports.add('datatables-fixed-columns')
      self.aresObj.cssImport.add('datatables-fixed-columns')
      self.addAttr('leftColumns', tableOptions['fixedLeftColumnId'], 'fixedColumns')
      self.aresObj.cssObj.add('CssTableColumnFixed')
      for i in range(tableOptions['fixedLeftColumnId']):
        self.__table.header[i]['className'] = 'py_CssTableColumnFixed'.lower()
    # Add the different export possible from a table
    #self.addAttr('dom', 'Bfrtip')  # (B)utton (f)iltering
    self.aresObj.cssObj.add('CssDivHidden')
    #for button, name in [('copyHtml5', 'copy'), ('csvHtml5', 'csv'), ('excelHtml5', 'excel'), ('pdfHtml5', 'pdf')]:
    #  self.addButton( {'extend': button, 'text': '', 'className': 'py_cssdivhidden', 'title': '%s_%s' % (name, self.htmlId)} )
    self.aresObj.cssObj.add('CssDivTextLeft')
    self.title = title
    self.css({'margin-top': '5px'})
    # if saveRow is not None:
    #   self.addColSave(saveRow)
    #
    # if deleteCol:
    #   self.addColDelete(deleteCol)


  # --------------------------------------------------------------------------------------------------------------
  #
  #                                     CSS / JS WRAPPER DEFINITION
  # --------------------------------------------------------------------------------------------------------------
  def styleCols(self, colIds, values, attr=None):
    """
    :category: Table Column Style
    :rubric: CSS
    :type: Display
    :dsc:
      Change the style of the defined list of columns indices. If all the columns are selected the keyword _all can be
      used. This can be useful to change some row in the datatable.
    :example: tb.styleCols(0, 'css', attr={'css': {'color': 'dark-green', 'background-color': 'yellow'}})
    :example: tb.styleCols('_all', 'css_id', attr={'cssCell': {'border-top': '5px solid pink', 'border-bottom': '5px solid pink'}, 'id': 2})
    """
    self._cols.add(colIds, values, attr)

  def styleColsByNames(self, colNames, values, attr=None):
    """
    :category: Table Column Style
    :rubric: CSS
    :type: Display
    :dsc:
      Change the style of the defined list of columns names. Those names should exist in the input dataframe and available
      column names. The keyword _all cannot be used here.
    :example: tb.styleColsByNames(['Series4'], 'class', attr={'class': css[0].classname})
    """
    if not isinstance(colNames, list):
      colNames = [colNames]
    colIds = [self.columns.index(colName) for colName in colNames]
    self._cols.add(colIds, values, attr)

  def cssRows(self, cssCls=None, rowIds=None, data=None, colName=None, cssOvrs=None):
    """
    :category: Table Rows Formatting
    :rubric: JS
    :type: Configuration
    :dsc:
      This Python wrapper will implement the following javascript function, createdRow: function(row, data, dataIndex ) {}
    :example: tableObj.cssRows({'color': 'red', 'background': 'green'}, data='Increasing', colName='direction')
    :example: tableObj.cssRows(['CssTablePinkBorder', 'CssTableRedCells'])
    :example: tableObj.cssRows(['CssTableTotal'], rowIds=[2])
    :return: The Python table object
    :link Datatable Documentation: https://datatables.net/reference/option/createdRow
    """
    cssAttr, cssClsName = {}, []
    if isinstance(cssCls, list):
      for css in cssCls:
        cssMod = self.aresObj.cssObj.get(css)
        if cssMod is not None:
          self.addPyCss(css)
          cssClsName.append(cssMod().classname)
    elif isinstance(cssCls, dict):
      cssAttr = cssCls
    else:
      cssMod = self.aresObj.cssObj.get(cssCls)
      if cssMod is not None:
        self.addPyCss(cssCls)
        cssClsName.append(cssMod().classname)
    if cssOvrs is not None:
      cssAttr.update(cssOvrs)

    jsFncs = []
    if len(cssClsName) > 0:
      jsFncs.append("$(row).addClass('%s')" % " ".join(cssClsName))
    if len(cssAttr) > 0:
      jsFncs.append("$(row).css(%s)" % json.dumps(cssAttr))

    if rowIds is not None:
      # In this case if has to be controlled by the column renderer
      #self.cssCols(cssCls, rowIds=rowIds)
      return self

    if data is not None:
      if colName is None:
        raise Exception("cssRows Error - You should supply a column name (colName) to use this function")

      self._jsRowFncs.append("if(data['%(colName)s'] == %(data)s) {%(jsFnc)s}" % {"data": json.dumps(data), "jsFnc": ";".join(jsFncs), "colName": colName})

    if rowIds is None and data is None and colName is None:
      self._jsRowFncs.append("$(row).css(%(jsFnc)s)" % {"jsFnc": ";".join(jsFncs)})
    return self

  def cssSelection(self, pyCssCls="CssTableSelected"):
    """
    :category: Table Style
    :rubric: CSS
    :type: Display
    :example: >>> tableObj.cssSelection( aresObj.cssCls("CssBespoke", {"color": "red"} ) )
    :return: Returns a CSS String with the name of the CSS class to be used as reference
    :dsc:
      Change the selection CSS class to be used in the different cell and row event.
      This can be an existing class in the framework or a bespoke one created on the fly
    """
    import inspect

    if inspect.isclass(pyCssCls):
      self.aresObj.cssObj.addPy(pyCssCls)
      pyCssCls = [pyCssCls.__name__]

    if isinstance(pyCssCls, str):
      pyCss = self.addPyCss(pyCssCls)
    else:
      for attr in pyCssCls.style:
        attr["value"] = "%s!important" % attr["value"] if not attr["value"].endswith("!important") else attr["value"]
      self.aresObj.cssObj.cssStyles.update(pyCssCls.getStyles())
      pyCss = pyCssCls.classname
    return pyCss


  # --------------------------------------------------------------------------------------------------------------
  #
  #                                     SYSTEM SECTION
  # --------------------------------------------------------------------------------------------------------------
  @property
  def val(self):
    """
    :category: Javascript features
    :rubric: JS
    :example: tableObj.val
    :return: Javascript string with the function to get the content of the component
    :dsc:
      Property to get the jquery value of the HTML object in a python HTML object.
      This method can be used in any jsFunction to get the value of a component in the browser.
      This method will only be used on the javascript side, so please do not consider it in your algorithm in Python
    """
    return "%s.data().toArray()" % self.jsTableId

  @property
  def contextVal(self):
    """
    :category: Javascript Event
    :rubric: JS
    :example: tableObj.contextVal
    :return: Javascript String with the value attached to the context menu
    :dsc:
      Set the javascript data defined when the context menu is created from a table object
    """
    return "{val: $(event.target).html(), row: event.target._DT_CellIndex.row, column: event.target._DT_CellIndex.column}"

  @property
  def json(self):
    """
    :category: Javascript features
    :rubric: JS
    :example: myObj.json
    :returns: Javascript string with the function to get the content of the component
    :dsc:
      Property to get the jquery value as a String of the HTML object in a python HTML object.
      This method can be used in any jsFunction to get the value of a component in the browser.
      This method will only be used on the javascript side, so please do not consider it in your algorithm in Python
      this will return the table content but also the selected line if any
    """
    return "JSON.stringify({data: %(jsTableId)s.data().toArray(), selection: %(jsClickState)s })" % {"jsTableId": self.jsTableId, 'jsClickState': self.jsClickState() }

  def filter(self, jsId, colName, allSelected=True, filterGrp=None):
    """
    :category: Data Transformation
    :rubric: JS
    :type: Filter
    :dsc:
      Link the data to the filtering function. The record will be filtered based on the composant value
    :return: The Python Html Object
    """
    self.aresObj.jsOnLoadFnc.add("%(breadCrumVar)s['params']['%(htmlCode)s'] = ''" % {'htmlCode': self._code, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar})
    val = "%(breadCrumVar)s['params']['%(htmlCode)s'] " % {'htmlCode': self._code, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar}
    if allSelected:
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {'allIfEmpty': []})[colName] = val
      self.aresObj.jsSources.setdefault(jsId, {})['filters']['allIfEmpty'].append(colName)
    else:
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {})[colName] = val
    return self

  def onDocumentLoadVar(self): pass
  def onDocumentLoadFnc(self): pass

  def onDocumentReady(self):
    self.aresObj.jsOnLoadFnc.add('''
      %(jsGenerate)s; $('#%(htmlId)s table').find('th').tooltip(); %(extraJsInitFnc)s ;
      ''' % {'jsGenerate': self.jsGenerate(None), 'htmlId': self.htmlId, 'extraJsInitFnc': ';'.join(self.extraJsInitFnc)})

  def jsGenerate(self, jsData='data', jsDataKey=None, isPyData=False, jsParse=False):
    """

    :return:
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    if jsParse:
      jsData = "JSON.parse(%s)" % jsData
    if not hasattr(self, 'ctx'):
      self.addAttr('columns', self.__table.header)
      self.addAttr('createdRow', "function(row, data, dataIndex) {%s}" % ";".join(self._jsRowFncs), isPyData=False)
      columnOrders = [col['data'] for col in self.__table.header]
      self.addAttr('aoColumnDefs', self._cols.toJs(), isPyData=False)
      self.ctx = self.__table.js()
    return '''
      var table_data = {%(options)s};
      if(typeof %(jsTableId)s === 'undefined'){
        table_data.data = %(jsData)s;
        %(jsTableId)s = $('#%(htmlId)s table').DataTable(table_data)}
      else {
        %(jsClear)s; %(jsTableId)s.rows.add(%(jsData)s); %(jsDraw)s;
      } ''' % {'jsClear': self.jsClear(), 'jsTableId': self.jsTableId, 'jsDraw': self.jsDraw(), 'htmlId': self.htmlId,
               'options': ", ".join(self.ctx), 'jsData': self.__table.data.setId(jsData).getJs()}

  def ordering(self, orders):
    """
    :category: Javascript - Datatable Table ordering
    :rubric: JS
    :example: myTable.orders( [('col1', 'desc'), ('col2', 'asc')] )
    :example: tableObj.ordering(False)
    :dsc:
        Order the table according to the content of some defined columns.
        Default behaviour will use the first column (visible or hidden) to order the table
    :link Datatable Documentation: https://datatables.net/examples/basic_init/table_sorting.html
    :return: self
    """
    self.__table.ordering(orders)
    return self

  def selectRow(self, colName, jsValue, pyCssCls='CssTableSelected', isPyData=True):
    """
    :category: Javascript - Datatable
    :rubric: JS
    :example: >>> myTable.selectRow( 'col1', 'test') ;
    :dsc:
      Function to set the selection of some row in the table.
      The selection can be done on the javascript side but also in the init in the Python
    :link Datatable Documentation:
    """
    pyCss = self.cssSelection(pyCssCls)
    if isPyData:
      jsValue = json.dumps(jsValue)
    self.__table.formatRow('''
      if ( data['%(colName)s'] == %(value)s) {
        $( row ).addClass( '%(pyCss)s' );
        if ( DATATABLES_STATE['#%(htmlId)s'] == undefined ) { DATATABLES_STATE['#%(htmlId)s'] = [] } ;
        DATATABLES_STATE['#%(htmlId)s'].push( {'row': JSON.stringify(data), row_id: index } );
      } ''' % {"value": jsValue, 'colName': colName, 'htmlId': self.htmlId, 'jsTableId': self.jsTableId, 'pyCss': pyCss} )

  def addButton(self, data):
    """
    :category: Javascript - Datatable Initialisation
    :rubric: JS
    :example: >>> myTable.addButton( {'copy': 'Copy to clipboard' ] )
    :dsc:
      Display the generic buttons on the table of the table.
    :link Datatable Documentation: https://datatables.net/extensions/buttons/
    :link Datatable Documentation 2: https://datatables.net/reference/option/buttons.buttons.text
    """
    self.__table['buttons'].append({})
    for key, val in data.items():
      self.__table.addAttr(key, val, ('buttons', -1))


  # -----------------------------------------------------------------------------------------
  #                                Generic Python function to the attribute tables
  # -----------------------------------------------------------------------------------------
  def addAttr(self, key, val=None, category=None, isPyData=True):
    """
    :category: Table Definition
    :rubric: PY
    :type: Configuration
    :dsc:
      Add parameters to the Datatable definition before buidling it.
    :link Datatable Documentation: https://datatables.net/manual/styling/
    :return: Python Object
    """
    if isinstance(key, dict):
      for k, v in key.items():
        self.__table.addAttr(k, v, category, isPyData)
    else:
      self.__table.addAttr(key, val, category, isPyData)
    return self

  def delAttr(self, key, category=None):
    """
    :category: Table Definition
    :rubric: PY
    :type: Configuration
    :dsc:
      Add parameters to the Datatable definition before buidling it.
    :link Datatable Documentation: https://datatables.net/manual/styling/
    :return: Python Object
    """
    self.__table.delAttr(key, category)
    return self


  # -----------------------------------------------------------------------------------------
  #                                STANDARD DATATABLE JAVASCRIPT
  # -----------------------------------------------------------------------------------------
  def jsDataRow(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Python - Datatable Data conversion
    :rubric: PY
    :example: >>> myTable.jsDataRow()
    :example: >>> myTable.jsFilterCol('Product', jsData=t.jsDataRow(), jsDataKey='Product')
    :dsc:
      This function will change the data object used in the event to be the row directly as a dictionary.
    :tip: You can use this in jsData to replace the data in the function like jsFilterCol
    :return: Returns a string as a javascript dictionary with the row data as a dictionary
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return "JSON.parse(%s.row)" % jsData

  def jsFilterCol(self, colName, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Javascript - Datatable Filter
    :rubric: JS
    :example: >>> myTable.jsFilterCol('Product', jsData=t.jsDataRow(), jsDataKey='Product')
    :TODO: Extend this method to filter on multiple columns
    :dsc:
        Filtering function on the datatable based on external rules. This will use the internal Datatable engine to filter the data
    :tip: Use the function to replace the jsData to be the row using jsDataRow() to filter on another table click row event
    :return: Return a string corresponding to the filtering function on the table
    :link Datatable Documentation: https://datatables.net/reference/api/search()
    """
    for i, col in enumerate(self.__table.header):
      if col['data'] == colName:
        colIndex = i
        break

    else:
      return ''

    if isPyData:
      jsData = json.dumps(jsData)
    else:
      if jsDataKey is not None:
        jsData = "%s['%s']" % (jsData, jsDataKey)
    self.addAttr('searching', True)
    return '''%(jsTableId)s.column( [%(colIndex)s] ).search( %(jsData)s ).draw();''' % {'jsTableId': self.jsTableId, 'colIndex': colIndex, 'jsData': jsData}

  def jsFilterFromCell(self):
    """
    :category: Javascript - Datatable Filter
    :rubric: JS
    :example: >>> myTable.jsFilterFromCell()
    :TODO: Extend this method to filter on multiple columns
    :dsc:
        Filtering function on the datatable based on an external cell object. This will use the internal Datatable engine to filter the data
    :return: Return a string corresponding to the filtering function on the table
    :link Datatable Documentation: https://datatables.net/reference/api/search()
    """
    self.addAttr('searching', True)
    return '''%(jsTableId)s.columns().search('').draw();%(jsTableId)s.column( [data.col_id] ).search( data.cell ).draw(); ''' % {'jsTableId': self.jsTableId}

  def jsClear(self, update=False):
    """
    :category: Javascript - Datatable Refresh
    :rubric: JS
    :type: Table Event
    :example: myTable.jsClear()
    :dsc:
      Function to clear the content of a table. The table will still be present but only with the headers.
      It will be then possible to add rows to this table as long as the expected keys are presented in the dictionary
    :link Datatable website: https://datatables.net/reference/api/clear()
    """
    updateFnc = self.jsDraw() if update else ""
    return "%(jsTableId)s.clear();%(jsDraw)s" % {'jsTableId': self.jsTableId, "jsDraw": updateFnc}

  def jsDraw(self, scope=None):
    """
    :category: Javascript - Datatable Refresh
    :rubric: JS
    :type: Table Event
    :example: >>> myTable.jsDraw() ;
    :dsc:
      Function on the javascript side to force a table to be refreshed. This can be triggered in a javascript event
      or after a change but on the javascript side
    :link Datatable website: https://datatables.net/reference/api/draw()
    """
    if scope is None:
      return "%(jsTableId)s.draw()" % {'jsTableId': self.jsTableId}

    return "%(jsTableId)s.draw(%(scope)s)" % {'jsTableId': self.jsTableId, 'scope': json.dumps(scope)}

  def jsRemoveRow(self, jsData="$(this).parents('tr')", jsDataKey=None, update=True, isPyData=False):
    """
    :category: Javascript - Datatable Refresh
    :rubric: JS
    :type: Table Event
    :example: >>> myTable.jsRemoveRow() ;
    :example: >>> click(myTable.jsRemoveRow(1)) ;
    :dsc:
      Function to remove the selected row. This function should be triggered only in a row click event as the this (self)
      object is used.
    :link Datatable website: https://datatables.net/reference/api/row()
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    updateFnc = self.jsDraw('page') if update else ""
    return "var row = %(jsTableId)s.row(%(rowIdx)s); var rowNode = row.node(); row.remove();%(jsDraw)s" % {"rowIdx": jsData, 'jsTableId': self.jsTableId, "jsDraw": updateFnc}

  def jsUpdateCell(self, jsData='data', jsDataKey='cell', isPyData=False, update=True):
    """
    :category: Javascript - Datatable Refresh
    :rubric: JS
    :example: >>> myTable.jsUpdateCell() ;
    :example: >>> myTable.jsUpdateCell( jsData= {'cell': ["A", "B"], 'col_id': 1, 'row_id': 1 }, isPyData=True) ;
    :dsc:
      Function to update the value of a cell. Can be the current one or another.
      This information should be defined in the jsDataKey object.
    :link Datatable website: https://datatables.net/reference/api/cell()
    """
    if isPyData:
      jsData = json.dumps(jsData)
    updateFnc = self.jsDraw('page') if update else ""
    return "%(jsTableId)s.cell( %(jsData)s['row_id'], %(jsData)s['col_id'] ).data(%(jsData)s['%(cell)s']);%(jsDraw)s" % {'jsTableId': self.jsTableId, 'jsData': jsData, 'cell': jsDataKey, "jsDraw": updateFnc}

  def jsCellGoTo(self, url=None, jsData='data', jsDataKey='cell', jsCellCode='cell', isPyData=False):
    """
    :category: Javascript function
    :rubric: JS
    :type: Cell event
    :example: >>> myObj.jsCellGoTo( 'http://www.google.fr' )
    :dsc:
      The href property sets or returns the entire URL of the current page.
    :return: A string representing the Javascript fragment to be added to the page to go to another web page
    :link W3C Documentation: https://www.w3schools.com/jsref/prop_loc_href.asp
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if url is None:
      return "%s;location.href=buildBreadCrum();" % self.jsAddUrlParam(jsCellCode, "%s.%s" %(jsData, jsDataKey), isPyData=False)

    return 'window.location.href="%s?%s=" + %s;' % (url, jsCellCode, "%s.%s" %(jsData, jsDataKey))

  def jsUpdateRow(self, jsData='data', jsDataKey='row', isPyData=False, update=True):
    """
    :category: Javascript - Datatable Refresh
    :rubric: JS
    :example: >>> myTable.jsUpdateRow() ;
    :example: >>> myTable.jsUpdateCell( jsData= {'row': ["A", "B"], 'row_id': 1 }, isPyData=True) ;
    :dsc:
      Function to update a row in a table. This can work very well with a clickRow event as the object will already have the
      expected format. So by returning from a ajax call from this kind of data and calling this function the source row will be changed
    :link Datatable website: https://datatables.net/reference/api/row()
    """
    if isPyData:
      jsData = json.dumps(jsData)
    updateFnc = self.jsDraw('page') if update else ""
    return "%(jsTableId)s.row( %(jsData)s['row_id']).data( %(jsData)s['%(jsDataKey)s']);%(jsDraw)s" % {'jsTableId': self.jsTableId, 'jsData': jsData, 'jsDataKey': jsDataKey, "jsDraw": updateFnc}

  def jsAddRow(self, jsData='data', uniqKey=None, jsDataKey=None, pyCssCls='CssTableNewRow', isPyData=False):
    """
    :category: Javascript - Datatable Refresh
    :rubric: JS
    :type: Table Event
    :example: >>> myTable.jsAddRow()
    :example: >>> .click(myTable.jsAddRow([{'direction': 'test', 'dn': -11}], isPyData=True))
    :example: >>> myTable.jsAddRow( [{}], isPyData=True )
    :dsc:
        Function to add a row to a table. This will use the internal Javascript data object generated automatically from the event.
        Even a service call will return a data object as a dictionary. The jsDataKey is the key in the data dictionary where the
        relevant row information are.
    :link Datatable website: https://datatables.net/reference/api/row()
    """
    if pyCssCls == 'CssTableNewRow':
      # Add the class to the Python factory and create the reference to it
      pyCssCls = self.addPyCss(pyCssCls)
    if isPyData:
      jsData = json.dumps(jsData)
    return '''
      var uniqKeys = %(uniqKey)s ; var rows = %(rows)s; var keys = {} ;
      if (%(jsDataKey)s != null) { rows = rows[%(jsDataKey)s] ;};
      if (uniqKeys != null) {
        rows.forEach( function(rec) {
          var newKey = [] ; uniqKeys.forEach( function(code) { newKey.push( rec[code] ) ; }) ;
          keys[ newKey.join('#') ] = true ; }) ;
        
        var rowToBeDeleted = -1;
        %(jsTableId)s.rows().every( function ( rowIdx, tableLoop, rowLoop ) {
            var data = this.data();
            var newKey = [] ; uniqKeys.forEach( function(code) { newKey.push( data[code] ) ; }) ;
            if ( newKey in keys) { rowToBeDeleted = rowIdx; } } );
        if (rowToBeDeleted != -1) { %(jsTableId)s.row( rowToBeDeleted ).remove().draw() } ; }
        
      %(jsTableId)s.rows.add( rows ).draw().nodes().to$().addClass( '%(pyCssCls)s' ); %(extraJsInitFnc)s;
      if (typeof data != 'undefined') { data.uniqKeys = uniqKeys; data.row = JSON.stringify(%(rows)s) ; };
      ''' % {'jsTableId': self.jsTableId, 'uniqKey': json.dumps(uniqKey), 'rows': jsData, 'pyCssCls': pyCssCls,
             'jsDataKey': json.dumps(jsDataKey), 'extraJsInitFnc': ";".join(self.extraJsInitFnc)}
  #
  # def jsLoadFromSrc(self, jsDataKey=None):
  #   return '''
  #     $('#%(htmlId)s_loading_icon').show() ; $('#%(htmlId)s').hide(); $('#%(htmlId)s_loading').show();
  #     %(ajax)s ;
  #     ''' % {"ajax": self.aresObj.jsPost(self.dataSrc['script'], jsData=self.dataSrc.get('htmlObjs'), htmlCodes=self.dataSrc.get('htmlCodes'),
  #                                        jsFnc=["$('#%(htmlId)s').show(); $('#%(htmlId)s_loading').hide(); $('#%(htmlId)s_loading_icon').hide() ; " % {"htmlId": self.htmlId},
  #                                               self.jsLoad('data', jsDataKey=jsDataKey), self.jsLastUpdate()] ),
  #            'htmlId': self.htmlId}

  def jsSetRowSelected(self, colNames, jsValue='data.row', jsDataKey=None, isPyData=False, pyCssCls='CssTableSelected'):
    """
    :category: Javascript - Datatable Selections
    :rubric: JS
    :type: Table Event
    :example: >>> click(tb.jsSetRowSelected(['direction'], {'direction': 'Increasing'}, isPyData=True))
    :example: >>> button.click(t3.jsSetRowSelected(["C"], {"C": 1}, isPyData=True))
    :dsc:
      Force the row selection based on a list of value per columns in the table.
      this event should be defined in a Javascript event but as usual parameters can be both Javascript and Python.
    :tip: You can get hold of the selected row at any point of time in the Javascript by using jsClickState() in a js Event
    :return: The javascript fragment to select the matching rows and unselect the rest
    """
    pyCss = self.cssSelection(pyCssCls)
    if isPyData:
      jsValue = json.dumps(jsValue)
    if jsValue == 'data.row':
      jsValue = "JSON.parse(%s)" % jsValue
    if jsDataKey is not None:
      # Here we do not consider the default value of the jsValue as this is coming from jsDataKey
      jsValue = "data['%s']" % jsDataKey
    return ''' 
      if (DATATABLES_STATE['#%(htmlId)s'] != undefined) {
        DATATABLES_STATE['#%(htmlId)s'].forEach( function(rec) {$(%(jsTableId)s.row(rec.row_id).node()).removeClass('%(pyCss)s')})} ;
      DATATABLES_STATE['#%(htmlId)s'] = [] ;
      %(jsTableId)s.rows().every( function (rowIdx, tableLoop, rowLoop) {
        var dataRow = this.data(); var isSelected = true; console.log(dataRow);
        %(colName)s.forEach( function(col) {if (dataRow[col] != %(jsValue)s[col] ) {isSelected = false}}); 
        if (isSelected) { 
          $( %(jsTableId)s.row(rowIdx).node() ).addClass( '%(pyCss)s' );
          DATATABLES_STATE['#%(htmlId)s'].push( {row: JSON.stringify(%(jsTableId)s.rows( $(this) ).data()[0]), row_id: %(jsTableId)s.row( $(this) ).index() } ) 
        }})''' % {'jsTableId': self.jsTableId, 'colName': json.dumps(colNames), 'jsValue': jsValue, 'htmlId': self.htmlId, 'pyCss': pyCss}

  def jsDestroy(self):
    """
    :category: Javascript - Datatable Refresh
    :rubric: JS
    :type: Table Event
    :example: >>> myTable.jsDetroy() ;
    :dsc:
      Function to fully detroy the table definition. once this function is trigger there is no definition at all of this object and the
      datatable needs to be fully redefined (with the column headers, the styles...)
    :return: The javascript string fragment to destroy the table
    :link Datatable Documentation: https://datatables.net/reference/api/destroy()
    """
    return "%s.destroy()" % self.jsTableId

  def jsGetData(self):
    """
    :category: Javascript - Datatable Data Retrieval
    :rubric: JS
    :example: >>> myTable.jsGetData() ;
    :dsc:
      Function to get the datatable data in a table
    :return: The javascript string fragment to destroy the table
    """
    return 'GetTableData(%s)' % self.jsTableId

  def jsGetSize(self):
    """
    :category: Javascript function
    :rubric: JS
    :type: Table Event
    :example: >>> myTable.jsGetSize() ;
    :dsc:
      Function to get the number of rows in the javascript side
    :return: The Javascript string function to get the number of rows as an integer
    """
    return '%s.rows().data().length' % self.jsTableId

  def jsGetRow(self, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Javascript function
    :rubric: JS
    :type: Table Event
    :example: >>> myTable.jsGetRow( 1, isPyData=True ) ;
    :dsc:
      Function to get the row in the datatable from the row ID
    :return: The Javascript string function to get the row as an javascript Array
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '%s.rows().data()[%s]' % (self.jsTableId, jsData)

  def jsGetCol(self, jsData='data', jsDataKey=None, removeDuplicate=True, isPyData=False):
    """
    :category: Javascript function
    :rubric: JS
    :type: Table Event
    :example: >>> click(aresObj.jsConsole(tb.jsGetCol('direction', isPyData=True)))
    :dsc:
      Function to get the column in the datatable from the column name.
      This will return a list with the distinct values or the full column.
      By default distinct values are removed
    :return: The Javascript string function to get the column as an javascript Array
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return ''' function(){
       var columnName = %(jsData)s; var columnNames = [];
       %(jsTableId)s.settings().context[0].aoColumns.forEach(function(col){columnNames.push(col.data)});
       return %(jsTableId)s.column(columnNames.indexOf(columnName)).data().toArray()%(uniqueVals)s}()
       ''' % {'jsData': jsData, 'jsTableId': self.jsTableId, 'uniqueVals': '.unique()' if removeDuplicate else ''}


  # -----------------------------------------------------------------------------------------
  #                                ADD SYSTEM EVENT COLUMNS
  # -----------------------------------------------------------------------------------------
  # def addEventCol(self, icon, jsEvent, eventName=None, tooltip=''):
  #   if isinstance(jsEvent, list):
  #     jsEvent = ";".join(jsEvent)
  #   pyCssCls = self.addPyCss('CssTableColumnSystem')
  #   colReference = icon.replace(" ", "").replace("-", '') if eventName is None else eventName
  #   self.__table.header.append({'data': colReference, 'className': '%s %s' % (pyCssCls, colReference), 'title': '<div class=\'%s\'></div>' % icon, 'width': '5px',
  #                               'dsc': tooltip, 'format': '"<div name=\'%s\' title=\'%s\' style=\'cursor:pointer\' class=\'%s\'></div>"' % (self.htmlId, tooltip, icon)})
  #   self.aresObj.jsOnLoadFnc.add('''
  #       $(document).on('click', '.%(colReference)s', function() {
  #         var jsTableId = window[$(this).find('div').attr('name') + '_table'];
  #         var data = {row: JSON.stringify(jsTableId.rows( $(this) ).data()[0]), row_id: jsTableId.row( $(this) ).index(), event: '%(colReference)s' } ;
  #         %(jsPost)s}) ''' % {"colReference": colReference, 'jsPost': jsEvent, 'pyCssCls': pyCssCls })
  #   return self
  #
  # def addColDelete(self, deleteCol):
  #   pyCssCls = self.addPyCss('CssTableColumnSystem')
  #   self.__table.header.append({'data': '_delete', 'className': '%s delete_%s' % (pyCssCls, self.htmlId), 'title': '<div class=\'far fa-trash-alt\'></div>', 'width': '5px',
  #                               'format': '"<div id=\'delete\' name=\'%s\' title=\'Delete Row\' style=\'cursor:pointer\' class=\'far fa-trash-alt\'></div>"' % self.htmlId})
  #
  #   jsPost = self.aresObj.jsPost(deleteCol['url'], None, deleteCol.get('success', ''), htmlCodes=deleteCol.get('htmlCodes')) if isinstance(deleteCol, dict) else ''
  #   self.aresObj.jsOnLoadFnc.add('''
  #           $( document ).on('click', '.delete_%(htmlId)s', function() {
  #             if ($(this).find('div').attr('id') == 'delete') {
  #             var jsTableId = window[$(this).find('div').attr('name') + '_table'];
  #             var data = {row: JSON.stringify(jsTableId.rows( $(this) ).data()[0]), row_id: jsTableId.row( $(this) ).index(), event: 'delete' } ;
  #             jsTableId.row( $(this).parents() ).remove().draw('page');
  #             %(jsPost)s } }) ''' % {"deleteCls": pyCssCls, 'jsPost': jsPost, 'htmlId': self.htmlId})
  #   return self
  #
  # def addColSave(self, saveRow):
  #   self.addGlobalVar("%s_changed" % self.jsTableId, "true")
  #   pyCssCls = self.addPyCss('CssTableColumnSystem')
  #   self.__table.header.append({'data': '_save', 'className': '%s save_%s' % (pyCssCls, self.htmlId), 'title': '<div class=\'fas fa-check\'></div>', 'width': '5px',
  #                               'dsc': 'Click on the icon to save the row',
  #                               'format': '"<div id=\'save\' name=\'%s\' title=\'Save Row\' style=\'cursor:pointer;display:none\' class=\'fas fa-check\'></div>"' % self.htmlId})
  #
  #   jsPost = self.aresObj.jsPost(saveRow['url'], None, saveRow.get('success', ''), htmlCodes=saveRow.get('htmlCodes')) if 'url' in saveRow else ''
  #   self.aresObj.jsOnLoadFnc.add('''
  #         $( document ).on('click', '.save_%(htmlId)s', function() {
  #           if ($(this).find('div').css('display') != 'none' ) {
  #           var jsTableId = window[$(this).find('div').attr('name') + '_table'];
  #           var data = {row: JSON.stringify(jsTableId.rows( $(this) ).data()[0]), row_id: jsTableId.row( $(this) ).index(), event: 'save' } ;
  #           %(jsPost)s; $(this).find('div').css('display', 'none'); } }) ''' % {"deleteCls": pyCssCls, 'jsPost': jsPost, 'htmlId': self.htmlId})
  #   return self

  def setHeader(self, extraHeaders=None, cssClsStyles=None, cssClsHeader=None):
    """
    :category: Table Definition
    :rubric: HTML
    :type: Style
    :dsc:
      Add an extra layer on top of the header
    :example:
      tb.setHeader([
        [{'value': 'a', 'cols': 3, 'rows': 2}, {'value': 'b', 'cols': 3, 'rows': 1}],
        [{'value': 'd', 'cols': 3, 'rows': 1}]])
    :return: The Python Datatable object
    """
    headers = []
    if extraHeaders is not None:
      for i, h in enumerate(extraHeaders):
        tr = '<tr>'
        if cssClsStyles is not None:
          if isinstance(cssClsStyles, list):
            if cssClsStyles[i] is not None:
              tr = '<tr class="%s">' % cssClsStyles[i]
          else:
            tr = '<tr class="%s">' % cssClsStyles
        print(tr)
        headers.append("%s%s</tr>" % (tr, "".join(["<th colspan='%s' title='%s' rowspan='%s'>%s</th>" % (v.get('cols', 1), v.get('title', ''), v.get('rows', 1), v['value']) for v in h])))
    if cssClsHeader is not None and self.aresObj.cssObj.get(cssClsHeader) is not None:
      self.addPyCss(cssClsHeader)
      headers.append("<tr class='%s'>%s</tr>" % (self.aresObj.cssObj.get(cssClsHeader)().classname, "".join(["<th>%s</th>" % h['title'] for h in self.__table.header])))
    else:
      headers.append("<tr>%s</tr>" % "".join(["<th class='%s'>%s</th>" % (h['title'], h.get('class')) for h in self.__table.header]))
    self.header = "<thead>%(headers)s</thead>" % {'headers': "".join(headers)}
    return self

  def setFooter(self, row):
    """
    :category: Table Definition
    :rubric: HTML
    :type: Style
    :dsc:
      Add a footer to the table
    :example:
      tb.setFooter(['', '', 0, 1, 2, 3, 4])
    :return: The Python Datatable object
    """
    titles = ['<th>%s</th>' % (h['value'] if isinstance(h, dict) else h) for h in row]
    self.footer = '<tfoot><tr>%(columns)s</tr></tfoot>' % {'columns': "".join(titles)}
    return self

  def setTableCss(self, cssClss):
    """
    :category: Table Definition
    :rubric: CSS
    :type: Style
    :dsc:
      Add a style to the datatable. This can be used to change some specific part of the table (for example the header)
    :example:
      class CssTableHeader(object):
        __style = [{'attr': 'background', 'value': 'grey'}]
        childrenTag = 'th'

      tb.setTableCss(CssTableHeader)
    :return: The Python Datatable object
    """
    import inspect

    if not isinstance(cssClss, list):
      cssClss = [cssClss]

    for cssCls in cssClss:
      if inspect.isclass(cssCls):
        self.aresObj.cssObj.addPy(cssCls)
        cssCls = cssCls.__name__
      clssMod = self.aresObj.cssObj.get(cssCls)
      if clssMod is not None:
        self.addPyCss(cssCls)
        self.tableStyle.append(clssMod().classname)
    return self


  # -----------------------------------------------------------------------------------------
  #                                JAVASCRIPT CLICK EVENTS
  # -----------------------------------------------------------------------------------------
  # TODO finalise event on col and Row
  # TODO Add the global filtering aspect
  # TODO Add the possibility to add or remove columns on demand
  def jsClickState(self, htmlId=None):
    """
    :category: Javascript Event
    :rubric: JS
    :example: myObj.jsClickState()
    :dsc:
      Python function to return the javascript state of a table (the selected information)
    :return: Javascript list with the selected data
    """
    if htmlId is None:
      return "DATATABLES_STATE['#%(htmlId)s']" % {'htmlId': self.htmlId}

    return "DATATABLES_STATE"

  def clickRow(self, jsFncs, rowIndices=None, pyCssCls='CssTableSelected'):
    """
    :category: Javascript Event
    :rubric: JS
    :type: Table Event
    :example: >>> tableObj.clickRow( aresObj.jsConsole() )
    :dsc:
    :return: Javascript String of the variable used to defined the Jquery object in Javascript
    """
    self.cssSelection(pyCssCls)
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    self.clickCell(jsFncs, rowIndices=rowIndices)
    return self

    # self.aresObj.jsOnLoadFnc.add('''
    #   $('#%(htmlId)s').css( 'cursor', 'pointer') ;
    #   $('#%(htmlId)s').on('click', '%(eventSrc)s', function () {
    #     var loading = $("<div style='position:fixed;background:white;padding:5px;z-index:10;bottom:20px;left:60px;color:black' id='cell_loading'><i class='fas fa-spinner fa-spin'></i>&nbsp;&nbsp;Loading...</div>" ) ;
    #     $(this).append(loading) ; var useAsync = false ;
    #     if ( DATATABLES_STATE['#%(htmlId)s'] != undefined ) {
    #        DATATABLES_STATE['#%(htmlId)s'].forEach( function (rec) {
    #           $(%(jsTableId)s.row(rec.row_id).node()).removeClass( '%(pyCss)s' );
    #           $( %(jsTableId)s.row(rec.row_id).node()).find('td').each (function() {
    #               $(this).css( {"background-color": $(this).data("background") } ) ; }) ;
    #        } ) } ;
    #     DATATABLES_STATE['#%(htmlId)s'] = [] ;
    #     var data = {row: JSON.stringify(%(jsTableId)s.rows( $(this) ).data()[0]), row_id: %(jsTableId)s.row( $(this) ).index() } ;
    #     DATATABLES_STATE['#%(htmlId)s'].push( data );
    #
    #     $( %(jsTableId)s.row(data.row_id).node()).find('td').each (function() {
    #         $(this).data("background",  $(this).css("background-color") ) ;
    #         $(this).css( {"background-color": ""} ) ;
    #     }) ;
    #
    #     $( %(jsTableId)s.row(data.row_id).node() ).addClass( '%(pyCss)s' );
    #     %(jsFncs)s ; %(jsTableId)s.draw('page') ;
    #     if (!useAsync) { loading.hide() ; }} );
    #   ''' % {'htmlId': self.htmlId, 'jsTableId': self.jsTableId, 'jsFncs': ";".join(jsFncs), 'eventSrc': eventSrc, 'pyCss': pyCss} )

  def clickCol(self, jsFncs, colIndices=None, colNames=None):
    """
    :category: Javascript Event
    :rubric: JS
    :type: Table Event
    :example: tableObj.clickCol( aresObj.jsConsole() )
    :example: tableObj.clickCol( aresObj.jsConsole(), ['col1'] )
    :dsc:
      Function to add a click event on columns. If the variable colNames is not defined with a list of columns
      the framework will assume that the event should be applied on all the columns of the table
    :Tip: You can get the selected column by using the function jsClickState in a javascript Event function
    :return: The Javascript Fragment to enable the click on columns
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    if not isinstance(colNames, list):
      colNames = [colNames]
    if colNames is not None:
      colIds = [self.columns.index(colName) for colName in colNames]
    if colIndices is not None:
      colIndices += colIds
    else:
      colIndices = colIds
    self.clickCell(jsFncs, colIndices=colIndices)
    return self

  def clickCell(self, jsFncs, rowIndices=None, colIndices=None, colorSelected=True, pyCssCls='CssTableSelected'):
    """
    :category: Javascript Event
    :rubric: JS
    :type: Table Event
    :example: >>> t2.clickCell( aresObj.jsPost("BarChartData.py", jsFnc=barChart.jsGenerate() ) )
    :dsc:
      Function to add a click event on each cell in the table. It is possible to limit on some columns and row by using the
      variable rowIndex and colIndex
    :link Datatable Documentation: https://datatables.net/forums/discussion/46445/get-column-name-by-index
    :return: The Javascript Fragment to enable the click on columns
    """
    if colIndices is not None and not isinstance(colIndices, list):
      colIndices = [colIndices]
    if rowIndices is not None and not isinstance(rowIndices, list):
      rowIndices = [rowIndices]
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    pyCss = self.cssSelection(pyCssCls)
    pyCssSystemCls = self.getPyCss('CssTableColumnSystem')
    self.aresObj.jsOnLoadFnc.add('''
      $('#%(htmlId)s').css('cursor', 'pointer');
      $('#%(htmlId)s').on('click', 'td:not(.%(pyCssDeleteCls)s)', function () { 
        var isValid = true; 
        if((%(rowIndex)s != null) && ( %(rowIndex)s.indexOf(%(jsTableId)s.cell($(this)).index().row)) < 0) {isValid = false};
        if((%(colIndex)s != null) && ( %(colIndex)s.indexOf(%(jsTableId)s.cell($(this)).index().column)) < 0) {isValid = false};
        if (isValid) {
          var loading = $("<div style='position:fixed;background:white;padding:5px;z-index:10;bottom:20px;left:60px;color:black' id='cell_loading'><i class='fas fa-spinner fa-spin'></i>&nbsp;&nbsp;Loading...</div>" ) ;
          $(this).append(loading); var useAsync = false;
          if (DATATABLES_STATE['#%(htmlId)s'] != undefined) {
            DATATABLES_STATE['#%(htmlId)s'].forEach(function (rec) { 
              $(%(jsTableId)s.cell(rec.row_id, rec.col_id).node()).removeClass('%(pyCss)s')})};
          var data = {cell: %(jsTableId)s.cell($(this)).data(), row: JSON.stringify(%(jsTableId)s.rows($(this)).data()[0]), 
                      row_id: %(jsTableId)s.cell($(this)).index().row, col_id: %(jsTableId)s.cell($(this)).index().column,  
                      col_name: %(jsTableId)s.settings().init().columns[%(jsTableId)s.cell($(this)).index().column].title}; 
          DATATABLES_STATE['#%(htmlId)s'] = [data];
          if (%(colorSelected)s) {$(%(jsTableId)s.cell(data.row_id, data.col_id).node()).addClass('%(pyCss)s')}
          %(jsFncs)s; %(jsTableId)s.draw('page');
          if (!useAsync) {loading.hide()}}
        });
      ''' % {'pyCssDeleteCls': pyCssSystemCls, 'htmlId': self.htmlId, 'jsTableId': self.jsTableId, 'jsFncs': ";".join(jsFncs),
             'rowIndex': json.dumps(rowIndices), 'colIndex': json.dumps(colIndices), 'colorSelected': json.dumps(colorSelected), 'pyCss': pyCss})


  # -----------------------------------------------------------------------------------------
  #                                    TABLE EXPORT OPTIONS
  # -----------------------------------------------------------------------------------------
  def __str__(self):
    #     # self.addGlobalFnc("GetTableData(tableObj)", '''
    #     #   result = [] ;
    #     #   var data = tableObj.rows().data() ;
    #     #   for(var i = 0; i < data.data().length ; i++) { result.push(data[i]) ; }; return result; ''',
    #     #                   'Function to get in an Array the content of a Datatable')
    #     # options = []
    #     # if self.addCol is not None:
    #     #   plus = self.aresObj.plus()
    #     #   row = []
    #     #   for code, htmlObj in self.addCol.get('htmlObj', {}).items():
    #     #     row.append( '"%s": %s' % (code, htmlObj.val))
    #     #   for code, vals in self.addCol.get('default', {}).items():
    #     #     row.append( '"%s": %s' % (code, json.dumps(vals) ))
    #     #   row.append( 'last_mod_dt : Today()')
    #     #   self.addGlobalVar('%s_default_row' % self.jsTableId, '[ {%s} ]' % ','.join(row) )
    #     #   plus.click( self.jsAddRow( jsData="window['%s_default_row']" % self.jsTableId, uniqKey=self.addCol.get('uniqKey') ) )
    #     #   options.append(plus.html())
    #     # if self.calculator:
    #     #   options.append(self.aresObj.calculator(self.jqId).html())
    #     # if self.refresh:
    #     #   if self.dataSrc is not None and self.dataSrc['type'] == 'script':
    #     #     r = self.aresObj.refresh()
    #     #     r.click(self.jsLoadFromSrc(self.dataSrc.get('jsDataKey')))
    #     #     options.append(r.html())
    #     # if self.comment:
    #     #   t = self.aresObj.thumbtack(self.jqId)
    #     #   options.append(t.html())
    #     # if self.download:
    #     #   copy = self.aresObj.upButton()
    #     #   copy.click("%s.buttons('.buttons-copy').trigger();" % self.jsTableId)
    #     #   options.append(copy.html())
    #     # if self.pdf:
    #     #   pdf = self.aresObj.pdf()
    #     #   pdf.click(["%s.buttons('.buttons-pdf').trigger();" % self.jsTableId])
    #     #   options.append(pdf.html())
    #     # if self.excel:
    #     #   excel = self.aresObj.excel()
    #     #   excel.click("%s.buttons('.buttons-excel').trigger();" % self.jsTableId)
    #     #   options.append(excel.html())
    #     # if self.magnify:
    #     #   zoom = self.aresObj.zoom()
    #     #   zoom.click( '''
    #     #      if ( $('#%(htmlId)s').css('position') != 'fixed' ) {
    #     #        $('#%(htmlId)s').css( {'position': 'fixed', 'top': 0, 'left':0, 'background-color': 'white', 'height': '100%%', 'width': '100%%', 'z-index': 1300} );
    #     #     } else {
    #     #        $('#%(htmlId)s').css( {'position': 'relative' , 'z-index': 1} ); }
    #     #     %(jsTableId)s.draw() ;
    #     #     ''' % { 'htmlId': self.htmlId, 'jsTableId': self.jsTableId } )
    #     #   options.append(zoom.html())
    #     # #remove = self.aresObj.remove()
    #     # #remove.click([self.jsRemove()])
    #     # #options.append(remove.html())

    return '''
      <div %(strAttr)s><table class='%(tableCss)s'>%(header)s%(footer)s</table></div>
      ''' % {'strAttr': self.strAttr(pyClassNames=['CssDivWithBorder']), 'header': self.header, 'footer': self.footer, 'tableCss': " ".join(self.tableStyle)}

    # return '''
    #     <div id="%(htmlId)s_loading" style="display:none;height:%(height)s" %(loading)s>
    #       <div style="margin:auto;font-size:20px;width:40%%">
    #         <div style="width:100%%;text-align:right;padding:5px 10px 0 0">
    #             <i class="fas fa-times-circle" onclick="$('#%(htmlId)s_loading').hide(); $('#%(htmlId)s').show()"></i>
    #         </div>
    #         <p>Loading...</p>
    #         <i id="%(htmlId)s_loading_icon" class="fas fa-spinner fa-spin"></i><br />
    #       </div>
    #     </div>
    #
    #     <div %(strAttr)s>
    #       <div style="height:25px;width:100%%">
    #         <div style="height:25px;clear:left;float:left;margin-bottom:8px;font-size:16px;font-weight:bold;font-variant:small-caps;">%(title)s</div>
    #         <div style="height:25px;clear:right;float:right;color:#F5F5F5;text-align:right;align:right">%(options)s</div>
    #       </div>
    #       <div style="overflow:auto;width:100%%;height:100%%;">
    #         %(comments)s
    #         <table name='aresTable' class='%(tableStyle)s' style="width:%(tableWidth)s">%(header)s%(footer)s</table>
    #       </div>
    #       <div style='width:100%%;text-align:right;height:20px'>%(wrench)s<p id='%(htmlId)s_processing' style="margin-top:3px;font-size:12px;float:left;display:block;color:%(color)s"></p> &nbsp;&nbsp;%(clock)s<p id='%(htmlId)s_updated' style="margin-top:3px;font-size:12px;float:right;display:block;color:%(color)s">%(timestamp)s</p></div>
    #     </div>''' % {'strAttr': self.strAttr(pyClassNames=['CssDivWithBorder']), 'title': self.title, 'options': "".join(reversed(options)),
    #                'clock': self.aresObj.clock(''), 'color': self.getColor('border', 1), 'timestamp': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    #                'footer': ''.join(footer), 'header': ''.join(self.htmlHeader()), 'tableStyle': self.tableStyle,
    #                'wrench': self.aresObj.wrench('left'), 'htmlId': self.htmlId, "width": self.width, "tableWidth": self.tableWidth,
    #                'loading': self.aresObj.cssObj.getClsTag(['CssDivLoading']),
    #                'height': self.height, 'comments': self.dsc_comment}

  def to_word(self, document):
    """
    :category: Word export
    :rubric: Output
    :example: aresObj.to_word()
    :dsc:
      Special output function used by the framework to export the report to a word document
      This function cannot be used directly as it will write the report on the server but some buttons are available on the top to trigger it
    :link docx Documentation: http://python-docx.readthedocs.io/en/latest/
    """
    data = self.data.records()
    table = document.add_table(rows=1, cols=len(self.__table.header))
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(self.__table.header):
      hdr_cells[i].text = header['title']

    if len(self.__table.header) < 10 and len(data) < 20:
      for rec in data:
        row_cells = table.add_row().cells
        for i, header in enumerate(self.__table.header):
          row_cells[i].text = str(rec[header['data']])

  def to_xls(self, workbook, worksheet, cursor):
    """
    :category: Excel export
    :rubric: Output
    :example: aresObj.to_xls()
    :dsc:
      Special output function used by the framework to export the report to an Excel document
      This function cannot be used directly as it will write the report on the server but some buttons are available on the top to trigger it
    """
    if self.title != '':
      cell_format = workbook.add_format({'bold': True, 'align': 'center'})
      worksheet.merge_range(cursor['row'], cursor['col'], cursor['row'], cursor['col']+len(self.__table.header)-1, self.title, cell_format)
      cursor['row'] += 1

    for i, header in enumerate(self.__table.header):
      worksheet.write(cursor['row'], i, header['title'])
    cursor['row'] += 1
    for rec in self.data.records():
      for i, header in enumerate(self.__table.header):
        worksheet.write(cursor['row'], i, rec[header['data']])
      cursor['row'] += 1

    cursor['row'] += 1


  # -----------------------------------------------------------------------------------------
  #                                    MARKDOWN SECTION
  # -----------------------------------------------------------------------------------------
  @classmethod
  def matchMarkDownBlock(cls, data): return True if data[0].strip().startswith( "---Table" ) else None

  @staticmethod
  def matchEndBlock(data): return data.endswith("---")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj=None):
    """
    :category: Markdown
    :rubric: PY
    :example: Data structure recognised
      ---Table
      label|value|color
      Test 1|35|yellow
      Test 2|25|blue
      ---
    :dsc:
      convert the markdown text to a valid aresObj item.
      In order to include it to a report it is necessary to pass the aresObj
    """
    tableConfig = data[0].split(':')
    tableType = tableConfig[-1] if len(tableConfig) > 1 else 'base'
    headers = data[1].strip().split("|")
    records, pmts, attr = [], {}, {}
    for line in data[2:-1]:
      rec = {}
      if line.startswith("@"):
        dataAttr = line[1:].strip().split(";")
        for d in dataAttr:
          a, b = d.split(":")
          attr[a] = b
        continue

      if line.startswith("--"):
        dataAttr = line[2:].strip().split(";")
        for d in dataAttr:
          a, b = d.split(":")
          pmts[a] = b
        continue

      splitLine = line.replace(",", '.').strip().split("|")
      for i, val in enumerate( splitLine ):
        if i == 0:
          rec[headers[i]] = val
        else:
          rec[headers[i]] = val
      records.append(rec)

    if aresObj is not None:
      if 'pageLength' in pmts:
        pmts['pageLength'] = int(pmts['pageLength'])
      p = aresObj.table(records, header=headers, rows=headers, cols=[], tableTypes=tableType, tableOptions=pmts)
      p.addAttr(attr, isPyData=False)
    return []

  def jsMarkDown(self): return ""


class DataExcel(AresHtml.Html):
  """
  :category: Excel Data Table
  :rubric: JS
  :dsc:

  """
  name, category, callFnc, docCategory = 'Excel', 'Excel', 'excel', 'Standard'
  cssTitle = "CssTitle4"
  __pyStyle = ['CssTableExcel', 'CssTableExcelHeaderCell', 'CssTableExcelTd']

  def __init__(self, aresObj, recordSet, cols, rows, title, width, widthUnit, height, heightUnit, cellwidth, delimiter, htmlCode):
    self.title, self.recordSet, self.delimiter = title, recordSet, delimiter
    super(DataExcel, self).__init__(aresObj, [], code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self._jsStyles = {'header': rows + cols, 'cellwidth': cellwidth}
    self.css({'display': 'inline-block', 'overflow': 'auto', 'padding': 0, 'vertical-align': 'top'})

  @property
  def val(self):
    return "JSON.stringify(tableData(%s))" % self.jqId

  @property
  def records(self):
    return "listToRec(tableData(%s), %s)" % (self.jqId, json.dumps(self._jsStyles['header']))

  @property
  def jqId(self):
    """ Refer to the internal select item """
    return "$('#%s table')" % self.htmlId

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' htmlObj.empty();
      var tr = $('<tr></tr>');
      jsStyles.header.forEach(function(rec){tr.append("<th>"+ rec +"</th>")});
      htmlObj.append(tr); var tr = $('<tr></tr>'); var tbody = $('<tbody></tbody>');
      jsStyles.header.forEach(function(rec){tr.append("<td><input type='text' style='"+ jsStyles.cellwidth +"'/></td>")});
      tbody.append(tr);htmlObj.append(tbody)''')

  def __str__(self):
    self.aresObj.jsOnLoadFnc.add('''
      function tableData(tableObj){
        res = [];
        tableObj.find('tbody').find('tr').each(function(key, val){
          var row = [];
          $(this).find('td').each(function(key, cell) { row.push($(cell).find('input').val())});
          res.push(row)}); return res};
      
      function listToRec(data, header){
          var res = [];
          data.forEach(function(row){
            rec = {};
            header.forEach(function(h, i){rec[h] = row[i];});
            res.push(rec);
          }); return res}''')

    self.paste('''
      var tbody = $(this).find('tbody'); tbody.empty();
      var tableId = $(this).parent().attr('id');
      var lineDelimiter = $('#' + tableId + '_delimiter').val();
      if (lineDelimiter == 'TAB'){ lineDelimiter = '\\t' };
      data.split("\\n").forEach(function(line){
        if (line !== ''){
          var tr = $('<tr></tr>');
          line.split(lineDelimiter).forEach(function(rec){ tr.append("<td><input type='text'  value='"+ rec +"'/></td>")
        }); tbody.append(tr)}}) ''')
    title = ''
    if self.title != '':
      cssMod, titleCls = self.aresObj.cssObj.get(self.cssTitle), ""
      if cssMod is not None:
        self.addPyCss(self.cssTitle)
        titleCls = cssMod().classname
      title = '<div class="%(titleCls)s" style="margin:0;display:inline-block;margin-bottom:5px">%(title)s</div>' % {'titleCls': titleCls, 'title': self.title}
    if self.delimiter is None:
      delimiter = '<input id="%s_delimiter" type="text" value="%s" placeholder="Line delimiter"/>' % (self.htmlId, self.delimiter)
    else:
      delimiter = '<input id="%s_delimiter" type="text" value="%s" style="display:none" placeholder="Line delimiter"/>' % (self.htmlId, self.delimiter)
    return '<div %(strAttr)s>%(title)s%(delimiter)s<table></table></div>' % {'strAttr': self.strAttr(pyClassNames=self.pyStyle), 'title': title, 'delimiter': delimiter}