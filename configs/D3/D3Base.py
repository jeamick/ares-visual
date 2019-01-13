#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


class D3Base(dict):
  convertFnc = None

  def __init__(self, aresObj, data, htmlId):
    self.aresObj, self.data, self.options = aresObj, data, {}
    self.chartId = htmlId
    self.data = self.transformation(data)
    self.config()

  @classmethod
  def transformation(cls, data):
    return data

  def config(self): pass
