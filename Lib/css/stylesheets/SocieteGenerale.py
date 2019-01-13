#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

# All colors are coming from the template
# https://www.societegenerale.com/sites/default/files/documents/Document%20de%20r%C3%A9f%C3%A9rence/2018/ddr-2018-societe-generale-depot-amf-d18-0112-fr.pdf

import CssBase


charts = ['#730014', '#ad001e', '#ff5774', '#ff8fa2', '#e60028', '#dad7d7', '#c1bcbc', '#938b8b', '#635c5c',
          '#bb88ff', '#d1b3ff','#d15f32','#ffccaa','#ffeebb','#485d8c']


colorHtml = {
  'baseColor': [
    "#00673D",
    "#00673D",
    "#a4262c", # Side bar color
    "#00673D",
    "#e0e0eb",
    "#0000FF",
    "#0000FF",
    "#293846",
    "#0000FF",
    "#0000FF",
    "#EBF0F8",
    "#F4F4F4"

  ],

  'redColor': [
    "#FF0000",
    '#D40034',
    "#CCCCCC", # Button reopen in the sidebar
    "#ff9800",
    "#CCCCCC" # Button style
  ],

  'blueColor': [
    "#e60028", # Borders color
    "#293342",
    "#f5513c", # Color used in the titles
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
  ]

}


# --------------------------------------------------------------------------------------------------------------
#                                   HTML COMPONENTS STYLE CHANGES
#

class CssTitle1(CssBase.CssCls):
  """ Css Style for a simple text """
  __style = [
    {'attr': 'padding', 'value': '0 0 5px 0'},
    {'attr': 'font-size', 'value': '24px'},
    {'attr': 'text-transform', 'value': 'uppercase'},
    {'attr': 'white-space', 'value': 'pre-wrap'},
    {'attr': 'border-width', 'value': '2px'},
    {'attr': 'margin-bottom', 'value': '5px'},
    ]

  def customize(self, style, eventsStyles):
    style.update({"color": self.colorCharts['greyColor'][10]})
    style.update({"border-bottom": "1px solid %s" % self.colorCharts['blueColor'][0]})
    style.update({"border-color": self.colorCharts['blueColor'][5]})
