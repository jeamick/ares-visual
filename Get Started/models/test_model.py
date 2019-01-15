import sqlalchemy
import datetime


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
    
You also have on_init capability that we will comment further below. Just know that for the remaining of this example the
user table will be useless. it's just a way of showing you how to execute function on the initialization of the db.

You can refer to the sqlalchemy documentation for help on how to define your columns:
https://docs.sqlalchemy.org/en/latest/
"""



def on_init(sql_obj):
  """
  :dsc: This function will define a default account
  :params sql_obj: This parameter is the sql_obj passed by the framework to allow to execute queries
  """

  if not list(sql_obj.select(['user']).where([sql_obj.column('user', 'email') == 'example@ares.com']).fetch()):
    sql_obj.insert('user', {'uid': -1, 'email': 'example@ares.com'}, commit=True)


def user():
  return [sqlalchemy.Column('uid', sqlalchemy.Integer, autoincrement=True, primary_key=True),
          sqlalchemy.Column('email', sqlalchemy.String, nullable=False)]


def random_table():
  return [sqlalchemy.Column('id', sqlalchemy.Integer, autoincrement=True, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String, default='This is a string'),
    sqlalchemy.Column('security_number', sqlalchemy.Integer),
    sqlalchemy.Column('creation_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow)]

