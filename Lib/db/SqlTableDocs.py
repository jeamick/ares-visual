#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from app import db
import datetime



# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO THE DOCUMENTATION
#
class AresDoc(db.Model):
  __bind_key__ = 'documentation'
  __tablename__ = 'doc'

  doc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  hash_id = db.Column(db.NUMERIC, nullable=False)
  src_id = db.Column(db.Integer, nullable=False)
  dsc = db.Column(db.Text, nullable=False)
  rubric = db.Column(db.String(120), nullable=False)
  category = db.Column(db.String(120), nullable=False)
  module = db.Column(db.String(50), nullable=False)
  cls = db.Column(db.String(50), nullable=False)
  fnc = db.Column(db.String(50), nullable=False)
  type = db.Column(db.String(20), nullable=False) # FUNCTION, CLASS, MODULE
  section = db.Column(db.String(20), nullable=False) # ARES, REPORTS, CONNECTOR...
  return_dsc = db.Column(db.Text, nullable=False)
  name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, dsc, rubric, category, module, cls, fnc, doc_type, section, name,
               return_dsc, user_name, hostname, mac_address, src_id):
    self.dsc, self.rubric, self.category, self.module, self.cls = dsc, rubric, category, module, cls
    self.fnc, self.type, self.section, self.name, self.src_id = fnc, doc_type, section, name, src_id
    self.hash_id = AresSiphash.SipHash().hashId("%s_%s_%s_%s" % (module, cls, fnc, doc_type) )
    self.return_dsc, self.user_name, self.hostname, self.mac_address = return_dsc, user_name, hostname, mac_address


class AresDocView(db.Model):
  __bind_key__ = 'documentation'
  __tablename__ = 'doc_view'

  vw_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  hash_id = db.Column(db.NUMERIC, nullable=False)
  user_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, module, cls, fnc, doc_type, user_name, hostname, mac_address):
    self.user_name, self.hostname, self.mac_address = user_name, hostname, mac_address
    self.hash_id = hashlib.sha224("%s_%s_%s_%s" % (module, cls, fnc, doc_type))
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class AresDocComments(db.Model):
  __bind_key__ = 'documentation'
  __tablename__ = 'doc_comments'

  com_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  hash_id = db.Column(db.NUMERIC, nullable=False)
  com = db.Column(db.Text, nullable=False)
  status = db.Column(db.Integer, nullable=False)  # 1 active, 0 closed
  user_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, module, cls, fnc, doc_type, com, status, user_name, hostname, mac_address):
    self.com, self.status, self.user_name, self.hostname, self.mac_address = com, status, user_name, hostname, mac_address
    self.hash_id = AresSiphash.SipHash().hashId("%s_%s_%s_%s" % (module, cls, fnc, doc_type))
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class AresDocExamples(db.Model):
  __bind_key__ = 'documentation'
  __tablename__ = 'doc_examples'

  ex_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  hash_id = db.Column(db.NUMERIC, nullable=False)
  ex = db.Column(db.Text, nullable=False)
  user_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, module, cls, fnc, doc_type, ex, user_name, hostname, mac_address):
    self.ex, self.user_name, self.hostname, self.mac_address = ex, user_name, hostname, mac_address
    self.hash_id = AresSiphash.SipHash().hashId("%s_%s_%s_%s" % (module, cls, fnc, doc_type))
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class AresDocTags(db.Model):
  __bind_key__ = 'documentation'
  __tablename__ = 'doc_static_tags'

  ex_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  hash_id = db.Column(db.NUMERIC, nullable=False)
  tag = db.Column(db.Text, nullable=False)
  user_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, module, cls, fnc, doc_type, tag, user_name, hostname, mac_address):
    self.tag, self.user_name, self.hostname, self.mac_address = tag, user_name, hostname, mac_address
    self.hash_id = AresSiphash.SipHash().hashId("%s_%s_%s_%s" % (module, cls, fnc, doc_type))
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class AresDocLinks(db.Model):
  __bind_key__ = 'documentation'
  __tablename__ = 'doc_links'

  link_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  hash_id = db.Column(db.NUMERIC, nullable=False)
  link_name = db.Column(db.Text, nullable=False)
  link_url = db.Column(db.Text, nullable=False)
  user_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, module, cls, fnc, doc_type, link_name, link_url, user_name, hostname, mac_address):
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')
    self.link_name, self.link_url = link_name, link_url
    self.user_name, self.hostname, self.mac_address = user_name, hostname, mac_address
    self.hash_id = AresSiphash.SipHash().hashId("%s_%s_%s_%s" % (module, cls, fnc, doc_type))


class AresDocParams(db.Model):
  __bind_key__ = 'documentation'
  __tablename__ = 'doc_params'

  param_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  arc_id = db.Column(db.Integer, nullable=False)
  param_type = db.Column(db.Text, nullable=False)
  hash_id = db.Column(db.NUMERIC, nullable=False)
  name = db.Column(db.Text, nullable=False)
  dsc = db.Column(db.Text, nullable=False)
  duck_type = db.Column(db.Text, nullable=False)
  user_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, module, cls, fnc, doc_type, param_name, param_dsc, param_duck_type, user_name,
               hostname, mac_address):
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')
    self.user_name, self.hostname, self.mac_address = user_name, hostname, mac_address
    self.param_name, self.param_dsc, self.param_duck_type = param_name, param_dsc, param_duck_type
    self.hash_id = AresSiphash.SipHash().hashId("%s_%s_%s_%s" % (module, cls, fnc, doc_type))


class AresDocIO(db.Model):
  __bind_key__ = 'documentation'
  __tablename__ = 'doc_io'

  io_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  cod = db.Column(db.Text, nullable=False)
  dsc = db.Column(db.Text, nullable=False)
  typ = db.Column(db.Text, nullable=False)
  user_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

