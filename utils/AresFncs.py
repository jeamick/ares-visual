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
Section dedicated to the functions. The below functions are system functions and are available in all the reports.
It is possible to extend this by adding report functions specific to your environment. Those functions will be then added to the aresObj automatically.
It will be possible to use them then directly.

In order to get the functions loaded it is important to get the structure in the report:
  /fncs
    _ _init_ _.py
    NewFncs.py

It is possible to add multiple functions in the same module. The functions should have the below structure:


And please add the below documentation type to your functions. They will then be available here for the community !


It is possible to get functions from other environments by using the below line of code:

'''
}


def create(aresObj):
  """
  :category:
  :rubric: PY
  :type: System
  :dsc:
    Load the System utility functions defined in the AReS core framework
  :return: A dictionary with the list of available functions
  """
  fncs = {}
  for script in os.listdir(os.path.dirname(__file__)):
    if (script == "AresFncs.py") or (script == "__init__.py") or not script.endswith(".py"):
      continue

    mod = importlib.import_module('ares.utils.%s' % script.replace(".py", ""))
    functions_list = [o for o in inspect.getmembers(mod) if inspect.isfunction(o[1])]
    for fncName, fnc in functions_list:
      fncs[fncName] = fnc
  if aresObj.run.local_path not in ("", None):
    fncsPath = os.path.join(aresObj.run.local_path, 'fncs')
    if os.path.exists(fncsPath):
      for script in os.listdir(fncsPath):
        if script.endswith('.py') and script != "__init__.py":
          try:
            mod = importlib.import_module('%s.fncs.%s' % (aresObj.run.report_name, script.replace(".py", "")))
            functions_list = [o for o in inspect.getmembers(mod) if inspect.isfunction(o[1])]
            for fncName, fnc in functions_list:
              fncs[fncName] = fnc
          except Exception as err:
            logging.warning("%s, error %s" % (script, err))

  # Add the Hash ID function
  mod = importlib.import_module('ares.utils.AresSiphash')
  fncs["hashId"] = mod.SipHash().hashId
  return fncs


def docEnum(aresObj, outStream, lang='eng'):
  """
  :category: Functions
  :rubric: PY:
  :type: Configuration
  """
  fncsFactory = create(aresObj)
  outStream.append(DSC.get(lang, DSC.get('eng', '')))
  for alias, fnc in fncsFactory.items():
    docDetails = AresMarkDown.AresMarkDown.loads(fnc.__doc__)
    if 'tip' in docDetails:
      outStream.title("%s ares:info<%s>" % (alias, "".join( docDetails['tip'])), level=3)
    else:
      outStream.title(alias, level=2)
    outStream.append(docDetails.getAttr('dsc'))
    outStream.title('Examples', level=4)
    outStream.code(docDetails.getAttr('example'))
    varNames = inspect.getargspec(fnc).args
    if len(varNames) > 0:
      outStream.title('Arguments', level=4)
      for varName in varNames:
        if varName == 'self':
          continue

        outStream.append("%s: %s" % (varName, outStream.params(varName)))

  # Return the list of environments with functions
  outStream.title("Environments with bespoke functions", level=2)
  if hasattr(aresObj, 'reportsPath'):
    header = ['Environment', 'Module', 'Functions']
    data = []
    for path in aresObj.reportsPath.values():
      if os.path.exists(path):
        for folder in os.listdir(path):
          if os.path.exists( os.path.join(path, folder, 'fncs')) :
            for file in os.listdir( os.path.join(path, folder, 'fncs') ):
              if file != '__init__.py' and file.endswith('.py'):
                fncNames = []
                mod = importlib.import_module('%s.fncs.%s' % (folder, file.replace(".py", "")))
                for o in inspect.getmembers(mod):
                  if inspect.isfunction(o[1]):
                    fncNames.append( o[0] )
                data.append([folder, file, ",".join(fncNames)])
    outStream.table(header, data)
    outStream.src(__file__)

