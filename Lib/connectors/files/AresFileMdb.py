#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.connectors.files import AresFile


class FileMdb(AresFile.AresFile):
  """
  :category: Ares File
  :rubric: PY
  :type: Class
  :dsc:

  :link Documentation: https://en.wikipedia.org/wiki/MDB
  """
  __fileExt = ['.mdb']
  label = "Interface to deal with Access MDB files"
  _extPackages = [("pyodbc", 'pyodbc')]

  def __init__(self, data, filePath, aresObj=None):
    super(FileMdb, self).__init__(data, filePath, aresObj)
    self.__conn = None

  def toUrl(self, params):
    for opt in ['uid', 'password']:
      if not opt in params:
        params[opt] = ''
    return "DRIVER=Microsoft Access Driver (*.mdb);DBQ=%(path)s;Uid=%(uid)s;PWD=%(password)s" % params

  def _read(self, **kwargs):
    raise Exception('Read function not implemented for MDB, please use select function instead !')

  def cursor(self, params=None):
    """
    :category: MDB D
    :rubric:
    :type:
    :dsc:

    :return: A generator with the rows
    """
    if params is None:
      params = {}
    if self.__conn is None:
      params['path'] = self.filePath
      self.__conn = self.pkgs["pyodbc"].connect( self.toUrl(params) )
    return self.__conn.cursor()

  def tables(self):
    """
    :category: MDB D
    :rubric:
    :type:
    :dsc:

    :return: A generator with the rows
    """
    cursor = self.cursor()
    return [table.table_name for table in cursor.tables() if table[3] == 'TABLE' ]

  def select(self, tableName):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    :return: A generator with the rows
    """
    cursor = self.cursor()
    cursor.execute("SELECT * FROM %s" % tableName)
    for row in cursor.fetchall():
      yield row

  def addTable(self, tableName, df=None):
    """
    :category: MDB Database
    :rubric: PY
    :type: Table
    :example: mdbObj.dropTable('myTable')
    :dsc:
      Add a new table to the MDB database
    """
    if not tableName in self.tables():
      cursor = self.cursor()
      string = "CREATE TABLE %s(symbol varchar(15), leverage double, shares integer, price double)" % tableName
      cursor.execute(string)
      self.__conn.commit()

  def dropTable(self, tableName):
    """
    :category: MDB Database
    :rubric: PY
    :type: Table
    :example: mdbObj.dropTable('myTable')
    :dsc:
      Remove a table from the MDB database
    """
    if tableName in self.tables():
      self.cursor().execute("DROP TABLE %s" % tableName)
      self.__conn.commit()


if __name__ == '__main__':
  mdb = FileMdb(r'D:\BitBucket\Youpi-Ares\user_scripts\Books.mdb')
  mdb.dropTable('youpi')
  mdb.addTable('youpi', None)

