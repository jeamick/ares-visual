#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.configs.List import Mixin


class MixinMultiSelect(Mixin.ListBase):
  """
  :category: List
  :rubric: JS
  :type: Configuration
  :dsc:
    vrebrb
  """
  alias = "multi-select"

  def template(self):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.templateMultiSelect()
    :dsc:
        Python template a list with a multi select option. This list will store the selections and returns the list.
        No difference with the normal template on the record.
    """
    self.jsAction('selected', "far fa-list-alt", tooltip="Empty Selection", jsFncs=[
      '''
        LIST_STATE['%(htmlId)s'] = {} ;
        if ( $(this).attr('title') == 'Empty Selection') { 
          $(this).attr('title', 'Select all'); var newIcon = 'fas fa-times-circle' ; var color = 'red';
          $('#%(htmlId)s').get(0).childNodes.forEach( function(rec) {
           $(rec).find('[name=status]').attr('class', newIcon).css('color', color);  }) ;}
        else { 
          $(this).attr('title', 'Empty Selection'); var newIcon = 'fas fa-check'; var color = 'green';
          $('#%(htmlId)s').get(0).childNodes.forEach( function(rec) {
           LIST_STATE['%(htmlId)s'][rec.textContent] = true; 
           $(rec).find('[name=status]').attr('class', newIcon).css('color', color); }) ;
          } ''' % {'htmlId': self.htmlId}])

    self.addGlobalFnc('ChangeSection(srcObj)', '''
      var iconItem = $(srcObj).find('i') ; var htmlId = $(srcObj).parent().parent().attr('id') ;
      if ( iconItem.hasClass('fas fa-check') ) {  
        $(srcObj).find('i').attr('class', 'fas fa-times-circle').css('color', 'red'); 
        LIST_STATE[htmlId][ $(srcObj).find('span').text() ] = false; }
      else { 
        $(srcObj).find('i').attr('class', 'fas fa-check').css('color', 'green'); 
        LIST_STATE[htmlId][ $(srcObj).find('span').text() ] = true;
      }; ''')

    self.aresObj.jsOnLoadFnc.add("LIST_STATE['%s'] = {}" % self.htmlId  )
    self._template("<div onclick='ChangeSection(this)' style='display:inline-block;cursor:pointer;width:100%;'><span style='display:inline-block;float:left'>%(label)s</span><i name='status' style='display:inline-block;float:right;color:green' class='fas fa-check'></i></div>")
    self._jsStyles['template'] = '%s;LIST_STATE["%s"][ rec["label"] ] = true;' % (self._jsStyles['template'], self.htmlId)
    self.addGlobalFnc('GetListDataMultiSelect(htmlId)', '''
              var res = []; $('#'+ htmlId).get(0).childNodes.forEach( function(rec) { res.push( {'label': rec.textContent, 'selected': LIST_STATE[htmlId][rec.textContent]} ) ; } ) ;
              return res;''', 'Return the items and the selected state of an AReS list')
    self.valFnc = 'GetListDataMultiSelect'
    return self


class MixinMultiSelectWithFilter(Mixin.ListBase):
  alias = "multi-select-filters"

  def template(self):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.templateMultiSelectWithFilters()
    :dsc:
        Python template to display a multi select list with a filter option.
        No difference with the normal template on the record.
    :return: The python object itself
    """
    self.jsAction('selected', "far fa-list-alt", tooltip="Empty Selection", jsFncs=[
      '''
        LIST_STATE['%(htmlId)s'] = {} ;
        if ( $(this).attr('title') == 'Empty Selection') { 
          $(this).attr('title', 'Select all'); var newIcon = 'fas fa-times-circle' ; var color = 'red';
          $('#%(htmlId)s').get(0).childNodes.forEach( function(rec) {
           $(rec).find('[name=status]').attr('class', newIcon).css('color', color);  }) ;}
        else { 
          $(this).attr('title', 'Empty Selection'); var newIcon = 'fas fa-check'; var color = 'green';
          $('#%(htmlId)s').get(0).childNodes.forEach( function(rec) {
           LIST_STATE['%(htmlId)s'][rec.textContent] = true; 
           $(rec).find('[name=status]').attr('class', newIcon).css('color', color); }) ;
          } ''' % {'htmlId': self.htmlId} ])

    self.addGlobalFnc('ChangeComplexSection(srcObj)', '''
      var iconItem = $(srcObj); var htmlId = $(srcObj).closest('ul').attr('id') ;
      var value = $(srcObj).parent().parent().find('[name=label]').text() ;
      if ( iconItem.hasClass('fas fa-check') ) {  
        iconItem.attr('class', 'fas fa-times-circle').css('color', 'red'); 
        LIST_STATE[htmlId][ value ] = false; }
      else { 
        iconItem.attr('class', 'fas fa-check').css('color', 'green'); 
        LIST_STATE[htmlId][ value ] = true; }; ''', "")

    self.addGlobalFnc('AddFilter(srcObj)', '''
      var target = $(srcObj).parent().parent().next() ;
      var div = $("<div style='width:100%;display:inline-block'></div>") ;
      div.append("<input type='text' style='float:left;width:85%'><i onclick='$(this).parent().remove()' style='float:right;margin:5px' class='fas fa-times'></i><i style='float:right;margin:5px' class='fas fa-bookmark'></i>");
      target.append(div) ; ''', "Add specific filter on a list item")

    self.aresObj.jsOnLoadFnc.add("LIST_STATE['%s'] = {}" % self.htmlId  )
    self.template('''<div style='display:inline-block;cursor:pointer;width:100%;'>
        <div style='display:inline-block;width:100%;'>
          <div name='label' style='position:relative;float:left;'>%(label)s</div>
          <div style='position:relative;float:right;'>
            <i class='fas fa-filter' onclick='AddFilter(this)' style='color:#293846'></i>
            <i name='status' class='fas fa-check' style='color:green' onclick='ChangeComplexSection(this)'></i>
          </div>
        </div>
        <div style='width:100%;background-color:#EEEEEE;padding:2px'></div>
      </div> ''')
    self._jsStyles['template'] = '%s;LIST_STATE["%s"][ rec["label"] ] = true;' % (self._jsStyles['template'], self.htmlId)

    self.addGlobalFnc('GetListDataMultiSelectWithFilter(htmlId)', ''' 
              var res = []; $('#'+ htmlId).get(0).childNodes.forEach( function(rec) {
                var filter = "" ;
                if ( rec.firstChild.lastElementChild.childNodes.length > 0) { filter = rec.firstChild.lastElementChild.childNodes[0].firstChild.value};
                res.push( {'label': rec.textContent, 'selected': LIST_STATE[htmlId][rec.textContent], 'filter': filter} ) ; } ) ;
              return res;''', 'Return the items and the selected state of an AReS list')
    self.valFnc = 'GetListDataMultiSelectWithFilter'
    return self


class MixinBadge(Mixin.ListBase):
  alias = "list-badge"

  def template(self):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.templateBadge()
    :dsc:
        Python template to display the content of an item with a badge value.
        The record with this template should follow the below structure:
            record = { "background": "", "color": "", "url": "", "value": '', "title": ""}
    :return: The Python object itself
    """
    return self._template('''
      <div style="width:100%;border-radius:2px;padding:1px 10px 1px 10px;margin-bottom:5px">
        <span style="color:black;background-color:%(background)s;color:%(color)s;border-radius:5px;padding:1px 10px;margin-right:10px">%(value)s</span><a href='%(url)s' target='_BLANK'>%(title)s</a>
      </div>''' )

