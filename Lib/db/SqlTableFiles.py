#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from app import db
import datetime



# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO A SCRIPT RUN FOR A DEDICATED SCRIPT
#
class File(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file'

  int_id = db.Column(db.Integer, primary_key=True, nullable=False)  # This might need to be replicated from a serveur ?
  file_code = db.Column(db.Text)
  full_name = db.Column(db.Text) # This should be unique and it will include the subfolders
  file_type = db.Column(db.String(10)) # FUNCTIONS, REPORTS, OUTPUTS
  status = db.Column(db.String(10), default='')  # DELETED
  is_active = db.Column(db.Integer, nullable=False)  # 1 True, 0 False
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_code, full_name, file_type, is_active, user_name, hostname):
    self.file_code, self.full_name, self.file_type, self.user_name, self.is_active, self.hostname = file_code, full_name, file_type, user_name, is_active, hostname


class FileDsc(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file_dsc'

  file_dsc_id = db.Column(db.Integer, primary_key=True, nullable=False)
  file_code = db.Column(db.Text)
  comment = db.Column(db.Text)
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_code, comment, user_name, hostname):
    self.file_code, self.comment, self.user_name, self.hostname = file_code, comment, user_name, hostname


class FileUser(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file_user'

  file_used_id = db.Column(db.Integer, primary_key=True, nullable=False)
  file_code = db.Column(db.Text)
  user = db.Column(db.String(200), nullable=False)
  access_type = db.Column(db.String(200), nullable=False)
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_code, user, access_type, user_name, hostname):
    self.file_code, self.user, self.access_type, self.user_name, self.hostname = file_code, user, access_type, user_name, hostname


class FileHistory(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file_history'

  file_histo_id = db.Column(db.Integer, primary_key=True, nullable=False)
  file_code = db.Column(db.Text)
  comment = db.Column(db.Text)
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_code, comment, user_name, hostname):
    self.file_code, self.user_name, self.comment, self.hostname = file_code, comment, user_name, hostname


class FileData(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file_data'

  file_data_id = db.Column(db.Integer, primary_key=True, nullable=False)
  file_code = db.Column(db.Text)
  file_size = db.Column(db.Float)
  file_delimiter = db.Column(db.String(5))
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_code, file_size, file_delimiter, user_name, hostname):
    self.file_code, self.file_size, self.file_delimiter, self.user_name, self.hostname = file_code, file_size, file_delimiter, user_name, hostname


class FileDataDownload(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file_data_download'

  file_export_id = db.Column(db.Integer, primary_key=True, nullable=False)
  file_code = db.Column(db.Text)
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_code, user_name, hostname):
    self.file_code, self.user_name, self.hostname = file_code, user_name, hostname


class FileDataColumns(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file_data_columns'

  file_col_fnc_id = db.Column(db.Integer, primary_key=True, nullable=False)
  file_code = db.Column(db.Text)
  col_ord = db.Column(db.Integer)
  col_name = db.Column(db.String(120))
  col_type = db.Column(db.Text)
  col_dsc = db.Column(db.Text)
  start_dt = db.Column(db.String(10), default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  end_dt = db.Column(db.String(10), nullable=True, default=None)
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_code, col_ord, col_name, col_type, col_dsc, user_name, hostname):
    self.file_code, self.col_ord, self.col_name, self.col_type, self.col_dsc, self.user_name, self.hostname = file_code, col_ord, col_name, col_type, col_dsc, user_name, hostname


class FileDataAccess(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file_data_access'

  file_access_id = db.Column(db.Integer, primary_key=True, nullable=False)
  file_code = db.Column(db.Text)
  run_id = db.Column(db.Integer)
  cmmt = db.Column(db.Text)
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_code, run_id, cmmt, user_name, hostname):
    self.file_code, self.run_id, self.cmmt, self.user_name, self.hostname = file_code, run_id, cmmt, user_name, hostname


class FileUserArchive(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file_data_archives'

  file_archive_id = db.Column(db.Integer, primary_key=True, nullable=False)
  file_name = db.Column(db.Text)
  salt = db.Column(db.Integer) # For the hash of the markdown file
  cmmt = db.Column(db.Text)
  end_dt = db.Column(db.DateTime, nullable=True)
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_name, salt, end_dt, cmmt, user_name, hostname):
    year, month, day = end_dt.split('-')
    self.file_name, self.end_dt, self.cmmt, self.salt, self.user_name, self.hostname = file_name, datetime.datetime(int(year), int(month), int(day)), cmmt, salt, user_name, hostname


class FileUserArchiveViews(db.Model):
  __bind_key__ = 'files'
  __tablename__ = 'file_data_archives_views'

  file_archive_view_id = db.Column(db.Integer, primary_key=True, nullable=False)
  file_name = db.Column(db.Text)
  user_name = db.Column(db.String(200), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, file_name, user_name, hostname):
    self.file_name, self.user_name, self.hostname = file_name, user_name, hostname


