#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.connectors.files import AresFile
from ares.Lib import AresMarkDown


class FileMarkDown(AresFile.AresFile):
  """
  :category:
  :rubric:
  :type:
  :dsc:
  """
  __fileExt = ['.md', '.amd']
  label = "Interface to deal with Markdown files"

  def _read(self, toAresObj=False, **kwargs):
    inFile = open(self.filePath)
    data = AresMarkDown.AresMarkDown(self.filePath).convertStr(inFile.read().split("\n\n"), self.aresObj if toAresObj else None )
    inFile.close()
    return data

  def write(self, data, **kwargs):
    outFile = open(self.filePath.replace(self.fileExtension, '.py'), 'w')
    for line in data:
      outFile.write("%s\n" % line)
    outFile.close()
