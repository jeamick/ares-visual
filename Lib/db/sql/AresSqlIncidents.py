#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import inspect
import datetime

from sqlalchemy.sql import func
from ares.Lib.db import SqlTablesIncidents


def addQuestion(name, dsc, level, system, userName, hostname):
  """
  :dsc:
    Add a question to the defined system table. The default one here is the base table but this can be system specific.
    In this case the class should be find dyna,ically from the SqlAlchemy models
  """
  response = SqlTablesIncidents.IncQuestionsBase.query.filter_by(name=name).first()
  if response is None:
    runScriptResp = SqlTablesIncidents.IncQuestionsBase(name, dsc, level, userName, hostname)
    SqlTablesIncidents.db.session.add(runScriptResp)
    SqlTablesIncidents.db.session.commit()
    return {"status": True, "qId": runScriptResp.q_id, "dsc": "Question correctly added to %s" % system}

  return {"status": False, "qId": response.q_id, "dsc": "Question already defined for this system %s" % system}


def getQuestions(expr=None, numRecords=30):
  """
  :dsc:
    Returns the list of questions by creation date
  """
  records = {}
  baseQuery = SqlTablesIncidents.IncQuestionsBase.query.order_by(SqlTablesIncidents.IncQuestionsBase.lst_mod_dt.desc())
  if expr is not None:
    baseQuery = baseQuery.filter(SqlTablesIncidents.IncQuestionsBase.name.ilike(expr))
  for rec in baseQuery.limit(numRecords).all():
    records[rec.name] = rec.q_id
  return {"status": True, "records": records}


def addGroup(q_id, usr_name, hostname, system):
  """
  :dsc:
    Assumption here is a question can only belong to one group of answer.
    Indeed in this tree
      1) a question have multiple answer (one group of answers) and each answer point to one questions
      2) a group of answers can be linked to multiple questions
  """
  response = SqlTablesIncidents.IncQAGroupBase.query.filter_by(q_id=q_id).first()
  if response is None:
    maxGrpId = SqlTablesIncidents.db.session.query(func.max(SqlTablesIncidents.IncQAGroupBase.a_grp_id)).one()[0]
    if maxGrpId is None:
      maxGrpId = -1
    maxGrpId += 1
    runScriptResp = SqlTablesIncidents.IncQAGroupBase(q_id, maxGrpId, usr_name, hostname)
    SqlTablesIncidents.db.session.add(runScriptResp)
    SqlTablesIncidents.db.session.commit()
    return {"status": True, "dsc": "Group correctly added to %s" % system, 'gId': maxGrpId}

  return {"status": False, "dsc": "Group already available for this system %s" % system, 'gId': response.a_grp_id}


def addAnswer(gId, answer, team, targetQ, userName, hostname, system):
  """
  :dsc:
    Add an answer to the given question. From the UI it is not possible to define yet a question link or a priority.
    Those information should be added manually directly in the database.
  """
  response = SqlTablesIncidents.IncAnswersBase.query.filter_by(a_grp_id=gId, value=answer).first()
  if response is None:
    runScriptResp = SqlTablesIncidents.IncAnswersBase(answer, gId, 0, team, targetQ, 1, "auto", userName, system, hostname)
    SqlTablesIncidents.db.session.add(runScriptResp)
    SqlTablesIncidents.db.session.commit()
    return {"status": True, "dsc": "Answer correctly added to %s and question" % system}

  return {"status": False, "dsc": "Answer already available for this system %s and question" % system}


def addAdvice(gId, advice, userName, hostname):
  """
  :dsc:
    Advice table. This can be fully updated from the UI. Any users can update this table and add relevant information.
    If the advice helps on the incident resolution, the user can mention it and it will be reflected in the KPI
  """
  response = SqlTablesIncidents.IncAdvicesBase.query.filter_by(q_id=gId).first()
  if response is None:
    runScriptResp = SqlTablesIncidents.IncAdvicesBase(gId, advice, userName, hostname)
    SqlTablesIncidents.db.session.add(runScriptResp)
    SqlTablesIncidents.db.session.commit()
  else:
    response.text = advice
    response.usr_name = userName
    response.hostname = hostname
    SqlTablesIncidents.db.session.merge(response)
    SqlTablesIncidents.db.session.flush()
    SqlTablesIncidents.db.session.commit()
  return {"status": True, "dsc": "Advice correctly added"}


def addIncident(pry, attrs, usr_name, hostname):
  """
  :dsc:
    Add an new incident to the framework. This entry is used to keep track of the status changes during the decision tree.
    If no resolution is performed the full description is sent to the ,ain system to track the change and ask for a manual intervation
    from the relevant IT and support teams
  """
  runScriptResp = SqlTablesIncidents.IncRepo("", "", "", "", pry, "DIAGNOSIS", "[]", usr_name, hostname)
  SqlTablesIncidents.db.session.add(runScriptResp)
  SqlTablesIncidents.db.session.commit()
  runScriptResp = SqlTablesIncidents.IncScoreDtls(runScriptResp.inc_id, json.dumps(attrs), hostname)
  SqlTablesIncidents.db.session.add(runScriptResp)
  SqlTablesIncidents.db.session.commit()
  return {"status": True, "dsc": "Advice correctly added", 'incId': runScriptResp.inc_id}


def IncidentPry(incId, pry, label, dbase, qId, email):
  """
  :dsc:
    Update some information in the incident table in order to keep track of the priority and the questions answered in the
    decision tree.
  """
  response = SqlTablesIncidents.IncRepo.query.filter_by(inc_id=incId).first()
  if response is not None:
    qBreadCrumb = json.loads(response.tree)
    qBreadCrumb.append({"table": dbase, 'qId': qId, 'answer': label})
    response.lst_mod_dt = datetime.datetime.utcnow()
    response.pry += pry
    response.team = email
    response.last_q_id = qId
    response.tree = json.dumps(qBreadCrumb)
    SqlTablesIncidents.db.session.merge(response)
    SqlTablesIncidents.db.session.flush()
    SqlTablesIncidents.db.session.commit()
    return {"status": True}

  return {"status": False}


def IncidentOvrPry(incId, pry, usr_name, hostname):
  """

  """
  response = SqlTablesIncidents.IncPryOvr.query.filter_by(code=incId).first()
  if response is None:
    response = SqlTablesIncidents.IncPryOvr(incId, pry, usr_name, "", hostname)
    SqlTablesIncidents.db.session.add(response)
  else:
    response.pry = pry
    response.usr_name = usr_name
    response.hostname = hostname
    response.lst_mod_dt = datetime.datetime.utcnow()
  SqlTablesIncidents.db.session.commit()


def IncidentStatus(incId, nodeId, cmmt=None, status=None):
  """
  :dsc:
    Change some incident information and the status of the incident. This will help on the production of KPI to assess
    the efficiency of this model. With a good series of question and advices the framework should assist in the incident
    resolution. Those KPI will help finding reccurent issues and time spent on some branches in the decision tree.
  """
  response = SqlTablesIncidents.IncRepo.query.filter_by(inc_id=incId).first()
  if response is not None:
    response.lst_mod_dt = datetime.datetime.utcnow()
    if int(nodeId) != -1:
      response.last_q_id = nodeId
    if cmmt is not None:
      response.cmmt = cmmt
    if status is not None:
      response.status = status
      response.time_spent = response.lst_mod_dt - response.start_dt
    SqlTablesIncidents.db.session.merge(response)
    SqlTablesIncidents.db.session.flush()
    SqlTablesIncidents.db.session.commit()
    return {"status": True}

  return {"status": False}


def getQuestion(qId):
  """
  :dsc:
    Retrieve all the question information from the different tables. The question and its answers belong to the same system.
  """
  header = ["title", "advice", "answer", "db", "score", "team", "next_id"]
  records = {'id': qId, 'answers': {}}
  question = SqlTablesIncidents.IncQuestionsBase.query.filter_by(q_id=qId).first()
  if question is not None:
    records.update({'title': question.name, 'dsc': question.dsc, 'pry': question.lvl, 'details': question.details})
    advice = SqlTablesIncidents.IncAdvicesBase.query.filter_by(q_id=qId).first()
    if advice is not None:
      records['advice'] = advice.text
    groups = SqlTablesIncidents.IncQAGroupBase.query.filter_by(q_id=qId).first()
    if groups is not None:
      records['group_id'] = groups.a_grp_id
      for rec in SqlTablesIncidents.db.session.query(
          SqlTablesIncidents.IncAnswersBase.value, SqlTablesIncidents.IncAnswersBase.db_suffix, SqlTablesIncidents.IncAnswersBase.pry,
          SqlTablesIncidents.IncAnswersBase.q_dst_id, SqlTablesIncidents.IncAnswersBase.team) \
          .filter(SqlTablesIncidents.IncAnswersBase.valid == 1) \
          .filter(SqlTablesIncidents.IncAnswersBase.a_grp_id == groups.a_grp_id).all():
        records['answers'][rec[0]] = "%s|%s|%s|%s" % (rec[1], rec[2], rec[3], rec[4])
    else:
      records['group_id'] = None
  return records


def getSummary():
  """
  :dsc:
    Main query to produce the different KPI relative to this new framework
  """
  header, records = ['category', 'question', 'pry', 'count'], []
  for rec in SqlTablesIncidents.db.session.query(SqlTablesIncidents.IncRepo.status, SqlTablesIncidents.IncRepo.last_q_id,
                                                 SqlTablesIncidents.IncRepo.pry, func.count(SqlTablesIncidents.IncRepo.status))\
    .group_by(SqlTablesIncidents.IncRepo.status, SqlTablesIncidents.IncRepo.last_q_id).all():
    row = dict(zip(header, rec))
    if row['question'] is None:
      row['question'] = ""
    records.append(row)

  return records


def IncDelete(code):
  """
  :dsc:
    SQL function to remove an existing incident from the database.
    This will also remove the respective override if any
  """
  response = SqlTablesIncidents.IncRepo.query.filter_by(code=code).first()
  if response is None:
    SqlTablesIncidents.db.session.delete(response)
    SqlTablesIncidents.db.session.commit()
    responseOvr = SqlTablesIncidents.IncPryOvr.query.filter_by(code=code).first()
    if responseOvr is None:
      SqlTablesIncidents.db.session.delete(responseOvr)
      SqlTablesIncidents.db.session.commit()


def getIncident(incId):
  response = SqlTablesIncidents.IncRepo.query.filter_by(inc_id=incId).first()
  if response is not None:
    return {"pry": response.pry, "tree": json.loads(response.tree), "start_dt": response.start_dt, "team": response.team}

  return {}


def IncPryOvr(code, score):
  """
  :dsc:
    This SQL method will be in charge to apply an override to a wrong incident score.
    This will be done manually and some elements to detail the overrde might be added.
    The field comment might help in the future to put in place IA based on the history.
  """
  response = SqlTablesIncidents.IncRepo.query.filter_by(code=code).first()
  if response is not None:
    if response.pry == score:
      return {'status': False, "dsc": 'No change with the initial computed override'}

    responseOvr = SqlTablesIncidents.IncPryOvr.query.filter_by(code=code).first()
    if responseOvr is None:
      runScriptResp = SqlTablesIncidents.IncPryOvr(code, score)
      runScriptResp.db.session.add(runScriptResp)
      runScriptResp.db.session.commit()
      return {"status": True, 'dsc': "Override performed for %s" % code}

    return {"status": False, 'dsc': "Incident %s has already an override" % code }

  return {"status": False, 'dsc': "Incident code %s not found" % code}


def loadStatics(table, data):
  """

  """
  tableCls = None
  for name, obj in inspect.getmembers(SqlTablesIncidents):
    if inspect.isclass(obj):
      if obj.__tablename__ == table:
        tableCls = obj
        break

  if tableCls is not None:
    tableCls.query.delete()
    SqlTablesIncidents.db.session.commit()
    for name, val in data.items():
      newData = tableCls(name, val)
      SqlTablesIncidents.db.session.add(newData)
    SqlTablesIncidents.db.session.commit()


def getStatics(table):
  """

  """
  tableCls = None
  for name, obj in inspect.getmembers(SqlTablesIncidents):
    if inspect.isclass(obj):
      if obj.__tablename__ == table:
        tableCls = obj
        break

  if tableCls is not None:
    return dict([(rec.name, rec.score) for rec in tableCls.query.all()])

  return {}
