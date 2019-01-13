#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.widgets import Widget


class WidgetExample(Widget.Widget):
  """
  :category: Widget
  :rubric: PY
  :type: Structured component
  :dsc:
    Simple example of Widget using a defined kind of chart
  """
  name, label = 'Widget Example', 'Example module for a widget'

  def doc(self):
    return '''
      This is a simple example of widget
      '''

  def html(self, params):
    return self.aresObj.plot('hierarchy')


class WidgetGrid(Widget.Widget):
  """
  :category: Widget
  :rubric: PY
  :type: Structured component
  :dsc:
    Simple example of Widget using a defined kind of chart
  """
  name, label = 'Widget Grid Example', 'Grid widget width a table and a chart with some events'

  def doc(self):
    return '''
      This is a simple example of widget
      '''

  def html(self, params):
    data = [
      {'ptf': "A", 'prd': 1, 'val': 10},
      {'ptf': "B", 'prd': 1, 'val': 10},
      {'ptf': "B", 'prd': 2, 'val': 10},
      {'ptf': "C", 'prd': 3, 'val': 10}
    ]
    table = self.aresObj.table(data, title="Raw Data")
    pie = self.aresObj.plot('pie', self.aresObj.dc(data, seriesNames=['val'], xAxis='pft'), title='Pie Chart')
    pie.click( self.aresObj.jsConsole() )
    table.clickRow( pie.jsGenerate('{}') )
    bar = self.aresObj.plot('bar', self.aresObj.dc(data, seriesNames=['val'], xAxis='prd', dataFncs=['AggData']), title='Bar Chart')
    bar.click(self.aresObj.jsConsole())
    b = self.aresObj.button("test")
    #self.aresObj.grid([table, self.aresObj.col([pie, bar])], colsDim=[8, 4])
    return self.aresObj.col( [b, table, self.aresObj.grid( [pie, bar], colsDim=[4, 8] ) ])


class WidgetTableEvents(Widget.Widget):
  """
  :category: Widget
  :rubric: PY
  :type: Structured component
  :dsc:
    Simple example of Widget using a table and adding some pre defined events on it.
  """
  name, label = 'Widget Table Events', 'Table event widget'

  def html(self, params):
    data = [
      {'ptf': "A", 'prd': 1, 'val': 10},
      {'ptf': "B", 'prd': 1, 'val': 10},
      {'ptf': "B", 'prd': 2, 'val': 10},
      {'ptf': "C", 'prd': 3, 'val': 10}
    ]
    excel_alias = self.aresObj.input("", placeholder="Code", htmlCode="excel_alias")
    excel_path = self.aresObj.input("", placeholder="full excel mdb path", htmlCode="excel_path")
    button = self.aresObj.button("Add", icon="fas fa-plus")
    grid = self.aresObj.row([excel_alias, excel_path, button])
    table = self.aresObj.table([],
                               header=[ {"data": "alias", "title": "Alias"}, {"data": "path", "title": "Full Path"} ],
                               deleteCol={'url': "/reports/test", "success": "alert()"})
    button.click( [table.jsAddRow( "[{alias: %s, path: %s}]" % (excel_alias.val, excel_path.val))])
    return self.aresObj.col( [grid, table])


class WidgetTableInput(Widget.Widget):
  """
  :category: Widget
  :rubric: PY
  :type: Structured component
  :dsc:
    Simple example of Widget using a table and adding some pre defined events on it.
  """
  name, label = 'Widget Table Input', 'Table input widget'

  @classmethod
  def getData(cls, aresObj, params):
    import random
    return  [
      {'ptf': "A", 'prd': random.randrange(-1, 4), 'comm': ''},
      {'ptf': "B", 'prd': random.randrange(-1, 4), 'comm': '10'},
      {'ptf': "B", 'prd': random.randrange(-1, 4), 'comm': 'Youpi'},
      {'ptf': "C", 'prd': random.randrange(-1, 4), 'comm': random.randrange(1, 100)}
    ]

  def html(self, params):
    import random

    data = self.getData(self.aresObj, params)
    table = self.aresObj.table(data,
                               header=[ {"data": "ptf", "title": "Alias", 'display': 'select', 'items': ['A', 'B', 'C', 'D'] },
                                        {"data": "prd", "title": "", "display": "signal", 'signal_dsc': 'RRRRRR'},
                                        {"data": "comm", "title": "Comment", "display": "comment", "width": 200}],
                               htmlCode='MyTable',
                               saveRow={"url": '/admin/test', 'success': ''}
                               )
    table.setHeader( [ {'title': 'Super', 'colspan': 2, 'rowspan': 1}, {'title': 'Youpi', 'colspan': 2, 'rowspan': 1}])
    table.addEventCol( 'fas fa-save', [table.jsUpdateRow(jsData={'row': {'ptf': "D", 'prd': random.randrange(-1, 1), 'comm': '10'}, 'row_id': 1}, isPyData=True)] )
    button = self.aresObj.button("Get Data")
    button.click( self.getSource( [table], table.jsLoad() ) )
    return self.aresObj.col( [table, button])