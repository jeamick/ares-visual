#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import re
import json


class ListBase(object):

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return '$(this).text()'
