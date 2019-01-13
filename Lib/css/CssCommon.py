#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssBody(CssBase.CssCls):
  __style = [
    {'attr': 'font-size', 'value': '12px'},
    {'attr': 'top', 'value': '0'},
    {'attr': 'margin', 'value': '0 20px 0 60px'},
  ]
  htmlTag = 'body'

  def customize(self, style, eventsStyles):
    """ """
    style.update( {"background-color": self.colorCharts['greyColor'][2], "color": self.colorCharts['greyColor'][8]} )


class CssAresContent(CssBase.CssCls):
  __style = [
    {'attr': 'margin-top', 'value': '10px'},
    {'attr': 'padding', 'value': '5px'},
  ]

  def customize(self, style, eventsStyles):
    """ """
    style.update( {"background-color": self.colorCharts['greyColor'][0], "border": '1px solid %s' % self.colorCharts['greyColor'][1]} )


class CssAresLoadingBack(CssBase.CssCls):
  __style = [
    {'attr': 'text-align', 'value': 'center'},
    {'attr': 'top', 'value': '0'},
    {'attr': 'left', 'value': '0'},
    {'attr': 'width', 'value': '100%'},
    {'attr': 'padding-top', 'value': '20%'},
    {'attr': 'height', 'value': '100%'},
    {'attr': 'z-index', 'value': '295'},
    {'attr': 'position', 'value': 'fixed'},
    {'attr': 'opacity', 'value': '0.2'},
    {'attr': 'filter', 'value': 'alpha(opacity=20)'},
  ]

  def customize(self, style, eventsStyles):
    """ """
    style.update( {"background-color": self.colorCharts['greyColor'][12] } )


class CssAresLoading(CssBase.CssCls):
  __style = [
    {'attr': 'text-align', 'value': 'center'},
    {'attr': 'top', 'value': '0'},
    {'attr': 'left', 'value': '0'},
    {'attr': 'width', 'value': '100%'},
    {'attr': 'position', 'value': 'fixed'},
    {'attr': 'padding-top', 'value': '20%'},
    {'attr': 'height', 'value': '100%'},
    {'attr': 'display', 'value': 'none'},
    {'attr': 'z-index', 'value': '300'},
  ]

  def customize(self, style, eventsStyles):
    """ """
    style.update( {"color": self.colorCharts['greyColor'][8] } )




