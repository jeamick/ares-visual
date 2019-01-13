#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json

from ares.Lib.AresImports import requires


class AresAccess(object):
  """
  :category: Connector
  :rubric: PY
  :type: Class
  :dsc:
    Connector to Access databases. This connector will allow you to create, store and retrieve data from any MS Access Database.
    This will return the AReS database object. It will be possible to reuse the same syntaxe to then interact with it.

    This would need the ODBC driver available here: https://www.microsoft.com/en-us/download/confirmation.aspx?id=13255
  """
  dbFamily = 'access'
  _extPackages = [("pyodbc", 'pyodbc')]

  def __init__(self, dbFamily, database=None, **kwargs):
    self.pkgs = {}
    if self._extPackages is not None:
      for name, package in self._extPackages:
        self.pkgs[name] = requires(name, reason='Missing Package', install=package, autoImport=True, sourceScript=__file__)
    self.query = {}
    dbAttr = {'Driver': "{Microsoft Access Driver (*.mdb, *.accdb)}", 'DBQ': database}
    for opt in [('password', 'PWD'), ('username', 'UID')]:
      if kwargs.get(opt[0]) is not None:
        dbAttr[opt[1]] = kwargs[opt[0]]
    dbStr = []
    for k in ['Driver', 'DBQ', 'PWD', 'UID']:
      if k in dbAttr:
        dbStr.append("%s=%s" % (k, dbAttr[k]))
    self.conn = self.pkgs['pyodbc'].connect(";".join(dbStr))

  def select(self, tableNames):
    self.query = {'tables': tableNames}
    return self

  def getCol(self, tableName, columnName):
    if 'columns' not in self.query:
      self.query['columns'] = []
    self.query['columns'].append(self.column(tableName, columnName))
    return self

  def where(self, stmts):
    self.query['wheres'] = []
    for stmt in stmts:
      self.query['wheres'].append(stmt)
    return self

  def column(self, tableName, columnName):
    return "%s.%s" % (tableName, columnName)

  def getSql(self):
    strSql = "SELECT %s FROM %s" % (", ".join(self.query.get('columns', ['*'])), ", ".join(self.query['tables']))
    if len(self.query.get('wheres', [])) > 0:
      strSql = "%s WHERE %s" % (strSql, " and ".join(self.query['tables']))
    return strSql

  def insert(self, tableName, records, commit=False, colUserName=None):
    for rec in records:
      row = "(%s" % json.dumps(rec[0]).replace('"', "'")
      for r in rec[1:]:
        row = "%s,%s" % (row, json.dumps(r).replace('"', "'"))
      row = "%s)" % row
      cursor = self.conn.execute('insert into %s values%s' % (tableName, row))
      if commit:
        cursor.commit()

  def getData(self, limit=None):
    cursor = self.conn.cursor()
    records = []
    for rec in cursor.execute(self.getSql()):
      records.append(rec)
    return records