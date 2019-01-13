#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
'eng':
'''
:dsc:
Generic Connector to interact with a BitBucket repository.
'''
}


from ares.Lib.connectors import AresConn
from ares.Lib.AresImports import requires


# Will automatically add the external library to be able to use this module
ares_bitbucket = requires("bitbucket.client", reason='Missing Package', install='bitbucket-python', sourceScript=__file__)


class AresConnBitBucket(AresConn.AresConn):
  """
  :category: BitBucket
  :rubric: PY
  :type: Connector
  :example: aresObj.getData('BITBUCKET', {'repo': r''})
  :Link Documentation: https://pypi.org/project/bitbucket-python/
  :dsc:

  """
  ALIAS = 'BITBUCKET'

  @classmethod
  def isCompatible(cls, params):
    global ares_bitbucket

    if ares_bitbucket is None:
      ares_bitbucket = requires("bitbucket.client", reason='Missing Package', install='bitbucket-python', autoImport=True, sourceScript=__file__)
    if ares_bitbucket is not None:
      return (True, '<i class="far fa-check-square"></i>&nbsp;&nbsp;Available')

    return (False, '<i class="fas fa-times-circle"></i>&nbsp;&nbsp;Credential missing <a style="color:red;text-decoration:underline;font-weight:bold;" href="/admin/account">Account Settings</a>')

  @classmethod
  def _getData(cls, params, sourceDef=None, **kwargs):
    # TODO: Find a way to store KPI for different projects
    emails = []
    bbClient = ares_bitbucket.Client(sourceDef['user_id'], sourceDef['pwd'])
    print(bbClient.get_user())
    print(bbClient.get_repositories())
    return emails