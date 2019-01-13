#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssStdIcon(CssBase.CssCls):
  __style = [
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'margin', 'value': '0 0 0 20px'},
    {'attr': 'font-size', 'value': '20px'},
    {'attr': 'cursor', 'value': 'hand'},
    {'attr': 'cursor', 'value': 'pointer'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    style.update( {"color": self.colorCharts['blueColor'][6]} )
    eventsStyles['hover'].update( {"color": self.colorCharts['blueColor'][7]} )


class CssSmallIcon(CssBase.CssCls):
  __style = [
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'margin', 'value': '0 0 0 15px'},
    {'attr': 'font-size', 'value': '10px'},
    {'attr': 'cursor', 'value': 'hand'},
    {'attr': 'cursor', 'value': 'pointer'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    eventsStyles['hover'].update( {"color": self.colorCharts['blueColor'][7]} )


class CssSmallIconRigth(CssBase.CssCls):
  __style = [
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'margin', 'value': '0 0 0 15px'},
    {'attr': 'font-size', 'value': '10px'},
    {'attr': 'cursor', 'value': 'hand'},
    {'attr': 'float', 'value': 'right'},
    {'attr': 'cursor', 'value': 'pointer'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    eventsStyles['hover'].update( {"color": self.colorCharts['blueColor'][7]} )


class CssSmallIconRed(CssBase.CssCls):
  __style = [
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'margin', 'value': '0 0 0 15px'},
    {'attr': 'font-size', 'value': '10px'},
    {'attr': 'cursor', 'value': 'hand'},
    {'attr': 'cursor', 'value': 'pointer'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    style.update( {"color": self.colorCharts['redColor'][1]} )
    eventsStyles['hover'].update( {"color": self.colorCharts['redColor'][0]} )


class CssOutIcon(CssBase.CssCls):
  __style = [
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'margin', 'value': '0 0 0 20px'},
    {'attr': 'font-size', 'value': '15px'},
    {'attr': 'cursor', 'value': 'hand'},
    {'attr': 'cursor', 'value': 'pointer'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    style.update( {"color": self.colorCharts['redColor'][1]} )
    eventsStyles['hover'].update( {"color": self.colorCharts['redColor'][0]} )


class CssBigIcon(CssBase.CssCls):
  __style = [
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'margin', 'value': '0 10px 0 10px'},
    {'attr': 'cursor', 'value': 'hand'},
    {'attr': 'cursor', 'value': 'pointer'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    style.update( {"color": self.colorCharts['redColor'][1], 'font-size': self.fontSize} )
    eventsStyles['hover'].update( {"color": self.colorCharts['redColor'][0]} )
