from ares.Lib import Ares

"""
GENERAL PURPOSE
---------------

This script will aim to show how to store data once using a special key and then retreiving the information if the data is already there for that particular key

!! ATTENTION !! if you do not specify a filename in your db call your db will be created with the tables defined in all the files in the modelPath

PRE-REQUISITE
-------------

Here we use the connectors from the AReS framework - if you don't know how they work, please refer the connectors.py scripts in this folder
Check test_model_2.py to figure out the schema in this example
Check database_connections.py for an example of the basic syntax 

"""

def fetchData(cob_dt, db):
  """
  Part where we do the transformation logic and store in db
  """
  excludePtf = [123, 55, 79, 53]
  ptfMap = {'ASIA': [1, 2 , 3, 4], 'EUROPE': [5, 6, 7, 8, 9, 10], 'US': [11, 12, 13, 14, 15, 16, 17]}
  record_set = []
  for rec in aresObj.getData('WEB', {'url': 'something'}, toPandas=False):
    if rec['Portfolio'] in excludePtf:
      continue

    for node, ptfLst in ptfMap.items():
      if rec['Portfolio'] in ptfLst:
        record_set.append({'risk_type': rec['RiskType'], 'node': node, 'cob_dt': cob_dt, 'risk': rec['risk']})
        break

  db.insert('risk', record_set, commit=True)


aresObj = Ares.ReportAPI()

#create the db
my_db = aresObj.db(modelPath=r'models', filename='test_model_2.py')
cob_date = '2019-01-14'

hasData = False

#we're going to always this part of the query so we store it - it won't get executed as long as we don't call fetch() or getData()
base_query = my_db.select(['risk']).where([my_db.column('risk', 'cob_dt') == cob_date])

#check if the data exists
for rec in base_query.fetch(limit=1):
  hasData = True

#if it doesn't we call retrieve it and store it in the db
if not hasData:
  fetchData(cob_date, my_db)

#Finally we get the data and send it to the visualization part of AReS
aresObj.chart('pie', aresObj.df(base_query.getData()))

#output an HTML file
aresObj.toHtml()




