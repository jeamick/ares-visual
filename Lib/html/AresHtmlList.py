#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

# TODO fix issue with MarkDown conversion when use of ' "

import importlib
import os
import inspect
import re
import json

from ares.Lib.html import AresHtml
from ares.Lib import AresImports
from ares.Lib import AresMarkDown


# External package required
url_for = AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='url_for', sourceScript=__file__)
ares_pandas = AresImports.requires(name="pandas", reason='Missing Package', install='pandas', autoImport=True, sourceScript=__file__)


DSC = {
  'eng': '''

:dsc:
    List of all the different templates configurations available for displaying bespoke lists.
    This list can be extended and it is easy to test a new configuration by different defining the HTML template in the common list object.
    List are standard and very popular HTML objects, please have a look at the below websites if you need further information to manipulate them in your report
'''
}


class List(AresHtml.Html):
  """ Python wrapper to the HTML List element

  :example
  aresObj.list( [{'label': 'windows', 'url': 'google'}, {'label': 'Mac'}])
  """
  cssClsLi = "list-group-item"
  references = {'List W3C': 'https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp',
                'Icons': 'http://astronautweb.co/snippet/font-awesome/'}
  name, category, callFnc, docCategory = 'Simple List', 'List', 'list', 'Standard'
  __pyStyle = ['CssBasicList']
  __reqCss, __reqJs = ['bootstrap', 'font-awesome'], ['jquery', 'bootstrap']
  dashboards = ['DashBoardList']
  cssTitle = "CssTitle4"

  def __init__(self, aresObj, recordSet, icon, title, width, widthUnit, height, heightUnit, draggable, draggableGroupId, draggableMax, dfColumn,
               dataSrc, htmlCode, searchable, selectable, grid, template, globalFilter):
    self.icon, self.title, self.searchable, self.dataSrc, self._jsActions = icon, title, searchable, dataSrc, {}
    self.dsc, self._definedActions = "", []
    if recordSet is None:
      if dataSrc is None:
        recordSet = []
      else:
        self.aresObj = aresObj
        if dataSrc.get('on_init', False):
          recordSet = self.onInit(None, dataSrc)
    if issubclass( type(recordSet), ares_pandas.DataFrame):
      recordSet = recordSet[dfColumn].drop_duplicates().tolist()
    if isinstance(recordSet, dict):
      recordSet = [ {"label": k, "value": v} for k, v in recordSet.items()]
    super(List, self).__init__(aresObj, {'vals': recordSet, 'options': {'draggable': draggable, 'groupId': draggableGroupId, 'max': draggableMax}},
                               width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, htmlCode=htmlCode, globalFilter=globalFilter)
    self.valFnc = 'GetListData'
    if selectable:
      # Add the selection to a click event
      self.css({'cursor': 'pointer'})
      self.jsFrg('click', " $(this).parent().children().removeClass( 'text-primary' ); $(this).addClass( 'text-primary' ); %s['params']['%s'] = [$(this).text()];" % (self.aresObj.jsGlobal.breadCrumVar, self.htmlId))
      self.valFnc = 'GetListDataSelect'
      self.addGlobalFnc('GetListDataSelect(htmlId)', "return %(breadCrumVar)s['params'][htmlId];" % {"breadCrumVar": self.aresObj.jsGlobal.breadCrumVar}, 'Return the items present in an AReS list')
    self._jsStyles = {'li': {"padding": "2px 5px 2px 5px"} }
    if not grid:
      self._jsStyles['li']['border'] = 'none'
    self.addGlobalVar("LIST_STATE", "{}")
    if draggable:
      self.css({'cursor': 'pointer', 'background': '#eee'} )
    self.css({"overflow-y": 'hidden'})
    if template is not None:
      # Load the list definition from a pre defined template
      # This template can override some existing functions in order to make the list more specific
      # This can be considered (at least I do) as a Mixin !
      import ares.configs.List
      for script in os.listdir(os.path.dirname(ares.configs.List.__file__)):
        if script.startswith('Mixin') and script.endswith('py'):
          for name, obj in inspect.getmembers(importlib.import_module("ares.configs.List.%s" % script.replace(".py", "")), inspect.isclass):
            if hasattr(obj, 'alias') and obj.alias == template:
              self.__class__ = type("%s%s" % (self.__class__.__name__, obj.__name__), (obj, self.__class__), {})
              self.template()
              if self.htmlCode is None: # The htmlId should be reset to the new class name
                self.jsVal = "%s_data" % self.htmlId
              break

          else:
            continue

          break
      else:
        raise Exception("Template configuration %s for list not found !!!" % template)

  @property
  def json(self):
    return "JSON.stringify(%s('%s')) " % (self.valFnc, self.htmlId)

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return '$(this).text()'

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    cssMod = self.aresObj.cssObj.get("CssBasicListItems")
    if cssMod is not None:
      self.addPyCss("CssBasicListItems")
      itemStyle = cssMod().classname
    else:
      itemStyle = ""
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' htmlObj.empty() ;
      if (Array.isArray( data ) ) {
        var tmpData = {vals: []} ;
        data.forEach( function(rec) { 
          if (jsStyles.template != undefined) { tmpData.vals.push( rec ) } else { tmpData.vals.push( {label: rec } ) } } ) ;
        data = tmpData} 
      else if (Array.isArray( data.vals ) && !(typeof data.vals[0] === 'object'  ) ) {
        var tmpData = {vals: [] } ;
        data.vals.forEach( function(rec) { tmpData.vals.push( {label: rec } ) } ) ;
        data.vals = tmpData.vals } ;

      data.vals.forEach(function(rec){
        var label = rec.label; var dataVal = rec.label;
        if (rec.value != undefined) { dataVal = rec.value};
        if (jsStyles.template != undefined) { eval( jsStyles.template );} ;
        if (jsStyles.events != undefined) { jsStyles.events.forEach( function(rec) { label = label + rec } ) };
        if (jsStyles.close != undefined) { label = label + jsStyles.close} ;
        if (rec.dsc == undefined) { rec.dsc = "" } ;
        if (rec.url != undefined) { label = "<a href='"+ rec.url +"' style='color:%(blackColor)s'>" + label + "</a>"} ;
        var li = $('<li data-placement="right" data-value="'+ dataVal +'"  title="'+ rec.dsc +'" class="%(itemStyle)s"></li>').css( jsStyles['li'] )  ;
        li.append(toAresMarkup(label));
        htmlObj.append(li)
      }); 

      htmlObj.find('li').tooltip(); 
      if ( data.options != undefined && data.options.draggable) {
         if ( data.options.groupId != null) {
          htmlObj.addClass( data.options.groupId ) ; 
          if ( data.options.max != null ) { 
            htmlObj.sortable( {placeholder: "ui-state-highlight", 
              receive: function(event, ui) { if (htmlObj.children().length > data.options.max) { $(ui.sender).sortable('cancel'); } },
              dropOnEmpty: true, connectWith: "." + data.options.groupId} )
          } else {
            htmlObj.sortable( {placeholder: "ui-state-highlight", dropOnEmpty: true, connectWith: "." + data.options.groupId} ) 
          }}
         else { 
          if ( data.options.max != null ) { 
            htmlObj.sortable( {placeholder: "ui-state-highlight", 
              receive: function(event, ui) { if (htmlObj.children().length > data.options.max) { $(ui.sender).sortable('cancel'); } },
              dropOnEmpty: true, connectWith: "." + data.options.groupId} )
          } else {
            htmlObj.sortable( {placeholder: "ui-state-highlight", dropOnEmpty: true, connectWith: "." + data.options.groupId} ) 
          } } ;
         htmlObj.disableSelection() ;
      } ''' % {"blackColor": self.getColor('greyColor', 8), "itemStyle": itemStyle}, 'Javascript Object builder')

  def __add__(self, rec):
    """ Add items to a container """
    self.vals['vals'].append(rec)
    return self

  @property
  def eventId(self): return "#%s li" % self.htmlId

  @property
  def jsQueryData(self):
    """
    :category: Javascript features
    :dsc: Python function to define the Javascript object to be passed in case of Ajax call internally or via external REST service with other languages
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    return "{ event_val: $(event.currentTarget).data('value'), event_label: $(event.currentTarget).text(), event_data: %s, event_code: '%s' }" % (self.json, self.htmlId)

  def jsLoadFromSrc(self, jsData='data', jsDataKey=None, isPyData=False):
    if self.dataSrc['type'] == 'flask':
      url = url_for("%s.%s" % (self.dataSrc['blueprint'], self.dataSrc['fnc'].__name__), **dict(zip(self.dataSrc['pmts_def'], self.dataSrc['pmts'])) )
      return self.aresObj.jsPost(url, jsData=self.dataSrc.get('htmlObjs'), htmlCodes=self.dataSrc.get('htmlCodes'), jsFnc=[self.jsGenerate(jsData, jsDataKey=jsDataKey, isPyData=isPyData)])
    else:
      return self.aresObj.jsPost(self.dataSrc['script'], jsData=self.dataSrc.get('htmlObjs'), htmlCodes=self.dataSrc.get('htmlCodes'), jsFnc=[self.jsGenerate(jsData, jsDataKey=jsDataKey, isPyData=isPyData)] )

  def click(self, jsFncs):
    """
    :category: Javascript features
    :example: myObj.click( aresObj.jsConsole() )
    :dsc:
      This will create a Jquery click event and the data passed as parameter will be the ones defined in the function jsQueryData.
      Most of those parameters are common accross all AReS objects and they can be used directly in services done in Python or other languages
      By default all the js Python function will use as data the dictionary from jsQueryData
    :link Jquery Documentation: https://api.jquery.com/click/
    :return: self
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    self.css({'cursor': 'pointer'})
    return self.jsFrg('click', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)

  def delete(self, url=None, jsData=None, jsFncs='', cacheObj=None, isPyData=True, isDynUrl=False, httpCodes=None, htmlCodes=None):
    """
    :category: Javascript Event
    :rubric: JS
    :example: >>> myObj.delete( jsFncs=[aresObj.jsPost("test.py", jsFnc=[aresObj.jsConsole() ]) ])
    :dsc:
      Set a delete button to each item in the list. This can be enhanced with a special Ajax or simple javascript function
    :return: The python object itself
    """
    self._jsStyles[ 'close'] = "<i onclick='DeleteItem(event, this)' style='position:absolute;right:5px;color:#C00000' class='far fa-times-circle'></i>"
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    jsFncs.append("$(srcObj).parent().remove()")
    if url is not None:
      jsFncs = self.aresObj.jsPost(url=url, jsData=jsData, jsFncs=jsFncs, cacheObj=cacheObj, isPyData=isPyData, isDynUrl=isDynUrl,
                                   httpCodes=httpCodes, htmlCodes=htmlCodes)
    self.addGlobalFnc('DeleteItem(event, srcObj)', '''
          var data = $(srcObj).parent().text() ;
          %(jsFncs)s; event.stopPropagation(); ''' % {'jsFncs': ';'.join(jsFncs)}, "Delete an item from the list")
    return self

  def jsAction(self, action, icon, pyCssCls="CssSmallIcon", tooltip="", url=None, jsData=None, jsFncs=None, httpCodes=None):
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs] if jsFncs is not None else []

    # Add this to an ajax POST call if an URL is defined
    fnc = self.aresObj.jsPost(url=url, jsData=jsData, jsFnc=jsFncs, httpCodes=httpCodes) if url is not None else ";".join(jsFncs)
    self._jsActions[action] = "<span id='%(htmlId)s_%(action)s' title='%(tooltip)s' class='%(cssStyle)s %(icon)s'></span>" % {
      "icon": icon, "cssStyle": self.addPyCss(pyCssCls), "htmlId": self.htmlId, 'tooltip': tooltip, 'action': action}
    self.aresObj.jsOnLoadFnc.add("$('#%(htmlId)s_%(action)s').on('click', function(event) { %(jsFncs)s; })" % {"htmlId": self.htmlId, "jsFncs": fnc, 'action': action})
    if action not in self._definedActions:
      self._definedActions.append(action)
    return self

  def jsItemAction(self, icon, jsFncName, jsFncs):
    """
    :return:
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    if not 'events' in self._jsStyles:
      self._jsStyles['events'] = []
    self.css( {'cursor': 'pointer'} )
    self._jsStyles['events'].append("<i name='%s' style='position:absolute;right:%spx;color:black' class='%s'></i>" % (jsFncName, (len( self._jsStyles['events'])+1) * 20 + 5, icon ))
    self.aresObj.jsOnLoadFnc.add('''$(document).on('click', 'i[name="%s"]' , function(event) { var data = $(this).parent().text() ; %s })''' % (jsFncName, ';'.join(jsFncs)) )

  def jsAdd(self, data='data', isPyData=False):
    """
    :category: Javascript features
    :example: myObj.jsAdd( )
    :dsc:
      This function will allow to set a function to add from the browser and the user input new entries in a list
    :return: The String corresponding to the add of an item in a list from the data input dictionary
    """
    if isPyData:
      data = json.dumps(data)
    return '''
      %(jqId)s.append('<li class="%(clsLi)s" style="white-space:nowrap;padding:5px;background-color:%(lightBlue)s">' + %(data)s + '<i style="float:right;cursor:pointer" onclick="$(this).parent().remove()" class="far fa-times-circle"></i></li>') ;
      ''' % {'clsLi': self.cssClsLi, 'data': data, 'jqId': self.jqId, 'lightBlue': self.getColor('blueColor', 14)}

  def jsEvents(self):
    if hasattr(self, 'jsFncFrag'):
      for eventKey, fnc in self.jsFncFrag.items():
        if self.htmlCode is not None:
          fnc.insert(0, self.jsAddUrlParam(self.htmlCode, self.val, isPyData=False))
        self.aresObj.jsOnLoadEvtsFnc.add('''
          $( document ).on('%(eventKey)s', '%(eventId)s', function(event) {
            var useAsync = false; var data = %(data)s ;
            if (!$('#body_loading').length){ 
              var bodyLoading2 = $('<div id="body_loading" name="ares_loading" style="bottom:20px;left:70px;position:fixed;background-color:#F4F4F4;padding:5px"><i class="fas fa-spinner fa-spin" style="margin-left:10px;margin-right:10px"></i><div style="display:inline" id="loading_count">0</div> process running...</div>') ; } ;
            $('body').append(bodyLoading2) ; $('#loading_count').html( parseInt($('#loading_count').html()) + 1) ;
            %(jsFnc)s ; 
            if (!useAsync) {
              $('#loading_count').html( parseInt($('#loading_count').html()) - 1) ;
              if ($('#loading_count').html() == '0') { $('#body_loading').remove() ;} }
          }) ;''' % {'eventId': self.eventId, 'eventKey': eventKey, 'data': self.jsQueryData, 'jsFnc': ";".join([f for f in fnc if f is not None])})


  # -----------------------------------------------------------------------------------------
  #                                    LIST EXPORT OPTIONS
  # -----------------------------------------------------------------------------------------
  def __str__(self):
    """ Return the String representation of a HTML List """
    self.css({'overflow': 'auto', 'list-style-type': 'none', 'display': 'inline-block', 'margin': '0',
              'margin-right': '10px', 'padding': '0 5px 0 5px'})

    self.addGlobalFnc('GetListData(htmlId)', '''
          var res = [];
          $('#'+ htmlId + ' li').each(function(item){
            if ( $(this).children().length == 1) { res.push($( this ).find('a').html()) ;}
            else { res.push($( this ).html()) ;}}); return res''',
        'Return the items present in an AReS list')
    self.addGlobalFnc('SearchListData(htmlId)', '''
      $('#'+ htmlId + ' li').each( function(item){
        if ( $(this).text().indexOf( $('#'+ htmlId + '_search').val()) > -1) { $(this).show() ; }
        else { $(this).hide() ; $('#'+ htmlId).css({'overflow': 'hidden'}) }
      }) ''', 'Simple search function in an AReS list')

    icon = '<div style="width:100%%;text-align:center;font-size:50px">' % self.icon if self.icon is not None else ''
    searchableStr = ''

    events = []
    for action in self._definedActions:
      if action in self._jsActions:
        events.append(self._jsActions[action])

    cssMod, title4 = self.aresObj.cssObj.get(self.cssTitle), ""
    if cssMod is not None:
      self.addPyCss(self.cssTitle)
      title4 = cssMod().classname
    if self.dsc != '':
      self.dsc = "<div style='width:100%%;padding-bottom:5px;text-align:justify'>%s</div>" % self.dsc
    if self.searchable:
      searchableStr = '''
        <div style="width:100%%;padding:5px 0 5px 0;display:inline-block">
          <div onclick="SearchListData('%(htmlId)s')" style="margin-bottom:-60px;margin-right:4px;position:relative;float:right;cursor:hand;cursor:pointer;height:29px;font-size:12px;"><i class="fas fa-search"></i></div>
          <input onkeyup="SearchListData('%(htmlId)s')" id="%(htmlId)s_search" style="width:100%%;color:#777;" type="text" placeholder="Search for" />
        </div>
        ''' % {'htmlId': self.htmlId }
    return '''
      <div %(attr)s style="display:inline-block;width:100%%">
        <div style="margin-bottom: 5px">
          <i class="%(icon)s"></i><span style="cursor:initial" class="%(title4)s">%(title)s</span> 
           %(events)s
        </div>
        %(searchableStr)s
        %(dsc)s
        <ul id="%(htmlId)s" class="list-group"></ul>
      </div>%(helper)s''' % {'searchableStr': searchableStr, 'htmlId': self.htmlId, "attr": self.strAttr(pyClassNames=['CssBasicList'], withId=False), 'blackColor': self.getColor('greyColor', 8),
                             "icon": icon, "title": self.title, "helper": self.helper, "events": "".join(events),
                             "title4": title4, "dsc": self.dsc}

  def to_word(self, document):
    from docx.shared import RGBColor

    for rec in self.vals['vals']:
      if isinstance( rec, str):
        p = document.add_paragraph(style='ListBullet')
        runner = p.add_run( rec )
        if self.aresObj.http.get(self.htmlCode) == rec:
          runner.font.color.rgb = RGBColor(0x42, 0x24, 0xE9)
      else:
        document.add_paragraph(rec['label'], style='ListBullet')
        runner = p.add_run(rec)
        if self.aresObj.http.get(self.htmlCode) == rec['label']:
          runner.font.color.rgb = RGBColor(0x42, 0x24, 0xE9)

  def to_xls(self, workbook, worksheet, cursor):
    if self.title != '':
      cell_format = workbook.add_format({'bold': True})
      worksheet.write(cursor['row'], 0, self.title, cell_format)
      cursor['row'] += 1
    for rec in self.vals['vals']:
      cell = rec if isinstance(rec, str) else rec['label']
      cell_format = workbook.add_format({})
      if self.aresObj.http.get(self.htmlCode) == cell:
        cell_format = workbook.add_format({'bold': True, 'font_color': self.getColor('blueColor', 4)})
      worksheet.write(cursor['row'], 0, cell, cell_format)
      cursor['row'] +=1
    cursor['row'] += 1


  # --------------------------------------------------------------------------------------------------------------
  #                                   TEMPLATE ITEM SECTION
  #
  # Simple templates should be defined in the config / List section
  # The ones below are more complex and they are using some events
  #
  def _template(self, strTemplate):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.template("%(filename)s, last update %(lst_update)s")
    :dsc:
        Python template to display the content of an item in the list.
        This should be a string using the Python formatting
    """
    strTemplate = "".join([line.strip() for line in strTemplate.split('\n')]).replace('"', "'") # Cannot use the " in the string as this is the javascript delimiter
    formatStr = re.compile("%\(([0-9a-zA-Z_]*)\)s")
    matches = formatStr.findall(strTemplate)
    if matches:
      for res in formatStr.finditer(strTemplate):
        strTemplate = strTemplate.replace(res.group(0), '"+ rec["%s"] +"' % res.group(1))
    self._jsStyles['template'] = 'value = "%s"' % strTemplate
    return self

  def templateMessageDetails(self, withHr=True, color='black', icon=''):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.templateMessageDetails(withHr=True) # If bottom border
    :dsc:
        Python template to display the content of an message item.
        The record expected for those items are a bit special.
        Each items should get the below keys
          rec = {"url": "", "content": '', "title": ''}
    :return: The Python object itself
    """
    if icon != '':
      icon = '<i class="%s" style="margin-right:5px"></i>' % icon
    self._template('''
      <div style="width:100%;display:inline-block">
        <div style="width:60px;float:left">
          <div style="font-size:14px">%(views)s <span style="font-size:10px">views</span></div>
          <div style="font-size:14px">%(answers)s <span style="font-size:10px">answers</span></div>
          <div style="font-size:14px">%(interest)s <span style="font-size:10px">interest</span></div>
        </div>
        <div>
          <a href='%(url)s' target='_blank' style='color:'''+ color +''';text-decoration:none;font-weight:bold;font-size:14px;color:"+ self.getColor('blueColor', 1) +"'>'''+ icon +'''%(title)s</a>
          <div style="white-space:pre-wrap;"></div>
        </div>
      </div>
      ''' + '<hr />' if withHr else '' )
    return self

  def templateIdeas(self, jsFncs, icon="fas fa-users", tooltip="Support Idea"):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.templateIdeas()
    :dsc:
        Python template to display an special item with different features ( visible in the feedback / idea section )
        The record expected for those items are a bit special.
        Each items should get the below keys
            record = {"title": "", "color": "", "id": "", "icon": "", "content": "", "count": ""}
    :return: The Python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    self.addGlobalFnc('IdeaEvent(scrId)', ''' var data = {event_val: scrId } ; %(jsFncs)s ''' % {"jsFncs": ";".join(jsFncs)})

    self._template('''
      <div style="width:100%;border:1px solid %(color)s;border-radius:2px;padding:5px 10px 5px 10px;margin-bottom:5px">
        <span style="font-weight:bold;font-size:14px">%(title)s</span>
        <i onclick="IdeaEvent(%(id)s)" class="''' + icon + '''" title="''' + tooltip + '''" style="margin-left:15px;cursor:pointer"><span class="badge" style="color:black">%(count)s</span></i>
        <br />
        <div style="width:100%;display:inline-block;margin-top:5px">
          <div style="display:inline-block;float:left;width:50px;text-align:center;">
            <i class="%(icon)s" style="color:%(color)s;font-size:20px;margin-left:5px"></i>
          </div>
          <div style="white-space:pre-wrap;">%(content)s</div>
        </div>
      </div>''' )
    return self

  def templateTags(self, url=None, jsFncs='', cacheObj=None, isDynUrl=False, httpCodes=None, htmlCodes=None):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.templateTags()
    :dsc:
        Python template to display the content of an item with a badge value.
        The record with this template should follow the below structure:
            record = { "value": "", "id": ""}
    :return: The Python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    jsFncs.append( "$(srcObj).remove() " )
    if url is not None:
      js = [self.aresObj.jsPost(url, jsFnc=jsFncs, cacheObj=cacheObj, isDynUrl=isDynUrl, httpCodes=httpCodes, htmlCodes=htmlCodes)]
    else:
      js = jsFncs
    self.addGlobalFnc('RemoveListTag(srcObj)', "var data = { event_val: $(srcObj).text() };  %s" % ";".join(js))
    self._template('''
      <div style="width:100%;border-radius:2px;padding:1px 10px 1px 10px;margin-bottom:5px">
        <span style="color:black;background-color:'''+ self.getColor('blueColor', 10) +''';border-radius:5px;padding:4px 10px;">%(value)s<i onclick="RemoveListTag($(this).parent())" class="fas fa-times" style="margin-left:20px;cursor:pointer"></i></span>
      </div>''' )
    return self

  def templateUrl(self, target='_self', color='black'):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.templateUrl()
    :dsc:
        Python template to display the content of an item with URL link
        The record expected for those items are a bit special.
        Each items should get the below keys
            record = { "url": "", "title": ""}
    :return: The Python object itself
    """
    self._template(''' <a href="%(url)s" style="white-space:pre-wrap;color:'''+ color +'''" target="'''+ target +'''">%(title)s</a>''')
    return self

  def templateAnswer(self, url=None, jsFncs='', cacheObj=None, isDynUrl=False, httpCodes=None, htmlCodes=None):
    """
    :category: Python List Item Template
    :rubric: PY
    :example: >>> myObj.templateAnswer()
    :dsc:
        Python template to display the items corresponding to an answer. Those items are visible in the section Questions / details in the framework.
        TThe record expected for those items are a bit special.
        Each items should get the below keys
            record = {"title": "", "borderColor": "", "color": "", "id": "", "icon": "", "author": "", "interest": "", "lst_mod_dt": "" }
    :return: The Python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    jsFncs.append("srcObj.append( '<span style=\"font-style:italic;width:100%;display:block\">' + msg + '</span>' )")
    if url is not None:
      js = [self.aresObj.jsPost(url, jsFnc=jsFncs, cacheObj=cacheObj, isDynUrl=isDynUrl, httpCodes=httpCodes, htmlCodes=htmlCodes)]
    else:
      js = jsFncs
    self.addGlobalFnc('AddExtraComment(srcObj, msg, rowId)', "var data = { event_val: msg, event_id: rowId }; %s" % ";".join(js))
    self.addGlobalFnc('AnswerInterest(answerId, value)', self.aresObj.jsPost("'/questions/answer/ranking/' + answerId + '/' + value", isDynUrl=True) )

    self._template('''
      <div style="display:block;width:100%;border-radius:5px;border:1px solid %(borderColor)s;background-color:%(borderColor)s;color:%(color)s">
        <div style="display:block;width:50px;float:left;height:100%;">
          <i onclick="AnswerInterest(%(id)s, 1)" class="fas fa-caret-up" style="cursor:pointer;color:#C9CBCF;width:100%%;display:block;font-size:40px;text-align:center"></i>
          <span style="color:#C9CBCF;width:100%%;display:block;font-size:30px;text-align:center"> %(interest)s </span>
          <i onclick="AnswerInterest(%(id)s, -1)" class="fas fa-caret-down" style="cursor:pointer;color:#C9CBCF;width:100%%;display:block;font-size:40px;text-align:center"></i>
        </div>
        <div style='padding:10px;text-align:left;display:block;margin-left:50px;'>
          <span style='font-size:14px;display:inline-block;width:100%;white-space:pre-wrap;line-height:1.4;'>%(answer)s</span>
          <div style='margin-top:10px;text-align:right;width:100%;font-style:italic;'>%(author)s, %(lst_mod_dt)s</div>
          <hr style="margin-bottom:0px">
          <div id='%(id)s_extra' style='margin:0px;padding:0px'>%(xtra)s</div>
          <input type='text' class='form-control' style='margin-top:5px;width:100%' onkeydown='if (event.keyCode == 13) {  AddExtraComment($(this).prev(), $(this).val(), %(id)s ) }' />
          <hr style="margin:10px 20%;background:#888888">
        </div> 
      </div> ''')

    self._jsStyles['template'] = 'var xtra = []; rec["xtra"].forEach( function(val) { xtra.push("<span style=\'white-space:pre-wrap;font-style:italic;width:100%%;display:block\'>" + val + "</span>"); } ); rec["xtra"]=xtra.join(""); %s;' % self._jsStyles['template']
    return self


  # -----------------------------------------------------------------------------------------
  #                                    MARKDOWN SECTION
  # -----------------------------------------------------------------------------------------
  @staticmethod
  def matchMarkDownBlock(data): return re.match(">>>List", data[0])

  @staticmethod
  def matchEndBlock(data): return data.endswith("<<<")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj=None):
    records, pmts, css = [], {'selectable': False}, {}
    for val in data[1:-1]:
      val = val.strip()
      if val.startswith("@"):
        dataAttr = val[1:].strip().split(";")
        for d in dataAttr:
          a, b = d.split(":")
          css[a] = b
      elif val.startswith("--"):
        dataAttr = val[2:].strip().split(";")
        for d in dataAttr:
          a, b = d.split(":")
          pmts[a] = b
      else:
        records.append({"label": val.strip()})
    if aresObj is not None:
      getattr(aresObj, 'list')(records, **pmts).css(css)
    return ["aresObj.list(%s, selectable=False)" % json.dumps(records)]

  @classmethod
  def jsMarkDown(self, vals):
    return [">>>List", [rec for rec in vals['label']], "<<<"]


class ListBadge(AresHtml.Html):
  """ Python wrapper to the bootStrap List badge HTML component

  :example
  aresObj.listbadge( [{'label': 'windows', 'url': 'google', 'value': 12}, {'label': 'Mac', 'value': 4}])
  aresObj.listbadge([{"value": "132", "label": " Write markdown text in this textarea."}, {"value": "4.92", "label": " Click 'HTML Preview' button."}])
  """
  cssCls, cssClsLi = ['list-group'], "list-group-item"
  references = {'List W3C': 'https://www.w3schools.com/bootstrap/bootstrap_list_groups.asp',
                'List Bootstrap': 'https://v4-alpha.getbootstrap.com/components/list-group/'}
  __pyStyle = ['CssDivNoBorder']
  __reqCss, __reqJs = ['bootstrap'], ['bootstrap']
  name, category, callFnc, docCategory = 'List Badges', 'Container', 'listbadge', 'Advanced'
  mocks = [
    {'label': 'Python', 'url': 'https://www.python.org/', 'value': 100, 'color': 'red'},
    {'label': 'R', 'value': 90},
  ]

  def __init__(self, aresObj, recordSet, color, size, width, widthUnit, height, heightUnit, draggable, draggableGroupId, draggableMax, dfColumn):
    if issubclass(type(recordSet), ares_pandas.DataFrame):
      tmpDict = recordSet[dfColumn].value_counts().to_dict()
      recordSet = [{'label': k, 'value': int(v)} for k, v in tmpDict.items()]
    if recordSet:
      if isinstance(recordSet[0], str):
        recordSet = [ {'label': val, 'value': 0} for val in recordSet ]
    super(ListBadge, self).__init__(aresObj, {'vals': recordSet, 'options': {'draggable': draggable, 'groupId': draggableGroupId, 'max': draggableMax}}, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    self.color = self.getColor('baseColor', 2) if color is None else color

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
      data.vals.forEach(function(rec){
        if (rec.url != undefined) { var content = '<a href="' + rec.url + '">' + rec.label + '</a>' ;} else {var content = rec.label;};
        if (rec.color == undefined) { rec.color = '%(color)s'; };
        if (rec.size == undefined) { rec.size = '%(size)s'; };
        htmlObj.append('<li class="%(clsLi)s">'+ content +'&nbsp;<span class="badge" style="background-color:' + rec.color + ';color:white;font-size:' + rec.size + 'px">'+ rec.value +'</span></li>') ; 
      }) ;
      if ( data.options.draggable) {
         if ( data.options.groupId != null) {
          htmlObj.addClass( data.options.groupId ) ; 
          if ( data.options.max != null ) { 
            htmlObj.sortable( {placeholder: "ui-state-highlight", 
              receive: function(event, ui) { if (htmlObj.children().length > data.options.max) { $(ui.sender).sortable('cancel'); } },
              dropOnEmpty: true, connectWith: "." + data.options.groupId} )
          } else {
            htmlObj.sortable( {placeholder: "ui-state-highlight", dropOnEmpty: true, connectWith: "." + data.options.groupId} ) 
          }}
         else { 
          if ( data.options.max != null ) { 
            htmlObj.sortable( {placeholder: "ui-state-highlight", 
              receive: function(event, ui) { if (htmlObj.children().length > data.options.max) { $(ui.sender).sortable('cancel'); } },
              dropOnEmpty: true, connectWith: "." + data.options.groupId} )
          } else {
            htmlObj.sortable( {placeholder: "ui-state-highlight", dropOnEmpty: true, connectWith: "." + data.options.groupId} ) 
          } } ;
         htmlObj.disableSelection() ;
      }
      ''' % {'color': self.color, 'size': self.size, 'clsLi': self.cssClsLi}, 'Javascript Object builder')

  def __str__(self):
    """ Return the String representation of a HTML List """
    self.addGlobalFnc('GetListData(htmlId)', '''
      var res = []; $('#'+ htmlId + ' li').each(function(item){
      if ( $(this).children().length == 1) { res.push($( this ).find('a').html()) ;} else { res.push($( this ).html()) ;}}); return res;''',
      'Returns the HTML text of all the items in the object')
    return '<div %s><ul></ul></div>%s' % (self.strAttr(pyClassNames=self.pyStyle), self.helper)

  @staticmethod
  def matchMarkDownBlock(data): return re.match(">>>Badge", data[0])

  @staticmethod
  def matchEndBlock(data): return data.endswith("<<<")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj):
    recordSet = []
    for val in data[1:-1]:
      splitData = val.split("|")
      if len(splitData) == 1:
        splitData.append(0)
      recordSet.append( {'label': splitData[0], "value": splitData[1]})
    if aresObj is not None:
      getattr(aresObj, 'listbadge')(recordSet)
    return ["aresObj.listbadge(%s)" % json.dumps(recordSet)]

  @classmethod
  def jsMarkDown(self, vals):
    return [">>>Badge", ["%s|%s" % (rec['value'], rec['label']) for rec in vals['vals']], "<<<"]


class HtmlListAccordeon(AresHtml.Html):
  """ Python wrapper for the accordeon list

  :example
  aresObj.accordeon([{'value': 'super', 'url': "google", 'category': 'Test', 'icon': 'fas fa-heart'},
                     {'value': 'super2', 'url': "google", 'category': 'Youpi', 'icon': 'fab fa-google'},
                     {'value': 'super3', 'url': "google", 'category': 'Youpi'}])
  """
  references = {'Accordean W3C': 'http://designbump.com/create-a-vertical-accordion-menu-using-css3-tutorial/',
                'Example Jquery': 'http://thecodeplayer.com/walkthrough/vertical-accordion-menu-using-jquery-css3'}
  __pyStyle = ['CssHreftMenu', 'CssHrefSubMenu', 'CssListNoDecoration', 'CssListLiSubItem', 'CsssDivBoxMargin',
               'CssListLiUlContainer']
  name, category, callFnc, docCategory = 'Vertical expendable list', 'List', 'accordeon', 'Advanced'
  __reqCss, __reqJs = ['bootstrap', 'font-awesome'], ['bootstrap', 'font-awesome']
  mocks = [
    {"value": 'Python', 'url': "https://www.python.org/", 'category': 'script'},
    {"value": 'R', 'url': "https://www.r-project.org/", 'category': 'script'},
    {"value": 'Javascript', 'url': "https://www.javascript.com/", 'category': 'script'},
    {"value": 'C#', 'category': 'code'},
  ]

  def __init__(self, aresObj, recordSet, color, width, widthUnit, size):
    color = color if color is not None else 'black'
    super(HtmlListAccordeon, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit)
    size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    self.css( {'color': color, 'font-size': size } )

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
      var categories = {} ; var cats = [] ; var catsIcons = {} ;  
      data.forEach(function(rec){
        if (rec.icon != undefined) { catsIcons[rec.category] = '<i class="' + rec.icon +'"></i>&nbsp;'} ;
        if (rec.category in categories) { categories[rec.category].push(rec) ; } 
        else { categories[rec.category] = [rec] ; cats.push(rec.category) ; }}) ;
      htmlId = htmlObj.attr('id') ;
      
      var countItems = 0 ;   
      cats.forEach(function(cat){
        if (cat in catsIcons) {var liItem = $('<li %(cssLi)s name="' + htmlId + '_menu" id="' + htmlId + '_menu_' + countItems +'"><a href="#">' + catsIcons[cat] + cat + '</a></li>') ;}
        else {var liItem = $('<li %(cssLi)s name="' + htmlId + '_menu" id="' + htmlId + '_menu_'+ countItems +'"><a href="#' + htmlId + '_menu_'+ countItems +'">' + cat + '</a></li>') ;}
        countItems = countItems + 1 ;
        var ulItem = $('<ul></ul>') ;
        categories[cat].forEach(function(rec){
          if (rec.color != undefined) { var content = 'style="color:' + rec.color + '"'; } else { var content = '';};
          ulItem.append('<li %(cssItems)s '+ content +'><a href="'+ rec.url + '">' + rec.value + '</a></li>') ;
        }) ;
        liItem.append(ulItem) ;
        htmlObj.append(liItem) ;
      }) ; ''' % {'cssLi': self.aresObj.cssObj.getClsTag(['CssListNoDecoration', 'CssHreftMenu', 'CssListLiUlContainer']),
                  'cssItems': self.aresObj.cssObj.getClsTag(['CssListNoDecoration', 'CssHrefSubMenu', 'CssListLiSubItem'])}, 'Javascript Object builder')

  def __str__(self):
    """ HTML representation of the accordeon list """
    self.aresObj.jsOnLoadFnc.add( "$('li[name=%(htmlId)s_menu]').click(function() {$('#' + this.id + ' ul').toggle() ;});" % {'htmlId': self.htmlId} )
    return '<div %s></div>' % self.strAttr(pyClassNames=['CsssDivBoxMargin'])


class Bullets(AresHtml.Html):
  """

  :example
  aresObj.points([{"label": row.replace("  * ", "")} for row in data])
  """
  name, category, callFnc, docCategory = 'Bullet points', 'List', 'points', 'Standard'
  __pyStyle = ['CssDivNoBorder']
  puce = "circle"
  references = {"W3C": "https://www.w3schools.com/html/html_lists.asp"}
  mocks = [ {'label': 'Python', 'url': 'https://www.python.org/'}, {'label': 'R'} ]

  def __init__(self, aresObj, recordSet, marginTop, level, width, widthUnit, height, heightUnit, selectable, multiselectable, htmlCode):
    if recordSet is not None and len(recordSet) > 0:
      if not isinstance( recordSet[0], dict ):
        tmpRecordSet = []
        for rec in recordSet:
          tmpRecordSet.append( {'label': rec } )
        recordSet = tmpRecordSet
    super(Bullets, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, htmlCode=htmlCode)
    self.listVal = "%(breadcrumb)s['params']['%(htmlId)s']" % {"breadcrumb": self.aresObj.jsGlobal.breadCrumVar, "htmlId": self.htmlId}
    if level is not None:
      self.addPyCss("CssTitle%s" % level)
      self.css("margin-left", "-20px")
    else:
      self.css("font-size", "%spx" % self.aresObj.pyStyleDfl['fontSize'])
    if marginTop is not None:
      self.css("margin-top", "%spx" % marginTop)
    if selectable:
      # Add the selection to a click event
      self.css( {'cursor': 'pointer'} )
      self.jsFrg('click', "$(this).parent().children().removeClass( 'text-primary' ); $(this).addClass( 'text-primary' ); %s['params']['%s'] = [$(this).text()];" % (
                 self.aresObj.jsGlobal.breadCrumVar, self.htmlId))
    if multiselectable:
      # Add the selection to a click event
      self.css( {'cursor': 'pointer'} )
      self.jsFrg('click', '''
        if ( data['event_val'] == undefined) { data['event_val'] = {} } ;
        if ( $(this).hasClass('text-primary') ) { delete data['event_val'][$(this).index()] ; } 
        else { data['event_val'][$(this).index()] = $(this).text() ; } ;
        %(breadcrumb)s['params']['%(htmlId)s'] = data['event_val'];
        $(this).toggleClass( 'text-primary' ); ''' % {"breadcrumb": self.aresObj.jsGlobal.breadCrumVar, "htmlId": self.htmlId})

  @property
  def jqId(self): return "$('#%s ul')" % self.htmlId

  @property
  def eventId(self): return "#%s li" % self.htmlId

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return self.listVal

  @property
  def json(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return "JSON.stringify(%s)" % self.listVal

  @property
  def jsQueryData(self):
    """
    :category: Javascript features
    :dsc: Python function to define the Javascript object to be passed in case of Ajax call internally or via external REST service with other languages
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    return "{ event_val: %s, event_code: '%s' }" % (self.listVal, self.htmlId)

  def jsEvents(self):
    if hasattr(self, 'jsFncFrag'):
      for eventKey, fnc in self.jsFncFrag.items():
        if self.htmlCode is not None:
          fnc.insert(0, self.jsAddUrlParam(self.htmlCode, self.val, isPyData=False))
        self.aresObj.jsOnLoadEvtsFnc.add('''
          $( document ).on('%(eventKey)s', '%(eventId)s', function(event) {
            var useAsync = false; var data = %(data)s ;
            if (!$('#body_loading').length){ 
              var bodyLoading2 = $('<div id="body_loading" name="ares_loading" style="bottom:20px;left:70px;position:fixed;background-color:#F4F4F4;padding:5px"><i class="fas fa-spinner fa-spin" style="margin-left:10px;margin-right:10px"></i><div style="display:inline" id="loading_count">0</div> process running...</div>') ; } ;
            $('body').append(bodyLoading2) ; $('#loading_count').html( parseInt($('#loading_count').html()) + 1) ;
            %(jsFnc)s ; 
            if (!useAsync) {
              $('#loading_count').html( parseInt($('#loading_count').html()) - 1) ;
              if ($('#loading_count').html() == '0') { $('#body_loading').remove() ;} }
          }) ;''' % {'eventId': self.eventId, 'eventKey': eventKey, 'data': self.jsQueryData, 'jsFnc': ";".join([f for f in fnc if f is not None])})

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
      data.forEach(function(rec){
        if (rec.url != undefined) { htmlObj.append('<li><a href="' + rec.url + '">' + toAresMarkup(rec.label) + '</a></li>') ;} 
        else { htmlObj.append('<li>' + toAresMarkup(rec.label) + '</li>')}}); 
        htmlObj.css('list-style-type', '%s') ;
        ''' % self.puce, 'Javascript Object builder')

  def click(self, jsFncs):
    """
    :category: Javascript features
    :example: myObj.click( aresObj.jsConsole() )
    :dsc:
      This will create a Jquery click event and the data passed as parameter will be the ones defined in the function jsQueryData.
      Most of those parameters are common accross all AReS objects and they can be used directly in services done in Python or other languages
      By default all the js Python function will use as data the dictionary from jsQueryData
    :link Jquery Documentation: https://api.jquery.com/click/
    :return: self
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    return self.jsFrg('click', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)

  def __str__(self):
    return '<div %s><ul style="text-align:left;vertical-align:middle;margin-bottom:0"></ul>%s</div>' % (self.strAttr(pyClassNames=self.pyStyle), self.helper)

  @classmethod
  def matchMarkDownBlock(cls, data): return re.match(">>>%s" % cls.callFnc, data[0])

  @staticmethod
  def matchEndBlock(data): return data.endswith("<<<")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj=None):
    recordSet = [ {"label":  val } for val in data[1:-1]]
    if aresObj is not None:
      getattr(aresObj, cls.callFnc)(recordSet)
    return ["aresObj.%s(%s)" % (cls.callFnc, json.dumps(recordSet)) ]

  @classmethod
  def jsMarkDown(cls, vals):
    return [">>>%s" % cls.callFnc, [rec['label'] for rec in vals], "<<<"]


class Squares(Bullets):
  name, category, callFnc, docCategory = 'Bullet squares', 'List', 'squares', 'Standard'
  __pyStyle, __reqJs, __reqCss = ['CssSquareList'], ['font-awesome'], ['font-awesome']
  puce = "none"


class NumberList(Bullets):
  """

  """
  puce, name, callFnc, docCategory = "decimal", 'List Numbers', 'listnumbers', 'Standard'
  __pyStyle = ['CssDivNoBorder']
  references = {"W3C": "https://www.w3schools.com/html/html_lists.asp",
                'List Types': 'https://www.w3.org/wiki/CSS/Properties/list-style-type'}


class LetterList(Bullets):
  """

  """
  puce, name, callFnc, docCategory = "lower-alpha", 'List letter', 'listletter', 'Standard'
  __pyStyle = ['CssDivNoBorder']
  references = {"W3C": "https://www.w3schools.com/html/html_lists.asp",
                'List Types': 'https://www.w3.org/wiki/CSS/Properties/list-style-type'}


class CheckList(AresHtml.Html):
  """

    :example
    aresObj.points([{"label": row.replace("  * ", "")} for row in data])
    """
  name, category, callFnc, docCategory = 'List Checked', 'List', 'checklist', 'Standard'
  __pyStyle = ['CssDivNoBorder']
  references = {"W3C": "https://www.w3schools.com/html/html_lists.asp"}
  mocks = [
    {'label': 'Python', 'url': 'https://www.python.org/', 'value': 100, 'color': 'red'},
    {'label': 'R', 'value': 90},
  ]

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit):
    super(CheckList, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.css( {"padding-left": "20px"} )

  @property
  def jqId(self): return "$('#%s')" % self.htmlId

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
        var cat = htmlObj.attr('id') + "_cat" ;
        data.forEach(function(rec){
          if (rec.isChecked == undefined) { 
            if (rec.disabled != undefined) { htmlObj.append('<input type="radio" name="'+ cat + '" disabled value="' + rec.value + '">' + rec.value + '<br>') ; }
            else { htmlObj.append('<input type="radio" name="'+ cat + '" value="' + rec.value + '">' + rec.value + '<br>') ;} } 
          else { htmlObj.append('<input type="radio" name="'+ cat + '" value="' + rec.value + ' " checked>'+ rec.value + '<br>'); }
        }); ''', 'Javascript Object builder')

  def __str__(self):
    return '<div %s></div>%s' % (self.strAttr(pyClassNames=self.pyStyle), self.helper)

  @classmethod
  def matchMarkDownBlock(cls, data): return re.match(">>>%s" % cls.callFnc, data[0])

  @staticmethod
  def matchEndBlock(data): return data.endswith("<<<")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj=None):
    recordSet = []
    for val in data[1:-1]:
      line = val.strip()
      if line.startswith("- [x] "):
        recordSet.append({'value': line[5:], "isChecked": 1 })
      else:
        recordSet.append({'value': line[5:], 'disabled': 1})
    if aresObj is not None:
      getattr(aresObj, 'checklist')(recordSet)
    return ["aresObj.checklist(%s)" % json.dumps(recordSet)]

  @classmethod
  def jsMarkDown(cls, vals):
    result = []
    for rec in vals:
      if rec.get('isChecked') == 1:
        result.append("- [X] %s" % rec['value'])
      else:
        result.append("- [ ] %s" % rec['value'])
    return [">>>%s" % cls.callFnc, result, "<<<"]


class ListTree(AresHtml.Html):
  """

  """
  name, category, callFnc, docCategory = 'List Expandable', 'List', 'listexpandable', 'Advanced'
  mocks = [
    {'label': 'AAA', 'items': [
      {'label': 'A1'},
      {'label': 'A2', 'items':
          [
            {'label': 'A21'},
            {'label': 'A22'},
          ]
        },
      {'label': 'A3'},
      ],
     'label': 'BBB'
    }
  ]

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit, title, dataSrc, htmlCode, draggable):
    self.dataSrc, self.title = None, title
    self._jsActions, self._definedActions = {}, ['add', 'save', 'refresh', 'delete']
    if recordSet is None:
      if dataSrc is None:
        recordSet = []
      else:
        self.aresObj, self.dataSrc = aresObj, dataSrc
        if dataSrc.get('on_init', False):
          recordSet = self.onInit(None, dataSrc)
    super(ListTree, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, htmlCode=htmlCode)
    self.css( {"padding-left": "5px"} )
    # The flag start in _jsStyles is only used in the javascript recursion
    self._jsStyles = {'style': {"text-decoration": "none", "padding": 0, "margin": 0, "list-style-position": 'inside'}, 'start': True,
                      'icons': {'close': 'fas fa-folder', 'open': 'fas fa-folder-open'}, 'reset': True, 'draggable': draggable}
    self.jsFrg('click', ''' event.stopPropagation(); $('#%(htmlId)s li span[name=value],a').removeClass( 'text-primary' );
        $(event.currentTarget).addClass( 'text-primary' ); if ('%(htmlCode)s' != 'None') { 
        %(breadCrumVar)s['params']['%(htmlCode)s'] = $(event.currentTarget).parent('li').parent('ul').siblings('span[name=value]').text() +'/'+ $(event.currentTarget).text() } ;
      ''' % { 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'htmlCode': self.htmlCode, 'htmlId': self.htmlId} )
    if dataSrc is not None and dataSrc['type'] in ["script", 'url']:
      # TODO To extend to internal flask calls
      self.jsAction(action='refresh', icon='fas fa-sync-alt', pyCssCls="CssSmallIcon", tooltip="Refresh the tree", url=self.dataSrc.get('script', self.dataSrc.get('url', '')),
                    jsData=self.dataSrc.get('htmlObjs'), jsFncs=['var styles_%(htmlId)s = %(jsStyles)s; styles_%(htmlId)s.forceSelect = $("#%(htmlId)s").find(".text-primary").first().text()' % {"jsStyles": json.dumps(self._jsStyles), "htmlId": self.htmlId},
                                                                 self.jsGenerate(jsStyles="styles_%s" % self.htmlId)], httpCodes=self.dataSrc.get('httpCodes'))

  @property
  def jsQueryData(self):
    """
    :category: Javascript features
    :dsc: Python function to define the Javascript object to be passed in case of Ajax call internally or via external REST service with other languages
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    return "{ event_parent: $(event.currentTarget).parent('li').parent('ul').siblings('span[name=value]').text(), event_val: $(event.currentTarget).text(), event_code: '%s' }" % self.htmlId

  @property
  def val(self):
    return '$("#%s").find(".text-primary").first().text()' % self.htmlId

  @property
  def eventId(self): return "$('#%s li span[name=value],a')" % self.htmlId

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' 
      if (jsStyles.start == true && !Array.isArray(data)) {
        tmpData = [] ; jsStyles.start = false;
        for (var key in data) {
          var row = {'label': key, 'items': [] } ; 
          data[key].forEach( function (val) { row['items'].push( {'label': val } ) ; }) ;
          tmpData.push(row) ;}
        data = tmpData; } ;
      if (jsStyles.reset) { htmlObj.empty() ; } ; var ul = $("<ul style='margin:0 0 0 10px;padding:0'></u>") ; var resetFlag = jsStyles.reset;
      if (jsStyles.draggable) {ul.addClass( "list_draggable" ) } ;
      data.forEach( function(rec){ 
        var content = rec.label ; 
        if (rec.color != undefined) { jsStyles.style.color = rec.color ;} else { jsStyles.style.color = "%(blackColor)s" ;}
        if (rec.icon != '' && rec.icon != undefined) { content = '<i style="margin-left:5px;margin-right:5px" class="' + rec.icon + '"></i>' + rec.label ;}
        var li = $('<li name="expandable"></li>').css(jsStyles.style) ; 
        if (rec.url != undefined) { li.append('<a style="display:inline-block;text-decoration:none" href="'+ rec.url +'" target="_blank">' + content + '</a>') ;  }
        else { li.append( '<span name="value">'+ content +'</span>' ) ; }
        jsStyles.reset = false;
        if (rec.items != undefined) { 
          li.css( { 'list-style-type':'none', 'list-style-image':'none', 'cursor': 'pointer' }) ;
          var span = $( '<span data-close="'+ jsStyles.icons.close + '" data-open="'+ jsStyles.icons.open + '" class="'+ jsStyles.icons.open +'" style="margin-right:5px"></span>' ) ;
          span.attr('name', 'section') ;
          li.prepend( span ) ;
          ul.append( li ) ; htmlObj.append( ul ) ;
          %(jsFnc)s(li, rec.items, jsStyles) ; }
        else {
          if (jsStyles.forceSelect != undefined) {
            if (jsStyles.forceSelect == rec.label) {
              li.find('span').addClass( 'text-primary' ) ;
              jsStyles.forceSelect = undefined;
            } 
          } ;
          li.css( { 'list-style-type':'none', 'list-style-image':'none' }) ;
          ul.append( li ) ; htmlObj.append( ul ) ;}
      }) ; 
      if (jsStyles.draggable) {
        ul.sortable( {placeholder: "ui-state-highlight", dropOnEmpty: true, 
                      start: function(event, ui) { },
                      stop: function(event, ui) { },
           connectWith: '.list_draggable' } ).disableSelection()  ;  
      }
      ''' % {'jsFnc': self.__class__.__name__, 'blackColor': self.getColor("greyColor", 8)}, 'Javascript Object builder' )

  def jsEvents(self):
    if hasattr(self, 'jsFncFrag'):
      for eventKey, fnc in self.jsFncFrag.items():
        if self.htmlCode is not None:
          fnc.insert(0, self.jsAddUrlParam(self.htmlCode, self.val, isPyData=False))
        self.aresObj.jsOnLoadEvtsFnc.add('''
          $('body').on('%(eventKey)s', '#%(htmlId)s li span[name=value], #%(htmlId)s li a', function(event) {
            var useAsync = false; var data = %(data)s ;
            if (!$('#body_loading').length){ 
              var bodyLoading2 = $('<div id="body_loading" name="ares_loading" style="bottom:20px;left:70px;position:fixed;background-color:#F4F4F4;padding:5px"><i class="fas fa-spinner fa-spin" style="margin-left:10px;margin-right:10px"></i><div style="display:inline" id="loading_count">0</div> process running...</div>') ; 
            } ;
            $('body').append(bodyLoading2) ;
            $('#loading_count').html( parseInt($('#loading_count').html()) + 1) ;
            %(jsFnc)s ; 
            if (!useAsync) {
              $('#loading_count').html( parseInt($('#loading_count').html()) - 1) ;
              if ($('#loading_count').html() == '0') { $('#body_loading').remove() ;} }
          }) ;''' % {'htmlId': self.htmlId, 'eventKey': eventKey, 'data': self.jsQueryData, 'jsFnc': ";".join([f for f in fnc if f is not None])})

  def __str__(self):
    self.aresObj.jsOnLoadFnc.add('''
      $(document).on('click', 'span[name=section]' , function(event) {
        $(this).parent().children().not(":nth-child(0)").not(":nth-child(1)").not(":nth-child(2)").toggle('fast'); 
        if ( $(this).attr('class') == $(this).data('open') ){ $(this).attr('class',  $(this).data('close')) } 
        else { $(this).attr('class',  $(this).data('open')) } }) ''')
    events = []
    for action in self._definedActions:
      if action in self._jsActions:
        events.append(self._jsActions[action])
    return '''
      <div style="width:100%%;margin:5px 0 0 5px">
        <span style='font-weight:bold;font-size:14px'>%(title)s</span>
        %(events)s
      </div>
      <div %(strAttr)s></div>%(helper)s''' % {'title': self.title, 'strAttr': self.strAttr(), 'helper': self.helper, 'events': "".join(events)}

  def setSelected(self, value):
    self._jsStyles["forceSelect"] = value
    if self.htmlCode is not None:
      self.aresObj.jsOnLoadEvtsFnc.add(self.jsAddUrlParam(self.htmlCode, value, isPyData=True))
    return self

  # --------------------------------------------------------------------------------------------------------------
  #                                   EDITOR STANDARD EVENTS
  #
  def dblclick(self, jsFncs="", childOnly=True):
    if not isinstance( jsFncs, list):
      jsFncs = [jsFncs]
    self.jsFrg('dblclick', ''' 
      if ( $(event.currentTarget).prev().attr('name') != 'section') {
        var text = $(event.currentTarget).text(); $(event.currentTarget).text(''); input = $("<input type='text'>");
        input.val(text); input.appendTo($(event.currentTarget)).focus();
        input.focusout(function() {
          if ( $(this).val() == '') { $(event.currentTarget).text( text ); data.event_val = $(this).val(); } 
          else { $(event.currentTarget).text( $(this).val() ) ; data.event_val = $(this).val(); }; 
          $(this).remove(); %(jsFncs)s ; 
          if(%(htmlCode)s != null) { %(breadCrumbVar)s['params'][%(htmlCode)s] = data.event_val ; }
        }) ; 
        input.keypress(function(e) {
            if(e.which == 13) { $(this).trigger("focusout");}
            if(e.keyCode == 27) { $(this).val('') ;$(this).trigger("focusout"); }
        });
      }
      ''' % {"jsFncs": ';'.join(jsFncs), 'breadCrumbVar': self.aresObj.jsGlobal.breadCrumVar, 'htmlCode': json.dumps(self.htmlCode)} )

  def jsAction(self, action, icon, pyCssCls, tooltip, url=None, jsData=None, jsFncs=None, httpCodes=None):
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs] if jsFncs is not None else []

    # Add this to an ajax POST call if an URL is defined
    self.css( {"cursor": "pointer"})
    fnc = self.aresObj.jsPost(url=url, jsData=jsData, jsFnc=jsFncs, httpCodes=httpCodes) if url is not None else ";".join(jsFncs)
    self._jsActions[action] = "<span id='%(htmlId)s_%(action)s' title='%(tooltip)s' class='%(cssStyle)s %(icon)s'></span>" % {
      "icon": icon, "cssStyle": self.addPyCss(pyCssCls), "htmlId": self.htmlId, 'tooltip': tooltip, 'action': action}
    self.aresObj.jsOnLoadFnc.add("$('#%(htmlId)s_%(action)s').on('click', function(event) { %(jsFncs)s; })" % {"htmlId": self.htmlId, "jsFncs": fnc, 'action': action})
    if action not in self._definedActions:
      self._definedActions.append(action)
    return self

  def removeNode(self, jsFncs=None, url=None, jsData=None, httpCodes=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>>
    :dsc:
      Set the function to add a new node to a tree object. This function needs to be defined in order to set the
      corresponding javascript function used in the browser
    :return: The python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs] if jsFncs is not None else []
    jsFncs.append(''' 
      var selectedItem = $('#%(htmlId)s').find(".text-primary").first(); var selectedVal = selectedItem.text() ;
      var selectedParentVal = selectedItem.parent('li').parent('ul').siblings('span[name=value]').text();
      if (selectedVal != '') {
        var data = { event_parent: selectedParentVal, event_val: selectedVal, htmlId: '%(htmlId)s' }; selectedItem.remove() ;
      } ''' % { 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'htmlId': self.htmlId })
    return self.jsAction(action='delete', icon='far fa-trash-alt', pyCssCls="CssSmallIconRed", tooltip="Remove selected node", url=url,
                         jsData=jsData, jsFncs=jsFncs, httpCodes=httpCodes)

  def addNode(self, jsFncs="", url=None, jsData="NewScript.py", httpCodes=None, nodeId=0, icon="far fa-file-alt"):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>>
    :dsc:
      Set the function to add a new node to a tree object. This function needs to be defined in order to set the
      corresponding javascript function used in the browser
    :return: The python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs] if jsFncs is not None else []
    jsIcon = '' if icon is None else '<i style="margin-left:5px;margin-right:5px" class="far fa-file-alt"></i>'
    jsFncs.append('''var li = $('<li name="expandable"></li>').css(%(jsStyles)s.style);
      li.css( { 'list-style-type':'none', 'list-style-image':'none', 'cursor': 'pointer' });
      li.append( '%(jsIcon)s<span name="value">%(jsData)s</span>' );
      if($('#%(htmlId)s ul').get(0) == undefined){ var ul = $("<ul style='margin:0 0 0 10px;padding:0'></u>"); $('#%(htmlId)s').append(ul) ;};
      $($('#%(htmlId)s ul').get(%(nodeId)s)).append(li);
      ''' % {'jsStyles': json.dumps(self._jsStyles), 'jsData': jsData, 'htmlId': self.htmlId, 'jsFncs': ';'.join(jsFncs), 'nodeId': nodeId, "jsIcon": jsIcon})
    return self.jsAction(action='add', icon='fas fa-plus', pyCssCls="CssSmallIcon", tooltip="Add new node to a Tree object", url=url, jsData=jsData, jsFncs=jsFncs, httpCodes=httpCodes)

  def save(self, jsFncs="", url=None, jsData="NewScript.py", httpCodes=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>>
    :dsc:

    :return: The python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs] if jsFncs is not None else []

    return self.jsAction(action='save', icon='far fa-hdd', pyCssCls="CssSmallIcon",
                         tooltip="Save an empty file on the drive", url=url, jsData=jsData, jsFncs=jsFncs,
                         httpCodes=httpCodes)

  def to_word(self, document):
    pass


class ListTournaments(AresHtml.Html):
  name, category, callFnc, docCategory = 'Brackets', 'Container', 'brackets', 'Advanced'
  __reqCss, __reqJs = ['jquery-brackets'], ['jquery-brackets']

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit, options):
    self.options = {} if options is None else options
    super(ListTournaments, self).__init__(aresObj, {'vals': recordSet, 'save': 'null', 'edit': 'null', 'render': 'null',
                                                    'options': self.options}, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.css( {'overflow': 'auto', "padding": "auto", "margin": "auto"})

  def addFnc(self, fncName, jsFncs):
    if isinstance( jsFncs, list):
      jsFncs = ";".join(jsFncs)
    self.vals[fncName] = jsFncs

  def onDocumentLoadFnc(self):
    # , disableToolbar: true, disableTeamEdit: false
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
      parameters = { centerConnectors: true, init: data.vals }; 
      if (data.save != "null") { parameters['save'] = new Function('rec', 'userData', 'var data = {challenge: JSON.stringify(rec), userProno: JSON.stringify(userData) } ;' + data.save) };
      if (data.render != "null") { parameters['decorator'] = {render: new Function('rec', 'userData', data.save), edit: function(container, data, doneCb) { } } };
      if (data.edit != "null") { 
        if ( data.render == "null" ) { parameters['decorator']['render'] = function(rec, userData) {} } ;
        parameters['decorator']['edit'] = new Function('container', 'data', 'doneCb', data.edit); };
      for (var k in data.options) { parameters[k] = data.options[k] ;};
      htmlObj.bracket( parameters ) ;
      ''', 'Javascript Object builder')

  def __str__(self):
    return "<div %s></div>" % self.strAttr(pyClassNames=self.pyStyle)


