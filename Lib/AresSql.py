#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import inspect

import ares.doc
import ares.utils.AresSiphash
from ares.Lib.AresImports import requires

# Will automatically add the external library to be able to use this module
ares_pandas = requires("pandas", reason='Missing Package', install='pandas', autoImport=True, sourceScript=__file__)
ares_sqlalchemy = requires("sqlalchemy", reason='Missing Package', install='sqlalchemy', autoImport=True, sourceScript=__file__)
# TODO: Use correctly requires with sqlalchemy module

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import importlib
import logging
import sys
import os
import datetime
import traceback

from ares.Lib import AresMarkDown


class SqlConn(object):
  """
  :category: SQL Framework
  :rubric: PY
  :type: class
  :dsc:
    Base Class to create a database and perform SQL operations using the sqlalchemy interface
  :link Documentation: https://www.pythonsheets.com/notes/python-sqlalchemy.html#join-joined-two-tables-via-join-statement
  """
  _extPackages = None

  def __init__(self, dbFamily, database=None, filename=None, modelPath=None, reset=False, migrate=True, **kwargs):
    """
    :category: SQL Framework
    :rubric: PY
    :dsc:
      Here we try to setup as generic as we can all the variable environment variables for the DB.
      We try to not rely on the aresObj in order to be able to use this interface for various usage
    """
    self.pkgs = {}
    if self._extPackages is not None:
      for name, package in self._extPackages:
        self.pkgs[name] = requires(name, reason='Missing Package', install=package, autoImport=True, sourceScript=__file__)
    self.query = None  # In this design we decided to go to a route where each user will manage his database and also the person who can look at the data
    # This will simplify a lot the permissionning (we consider the storage not a problem at this stage as we split per user
    # Also this could be interesting to check the user data use
    # Some reports can get centralised databases using the module variable SINGLEDB
    dbConfig = {'drivername': dbFamily, 'username': kwargs.get('username'), 'password': kwargs.get('password'), 'host': kwargs.get('host'),
                'port': kwargs.get('port'), 'query': kwargs.get('query'), 'database': database}
    self.dbPath = database
    self.username = kwargs.get('username')
    self.userhost = kwargs.get('userhost')
    self.engine = sqlalchemy.create_engine(sqlalchemy.engine.url.URL(**dbConfig))
    self.metadata = sqlalchemy.MetaData(bind=self.engine)
    self.metadata.reflect()
    self.metadata.create_all(self.engine)
    self.session = sessionmaker(bind=self.engine)()
    if modelPath:
      self.loadSchema(filename=filename, modelPath=modelPath, reset=reset, migrate=migrate)
      self.metadata.reflect()


  def _loadSqlFile(self, fileName, reset, migrate):
    """

    :param filePath:
    :return:
    """
    on_init_fnc = None
    modelMod = importlib.import_module(fileName.replace('.py', ''))
    for tableName, table in inspect.getmembers(modelMod):
      if tableName == 'on_init':
        on_init_fnc = table
      elif '__' not in tableName and inspect.isroutine(table):
        tableDef = getattr(modelMod, tableName)()
        tableDef.append(sqlalchemy.Column('lst_mod_dt', sqlalchemy.DateTime, default=datetime.datetime.utcnow(), nullable=True))
        if not self.engine.has_table(tableName):
          newTable = sqlalchemy.Table(tableName, self.metadata, *tableDef)
          newTable.create(self.engine, checkfirst=True)
        else:
          # if migrate:
          #   oldTable = '__old_%s' % tableName
          #   self.cloneTable(tableName, oldTable, force=True)
          #   newTable = sqlalchemy.Table(tableName, self.metadata, *tableDef)
          #   newTable.drop(self.engine, checkfirst=True)
          #   newTable.create(self.engine, checkfirst=True)
          #   self.migrateTable(oldTable, tableName)
          #   sqlalchemy.Table(oldTable, self.metadata).drop(self.engine)
          if reset:
            newTable = sqlalchemy.Table(tableName, self.metadata, *tableDef)
            newTable.drop(self.engine, checkfirst=True)
            newTable.create(self.engine, checkfirst=True)
    #We do the part where we run default that need to happen on database creation
    if on_init_fnc:
      on_init_fnc(self)

  def help(self, category=None, rubric=None, type=None, value=None, enum=None, section=None, function=None, lang='eng', outType=None):
    """
    :category: Python function
    :rubric: PY
    :dsc:
      Display the Python documentation of the requested object.
      This is done by reading all the documentation from the object.
      Documentation is by default displayed in the Python console but it can be also written to a static html page.
      It is possible to zoom in the documentation to get more details
    :example: aresObj.help()
    """
    import collections

    outStream = AresMarkDown.DocCollection(self.aresObj)
    countMissing = collections.defaultdict(int)
    outStream.title("AReS Databases")
    outStream.append('''
The database framework in AReS is fully based on [SqlAlchemy]( https://www.sqlalchemy.org ). This Python module is an abstraction layer on top of a database. It will allow you to create, change and trash tables very easily.
[SqlAlchemy]( https://www.sqlalchemy.org ) is wrapping up any SQL databases (MySql, Oracle, postgre-SQL ...)
    ''')
    for method_name in dir(self):
      if method_name in ['loadSchema', 'loadDataFile']:
        continue

      if function is not None and function != method_name:
        continue

      if not "__" in method_name and callable(getattr(self, method_name)):
        varNames = inspect.getfullargspec(getattr(self, method_name)).args
        outStream.hr()
        outStream.title("Function %s(%s)" % (method_name, ", ".join(varNames)), level=2)
        docStr = AresMarkDown.AresMarkDown.loads(getattr(self, method_name).__doc__)
        outStream.append(docStr.getAttr('dsc'))
        if docStr.getAttr('example') != '':
          outStream.title("Examples", level=4)
          outStream.code(docStr.getAttr('example'))
        outStream.title("Arguments", level=4)
        for varName in varNames:
          if varName == 'self':
            continue

          if varName in ares.doc.DocAresPmts.PARAMETERS:
            outStream.append("%s: %s" % (varName, outStream.params(varName)))
          else:
            countMissing[varName] += 1
    outStream.src(__file__)
    outStream.export(outType)

  def loadSchema(self, filename=None, modelPath=None, reset=False, migrate=True):
    """
    :category: SQL Framework
    :rubric: PY
    :dsc:
      Function that takes care of initialising the DB
      Please note that some column names are prohibited such as lst_mod_dt
    """

    if not filename and not modelPath:
      raise Exception("You need to specify at least a file name or a model path")

    if modelPath:
      sys.path.append(modelPath)
      for pyFile in os.listdir(modelPath):
        if not pyFile.endswith('.py') or pyFile == '__init__.py':
          continue

        if filename and filename != pyFile:
          continue

        self._loadSqlFile(pyFile, reset, migrate)
    elif filename:
      self._loadSqlFile(filename, reset, migrate)

  def cloneTable(self, oldTable, newTable, mapping=None, force=False):
    """
    :dsc: Helps to migrate between two tables. The mapping argument is used in case the column names differ between the two tables
    """

    oldTableSchema = sqlalchemy.Table(oldTable, self.metadata)
    print(self.engine.table_names())
    print(self.metadata.tables)
    newTableSchema = sqlalchemy.Table(newTable, self.metadata)
    print(newTableSchema.name)
    print(newTableSchema.columns)
    print(oldTable)
    print(oldTableSchema.columns)
    if self.engine.has_table(newTable):
      newTableSchema.drop(self.engine, checkfirst=True)
    for column in oldTableSchema.columns:
      column.name = mapping.get(column.name, column.name) if mapping else column.name
      newTableSchema.append_column(column)
    print(newTableSchema.columns)
    newTableSchema.create(self.engine, checkfirst=True)

  def migrateTable(self, fromTable, toTable, mapping=None):
    """
    :dsc: copy data from one table to another
    """
    oldData = list(self.select([fromTable]).getData())
    self.insert(toTable, oldData.to_dict('records'), commit=True)

  def forceCreate(self):
    """
    :category: SQL Framework
    :rubric: PY
    :type: Creation
    :dsc:
      Force the creation of the database in the given project
    :return: The dbOjb
    """
    Base = declarative_base()
    Base.metadata.create_all(self.engine)
    return self

  def loadDataFile(self, fileName, filePath, reset=False, newTables=None):
    """
    :category: SQL Framework
    :rubric: PY
    :example: aresObj.db().loadDataFile("youpi3.py")
    :dsc:
      Load a python sql file to the local database.
      This will only add records and then commit the changes.

      Those data should not be sensitive ones if they are store and committed to the folder.
    """
    sys.path.append(filePath)
    dataMod = importlib.import_module(fileName.replace(".py", ""))
    if hasattr(dataMod, 'data') and hasattr(dataMod, 'target'):
      conn = self.engine.connect()
      header = dataMod.data[0]
      sqlTarget = self.table(dataMod.target)
      if reset:
        conn.execute(sqlTarget.delete())
      if dataMod.target in newTables or newTables is None:
        print("Loading data from %s" % dataMod.target)
        if isinstance(header, list):
          for rec in dataMod.data[1:]:
            conn.execute(sqlTarget.insert().values(dict(zip(header, rec))))
        else:
          for rec in dataMod.data:
            conn.execute(sqlTarget.insert().values(rec))

  def where(self, stmts):
    """
    :category: SQL Framework
    :rubric: PY
    :example:
      db.select().where([db.column("table", 'column') == 'X')
      db.select( ['BNP'] ).where([ db.column('BNP', 'date') == '22/04/2013 00:00'] ).toDf()
    :dsc:
      Add a where clause to the SqlAlchemy query.
    :return: The python object itself
    """
    for stmt in stmts:
      self.query = self.query.where(stmt)
    return self

  def select(self, tableNames):
    """
    :category: SQL Framework
    !rubric: PY
    :example: aresObj.db().select(["worldcup_teams"])
    :dsc:
      Create a SQL statment
    :link sqlalchemy: http://docs.sqlalchemy.org/en/latest/core/selectable.html
    :link sqlalchemy: http://docs.sqlalchemy.org/en/latest/core/sqlelement.html
    :return: self
    """
    tables = [sqlalchemy.Table(table, self.metadata, autoload=True) for table in tableNames]
    self.query = sqlalchemy.sql.select(tables)
    return self

  def delete(self, tableName):
    """
    :category: SQL Framework
    !rubric: PY
    :example: aresObj.db().delete('table1')
    :dsc:
      Create a delete SQL statment
    :link sqlalchemy: http://docs.sqlalchemy.org/en/latest/core/selectable.html
    :link sqlalchemy: http://docs.sqlalchemy.org/en/latest/core/sqlelement.html
    :return: self
    """
    if self.engine.has_table(tableName):
      self.engin
    self.query = sqlalchemy.sql.select(tables)
    return self

  def insert(self, tableName, records, commit=False, colUserName=None):
    """
    :category: SQL Framework
    !rubric: PY
    :example: db.insert('table1',[{'name': 'test'}], commit=True)
    :dsc:
        insert a list of records to a table
    :return: The python object itself
    """
    dflt = {'lst_mod_dt': datetime.datetime.utcnow()}
    errorCount, errorLog = 0, []
    table = sqlalchemy.Table(tableName, self.metadata)
    if not self.engine.has_table(table.name):
      raise Exception("Table does not exist")

    if colUserName is not None:
      dflt[colUserName] = self.username
    if 'hostname' in self.columnsList(tableName):
      dflt['hostname'] = self.userhost
    if isinstance(records, dict):
      records = [records]
    for rec in records:
      try:
        tmpRec = dict(rec)
        tmpRec.update(dflt)
        self.session.execute(table.insert().values(tmpRec))
      except Exception as err:
        logging.warning(traceback.format_exc())
        errorCount += 1
        errorLog.append(traceback.format_exc().split('\n')[-1])
    if commit:
      self.session.commit()
    if errorCount:
      return (False, errorCount, errorLog)

    return (True, 0, [])

  def getData(self, limit=None):
    """
    :category: SQL Framework
    :rubric: PY
    :example: aresObj.db().getData()
    :dsc:
      Returns the results of the select statement previously instantiated in a pandas dataframe

    :return: A pandas dataframe
    """
    if self.query is None:
      return None

    if limit:
      return ares_pandas.read_sql(self.query, self.query.bind).head(limit)

    return ares_pandas.read_sql(self.query, self.query.bind)

  def fetch(self, limit=None):
    """
    :category: SQL Framework
    :rubric: PY
    :example: aresObj.db().fetch()
    :dsc:
       Similar to getData but return an iterator over a list instead of using pandas
    :return: An iterator over the result of the query
    """
    if self.query is None:
      yield None

    counter = 0
    if not limit:
      limit = -1
    for row in self.engine.connect().execute(self.query):
      if limit == -1 or counter < limit:
        counter += 1
        yield row

      else:
        raise StopIteration

  def tablesList(self):
    """
    :category: SQL Framework
    :rubric: PY
    :example: aresObj.db().tablesList()
    :dsc:
        Return the list of tables defined in the selected database
    :return: A python object with the list of tables
    """
    return self.engine.table_names()

  def columnsList(self, tableName):
    """
    :category: SQL Framework
    :rubric: PY
    :example: aresObj.db().columnsList()
    :dsc:
        Return the list of columns defined in the selected database
    :return: A python object with the list of tables
    """

    table = sqlalchemy.Table(tableName, self.metadata)
    if self.engine.has_table(table.name):
      return table.columns

    raise Exception('Table does not exist')

  def table(self, tableName):
    """
    :category: SQL Framework
    :rubric: PY
    :example: db.table('table1')
    :dsc:
      Return a sqlAlchemy table object. This can be useful in the where clauses
    :return: Python table object
    """
    if self.engine.has_table(tableName):
      return sqlalchemy.Table(tableName, self.metadata)

    raise Exception('Table does not exist')

  def column(self, tableName, columnName):
    """
    :category: SQL Framework
    :rubric: PY
    :example: select().where([db.column("table", 'column') == 'X')
    :dsc:
      Return a sqlAlchemy column object. This can be useful in the where clauses
    :return: Python column object
    """
    table = sqlalchemy.Table(tableName, self.metadata, autoload=True)
    if self.engine.has_table(table.name):
      return getattr(table.c, columnName)

  def drop(self, tableName, withCheck=True):
    """
    :category: SQL Framework
    :rubric: PY
    :example:
      aresObj.db().drop('test')
      aresObj.db().drop('test', withCheck=False)
    :dsc:
        Delete the table from the database.
        The pre check can be disabled and the table will be automatically created again when the report will be retriggered.
        No extra function to create a table in the framework this is done by the AReS framework
    """
    if withCheck:
      try:
        name = input("Are you sure to delete the table %s (Y/N)? " % tableName)
      except:
        name = raw_input("Are you sure to delete the table %s (Y/N)? " % tableName)
      if name == 'Y':
        sqlalchemy.Table(tableName, self.metadata, autoload=True).drop()
        logging.info("Table %s deleted" % tableName)
    else:
      sqlalchemy.Table(tableName, self.metadata, autoload=True).drop()
      logging.info("Table %s deleted" % tableName)

  def delete(self, tableName, whereClauses=None, commit=False):
    """
    :category: SQL Framework
    :rubric: PY
    :type:
    :dsc:
      This function will delete records matching the whereClauses from an existing table
    :example: db.delete('test', [db.table('test').id == 1])
    :return: self
    """
    if whereClauses:
      self.engine.execute(self.table(tableName).delete().where(whereClauses))
    else:
      self.engine.execute(self.table(tableName).delete())
    if commit:
      self.commit()
    return self

  def emptyTable(self, tableName):
    """
    :category: SQL Framework
    :rubric: PY
    :type:
    :dsc:
      This function will empty an existing table
    :example: db.emptyTable('test')
    :return: self
    """
    self.delete(tableName)
    logging.info('Content of table %s deleted' % tableName)
    self.commit()
    return self

  def commit(self):
    self.session.commit()

  def createTable(self, records, fileName, tableName, path=None, reset=False, migrate=True, commit=True, isAresDf=True):
    """

    :example:
      df = aresObj.file(htmlCode=r"IBRD_Balance_Sheet__FY2010.csv").read()
      modelFilePath = df.saveTo(fileFamily="model")
      db = aresObj.db(database=r"newTest.db").forceCreate()
      dbObj.createTable(records=df, **modelFilePath)
    """
    self.loadSchema(modelPath=path, filename=fileName, reset=reset, migrate=migrate)
    self.insert(records=records.records(), commit=commit, tableName=tableName)


class AresSqlConn(SqlConn):
  """
  :category: SQL Framework
  :rubric: PY
  :dsc: Simple Wrapper around SqlConn to simplify DB interractions for the AReS Fwk
  """

  ARES_DEP = True

  def __init__(self, aresObj, dbFamily, database=None, modelPath=None, reset=False, **kwargs):
    """
    :category: SQL Framework
    :rubric: PY
    :dsc: Allocates the aresObj to access the user_reports folders
    """
    self.aresObj = aresObj
    if not modelPath and self.aresObj.run.host_name != 'Script':
      modelPath = os.path.join(self.aresObj.run.local_path, 'model', 'tables')
      if not os.path.exists(modelPath):
        modelPath = None
    super(AresSqlConn, self).__init__(dbFamily, database=database, modelPath=modelPath, reset=reset, **kwargs)

  def loadDataFile(self, fileName, filePath=None, reset=False, newTables=None):
    """
    :category: SQL Framework
    :rubric: PY
    :example: aresObj.db().loadDataFile("youpi3.py")
    :dsc:
      Load a python sql file to the local database.
      This will only add records and then commit the changes.

      Those data should not be sensitive ones if they are store and committed to the folder.
    """
    if not filePath:
      filePath = self.aresObj.run.report_name
    super(AresSqlConn, self).loadDataFile(fileName, filePath=filePath, reset=reset, newTables=newTables)




