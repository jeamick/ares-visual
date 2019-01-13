#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
import inspect
import sys

# The columns definition factory
factory = None

def definedColumns():
  global factory

  if factory is None:
    tmpFactory = {}
    for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
      if getattr(obj, 'alias', None) not in [None, '__main__']:
        tmpFactory[obj.alias] = obj
    # Atomic function to avoid asynchronous clashes on the server
    factory = tmpFactory
  return factory


def extTableFactory(cls):
  """
  :category: Columns Factory
  :rubric: PY
  :type: Framework Extension
  :dsc:
    Add to the factory the user defined entries.
    Those entries should be added to the system
  """
  factor = definedColumns()
  if not cls.alias in factor:
    factor[cls.alias] = cls
    return True


class TableCols(object):
  """
  :category: Table Row Creator
  :type: Configuration
  :rubric: JS
  :dsc:
    Wrapper on top the of the function aoColumnDefs in the Datatable configuration
  :link Datatable Documentation: http://legacy.datatables.net/usage/columns
  """

  def __init__(self, aresObj):
    # self.countStyles is used to split the multiple configuration attached to the _all columns
    self.cols, self.countStyles, self.aresObj = {}, 0, aresObj

  def typeAttrs(self, prefix, attrs):
    return dict([("%s_%s" % (prefix, k), v) for k, v in attrs.items()])

  def add(self, idCols, colObj, attr=None):
    """
    :category: Add Style
    :rubric: JS
    :type: System
    :dsc:
      Add a column configuration to the table definition object.
      This object will be in charge of the final rendering of the style of the table
    """
    definedCols = definedColumns()
    if not isinstance(idCols, list):
      idCols = [idCols]
    if attr is None:
      attr = {}
    for idCol in idCols:
      prefix = self.aresObj.cleanData("%s_%s_%s" % (idCol, self.countStyles, colObj))
      if idCol == '_all':
        for colDef, colVals in self.cols.items():
          _attrs = dict(getattr(definedCols[colObj], '_dflts', {}))
          _attrs.update(attr)
          newColObj = definedCols[colObj](self.typeAttrs(prefix, _attrs), prefix)
          colVals.add(newColObj)
          colVals._attrs.update(newColObj._attrs)

      if idCol not in self.cols:
        _attrs = dict(getattr(definedCols[colObj], '_dflts', {}))
        _attrs.update(attr)
        self.cols[idCol] = definedCols[colObj](self.typeAttrs(prefix, _attrs), prefix)
      else:
        _attrs = dict(getattr(definedCols[colObj], '_dflts', {}))
        _attrs.update(attr)
        newColObj = definedCols[colObj](self.typeAttrs(prefix, _attrs), prefix)
        self.cols[idCol].add(newColObj)
        self.cols[idCol]._attrs.update(newColObj._attrs)
      self.countStyles += 1

  def get(self):
    """
    :category: Factory
    :rubric: PY
    :type: System
    :dsc:
      Return a copy of the factory for analysis.
      This function is not called directly by it is available from the scripting interface in the tablesInfo() function
    """
    return dict(definedColumns())

  def toJs(self):
    """
    :category: Javascript Conversion
    :rubric: PY
    :type: System
    :dsc:
      Internal function to convert the table definition to a valid javascript definition for the Datatable library.
      This method will produce a pure javascript string which will be run in the web browser at the end.
      Some sanity checks are done in this layer to ensure a good quality of the Javascript generated
    """
    aoColumnDefs = []
    for col, vals in self.cols.items():
      aoColumnDefs.append("{aTargets: %s, %s}" % (json.dumps(col), vals.toJs()))
    return "[%s]" % ",".join(aoColumnDefs)


class TableColsFrg(object):
  """
  :category: Datatable Column Definition
  :type: Column
  :rubric: JS
  :dsc:
    Base class for an entry on the section aoColumnDefs of the Datatable.
    This class should not be used directly but configuration should derived from this one.
  """

  # parameters used for an entry in an item of the list aoColumnDefs
  __slots__ = ['visible', 'jsCreatedCell', 'cellClass', 'jsRenderFnc', 'type', 'reqJs']

  def __init__(self, attrs, prefix=""):
    self._attrs = {} if attrs is None else attrs
    for slot in ['jsCreatedCell', 'cellClass']:
      value = getattr(self, slot, None)
      if value is not None:
        value = [v.replace("%(", "%%(%s_" % prefix) for v in value]
        setattr(self, slot, value)

  def add(self, colObj):
    """
    :category: Column Merge
    :type: PY
    :rubric: System
    :dsc:
      Function in charge of the merge of two columns definition. This will guarantee that the data defined in the
      first column definition will not be overridden by the new one.
      This method will group the complementary sections and replace the unique ones
    """
    for slot in colObj.__slots__:
      value = getattr(colObj, slot, None)
      if value is not None:
        if slot in ['visible', 'type']:
          setattr(self, slot, value)
        else:
          if getattr(self, slot, None) is None:
            setattr(self, slot, [])
          setattr(self, slot, getattr(self, slot) + value)
    if getattr(colObj, 'jsRenderReturn', None) is not None:
      self.jsRenderReturn = colObj.jsRenderReturn
    return self

  def toJs(self):
    """
    :category: Column Definition Conversion
    :type: PY
    :rubric: System
    :dsc:
      Function in charge of converting the Python column definition to a valid javascript object which can be used
      in the parameter columnDefs of the datatable.
    """
    mapAttr = {'visible': 'bVisible: %s', 'jsCreatedCell': 'fnCreatedCell: function (nTd, sData, oData, iRow, iCol){%s}',
               'cellClass': 'sClass: %s', 'jsRenderFnc': 'mRender: function (data, type, row, meta) {%s}', 'type': 'sCellType: %s'}
    attrs = []
    for slot in ['visible', 'jsCreatedCell', 'cellClass', 'jsRenderFnc', 'type']:
      value = getattr(self, slot, None)
      if value is not None:
        if isinstance(value, list):
          if slot == 'cellClass':
            value = " ".join(value)
          elif slot in ['jsRenderFnc', 'jsCreatedCell']:
            value, tmpVal = ";".join(value), []
            for line in value.split("\n"):
              tmpVal.append(line.strip())
            value = " ".join(tmpVal)
            if slot == 'jsRenderFnc':
              if getattr(self, 'jsRenderReturn', None) is None:
                raise Exception("jsRenderReturn should be defined when jsRenderFnc is used")

              value = "%s;return %s" % (value, getattr(self, 'jsRenderReturn', None))
          else:
            value = ";".join(value)
        if slot in ['visible', 'type', 'cellClass']:
          value = json.dumps(value)
        attrs.append(mapAttr[slot] % value % self._attrs)
    return ", ".join(attrs)



# --------------------------------------------------------------------------------------------------------------
#
#                                     STYLE DEFINITION FOR COLUMNS
# --------------------------------------------------------------------------------------------------------------
class TableColsHidden(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Set the visible flag to False. The column and data will be available in the row dictionary but it will not
    be displayed in the interface.
  """
  alias = 'hidden'
  visible = False


class TableColStyleCss(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Style in charge of adding some CSS attributes to a cellule of the table.
    This column method will use the css [Jquery](http://api.jquery.com/css/) function.
    Any attributes available in CSS can be used.
    The full reference is available [here](https://www.w3schools.com/cssref/default.asp)
  """
  alias = 'css'
  jsCreatedCell = ["$(nTd).css(%(css)s)"]


class TableColStyleNumber(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Default style for values in a datatable. Columns defined as values will be displayed in red if negative and the
    number of digits will be 0. By default the table will only display integers
  """
  alias = 'number'
  _dflts = {'color': 'red', 'digits': 0, 'threshold': 0}
  jsCreatedCell = ['''
    if (sData !== null){
      if(sData < %(threshold)s){$(nTd).css('color', '%(color)s')}; 
      sData = sData.formatMoney(%(digits)s, ',', '.'); $(nTd).text(sData)}
    else {$(nTd).text(sData)}''']


class TableColStyleNumberReport(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Alternative format for numbers used in some official documentation. This will not color the negative numbers but
    it will be them between (). By default the number of digits is 0 so it will only display integers
  """
  alias = 'number-report'
  _dflts = {'digits': 0, 'threshold': 0}
  jsCreatedCell = ['''
    if (sData !== null){
      if(sData < %(threshold)s){ sData =  Math.abs(sData).formatMoney(%(digits)s, ',', '.'); sData = '('+ sData +')' } 
      else {sData =  Math.abs(sData).formatMoney(%(digits)s, ',', '.')}
      $(nTd).html(sData)}
    else {$(nTd).html(sData)}''']


class TableColStyleCssId(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Apply a format to a dedicated row in the column. Only this row number will be impacted by this formatting.
    Be aware that row number might not be the same than the ones defined in the datatable.
  """
  alias = 'css_id'
  jsCreatedCell = ["if(iRow == %(id)s) {$(nTd).css(%(cssCell)s)}"]


class TableColStyleCssValue(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Apply a format to a dedicated row in the column. Only this row with the key validating the condition will get the
    CSS Style applied.
  """
  _dflts = {'operator': "=="}

  alias = 'css_value'
  jsCreatedCell = ["if(oData['%(col)s'] %(operator)s %(val)s) {$(nTd).css(%(cssCell)s)}"]


class TableColStyleClass(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Apply a class to all the cell in the column. This will apply a pre defined CSS class.
    This function does not accept CSS parameters. More details about the HTML CSS Classes [here](https://www.w3schools.com/html/html_classes.asp)
  """
  alias = 'class'
  cellClass = ["%(class)s"]


class TableCellStyleAge(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Function in charge of changing the background color of the cell object if the age is added to the recordSet.
    This will automatically assigned a color to the age.
  """
  reqJs = ['d3']
  alias = 'age'
  _dflts = {'start': 'white', 'end': 'red', 'steps': 100, 'factor': 100}
  jsCreatedCell = ['''
    var colorFnc = d3.scale.linear().domain([1, %(steps)s]).range([d3.rgb('%(start)s'), d3.rgb('%(end)s')]);
    var cellAge = getDict(oData, %(table)s[iCol].data + '.age', 0);
    $(nTd).css('background-color', colorFnc(%(factor)s * cellAge));
    if (cellAge > 0){
      var curTitle = $(nTd).attr("title"); if (curTitle === undefined) {curTitle = ''};
      $(nTd).attr("title", 'cell age: ' + cellAge)}
    ''']


class TableCellStyleQuality(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:

  """
  reqJs = ['d3']
  alias = 'quality'
  _dflts = {'start': 'white', 'end': 'red', 'steps': 100, 'factor': 100}
  jsCreatedCell = ['''
    var colorFnc = d3.scale.linear().domain([1, %(steps)s]).range([d3.rgb('%(start)s'), d3.rgb('%(end)s')]);
    var cellQuality = getDict(oData, %(table)s[iCol].data + '.quality', 0);
    $(nTd).css('border', '1px solid ' + colorFnc(%(factor)s * cellQuality));
    if (cellQuality > 0){
      var curTitle = $(nTd).attr("title"); if (curTitle === undefined) {curTitle = ''};
      $(nTd).attr("title", curTitle + 'cell quality: ' + cellQuality)}''']


class TableCellStyleIntensityNumber(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:

  """
  _dflts = {'start': 'white', 'end': 'red', 'factor': 100}

  alias = 'intensity'
  jsCreatedCell = ['''
    if (sData !== null){
      var cellIntensity = getDict(oData, %(table)s[iCol].data + '.intensity', 0);
      $(nTd).css('background', 'linear-gradient(to right, %(end)s, %(start)s '+ (%(factor)s * cellIntensity)  +'%%)'); 
    }''']


class TableCellStyleBoundNumber(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:

  """
  _dflts = {'belowColor': 'blue', 'aboveColor': 'red', 'thresholdMin': 0, 'thresholdMax': 4}

  alias = 'bounds'
  jsCreatedCell = ['''
    if (sData !== null){
      if(sData <= %(thresholdMin)s) {$(nTd).css('background-color', '%(belowColor)s')}
      else if(sData >= %(thresholdMax)s) {$(nTd).css('background-color', '%(aboveColor)s')}
    }''']


# --------------------------------------------------------------------------------------------------------------
#
#                                     FORMAT DEFINITION FOR CELLS IN COLUMN
# --------------------------------------------------------------------------------------------------------------
class TableCellStyleFormat(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Change the content of the cell and add an input HTML object.
    The type parameter will define which input object should be added. It is possible to add a class to change its
    style
  """
  _dflts = {'type': 'text', 'class': ''}

  alias = 'input'
  jsCreatedCell = ['''var tmpVal = $(nTd).text(); $(nTd).html("<input type='%(type)s' class='%(class)s' value='"+ tmpVal +"' />") ''']


class TableCellStyleFormatDiv(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Change the content of the cell in the defined column to a div component
  """
  _dflts = {'dsc': ''}

  alias = 'div'
  jsCreatedCell = ["$(nTd).prop('title', '%(dsc)s')"]


class TableCellStyleClass(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Add a class to an cell with an object
  """
  alias = 'container_class'
  jsCreatedCell = ['''$(nTd).addClass("%(class)s")''']


class TableCellStyleProgress(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:

  """
  alias = 'progress'
  jsRenderFnc = ['''var cellContent =  "<progress value='"+ data +"' max=%(max)s></progress>"''']
  jsRenderReturn = "cellContent"


class TableCellStyleUrl(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:
    Add a hyperlink to the cell in the defined column
  """
  _dflts = {'link': '', 'target': '_blank'}

  alias = 'url'
  jsCreatedCell = ['''var tmpVal = $(nTd).text(); $(nTd).html("<a href='%(link)s"+ tmpVal +"' target='%(target)s'>"+ tmpVal +"</a>") ''']


class TableCellStyleButton(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:

  """
  _dflts = {'class': ''}

  alias = 'button'
  jsCreatedCell = ['''var tmpVal = $(nTd).text(); $(nTd).html("<button class='%(class)s'>"+ tmpVal +"</button>") ''']


class TableCellStyleSignal(TableColsFrg):
  """
  :category: Column Cell Format
  :type: Configuration
  :rubric: JS
  :dsc:

  """
  alias = 'signal'
  jsCreatedCell = ['''
    var tmpVal = $(nTd).text(); var cell = '';
    if(tmpVal >= 1) {cell = "<div style='border:1px solid black;margin:auto;background-color:green;border-radius:20px;width:20px;cursor:pointer' value='"+ tmpVal +"' title='"+ tmpVal +"'>&nbsp;</div>"}
    else if (tmpVal == 0){cell = "<div style='border:1px solid black;margin:auto;background-color:orange;border-radius:20px;width:20px;cursor:pointer' value='"+ tmpVal +"' title='"+ tmpVal +"'>&nbsp;</div>"}
    else{cell = "<div style='border:1px solid black;margin:auto;background-color:red;border-radius:20px;width:20px;cursor:pointer' value='"+ tmpVal +"' title='"+ tmpVal +"'>&nbsp;</div>"}
    $(nTd).html(cell); ''']



if __name__ == "__main__":
  cols = TableCols()
  cols.add([1, 2], 'div', attr={'dsc': "dfgfd"})
  cols.add([1, 2], 'container_class', attr={'class': "dfgfd"})
  cols.add(1, 'age', attr={'steps': 100, 'start': 'white', 'end': 'pink', 'columnOrders': []})
  #cols.add(2, TableRowStyle, attr={'class': "gdfgdf"})
  #cols.add(2, TableRowStyle, attr={'class': "youpi"})
  #cols.add(1, TableRowStyleCss, attr={'css': {'color': 'yellow'}})

  print(cols.toJs())
