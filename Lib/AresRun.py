#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import os
import importlib

from ares.Lib import AresImports
ares_flask = AresImports.requires(name="flask", reason='Missing Package', install='flask', autoImport=True, sourceScript=__file__)


class Run(object):
  """
  :category:
  :rubric:
  :type:
  :dsc:

  """
  __slots__ = ['mac_address', 'host_name', 'current_user', 'report_name', 'script_name', 'local_path', 'url_root',
               'title', 'is_local', 'url']

  def __init__(self, report_name, script_name, current_user, host_name, mac_address, url_root, title=None):
    self.report_name, self.script_name = report_name, script_name
    self.current_user, self.host_name = current_user, host_name
    self.mac_address, self.url_root = mac_address, url_root
    self.url = "#"
    if report_name is not None:
      mod = importlib.import_module('%s.__init__' % report_name)
      self.local_path, _ = os.path.split(os.path.abspath(mod.__file__))
      if script_name is not None and ares_flask is not None:
        self.url = "%s/run/%s/%s" % (ares_flask.current_app.config['URLS']['ares-report'], self.report_name, self.script_name)
    else:
      self.local_path = None
    self.title = "%s \ %s " % (self.report_name.upper(), self.script_name) if title is None else title
    self.is_local = True if (ares_flask is None or ares_flask.request.url_root.startswith('http://127.0.0.1')) else False
