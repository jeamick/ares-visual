#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import ares.Lib.AresSql


class AresMySAP(ares.Lib.AresSql.AresSqlConn):
  """
  :category: Connector SAP
  :rubric: PY
  :type: Class
  :dsc:
    This connector will allow a configuration to any SAP database.
    This could be either a ASE or IQ database
  """
  dbFamily = 'sybase+pyodbc'
  _extPackages = [("python-sybase", 'python-sybase'), ('sqlanydb', 'sqlanydb')]


