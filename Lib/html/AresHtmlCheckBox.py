#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
    'eng':
'''
:dsc:

'''}


import json
from ares.Lib.html import AresHtml
from ares.Lib import AresImports

# External package required
ares_pandas = AresImports.requires(name="pandas", reason='Missing Package', install='pandas', autoImport=True, sourceScript=__file__)


class HtmlCheckbox(AresHtml.Html):
  """
  :function val:
  :example: aresObj.checkbox([ { "value": "Windows", "checked": True }, { "value": "Apple" } ]).display([ { "value": "Pomme" }, { "value": "Poire", "checked": True } ])
  :dsc:
    Python wrapper to the HTML checkbox elements
  """
  references = {'Checkbox W3C': 'https://www.w3schools.com/howto/howto_css_custom_checkbox.asp'}
  __pyStyle = ['CssLabelContainer', 'CssDivNoBorder', 'CssCheckMark', 'CssLabelCheckMarkHover']
  name, category, callFnc, docCategory = 'Check Box', 'Button', 'checkbox', 'Advanced'
  cssTitle = "CssTitle4"

  def __init__(self, aresObj, recordSet, title, color, width, widthUnit, height, heightUnit, align, htmlCode,
               globalFilter, tooltip, dfColumn):
    if issubclass(type(recordSet), ares_pandas.DataFrame):
      if globalFilter:
        globalFilter = {'jsId': recordSet.htmlCode, 'colName': dfColumn}
      recordSet = recordSet[dfColumn].unique().tolist()
    if isinstance(recordSet, list):
      # Transform the recordSet to have exactly the expected structure
      if recordSet is not None and isinstance(recordSet[0], str):
        recordSet = [{"value": rec} for rec in recordSet]
    super(HtmlCheckbox, self).__init__(aresObj, recordSet, htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, globalFilter=globalFilter)
    self.css( {'text-align': align, 'color': self.getColor("greyColor", 8) if color is None else color} )
    self._jsStyles = {"tooltip": tooltip}
    self.jsFrg('click', '''
      if (data.event_val) {
        if ( %(breadCrumVar)s['params']["%(htmlId)s"] === undefined ) {%(breadCrumVar)s['params']['%(htmlId)s'] = [data.event_label] }
        else {%(breadCrumVar)s['params']['%(htmlId)s'].push(data.event_label)}}
      else { var index = %(breadCrumVar)s['params']['%(htmlId)s'].indexOf(data.event_label); %(breadCrumVar)s['params']['%(htmlId)s'].splice(index, 1) }
      ''' % {"breadCrumVar": self.aresObj.jsGlobal.breadCrumVar, "htmlId": self.htmlId} )
    self.title = title

  def initVal(self, val):
    for rec in self.vals:
      rec['checked'] = True if rec['value'] == val else False

  def tooltip(self, value, location='top'):
    self._jsStyles['tooltip'] = value
    return self

  @property
  def val(self):
    """
    :category: Javascript features
    :example: myObj.val
    :dsc:
      Property to get the jquery value of the HTML object in a python HTML object.
      This method can be used in any jsFunction to get the value of a component in the browser.
      This method will only be used on the javascript side, so please do not consider it in your algorithm in Python
    """
    return "%(breadCrumVar)s['params']['%(htmlCode)s']" % {"htmlCode": self.htmlCode, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar }

  @property
  def jsQueryData(self):
    """
    :category: Javascript features
    :dsc:
      Python function to define the Javascript object to be passed in case of Ajax call internally or via external REST service with other languages
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    return "{ event_label: $(this).text(), event_type: $(this).find('span').data('content'), event_val: isChecked, event_code: '%s' }" % (self.htmlId)

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' htmlObj.empty() ;
      data.forEach(function(rec){
        if (rec.color == undefined) { rec.color = 'black'; }
        var style = {'color': rec.color, 'display': 'block', 'font-size': '14px',  'position': 'relative', 'cursor': 'pointer'};
        if (rec.style != undefined) { for (key in rec.style) { style[key] = rec.style[key] }} ;
        if (rec.dsc == undefined) { rec.dsc = ''}
        if (rec.name == undefined) { rec.name = rec.value}
        var strCss = []; for (key in style) { strCss.push( key + ":" + style[key])};
        if (rec.checked == true) { var spanContent = '<span data-content="' + rec.value + '" style="display:inline-block;height:25px;width:25px;float:left;margin:0 5px 0 0"><i class="fas fa-check"></i></span><p style="margin:0" title="'+ rec.dsc + '">' + rec.name + '</p>'; }
        else { var spanContent = '<span data-content="'+ rec.value + '" style="display:inline-block;height:25px;width:25px;float:left;margin:0 5px 0 0"></span><p style="margin:0" title="'+ rec.dsc + '">' + rec.name + '</p>';}     
        htmlObj.append( $('<label style="' + strCss.join(";") + '">' + spanContent + '</label>') )}); htmlObj.find("p").tooltip(); 
        if (jsStyles.tooltip != ""){ 
          var tip = $('<i class="fas fa-info-circle" style="right:0" title="'+ jsStyles.tooltip +'"></i>') ;
          tip.tooltip() ; htmlObj.append($("<div style='width:100%;text-align:right'></div>").append(tip) )}
      ''', 'Javascript Object builder' )

  def jsEvents(self):
    if hasattr(self, 'jsFncFrag'):
      for eventKey, fnc in self.jsFncFrag.items():
        if self.htmlCode is not None:
          fnc.insert(0, self.jsAddUrlParam(self.htmlCode, self.val, isPyData=False))
        self.aresObj.jsOnLoadEvtsFnc.add('''
          $( document ).on('%(eventKey)s', '#%(htmlId)s label', function(event) {
            var useAsync = false; var isChecked = false; var htmlContent = $(this).find('span').html() ;
            if (htmlContent == '') { $(this).find('span').html('<i class="fas fa-check" style="color:%(checkColor)s"></i>'); isChecked = true} else { $(this).find('span').html('') ;}
            var data = %(data)s ; var returnVal = undefined;
            if (!$('#body_loading').length){ 
              var bodyLoading2 = $('<div id="body_loading" name="ares_loading" style="bottom:20px;left:70px;position:fixed;background-color:#F4F4F4;padding:5px"><i class="fas fa-spinner fa-spin" style="margin-left:10px;margin-right:10px"></i><div style="display:inline" id="loading_count">0</div> process running...</div>') ; 
            } ;
            $('body').append(bodyLoading2) ;
            $('#loading_count').html( parseInt($('#loading_count').html()) + 1) ;
            %(jsFnc)s ; 
            if (!useAsync) {
              $('#loading_count').html( parseInt($('#loading_count').html()) - 1) ;
              if ($('#loading_count').html() == '0') { $('#body_loading').remove() ;} }
            if (returnVal != undefined) { return returnVal } ; 
          }) ;''' % {'htmlId': self.htmlId, 'eventKey': eventKey, 'data': self.jsQueryData, 'checkColor': self.getColor('blueColor', 2),
                     'jsFnc': ";".join([f for f in fnc if f is not None])})

  def __str__(self):
    """
    :category: Output function
    :dsc:
      Apply the corresponding function to build the HTML HtmlCheckbox.
      This function is very specific and it has to be defined in each class.
    """
    cssMod, titleTag = self.aresObj.cssObj.get(self.cssTitle), ""
    if cssMod is not None:
      self.addPyCss(self.cssTitle)
      titleTag = "<div class='%s'>%s</div>" % (cssMod().classname, self.title)
    return '''
      <div %(strAttr)s>
        %(titleTag)s
        <div id='%(htmlId)s'></div>
      </div>''' % {'titleTag': titleTag, 'strAttr': self.strAttr(withId=False, pyClassNames=['CssDivNoBorder']), 'htmlId': self.htmlId }

  def to_word(self, document):
    from docx.shared import RGBColor

    selections = self.aresObj.http.get(self.htmlCode).split(',')
    for rec in self.vals:
      p = document.add_paragraph(style='ListBullet')
      runner = p.add_run(rec['value'])
      if rec['value'] in selections:
        runner.font.color.rgb = RGBColor(0x42, 0x24, 0xE9)

  def to_xls(self, workbook, worksheet, cursor):
    selections = self.aresObj.http.get(self.htmlCode).split(',')
    cellTitle = self.title if self.title != '' else 'Checkbox:'
    cell_format = workbook.add_format({'bold': True})
    worksheet.write(cursor['row'], 0, cellTitle, cell_format)
    cursor['row'] += 1
    for rec in self.vals:
      cell_format = workbook.add_format({})
      if rec['value'] in selections:
        cell_format = workbook.add_format({'bold': True, 'font_color': self.getColor('blueColor', 4)})
      worksheet.write(cursor['row'], 0, rec['value'], cell_format)
      cursor['row'] +=1
    cursor['row'] += 1


class HtmlCheckButton(AresHtml.Html):
  mocks = 'Button'
  name, category, callFnc, docCategory = 'Check Button', 'Button', 'checkbutton', 'Advanced'
  __pyStyle = ['CssDivNoBorder']

  def __init__(self, aresObj, text, title, width, widthUnit, height, heightUnit, label, htmlCode, isChecked, isDisable):
    super(HtmlCheckButton, self).__init__(aresObj, 'N', htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.label, self.title, self.isChecked, self.isDisable, self.title = '' if label is None else label, text, isChecked, isDisable, title
    self.css( {'cursor': 'pointer', 'display': 'inline' })
    self.clickEvent = {'Y': [], 'N': []}
    self.jsVal = "%s_data" % self.htmlId
    self.addGlobalVar(self.jsVal, json.dumps(self.vals) )

  @property
  def val(self): self.jsVal

  def click(self, jsFncs, isChecked=False, allevents=False):
    if allevents:
      jsFncs = [jsFncs] if not isinstance(jsFncs, list) else jsFncs
      self.clickEvent = {"Y": jsFncs, "N": jsFncs}
    else:
      if isinstance(jsFncs, list):
        for jsFnc in jsFncs:
          if isChecked:
            self.clickEvent['Y'].append(jsFnc)
          else:
            self.clickEvent['N'].append(jsFnc)
      else:
        if isChecked:
          self.clickEvent['Y'].append(jsFncs)
        else:
          self.clickEvent['N'].append(jsFncs)

  def __str__(self):
    if not self.isDisable:
      self.aresObj.jsOnLoadFnc.add('''
        %(jqId)s.on('click', function(event) {
          var useAsync = false;
          if (!$('#body_loading').length){ 
            var bodyLoading2 = $('<div id="body_loading" name="ares_loading" style="bottom:20px;left:0;position:fixed;background-color:%(lightGrey)s;padding:5px"><i class="fas fa-spinner fa-spin" style="margin-left:10px;margin-right:10px"></i><div style="display:inline" id="loading_count">0</div> process running...</div>') ; 
          } ; $('body').append(bodyLoading2) ; $('#loading_count').html( parseInt($('#loading_count').html()) + 1) ;
          
          var value = 'N' ;
          if ($(this).find('div').css('background-color') == 'rgb(244, 244, 244)' ) {
            var data = { event_label: '%(label)s', event_val: value, event_code: '%(htmlCode)s' } ; %(isNotChecked)s;
            $(this).find('div').css('background-color', 'white') ; $(this).find('div').html('') ; }
          else {
            value = 'Y'; var data = { event_label: '%(label)s', event_val: value, event_code: '%(htmlCode)s' } ;
            %(isChecked)s; $(this).find('div').css('background-color', 'rgb(244, 244, 244)') ; 
            $(this).find('div').html('<i class="fas fa-check" style="margin-bottom:2px;margin-left:2px"></i>') }
          if ( '%(htmlCode)s' != 'None') { %(breadCrumVar)s['params']['%(htmlCode)s'] = value } ;
          %(jsVal)s = value;
          
          if (!useAsync) { 
            $('#loading_count').html( parseInt($('#loading_count').html()) - 1) ;
            if ($('#loading_count').html() == '0') { $('#body_loading').remove() ; } }
        }) ; ''' % {'jqId': self.jqId, 'htmlCode': self.htmlCode, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'jsVal': self.jsVal,
                    'isChecked': ";".join(self.clickEvent['Y']), 'isNotChecked': ";".join(self.clickEvent['N']), 'label': self.label,
                    'lightGrey': self.getColor('greyColor', 2) })

    if self.isChecked:
      return ''' 
          <div %s title="%s">
              <div style="background-color:%s;display:inline-block;vertical-align:bottom;margin-right:5px;float:left;border:1px solid black;width:16px;height:16px">
                  <i class="fas fa-check" style="margin-bottom:2px;margin-left:2px"></i>
              </div>
              %s
          </div>''' % (self.strAttr(pyClassNames=self.pyStyle), self.getColor('greyColor', 2), self.title, self.label)

    return '''<div %s title="%s"><div style="display:inline-block;vertical-align:bottom;margin-right:5px;float:left;border:1px solid black;width:16px;height:16px"></div>%s</div>''' % (self.strAttr(pyClassNames=self.pyStyle), self.title, self.label)
