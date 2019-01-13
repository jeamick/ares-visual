#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import ares.Lib.AresSql


class AresMySql(ares.Lib.AresSql.AresSqlConn):
  """
  :category: Connector
  :rubric: PY
  :type: Class
  :dsc:

    **The forceCreate function only works for sqlite**, create your database before starting adding the tables and data

    ## MySql Database

    ```python
    df = aresObj.file(htmlCode=r"IBRD_Balance_Sheet__FY2010.csv").read()
    modelFilePath = df.saveTo(fileFamily="model", dbName='Youpi2')

    db = aresObj.db(dbFamily="mysql+pymysql", database="mysql", host="127.0.0.1", port="3306", username='root', password="") #database=r"newTestSuper.db")
    db.createTable(records=df, **modelFilePath)
    db.drop('youpi', withCheck=False )
    ```

    https://www.w3schools.com/python/python_mysql_getstarted.asp
  """
  dbFamily = 'mysql+pymysql'
  _extPackages = [("pymysql", 'pymysql')]

