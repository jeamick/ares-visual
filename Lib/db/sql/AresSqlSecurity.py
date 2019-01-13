#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès



from ares.Lib.db import SqlTableSecurity
from flask_login import current_user


def dbAddFileTokens(fileCode, token, hostname, userName=None):
  if userName is None:
    userName = current_user.email
  response = SqlTableSecurity.SecArchiveStoreTokens.query.filter_by(key_alias=str(fileCode)).first()
  # Check if user exist and if he is not already attached to this file
  if response is None:
    response = SqlTableSecurity.SecArchiveStoreTokens(fileCode, token, userName, hostname)
    SqlTableSecurity.db.session.add(response)
    SqlTableSecurity.db.session.commit()

def getToken(alias):
  response = SqlTableSecurity.SecArchiveStoreTokens.query.filter_by(key_alias=str(alias)).first()
  return response.key_token