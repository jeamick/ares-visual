import sqlalchemy

import datetime



def table1():
  return [sqlalchemy.Column('id', sqlalchemy.Integer, autoincrement=True, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String, default='This is a string'),
    sqlalchemy.Column('security_number', sqlalchemy.Integer),
    sqlalchemy.Column('creation_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow)]




def table2():
  return [sqlalchemy.Column('id2', sqlalchemy.Integer, autoincrement=True, primary_key=True),
    sqlalchemy.Column('name2', sqlalchemy.String, default='This is another string'),
    sqlalchemy.Column('creation_date', sqlalchemy.DateTime, default=datetime.datetime.utcnow)]
