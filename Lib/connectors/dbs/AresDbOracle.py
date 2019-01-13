#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import ares.Lib.AresSql


class AresOracle(ares.Lib.AresSql.AresSqlConn):
  """
  :category: Connector
  :rubric: PY
  :type: Class
  :dsc:
    Connector to Access databases. This connector will allow you to create, store and retrieve data from any MS Access Database.
    This will return the AReS database object. It will be possible to reuse the same syntaxe to then interact with it.

  https://www.oracle.com/database/technologies/appdev/xe.html
  https://docs.oracle.com/cd/E17781_01/admin.112/e18585/toc.htm#XEGSG111
  """
  dbFamily = 'oracle'
  _extPackages = [("cx_Oracle", 'cx_Oracle')]

