from ares.Lib import Ares

"""
GENERAL PURPOSE
---------------

This script will aim to show how to store data into a database - nothing more

The sequel to this script (database_connections_2.py) will show how to retrieve data from the same db
and then display it using the visual capabilities of the AReS library

Finally database_connection_3.py will show a simple example of data extraction using the AReS connectors capabilities 
(see the scripts example connectors.py for more info),do some simple transformations, store it in the database. 
The aim of this module is to show a quick example on retreiving
the data directly from the db if it's there or go through the data extraction step if it's missing

After going through the three examples you should have the basics to use databases within AReS


PRE-REQUISITE
-------------

The database we will create in this script will be defined in the models folder as indicated with the modelPath argument
by default it will parse all the python scripts in that folder unless the filename argument is specified

"""
import random
import string

aresObj = Ares.ReportAPI()

#create the database - the on_init() function will be called if it exists in the model file (here test_models.py)
#if no database argument is specified the database will be created where this script is located
my_db = aresObj.db(modelPath=r'models', filename='test_model.py')

#Generate random data
record_set = []
for i in range(100):
  record_set.append({'name': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)), 'security_number': random.choice(range(10000))})

#get the column names for information
print(my_db.table('random_table').columns)

#insert the records in the database
my_db.insert('random_table', record_set, commit=True)

#get data using the fetch method which return an iterator
print list(my_db.select(['random_table']).fetch(limit=10))

#delete the first 20 records
my_db.delete('random_table').where([my_db.column('random_table', 'id') <= 20]).execute()


print list(my_db.select(['random_table']).fetch())

##delete with an or statement
my_db.delete('random_table').where([my_db.or_(my_db.column('random_table', 'id') == 21, my_db.column('random_table', 'id') == 55)]).execute()

#get data using the getData method which returns a pandas dataframe
print my_db.select(['random_table']).getData()

##delete with an and statement
my_db.delete('random_table').where([my_db.column('random_table', 'id') == 25]).where([my_db.column('random_table', 'name') != '']).execute()


#get data using the getData method which returns a pandas dataframe
print my_db.select(['random_table']).getData()