#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
  'eng':
'''
:dsc:
# Scripting API Documentation

***

&nbsp;&nbsp;[!(fas fa-chevron-circle-right) Common API Documentation](api)

***

This section is more dedicated to the prototype phase when you do not really know the data you will face.
In this scripting mode you will only focus on the data transformation and also in putting in place the right logic to get a good data quality for your algorithms.
Here you can easily benefit from everything in the framework and the way it work will encourage you to produce something ready for the next phase (the web dashboard).

## Ares Object

As long as the path of the project is in your python classpath you can use one of the two way to get an aresObj
In the framework you always get the secured one but as a shortcut if you only need to tranform data from unsecured sources you can skip this.
**Please keep in mind to never share any report in which you are using your AReS credentials !**

```python
import ares.Lib.Ares as Ares
aresObj = Ares.ReportAPI()
```

```python
import ares.Lib.Ares as Ares
aresObj = Ares.ReportAPI(username='', password='')
```

## Existing and Bespoke functions

You can load existing functions from a report or even create new ones and attached them to your local AReS object.
This will allow you to reuse the existing bespoke functions but also to extend with new ones.
If you want to push your changes to production please liaise first with your IT team.
__
**The bespoke functions are usefull to test a project and also to correctly split your work during the prototyping phase but obviously this cannot be used on a server. **
If you want to push your project on a server you will have to commit your functions to an environment. At this stage there is no common modules with functions shared with all the environments but do not hesitate to let us know if you think this should be added.

```python
# Loads a bespoke function on my computer
aresObj.fncs(fileFullPath='/youpi3/MyFncs.py')
print( aresObj.MyNewFnc(1, 4, 3) )
&nbsp;
# Loads all the functions available for the project Project1
aresObj.fncs(reportName='Project1', reportPath='D:/RiskLab/user_reports')
print( aresObj.toto(1222) )
```

## Databases

Get rid a flat files to store data and start to produce the right data model using light databases.
AReS will use [Sqlite](https://www.sqlite.org/index.html) and [SqlAlchemy](https://www.sqlalchemy.org/) to allow you to structure your project as a proper IT project.
Even if in a production environment Database might differ (using more robust plateforms like Oracle, MySql or SaP) the data model is the most important part in the data processing.

```python
# Create a bespoke database in your scripting environment
db = aresObj.db().forceCreate()
db.loadSqlFile("DbTableTest.py", filePath=r"./user_reports/test/model/tables") # Add a table
db.insert([ {"col1": 3, "col2": "Test"}], tableName='test', commit=True)

# Create a database with a specific name
db = aresObj.db(dbFullPath=r"./user_scripts/myDBTest.db").forceCreate()

# Get data from an existing database in an AReS environment
dbQuizz = aresObj.db(dbFullPath=r"../user_reports/QUIZZ/QUIZZ_17242600690872495757.db")
print( dbQuizz.select(['quizz_answers']).toDf() )
```

It is possible to retrieve data from variables datatabase [Access databases](https://en.wikipedia.org/wiki/Microsoft_Access) for Excel project or [MongoDb](https://en.wikipedia.org/wiki/MongoDB).
It is very easy to mix files and database tables from this framework. Thus you can based on files create your SqlAlchemy data model and then share this to move to production. The key to get the best project is to store and retrieve data the most efficiently (and this will rely only on the datamodel !)
**So please think about data storage before starting your algorithms**

```python
# Get data from a local version of a postgreSql database 
db = aresObj.db(dbFamily="postgresql", database="youpi", host="127.0.0.1", port="5433", username='postgres', password="240985")
db.loadSqlFile("SqlYoupi3.py", path='./') # Load a table structure from a file

# Load a file by defining a delimter and also filtering on some column only
df = aresObj.file(filename='DATA_2018-04-22.txt').read(usecols=['date', 'ouv', 'haut'], sep='\t')
modelFilePath = df.saveTo(fileFamily="model", dbName='TEST') # Create a SQL table structure file
# THen I add it to my model with the respective data
db.createTable(records=df, reset=True, **modelFilePath)
```

**The above example can be done in any database by changing the dbFamily to sqlite, mysql+pymysql...**

We are currently working on implmeenting simple wrapper to [Neo4j](https://neo4j.com/download-neo4j-now/?utm_source=google&utm_medium=ppc&utm_campaign=*UK%20-%20Search%20-%20Branded&utm_adgroup=*UK%20-%20Search%20-%20Branded%20-%20Neo4j%20-%20Exact&utm_term=neo4j&gclid=CjwKCAjw0oveBRAmEiwAzf6_rBVM-EcGh_SxIDJNIabex4rdRAEjWC_I3D5ocpmYd9G8th_4xSNU6hoCu1IQAvD_BwE) database to get the best of them

## Connectors

Most of the connectors can be used to test the processes before thinking of the web interface.
You can see below some examples of code ready to use. With the connectors no need to rewrite everything you can implement those bridges to get data from different systems.
You can get the help on the connector either from the web insterface or by calling the function **help()** *(please keep in mind that this is still a work in progress task)*

```python
import ares.Lib.Ares as Ares
aresObj = Ares.ReportAPI()
print( aresObj.getData('PDF', {'page': 1}, filename='D:/file.pdf') )
```

```python
import ares.Lib.Ares as Ares
aresObj = Ares.ReportAPI(username='', password='')
aresObj.conn('JIRA').help()
```

## How to test external Services / Sources ?

It is possible to test also the services (script in the folders sources) locally from this API. 
This should be done using a special function and some extra parameters as shown below.
**This is only to test Ajax services locally, this should be removed when deployed on the server as those services should be consummed by the javascript layer**

```python
import ares.Lib.Ares as Ares
aresObj = Ares.ReportAPI()
result = aresObj.services(params={"zzf": 12}, reportName="examples", scriptName="dataRest.py", reportPath=r"../user_reports")
print result
```

## Python Packages

You can also use external packages within the framework. Indeed the underlying objects in the AReS Framework are based on standard ones. Pandas and Numpy are the main pillars in order to store and tranform the data.
Most of the best Python packages are already included to the AReS ecosystem so please double check before try to use a new one. Each package should be carrefully studied before adding it.

#### Numpy 

You can use the function .np() to retrieve the numpy package and then to use all the existing functions.
Do not hesitate to have a look at the only [Numpy](http://www.numpy.org/) documentation.
I would recommend to look at the very useful Numpy CheatSheet [here](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Numpy_Python_Cheat_Sheet.pdf)

```python
np = aresObj.np()
a = np.arange(15).reshape(3, 5)
print(a)
```

#### Pandas 

The below lines of code are returning a AReS dataframe object. The real [Pandas](https://pandas.pydata.org/) object is wrapped within the AReS dataframe. You can obviously retrieve it but the best wouls be to trry as much as possible to use this layer of abstraction. The purpose of this class is to enrich the Dataframe with some Javascript function to optimise the conversion in the front end
I would recommend to look at the very useful Pandas CheatSheet [here](https://github.com/pandas-dev/pandas/blob/master/doc/cheatsheet/Pandas_Cheat_Sheet.pdf)

```python
# Returns a AReS dataframe from a list of dictionaries
aresObj.df([{"a": "gre", "b": "gre"}]).to_txt()
&nbsp;
# Returns a AReS dataframe from a file
adf = aresObj.file(filename="data3.csv", path=r"D:/Risklab/user_reports/examples/outputs")
print( adf )
```

Other frameworks are also available in order to perform Data mining or some IA work like TensorFlow but do not hesitate to let us know if you need further details.
Anyway a generic way to import and use an external package is ti use the imp function.

```python
np = aresObj.imp('numpy')
```

**We prioritise the creation of the interfaces according to the request to please let us know your needs !**

'''
}
