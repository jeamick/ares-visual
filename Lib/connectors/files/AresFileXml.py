#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import xml.sax
from ares.Lib.connectors.files import AresFile


class FileXml(AresFile.AresFile):
  """
  :category:
  :rubric:
  :type:
  :dsc:

  """
  __fileExt = ['.xml']

  def _read(self, **kwargs):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    """
    parser = xml.sax.make_parser()
    return parser.parse(open(self.filePath, "r"))

  def write(self, data):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    """
    with open(self.filePath, 'w') as outfile:
      json.dump(data, outfile)
