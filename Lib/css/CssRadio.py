#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssRadioButton(CssBase.CssCls):
  __style = [
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'cursor', 'value': 'pointer'},
    ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background': self.colorCharts['greyColor'][0], 'color': self.colorCharts['greyColor'][8], 'font-size': CssBase.CssCls.fontSize})


class CssRadioButtonSelected(CssBase.CssCls):
  __style = [
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'cursor', 'value': 'pointer'},
    ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background': self.colorCharts['blueColor'][2], 'color': self.colorCharts['greyColor'][0], 'font-size': CssBase.CssCls.fontSize})


class CssRadioSwitch(CssBase.CssCls):
  """ CSS Style for the excel tables """
  __style = [{'attr': 'height', 'value': '0'},
             {'attr': 'width', 'value': '0'},
             {'attr': 'visibility', 'value': 'hidden'}]
  childrenTag = 'input'


class CssRadioSwitchLabel(CssBase.CssCls):
  """ CSS Style for the excel tables """
  __style = [{'attr': 'cursor', 'value': 'pointer'},
             {'attr': 'margin', 'value': '2px'},
             {'attr': 'text-indent', 'value': '-9999px'},
             {'attr': 'display', 'value': 'block'},
             {'attr': 'border-radius', 'value': '100px'},
             {'attr': 'position', 'value': 'relative'},
  ]

  after = [{'attr': 'content', 'value': "''"},
           {'attr': 'position', 'value': 'absolute'},
           {'attr': 'left', 'value': '5px'},
           {'attr': 'width', 'value': '20px'},
           {'attr': 'height', 'value': '100%'},
           {'attr': 'border-radius', 'value': '20px'},
           {'attr': 'transition', 'value': '0.3s'},
  ]
  childrenTag = 'label'

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background': self.colorCharts['greyColor'][1]})
    eventsStyles['after'].update({'background-color': self.colorCharts['greyColor'][0]})


class CssRadioSwitchChecked(CssBase.CssCls):
  """ """
  __style = []
  after = [
    {'attr': 'left', 'value': 'calc(100% - 5px)'},
    {'attr': 'transform', 'value': 'translateX(-100%)'}
  ]
  childrenTag = "input:checked + label"

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background': self.colorCharts['baseColor'][7]})

