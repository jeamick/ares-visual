#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssTableRedCells(CssBase.CssCls):
  __style = [
    {'attr': 'color', 'value': 'red'},
  ]

  after = [
    {'attr': 'content', 'value': '" $"'},
  ]


class CssTableBackGroundRedCells(CssBase.CssCls):
  __style = [
    {'attr': 'color', 'value': 'red'},
  ]