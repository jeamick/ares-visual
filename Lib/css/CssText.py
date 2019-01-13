#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssTextBold(CssBase.CssCls):
  """ """
  __style = [{'attr': 'font-weight', 'value': 'bold'}]


class CssText(CssBase.CssCls):
  """ Css Style for a simple text """
  __style = [
     {'attr': 'padding', 'value': '0'},
     {'attr': 'font-family', 'value': 'arial'},
     {'attr': 'margin', 'value': '0'},
     {'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
  ]


class CssTitle1(CssBase.CssCls):
  """ Css Style for a simple text """
  __style = [
    {'attr': 'padding', 'value': '0 0 5px 0'},
    {'attr': 'font-size', 'value': '24px'},
    {'attr': 'font-weight', 'value': 'bold'},
    {'attr': 'text-transform', 'value': 'uppercase'},
    {'attr': 'white-space', 'value': 'pre-wrap'},
    {'attr': 'border-bottom', 'value': '1px dashed black'},
    {'attr': 'border-width', 'value': '2px'},
    {'attr': 'margin-bottom', 'value': '5px'},
    ]

  def customize(self, style, eventsStyles):
    style.update({"color": self.colorCharts['greyColor'][10]})
    style.update({"border-color": self.colorCharts['blueColor'][5]})


class CssTitle2(CssBase.CssCls):
  """ Css Style for a simple text """
  __style = [
    {'attr': 'padding', 'value': '0'},
    {'attr': 'font-size', 'value': '22px'},
    {'attr': 'margin-top', 'value': '5px'},
    {'attr': 'font-weight', 'value': 'bold'},
    {'attr': 'text-transform', 'value': 'uppercase'},
    {'attr': 'white-space', 'value': 'pre-wrap'},
    ]

  def customize(self, style, eventsStyles):
    style.update({"color": self.colorCharts['blueColor'][2]})


class CssTitle3(CssBase.CssCls):
  """ Css Style for a simple text """
  __style = [
    {'attr': 'padding', 'value': '0'},
    {'attr': 'font-size', 'value': '16px'},
    {'attr': 'margin-top', 'value': '5px'},
    {'attr': 'font-weight', 'value': 'bold'},
    {'attr': 'text-transform', 'value': 'uppercase'},
    {'attr': 'white-space', 'value': 'pre-wrap'},
    ]

  def customize(self, style, eventsStyles):
    style.update( {"color": self.colorCharts['blueColor'][2] })


class CssTitle4(CssBase.CssCls):
  """ Css Style for a simple text """
  __style = [
    {'attr': 'padding', 'value': '0'},
      {'attr': 'font-size', 'value': '14px'},
    {'attr': 'margin-top', 'value': '5px'},
    {'attr': 'font-weight', 'value': 'bold'},
    {'attr': 'text-transform', 'value': 'uppercase'},
    {'attr': 'white-space', 'value': 'pre-wrap'},
    ]


class CssTitle(CssBase.CssCls):
  """ Css Style for a simple text """
  __style = [
    {'attr': 'padding', 'value': '0'},
     {'attr': 'font-size', 'value': CssBase.CssCls.headerFontSize},
     {'attr': 'font-family', 'value': 'arial'},
     {'attr': 'margin-bottom', 'value': '0'},
     {'attr': 'white-space', 'value': 'pre-wrap'},
     {'attr': 'font-weight', 'value': 'bold'},
    ]


class CssNumberCenter(CssBase.CssCls):
  """ """
  reqCss = [CssTitle]
  __style = [
    {'attr': 'width', 'value': '100%'},
    {'attr': 'text-align', 'value': 'center'},
  ]


class CssMarkRed(CssBase.CssCls):
  """ CSS Style with a Red Color """
  __style = [
    {'attr': 'background', 'value': 'none'},
    {'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
  ]

  def customize(self, style, eventsStyles):
    style.update( {"color": self.colorCharts['redColor'][5] })


class CssMarkBlue(CssBase.CssCls):
  """ CSS Style with a Blue Color """
  __style = [
    {'attr': 'background', 'value': 'none'},
    {'attr': 'font-weight', 'value': 'bold'},
    {'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
  ]

  def customize(self, style, eventsStyles):
    style.update( {"color": self.colorCharts['blueColor'][19] })


class CssTextWithBorder(CssBase.CssCls):
  """ """
  __style = [{'attr': 'border', 'value': '1px solid'},
             {'attr': 'padding', 'value': '5px'},
             {'attr': 'margin', 'value': '10px'},
             ]
  childrenTag = "fieldset"

  def customize(self, style, eventsStyles):
    style.update( {"background-color": self.colorCharts['greyColor'][0] })


class CssCheckMark(CssBase.CssCls):
  """ CSS Style for the Ckecbox text """
  __style = [
      {'attr': 'text-align', 'value': 'center'},
      {'attr': 'display', 'value': 'inline-block'},
      {'attr': 'font-family', 'value': 'FontAwesome'},
      {'attr': 'height', 'value': '18px'},
      {'attr': 'width', 'value': '18px'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update( { "background-color": self.colorCharts['greyColor'][0], "color": self.colorCharts['greyColor'][8] })
    eventsStyles['hover'].update({'color': 'white', 'background-color': self.colorCharts['baseColor'][0]})


class CssSearchExt(CssBase.CssCls):
  __style = [
      {'attr': 'width', 'value': '130px'},
      {'attr': 'height', 'value': '30px'},
      {'attr': 'box-sizing', 'value': 'border-box'},
      {'attr': 'border-radius', 'value': '4px'},
      {'attr': 'font-size', 'value': '16px'},
      {'attr': 'background-position', 'value': '10px 10px'},
      {'attr': 'background-repeat', 'value': 'no-repeat'},
      {'attr': 'padding', 'value': '12px 20px 12px 40px'},
      {'attr': '-webkit-transition', 'value': 'width 0.4s ease-in-out'},
      {'attr': 'transition', 'value': 'width 0.4s ease-in-out'},
  ]

  focus = [
      {'attr': 'width', 'value': '100%'},
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update( { "background-color": self.colorCharts['greyColor'][0], "border": '2px solid %s' % self.colorCharts['greyColor'][8] })


class CssSearch(CssBase.CssCls):
  __style = [
      {'attr': 'width', 'value': '100%'},
      {'attr': 'height', 'value': '30px'},
      {'attr': 'display', 'value': 'inline-block'},
      {'attr': 'border-radius', 'value': '4px'},
      {'attr': 'font-size', 'value': '16px'},
      {'attr': 'background-position', 'value': '10px 10px'},
      {'attr': 'background-repeat', 'value': 'no-repeat'},
      {'attr': 'padding', 'value': '20px 20px 20px 40px'},
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update( { "background-color": self.colorCharts['greyColor'][0], "border": '2px solid %s' % self.colorCharts['greyColor'][8] })


class CssTextItem(CssBase.CssCls):
  """
  :category: Style
  :rubric: CSS
  :type: Configuration
  :dsc:
    Default text selection component. This is used in different component containing lists like for example the ContextMenu.

  """
  __style = [
    {'attr': 'cursor', 'value': 'pointer'},
    {'attr': 'width', 'value': '200px'},
    {'attr': 'padding', 'value': '5px'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    eventsStyles['hover'].update(
      {"color": self.colorCharts['greyColor'][0], "background": self.colorCharts['blueColor'][0]})
