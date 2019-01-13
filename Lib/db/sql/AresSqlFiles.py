#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import datetime
import os

from ares.Lib.db import SqlTableFiles, SqlTableAres
from flask_login import current_user


# ---------------------------------------------------------------------------------------------------------
#                                          ADD ENTRIES TO THE FILES DATABASE
#
def dbAddFileUser(fileCode, accessType, hostname, userName=None):
  if userName is None:
    userName = current_user.email
  response = SqlTableFiles.FileUser.query.filter_by(file_code=str(fileCode), user=userName ).first()
  # Check if user exist and if he is not already attached to this file
  isValidUser = SqlTableAres.User.query.filter_by(email=userName).first()
  if response is None and isValidUser is not None:
    response = SqlTableFiles.FileUser(fileCode, userName, accessType, current_user.email, hostname)
    SqlTableFiles.db.session.add(response)
    SqlTableFiles.db.session.commit()

def dbAddFileArchive(fileName, salt, hostname, endDt, userName=None):
  if userName is None:
    userName = current_user.email
  response = SqlTableFiles.FileUserArchive.query.filter_by(file_name=str(fileName)).first()
  # Check if user exist and if he is not already attached to this file
  if response is None:
    response = SqlTableFiles.FileUserArchive(fileName, salt, endDt, "", userName, hostname)
    SqlTableFiles.db.session.add(response)
    SqlTableFiles.db.session.commit()
  else:
    response.salt = salt
    response.user_name = userName
    response.lst_mod_dt = datetime.datetime.utcnow()
    SqlTableAres.db.session.merge(response)
    SqlTableAres.db.session.flush()
    SqlTableAres.db.session.commit()

def dbAddFileArchiveView(fileName, hostname, userName=None):
  response = SqlTableFiles.FileUserArchiveViews(fileName, userName, hostname)
  SqlTableFiles.db.session.add(response)
  SqlTableFiles.db.session.commit()

def _getSaltinfo(fileName):
  response = SqlTableFiles.FileUserArchive.query.filter_by(file_name=str(fileName)).first()
  return response.salt, response.end_dt

def dbRemFile(fileCode):
  response = SqlTableFiles.File.query.filter_by(file_code=str(fileCode)).first()
  if response is not None:
    response.status = 'DELETED'
    response.is_active = 0
    response.user_name = current_user.email
    SqlTableAres.db.session.merge(response)
    SqlTableAres.db.session.flush()
    SqlTableAres.db.session.commit()
    return {'status': True}

  return {'status': False}

def dbAddFileHistory(fileId, comment, hostname):
  response = SqlTableFiles.FileHistory(str(fileId), comment, current_user.email, hostname)
  SqlTableFiles.db.session.add(response)
  SqlTableFiles.db.session.commit()

def dbAddFileAccess(fileId, runId, cmmt, hostname):
  response = SqlTableFiles.FileDataAccess(str(fileId), runId, cmmt, current_user.email, hostname)
  SqlTableFiles.db.session.add(response)
  SqlTableFiles.db.session.commit()

def dbAddFileDownload(fileId, hostname):
  response = SqlTableFiles.FileDataDownload(str(fileId), current_user.email, hostname)
  SqlTableFiles.db.session.add(response)
  SqlTableFiles.db.session.commit()

def dbAddFileColumns(fileId, cols, colsType, hostname):
  fileCode = str(fileId)
  response = SqlTableFiles.FileDataColumns.query.filter_by(file_code=fileCode).first()
  if response is None:
    # col_dsc, user_name, hostname
    for i, col in enumerate(cols):
      response = SqlTableFiles.FileDataColumns(fileCode, i, col, str(colsType[i]), "", current_user.email, hostname)
      SqlTableFiles.db.session.add(response)
      SqlTableFiles.db.session.commit()

def dbAddFileInfo(fileId, size, delimiter, hostname):
  fileCode = str(fileId)
  response = SqlTableFiles.FileData.query.filter_by(file_code=fileCode).first()
  if response is None:
    response = SqlTableFiles.FileData(fileCode, size, delimiter, current_user.email, hostname)
    SqlTableFiles.db.session.add(response)
    SqlTableFiles.db.session.commit()

def dbAddFile(fileId, fullName, fileType, hostname):
  fileCode, isNew = str(fileId), False
  response = SqlTableFiles.File.query.filter_by(file_code=fileCode).first()
  if response is None:
    response = SqlTableFiles.File(file_code=fileCode, full_name=fullName, file_type=fileType, is_active=1, user_name=current_user.email, hostname=hostname)
    SqlTableFiles.db.session.add(response)
    SqlTableFiles.db.session.commit()
    dbAddFileUser(fileCode, 'New File', hostname, current_user.email)
    isNew = True
  return {"new": isNew, 'data': response}


# ---------------------------------------------------------------------------------------------------------
#                                          RETRIEVE DATA FROM THE FILES DATABASE
#

AUTH_FOLDERS = {"OUTPUTS": "outputs", "REPORTS": "reports", "FUNCTIONS": 'fncs', 'EXTERNALS': 'ext', "SERVICES": 'sources', 'SQL_DB': "model"}

def getUsers(fileId):
  users = []
  for rec in SqlTableFiles.FileUser.query.filter_by(file_code=str(fileId)).all():
    users.append( rec.user )
  return users

def getFileDetails(fileId):
  response = SqlTableFiles.db.session.query(SqlTableFiles.File, SqlTableFiles.FileUser)\
    .filter(SqlTableFiles.File.is_active == 1) \
    .filter(SqlTableFiles.File.file_code == str(fileId)) \
    .filter(SqlTableFiles.File.file_code == SqlTableFiles.FileUser.file_code) \
    .filter(SqlTableFiles.FileUser.user == current_user.email).first()
  if response is not None:
    return {}
  return {}

def getUserFiles(report_name, folder_code, user_name='ALL'):
  myFiles = {}
  sqlFiles = SqlTableFiles.db.session.query(SqlTableFiles.File, SqlTableFiles.FileUser, SqlTableFiles.FileData) \
      .filter(SqlTableFiles.File.file_code == SqlTableFiles.FileUser.file_code) \
      .filter(SqlTableFiles.File.file_type == folder_code) \
      .filter(SqlTableFiles.File.full_name.like("%"+ report_name +"%")) \
      .filter(SqlTableFiles.File.is_active == 1) \
      .outerjoin(SqlTableFiles.FileData, SqlTableFiles.File.file_code == SqlTableFiles.FileData.file_code)
  if user_name != 'ALL':
    sqlFiles = sqlFiles.filter(SqlTableFiles.FileUser.user == user_name)
  for res in sqlFiles.all():
    # Split to path to only keep the path to the
    splitFileName = res[0].full_name.split(report_name)
    fileShortPath = report_name.join(splitFileName[1:])
    if res[0].file_type in ["FUNCTIONS", "SERVICES"]:
      fileShortPath = os.path.join(*fileShortPath.split( AUTH_FOLDERS[res[0].file_type] ))[1:]
    myFiles[fileShortPath] = {'filename': fileShortPath, 'label': fileShortPath, 'delimiter': res[2].file_delimiter if res[2] is not None else '',
                              'size': "%0.2f MB" % (res[2].file_size / 1024) if res[2] is not None else '', 'lst_update': res[0].lst_mod_dt.strftime('%Y-%m-%d %H:%M:%S'),
                              'icon': "far fa-file-alt", 'file_path': res[0].full_name}
  return myFiles

def getAllReports(report_name):
  records = []
  for res in SqlTableFiles.db.session.query(SqlTableFiles.Environments, SqlTableFiles.Scripts) \
      .filter(SqlTableFiles.Environments.report_name == report_name) \
      .filter(SqlTableFiles.Scripts.is_valid == 1) \
      .filter(SqlTableFiles.Environments.env_id == SqlTableFiles.Scripts.env_id).all():
    if res[1].script_name != "__init__":
      records.append( "%s.py" % res[1].script_name )
  return {report_name: records}

def changeReportFlag(report_name, script_name, flag):
  response = SqlTableFiles.db.session.query(SqlTableFiles.Environments, SqlTableFiles.Scripts) \
      .filter(SqlTableFiles.Environments.report_name == report_name) \
      .filter(SqlTableFiles.Scripts.script_name == script_name) \
      .filter(SqlTableFiles.Environments.env_id == SqlTableFiles.Scripts.env_id).first()
  if response is not None:
    response[1].is_valid = flag
    SqlTableFiles.db.session.merge(response[1])
    SqlTableFiles.db.session.flush()
    SqlTableFiles.db.session.commit()
  return True