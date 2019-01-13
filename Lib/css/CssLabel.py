""" CSS Style for the different Labels elements
@author: Olivier Nogues

"""


import CssBase


class CssLabelContainer(CssBase.CssCls):
  """ CSS Style for a simple Label """
  __style = [{'attr': 'display', 'value': 'block'},
             {'attr': 'position', 'value': 'relative'},
             {'attr': 'cursor', 'value': 'pointer'},
             {'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
             {'attr': '-webkit-user-select', 'value': 'none'},
             {'attr': '-moz-user-select', 'value': 'none'},
             {'attr': '-ms-user-select', 'value': 'none'},
             {'attr': 'user-select', 'value': 'none'}]


class CssLabelCheckMarkHover(CssBase.CssCls):
  """ """

  __style, hover = [], []
  childrenTag = 'label'

  def customize(self, style, eventsStyles):
    """ Enhance the different static configurations """
    eventsStyles['hover'].update({'background-color': self.colorCharts['baseColor'][6]})
