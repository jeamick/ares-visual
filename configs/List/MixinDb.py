#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
from ares.configs.List import Mixin


class ListMixinDbColumns(Mixin.ListBase):
  alias = "db-columns"

  item = '''
    <div style="display:inline-block;">
      <input name="colName" type="text" class="form-control" style="display:inline-block;margin-right:20px;width:200px;height:30px" placeholder="column name"/>
      <select name="colType" style="display:inline-block;margin-right:20px;width:200px;height:30px"><option>Text</option><option>Integer</option></select>
      <input name="colDefault" type="text" class="form-control" style="display:inline-block;margin-right:20px;width:400px;height:30px" placeholder="Default value" />
    </div>'''

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return 'GetListColVals("%s")' % self.htmlId

  def template(self):
    self.addGlobalFnc('GetListColVals(htmlId)', '''
      var jqObj = $("#"+ htmlId); var cols = [];
      jqObj.find('li').each(function(){
        cols.push( {colName: $(this).find('[name=colName]').val(), colType: $(this).find('[name=colType]').val(), colDefault: $(this).find('[name=colDefault]').val()} ) ;
      }) ; return cols ''')
    return self._template(self.item)

  def jsAdd(self, isPyData=False):
    return '''
      %(jqId)s.append('<li data-placement="right" class="list-group-item" style="border:none;padding:2px 5px 2px 5px">%(data)s</li>') ;
      ''' % {'clsLi': self.cssClsLi, 'data': self.item.replace("\n", ""), 'jqId': self.jqId}

