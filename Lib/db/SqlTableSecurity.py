#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from app import db
import datetime


class SecArchiveStoreTokens(db.Model):
  __bind_key__ = 'security'
  __tablename__ = 'archive_keys_store'

  key_id = db.Column(db.Integer, primary_key=True, nullable=False)  # This might need to be replicated from a serveur ?
  key_alias = db.Column(db.Text)
  key_token = db.Column(db.Text)
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, key_alias, key_token, user_name, hostname):
    self.key_alias, self.key_token, self.user_name, self.hostname =  key_alias, key_token, user_name, hostname

