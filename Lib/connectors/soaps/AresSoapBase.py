#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
'eng':
'''
:dsc:

'''
}


from ares.Lib.connectors import AresConn
from ares.Lib.AresImports import requires


# Will automatically add the external library to be able to use this module
ares_soap = requires("zeep", reason='Missing Package', install='zeep', sourceScript=__file__)


class AresSoap(AresConn.AresConn):
  """

  """
  ALIAS = 'SOAP'

  @classmethod
  def isCompatible(cls, params):
    global ares_soap

    if ares_soap is None:
      ares_soap = requires("zeep", reason='Missing Package', install='zeep', autoImport=True, sourceScript=__file__)
    if ares_soap is not None:
      return (True, '<i class="far fa-check-square"></i>&nbsp;&nbsp;Available')

    return (False, '<i class="fas fa-times-circle"></i>&nbsp;&nbsp;Credential missing <a style="color:red;text-decoration:underline;font-weight:bold;" href="/admin/account">Account Settings</a>')

  @classmethod
  def _getData(cls, params, sourceDef=None, **kwargs):

    return []

