""" CSS Style for the different input elements
@author: Olivier Nogues

"""

import CssBase


class CssInput(CssBase.CssCls):
  """ CSS Style for a standard Div item """
  __style = [{'attr': 'height', 'value': '32px'},
             {'attr': 'display', 'value': 'block'},
             ]


class CssInputLabel(CssBase.CssCls):
  """ CSS Style for a standard Div item """
  __style = [{'attr': 'font-size', 'value': CssBase.CssCls.fontSize},
             {'attr': 'line-height', 'value': '1.5'},
             {'attr': 'margin-left', 'value': '10px'},
             ]
  childrenTag = 'label'


class CssInputInt(CssBase.CssCls):
  """ CSS Style for a standard Div item """
  __style = [{'attr': 'width', 'value': '100px'},
             {'attr': 'margin-left', 'value': '10px'},
             ]
  childrenTag = 'input'


class CssInputText(CssBase.CssCls):
  """ CSS Style for a standard Div item """
  __style = [{'attr': 'margin-left', 'value': '10px'},
             ]
  childrenTag = 'input'

