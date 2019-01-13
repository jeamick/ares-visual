#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import ares.Lib.AresSql


class AresPostGres(ares.Lib.AresSql.AresSqlConn):
  """
  :category: Connector
  :rubric: PY
  :type: Class
  :dsc:
    Connector to Access databases. This connector will allow you to create, store and retrieve data from any MS Access Database.
    This will return the AReS database object. It will be possible to reuse the same syntaxe to then interact with it.
    **The forceCreate function only works for sqlite**, create your database before starting adding the tables and data

    ## PostGreSql Database
    If you want to test your set up locally with a PostGres locally you can install one install locally [Here](https://www.enterprisedb.com/thank-you-downloading-postgresql?anid=1255962)
    Once the installation is done you will only have to get the localhost url of your database server

    ```python
      db = aresObj.db(dbFamily="postgresql", database="youpi", host="127.0.0.1", port="5433", username='postgres', password="240985") #database=r"newTestSuper.db")
      df = aresObj.file(htmlCode=r"IBRD_Balance_Sheet__FY2010.csv").read()
      modelFilePath = df.saveTo(fileFamily="model", dbName='Youpi2')
    ```

  """
  dbFamily = 'postgresql'
  _extPackages = [("psycopg2", 'psycopg2')]

