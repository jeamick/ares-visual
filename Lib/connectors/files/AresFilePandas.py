#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import time
import os
import json

from ares.Lib.connectors.files import AresFile
from ares.Lib.js import AresJsEncoder
from ares.Lib.AresImports import requires

# Will automatically add the external library to be able to use this module
ares_pandas = requires("pandas", reason='Missing Package', install='pandas', autoImport=True, sourceScript=__file__)


class AresFileSeries(ares_pandas.Series):

  @property
  def _constructor(self):
    return AresFileSeries

  @property
  def _constructor_expanddim(self):
    return AresFileDataFrame

  _metadata = ['filePath', 'aresObj', 'selectCols', '_ares_data', '_filters', 'htmlId', 'jsColsUsed']

  # @classmethod
  # def _internal_ctor(cls, *args, **kwargs):
  #   kwargs['htmlCode'] = None
  #   return cls(*args, **kwargs)


class AresFileDataFrame(ares_pandas.DataFrame):
  """

  """
  __fileExt = ['.csv', '.txt']
  _metadata = ['filePath', 'aresObj']
  label = "Pandas Dataframe Interface"

  # https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html
  dataTypeMap = {'object': {'python': 'str'}, 'int64': {'python': 'int'}, 'float64': {'python': 'float'}}

  @property
  def _constructor(self):
    return AresFileDataFrame

  @property
  def _constructor_sliced(self):
    return AresFileSeries

  # @classmethod
  # def _internal_ctor(cls, *args, **kwargs):
  #   print(kwargs)
  #   kwargs['htmlCode'] = None
  #   return cls(*args, **kwargs)

  # Remove the error message by declaring the columns as metadata
  _metadata = ['filePath', 'aresObj', 'selectCols', '_ares_data', '_filters', 'htmlId', 'jsColsUsed']

  def __init__(self, data=None, filePath=None, aresObj=None, htmlCode=None, index=None, columns=None, dtype=None, copy=True):
    super(AresFileDataFrame, self).__init__(data=data, index=index, columns=columns, dtype=dtype, copy=copy)
    self.filePath, self.aresObj, self.selectCols, self._ares_data, self.htmlCode = filePath, aresObj, [], [], htmlCode.replace("/", "_") if htmlCode is not None else htmlCode
    self._filters, self.htmlId, self.jsColsUsed = {}, 'recordset_%s' % id(self) if self.htmlCode is None else self.htmlCode.replace("/", "_"), set()
    self.filePathNoExt, self.fileExtension = os.path.splitext(filePath) if filePath is not None else (None, None)
    self.path, self.filename = os.path.split(filePath) if filePath is not None else (None, None)

  @property
  def exists(self):
    return os.path.exists(self.filePath)

  @property
  def timestamp(self):
    if self.exists:
      return time.strftime("%Y%m%d_%H%M%S", time.gmtime())

  def read(self, **kwargs):
    """
    :example: df = aresObj.file(filename='BNPPARIBASBRA_2018-04-22.txt', path=r'.\ares\doc\data').read(usecols=['date', 'ouv', 'haut'], sep='\t')
    """
    if self.filePath is not None:
      htmlCode = kwargs.get('htmlCode', self.htmlCode)
      if 'htmlCode' in kwargs:
        del kwargs['htmlCode']

      self._ares_data = AresFileDataFrame(data=ares_pandas.read_csv(self.filePath, sep=kwargs["delimiter"] if kwargs.get("delimiter") is not None else '\t', **kwargs), filePath=self.filePath, aresObj=self.aresObj, htmlCode=htmlCode)
      # TODO: Remove this when we will migrate to a list of lists instread of dictionary
      cols = dict([(col, col.replace("[", "").replace("]", "").replace("(", "").replace(")", "")) for col in self._ares_data.headers])
      self._ares_data.rename(cols, axis='columns', inplace=True)
    return self._ares_data

  def save(self, **kwargs):
    """

    """
    if 'htmlCode' in kwargs and self.aresObj is not None:
      self.filename = kwargs['htmlCode']
      self.htmlCode = kwargs['htmlCode'].replace("/", "_")
      self.path = self.aresObj.run.local_path

    if self.path is None:
      raise Exception("save error. Path not defined, plase add an html code in this function")

    if not os.path.exists(self.path):
      os.makedirs(self.path)
    self.to_csv(os.path.join(self.path, self.filename), index=kwargs.get("index", False), sep=kwargs["delimiter"] if kwargs.get("delimiter") is not None else '\t', encoding=kwargs.get("encoding", 'utf8'))

  def saveTo(self, fileFamily, filePath=None, dbName=None):
    """

    """
    facts = AresFile.loadFactory()
    if fileFamily.lower() in facts:
      if filePath is None:
        filePath = self.filePath.replace( self.fileExtension, fileFamily)
      newFile = facts[fileFamily](filePath)
      newFile.write(self, isAresDf=True)
      path, fileName = os.path.split(filePath)
      return {'fileName': fileName, 'path': path}

    elif fileFamily.lower() == 'model':
      if filePath is None:
        filePath = self.filePath.replace( self.fileExtension, ".py")
      dbName = self.filename.split('.')[0] if dbName is None else dbName
      dbTableFile = ["import sqlalchemy", "def table(meta):"]
      dbMapType = {"object": 'Text', 'int64': 'Integer', 'float64': 'REAL'}
      dbTableFile.append("  return sqlalchemy.Table('%s', meta, " % dbName)
      for i, h in enumerate(list(self.dtypes)):
        dbTableFile.append("    sqlalchemy.Column('%s', sqlalchemy.%s, nullable=False)," % (self.dtypes.index[i], dbMapType[str(h)]) )
      dbTableFile.append("    )")
      outFile = open(filePath, "w")
      outFile.write( "\n".join(dbTableFile) )
      outFile.close()
      path, fileName = os.path.split(filePath)
      return {'fileName': fileName, 'path': path, 'tableName': dbName}

  @property
  def headers(self): return list(self.dtypes.index)

  @property
  def types(self):
    return [['Column Name', 'Type']] + [[self.dtypes.index[i], self.dataTypeMap[str(d)]['python']] for i, d in enumerate(list(self.dtypes))]

  @property
  def details(self):
    return [['Attribute', 'Value'], ['Columns count', self.shape[1]], ['Rows count', self.shape[0]], ["Timestamp", self.timestamp]]

  @property
  def count(self): return self.shape[0]
  def max(self, column): return self.loc[self[column].idxmax()][column]
  def min(self, column): return self.loc[self[column].idxmin()][column]

  def dict(self, index, value):
    """
    :category: Dataframe
    :rubric: PY
    :type: Pandas
    :example: aresDf.dict("col1", "col2")
    :dsc:
      Create a dictionary from two Pandas Dataframe columns
    :link Pandas documentation: https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.DataFrame.to_dict.html
    :return: Python dictionary
    """
    return ares_pandas.Series(self[value].values, index=self[index]).to_dict()

  def forEach(self, fnc, inplace=True, **kwds):
    """
    :category: Dataframe
    :rubric: PY
    :type: Transformation
    :dsc:
      Functional way to transform each records in a dataframe.
      The function should return a new dictionary which will be added to the new underlying records object.
    :return: The AReS Dataframe
    :example: dfObj.forEach(lambda rec: {'a': rec['a'] + 4, "b": "aa%s" % rec['b'] }, inplace=False )
    """
    tmpDf = AresFileDataFrame( [ fnc(rec, **kwds) for rec in self.to_dict(orient='records') ] )
    if inplace:
      self = tmpDf
      return self

    return tmpDf

  def to_numeric(self, colNames):
    if self.empty:
      return self

    if isinstance(colNames, list):
      for colName in colNames:
        self[colName] = self[colName].apply(ares_pandas.to_numeric)
    else:
      self[colNames] = self[colNames].apply(ares_pandas.to_numeric)
    return self

  def addColMap(self, dstColName, srcColName, mapDict, intKey=None, dflt='', replace=True):
    """
    :category: Python - Pandas  wrapper
    :example: dfObj.addColMap('test', 'col1', {"col1": 1, "b": 2}, intKey="b" )
    :dsc:
      Add a column from a python dictionnary.
    :return: The AReS Dataframe itself
    :link Pandas documentation: https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.DataFrame.apply.html
    """
    if intKey is None:
      self.addCol(dstColName, lambda row: mapDict.get(row[srcColName], dflt))
    else:
      self.addCol(dstColName, lambda row: mapDict.get(row[srcColName], {}).get(intKey, dflt))
    if replace:
      self.dropCol([srcColName])
    return self

  def top(self, n, colName, ascending=False):
    """
    :category: Python - Pandas  wrapper
    :example: aresDf.top(10, "col1")
    :dsc:
      Return a new AReS dataframe with only the Nth top values in the selected column
    :link Pandas documentation: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html
    :return: A reduced AReS Dataframe
    """
    return self.sort_values(colName, ascending=ascending).head(n)

  def addCol(self, colName, fnc, isJsUsed=True, axis=1):
    """
    :category: Dataframe
    :example: dfObj.addCol('test', lambda x: x['col1'] + 2)
    :dsc:
      Add a column to the existing Dataframe according to a special function.
    :return: The AReS Dataframe itself
    :link Pandas documentation: https://pandas.pydata.org/pandas-docs/version/0.22/generated/pandas.DataFrame.apply.html
    """
    self[colName] = self.apply(fnc, axis=axis)
    if isJsUsed:
      self.jsColsUsed.add(isJsUsed)
    return self

  def reduce(self, colNames, inplace=True):
    """

    :return: Return the or a new AReS Dataframe
    """
    for colName in colNames:
      self.jsColsUsed.add(colName)
    colsToDrop = []
    for col in self.headers:
      if not col in colNames:
        colsToDrop.append(col)
    if inplace:
      self.drop(colsToDrop, axis=1, inplace=inplace)
      return self
    else:
      return AresFileDataFrame(self.drop(colsToDrop, axis=1, inplace=inplace))

  def lookupCol(self, left_on, df2, cols, renameCols, right_on=None, aggFnc=None):
    """

    :return: Return the AReS Dataframe
    """
    if right_on is None:
      right_on = left_on
    tempDf = df2.df[[right_on] + cols]
    tempDf.rename(renameCols, axis=1, inplace=True)
    newDf = ares_pandas.merge(self, tempDf, how='left', left_on=left_on, right_on=right_on).fillna(0)
    if aggFnc is not None:
      headers = self.headers
      for col in renameCols.values():
        if "%s_x" % col in headers and "%s_y" % col in headers:
          if aggFnc == 'sum':
            newDf.addCol(col, lambda x: x['%s_x' % col] + x['%s_y' % col])
          elif aggFnc == 'avg':
            newDf.addCol(col, lambda x: (x['%s_x' % col] + x['%s_y' % col]) / 2)
          newDf.dropCol( ['%s_x' % col, '%s_y' % col])
    return newDf

  def dropCol(self, colNames, inplace=True):
    """
    :category: Dataframe
    :rubric: PY
    :type: Pandas
    :example:
    :dsc:

    :return:
    """
    dfHeader = self.headers
    if isinstance(colNames, list):
      if inplace:
        for colName in colNames:
          if colName in dfHeader: # Need to check as the export will create a first column
            if colName in self.jsColsUsed:
              self.jsColsUsed.remove(colNames)
            self.drop(colName, axis=1, inplace=inplace)
        return self
      else:
        firstCol = True
        for colName in colNames:
          if colName in dfHeader:
            # Need to check as the export will create a first column
            if firstCol:
              newDf = self.drop(colName, axis=1, inplace=False)
            else:
              newDf.drop(colName, axis=1, inplace=True)
        return self.aresObj.df(newDf)
    else:
      if colNames in dfHeader:
        # Need to check as the export will create a first column
        if colNames in self.jsColsUsed and inplace:
          self.jsColsUsed.remove(colNames)
        result = self.drop(colNames, axis=1, inplace=inplace)
        return result if inplace else self.aresObj.df(result)
    return self

  def sort(self, colsIdx, ascending=True, axis=0, inplace=True):
    """
    :category: Python - Pandas  wrapper
    :example: aresDf.sort("col1")
    :dsc:
      Function to sort the content of a dataframe according to a defined column
    :link Pandas documentation: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.sort_values.html
    :return: A reduced AReS Dataframe
    """
    self.sort_values(colsIdx, ascending=ascending, axis=axis, inplace=inplace)
    return self

  def tolist(self, colName, dropDuplicates=False, withAll=False):
    """
    :category: Dataframe
    :rubric: PY
    :type: Transformation
    :dsc:
      Get from a dataframe a single series based on its column name
    :example: data.tolist("b", duplicate=False) # This will remove the duplicated entries
    :return: Return a Python list with or without duplicated entries
    """
    if dropDuplicates:
      if withAll:
        return [''] + self[colName].drop_duplicates().tolist()

      return self[colName].drop_duplicates().tolist()

    if withAll:
      return [''] + self[colName].tolist()

    return self[colName].tolist()

  def attach(self, htmlObj):
    """
    :category: Dataframe
    :rubric: JS
    :type: Front End
    :dsc:
      Attach the Dataframe to a HTML Object. This function is normally used in the different components in order
      to guarantee the link of the data. This will also ensure that the same data set will be store only once in the page
    """
    self.aresObj.jsSources[self.htmlCode]['containers'].append(htmlObj)

  def records(self, selectCols=None, dropna=None):
    """
    :category: Dataframe
    :rubric: PY
    :type: Transformation
    :dsc:
      Return a clean list of dictionaries. If the selectCols is set to false there will be not
      clean up based on the selected column in the report. All the columns will remain in the report.
    :return:
    """
    selectCols = self.selectCols if selectCols is None else selectCols
    dropna = self.dropna if dropna is None else dropna
    if selectCols:
      self.reduce(self.jsColsUsed)
    if dropna:
      return [{k: v for k, v in m.items() if ares_pandas.notnull(v)} for m in self.to_dict(orient='rows')]

    return self.to_dict(orient='records')

  def toList(self):
    """
    :category: Dataframe
    :rubric: PY
    :type: Transformation
    :dsc:

    :return: A list of lists with the data
    """
    if len(self.selectCols) == 0:
      self.selectCols = self.columns.tolist()
    return [self.selectCols] + self[self.selectCols].values.tolist()

  def html(self):
    # for filterId, filterDefinition in self._filters.items():
    #   jsFilters = []
    #   for rule in filterDefinition['filters']:
    #     jsFilters.append("if (!( %s )) { validLine = false ;} ;" % rule)
    #   self.aresObj.jsGlobal.fnc('%s(data)' % filterId, '''
    #     filteredData = [];
    #     data.forEach( function (rec) {
    #       var validLine = true ; %s ;
    #       if (validLine) { filteredData.push( rec ); }
    #     }); return filteredData ; ''' % ";".join(jsFilters))
    #
    #   for container in self.aresObj.jsSources[self.htmlCode]['containers']:
    #     if container.category == 'Charts':
    #       dataComp = "DictToChart(%s(%s), %s, %s)" % (filterId, self.htmlCode, json.dumps(container.data.xAxis), json.dumps(container.data.seriesNames))
    #     else:
    #       dataComp = "%s(%s)" % (filterId, self.htmlCode)
    #     if getattr(container.data, 'dataFncs', None) is not None:
    #       for fnc in container.data.dataFncs:
    #         self.aresObj.jsGlobal.fnc("%s(data)" % fnc, DataFncChart.DATA_TRANS[fnc])
    #         dataComp = "%s(%s)" % (fnc, dataComp)
    #     for src in filterDefinition['src']:
    #       src['obj'].jsFrg(src['event'], container.jsGenerate(dataComp))
    self.aresObj.jsGlobal.add(self.htmlCode, json.dumps(self.records(), cls=AresJsEncoder.AresEncoder))
    return ''

  def tableHeader(self, forceHeader=None, headerOptions=None):
    if forceHeader is not None:
      for header in forceHeader:
        if 'format' not in header and 'className' not in header:
          header['className'] = 'py_cssdivtextleft'
        # The table does not work well when both are defined
        if 'className' in header and 'class' in header:
          header['className'] = "%s %s" % (header['className'], header['class'])
          del header['class']
      return forceHeader
    #
    colTypes = {}
    # if self.dtypes is not None:
    #   print self.dtypes
    #   if not self.empty and self.dtypes == 'tuple':
    #     for hdr in self.headers:
    #       colTypes[hdr] = {'type': 'tuple'}
    #   elif not self.empty and self.dtypes == 'cell':
    #     for hdr in self.headers:
    #       colTypes[hdr] = {'type': 'cell'}
    #   else:
    #     colTypes = self.dtypes
    if headerOptions is None:
      headerOptions = {}
    # headerMap will order and reduce the perimeter of columns
    headerMap = {'orderCols': []}

    for i, val in enumerate(self.dtypes):
      colName = self.dtypes.index[i]
      if val == 'float64':
        row = {'data': colName, 'title': colName, 'format': 'float', "searchable": True}
      elif val == 'bool':
        row = {'data': colName, 'title': colName, 'display': 'checkbox', "searchable": True}
      elif val == 'int64':
        row = {'data': colName, 'title': colName, 'format': 'float', 'digits': 0, "searchable": True}
      else:
        row = {'data': colName, 'title': colName, 'className': 'py_cssdivtextleft', "searchable": True}
        row.update(colTypes.get(colName, {}))
      row.update(headerOptions.get(colName, {}))
      headerMap[colName] = row
      headerMap['orderCols'].append(colName) # This is to keep the header in the file

    headers = []
    for colName in headerOptions.get('fixedColumns', headerMap['orderCols'] ):
      row = headerMap.get(colName)
      if row is not None:
        # The table does not work well when both are defined
        if 'className' in row and 'class' in row:
          row['className'] = "%s %s" % (row['className'], row['class'])
          del row['class']

        if 'factor' in row:
          row['title'] = "%s (%s)" % (row.get('title', colName), row['factor'])
        headers.append( row )
    return headers

  @property
  def jsData(self): return self.htmlId

if __name__ == '__main__':
  df = AresFileDataFrame(data=[["feef", "bfb"], ["vfv", "bfffsb"]], columns=['A', "V"], filePath=r'D:\BitBucket\Youpi-Ares\user_scripts\outputs\coucou\test.csv')
  df.save()