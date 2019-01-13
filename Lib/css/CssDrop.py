#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import CssBase


class CssDropFile(CssBase.CssCls):
  __style = [
    {'attr': 'text-align', 'value': 'center'},
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'margin', 'value': '5px 0 10px 0'}
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'border': '1px dashed %s' % self.colorCharts['blueColor'][11], 'color': self.colorCharts['blueColor'][11]})

