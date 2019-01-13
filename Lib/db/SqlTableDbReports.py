#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from app import db
import datetime
from ares.utils import AresSiphash


class TableDb(db.Model):
  __bind_key__ = 'db_data'
  __tablename__ = 'dbs'

  db_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  db_name = db.Column(db.Text, unique=True, nullable=False)
  report_name = db.Column(db.Text)
  usr_nam = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


  def __init__(self, db_name, report_name, usr_nam, hostname):
    self.db_name, self.report_name, self.usr_nam, self.hostname = db_name, report_name, usr_nam, hostname