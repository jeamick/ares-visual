#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase



# Special override for colors in the different chart libraries
charts = ['#00e626','#00CC22','#00b31e', '#8B98E8', '#005566', '#269493', '#66bbaa', '#bbeeee', '#4e1c72',
          '#bb88ff', '#d1b3ff','#d15f32','#ffccaa','#ffeebb','#485d8c']


class CssSelectStyle(CssBase.CssCls):
  __style = [
    {'attr': 'background', 'value': 'green'},
    {'attr': 'color', 'value': 'white'},
  ]


class CssTableStyled(CssBase.CssCls):
  __style = [
    {'attr': 'border', 'value': '1px solid green'},
  ]


class CssTableSelected(CssBase.CssCls):
  __style = [
    {'attr': 'background-color', 'value': 'green!important'},
    {'attr': 'color', 'value': 'white!important'},
  ]



class CssTablePrevCol(CssBase.CssCls):
  __style = [
    {'attr': 'background-color', 'value': '#648C5E'},
  ]



class CssTableTotal(CssBase.CssCls):
  __style = [
    {'attr': 'border-top', 'value': '1px solid green!important'},
    {'attr': 'color', 'value': 'green!important'},
    {'attr': 'border-bottom', 'value': '1px solid green!important'},
  ]


class CssTableHeader(CssBase.CssCls):
  __style = [
    {'attr': 'background-color', 'value': '#007E00'},
    {'attr': 'color', 'value': 'white'},
    ]


class CssTableTitle(CssBase.CssCls):
  __style = [
    {'attr': 'background-color', 'value': '#E6E6FA'},
    ]