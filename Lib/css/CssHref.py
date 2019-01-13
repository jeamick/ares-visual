#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase
import CssDiv
import CssList


class CssHrefNoDecoration(CssBase.CssCls):
  """ CSS Basic style for links """
  __style = [
    {'attr': 'text-decoration', 'value': 'none'},
  ]
  directChildrenTag = "a"


class CssLabelDates(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'background-image', 'value': 'none!important'},
  ]
  childrenTag = "a"

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background-color': '%s!important' % self.colorCharts['blueColor'][0], 'color': '%s!important' % self.colorCharts['greyColor'][0]})


class CssHreftMenu(CssBase.CssCls):
  """ """
  reqCss = [CssDiv.CssDivNoBorder, CssList.CssListNoDecoration, CssHrefNoDecoration]
  __style = [
    {'attr': 'display', 'value': 'block'},
    {'attr': 'position', 'value': 'relative'},
    {'attr': 'font-size', 'value': CssBase.CssCls.headerFontSize},
    {'attr': 'height', 'value': '32px'},
    {'attr': 'text-shadow', 'value': '1px 1px 0px rgba(255,255,255, .2)'},
  ]

  hover = [ {'attr': 'color', 'value': 'yellow'} ]
  directChildrenTag = "a"

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background': self.colorCharts['baseColor'][5], 'color': self.colorCharts['greyColor'][0]})


class CssHrefSubMenu(CssBase.CssCls):
  """ CSS Style for the link sub menu """
  __style = [{'attr': 'width', 'value': '100%'},
             {'attr': 'padding-left', 'value': '5px'},
             {'attr': 'color', 'value': 'white'},
             {'attr': 'text-decoration', 'value': 'none'},]

  childrenTag = "a"


class CssSideBarLinks(CssBase.CssCls):
  """ CSS Style for the link side bar menu """
  __style = [
    {'attr': 'padding-top', 'value': '5px'},
    {'attr': 'padding-bottom', 'value': '5px'},
    {'attr': 'text-decoration', 'value': 'none'},
    {'attr': 'display', 'value': 'block'},
  ]

  # On mouse over CSS event
  hover = [
    {'attr': 'text-decoration', 'value': 'none'},
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    eventsStyles['hover'].update({'background-color': self.colorCharts['greyColor'][2]})


class CssHrefContentLevel1(CssBase.CssCls):
  __style = [
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'margin', 'value': '0'},
    {'attr': 'margin', 'value': '5px 0 0 0'},
    {'attr': 'padding', 'value': '0'},
    {'attr': 'font-size', 'value': '14px'},
  ]


class CssHrefContentLevel2(CssBase.CssCls):
  __style = [
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'font-size', 'value': '14px'},
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'margin-left', 'value': '20px'},
    {'attr': 'padding', 'value': '0'},
  ]


class CssHrefContentLevel3(CssBase.CssCls):
  __style = [
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'font-size', 'value': '14px'},
    {'attr': 'margin-left', 'value': '40px'},
    {'attr': 'padding', 'value': '0'},
  ]


class CssHrefContentLevel4(CssBase.CssCls):
  __style = [
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'font-size', 'value': '14px'},
    {'attr': 'margin-left', 'value': '60px'},
    {'attr': 'padding', 'value': '0'},
  ]


class CssFeedbackLink(CssBase.CssCls):
  __style = [
    {'attr': 'position', 'value': 'fixed'},
    {'attr': 'bottom', 'value': '5px'},
    {'attr': 'cursor', 'value': 'pointer'},
    {'attr': 'right', 'value': '25px'},
    {'attr': 'padding', 'value': '0 10px'},
    {'attr': 'z-index', 'value': '1000'},
  ]

  hover = [
    {'attr': 'text-decoration', 'value': 'underline'},
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background-color': self.colorCharts['greyColor'][2]})