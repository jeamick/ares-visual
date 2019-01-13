#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.configs.List import Mixin


class MixinFiles(Mixin.ListBase):
  alias = "files-list"

  def template(self, withHr=True):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.templateFiles(withHr=True) # If bottom border
    :dsc:
        Python template to display the content of an message item.
        The record expected for those items are a bit special.
        Each items should get the below keys
          rec = {"url": "", "icon": '', "title": ''}
    :return: The Python object itself
    """
    self.addGlobalVar("LIST_CHECKS", "{}")
    self.addGlobalFnc('UpdateListChecks(srcObj)', '''
      var htmlId = $(srcObj).parent().parent().parent().attr('id') ;
      var value = $(srcObj).next().next().text() ;
      if (LIST_CHECKS[htmlId] == undefined) { LIST_CHECKS[htmlId] = {} }
      if ( $(srcObj).prop( "checked" ) ) { LIST_CHECKS[htmlId][value] = true; }
      else { delete LIST_CHECKS[htmlId][value]; }
      ''')

    self.addGlobalFnc('FileNameEvent(srcObj)', '''
      if ( $(srcObj).prev().attr('class') == 'far fa-file-alt' ) { 
        $('<form method="POST" action="/transfer/viewer/file/%(reportName)s" target="_blank"><input type="hidden" name="filename" value="'+ $(srcObj).text() +'"></form>').appendTo('body').submit();
      }
      if ( $(srcObj).prev().attr('class') == 'far fa-folder' ) {
        $('<form method="POST" action="/transfer/viewer/files/%(reportName)s" target="_blank"><input type="hidden" name="filename" value="'+ $(srcObj).text() +'"></form>').appendTo('body').submit();
      }
      ''' % {'reportName': self.aresObj.run.report_name})
    self.jsChecked = "LIST_CHECKS['%s']" % self.htmlId
    return self._template('''
      <div class="''' + self.addPyCss('CssDivRow', toMainStyle=False) + '''">
        <input type="checkbox" onclick="UpdateListChecks(this)" style="margin-right:20px;" />
        <i class="%(icon)s" style="padding-top:5px"></i>
        <span style="margin-left:20px;color:blue;cursor:pointer" onclick="FileNameEvent(this)">%(filename)s</span>
        <span style="margin-left:20px;font-style:italic;color:grey">%(size)s</span>
        <span style="float:right">%(lst_update)s</span>
      </div>''' + '<hr style="padding:0;margin:0" />' if withHr else '')

