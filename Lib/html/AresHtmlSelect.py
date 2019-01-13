#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
from ares.Lib.html import AresHtml
from ares.Lib import AresImports

# External package required
ares_pandas = AresImports.requires(name="pandas", reason='Missing Package', install='pandas', autoImport=True, sourceScript=__file__)



class SelectDropDown(AresHtml.Html):
  """ Python interface to the Select Drop Down

  """
  alias, cssCls = 'dropdown', ['btn', 'dropdown-toggle']
  references = {'Bootstrap Definition': 'http://getbootstrap.com/docs/4.0/components/dropdowns/',
                'W3C Definition': 'https://www.w3schools.com/bootstrap/tryit.asp?filename=trybs_ref_js_dropdown_multilevel_css&stacked=h',
                'Example': 'https://codepen.io/svnt/pen/beEgre'}
  __reqCss, __reqJs = ['bootstrap', 'jqueryui'], ['bootstrap', 'jquery']
  __pyStyle = ['CssDivNoBorder']
  name, category, callFnc, docCategory = 'DropDown Select', 'Select', 'dropdown', 'Advanced'

  def __init__(self, aresObj, title, recordSet, width, widthUnit, height, heightUnit, htmlCode, scriptSrc, globalFilter):
    if recordSet is None:
      title = 'Languages'
    super(SelectDropDown, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, htmlCode=htmlCode, globalFilter=globalFilter)
    if scriptSrc is not None and scriptSrc.get('on_init', False):
      self.vals = self.onInit(htmlCode, scriptSrc)
    if htmlCode is not None and htmlCode in self.aresObj.http:
      self.initVal(self.aresObj.http[htmlCode])
    self.title, self.scriptSrc = title, scriptSrc
    # To replace non alphanumeric characters https://stackoverflow.com/questions/20864893/javascript-replace-all-non-alpha-numeric-characters-new-lines-and-multiple-whi
    #self.jsFrg = ["%s = CleanText($(this).text()) ;" % self.htmlId]
    self.allowTableFilter, self._jsStyles = [], {"clearDropDown": True, 'dropdown_submenu': {},
      'a_dropdown_item': {"width": "100%", 'font-size': '12px', 'text-decoration': 'none', 'padding-left': "10px"},
      "li_dropdown_item": {"text-align": "left", 'font-size': '12px'} }
    self.css( {"margin-top": "5px", "display": "inline-block"} )
    for evts in ['click', 'change']:
      # Add the source to the different events
      self.jsFrg(evts, '''
        event.stopPropagation(); $("#%(htmlId)s_button").html(data.event_val);
        if ( '%(htmlCode)s' != 'None') { %(breadCrumVar)s['params']['%(htmlCode)s'] = %(jsEventVal)s } ;
        ''' % {'htmlId': self.htmlId, 'htmlCode': self.htmlCode, 'jsEventVal': self.jsEventVal, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar})

  @property
  def jsQueryData(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsQueryData
    :dsc: Python function to define the Javascript object to be passed in case of Ajax call internally or via external REST service with other languages
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    return "{event_val: %s, event_code: '%s'}" % (self.jsEventVal, self.htmlId)

  @property
  def jsEventVal(self): return "$(this).contents()[0].text"

  def initVal(self, val, isPyData=True):
    """
    :category: Javascript On-Load function
    :rubric: JS
    :example: >>> myObj.initVal('Test')
    :dsc:
      This function will set the initial value selected by the SelectDropDown component.
    """
    if isPyData:
      val = json.dumps(val)
    self.aresObj.jsOnLoadFnc.add('$("#%(htmlId)s_button").html(%(jsVal)s)' % {"htmlId": self.htmlId, "jsVal": val})

  def setDefault(self, value, isPyData=True):
    """
    :category: Javascript Global variable
    :rubric: JS
    :example: >>> myObj.setDefault( 'btn-default' )
    :dsc:
      Set the default value selected to the dropdown box
    """
    if isPyData:
      value = json.dumps(value)
    self.aresObj.jsGlobal.add("%s = %s;" % (self.htmlId, value))

  @property
  def val(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.val
    :returns: Javascript string with the function to get the current value of the component
    :dsc:
      Property to get the jquery value of the HTML object in a python HTML object.
      This method can be used in any jsFunction to get the value of a component in the browser.
      This method will only be used on the javascript side, so please do not consider it in your algorithm in Python
    """
    return '$("#%s_button").html()' % self.htmlId

  @property
  def eventId(self): return "$('#%s li')" % self.htmlId

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' 
        if (jsStyles.clearDropDown) { htmlObj.empty() ; } ;
        data.forEach(function(rec){
          if (rec.subItems != undefined) {
            var li = $('<li class="dropdown-submenu"></li>' ).css( jsStyles.dropdown_submenu );
            var a = $('<a class="dropdown-item" tabindex="-1" href="#" style="display:inline-block"><span style="display:inline-block;float:left">' + rec.value + '</span></a>').css( jsStyles.a_dropdown_item )
                .append('<i class="fas fa-caret-right" style="display:inline-block;float:right"></i>');
            li.append( a ); var ul = $('<ul class="dropdown-menu"></ul>'); li.append( ul ); jsStyles.clearDropDown = false;
            htmlObj.append( li ); %(pyCls)s(ul, rec.subItems, jsStyles) ;
          } else {
            if (rec.disable == true) {htmlObj.append('<li class="dropdown-item disabled"><a tabindex="-1" href="#">' + rec.value + '</a></li>');}
            else {
              if (rec.url == undefined) { var a = $('<a class="dropdown-item" tabindex="-1" href="#">' + rec.value + '</a>').css( jsStyles.a_dropdown_item ); }
              else { var a = $('<a class="dropdown-item" tabindex="-1" href="' + rec.url + '">' + rec.value + '</a>').css( jsStyles.a_dropdown_item ); }
              a.css( jsStyles.a_dropdown_item );
              var li = $('<li class="dropdown-submenu"></li>' ).css( jsStyles.dropdown_submenu );
              li.append( a ); htmlObj.append( li )
            }
          }
        }) ; ''' % {"pyCls": self.__class__.__name__} )

  def __str__(self):
    """  String representation of a Drop Down item """
    return ''' 
      <div class="dropdown" %(cssAttr)s>
        <button id="%(htmlId)s_button" class="%(class)s" style="font-weight:bold;width:100%%;font-size:12px;background-color:%(darkBlue)s;color:%(color)s" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">%(title)s<span class="caret"></span></button>
        <ul class="dropdown-menu" id="%(htmlId)s" aria-labelledby="dropdownMenu"></ul>
      </div> ''' % {'cssAttr': self.strAttr(withId=False), 'class': self.getClass(), 'title': self.title, 'htmlId': self.htmlId,
                    'darkBlue': self.getColor('blueColor', 2), 'color': self.getColor('greyColor', 0)}

  def to_word(self, document):
    p = document.add_paragraph()
    p.add_run("Selected: ")
    runner = p.add_run( self.aresObj.http.get(self.htmlCode, self.vals) )
    runner.bold = True

  def to_xls(self, workbook, worksheet, cursor):
    if self.htmlId in self.aresObj.http:
      cellTitle = self.title if self.title != "" else 'Input'
      cell_format = workbook.add_format({'bold': True})
      worksheet.write(cursor['row'], 0, cellTitle, cell_format)
      cursor['row'] += 1
      worksheet.write(cursor['row'], 0, self.aresObj.http[self.htmlId] )
      cursor['row'] += 2


class Select(AresHtml.Html):
  """
  :category: Ares Component
  :rubric: HTML
  :type:
  :dsc:

  """
  # TODO: Extend the python object to handle multi select and all the cool features
  cssCls = ["selectpicker show-tick"]
  references = {'Example': 'https://silviomoreto.github.io/bootstrap-select/examples/',
                'Bootstrap Definition': 'https://www.npmjs.com/package/bootstrap-select-v4',
                'Jquery Events': 'https://www.jqueryscript.net/form/Bootstrap-4-Dropdown-Select-Plugin-jQuery.html'}
  __reqCss, __reqJs = ['select'], ['select']
  __pyStyle = ['CssSelect']
  name, category, callFnc, docCategory = 'Simple Select', 'Select', 'select', 'Advanced'

  def __init__(self, aresObj, recordSet, title, htmlCode, dataSrc, event, selected, docBlock, allSelected, label, width,
               widthUnit, height, heightUnit, dfColumn, globalFilter):
    """ Instantiate the object and store the selected item """
    selectedVal, self.container, self.label = None, None, label
    if recordSet is not None:
      if issubclass(type(recordSet), ares_pandas.DataFrame) and dfColumn is not None:
        if globalFilter is not None:
          if globalFilter is True:
            if htmlCode is None:
              raise Exception("Please set a htmlCode to the %s to use this as a filter" % self.callFnc)

            dataId, dataCode = id(recordSet), None
            for key, src in aresObj.jsSources.items():
              if src.get('dataId') == dataId:
                dataCode = key
                break

            if not hasattr(recordSet, 'htmlCode') and dataCode is None:
              dataCode = "ares_id_%s" % len(aresObj.jsSources)
              recordSet = aresObj.df(recordSet, htmlCode=dataCode)
            dataCode = recordSet.htmlCode
            globalFilter = {'jsId': dataCode, 'colName': dfColumn}
            if not dataCode in aresObj.jsSources:
              aresObj.jsSources[dataCode] = {'dataId': dataId, 'containers': [], 'data': recordSet}
            aresObj.jsSources[dataCode]['containers'].append(self)
        recordSet = recordSet[dfColumn].unique().tolist()
      elif isinstance(recordSet, set):
        recordSet = list(recordSet)
      elif isinstance(recordSet, dict):
        recordSet = [{'value': v, 'name': k} for k, v in recordSet.items()]
      if recordSet and not isinstance(recordSet[0], dict):
        if docBlock is not None:
          if not isinstance(docBlock, dict):
            docBlock = {"id": docBlock}
          docBlock['params'] = recordSet
          if selected is not None:
            docBlock['params'] = "%s, selected='%s'" % (docBlock['params'], selected)
        recordSet = [{'value': val, 'selected': True} if val == selected else {'value': val} for val in recordSet]
      elif selected is not None:
        for rec in recordSet:
          if rec['value'] == selected:
            rec['selected'] = True

    if htmlCode in aresObj.http:
      if recordSet is None:
        recordSet = [{'name': aresObj.http[htmlCode], 'value': aresObj.http[htmlCode]}]
      for rec in recordSet:
        if rec['value'] == aresObj.http[htmlCode]:
          rec['selected'] = True
          selectedVal = rec['value']
          title = aresObj.http[htmlCode]
        else:
          rec['selected'] = False

    if allSelected:
      recordSet = [{'name': 'All', 'value': ''}] + recordSet
    super(Select, self).__init__(aresObj, recordSet, htmlCode=htmlCode, docBlock=docBlock, width=width, widthUnit=widthUnit,
                                 height=height, heightUnit=heightUnit, globalFilter=globalFilter)
    if dataSrc is not None and dataSrc.get('on_init', False):
      self.vals = self.onInit(htmlCode, dataSrc)
      for rec in self.vals:
        if rec['value'] == aresObj.http.get(htmlCode):
          rec['selected'] = True
          selectedVal = rec['value']
          title = aresObj.http[htmlCode]
        else:
          rec['selected'] = False
    self.title, self.htmlCode, self.dataSrc, self.selectStyle = title, htmlCode, dataSrc, []
    self.aresObj.jsOnLoadFnc.add('%s.selectpicker( {liveSearch: true, style: "show-menu-arrow"} );' % self.jqId)
    if htmlCode is not None:
      if selectedVal is not None:
        self.aresObj.jsOnLoadFnc.add("%s.val('%s')" % (self.jqId, selectedVal))
    self.css({'padding': 0, 'clear': 'both', 'margin': '5px 0'})
    if event is not None:
      self.change(aresObj.jsPost(event['script'], event.get('htmlCodes'), event.get('success', '')))

  def initVal(self, val):
    """
    :category: Python function
    :rubric: PY
    :example: >>> myObj.initVal( 'test' )
    :dsc:
      Set the initial value of the select HTML component
    """
    for rec in self.vals:
      rec['selected'] = True if rec['value'] == val else False

  @property
  def jsQueryData(self):
    return "{event_val: %s.val(), event_code: '%s', event_icon: %s.find(':selected').data('icon')}" % (self.jqId, self.htmlId, self.jqId)

  @property
  def jqId(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jqId
    :dsc: Python property to get a unique Jquery ID function for a given AReS Object
    :return: Javascript String of the variable used to defined the Jquery object in Javascript
    """
    return "$('#%s select')" % self.htmlId

  def setSelectCss(self, cssClss):
    """
    :category: Table Definition
    :rubric: CSS
    :type: Style
    :dsc:

    :return: The Python Datatable object
    """
    for cssCls in cssClss:
      self.addPyCss(cssCls)
      self.selectStyle.append(self.aresObj.cssObj.get(cssCls)().classname)
    return self

  def jsLoad(self, jsData, isPyData=False):
    if isPyData:
      jsData = json.dumps(jsData)
    return "%(builder)s($('#%(htmlId)s_select'), %(jsData)s); " % { 'builder': self.__class__.__name__, 'htmlId': self.htmlId, 'jsData': jsData}

  def jsLoadFromSrc(self, outKey): return '''
    var params = %(script)s; var attr = {} ; 
    if (params.htmlCodes != undefined) {params.htmlCodes.forEach( function(code) {attr[code] = %(breadCrumbVar)s['params'][code] ; }); } ;
    $.ajax({ url: "/reports/data/%(report_name)s/" + params.script,  method: "POST", data: JSON.stringify(attr, null, '\t'), contentType: 'application/json;charset=UTF-8', cache: false
           }).done( function(data) { var results = JSON.parse(data); %(jsLoad)s;
             if (results.aresPopup != undefined) {
              $('#popup').html(results.aresPopup);
              $('#popup').css( {'top': '140px', 'right': '20px', 'position': 'fixed', 'padding': '10px 20px 10px 20px', 'border': '1px solid %(grey)s', 'border-radius': '5px' } ) ;
              $('#popup').show() ; $('#popup').fadeOut(3000) ; }
           }).fail( function(data) {  });
    ''' % {'script': self.dataSrc, 'jsLoad': self.jsLoad('results.%s' % outKey), 'breadCrumbVar': self.aresObj.jsGlobal.breadCrumVar,
           'report_name': self.aresObj.report_name, 'grey': self.getColor('greyColor', 3) }

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
      var categories = {} ; var cats = [] ; var selectedVals = [];
      data.forEach(function(rec){
        if (rec.category == undefined) { rec.category = 'None' ; }
        if (rec.category in categories) { categories[rec.category].push(rec) ; } 
        else { categories[rec.category] = [rec] ; cats.push(rec.category) ; }}) ;
      cats.forEach(function(cat){
        if (cat != 'None') {
          var optgroup = $('<optgroup label="'+ cat + '">' + cat + '</optgroup>') ;
          categories[cat].forEach(function(rec){
            if (rec.selected == true) { var selected = 'selected=true'} else { var selected = ''};
            if (rec.name == undefined) { rec.name = rec.value };
            if (rec.icon != undefined) { options =  options + 'data-icon="'+ rec.icon +'"'};
            optgroup.append('<option value="' + rec.value + '" ' + selected + '>' + rec.name + '</option>')}) ;
          htmlObj.append(optgroup)}
        else {
          categories[cat].forEach(function(rec){
            var options = ' ';
            if (rec.selected == true) { var selected = 'selected'; selectedVals.push(rec.value) } else { var selected = ''};
            if (rec.name == undefined) { rec.name = rec.value };
            if (rec.icon != undefined) { options =  options + 'data-icon="'+ rec.icon +'"'};
            if (rec['data-subtext'] != undefined) { options = options + ' data-subtext="' + rec['data-subtext'] + '"' };
            htmlObj.append('<option value="' + rec.value + '" ' + selected + options + '>' + rec.name + '</option>')}) ;
        } }) ; htmlObj.selectpicker('refresh'); htmlObj.val(selectedVals)''')

  def __str__(self):
    """ Return the HTML string for a select """
    containerTag = '' if self.container is None else 'data-container="%s"' % self.container
    # Quick hack to be able to override the style of the title of the select
    # TODO: Should be done correctly: https://developer.snapappointments.com/bootstrap-select/examples/
    if len(self.selectStyle) == 0:
      self.setSelectCss(['CssSelectStyle'])
    selectStyle = "" if len(self.selectStyle) == 0 else 'data-style="%s"' % " ".join(self.selectStyle)
    return '<div %s>%s <select %s %s title="%s"></select></div>' % (self.strAttr(pyClassNames=['CssSelect']),  self.label, selectStyle, containerTag, self.title)

  def to_xls(self, workbook, worksheet, cursor):
    if self.htmlId in self.aresObj.http:
      cellTitle = self.title if self.title != "" else 'Input'
      cell_format = workbook.add_format({'bold': True})
      worksheet.write(cursor['row'], 0, cellTitle, cell_format)
      cursor['row'] += 1
      worksheet.write(cursor['row'], 0, self.aresObj.http[self.htmlId])
      cursor['row'] += 2

  def to_word(self, document):
    p = document.add_paragraph()
    p.add_run("Selected: ")
    runner = p.add_run( self.aresObj.http.get(self.htmlCode, self.vals) )
    runner.bold = True


class SelectMulti(Select):
  """ Python interface to the multi select element

  """
  __reqCss, __reqJs = ['select'], ['select']
  references = {'Example': 'https://silviomoreto.github.io/bootstrap-select/examples/'}
  name, category, callFnc, docCategory = 'Multi Select', 'Select', 'selectmulti', 'Advanced'

  def __init__(self, aresObj, vals, title, maxSelections, htmlCode, dataSrc, event, selectedItems, docBlock, label,
               width, widthUnit, height, heightUnit, dfColumn, globalFilter):
    """ Instantiate the Drop Down button """
    if vals is not None:
      selectedItems = [] if selectedItems is None else selectedItems
      if issubclass(type(vals), ares_pandas.DataFrame):
        if globalFilter:
          globalFilter = {'jsId': vals.htmlCode, 'colName': dfColumn}
        vals = vals[dfColumn].unique().tolist()
      elif isinstance(vals, list) and isinstance(vals[0], str):
        vals = [{'value': val, 'selected': True} if val in selectedItems else {'value': val} for val in vals]
      elif selectedItems:
        for rec in vals:
          if rec['value'] in selectedItems:
            rec['selected'] = True

    super(SelectMulti, self).__init__(aresObj, vals, title, htmlCode, dataSrc, event, None, docBlock, False, label, width,
                                      widthUnit, height, heightUnit, dfColumn, globalFilter)
    if dataSrc is not None and dataSrc.get('on_init', False):
      recordSet = self.onInit(htmlCode, dataSrc)
      self.vals = recordSet
    if htmlCode in self.aresObj.http:
      for val in self.aresObj.http[htmlCode].split(","):
        for rec in self.vals:
          if val == rec['value']:
            rec['selected'] = True
    self.title, self.maxSelections = title, maxSelections
    if htmlCode is not None:
      self.aresObj.htmlCodes[self.htmlCode] = self
      # self.change('') # Add the onchange method to update the breadcrumb

  def initVal(self, val):
    for rec in self.vals:
      rec['selected'] = True if rec['value'] in val.split(",") else False

  def selected(self, vals):
    """ Set default selected values """
    self.aresObj.jsOnLoadFnc.add("%s.val(%s); %s.selectpicker('refresh');" % (self.jqId, json.dumps(vals), self.jqId))

  def __str__(self):
    """ Return the HTML string for a select """
    containerTag = '' if self.container is None else 'data-container="%s"' % self.container
    # Quick hack to be able to override the style of the title of the select
    # TODO: Should be done correctly: https://developer.snapappointments.com/bootstrap-select/examples/
    selectStyle = "" if len(self.selectStyle) == 0 else 'data-style="%s"' % " ".join(self.selectStyle)
    return '''
      <div %s>%s
        <select %s multiple data-max-options="%s" %s data-actions-box="true" data-width="auto" title="%s"></select>
      </div>''' % (self.strAttr(pyClassNames=['CssSelect']), self.label, selectStyle, self.maxSelections, containerTag, self.title)

