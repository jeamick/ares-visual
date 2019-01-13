#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import pickle
from ares.Lib.connectors.files import AresFile


class FilePickle(AresFile.AresFile):
  """
  :category: Ares File
  :rubric: PY
  :type: Class
  :dsc:

  """
  __fileExt = ['.pkl']
  label = "Interface to read and write Pickle files"

  def _read(self, **kwargs):
    """
    :category: Ares File
    :rubric: PY
    :type: Data Loading
    :dsc:

    """
    return pickle.load(open(self.filePath))

  def write(self, data, isAresDf=False):
    """
    :category: Ares File
    :rubric: PY
    :type: Data Loading
    :dsc:

    """
    if isAresDf:
      data = data.records()

    self.setFolder()
    with open(self.filePath, 'w') as outfile:
      pickle.dump(data, outfile)
