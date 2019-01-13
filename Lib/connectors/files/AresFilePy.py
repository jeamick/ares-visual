#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import sys
from ares.Lib.connectors.files import AresFile


class FilePy(AresFile.AresFile):
  """
  :category:
  :rubric:
  :type:
  :dsc:

  """
  __fileExt = ['.py']
  label = "Interface to deal with Python files"

  def _read(self, **kwargs):
    if self.aresObj is None:
      sys.path.append(self.path)
      return __import__(self.filename.replace('.py', ''))

    else:
      if self.aresObj.run.is_local:
        self.aresObj.notification('DANGER', 'Python module injected', '%s should not be loaded from a report' % self.filename)
        sys.path.append(self.path)
        return __import__(self.filename.replace('.py', ''))

    raise Exception('Cannot import the module %s' % self.filename)

  def write(self, data, **kwargs): pass