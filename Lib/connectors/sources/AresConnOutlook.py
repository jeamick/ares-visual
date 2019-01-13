#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
'eng':
'''
:dsc:
Generic Connector to retrieve data from an Outlook open application.
This script will parse the emails of the selected set of folders. Not all the mailbox will be scanned by default.

For security reason this connector does not work on server mode in order to avoid interacting with the mail box of the
server. This could be used to locally retrieve information and then feed a centralise database.

The idea of this connector is to put in place specialised nodes in the network to get specific information and only the results
will be shared
'''
}


from ares.Lib.connectors import AresConn
from ares.Lib.AresImports import requires


# Will automatically add the external library to be able to use this module
ares_pywin32 = requires("win32com.client", reason='Missing Package', install='pywin32', sourceScript=__file__)


class AresConnOutlook(AresConn.AresConn):
  """
  :category: Outlook
  :rubric: PY
  :type: Connector
  :example: print(aresObj.getData('OUTLOOK', {'folders': ['Example']}))
  :Link Documentation: https://www.codementor.io/aliacetrefli/how-to-read-outlook-emails-by-python-jkp2ksk95
  :dsc:
    Connector to retrieve emails from an open Outlook session.
    The list of folders to be read should be defined by default no folders will be used to extract emails.
    This could be a way to retrieve data from a mailing list to produce KPI
  """
  ALIAS = 'OUTLOOK'

  @classmethod
  def isCompatible(cls, params):
    global ares_pywin32

    if not params['is_local']:
      return (False,
            '<i class="fas fa-times-circle"></i>&nbsp;&nbsp;Oulook connector cannot be used if script is not done locally')

    if ares_pywin32 is None:
      ares_pywin32 = requires("win32com.client", reason='Missing Package', install='pywin32', autoImport=True, sourceScript=__file__)
    if ares_pywin32 is not None:
      return (True, '<i class="far fa-check-square"></i>&nbsp;&nbsp;Available')

    return (False, '<i class="fas fa-times-circle"></i>&nbsp;&nbsp;Credential missing <a style="color:red;text-decoration:underline;font-weight:bold;" href="/admin/account">Account Settings</a>')

  @classmethod
  def _getData(cls, params, sourceDef=None, **kwargs):
    emails = []
    outlook = ares_pywin32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    accounts = ares_pywin32.Dispatch("Outlook.Application").Session.Accounts;
    for account in accounts:
      inbox = outlook.Folders(account.DeliveryStore.DisplayName)
      folders = inbox.Folders
      for folder in folders:
        if not str(folder) in params['folders']:
          continue

        messages = folder.Items
        if len(messages) > 0:
          for message2 in messages:
            try:
              sender = message2.SenderEmailAddress
              subject = message2.Subject
              content = message2.Body
              date = message2.SentOn.strftime("%d-%m-%y")
              if sender != "":
                emails.append({'to': sender, 'subject': subject, 'body': content, 'date': date})
            except:
              print("Error")
              print(account.DeliveryStore.DisplayName)
              pass
    return emails