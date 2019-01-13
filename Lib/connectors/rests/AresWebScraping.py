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
ares_bs4 = requires("bs4", reason='Missing Package', install='beautifulsoup4', sourceScript=__file__)
ares_requests = requires("requests", reason='Missing Package', install='requests', sourceScript=__file__)


class AresConnOutlook(AresConn.AresConn):
  """
  :category: RSS / Web Site data
  :rubric: PY
  :type: Connector
  :example: aresObj.getData('WEB', {'url': r'http://feeds.reuters.com/reuters/businessNews'})
  :Link Documentation:
  :Link Example: https://ahmedbesbes.com/how-to-mine-newsfeed-data-and-extract-interactive-insights-in-python.html
  :dsc:
    Example to retrieve data from a web source.
  """
  ALIAS = 'WEB'

  @classmethod
  def isCompatible(cls, params):
    global ares_bs4, ares_requests

    if ares_bs4 is None:
      ares_bs4 = requires("bs4", reason='Missing Package', install='beautifulsoup4', autoImport=True, sourceScript=__file__)
      ares_requests = requires("requests", reason='Missing Package', install='requests', autoImport=True, sourceScript=__file__)
    if ares_bs4 is not None:
      return (True, '<i class="far fa-check-square"></i>&nbsp;&nbsp;Available')

    return (False, '<i class="fas fa-times-circle"></i>&nbsp;&nbsp;Credential missing <a style="color:red;text-decoration:underline;font-weight:bold;" href="/admin/account">Account Settings</a>')

  @classmethod
  def _getData(cls, params, sourceDef=None, **kwargs):
    feed = []
    response = ares_requests.get(params['url'])
    xml_soup = ares_bs4.BeautifulSoup(response.text, 'xml')
    takeaways = xml_soup.findAll('title')
    for eachtakeaway in takeaways:
      feed.append({'title': eachtakeaway.text})
    return feed