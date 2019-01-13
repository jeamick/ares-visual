#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

from ares.Lib.db import SqlTableQuestions, SqlTableAres
from flask_login import current_user
from sqlalchemy import func
from flask import Markup


def newQuestion(title, message, type, urgency, group, remote_addr):
  runScriptResp = SqlTableQuestions.Questions(issue_title=title, issue_content=message, type=type, status='OPEN', urgent=urgency,
                                          group=group, usr_name=current_user.email, interest=0, hostname=remote_addr)
  SqlTableQuestions.db.session.add(runScriptResp)
  SqlTableQuestions.db.session.commit()
  try:
    newView = SqlTableQuestions.QuestionsViews(issue_id=runScriptResp.issue_id, value=1, usr_name=current_user.email)
    SqlTableQuestions.db.session.add(newView)
    SqlTableQuestions.db.session.commit()
    return {"status": True, 'id': runScriptResp.issue_id }
  except Exception as err:
    return {"status": False, 'dsc': Markup.escape(str(err))}

def addAnswer(issue_id, message, remote_addr):
  runScriptResp = SqlTableQuestions.QuestionsAnswer(issue_id=issue_id, answer_content=message, status='VALID', group_cod='PUBLIC', interest=0, usr_name=current_user.email, hostname=remote_addr)
  SqlTableQuestions.db.session.add(runScriptResp)
  try:
    SqlTableQuestions.db.session.commit()
    answerInterest = SqlTableQuestions.QuestionsAnswerInterest(answer_id=runScriptResp.answer_id, value=1, usr_name=current_user.email, hostname=remote_addr)
    SqlTableQuestions.db.session.add(answerInterest)
    SqlTableQuestions.db.session.commit()
    return True
  except:
    return False

def addTag(issue_id, tag):
  response = SqlTableQuestions.QuestionsTags.query.filter_by(issue_id=issue_id, tag_name=tag).first()
  if response is None:
    try:
      response = SqlTableQuestions.QuestionsTags(issue_id=issue_id, tag_name=tag, usr_name=current_user.email)
      SqlTableQuestions.db.session.add(response)
      SqlTableQuestions.db.session.commit()
      return {'status': True}
    except Exception as err:
      return {'status': False, 'dsc': Markup.escape(str(err))}
  else:
    return {'status': False, 'dsc': 'Tag already exists'}

def remTag(issue_id, tag):
  response = SqlTableQuestions.QuestionsTags.query.filter_by(issue_id=issue_id, tag_name=tag).first()
  if response is not None:
    try:
      SqlTableQuestions.db.session.delete(response)
      SqlTableQuestions.db.session.commit()
      return {'status': True}
    except Exception as err:
      return {'status': False, 'dsc': Markup.escape(str(err))}
  else:
    return {'status': False, 'dsc': 'Tag does not exist'}

def getQuestionStats():
  questions = SqlTableQuestions.Questions.query.count()
  answers = SqlTableQuestions.QuestionsAnswer.query.count()
  answers += SqlTableQuestions.QuestionsAnswerExra.query.count()
  users = SqlTableAres.User.query.count()
  # Contributors
  contributors = SqlTableQuestions.Questions.query.group_by(SqlTableQuestions.Questions.usr_name).count()
  return {"contributors": contributors, 'members': users, 'questions': questions, 'answers': answers}

def getQuestion(issueId):
  rec = SqlTableQuestions.Questions.query.filter_by(issue_id=issueId).first()
  views = SqlTableQuestions.QuestionsViews.query.filter_by(issue_id=issueId, usr_name=current_user.email).first()
  if views is None:
    views = SqlTableQuestions.QuestionsViews(issue_id=issueId, value=1, usr_name=current_user.email)
    SqlTableQuestions.db.session.add(views)
    SqlTableQuestions.db.session.commit()
  lastAnswer = ''
  recAnswer = SqlTableQuestions.QuestionsAnswer.query.filter_by(issue_id=issueId).order_by(SqlTableQuestions.QuestionsAnswer.lst_mod_dt.desc()).first()
  if recAnswer is not None:
    lastAnswer = recAnswer.lst_mod_dt.strftime("%Y-%m-%d %H:%M:%S")
  relatedTopics = []
  for recLinks in SqlTableQuestions.db.session.query(SqlTableQuestions.QuestionsLinkTopic.related_question_id, SqlTableQuestions.Questions.issue_title, func.count(SqlTableQuestions.QuestionsAnswer.answer_id)) \
      .filter(SqlTableQuestions.QuestionsLinkTopic.issue_id == issueId) \
      .filter(SqlTableQuestions.QuestionsLinkTopic.related_question_id == SqlTableQuestions.Questions.issue_id) \
      .filter(SqlTableQuestions.QuestionsLinkTopic.related_question_id == SqlTableQuestions.QuestionsAnswer.issue_id)\
      .group_by(SqlTableQuestions.QuestionsLinkTopic.related_question_id, SqlTableQuestions.Questions.issue_title).all():
      background = "white"
      if recLinks[2] > 10:
        background = '#00FF00'
      elif recLinks[2] > 4:
        background = '#FFFF00'
      relatedTopics.append( {"id": recLinks[0], "title": Markup.escape(recLinks[1]), "value": Markup.escape(recLinks[2]), 'url': '/questions/details/%s' % recLinks[0], 'background': background, 'color': 'black'})
  extLinks = []
  for recExtLinks in SqlTableQuestions.QuestionsLinkExt.query.filter_by(issue_id=issueId).all():
    if recExtLinks.system_code == "WEB":
      extLinks.append({'url': recExtLinks.system_id, 'title': Markup.escape(recExtLinks.title) if recExtLinks.title else recExtLinks.system_code})
    else:
      extLinks.append( {'url': '', 'title': Markup.escape(recExtLinks.title) if recExtLinks.title else "%s-%s" % (recExtLinks.system_code, recExtLinks.system_id)} )

  countViews = SqlTableQuestions.db.session.query(func.sum(SqlTableQuestions.QuestionsViews.value)).filter_by(issue_id=issueId).first()
  comms = []
  for comm in SqlTableQuestions.QuestionsDetail.query.filter_by(issue_id=issueId).all():
    comms.append( '%s, by <span style="border-radius:5px;background:#293846;padding:2px 5px;color:white;font-weight:bold">%s</span> - %s ' % (Markup.escape(comm.content), comm.usr_name, comm.lst_mod_dt) )
  return {'id': rec.issue_id, 'title': Markup.escape(rec.issue_title), 'comms': comms, 'content': Markup.escape(rec.issue_content), 'view': countViews[0], 'last_answer': lastAnswer, 'ext_links': extLinks,
          'date': rec.lst_mod_dt.strftime("%Y-%m-%d %H:%M:%S"), 'author': rec.usr_name, 'status': rec.status, 'related_topics': relatedTopics}

def getAnswers(issueId):
  records, answerIds = {}, set()
  for rec in SqlTableQuestions.QuestionsAnswer.query.filter_by(issue_id=issueId).all():
    records[rec.answer_id] = {'borderColor': 'white', 'color': 'black', 'id': rec.answer_id, "interest": 0, "answer": rec.answer_content.replace('<script>', ''), "author": rec.usr_name, "status": rec.status,
                              'lst_mod_dt': rec.lst_mod_dt.strftime("%Y-%m-%d %H:%M:%S"), 'xtra': []}
    answerIds.add( rec.answer_id )
  for rec in SqlTableQuestions.db.session.query(SqlTableQuestions.QuestionsAnswerInterest.answer_id, func.sum(SqlTableQuestions.QuestionsAnswerInterest.value))\
    .filter(SqlTableQuestions.QuestionsAnswerInterest.answer_id.in_( list(answerIds)))\
    .group_by(SqlTableQuestions.QuestionsAnswerInterest.answer_id).all():
    records[rec[0]]["interest"] = rec[1]
  for rec in SqlTableQuestions.QuestionsAnswerExra.query.filter(SqlTableQuestions.QuestionsAnswerExra.answer_id.in_( list(answerIds))).all():
    records[rec.answer_id]['xtra'].append( "%s, by %s, %s" % (Markup.escape(rec.extra_content), rec.usr_name, rec.lst_mod_dt.strftime("%Y-%m-%d %H:%M:%S")) )
  results = sorted(list(records.values()), key=lambda k: k['interest'])[::-1]
  if records:
    results[0]['borderColor'] = '#f9fcff'
  return results

def getRecentIssues(count, date=None, questionIds=None, urgentFlag=None):
  records = []
  questions = SqlTableQuestions.db.session.query(SqlTableQuestions.Questions, func.sum(SqlTableQuestions.QuestionsViews.value),
                                             func.count(func.distinct(SqlTableQuestions.QuestionsAnswer.answer_id)),
                                             func.sum(func.distinct(SqlTableQuestions.QuestionsInterest.interest_value))) \
    .filter(SqlTableQuestions.Questions.issue_id == SqlTableQuestions.QuestionsViews.issue_id) \
    .outerjoin(SqlTableQuestions.QuestionsAnswer, SqlTableQuestions.Questions.issue_id == SqlTableQuestions.QuestionsAnswer.issue_id) \
    .outerjoin(SqlTableQuestions.QuestionsInterest, SqlTableQuestions.Questions.issue_id == SqlTableQuestions.QuestionsInterest.issue_id) \
    .group_by(SqlTableQuestions.Questions) \
    .order_by(SqlTableQuestions.Questions.lst_mod_dt.desc())

  if date is not None:
    questions = questions.filter(SqlTableQuestions.Questions.clc_dt == date)
  if urgentFlag is not None:
    questions = questions.filter(SqlTableQuestions.Questions.urgent == urgentFlag)
  if questionIds is not None:
    questions = questions.filter(SqlTableQuestions.Questions.issue_id.in_(questionIds) )

  for rec, views, answerCount, interest in questions.limit(count).all():
    interest = 0 if interest is None else interest
    records.append( {'id': rec.issue_id, 'title': Markup.escape(rec.issue_title), 'content': Markup.escape(rec.issue_content), 'answers': answerCount, 'views': views,
                     'date': rec.lst_mod_dt.strftime("%Y-%m-%d %H:%M:%S"), 'author': rec.usr_name, 'status': rec.status, 'interest': interest} )
  return records

def getTags(issueId):
  records = []
  for rec in SqlTableQuestions.QuestionsTags.query.filter_by(issue_id=issueId).all():
    records.append( {"value": rec.tag_name })
  return records

def getIssuesByTag(tag):
  records = []
  issuesList = [issue.issue_id for issue in SqlTableQuestions.QuestionsTags.query.filter_by(tag_name=tag).all()]
  for issue in SqlTableQuestions.Questions.query.filter(SqlTableQuestions.Questions.issue_id.in_(tuple(issuesList))):
    interest = SqlTableQuestions.QuestionsInterest.query.filter_by(issue_id=issue.issue_id).first()
    interest_value = interest.interest_value if interest else 0
    records.append({'issue_id': issue.issue_id, 'issue_title': issue.issue_title, 'interest': interest_value, 'lst_mod_dt': issue.lst_mod_dt,
                    'usr_name': issue.usr_name, 'status': issue.status})
  return records

def getRecentUpdatedIssues(count, urgentFlag=None):
  records, questionId, tmpResult = [], [], {}
  for rec in SqlTableQuestions.QuestionsAnswer.query.order_by(SqlTableQuestions.QuestionsAnswer.lst_mod_dt.desc()).limit(count).all():
    if rec.issue_id not in questionId: # Need to keep the order here
      questionId.append( rec.issue_id )
  return getRecentIssues(count, questionIds=questionId, urgentFlag=urgentFlag)

def getInterest(issueId):
  res = 0
  for rec in SqlTableQuestions.QuestionsInterest.query.filter_by(issue_id=issueId).all():
    res += rec.interest_value
  return res

def getFollow(issueId):
  return SqlTableQuestions.QuestionsFollow.query.filter_by(issue_id=issueId).count()

def addInterest(issueId, value, hostname):
  if abs(value) == 1:
    response = SqlTableQuestions.QuestionsInterest.query.filter_by(issue_id=issueId, usr_name=current_user.email).first()
    if response is None:
      response = SqlTableQuestions.QuestionsInterest(issue_id=issueId, usr_name=current_user.email, interest_value=value, hostname=hostname)
      SqlTableQuestions.db.session.add(response)
      try:

        SqlTableQuestions.db.session.commit()
        return True
      except:
        return False
  else:
    return False

def addAnswerInterest(answerId, value, hostname):
  if abs(value) == 1:
    response = SqlTableQuestions.QuestionsAnswerInterest.query.filter_by(answer_id=answerId, usr_name=current_user.email).first()
    if response is None:
      response = SqlTableQuestions.QuestionsAnswerInterest(answer_id=answerId, usr_name=current_user.email, value=value, hostname=hostname)
      SqlTableQuestions.db.session.add(response)
      try:

        SqlTableQuestions.db.session.commit()
        return {"status": True}
      except Exception as err:
        return {"status": False, 'dsc': Markup.escape(str(err))}
  else:
    return {"status": False, 'dsc': 'You have already voted'}

def addFollow(issueId, hostname):
  response = SqlTableQuestions.QuestionsFollow.query.filter_by(issue_id=issueId, usr_name=current_user.email).first()
  if response is None:
    response = SqlTableQuestions.QuestionsFollow(issue_id=issueId, usr_name=current_user.email, hostname=hostname)
    SqlTableQuestions.db.session.add(response)
    try:
      SqlTableQuestions.db.session.commit()
      return True
    except:
      return False

def addDetail(issueId, content, hostname):
  response = SqlTableQuestions.QuestionsDetail(issue_id=issueId, content=content, usr_name=current_user.email, hostname=hostname)
  SqlTableQuestions.db.session.add(response)
  try:
    SqlTableQuestions.db.session.commit()
    return {"status": True }
  except:
    return {"status": False }

def addAlert(qId):
  response = SqlTableQuestions.QuestionsAlert(issue_id=qId, usr_name=current_user.email)
  SqlTableQuestions.db.session.add(response)
  try:
    SqlTableQuestions.db.session.commit()
    return {"status": True}
  except:
    return {"status": False}

def hasAlert(qId):
  response = SqlTableQuestions.QuestionsAlert.query.filter_by(issue_id=qId).first()
  return False if response is None else True

def addTopicLinks(qId, relatedQId, hostname):
  response = SqlTableQuestions.QuestionsLinkTopic.query.filter_by(issue_id=qId, related_question_id=relatedQId).first()
  if response is None:
    response = SqlTableQuestions.QuestionsLinkTopic(issue_id=qId, related_question_id=relatedQId,  usr_name=current_user.email, hostname=hostname)
    SqlTableQuestions.db.session.add(response)
    response = SqlTableQuestions.QuestionsLinkTopic(issue_id=relatedQId, related_question_id=qId, usr_name=current_user.email, hostname=hostname)
    SqlTableQuestions.db.session.add(response)
    try:
      SqlTableQuestions.db.session.commit()
      return {'status': True}
    except Exception as err:
      return {'status': False, 'dsc': Markup.escape(str(err))}
  else:
    return {'status': False, 'dsc': 'Link already available'}

def addExtLink(issue_id, systemCode, systemId, hostname):
  response = SqlTableQuestions.QuestionsLinkExt.query.filter_by(issue_id=issue_id, system_code=systemCode, system_id=systemId).first()
  if response is None:
    response = SqlTableQuestions.QuestionsLinkExt(issue_id=issue_id, system_code=systemCode, system_id=systemId, title="", usr_name=current_user.email, hostname=hostname)
    SqlTableQuestions.db.session.add(response)
    try:
      SqlTableQuestions.db.session.commit()
      return {'status': True}
    except Exception as err:
      return {'status': False, 'dsc': Markup.escape(str(err))}
  else:
    return {'status': False, 'dsc': 'Link already available'}

def addComms(issueId, answerId, message, hostname):
  response = SqlTableQuestions.QuestionsAnswerExra(answer_id=answerId, extra_content=message, usr_name=current_user.email, hostname=hostname)
  SqlTableQuestions.db.session.add(response)
  try:
    SqlTableQuestions.db.session.commit()
    return True
  except:
    return False

def addFeedback(title, content, system, hostname):
  response = SqlTableAres.Feedback(title=title, content=content, status=1, system=system, usr_name=current_user.email, hostname=hostname)
  SqlTableQuestions.db.session.add(response)
  try:
    SqlTableQuestions.db.session.commit()
    response = SqlTableAres.FeedbackSupport(feedback_id=response.feedback_id, usr_name=current_user.email, hostname=hostname)
    SqlTableQuestions.db.session.add(response)
    SqlTableQuestions.db.session.commit()
    return True
  except:
    return False

def addIdeaSupport(ideaId, hostname):
  response = SqlTableAres.FeedbackSupport.query.filter_by(feedback_id=ideaId, usr_name=current_user.email).first()
  if response is None:
    response = SqlTableAres.FeedbackSupport(feedback_id=ideaId, usr_name=current_user.email, hostname=hostname)
    SqlTableQuestions.db.session.add(response)
    try:
      SqlTableQuestions.db.session.commit()
      return {"status": True}
    except Exception as err:
      return {"status": False}
  else:
    return {"status": False}

def getFeedbacks():
  ideas = {}
  for rec in SqlTableAres.Feedback.query.order_by(SqlTableAres.Feedback.lst_mod_dt.desc()).all():
    ideas[rec.feedback_id] = {'id': rec.feedback_id, 'count': 0, 'title': Markup.escape(rec.title), 'content': Markup.escape(rec.content), 'date': rec.lst_mod_dt.strftime("%Y-%m-%d %H:%M:%S"), 'author': rec.usr_name, 'status': rec.status}

  for rec in SqlTableAres.FeedbackSupport.query.all():
    ideas[rec.feedback_id]['count'] += 1
  return sorted(list(ideas.values()), key=lambda k: k['date'])[::-1]