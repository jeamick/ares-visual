import ares.Lib.AresSql



class Sqlite(ares.Lib.AresSql.SqlConn):
  """
  :category: Connector
  :rubric: PY
  :type: Class
  :dsc:

    **The forceCreate function only works for sqlite**, create your database before starting adding the tables and data

    ## Sqlite Database

    ```python
    db = aresObj.db(dbFamily="mysql+pymysql", database="mysql", host="127.0.0.1", port="3306", username='root', password="") #database=r"newTestSuper.db")
    db.createTable(records=df, **modelFilePath)
    db.drop('youpi', withCheck=False )
    ```

    https://www.w3schools.com/python/python_mysql_getstarted.asp
  """
  dbFamily = 'reg_sqlite'


class AresSqlite(ares.Lib.AresSql.AresSqlConn):
  dbFamily = 'sqlite'

