#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import random
import math


DSC = {
  'eng': '''
:category: Style
:rubric: CSS
:type: Colors
:dsc:
  Python module to be able to easily transform and manipulate CSS colors in different formats.
  The main color format used in the framework is the hexadecimal format. If you need further details about this format [Wikipedia](https://en.wikipedia.org/wiki/Web_colors)
  [Here](https://fr.wikipedia.org/wiki/Syst%C3%A8me_hexad%C3%A9cimal) you can get more details about this format

'''
}

class CssColorMaker(object):
  """
  :category: Colors
  :rubric: CSS
  :type: Class
  :dsc:

  """
  charts = ['#334D6B', '#aabbee', '#6677bb', '#8B98E8', '#005566', '#269493', '#66bbaa', '#bbeeee', '#4e1c72',
            '#bb88ff', '#d1b3ff', '#d15f32', '#ffccaa', '#ffeebb', '#485d8c']

  def __init__(self, aresObj=None):
    self.aresObj = aresObj
    self.colors = [
      {"type": "baseColor", "color": "#293846", "dsc": ""},
      {"type": "baseColor", "color": "#293846", "dsc": ""},
      {"type": "baseColor", "color": "#293846", "dsc": ""},
      {"type": "baseColor", "color": "#293846", "dsc": ""},
      {"type": "baseColor", "color": "#e0e0eb", "dsc": ""},
      {"type": "baseColor", "color": "#0000FF", "dsc": ""},
      {"type": "baseColor", "color": "#0000FF", "dsc": ""},
      {"type": "baseColor", "color": "#293846", "dsc": ""},
      {"type": "baseColor", "color": "#0000FF", "dsc": ""},
      {"type": "baseColor", "color": "#0000FF", "dsc": ""},
      {"type": "baseColor", "color": "#EBF0F8", "dsc": ""},
      {"type": "baseColor", "color": "#F4F4F4", "dsc": ""},

      {"type": "textColor", "color": "#293846", "dsc": ""},
      {"type": "textColor", "color": "#293846", "dsc": ""},

      {"type": "greyColor", "color": "#FFFFFF", "dsc": ""},
      {"type": "greyColor", "color": "#E6E6E6", "dsc": ""},
      {"type": "greyColor", "color": "#F4F4F4", "dsc": ""},
      {"type": "greyColor", "color": "#888888", "dsc": ""},
      {"type": "greyColor", "color": "#404040", "dsc": ""},
      {"type": "greyColor", "color": "#FFFFFF", "dsc": ""},
      {"type": "greyColor", "color": "#282828", "dsc": ""},
      {"type": "greyColor", "color": "#000008", "dsc": ""},
      {"type": "greyColor", "color": "#000008", "dsc": ""},
      {"type": "greyColor", "color": "#CCCCCC", "dsc": ""}, #9
      {"type": "greyColor", "color": "#212529", "dsc": ""},
      {"type": "greyColor", "color": "#545454", "dsc": ""},
      {"type": "greyColor", "color": "#808080", "dsc": ""},
      {"type": "greyColor", "color": "#F6F8FA", "dsc": ""},
      {"type": "greyColor", "color": "#000000", "dsc": ""},

      {"type": "border", "color": "#F4F4F4", "dsc": ""},
      {"type": "border", "color": "#808080", "dsc": ""},

      {"type": "redColor", "color": "#FF0000", "dsc": ""},
      {"type": "redColor", "color": "#D40034", "dsc": ""},
      {"type": "redColor", "color": "#f44336", "dsc": ""},
      {"type": "redColor", "color": "#ff9800", "dsc": ""},
      {"type": "redColor", "color": "#C00000", "dsc": ""}, # Button
      {"type": "redColor", "color": "#ff0000", "dsc": ""},
      {"type": "redColor", "color": "#FFF3CD", "dsc": ""}, # Notifications WARNING
      {"type": "redColor", "color": "#F8D7DA", "dsc": ""}, # Notifications DANGER

      {"type": "greenColor", "color": "#4CAF50", "dsc": ""},
      {"type": "greenColor", "color": "#006621", "dsc": ""},
      {"type": "greenColor", "color": "#398438", "dsc": ""},
      {"type": "greenColor", "color": "#D4EDDA", "dsc": ""},

      {"type": "blueColor", "color": "#6285b0", "dsc": ""},
      {"type": "blueColor", "color": "#293342", "dsc": ""},
      {"type": "blueColor", "color": "#384884", "dsc": ""},
      {"type": "blueColor", "color": "#292B2C", "dsc": ""},
      {"type": "blueColor", "color": "#292bb2", "dsc": ""},
      {"type": "blueColor", "color": "#343435", "dsc": ""},
      {"type": "blueColor", "color": "#2196F3", "dsc": ""},
      {"type": "blueColor", "color": "#5c96d4", "dsc": ""},
      {"type": "blueColor", "color": "#55adda", "dsc": ""},
      {"type": "blueColor", "color": "#D3D3D3", "dsc": ""},
      {"type": "blueColor", "color": "#cbe3ef", "dsc": ""}, #10
      {"type": "blueColor", "color": "#d3dfea", "dsc": ""},
      {"type": "blueColor", "color": "#213B68", "dsc": ""},
      {"type": "blueColor", "color": "#1a8bf0", "dsc": ""},
      {"type": "blueColor", "color": "#AEDAF8", "dsc": ""},
      {"type": "blueColor", "color": "#9ea9b2", "dsc": ""},
      {"type": "blueColor", "color": "#480DC6", "dsc": ""},
      {"type": "blueColor", "color": "#1A0DAB", "dsc": ""},
      {"type": "blueColor", "color": "#959EAE", "dsc": ""},
      {"type": "blueColor", "color": "#0000A0", "dsc": ""},
    ]

  def help(self, category=None, rubric=None, type=None, value=None, enum=None, section=None, lang='eng', outType=None):
    """
    :return:
    """
    pass

  @classmethod
  def getHexToRgb(cls, hexColor):
    """
    :category: Color Format Transformation
    :rubric: CSS
    :type: Colors
    :example: colorObj.getHexToRgb('#213B68')
    :dsc:
      Convert an hexadecimal color format to a RGB one
    :link RGB Documentation:
    :link Hexadecimal Documentation:
    :link Color convertor:
    :return: The RGB Color list
    """
    if not hexColor.startswith("#"):
      raise Exception("Hexadecimal color should start with #")

    if not len(hexColor) == 7:
      raise Exception("Color should have a length of 7")

    return [ int(hexColor[1:3], 16), int(hexColor[3:5], 16), int(hexColor[5:7], 16) ]

  @classmethod
  def getRgbToHex(cls, rgbColor):
    """
    :category: Color Format Transformation
    :rubric: CSS
    :type: Colors
    :example: colorObj.getRgbToHex( [255, 0, 0] )
    :dsc:
      Convert a RGB color format to an hexadecimal one
    :link RGB Documentation:
    :link Hexadecimal Documentation:
    :link Color convertor:
    :return: The RGB Color list
    """
    color = []
    for val in rgbColor:
      val = hex(int(val)).lstrip('0x')
      if len(val) != 2:
        leadingZeros = ["0"] * (2 - len(val))
        val = "%s%s" % ("".join(leadingZeros), val)
      color.append(val)
    return "#%s" % "".join(color)

  @staticmethod
  def getRandColor():
    """
    :category: Colors Generator
    :rubric: CSS
    :type: Colors
    :example: colorObj.getRandColor()
    :dsc:
      Return a random hexadecimal color
    :return: Hexadecimal color
    """
    letters = '0123456789ABCDEF'
    color = ['#']
    for i in range(6):
      color.append( letters[math.floor(random.random() * 16)] )
    return "".join(color)

  @classmethod
  def getColors(cls, start, end, countColors):
    """
    :category: Colors Generator
    :rubric: CSS
    :type: Colors
    :example:
    :dsc:

    :return: Return a list of hexadecimal colors
    """
    colors = [start]
    for i in range(countColors-2):
      colors.append(cls.getGradient(start, end, 1.0/ (countColors-1) * (i + 1)))
    colors.append(end)
    return colors

  @classmethod
  def getGradient(cls, start, end, percent):
    """
    :category: Colors Generator
    :rubric: CSS
    :type: Colors
    :example: colorObj.getGradient(, , 0.2)
    :dsc:


    :return:
    """
    rgbEnd = cls.getHexToRgb(end)
    rgbDiff = [ (rgbEnd[i] - val) * percent + val for i, val in enumerate(cls.getHexToRgb(start)) ]
    return cls.getRgbToHex(rgbDiff)


def docEnum(aresObj, outStream, lang='eng'):
  """
  :category: Datatable
  :rubric: PY:
  :type: Configuration
  """
  categories = {}
  for color in CssColorMaker(aresObj).colors:
    categories[ color['type'] ] = categories.get( color['type'], 0 )  + 1

  for color, countColor in categories.items():
    outStream.link("**%s** - Range of %s code colors" % (color, countColor), "", cssPmts={"margin": "5px"})

  outStream.src(__file__)
