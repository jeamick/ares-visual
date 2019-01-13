#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssSelectStyle(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'font-weight', 'value': 'bold'},
    {'attr': 'font-size', 'value': '16px'},
  ]

  def customize(self, style, eventsStyles):
    style.update({"background": self.colorCharts['blueColor'][2]})
    style.update({"color": self.colorCharts['greyColor'][0]})


class CssSelect(CssBase.CssCls):
  """ Change the style of the generic selection component """
  __style = [
      {'attr': 'margin', 'value': '0'},
      {'attr': 'overflow', 'value': 'hidden'},
      {'attr': 'display', 'value': 'inline-block'}
  ]

  hover = []

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background': self.colorCharts['baseColor'][10], 'color': self.colorCharts['baseColor'][0]})
    eventsStyles['hover'].update({'background': self.colorCharts['baseColor'][0], 'color': 'white'})

  directChildrenTag = "select"