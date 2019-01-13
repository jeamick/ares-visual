#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase

WIDTH = 250
HEIGHT = 150


class CssImgBasic(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'display', 'value': 'block'},
    {'attr': 'border-radius', 'value': '15px'},
    {'attr': 'margin', 'value': '5px'},
  ]


class CssImgParagraph(CssBase.CssCls):
  """ """
  __style = [{'attr': 'transform', 'value': 'scale(1.1)'},
             {'attr': 'font-family', 'value': 'Georgia, serif'},
             {'attr': 'font-style', 'value': 'italic'},
             {'attr': 'font-size', 'value': '10px'},
             {'attr': 'position', 'value': 'relative'},
             {'attr': 'width', 'value': '%spx' % (WIDTH - 20 )},
             {'attr': 'color', 'value': '#fff'},
             {'attr': 'padding', 'value': '10px 20px 20px'},
             {'attr': 'text-align', 'value': 'center'}]
  hover = [{'attr': 'transition', 'value': 'all 0.2s linear'}]
  childrenTag = 'p'


class CssImgH2(CssBase.CssCls):
  """ """
  __style = [{'attr': 'transform', 'value': 'translateY(-100px)'},
             {'attr': 'opacity', 'value': '0'},
             {'attr': 'transition', 'value': 'all 0.2s ease-in-out'},
             {'attr': 'text-transform', 'value': 'uppercase'},
             {'attr': 'color', 'value': '#fff'},
             {'attr': 'text-align', 'value': 'center'},
             {'attr': 'position', 'value': 'relative'},
             {'attr': 'font-size', 'value': '14px'},
             {'attr': 'padding', 'value': '10px'},
             {'attr': 'background', 'value': '#000008'},
             {'attr': 'margin', 'value': '20px 0 0 0'}]
  hover = [{'attr': 'opacity', 'value': '1'},
           {'attr': 'transform', 'value': 'translateY(0px)'}]
  childrenTag = 'h2'


class CssImgMask(CssBase.CssCls):
  """ """
  __style = [{'attr': 'opacity', 'value': '0'},
             {'attr': 'background-color', 'value': CssBase.CssCls.colors10[0]},
             {'attr': 'transition', 'value': 'all 0.4s ease-in-out'},
             {'attr': 'width', 'value': '100%'},
             {'attr': 'height', 'value': '100%'},
             {'attr': 'position', 'value': 'absolute'},
             {'attr': 'overflow', 'value': 'hidden'},
             {'attr': 'top', 'value': '0'},
             {'attr': 'left', 'value': '0'}]
  hover = [{'attr': 'opacity', 'value': '1'}]
  childrenTag = '.mask'


class CssImgAInfo(CssBase.CssCls):
  """ """
  __style = [{'attr': 'opacity', 'value': '0'},
             {'attr': 'transition', 'value': 'all 0.2s ease-in-out'},
             {'attr': 'display', 'value': 'inline-block'},
             {'attr': 'text-decoration', 'value': 'none'},
             {'attr': 'padding', 'value': '7px 14px'},
             {'attr': 'background', 'value': '#000'},
             {'attr': 'color', 'value': '#fff'},
             {'attr': 'position', 'value': 'relative'},
             {'attr': 'top', 'value': '70%'},
             {'attr': 'text-transform', 'value': 'uppercase'},
             {'attr': 'box-shadow', 'value': '0 0 1px #000'}]
  hover = [{'attr': 'opacity', 'value': '1'},
           {'attr': 'transform', 'value': 'translateY(0px)'},
           {'attr': 'box-shadow', 'value': '0 0 5px #000'},
           {'attr': 'transition-delay', 'value': '0.2s'}]
  childrenTag = 'a.info'


class CssImg(CssBase.CssCls):
  """ """
  __style = [{'attr': 'transition', 'value': 'all 0.2s linear'},
             {'attr': 'display', 'value': 'block'},
             {'attr': 'position', 'value': 'relative'}]
  hover = [{'attr': 'transform', 'value': 'scale(1.1)'}]
  childrenTag = 'img'


class CssContent(CssBase.CssCls):
  """ """
  __style = [{'attr': 'width', 'value': '100%'},
             {'attr': 'height', 'value': '70%'},
             {'attr': 'position', 'value': 'absolute'},
             {'attr': 'overflow', 'value': 'hidden'},
             {'attr': 'top', 'value': '20%'},
             {'attr': 'left', 'value': '0'}]
  childrenTag = '.content'


class CssView(CssBase.CssCls):
  """ """
  __style = [{'attr': 'height', 'value': '70%'},
             {'attr': 'margin', 'value': '10px'},
             {'attr': 'float', 'value': 'left'},
             {'attr': 'border', 'value': '10px solid #fff'},
             {'attr': 'overflow', 'value': 'hidden'},
             {'attr': 'position', 'value': 'relative'},
             {'attr': 'text-align', 'value': 'center'},
             {'attr': 'box-shadow', 'value': '1px 1px 2px #e6e6e6'},
             {'attr': 'cursor', 'value': 'default'}]


class CssCarrousel(CssBase.CssCls):
  """ """
  __style = []


class CssCarrouselImg(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'width', 'value': '100%'},
    {'attr': 'height', 'value': 'auto'},
    {'attr': 'position', 'value': 'relative'},
  ]
  childrenTag = 'img'


class CssCarrouselLi(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'list-style', 'value': 'none'},
    {'attr': 'display', 'value': 'none'},
  ]
  childrenTag = 'li'


class CssCarrouselLabel(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'background', 'value': 'black'},
    {'attr': 'padding', 'value': '10px'},
    {'attr': 'border-radius', 'value': '50%'},
    {'attr': 'display', 'value': 'inline-block'},
    {'attr': 'text-align', 'value': 'center'},
  ]
  childrenTag = 'label'


class CssCarrouselH2(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'position', 'value': 'absolute'},
    {'attr': 'top', 'value': '10px'},
    {'attr': 'color', 'value': '#fff'},
    {'attr': 'padding', 'value': '10px'},
    {'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
    {'attr': 'background-color', 'value': '#292B2C'},
  ]
  childrenTag = 'h2'