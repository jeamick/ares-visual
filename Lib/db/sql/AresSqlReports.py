#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import datetime

from ares.Lib.db import SqlTableAres
from flask_login import current_user


def getUserId(user_name):
  response = SqlTableAres.User.query.filter_by(email=user_name).first()
  if response is None:
    return None

  return response.uid

def getRepoPath(group_name):
  return SqlTableAres.GroupsRepository.query.filter_by(group_name=group_name).first()

def getEnvId(report_name):
  response = SqlTableAres.Environments.query.filter_by(report_name=report_name).first()
  if response is None:
    return None

  return response.env_id

def getScriptId(report_name, script_name):
  scriptId = SqlTableAres.db.session.query(SqlTableAres.Environments, SqlTableAres.Scripts)\
    .filter(SqlTableAres.Environments.report_name == report_name) \
    .filter(SqlTableAres.Scripts.script_name == script_name).first()
  if scriptId is None:
    return (None, None)

  return (scriptId[0].env_id, scriptId[1].script_id)

def getContributors(report_name):
  env_id = getEnvId(report_name)
  records = set()
  for rec in SqlTableAres.EnvironmentsContributor.query.filter_by(env_id=env_id, report_name=report_name).all():
    if rec.end_dt is None and rec.start_dt < datetime.datetime.now():
      records.add(rec.contributor)
    elif rec.start_dt < datetime.datetime.now() < rec.end_dt:
      records.add(rec.contributor)
  return records

def addEnv(env_name, env_path, env_dsc, remote_addr):
  response = SqlTableAres.Environments(env_name, env_path, env_dsc, current_user.email)
  SqlTableAres.db.session.add(response)
  SqlTableAres.db.session.commit()
  addContributors(env_name, current_user.email, remote_addr)
  return response.env_id

def addContributors(report_name, user_name, remote_addr):
  uid = getUserId(user_name)
  env_id = getEnvId(report_name)
  if uid is not None and env_id is not None:
    runScriptResp = SqlTableAres.EnvironmentsContributor(env_id=env_id, report_name=report_name, contributor=user_name, usr_name=current_user.email, hostname=remote_addr)
    SqlTableAres.db.session.add(runScriptResp)
    try:
      SqlTableAres.db.session.commit()
      return True
    except Exception as err:
      return False
  return False


# ---------------------------------------------------------------------------------------------------------
#                                          DOCUMENTATION SECTION
#
def addDocView(report_name, script_name):
  envId, scriptId = getScriptId(report_name, script_name)
  runScriptResp = SqlTableAres.ScriptsDocViews(script_id=scriptId, usr_name=current_user.email)
  SqlTableAres.db.session.add(runScriptResp)
  try:
    SqlTableAres.db.session.commit()
    return True
  except:
    return False

def updateDocView(report_name, script_name, remote_addr):
  envId, scriptId = getScriptId(report_name, script_name)
  runScriptResp = SqlTableAres.ScriptsDocViewsUpdate(script_id=scriptId, usr_name=current_user.email, hostname=remote_addr)
  SqlTableAres.db.session.add(runScriptResp)
  try:
    SqlTableAres.db.session.commit()
    return True
  except:
    return False

def getLastDocUpdate(report_name, script_name):
  envId, scriptId = getScriptId(report_name, script_name)
  response = SqlTableAres.ScriptsDocViewsUpdate.query.filter_by(script_id=scriptId).order_by(
      SqlTableAres.ScriptsDocViewsUpdate.lst_mod_dt.desc()).first()
  if response is not None:
    return {"author": response.usr_name, "lst_mod_dt": response.lst_mod_dt.strftime("%Y-%m-%d %H:%M:%S")}
  return {"author": "", "lst_mod_dt": ""}
