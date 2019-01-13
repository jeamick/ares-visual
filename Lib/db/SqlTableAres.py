#!/usr/bin/env python
# -*- coding: utf-8 -*-


from app import db
from flask_login import UserMixin
import datetime
import hashlib
from ares.utils import AresSiphash


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO THE USER SETTINGS
#
class User(db.Model, UserMixin):
  uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)

  def __init__(self, email, password):
    self.email = email
    self.password = hashlib.sha256(bytes(password.encode('utf-8'))).hexdigest()

  def __repr__(self):
    return '<User %r>' % self.email

  def get_id(self):
    """ """
    return self.email


class UserDetails(db.Model):
  __tablename__ = 'user_details'

  uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  surname = db.Column(db.String(50), unique=True, nullable=False)
  first_name = db.Column(db.String(50), unique=True, nullable=False)
  user_id = db.Column(db.String(50), unique=True, nullable=False)
  alias = db.Column(db.String(50), unique=True, nullable=False)
  picture = db.Column(db.String(50), unique=True, nullable=False)
  is_active = db.Column(db.Integer, nullable=False, default=1)  # The environment is valid
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, email, password, alias, picture):
    self.email, self.password, self.alias, self.picture = email, password, alias, picture


class UserAttribute(db.Model):
  __tablename__ = 'user_attributes'

  attr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  usr_name = db.Column(db.String(120), nullable=False)
  attr_code = db.Column(db.String(120), nullable=False)
  attr_value = db.Column(db.String(120), nullable=False)
  group_id = db.Column(db.Integer)
  source_type = db.Column(db.String(30))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, usr_name, attr_code, attr_value, group_id=None, source_type=None):
    self.usr_name = usr_name
    self.attr_code = attr_code
    self.attr_value = attr_value
    self.group_id = group_id
    self.source_type = source_type


class UserLibPaths(db.Model):
  __tablename__ = 'user_lib_path'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  lib_path = db.Column(db.String(2000), nullable=False)
  usr_nam = db.Column(db.String(120), nullable=False)

  def __init__(self, lib_path, usr_nam):
    self.usr_nam = usr_nam
    self.lib_path = lib_path


class UserDataSourcePmt(db.Model):
  __tablename__ = 'user_datasource_pmt'

  src_entry = db.Column(db.Integer, primary_key=True, autoincrement=True)
  src_code = db.Column(db.String(20), nullable=False)
  pmt_user = db.Column(db.String(120), nullable=False)
  pmt_env = db.Column(db.String(20), nullable=False)
  pmt_code = db.Column(db.String(120), nullable=False)
  pmt_val = db.Column(db.String(120), nullable=False)
  salt = db.Column(db.Integer)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, src_code, pmt_user, pmt_env, pmt_code, pmt_val, salt):
    self.src_code = src_code
    self.pmt_user = pmt_user
    self.pmt_env = pmt_env
    self.pmt_code = pmt_code
    self.pmt_val = pmt_val
    self.salt = salt


class UserTagNotes(db.Model):
  __tablename__ = 'user_tag_note'

  tag_note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  tag_name = db.Column(db.String(30), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  note = db.Column(db.Text, nullable=False)
  visible = db.Column(db.Integer, nullable=False) # 1 is visible
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, tag_name, usr_name, note, visible=1):
    self.tag_name = tag_name
    self.usr_name = usr_name
    self.note = note
    self.visible = visible


class UserEnvFollow(db.Model):
  __tablename__ = 'user_env_follow'

  follow_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  env_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)

  def __init__(self, env_id, usr_name):
    self.env_id = env_id
    self.usr_name = usr_name


class UserScriptsFavourites(db.Model):
  __tablename__ = 'favourites'

  fav_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  script_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)

  def __init__(self, script_id, usr_name):
    self.script_id = script_id
    self.usr_name = usr_name


class UserScriptsLikes(db.Model):
  __tablename__ = 'user_likes'

  like_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  script_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, script_id, usr_name):
    self.script_id = script_id
    self.usr_name = usr_name


class UserKeysStore(db.Model):
  __tablename__ = 'user_keys_store'

  key_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  key = db.Column(db.Text, nullable=False)
  key_attr = db.Column(db.Text, nullable=False) # Just in case further details are needed
  group_name = db.Column(db.String(50), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, key, group_name, usr_name):
    self.key = key
    self.group_name = group_name
    self.usr_name = usr_name


class UserMails(db.Model):
  __tablename__ = 'user_mails'

  mail_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  run_id = db.Column(db.Integer)
  script_id = db.Column(db.Integer)
  message_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  subject = db.Column(db.String(120), nullable=False)
  content = db.Column(db.Text, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, usr_name, subject, mail_category, run_id, script_id, content, message_id=-1):
    self.usr_name, self.run_id, self.message_id = usr_name, run_id, message_id
    self.subject, self.script_id = subject, script_id
    self.content, self.mail_category = content, mail_category
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO GROUP PROPERTIES
# Default Groups
# > Public
# > user email
# > Team email ( After validation from other member if any )
#
class Groups(db.Model):
  __tablename__ = 'groups'

  group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  group_fam = db.Column(db.String(50), nullable=False) # This will be the reference for the sync with a server
  group_name = db.Column(db.String(50), nullable=False) # This will be the reference for the sync with a server
  group_dsc = db.Column(db.String(100), nullable=False)
  group_owner_name = db.Column(db.String(200), nullable=False)
  group_system = db.Column(db.Integer, nullable=False) # 0 deleted
  is_active = db.Column(db.Integer, nullable=False) # 0 deleted
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  group_member = db.relationship('GroupsMember')

  def __init__(self, group_fam, group_name, group_dsc, group_owner_name, group_system=0, is_active=1):
    self.group_fam = group_fam
    self.group_name = group_name
    self.group_dsc = group_dsc
    self.group_owner_name = group_owner_name
    self.group_system = group_system
    self.is_active = is_active


class GroupsMember(db.Model):
  __tablename__ = 'groups_members'

  group_member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  group_fam = db.Column(db.String(50), nullable=False) # This will be the reference for the sync with a server
  group_name = db.Column(db.String(50), db.ForeignKey('groups.group_name'))  # This will be the reference for the sync with a server
  user_name = db.Column(db.String(200), nullable=False)
  approver = db.Column(db.String(200))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  group = db.relationship('Groups')

  def __init__(self, group_fam, group_name, user_name, approver):
    self.group_fam = group_fam
    self.group_name = group_name
    self.user_name = user_name
    self.approver = approver


class GroupsRepository(db.Model):
  __tablename__ = 'groups_repos'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  group_fam = db.Column(db.String(50), nullable=False)  # This will be the reference for the sync with a server
  group_name = db.Column(db.String(50), nullable=False)  # This will be the reference for the sync with a server
  repo_path = db.Column(db.String(200), nullable=False)
  user_name = db.Column(db.String(200), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, group_fam, group_name, repo_path, user_name):
    self.group_fam = group_fam
    self.group_name = group_name
    self.repo_path = repo_path
    self.user_name = user_name


class GroupsCommonAttributes(db.Model):
  __tablename__ = 'groups_attributes'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  group_fam = db.Column(db.String(50), nullable=False)  # This will be the reference for the sync with a server
  group_name = db.Column(db.String(50), nullable=False)  # This will be the reference for the sync with a server
  group_attr_code = db.Column(db.String(20), nullable=False)
  group_attr_val = db.Column(db.String(200), nullable=False)
  user_name = db.Column(db.String(200), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, group_fam, group_name, group_attr_code, group_attr_val, user_name):
    self.group_fam = group_fam
    self.group_name = group_name
    self.group_attr_code = group_attr_code
    self.group_attr_val = group_attr_val
    self.user_name = user_name


class GroupsUsersAttributes(db.Model):
  __tablename__ = 'groups_specific_attributes'

  group_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  group_fam = db.Column(db.String(50), nullable=False)  # This will be the reference for the sync with a server
  group_name = db.Column(db.String(50), nullable=False)  # This will be the reference for the sync with a server
  group_user_attr_code = db.Column(db.String(20), nullable=False)
  group_user_attr_dsc = db.Column(db.String(200), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, group_fam, group_name, group_attr_code, group_attr_val, user_name):
    self.group_fam = group_fam
    self.group_name = group_name
    self.group_attr_code = group_attr_code
    self.group_attr_val = group_attr_val
    self.user_name = user_name


class GroupsPendingApproval(db.Model):
  __tablename__ = 'groups_approval'

  id_approval = db.Column(db.Integer, primary_key=True, autoincrement=True)
  group_fam = db.Column(db.String(50), nullable=False)  # This will be the reference for the sync with a server
  group_name = db.Column(db.String(50), nullable=False)  # This will be the reference for the sync with a server
  group_member_id = db.Column(db.Integer)
  user_name = db.Column(db.String(200), nullable=False)

  def __init__(self, group_fam, group_name, group_member_id, user_name):
    self.group_fam = group_fam
    self.group_name = group_name
    self.group_member_id = group_member_id
    self.user_name = user_name


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO THE ARES INTERNAL LOGS FOR A REPORT
#
class ComponentUsages(db.Model):
  __tablename__ = 'ares_component_usage'

  usage_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  run_id = db.Column(db.Integer)
  script_id = db.Column(db.Integer)
  component_category = db.Column(db.String(120), nullable=False)
  component_name = db.Column(db.String(120), nullable=False)
  call_count = db.Column(db.Integer, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, script_id, component_category, component_name, call_count):
    self.run_id = run_id
    self.script_id = script_id
    self.component_category = component_category
    self.component_name = component_name
    self.call_count = call_count


class AresWebPackages(db.Model):
  __tablename__ = 'ares_web_packages'

  rpt_pkg_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  run_id = db.Column(db.Integer)
  script_id = db.Column(db.Integer)
  import_type = db.Column(db.String(120), nullable=False)
  ares_import_alias = db.Column(db.String(120), nullable=False)
  pkg_ver = db.Column(db.String(120), nullable=False)
  web_site = db.Column(db.String(120), nullable=False)
  actions = db.Column(db.String(50), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, script_id, import_type, ares_import_alias, pkg_ver, web_site, actions):
    self.run_id = run_id
    self.script_id = script_id
    self.import_type = import_type
    self.ares_import_alias = ares_import_alias
    self.pkg_ver = pkg_ver
    self.web_site = web_site
    self.actions = actions


class AresLibPaths(db.Model):
  __tablename__ = 'ares_lib_path'

  ares_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  lib_path = db.Column(db.String(2000), nullable=False)
  usr_nam = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, lib_path, usr_nam):
    self.usr_nam = usr_nam
    self.lib_path = lib_path


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO ENVIRONMENTS
#
# Possible actions
# Create an env with an owner and a main group responsible
# Monitor the download
#
class Environments(db.Model):
  __tablename__ = 'envs'

  env_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  report_name = db.Column(db.String(120), nullable=False)
  report_path = db.Column(db.String(200), nullable=False)
  report_dsc = db.Column(db.Text, nullable=False)
  group_id = db.Column(db.Integer, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  is_valid = db.Column(db.Integer, nullable=False) # The environment is valid
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, report_name, report_path, report_dsc, usr_name, is_valid=1, group_id='PUBLIC'):
    self.report_name = report_name
    self.report_path = report_path
    self.report_dsc = report_dsc
    self.usr_name = usr_name
    self.group_id = group_id
    self.is_valid = is_valid


class EnvironmentsContributor(db.Model):
  __tablename__ = 'envs_contributors'

  env_contrib_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  env_id = db.Column(db.Integer)
  report_name = db.Column(db.String(120), nullable=False)
  contributor = db.Column(db.String(120), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  start_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  end_dt = db.Column(db.DateTime, nullable=True)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, env_id, report_name, contributor, usr_name, hostname):
    self.env_id, self.report_name, self.contributor, self.usr_name, self.hostname = env_id, report_name, contributor, usr_name, hostname


class EnvironmentsUpdate(db.Model):
  __tablename__ = 'envs_updates'

  env_updt_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  usr_name = db.Column(db.String(120), nullable=False)
  cmmt = db.Column(db.Text, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside
  mac_address = db.Column(db.Integer, nullable=False)

  def __init__(self, usr_name, cmmt, clc_dt, hostname, mac_address):
    self.clc_dt, self.usr_name, self.hostname, self.mac_address, self.cmmt = clc_dt, usr_name, hostname, mac_address, cmmt


class EnvironmentsDownloads(db.Model):
  __tablename__ = 'envs_download'

  download_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  env_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, env_id, usr_name):
    self.env_id = env_id
    self.usr_name = usr_name
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class EnvironmentsFncs(db.Model):
  __tablename__ = 'envs_fncs'

  env_fnc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  env_id = db.Column(db.Integer)
  env_fnc_name = db.Column(db.String(30))
  is_active = db.Column(db.Integer, nullable=False) # 0 deleted
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, env_id, env_fnc_name, is_active, usr_name, hostname, mac_address):
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')
    self.env_id, self.env_fnc_name, self.is_active = env_id, env_fnc_name, is_active
    self.usr_name, self.hostname, self.mac_address = usr_name, hostname, mac_address


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO SCRIPTS
#
# Create an script with an owner and a main group responsible
# Monitor the download
# Add comments on the script
# Possiblity to store version of the report as amd file hashed
#
class Scripts(db.Model):
  __tablename__ = 'scripts'

  script_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  env_id = db.Column(db.Integer)
  script_name = db.Column(db.String(120), nullable=False)
  script_dsc = db.Column(db.Text, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  group_id = db.Column(db.Integer, nullable=False)
  is_valid = db.Column(db.Integer, nullable=False) # 1 the script is still active
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, env_id, script_name, script_dsc, usr_name, is_valid=1, group_id='PUBLIC'):
    self.env_id, self.script_name, self.usr_name, self.group_id = env_id, script_name, usr_name, group_id
    self.is_valid, self.script_dsc = is_valid, script_dsc


class ScriptsDownloads(db.Model):
  __tablename__ = 'scripts_download'

  download_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  script_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, script_id, usr_name):
    self.script_id = script_id
    self.usr_name = usr_name
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class ScriptsArchives(db.Model):
  __tablename__ = 'script_archived'

  arch_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  script_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  group_name = db.Column(db.String(50), nullable=False) # An archive file is always attached to a group
  url_token = db.Column(db.Text, nullable=False)
  salt = db.Column(db.Integer) # For the hash of the markdown file
  is_active = db.Column(db.Integer)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, script_id, usr_name, url_token, salt, group_name, is_active=1):
    self.script_id = script_id
    self.usr_name = usr_name
    self.url_token = url_token
    self.salt = salt
    self.is_active = is_active
    self.group_name = group_name


class ScriptsTag(db.Model):
  __tablename__ = 'script_tag'

  report_tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  script_id = db.Column(db.Integer, nullable=False)
  tag_name = db.Column(db.String(30), nullable=False)
  is_active = db.Column(db.Integer, nullable=False)  # 1 True, 0 False
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, script_id, tag_name, usr_name, is_active=1):
    self.script_id = script_id
    self.tag_name = tag_name
    self.usr_name = usr_name
    self.is_active = is_active


class ScriptsDocViews(db.Model):
  __tablename__ = 'script_doc_views'

  script_view_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  script_id = db.Column(db.Integer, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, script_id, usr_name):
    self.script_id = script_id
    self.usr_name = usr_name


class ScriptsDocViewsUpdate(db.Model):
  __tablename__ = 'script_doc_views_update'

  doc_update_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  script_id = db.Column(db.Integer, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, script_id, usr_name, hostname):
    self.script_id, self.usr_name, self.hostname = script_id, usr_name, hostname


class ScriptsMessage(db.Model):
  __tablename__ = 'script_user_msg'

  message_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  script_id = db.Column(db.Integer)
  message_key_id = db.Column(db.Integer)
  group_name = db.Column(db.String(50), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  subject = db.Column(db.String(60), nullable=False)
  category = db.Column(db.String(20), nullable=False)
  comment = db.Column(db.Text, nullable=False)
  is_valid = db.Column(db.Integer, nullable=False) # The environment is valid
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, script_id, message_key_id, group_name, usr_name, category, subject, comment, is_valid=1):
    self.script_id, self.category, self.subject = script_id, category, subject
    self.usr_name, self.group_name = usr_name, group_name
    self.comment, self.message_key_id = comment, message_key_id
    self.is_valid = is_valid
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class ScriptsMessagePmts(db.Model):
  __tablename__ = 'script_user_msg_pmt'

  message_key_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  script_id = db.Column(db.Integer)
  html_codes = db.Column(db.Text, nullable=False)
  html_vals = db.Column(db.Text, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, script_id, html_codes, html_vals):
    self.html_vals, self.html_codes, self.script_id = html_vals, html_codes, script_id
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO A DATA SERVICE
# > Services are only things called from a report from the jsPost of jsGet
# > It is not related to the external systems
#
class Service(db.Model):
  __tablename__ = 'service'

  service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  group_id = db.Column(db.Integer, nullable=False)
  service_url = db.Column(db.String(100), nullable=False)
  service_name = db.Column(db.String(100), nullable=False)
  service_type = db.Column(db.String(30), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, usr_name, service_url, service_name, service_type, mac_address, group_id='PUBLIC'):
    self.usr_name = usr_name
    self.group_id = group_id
    self.service_name = service_name
    self.service_url = service_url
    self.service_type = service_type
    self.mac_address = mac_address


class ServiceDsc(db.Model):
  __tablename__ = 'service_dsc'

  service_dsc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  service_id = db.Column(db.Integer)
  service_name = db.Column(db.String(100), nullable=False)
  service_dsc = db.Column(db.Text, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, service_id, service_name, service_dsc):
    self.service_id, self.service_name, self.service_dsc = service_id, service_name, service_dsc


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO A SCRIPT RUN
#
class RunScript(db.Model):
  __tablename__ = 'run_script'

  run_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  script_id = db.Column(db.Integer)
  host_name = db.Column(db.String(120), nullable=False)
  url = db.Column(db.String(1200), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, usr_name, script_id, url, host_name):
    self.usr_name = usr_name
    self.url = url
    self.script_id = script_id
    self.host_name = host_name
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class RunScriptServices(db.Model):
  __tablename__ = 'run_script_services'

  run_service_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  run_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  script_id = db.Column(db.Integer)
  service_id = db.Column(db.Integer)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, usr_name, script_id, service_id):
    self.run_id = run_id
    self.usr_name = usr_name
    self.script_id = script_id
    self.service_id = service_id
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class RunScriptServicePmt(db.Model):
  __tablename__ = 'run_script_service_pmt'

  run_pmt_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  run_id = db.Column(db.Integer)
  run_script_id = db.Column(db.Integer)
  run_service_id = db.Column(db.Integer)
  service_data = db.Column(db.Text)
  usr_name = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, run_script_id, run_service_id, service_data, usr_name, mac_address):
    self.run_id = run_id
    self.run_script_id = run_script_id
    self.run_service_id = run_service_id
    self.service_data = service_data
    self.mac_address = mac_address
    self.usr_name = usr_name


class RunScriptServiceTime(db.Model):
  __tablename__ = 'run_script_service_time'

  run_time_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  run_id = db.Column(db.Integer)
  run_service_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  run_time = db.Column(db.Float, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, run_service_id, usr_name, run_time):
    self.run_id = run_id
    self.run_service_id = run_service_id
    self.usr_name = usr_name
    self.run_time = run_time
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class RunScriptServiceFailures(db.Model):
  __tablename__ = 'run_script_service_failure'

  failed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  run_service_id = db.Column(db.Integer)
  run_id = db.Column(db.Integer)
  category = db.Column(db.String(100), nullable=False)
  detail = db.Column(db.String(300), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, run_service_id, category, detail, usr_name):
    self.run_id = run_id
    self.category = category
    self.detail = detail
    self.run_service_id = run_service_id
    self.usr_name = usr_name
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class RunScriptHtmlCodes(db.Model):
  __tablename__ = 'run_script_htmlcodes'

  run_code_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  run_id = db.Column(db.Integer)
  script_id = db.Column(db.Integer)
  html_code = db.Column(db.String(50), nullable=False)
  ares_class = db.Column(db.String(50), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, script_id, html_code, ares_class):
    self.run_id, self.script_id, self.html_code, self.ares_class = run_id, script_id, html_code, ares_class
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class RunScriptPmt(db.Model):
  __tablename__ = 'run_script_pmt'

  run_pmt_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  run_id = db.Column(db.Integer)
  script_id = db.Column(db.Integer)
  parameters = db.Column(db.Text)

  def __init__(self, run_id, script_id, parameters):
    self.run_id = run_id
    self.script_id = script_id
    self.parameters = parameters


class RunScriptFailures(db.Model):
  __tablename__ = 'run_script_failure'

  failed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  script_id = db.Column(db.Integer)
  run_id = db.Column(db.Integer)
  # Redondant but just defined in case of failure in the import
  report_name = db.Column(db.String(120))
  script_name = db.Column(db.String(120))
  category = db.Column(db.String(100), nullable=False)
  detail = db.Column(db.String(300), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, report_name, script_name, script_id, category, detail, usr_name):
    self.run_id = run_id
    self.report_name = report_name
    self.script_name = script_name
    self.category = category
    self.detail = detail
    self.script_id = script_id
    self.usr_name = usr_name
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class RunScriptSystems(db.Model):
  __tablename__ = 'run_system'

  system_run_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  script_id = db.Column(db.Integer)
  run_id = db.Column(db.Integer)
  # To get the full definition of a system call
  system_code = db.Column(db.String(100), nullable=False)
  system_pmt = db.Column(db.Text, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  read_time = db.Column(db.Float, nullable=False)
  write_time = db.Column(db.Float, nullable=False)
  count_calls = db.Column(db.Float, nullable=False)
  run_time = db.Column(db.Float, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, script_id, run_id, system_code, system_pmt, read_time, write_time, count_calls, run_time, usr_name):
    self.script_id = script_id
    self.run_id = run_id
    self.system_code = system_code
    self.read_time = read_time
    self.system_pmt = system_pmt
    self.write_time = write_time
    self.count_calls = count_calls
    self.run_time = run_time
    self.usr_name = usr_name
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class RunScriptSystemsFailures(db.Model):
  __tablename__ = 'run_system_failures'

  system_failed_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  script_id = db.Column(db.Integer)
  run_id = db.Column(db.Integer)
  # To get the full definition of a system call
  system_call = db.Column(db.String(20), nullable=False)  # get, set, del....
  system_code = db.Column(db.String(100), nullable=False)
  system_pmt = db.Column(db.Text, nullable=False)
  system_fnc = db.Column(db.String(20), nullable=False)
  category = db.Column(db.String(100), nullable=False)
  detail = db.Column(db.String(300), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, script_id, run_id, system_call, system_code, system_pmt, system_fnc, category, detail, usr_name):
    self.run_id = run_id
    self.category = category
    self.detail = detail
    self.script_id = script_id
    self.system_call = system_call
    self.system_code = system_code
    self.system_pmt = system_pmt
    self.system_fnc = system_fnc
    self.usr_name = usr_name
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class RunScriptTime(db.Model):
  __tablename__ = 'run_script_time'

  run_time_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  run_id = db.Column(db.Integer)
  script_id = db.Column(db.Integer)
  # Redondant but just defined in case of failure in the import
  report_name = db.Column(db.String(120))
  script_name = db.Column(db.String(120))
  usr_name = db.Column(db.String(120), nullable=False)
  run_time = db.Column(db.Float, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, script_id, report_name, script_name, usr_name, run_time):
    self.run_id = run_id
    self.script_id = script_id
    self.report_name = report_name
    self.script_name = script_name
    self.usr_name = usr_name
    self.run_time = run_time
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class RunScriptFncs(db.Model):
  __tablename__ = 'run_script_fncs'

  run_fnc_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  run_id = db.Column(db.Integer)
  script_id = db.Column(db.Integer)
  # Redondant but just defined in case of failure in the import
  report_name = db.Column(db.String(120))
  script_name = db.Column(db.String(120))
  function_name = db.Column(db.String(120))
  module = db.Column(db.String(120))
  language = db.Column(db.String(10), nullable=False)
  total_time = db.Column(db.Integer)
  count = db.Column(db.Integer)
  components = db.Column(db.Text)
  usr_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, run_id, script_id, report_name, script_name, module, function_name, language, total_time, count, components, usr_name, hostname, mac_address):
    self.run_id, self.script_id, self.report_name, self.script_name, self.module = run_id, script_id, report_name, script_name, module
    self.language, self.total_time, self.count, self.components = language, total_time, count, components
    self.usr_name, self.hostname, self.mac_address, self.function_name = usr_name, hostname, mac_address, function_name


class PasswordUpdates(db.Model):
  __tablename__ = 'pwd_updates'

  usr_nam = db.Column(db.String(120), primary_key=True, nullable=False)
  tmp_token = db.Column(db.String(35), nullable=False)
  crea_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, usr_nam, tmp_token):
    self.usr_nam = usr_nam
    self.tmp_token = tmp_token


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO MANAGE THE SCHEDULER
#
class Tasks(db.Model):
  __tablename__ = 'tsk'

  tsk_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  tsk_name = db.Column(db.String(120), nullable=False)
  path = db.Column(db.Text, nullable=False)
  dsc = db.Column(db.Text, nullable=False)
  script = db.Column(db.String(120), nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  approver = db.Column(db.String(120), nullable=False)
  status = db.Column(db.String(10), nullable=False)
  is_active = db.Column(db.Integer, nullable=False, default=1)  # The environment is valid
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, tsk_name, path, dsc, script, usr_name, approver, status, is_active=1):
    self.tsk_name, self.path, self.dsc, self.script, self.usr_name, self.approver, self.status, self.is_active = tsk_name, path, dsc, script, usr_name, approver, status, is_active


class TskConfig(db.Model):
  __tablename__ = 'tsk_config'

  tsk_config_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  tsk_id = db.Column(db.Integer, nullable=False)
  tsk_name = db.Column(db.String(120), nullable=False)
  params = db.Column(db.Text, nullable=False)
  fct = db.Column(db.String(30)) # put main by default
  is_active = db.Column(db.Integer, nullable=False, default=1)  # The environment is valid
  tsk_recurrence = db.Column(db.String(20), nullable=False)
  tsk_stt_dt = db.Column(db.String(10), nullable=False, default=datetime.datetime.utcnow)
  tsk_end_dt = db.Column(db.String(10), nullable=False, default=datetime.datetime.utcnow)
  day = db.Column(db.String(20), nullable=False)
  week = db.Column(db.String(20), nullable=False)
  day_of_week = db.Column(db.String(20), nullable=False)
  hour = db.Column(db.Integer, nullable=False)
  minute = db.Column(db.Integer, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside
  mac_address = db.Column(db.Integer, nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, tsk_id, tsk_name, params, fct, usr_name, tsk_recurrence, tsk_stt_dt, tsk_end_dt, day, week, day_of_week, hour, minute, hostname, mac_address, is_active=1):
    self.tsk_id, self.tsk_name, self.params, self.fct, self.usr_name, self.is_active = tsk_id, tsk_name, params, fct, usr_name, is_active
    self.tsk_recurrence, self.tsk_stt_dt, self.tsk_end_dt, self.day, self.week, self.day_of_week, self.hour, self.minute = tsk_recurrence, tsk_stt_dt, tsk_end_dt, day, week, day_of_week, hour, minute
    self.hostname, self.mac_address = hostname, mac_address,


class TaskHistory(db.Model):
  __tablename__ = 'tsk_history'

  tsk_run_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  tsk_id = db.Column(db.Integer, nullable=False)
  tsk_name = db.Column(db.String(120), nullable=False)
  tsk_config_id = db.Column(db.Integer)
  tsk_trigger_type = db.Column(db.String(120), nullable=False)
  tsk_process_time = db.Column(db.Numeric, nullable=False)
  tsk_process_mem = db.Column(db.Numeric, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False, default=lambda: datetime.datetime.today().strftime('%Y-%m-%d'))
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, tsk_id, tsk_name, tsk_config_id, tsk_trigger_type, tsk_process_time, tsk_process_mem):
    self.tsk_id, self.tsk_name, self.tsk_config_id, self.tsk_trigger_type, self.tsk_process_time = tsk_id, tsk_name, tsk_config_id, tsk_trigger_type, tsk_process_time
    self.tsk_process_mem = tsk_process_mem


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO SET THE INTERNAL SETTINGS RELATED TO THE FRAMEWORK
#
class AresSettings(db.Model):
  __tablename__ = 'ares_settings'

  setting_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  usr_name = db.Column(db.String(120), nullable=False)
  setting_code = db.Column(db.String(120), nullable=False)
  setting_value = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, usr_name, setting_code, setting_value):
    self.usr_name = usr_name
    self.setting_code = setting_code
    self.setting_value = setting_value


class AresLogs(db.Model):
  __tablename__ = 'ares_log'

  log_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  user_name = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, user_name, hostname, mac_address):
    self.user_name = user_name
    self.hostname = hostname
    self.mac_address = mac_address
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class AresLocalUse(db.Model):
  __tablename__ = 'ares_server_use'

  local_use_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  mac_address = db.Column(db.Integer, nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, user_name, hostname, mac_address):
    self.mac_address, self.user_name, self.hostname  = mac_address, user_name, hostname
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


class AresPackagesDownloads(db.Model):
  __tablename__ = 'ares_package_download'

  download_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  package_name = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  clc_dt = db.Column(db.String(10), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, package_name, usr_name):
    self.package_name = package_name
    self.usr_name = usr_name
    self.clc_dt = datetime.datetime.today().strftime('%Y-%m-%d')


# -------------------------------------------------------------------------------------------------------------------
#             SECTION DEDICATED TO THE FEEDBACKS
#
class Feedback(db.Model):
  __tablename__ = 'feedback'

  feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  title = db.Column(db.Text)
  system = db.Column(db.String(120))
  content = db.Column(db.Text)
  status = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  hostname = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

  def __init__(self, title, content, system, status, usr_name, hostname):
    self.title, self.content, self.system, self.status, self.usr_name, self.hostname = title, content, system, status, usr_name, hostname


class FeedbackSupport(db.Model):
  __tablename__ = 'feedback_support'

  feedback_support_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
  feedback_id = db.Column(db.Integer)
  usr_name = db.Column(db.String(120), nullable=False)
  lst_mod_dt = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
  hostname = db.Column(db.String(120), nullable=False)  # This is mandatory when data can come from outside

  def __init__(self, feedback_id, usr_name, hostname):
    self.feedback_id, self.usr_name, self.hostname = feedback_id, usr_name, hostname
