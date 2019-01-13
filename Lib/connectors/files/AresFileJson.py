#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
from ares.Lib.connectors.files import AresFile


class FileJson(AresFile.AresFile):
  """
  :category: Ares File
  :rubric: PY
  :type: Class
  :dsc:
    Parse the Json file
  """
  __fileExt = ['.json']
  label = "Interface to deal with Json files"

  def _read(self, **kwargs):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    """
    return json.load(open(self.filePath))

  def write(self, data, isAresDf=False):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    """
    if isAresDf:
      data = data.records()

    self.setFolder()
    with open(self.filePath, 'w') as outfile:
      json.dump(data, outfile)
