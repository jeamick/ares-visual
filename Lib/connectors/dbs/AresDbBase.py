#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import logging
import os
import inspect
import importlib

from ares.Lib import AresSql


DSC = {
  'eng': '''
  
'''
}


def loadFactory():
  """

  """
  tmp = {}
  for script in os.listdir(os.path.dirname(__file__)):
    try:
      if script.startswith("AresDb") and script.endswith('py') and script != "AresDbBase.py":
        for name, obj in inspect.getmembers(importlib.import_module("ares.Lib.connectors.dbs.%s" % script.replace(".py", "")), inspect.isclass):
          tmp[obj.dbFamily] = obj
    except Exception as err:
      logging.warning( "%s, error %s" % (script, err) )
  return tmp


class ConnDb(object):
  """

  """
  DB_FACTORIES = None
  def __init__(self, database=None, dbName=None, aresObj=None):
    self.aresObj, self.database, self.dbName = aresObj, database, dbName

  def get(self, dbFamily=None, **kwargs):
    if self.DB_FACTORIES is None:
      self.DB_FACTORIES = loadFactory()

    if len(self.DB_FACTORIES) > 0:
      if dbFamily.lower() in self.DB_FACTORIES:
        if getattr(self.DB_FACTORIES[dbFamily], 'ARES_DEP', False):
          if not kwargs.get('modelPath') and kwargs.get('loadModel'):
            kwargs['modelPath'] = os.path.join(self.aresObj.run.local_path, 'model', 'tables')
          return self.DB_FACTORIES[dbFamily](self.aresObj, dbFamily, database=self.database, **kwargs)

        return self.DB_FACTORIES[dbFamily](dbFamily, database=self.database, **kwargs)
    if not self.aresObj:
      return AresSql.SqlConn(dbFamily, database=self.database, **kwargs)

  @classmethod
  def addDynamicDatabase(cls, databaseCls):
    """
    :category: Database Connection
    :rubric: PY
    :type: Framework Extension
    :param sqlFamily: alias of the sqlFamily with which this database will be cable (i.e if the alias is 'newDb' -> aresObj.db('newDb') )
    :dsc:
      Add an external database connection setup by the user
    """

    if cls.DB_FACTORIES is None:
      cls.DB_FACTORIES = loadFactory()

    dbFamily = getattr(databaseCls, 'dbFamily')
    if not dbFamily:
      raise Exception('dbFamily attribute has to be defined in your class %s' % databaseCls.__name__)

    if dbFamily in cls.DB_FACTORIES:
      raise Exception('This sqlFamily %s is already defined in the framework' % dbFamily)

    cls.DB_FACTORIES[dbFamily] = type(databaseCls.__name__, (databaseCls, AresSql.AresSqlConn), {})






def docEnum(aresObj, outStream, lang='eng'):
  """

  :return:
  """

  for ext, aresClass in loadFactory().items():
    outStream.link(
      " **%s** | %s" % (ext, aresClass.label.strip()), "api?module=file&alias=%s" % ext, cssPmts={"margin": "5px"})
