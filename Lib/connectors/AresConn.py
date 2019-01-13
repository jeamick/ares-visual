#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import importlib
import inspect
import logging
import os
import sys
import traceback

from ares.Lib import AresMarkDown
import ares.Lib.AresSql


DSC = {
  'eng': '''
  :dsc:
AReS connectors are external modules used in within the framework to transform the data. Those connectors can be direct libraries imported with specific features or just a bridge to a full system.
Connectors are designed in a common and standardised way to be able to produce KPI use but also to propose a rich and interactor documentation.
__
AReS Framework is based mainly on [REST API](https://fr.wikipedia.org/wiki/Representational_state_transfer) for everything which cannot directly interact with Python.
For example a C or C++ module can be used directly from Python (if compiled accordinly).
__
For all the other systems, no need to revamp them (at least today), you can simply use REST service to get your data transformed and interact with AReS components.
This is simple to set up and does not require a full revamping to your IT architecture. The first benefit will be to bring a better documentation to users.
Thus users will be able to enrich the documentation and also start asking questions to both the data and the API.
__
All this metadata will benefit the framework and the whole community.
'''}


class AresConn(object):

  # Parameters to know if credentials are expected for this and also if some environments required specific settings
  ENV = None
  SECURED = True

  def __init__(self, aresObj=None):
    """
    :category: Connector
    :type: Constructor
    :dsc:
      Optional aresObj parameter in the object creation. This is mandatory only in the documentation as each doc string will be converted to markdown.
      Those Markdown can then be converted back to AReS object for the web display
    """
    self.aresObj = aresObj

  @classmethod
  def getData(cls, params, **kwargs):
    try:
      res = cls._getData(params, **kwargs)
      return (True, res)

    except Exception as e:
      print(e)
      logging.debug("%s | %s" % (cls.__name__, e), exc_info=True)
      return (False, "%s %s" % (cls.__name__, traceback.format_exc().strip().split('\n')[-1]) )

  @classmethod
  def getSource(cls, sourceCode, run_details):
    return cls.getSources()[sourceCode][1]

  @classmethod
  def getSources(cls):
    try:
      return cls.__sourceFnc
    except AttributeError:
      cls.resetSourceFnc()
      return cls.__sourceFnc

  @classmethod
  def resetSourceFnc(cls):
    sourceFnc = {}
    for conn_path in ['soaps', 'rests', 'models', 'files', 'dbs', 'sources']:
      for file in os.listdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), conn_path)):
        if file.endswith('.py') and file != '__init__.py':
          try:
            mod = importlib.import_module('ares.Lib.connectors.%s.%s' % (conn_path, file.replace('.py', '')))
          except Exception as e:
            logging.exception("%s | %s, %s" % (cls.__name__, conn_path, file))
            continue

          cls.addConnMod(mod, sourceFnc)
    for conn_path in os.environ.get('SPECIFIC_CONNECTOR_PATHS', '').split(';'):
      if not conn_path:
        continue

      if conn_path not in sys.path:
        sys.path.append(conn_path)
      for file in os.listdir(conn_path):
        if file.endswith('.py') and file != '__init__.py':
          try:
            mod = importlib.import_module(file.replace('.py', ''))
          except Exception as e:
            logging.exception("error for %s, %s, %s" % (cls.__name__, e, conn_path, file))
            continue
          cls.addConnMod(mod, sourceFnc)

    cls.__sourceFnc = sourceFnc


  @classmethod
  def addDynamicConn(cls, connCls):
    """
    :category: Connectors
    :rubric: PY
    :type: Framework Extension
    :dsc:
      Add a connector class dynamically
    """
    alias = getattr(connCls, 'ALIAS')
    if not alias:
      raise Exception('ALIAS needs to be defined as an attribute of the class %s' % connCls.__name__)

    if alias in cls.getSources():
      raise Exception('Alias %s already part of the aresObj' % alias)

    newCon = type(connCls.__name__, (connCls, cls), {})
    cls.__sourceFnc[alias] = (getattr(newCon, 'SHOW_IN_SETTINGS', False), newCon)


  @classmethod
  def addConnMod(cls, mod, sourceFnc):
    for member in inspect.getmembers(mod):
      if hasattr(member[1], 'ALIAS'):
        sourceFnc[getattr(member[1], 'ALIAS')] = (getattr(member[1], 'SHOW_IN_SETTINGS', True), member[1])
        # instantiates the db associated with each connector if any
        # cls.attachSqlConn(getattr(member[1], 'ALIAS'), member[1])

      if hasattr(member[1], '_ARES_TYPE'):
        # Add the SQLite and Excel generic connectors
        sourceFnc[getattr(member[1], '_ARES_TYPE')] = (getattr(member[1], 'SHOW_IN_SETTINGS', True), member[1])


  @classmethod
  def attachSqlConn(cls, alias, source):
    """
    :dsc:
      For every connector defined in the framework we attach a sql connection that will allow them to store information
    """
    dbPath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
    if os.path.isfile(os.path.join(dbPath, 'models', '%sDbModels.py' % alias.title())):
      sqlConn = ares.Lib.AresSql.SqlConn('sqlite', os.path.join(dbPath, 'db', '%s.db' % alias), filename='%sDbModels.py' % alias.title(), modelPath=os.path.join(dbPath, 'models'))
    else:
      sqlConn = ares.Lib.AresSql.SqlConn('sqlite', os.path.join(dbPath, 'db', '%s.db' % alias))
    setattr(source, 'sqlConn', sqlConn)


  @classmethod
  def isCompatible(cls, params):
    return (True, 'No Check configured')
