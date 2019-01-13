#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
import base64

try:
  import urllib.request as request
  from urllib.error import HTTPError, URLError
  import urllib
except ImportError:
  import urllib2 as request
  from urllib2 import HTTPError, URLError
  import urllib

from ares.Lib.connectors import AresConn


class AresJira(AresConn.AresConn):
  """
  :category: Connector
  :rubric: PY
  :type: class
  :dsc:
      Youpi
  """
  ALIAS = 'JIRA'

  @classmethod
  def isCompatible(cls, params):
    if params.get('pwd', '') != '' and params.get('user_id', '') != '':
      return (True, '<i class="far fa-check-square"></i>&nbsp;&nbsp;Available')

    return (False, '<i class="fas fa-times-circle"></i>&nbsp;&nbsp;Credential missing <a style="color:red;text-decoration:underline;font-weight:bold;" href="/admin/account">Account Settings</a>')

  @classmethod
  def _getData(cls, params, sourceDef=None, **kwargs):
    base64Str = base64.b64encode('%(user_id)s:%(pwd)s' % sourceDef)
    try:
      searchData = {"maxResults": "200", "jql": params['searchJql'] }
      searchUrl = '%s/search?%s' % (sourceDef['baseUrl'], urllib.urlencode(searchData))
      searchRequest = request.Request(url=searchUrl)
      searchRequest.add_header('Authorization', 'Basic %s' % base64Str)
      issues_fields = ['created', 'status', 'summary', 'assignee', 'resolutiondate', 'updated',
                       'timeestimate', 'timespent', 'duedate', 'description', 'resolution']
      issues_list = []
      jsonResponse = request.urlopen(searchRequest)
      for issue in json.loads(jsonResponse.read())['issues']:
        newIssue = {'key': issue['key']}
        for field in issues_fields:
          newIssue[field] = 'NA'
          if field == 'assignee' and issue['fields'] and field in issue['fields'] and issue['fields'][field] and 'displayName' in issue['fields'][field]:
            newIssue[field] = issue['fields'][field]['displayName']
          elif field == 'status' and issue['fields'] and field in issue['fields'] and 'name' in issue['fields'][field]:
            newIssue[field] = issue['fields'][field]['name']
          elif issue['fields'] and field in issue['fields']:
            newIssue[field] = issue['fields'][field]
        issues_list.append(newIssue)
      return issues_list
    except HTTPError as e:
      return [{ 'status': False, 'message': 'url %s, data %s' % (e.url, searchRequest.get_data()) }]
