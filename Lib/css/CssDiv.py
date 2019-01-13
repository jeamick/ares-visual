#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssDivNoBorder(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'margin', 'value': '0'},
    {'attr': 'font-family', 'value': 'arial'},
    {'attr': 'clear', 'value': 'both'},
    {'attr': 'padding', 'value': '0'},
    {'attr': 'border', 'value': '0'},
    {'attr': 'outline', 'value': 'none'},
  ]


class CssDivWithBorder(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'margin', 'value': '0 0 5px 0'},
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'outline', 'value': 'none'},
  ]

  def customize(self, style, eventsStyles):
    style.update({'border': "1px solid %s" % self.colorCharts['border'][0]})


class CssDivChart(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'margin', 'value': '0 0 5px 0'},
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'outline', 'value': 'none'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    style.update({'border': "1px solid %s" % self.colorCharts['border'][0]})
    eventsStyles['hover'].update({'border': "1px solid %s" % self.colorCharts['blueColor'][0]})


class CssDivConsole(CssBase.CssCls):
  """ Console Div Style """
  __style = [
    {'attr': 'margin', 'value': '0'},
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'border', 'value': '0'},
    {'attr': 'outline', 'value': 'none'},
  ]

  before = [
    {'attr': 'content', 'value': r"'C:\Users\LONDON>'"},
  ]

  def customize(self, style, eventsStyles):
    style.update({'background-color': self.colorCharts['greyColor'][8]})


class CssDivCursor(CssBase.CssCls):
  """ Style reprensentation of a change on the mouse display """
  __style = [
    {'attr': 'cursor', 'value': 'cursor'},
  ]

  hover = [
    {'attr': 'cursor', 'value': 'pointer'}
  ]


class CsssDivBoxMargin(CssBase.CssCls):
  """ CSS Style for Div element with a 5 pixel margin """
  __style = [
    {'attr': 'margin', 'value': '0'},
    {'attr': 'padding', 'value': '0 2px 0 2px'},
    {'attr': 'font-family', 'value': 'arial'},
    {'attr': 'white-space', 'value': 'pre-wrap'},
  ]

  hover = []

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update( {"border": '1px solid %s' % self.colorCharts['greyColor'][0]} )
    eventsStyles['hover'].update({'border': "1px solid %s" % self.colorCharts['baseColor'][2]})


class CssDivBoxCenter(CssBase.CssCls):
  """ CSS Style for a standard Div item """
  __style = [{'attr': 'width', 'value': '100%'},
             {'attr': 'text-align', 'value': 'center'}]


class CssDivBoxWithDotBorder(CssBase.CssCls):
  """ CSS Style for a Div item with a border with dots"""
  __style = [{'attr': 'margin', 'value': '5px'}]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update( {"border": '1px dashed %s' % self.colorCharts['greyColor'][8]} )


class CssDivBubble(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'width', 'value': '80px'},
    {'attr': 'margin-left', 'value': 'auto'},
    {'attr': 'margin-right', 'value': 'auto'},
    {'attr': 'height', 'value': '80px'},
    {'attr': 'border-radius', 'value': '50%'},
    {'attr': 'padding-top', 'value': '20px'},
    {'attr': 'text-align', 'value': 'center'}
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update( {"border": '1px solid %s' % self.colorCharts['greyColor'][12]} )


class CssDivBox(CssBase.CssCls):
  """ CSS Style for a standard Div item """
  __style = [{'attr': 'width', 'value': '100%'}]

  hover = []

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    eventsStyles['hover'].update({"border-left": "4px solid %s" % self.colorCharts['greyColor'][0], 'background-color': self.colorCharts['baseColor'][0]})
    #eventsStyles['hover'].update({'background': "linear-gradient(to right, %s, white)" % self.colorCharts['baseColor'][2]})


class CssDivLeft(CssBase.CssCls):
  """ CSS Style for a box located on the left """
  __style = [{'attr': 'float', 'value': 'left'},
             {'attr': 'width', 'value': '20%'}]


class CssDivRight(CssBase.CssCls):
  """ CSS Style for a box located on the right """
  __style = [{'attr': 'float', 'value': 'right'},
             {'attr': 'width', 'value': '80%'}]


class CssDivBorder(CssBase.CssCls):
  """ CSS Style for a div element with a black border """
  __style = []

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    eventsStyles['hover'].update({"border": "1px solid %s" % self.colorCharts['greyColor'][8]})


class CssDivShadow(CssBase.CssCls):
  """ CSS Style for a div element with a black border """
  __style = [{'attr': 'box-shadow', 'value': '10px 10px 8px 10px #888888'}]


class CssDivWhitePage(CssBase.CssCls):
  """ CSS Style for a div white page """
  reqCss = [CssDivShadow, CssDivBorder]
  __style = [
    {'attr': 'height', 'value': '80%'},
    {'attr': 'min-height', 'value': '600px'},
    {'attr': 'margin', 'value': '0 10px 0 10px'}
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    eventsStyles['hover'].update({'background-color': self.colorCharts['greyColor'][0]})


class CssDivBanner(CssBase.CssCls):
  """ CSS Style for the Index Banner """
  __style = [{'attr': 'width', 'value': '100%'},
             {'attr': 'margin', 'value': '0'},
             {'attr': 'overflow-y', 'value': 'auto'},
             {'attr': 'padding', 'value': '10px'}]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background-color': self.colorCharts['greyColor'][0]})


class CssDivSubBanner(CssBase.CssCls):
  """ CSS Style for the Index Banner """
  __style = [
    {'attr': 'height', 'value': '400px'},
    {'attr': 'width', 'value': '100%'},
    {'attr': 'overflow-y', 'value': 'auto'},
    {'attr': 'margin-top', 'value': '50px'},
    {'attr': 'padding', 'value': '0'},
    {'attr': 'margin', 'value': '0'}
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'color': self.colorCharts['greyColor'][8], 'background-color': self.colorCharts['greyColor'][0]})


class CssDivLabelPoint(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'padding', 'value': '10px'},
    {'attr': 'margin-top', 'value': '20px'},
    {'attr': 'margin-left', 'value': '5px'},
    {'attr': 'border-radius', 'value': '50%'},
    {'attr': 'cursor', 'value': 'pointer'},
    {'attr': 'display', 'value': 'inline-block'},
  ]
  childrenTag = 'label'

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background': self.colorCharts['greyColor'][2]})


class CssDivCommBubble(CssBase.CssCls):
  """ """

  __style = [
    {'attr': 'width', 'value': '100%'},
    {'attr': 'vertical-align', 'value': 'top'},
    {'attr': 'top', 'value': '0'},
    {'attr': 'margin-bottom', 'value': '20px'},
    {'attr': 'margin-left', 'value': '20px'},
    {'attr': 'display', 'value': 'inline-block'},
  ]

  before = [
    {'attr': 'content', 'value': "''"},
    {'attr': 'width', 'value': '0'},
    {'attr': 'height', 'value': '0'},
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'border', 'value': '15px solid transparent'},
    {'attr': 'margin-left', 'value': '-30px'},
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'color': self.colorCharts['greyColor'][0]})
    eventsStyles['before'].update({'border-right-color': self.colorCharts['baseColor'][2] })


class CssDivComms(CssBase.CssCls):
  __style = [
    {'attr': 'margin-top', 'value': '10px'},
    {'attr': 'padding', 'value': '5px'},
  ]


class CssDivLoading(CssBase.CssCls):
  """ """

  __style = [
    {'attr': 'opacity', 'value': '0.5'},
    {'attr': 'filter', 'value': 'alpha(opacity=50)'},
    {'attr': 'width', 'value': '100%'},
    {'attr': 'height', 'value': '90%'},
    {'attr': 'text-align', 'value': 'center'},
    {'attr': 'padding-top', 'value': '10%'},
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'color': self.colorCharts['greyColor'][8]})


class CssDivHidden(CssBase.CssCls):
  __style = [
    {'attr': 'display', 'value': 'none'},
  ]


class CssDivTextLeft(CssBase.CssCls):
  __style = [
    {'attr': 'text-align', 'value': 'left'},
  ]


class CssDivTableContent(CssBase.CssCls):
  __style = [
    {'attr': 'padding', 'value': '5px 10px 5px 10px'},
    {'attr': 'width', 'value': 'auto'},
    {'attr': 'display', 'value': 'inline-block'},
  ]

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'border': '1px solid %s' % self.colorCharts['greyColor'][12], 'background-color': self.colorCharts['greyColor'][2]})


class CssDivPagination(CssBase.CssCls):
  __style = [
      {'attr': 'margin', 'value': 'auto'},
      {'attr': 'padding', 'value': '8px 16px'},
      {'attr': 'text-decoration', 'value': 'none'},
      {'attr': 'transition', 'value': 'background-color .3s'},
    ]
  hover = []
  childrenTag = 'a'

  def customize(self, style, eventsStyles):
    style.update({'color': self.colorCharts['greyColor'][8]})
    eventsStyles['hover'].update( {"background-color": self.colorCharts['greyColor'][1]} )


class CssDivEditor(CssBase.CssCls):
  __style = [
    {'attr': 'overflow', 'value': 'hidden'},
    {'attr': 'white-space', 'value': 'pre'},
    {'attr': 'display', 'value': 'block'},
    {'attr': 'padding', 'value': '30px 10px 10px 10px'},
    {'attr': 'margin-top', 'value': '5px'},
    {'attr': 'text-align', 'value': 'left'},
  ]
  focus = []

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'border': "1px solid %s" % self.colorCharts['blueColor'][9], 'background-color': self.colorCharts['greyColor'][2]})
    eventsStyles['focus'].update( {'background-color': self.colorCharts['greyColor'][0], 'border': "2px solid %s" % self.colorCharts['blueColor'][6]})


class CssDivRow(CssBase.CssCls):
  __style = [
    {'attr': "width",  'value': "100%"},
    {'attr': "padding", 'value': "5px 10px"},
    {'attr': "margin", 'value': "0"}
  ]

  hover = []

  def customize(self, style, eventsStyles):
    eventsStyles['hover'].update({'background-color': self.colorCharts['greyColor'][13]})