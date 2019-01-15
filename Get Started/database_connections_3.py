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

The database we will create in this script will use a model defined in the models folder - just know you can either
you can refer to that script to know how you can define your own model for you db.

The Model folder can actually be anywhere you want, as long as you define modelPath
"""


aresObj = Ares.ReportAPI()

