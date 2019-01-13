#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssTableBasic(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'margin', 'value': '5px'},
    {'attr': 'border-collapse', 'value': 'collapse'},
  ]


class CssTableColumnSystem(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'margin', 'value': '5px'},
    {'attr': 'text-align', 'value': 'left'},
    {'attr': 'font-weight', 'value': 'bold'},
  ]


class CssTableColumnFixed(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'margin', 'value': '5px'},
    {'attr': 'text-align', 'value': 'left'},
    {'attr': 'font-weight', 'value': 'bold'},
  ]


class CssTableNewRow(CssBase.CssCls):
  __style = [
    {'attr': 'color', 'value': '#546472'},
  ]


class CssTableSelected(CssBase.CssCls):
  __style = [
    {'attr': 'background-color', 'value': '#AEDAF8!important'},
  ]


class CssCellComment(CssBase.CssCls):
  __style = [
    {'attr': 'margin', 'value': '0!important'},
    {'attr': 'padding', 'value': '2px 0 0 2px!important'},
  ]


class CssCellSave(CssBase.CssCls):
  __style = [
    {'attr': 'color', 'value': '#293846!important'},
  ]


class CssTdEditor(CssBase.CssCls):
  __style = [
    {'attr': 'border-width', 'value': '1px'},
    {'attr': 'border-style', 'value': 'solid'},
    {'attr': 'text-align', 'value': 'left'},
    {'attr': 'height', 'value': '30px'},
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'vertical-align', 'value': 'middle'},
  ]

  def customize(self, style, eventsStyles):
    style.update({"color": self.colorCharts['blueColor'][6], 'border-color': self.colorCharts['greyColor'][9]})


class CssTdDetails(CssBase.CssCls):
  __style = []

  before = [
    {'attr': "content", "value": r"'\f0fe'"},
    {'attr': "font-family", "value": "'Font Awesome 5 Free'"},
    {'attr': 'cursor', 'value': 'pointer'},
    {'attr': 'padding', 'value': '0 5px 0 0'}
  ]

  htmlTag = 'td'


class CssTdDetailsShown(CssBase.CssCls):
  """
  :category:
  :rubric: CSS
  :type: Configuration
  :dsc:

  """
  __style = []

  before = [
    {'attr': "content", "value": r"'\f146'"},
    {'attr': "font-family", "value": "'Font Awesome 5 Free'"},
    {'attr': 'cursor', 'value': 'pointer'},
    {'attr': 'padding', 'value': '0 5px 0 0'}
  ]

  htmlTag = 'td'