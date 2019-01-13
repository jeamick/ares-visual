#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from app import db
import datetime


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO THE QUESTIONS
#
class Questions(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question'

  issue_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  issue_title = db.Column(db.String(120), nullable=False, unique=True)
  issue_content = db.Column(db.Text, nullable=False)
  type = db.Column(db.Text, nullable=False)
  status = db.Column(db.String(50), nullable=False)
  urgent = db.Column(db.Integer, nullable=False) # 0 = N, 1 = Y
  group = db.Column(db.String(120), nullable=False) # Default public
  usr_name = db.Column(db.String(120), nullable=False)
  interest = db.Column(db.Integer, default=0)
  best_answer_id = db.Column(db.Integer, default=-1) #-1
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False) # This is mandatory when data can come from outside

  def __init__(self, issue_title, issue_content, type, status, urgent, group, usr_name, interest, hostname):
    self.issue_title, self.issue_content, self.type, self.status = issue_title, issue_content, type, status
    self.usr_name, self.hostname, self.interest, self.urgent, self.group = usr_name, hostname, interest, urgent, group


class QuestionsDetail(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_detail'

  question_extra_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  issue_id = db.Column(db.Integer, nullable=False)
  content = db.Column(db.String(120), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, issue_id, content, usr_name, hostname):
    self.issue_id, self.content, self.usr_name, self.hostname = issue_id, content, usr_name, hostname


class QuestionsViews(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_views'

  view_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  issue_id = db.Column(db.Integer)
  value = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, issue_id, value, usr_name):
    self.issue_id, self.value, self.usr_name = issue_id, value, usr_name


class QuestionsAlert(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_alert'

  alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  issue_id = db.Column(db.Integer)
  status = db.Column(db.Integer, default=1) # 1 = Active
  moderator = db.Column(db.String(120), default='') # Should be mentioned when status is 0
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, issue_id, usr_name):
    self.issue_id, self.usr_name = issue_id, usr_name


class QuestionsInterest(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_interest'

  interest_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  issue_id = db.Column(db.Integer)
  interest_value = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, issue_id, interest_value, usr_name, hostname):
    self.issue_id, self.interest_value, self.usr_name, self.hostname = issue_id, interest_value, usr_name, hostname


class QuestionsTags(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_tags'

  question_tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  tag_name = db.Column(db.Text)
  issue_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, issue_id, tag_name, usr_name):
    self.tag_name, self.issue_id, self.usr_name = tag_name, issue_id, usr_name


class QuestionsFollow(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_follow'

  follow_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  issue_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False) # This is mandatory when data can come from outside

  def __init__(self, issue_id, usr_name, hostname):
    self.issue_id, self.usr_name, self.hostname = issue_id, usr_name, hostname


class QuestionsAnswer(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_answer'

  answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  issue_id = db.Column(db.Integer, nullable=False)
  answer_content = db.Column(db.Text, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  status = db.Column(db.String(50), nullable=False) # Best answer, Removed...
  group_cod = db.Column(db.String(50), nullable=False)
  interest = db.Column(db.Integer, default=0)
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, issue_id, answer_content, usr_name, status, group_cod, interest, hostname):
    self.issue_id, self.answer_content, self.usr_name, self.status = issue_id, answer_content, usr_name, status
    self.hostname, self.group_cod, self.interest = hostname, group_cod, interest


class QuestionsAnswerInterest(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_anwser_interest'

  interest_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  answer_id = db.Column(db.Integer)
  value = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, answer_id, value, usr_name, hostname):
    self.answer_id, self.value, self.usr_name, self.hostname = answer_id, value, usr_name, hostname


class QuestionsAnswerMail(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_answer_mail'

  answer_mail_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  answer_id = db.Column(db.Integer)
  email_group = db.Column(db.String(120), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, answer_id, email_group, usr_name, hostname):
    self.answer_id, self.email_group, self.usr_name, self.hostname = answer_id, email_group, usr_name, hostname


class QuestionsAnswerExra(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_answer_extra'

  answer_extra_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  answer_id = db.Column(db.Integer, nullable=False)
  extra_content = db.Column(db.String(120), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, answer_id, extra_content, usr_name, hostname):
    self.answer_id, self.extra_content, self.usr_name, self.hostname = answer_id, extra_content, usr_name, hostname


class QuestionsLinkExt(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_link_external'

  link_ext_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  issue_id = db.Column(db.Integer)
  system_code = db.Column(db.String(10), nullable=False)
  system_id = db.Column(db.Text, nullable=False)
  title = db.Column(db.Text, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, issue_id, system_code, system_id, title, usr_name, hostname):
    self.issue_id, self.system_code, self.system_id, self.title, self.usr_name, self.hostname = issue_id, system_code, system_id, title, usr_name, hostname


class QuestionsLinkTopic(db.Model):
  __bind_key__ = 'questions'
  __tablename__ = 'question_link_topic'

  link_topic_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  issue_id = db.Column(db.Integer)
  related_question_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, issue_id, related_question_id, usr_name, hostname):
    self.issue_id, self.related_question_id, self.usr_name, self.hostname = issue_id, related_question_id, usr_name, hostname


