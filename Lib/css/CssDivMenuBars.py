#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssSideBarMenu(CssBase.CssCls):
  __style = [
    {'attr': 'display', 'value': 'block'},
    {'attr': 'width', 'value': '100%'},
  ]

  hover = [
    {'attr': 'text-decoration', 'value': 'underline'},
  ]

  def customize(self, style, eventsStyles):
    style.update({'color': self.colorCharts['baseColor'][0]})


class CssSideBarFixed(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'height', 'value': '100%'},
    {'attr': 'width', 'value': '40px'},
    {'attr': 'text-align', 'value': 'center'},
    {'attr': 'position', 'value': 'fixed'},
    {'attr': 'padding', 'value': '60px 0 0 0'},
    {'attr': 'z-index', 'value': '5'},
    {'attr': 'top', 'value': '0'},
    {'attr': 'left', 'value': '0'},
    {'attr': 'overflow-x', 'value': 'hidden'},
  ]

  def customize(self, style, eventsStyles):
    style.update({'background-color': self.colorCharts['baseColor'][2]})


class CssSideBarBubble(CssBase.CssCls):
  __style = [
    {'attr': 'position', 'value': 'fixed'},
    {'attr': 'display', 'value': 'none'},
    {'attr': 'overflow-x', 'value': 'hidden'},
    {'attr': 'text-align', 'value': 'left'},
    {'attr': 'font-size', 'value': '12px'},
    {'attr': 'height', 'value': '100%'},
    {'attr': 'min-width', 'value': '200px'},
    {'attr': 'padding', 'value': '10px'},
    {'attr': 'color', 'value': 'black'},
  ]

  def customize(self, style, eventsStyles):
    style.update({'background-color': self.colorCharts['baseColor'][11], 'font-size': self.fontSize})
    #eventsStyles['after'].update({'border-top': '10px solid #293846'} )


class CssSideBar(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'height', 'value': '100%'},
    {'attr': 'position', 'value': 'fixed'},
    {'attr': 'z-index', 'value': '5'},
    {'attr': 'left', 'value': '0'},
    {'attr': 'overflow-x', 'value': 'hidden'},
    {'attr': 'padding-top', 'value': '15px'},
  ]


class CssSideBarLiHref(CssBase.CssCls):
  __style = [
    {'attr': 'color', 'value': 'white'},
    {'attr': 'margin', 'value': '0'},
    {'attr': 'padding', 'value': '0'},
  ]

  childrenTag = 'li ul a'

  def customize(self, style, eventsStyles):
    style.update({'background-color': self.colorCharts['baseColor'][2]})


class CssSideBarLi(CssBase.CssCls):
  __style = [
    {'attr': 'color', 'value': 'white'},
    {'attr': 'list-style-type', 'value': 'none'},
  ]

  childrenTag = 'li'

  def customize(self, style, eventsStyles):
    style.update({'background-color': self.colorCharts['baseColor'][2]})


class CssParamsBar(CssBase.CssCls):
  """
  height:%(height)spx;
  padding:0;%(top)spx;
  """
  __style = [
    {'attr': 'vertical-align', 'value': 'middle'},
    {'attr': 'white-space', 'value': 'nowrap'},
    {'attr': 'overflow-x', 'value': 'auto'},
    {'attr': 'overflow-y', 'value': 'hidden'},
    {'attr': 'padding', 'value': '0'},
    {'attr': 'z-index', 'value': '10'},
    {'attr': 'width', 'value': '100%'},
    {'attr': 'position', 'value': 'fixed'},
    {'attr': 'left', 'value': '0'},
    {'attr': 'margin', 'value': '0'},
  ]

  def customize(self, style, eventsStyles):
    style.update({'border-bottom': "1px solid %s" % self.colorCharts['greyColor'][4]})
    style.update({'background-color': self.colorCharts['greyColor'][0]})