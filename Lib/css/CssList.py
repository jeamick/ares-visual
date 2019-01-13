""" CSS Style for the different lists
@author: Olivier Nogues

"""

import CssBase
import CssDiv


class CssBasicList(CssBase.CssCls):
  """ CSS Style for the square lists """
  __style = [
    {'attr': 'padding', 'value': '15px'},
    {'attr': 'font-size', 'value': '16px'},
    {'attr': 'font-weight', 'value': 'bold'},
  ]
  childrenTag = 'ul li:first-child'

  def customize(self, style, eventsStyles):
    style.update({"background": self.colorCharts['blueColor'][2]})
    style.update({"color": self.colorCharts['greyColor'][0]})


class CssBasicListItems(CssBase.CssCls):
  """ CSS Style for the square lists """
  __style = [
    {'attr': 'padding', 'value': '15px 0 0 0'},
    {'attr': 'display', 'value': 'block'},
  ]

  def customize(self, style, eventsStyles):
    style.update({"color": self.colorCharts['greyColor'][10]})
    style.update({"border-bottom": "1px solid %s" % self.colorCharts['blueColor'][2]})


class CssSquareList(CssBase.CssCls):
  """ CSS Style for the square lists """
  __style = [
    {'attr': 'list-style', 'value': 'none'},
    {'attr': 'text-align', 'value': 'justify'},
  ]

  before = [
    {'attr': "content", "value": r"'\f0c8'"},
    {'attr': "font-family", "value": "'Font Awesome 5 Free'"},
    {'attr': 'padding', 'value': '0 5px 0 0'}
  ]

  childrenTag = 'li'

  def customize(self, style, eventsStyles):
    eventsStyles['before'].update({"color": self.colorCharts['blueColor'][2]})


class CssListBase(CssBase.CssCls):
  """ CSS Style for a list """
  reqCss = [CssDiv.CssDivBorder]
  __style = [
    {'attr': 'width', 'value': '142px'},
    {'attr': 'min-height', 'value': '20px'},
    {'attr': 'list-style-type', 'value': 'none'},
    {'attr': 'margin', 'value': '0'},
    {'attr': 'padding', 'value': '5px 0 0 0'},
    {'attr': 'float', 'value': 'left'},
    {'attr': 'margin-right', 'value': '10px'},
  ]


class CssListLiBase(CssBase.CssCls):
  """ CSS Style for components of a list """
  __style = [
    {'attr': 'margin', 'value': '0 5px 5px 5px'},
    {'attr': 'padding', 'value': '5px'},
    {'attr': 'width', 'value': '120px'},
  ]


class CssListNoDecoration(CssBase.CssCls):
  """ """
  reqCss = [CssDiv.CssDivNoBorder]
  __style = [
    {'attr': 'list-style', 'value': 'none'},
    {'attr': 'padding', 'value': '0 0 0 5px'},
  ]


class CssListLiUlContainer(CssBase.CssCls):
  """ """
  __style = [
    {'attr': 'display', 'value': 'none'},
    {'attr': 'width', 'value': '100%'},
    {'attr': 'padding', 'value': '0'},
    {'attr': 'margin', 'value': '0'},
    {'attr': 'overflow', 'value': 'hidden'},
    {'attr': 'transition', 'value': 'height .2s ease-in-out'},
  ]

  directChildrenTag = 'ul'


class CssListLiSubItem(CssBase.CssCls):
  __style = [
    {'attr': 'display', 'value': 'table'},
    {'attr': 'width', 'value': '100%'},
    {'attr': 'height', 'value': '30px'},
    {'attr': 'vertical-align', 'value': 'middle'},
    {'attr': 'list-style-type', 'value': 'none'},
    {'attr': 'float', 'value': 'left'},
    {'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
    {'attr': 'margin', 'value': 0}
  ]

  hover = []

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    style.update({'background': self.colorCharts['greyColor'][6]})
    eventsStyles['hover'].update({"background": self.colorCharts['blueColor'][18], 'border-left': '4px solid %s' % self.colorCharts['baseColor'][7]})


