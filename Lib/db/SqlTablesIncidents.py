#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app import db
import datetime


class IncRepo(db.Model):
  """
  :dsc:
    Store the final message and create the description of the incident.
    Incident descriptions are standardised and this will allow the reuse the data by a machine in the same way that we use logs.
    This table will be updated at the end of the tree process. The only information that the users will be able to add is the cmmt.

    This framework will not replace any other system in charge of keeping track of the different interation within the team to solve this problem.
    The status of the incident should not be stored here. This framework is only dedicated to provide a dynamic score but also to try to diagnose it
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'incidents'

  inc_id = db.Column(db.Integer, primary_key=True, nullable=False)
  ticket = db.Column(db.Text) # Produced from the system in charge of storing the incident history
  dsc = db.Column(db.Text)  # Created automatically from the tree
  cmmt = db.Column(db.Text)  # Added by the user to detail the issue (to allow the creation of extra branches)
  team = db.Column(db.Text, nullable=False)  # The team in charge of the incident from the question
  start_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  usr_name = db.Column(db.String(120), nullable=False)  # Should be retrieve from the SSO in the future
  pry = db.Column(db.Integer, nullable=False)# Should be the result of the scoring algorithm
  status = db.Column(db.Text)
  tree = db.Column(db.Text)
  last_q_id = db.Column(db.Integer, nullable=True)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  time_spent = db.Column(db.Interval, nullable=True)

  def __init__(self, ticket, dsc, cmmt, team, pry, status, tree, usr_name, hostname):
    self.ticket, self.dsc, self.cmmt, self.team, self.pry, self.status, self.tree, self.usr_name, self.hostname = ticket, dsc, cmmt, team, pry, status, tree, usr_name, hostname


class IncScoreDtls(db.Model):
  """
  :dsc:
    In this table will be stored the details of the scoring algorithm for a incident.
    The column attrs will store the details in a json format. In inc_id is the primary key in the incident table.
    This will be created when the button "start diagnosis" is clicked
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'incidents_score_info'

  score_id = db.Column(db.Integer, primary_key=True, nullable=False)
  inc_id = db.Column(db.Integer)
  attrs = db.Column(db.Text)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)

  def __init__(self, inc_id, attrs, hostname):
    self.inc_id, self.attrs, self.hostname = inc_id, attrs, hostname


class IncPryOvr(db.Model):
  """
  :dsc:
    Table to allow the end user to override the automated score allocated to an incident.
    This action will also help on reviewing constantly the incidents priorities algorithm by check those overrides.

    Any answer can have a score in order to help on refining the algorithm and get something in line with the users expectations.
    The default priority of an answer is 0
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'incidents_pry_ovr'

  inc_id = db.Column(db.Integer, primary_key=True, nullable=False)
  code = db.Column(db.Text)
  pry = db.Column(db.Integer, nullable=False)# Should be the result of the scoring algorithm
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  usr_name = db.Column(db.String(120), nullable=False) # Should be retrieve from the SSO in the future
  cmmt = db.Column(db.Text)
  hostname = db.Column(db.String(120), nullable=False)

  def __init__(self, code, pry, usr_name, cmmt, hostname):
    self.code, self.pry, self.usr_name, self.cmmt, self.hostname = code, pry, usr_name, cmmt, hostname

# --------------------------------------------------------------------
#                       IA Algorithm
#
# This should be based on a decision tree to get a predictive model
# This decision tree should then be updated by the learning https://en.wikipedia.org/wiki/Decision_tree_learning
class IncQuestionsBase(db.Model):
  """
  :dsc:
    Main table of the incident diagnosis. This will store the list of questions. In the same table are mixed questions of different level.
    A level will correspond to a tree. Basically the level 0 is the basic level for a incident. Once the incident is defined by a user, it will go the the tree of the relevant team.
    Each team will then have a level and each node will ensure the necessary steps are done to pass to the next team.
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'tree_questions_base'

  q_id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.Text, nullable=False)
  dsc = db.Column(db.Text, nullable=False)
  lvl = db.Column(db.Integer)
  details = db.Column(db.Boolean, default=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  usr_name = db.Column(db.String(120), nullable=False)  # Should be retrieve from the SSO in the future
  hostname = db.Column(db.String(120), nullable=False)

  def __init__(self, name, dsc, lvl, usr_name, hostname):
    self.name, self.dsc, self.lvl, self.usr_name, self.hostname = name, dsc, lvl, usr_name, hostname


class IncSplitDb(db.Model):
  """
  :dsc:
    Table in charge of splitting the questions and the answers. This will allow a better split of the different data (even in a traditional SQL model)
    This will allow the creation of small tables and potentially the creation of different trees
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'tree_split_db'

  split_id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.Text, nullable=False)
  db_suffix = db.Column(db.Text, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  usr_name = db.Column(db.String(120), nullable=False)  # Should be retrieve from the SSO in the future

  def __init__(self, name, db_suffix, usr_name):
    self.name, self.db_suffix, self.usr_name = name, db_suffix, usr_name


class IncAdvicesBase(db.Model):
  """
  :dsc:
    This table will allow the display of events in order to try to solve the problem in an automated manner.
    This table can be filled by advanced users but also by the different development teams
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'tree_advices_base'

  c_id = db.Column(db.Integer, primary_key=True, nullable=False)
  q_id = db.Column(db.Integer, nullable=False)
  text = db.Column(db.Text)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  usr_name = db.Column(db.String(120), nullable=False)  # Should be retrieve from the SSO in the future
  hostname = db.Column(db.String(120), nullable=False)

  def __init__(self, q_id, text, usr_name, hostname):
    self.q_id, self.text, self.usr_name, self.hostname = q_id, text, usr_name, hostname


class IncQAGroupBase(db.Model):
  """
  :dsc:
    This table will link the question to a dedicated gtoup of answer.
    So basically a group of answer can be linked to multiple questions
    This will allow the tree to link two branches and to avoid to duplicate the same series of questions
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'tree_question_group_base'

  g_id = db.Column(db.Integer, primary_key=True, nullable=False)
  q_id = db.Column(db.Integer, nullable=False)
  a_grp_id = db.Column(db.Integer, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  usr_name = db.Column(db.String(120), nullable=False)  # Should be retrieve from the SSO in the future
  hostname = db.Column(db.String(120), nullable=False)

  def __init__(self, q_id, a_grp_id, usr_name, hostname):
    self.q_id, self.a_grp_id, self.usr_name, self.hostname = q_id, a_grp_id, usr_name, hostname


class IncAnswersBase(db.Model):
  """
  :dsc:
    This table will store all the different groups of answers.
    Each answer will get the following question id and the database suffix in case of split of questions (to avoid too important tables)
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'tree_answer_base'

  a_id = db.Column(db.Integer, primary_key=True, nullable=False)
  value = db.Column(db.Text)
  db_suffix = db.Column(db.Text) # If the db is still in the base framework
  a_grp_id = db.Column(db.Integer, nullable=False)
  pry = db.Column(db.Integer, nullable=False)
  team = db.Column(db.Text, nullable=False) # The team in charge of the incident from the question
  q_dst_id = db.Column(db.Integer, nullable=True)
  valid = db.Column(db.Integer)
  ares_usr_nam = db.Column(db.Text, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  usr_name = db.Column(db.String(120), nullable=False)  # Should be retrieve from the SSO in the future
  hostname = db.Column(db.String(120), nullable=False)

  def __init__(self, value, a_grp_id, pry, team, q_dst_id, valid, ares_usr_nam, usr_name, db_suffix, hostname):
    self.value, self.a_grp_id, self.pry, self.team, self.q_dst_id = value, a_grp_id, pry, team, q_dst_id
    self.valid, self.ares_usr_nam, self.usr_name, self.db_suffix = valid, ares_usr_nam, usr_name, db_suffix
    self.hostname = hostname


# --------------------------------------------------------------------
#                       Scoring containers
#
# All those tables will be used in the process on allocating a score to the incident
class IncUserLevel(db.Model):
  """
  :dsc:
    Table in charge of defining the correct level for a team. This will allow the construct of multiple dimensions in case of isse.
    For example a user level 0 will not see the branches level 1 of the diagnosis as it will not be able to perform the actions.
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'tree_user_level'

  lvl_id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.Text)
  score = db.Column(db.Integer, nullable=False)

  def __init__(self, name, score):
    self.name, self.score = name, score


class IncProcesses(db.Model):
  """
  :dsc:

  """
  __bind_key__ = 'incidents'
  __tablename__ = 'processes'

  proc_id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.Text)
  score = db.Column(db.Integer, nullable=False)

  def __init__(self, name, score):
    self.name, self.score = name, score


class IncPerimeter(db.Model):
  """
  :dsc:

  """
  __bind_key__ = 'incidents'
  __tablename__ = 'perimeter'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.Text)
  score = db.Column(db.Integer, nullable=False)

  def __init__(self, name, score):
    self.name, self.score = name, score


class IncBussImpact(db.Model):
  """
  :dsc:
    Table in charge of storing the different
  """
  __bind_key__ = 'incidents'
  __tablename__ = 'bus_impact'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.Text)
  score = db.Column(db.Integer, nullable=False)

  def __init__(self, name, score):
    self.name, self.score = name, score


class IncRepImpact(db.Model):
  """
  :dsc:

  """
  __bind_key__ = 'incidents'
  __tablename__ = 'rep_impact'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.Text)
  score = db.Column(db.Integer, nullable=False)

  def __init__(self, name, score):
    self.name, self.score = name, score


class IncUrgency(db.Model):
  """
  :dsc:

  """
  __bind_key__ = 'incidents'
  __tablename__ = 'urgency'

  id = db.Column(db.Integer, primary_key=True, nullable=False)
  name = db.Column(db.Text)
  score = db.Column(db.Integer, nullable=False)

  def __init__(self, name, score):
    self.name, self.score = name, score
