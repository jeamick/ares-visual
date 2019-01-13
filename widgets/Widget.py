#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import os
import inspect
import importlib
import logging

from ares.Lib import AresMarkDown


DSC = {
  'eng': '''
:category: Widget
:rubric: PY
:type: Base class
:dsc:
A widget is a group of AReS components with some extra features. A widget is defined for a given purpose and it will provide some shortcut in the implementation.
Those components when call from an aresObj can require some parameters.
'''}


def requires(moduleName, reason, install):
  """
  :category: AReS System
  :rubric: PY
  :type: system
  :dsc:
    Import the necessary external packages and provide explicit message to find a way to solve this error message.
    This method should also explain why this module is required to make sure this is really expected to get an error.
  """
  try:
    importlib.import_module(moduleName)
  except Exception as err:
    print("*** Module %s required ***" % moduleName)
    print(reason)
    print("Command to fix this error:")
    print(">>> %s" % install)
    raise


class Widget(object):
  """
  :dsc:
    Widget Definition
  """
  name, label = None, ""

  def __init__(self, aresObj):
    self.aresObj = aresObj

  def getSource(self, jsData, jsFnc, cacheObj=None, isPyData=True, isDynUrl=False, htmlCodes=None, datatype='json'):
    return self.aresObj.jsPost("%s/widget/%s/%s" % (self.aresObj.__urlsApp['ares-report'], 'WidgetExample',
             self.__class__.__name__), jsData, jsFnc, cacheObj, isPyData, isDynUrl, htmlCodes, datatype)

  def doc(self):
    raise NotImplementedError("Widget documentation should be defined")

  def html(self, params):
    raise NotImplementedError("Widget content should be defined")

  def _component(self, params):
    return self.html(params)


def docEnum(aresObj, outStream, lang='eng'):
  """
  :category: Datatable
  :rubric: PY:
  :type: Configuration
  """
  widgetPath = os.path.dirname(__file__)
  for file in os.listdir(widgetPath):
    if file.endswith(".py"):
      try:
        for name, obj in inspect.getmembers(importlib.import_module("ares.widgets.%s" % file.replace(".py", "")), inspect.isclass):
          if issubclass(obj, Widget):
            if obj.name is not None:
              docDetails = AresMarkDown.AresMarkDown.loads(obj.__doc__)
              outStream.link("**%s** | %s" % (obj.name, obj.label), "api?module=widget&enum=%s" % obj.name, cssPmts={"margin": "5px"})
      except Exception as err:
        logging.warning("%s, error %s" % (file, err))


