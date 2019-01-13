#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import CssBase


class CssTableExcel(CssBase.CssCls):
  """ CSS Style for the excel tables """
  __style = [{'attr': 'border-collapse', 'value': 'collapse'},
             {'attr': 'border-spacing', 'value': '0'},
             {'attr': 'margin', 'value': '0'},
             {'attr': 'border', 'value': '1px solid #e5e0e0'},
             ]
  childrenTag = 'table'


class CssTableExcelHeaderCell(CssBase.CssCls):
  """ CSS Style for the Excel cell """
  __style = [{'attr': 'border', 'value': '1px solid #cecece'},
             {'attr': 'padding', 'value': '1px 5px'},
             {'attr': 'text-align', 'value': 'center'},
             {'attr': 'background-color', 'value': '#DCDCDC'},
             ]
  childrenTag = 'table th'


class CssTableExcelTd(CssBase.CssCls):
  """ CSS Style for the Excel cell """
  __style = [{'attr': 'padding', 'value': '0'},
             {'attr': 'margin', 'value': '0'},
             ]
  htmlTag = 'table td'


class CssTableExcelCell(CssBase.CssCls):
  """ CSS Style for the Excel cell """
  __style = [{'attr': 'border', 'value': '2px solid white'},
             {'attr': 'background-color', 'value': 'white'},
             {'attr': 'height', 'value': '100%'},
             {'attr': 'width', 'value': '100%'},
             ]
  htmlTag = 'td > div'

  active = [{'attr': 'border', 'value': '2px solid #8EB0E7'},]


class CssTableExcelTitle(CssBase.CssCls):
  """ """
  htmlTag = 'td.rows'

  __style = [{'attr': 'border', 'value': '1px solid #cecece'},
             {'attr': 'cursor', 'value': 'pointer'},
             {'attr': 'padding', 'value': '1px 20px 1px 20px'},
             {'attr': 'background-color', 'value': '#F3F3F3'}]

  # CSS Event on mouse over
  hover = [{'attr': 'cursor', 'value': 'pointer'}]

  # CSS Event on click
  active = [{'attr': 'background-color', 'value': '#8EB0E7'}]


# -------------------------------------------------------------------------------------------
# CSS Style for the selected rows
# -------------------------------------------------------------------------------------------
class CssTableExcelSelectedRow(CssBase.CssCls):
  """ Change the color of the selected row """
  htmlTag = 'tr.blue td > div'
  __style = [
      {'attr': 'background-color', 'value': '#E6EFFF'},
  ]


class CssTableExcelSelected(CssBase.CssCls):
  """ Change the color of the first column of the selected row """
  htmlTag = 'tr.blue td:first-child'
  __style = [
      {'attr': 'background-color', 'value': '#8EB0E7'},
      {'attr': 'border', 'value': '1px dotted #5292F7'},
  ]
