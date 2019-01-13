#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase
from ares.Lib.css import CssText


class CssButtonBasic(CssBase.CssCls):
  """
  :category: CSS Class
  :rubric: CSS
  :dsc:
    CSS Definition for a common button
  """
  reqCss = [CssText.CssTextBold]

  __style = [{'attr': 'padding', 'value': '1px 10px 5px 10px'},
             {'attr': 'margin', 'value': '2px 0 2px 0'},
             {'attr': 'text-decoration', 'value': 'none'},
             {'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
             {'attr': 'border-radius', 'value': '5px'},
             {'attr': 'display', 'value': 'inline-block'},
             {'attr': 'text-transform', 'value': 'uppercase'}
             ]

  hover = [
    {'attr': 'text-decoration', 'value': 'none'},
    {'attr': 'cursor', 'value': 'pointer'},
  ]

  def customize(self, style, eventsStyles):
    """
    :category: CSS Class override
    :rubric: CSS
    :dsc:
      Enhance the border and background-color to get the standard colors defined in the base CSS class.
      This will ensure that this component will always be in sync if the colors chart is updated
    """
    style.update({'border': '1px solid %s' % self.colorCharts['baseColor'][0], 'background-color': self.colorCharts['greyColor'][0]})
    eventsStyles['hover'].update({'background-color': self.colorCharts['baseColor'][1], 'color': self.colorCharts['greyColor'][0]})


class CssButtonReset(CssBase.CssCls):
  """
  :category: CSS Class
  :rubric: CSS
  :dsc:
    Bespoke CSS Definition for the Reset button
  """
  reqCss = [CssText.CssTextBold]

  __style = [{'attr': 'padding', 'value': '5px 10px 5px 10px'},
             {'attr': 'margin-top', 'value': '5px'},
             {'attr': 'text-decoration', 'value': 'none'},
             {'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
             {'attr': 'border-radius', 'value': '5px'},
             {'attr': 'display', 'value': 'inline-block'},
             {'attr': 'text-transform', 'value': 'uppercase'}
             ]

  hover = [
    {'attr': 'text-decoration', 'value': 'none'},
    {'attr': 'cursor', 'value': 'pointer'},
  ]

  def customize(self, style, eventsStyles):
    """
    :category: CSS Class override
    :rubric: CSS
    :dsc:
      Enhance the border and background-color to get the standard colors defined in the base CSS class.
      This will ensure that this component will always be in sync if the colors chart is updated
    """
    style.update( {'border': '1px solid %s' % self.colorCharts['redColor'][4], 'color': self.colorCharts['redColor'][4], 'background-color': self.colorCharts['greyColor'][0]} )
    eventsStyles['hover'].update( {'background-color': self.colorCharts['redColor'][4], 'color': self.colorCharts['greyColor'][0]} )


class CssButtonSuccess(CssBase.CssCls):
  """
  :category: CSS Class
  :rubric: CSS
  :dsc:
    Bespoke CSS Definition for the Success button
  """
  reqCss = [CssText.CssTextBold]

  __style = [{'attr': 'padding', 'value': '10px 10px 10px 10px'},
             {'attr': 'margin', 'value': '10px 0px 10px 5px'},
             {'attr': 'text-decoration', 'value': 'none'},
             {'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
             {'attr': 'border-radius', 'value': '5px'},
             {'attr': 'display', 'value': 'inline-block'},
             {'attr': 'text-transform', 'value': 'uppercase'},
             ]

  hover = [
    {'attr': 'text-decoration', 'value': 'none'},
    {'attr': 'cursor', 'value': 'pointer'},
  ]

  def customize(self, style, eventsStyles):
    """
    :category: CSS Class override
    :rubric: CSS
    :dsc:
      Enhance the border, color and background-color to get the standard colors defined in the base CSS class.
      This will ensure that this component will always be in sync if the colors chart is updated
    """
    style.update({'color': self.colorCharts['baseColor'][0], 'background-color': self.colorCharts['greyColor'][0],
                  'border': '1px solid %s' % self.colorCharts['baseColor'][0]})
    eventsStyles['hover'].update({'color': self.colorCharts['greyColor'][0], 'background-color': self.colorCharts['baseColor'][1], 'color': self.colorCharts['greyColor'][0]})