#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

# http://ryrobes.com/python/sql-server-query-to-tableau-data-extract-more-tde-api-fun-with-python-tableau-8/

# From TDE-API-Python-64Bit.zip (available here https://www.tableau.com/products/api-download?ref=lp&signin=17c5a22f71849b44ea037b395cc1bbe3)

import os
import platform
from ares.Lib.connectors.files import AresFile
from ares.Lib.AresImports import requires

ares_tde = requires("dataextract",
  reason='Missing Package, please go to the TABLEAU website to get more details about this module: ',
  install=False, autoImport=False, sourceScript=__file__)

class FileTableau(AresFile.AresFile):
  """
  :category:
  :rubric:
  :type:
  :dsc:

  :link Example: https://stackoverflow.com/questions/39449673/how-to-convert-csv-format-file-to-tde-format-file-tableau-extract-using-pyth
  """
  __fileExt = ['.tde']

  def __init__(self, data, filePath, aresObj=None):
    super(FileTableau, self).__init__(data, filePath, aresObj)
    self.head, self.tail = os.path.split(filePath)

  def isCompatible(self, **kwargs):
    if platform.architecture()[0] == '64bit':
      return (True, "")

    return (False, "")

  def _read(self, **kwargs):
    raise Exception("No idea how to implement this part, feel free to propose ! Thanks")

  def write(self, jdf, replace=False):
    if os.path.isfile(self.filePath) and replace:
      os.remove(self.filePath)

    tdefile = ares_tde.Extract(self.filePath)
    tableDef = ares_tde.TableDefinition()
    tableDef.addColumn('Country', ares_tde.Type.CHAR_STRING)
    tableDef.addColumn('sales', ares_tde.Type.INTEGER)
    tableDef.addColumn('units', ares_tde.Type.INTEGER)
    table = tdefile.addTable("Extract", tableDef)

    # Create new row
    # https://onlinehelp.tableau.com/current/api/sdk/en-us/SDK/tableau_sdk_working_with_extracts.htm
    new_row = ares_tde.Row(tableDef)


if __name__ == '__main__':
  tdeFile = FileTableau("MyOrders.tde")
  tdeFile.read()

