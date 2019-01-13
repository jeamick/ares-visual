""" CSS Style for the HR tags
@author: Olivier Nogues

"""

import CssBase


class CssHr(CssBase.CssCls):
  """ Css Style for a simple hr element """
  __style = [
    {'attr': 'display', 'value': 'block'},
    {'attr': 'border-style', 'value': 'inset'},
    {'attr': 'border-width', 'value': '1px'},
    {'attr': 'margin', 'value': '5px'},
  ]

  directChildrenTag = "hr"