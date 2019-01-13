#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.AresImports import requires


class AresMongo(object):
  """
  :category: Connector
  :rubric: PY
  :type: Class
  :dsc:

  :link Documentation: https://www.w3schools.com/python/python_mongodb_getstarted.asp
  :link Local Server: https://www.mongodb.com/dr/fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-4.0.3-signed.msi/download
  """

  ALIAS = 'MONGODB'
  _extPackages = [("pyMongo", 'pyMongo')]

  def __init__(self, database=None, **kwargs):
    self.pkgs = {}
    if self._extPackages is not None:
      for name, package in self._extPackages:
        self.pkgs[name] = requires(name, reason='Missing Package', install=package, autoImport=True, sourceScript=__file__)
    self.engine = self.pkgs['pyMongo'].MongoClient("mongodb://%s:%s/" % (kwargs.get('host'), kwargs.get('port')))
    if database:
      self.database = self.engine[database]
    else:
      self.database = self.engine['local']


  def __getitem__(self, key):
    """:dsc: Choose a collection in a particular database"""
    return self.database[key]


  @property
  def dbList(self):
    return self.engine.list_database_names()


  def changeDb(self, database):
    """
    :dsc: change the currently selected DB
    """
    if database in ['admin', 'config']:
      raise Exception("You don't have access to those databases")

    self.database = self.engine[database]
