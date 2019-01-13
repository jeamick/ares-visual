#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.AresImports import requires


class AresCassandra(object):
  """
  :category: Connector
  :rubric: PY
  :type: Class
  :dsc:

  :link Documentation: https://www.w3schools.com/python/python_mongodb_getstarted.asp
  :link Local Server: https://www.mongodb.com/dr/fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-4.0.3-signed.msi/download
  """

  dbFamily = 'cassandra'
  _extPackages = [("cassandra.cluster", 'cassandra-driver')]

  def __init__(self, aresObj, dbFamily, database=None, **kwargs):
    self.pkgs = {}
    if self._extPackages is not None:
      for name, package in self._extPackages:
        self.pkgs[name] = requires(name, reason='Missing Package', install=package, autoImport=True, sourceScript=__file__)

  @property
  def dbList(self):
    pass


if __name__ == '__main__':
  cassandraDb = AresCassandra(None, dbFamily="cassandra", database="testMongo", host="127.0.0.1", port="27017")
  print(cassandraDb.dbList)
