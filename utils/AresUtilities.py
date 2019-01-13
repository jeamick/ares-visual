#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import datetime
import traceback
import sys
import importlib
import types
import re

regex = re.compile('[^a-zA-Z0-9_]')


def cleanData(value):
  """ Function to clean the javascript data to allow the use of variables """
  return regex.sub('', value.strip())


def getDateFromAlias(aliaDt, fromDt=None):
  """
  :category: Python Utilities - Date function
  :example: getDateFromAlias("T")
  :icon: fab fa-python
  :dsc:
    Return the date corresponding to an alias code like T, T-N, M...
  :return: The converted date or a list of dates
  """
  if fromDt is None:
    cobDate = datetime.datetime.today()
  else:
    cobDate = datetime.datetime( *map( lambda x: int(x), fromDt.split("-") ) )
  if len(aliaDt) > 1:
    fType, fCount = aliaDt[0], "".join(aliaDt[2:])
  else:
    fType, fCount = aliaDt, 0
  if fType == 'T':
    for i in range(0, int(fCount) + 1):
      if len(aliaDt) > 1:
        if aliaDt[1] == '+':
          cobDate = cobDate + datetime.timedelta(days=1)
          while cobDate.weekday() in [5, 6]:
            cobDate = cobDate + datetime.timedelta(days=1)
      else:
        cobDate = cobDate - datetime.timedelta(days=1)
        while cobDate.weekday() in [5, 6]:
          cobDate = cobDate - datetime.timedelta(days=1)
    return cobDate.strftime('%Y-%m-%d')

  if fType == 'M':
    endMontDate = datetime.datetime(cobDate.year, cobDate.month - int(fCount), 1)
    endMontDate = endMontDate - datetime.timedelta(days=1)
    while endMontDate.weekday() in [5, 6]:
      endMontDate = endMontDate - datetime.timedelta(days=1)
    return endMontDate.strftime('%Y-%m-%d')

  if fType == 'W':
    cobDate = cobDate - datetime.timedelta(days=1)
    while cobDate.weekday() != 4:
      cobDate = cobDate - datetime.timedelta(days=1)
    cobDate = cobDate - datetime.timedelta(days=(int(fCount) * 7))
    return cobDate.strftime('%Y-%m-%d')

  if fType == 'Y':
    endYearDate = datetime.datetime(cobDate.year - int(fCount), 1, 1)
    endYearDate = endYearDate - datetime.timedelta(days=1)
    while endYearDate.weekday() in [5, 6]:
      endYearDate = endYearDate - datetime.timedelta(days=1)
    return endYearDate.strftime('%Y-%m-%d')

  return aliaDt


def getDates(fromDt, toDt, weekdays=True):
  """
  :category: Python Utilities - Python Date function
  :example: aresObj.getDates("2018-02-01", "2018-01-01")
  :icon: fab fa-python
  :dsc:
    get the list of dates between two dates
  :return: A list of string dates in the common AReS format YYYY-MM-DD
  """
  resDt = []
  startDt = getDateFromAlias(fromDt)
  endDt = getDateFromAlias(toDt, fromDt=startDt)
  dt = datetime.datetime( *map(lambda x: int(x), startDt.split('-')))
  tgDt = datetime.datetime( *map(lambda x: int(x), endDt.split('-')))
  resDt.append(startDt)
  while dt > tgDt:
    dt = dt - datetime.timedelta(days=1)
    if not dt.weekday() in [5, 6] or not weekdays:
      resDt.append( dt.strftime('%Y-%m-%d') )
  return resDt


def getDateFromXl(xlDate):
  """
  :category: Python Utilities - Python Date function
  :example: aresObj.getDateFromXl(42948)
  :icon: fab fa-python
  :dsc:
    Convert a Excel date to a AReS standard date format YYYY-MM-DD.
  :return: The date as a String in the common format YYYY-MM-DD in AReS
  """
  dt = datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + xlDate - 2)
  return dt.strftime('%Y-%m-%d')


def fakefunction(*args, **kwargs):
  """
  :dsc: Simple wrapper to attache this to classes of module when we end up with a fake attribute
  """
  return None


def parseAttrError():
  """
  :dsc: Parse and fix AttributeError Exceptions
  """

  current_mod = None
  trace = traceback.format_exc().strip().split('\n')
  missing_attr = trace[-2].strip()
  if missing_attr.lstrip().startswith('class '):
    missing_attr = missing_attr.split('(')[1].split(')')[0]
  elif ' as ' in missing_attr:
    missing_attr = missing_attr.split()[1]
  elif ' ' in missing_attr:
    missing_attr = missing_attr.split()[-1]
  if '=' in missing_attr:
    missing_attr = missing_attr.split('=')[-1]
  for i, attr in enumerate(missing_attr.split('.')):
    if i == 0:
      current_mod = sys.modules[attr]
      continue

    if '(' in attr:
      attr = attr.split('(')[0]
      setattr(current_mod, attr, staticmethod(fakefunction))
      continue

    setattr(current_mod, attr, type(attr, (object,), {}))
    current_mod = getattr(current_mod, attr)


def parseImportError():
  """
  :dsc: Parse and fix ImportError Exceptions
  """
  error_line = traceback.format_exc().strip().split('\n')[-2]
  missing_names = []
  if 'from' in error_line:
    missing_mod = error_line.strip().split()[1]
    missing_names = [attr.strip() for attr in ''.join(error_line.strip().split()[3:]).split(',')]
  else:
    missing_mod = error_line.strip().split()[-1]
  previous_mod = []
  for module in missing_mod.split('.'):
    previous_mod.append(module)
    current_mod = '.'.join(previous_mod)
    if current_mod in sys.modules:
      for attr in missing_names:
        setattr(sys.modules[current_mod], attr, type(attr, (object,), {}))
      continue

    try:
      importlib.import_module(current_mod)
    except:
      mod = types.ModuleType(current_mod)
      for attr in missing_names:
        setattr(mod, attr, type(attr, (object,), {}))
      sys.modules[mod.__name__] = mod


def parse_error(file, error):
  """
  :dsc: import required module in python and handles error by creating fake modules on the fly
  We just use a counter here to make sure we get out of the loop after 99 tries
  """
  counter = 0
  while error:
    counter += 1
    if 'ImportError' in error.strip().split('\n')[-1]:
      parseImportError()
    elif 'AttributeError' in error.strip().split('\n')[-1]:
      parseAttrError()
    try:
      mod = importlib.import_module(file.replace('.py', ''))
      error = None
    except ImportError as e:
      error = traceback.format_exc()
    except AttributeError as e:
      error = traceback.format_exc()
    if counter > 99:
      return {}

  return mod