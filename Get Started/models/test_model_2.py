import sqlalchemy


"""
GENERAL PURPOSE
---------------

This is the model script used to create our table and the columns within them
the table names will be the function names and each function will return a list of sqlalchemy columns 
- for instance if you want to create a table customers, containing an id, a first name, a name, an address you will do as follow:

def customers():
  return  [sqlalchemy.Column('id', sqlalchemy.Integer, autoincrement=True, primary_key=True),
    sqlalchemy.Column('first name', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('name', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('address', sqlalchemy.String, nullable=False)]
    
You also have on_init capability see test_model.py in the same folder for more info

You can refer to the sqlalchemy documentation for help on how to define your columns:
https://docs.sqlalchemy.org/en/latest/
"""


def risk():
  return [sqlalchemy.Column('id', sqlalchemy.Integer, autoincrement=True, primary_key=True),
    sqlalchemy.Column('cob_dt', sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column('node', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('risk_type', sqlalchemy.String, nullable=False),
    sqlalchemy.Column('risk', sqlalchemy.Float, nullable=False)]

