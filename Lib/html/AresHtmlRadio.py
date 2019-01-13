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


class Radio(AresHtml.Html):
  """ Python Wrapper of the HTML radio buttons """
  references = {'Bootstrap Forms': 'https://www.w3schools.com/bootstrap/bootstrap_forms_inputs.asp'}
  __reqCss, __reqJs = ['font-awesome'], ['font-awesome', 'jquery']
  name, category, callFnc, docCategory = 'Radio Buttons', 'Button', 'radio', 'Advanced'
  __pyStyle = ['CssDivNoBorder']
  cssTitle =  "CssTitle4"

  def __init__(self, aresObj, vals, checked, htmlCode, width, widthUnit, height, heightUnit, radioVisible, event,
               withRemoveButton, dfColumn, align, globalFilter, tooltip, title):
    hasJsEvents, self.title = False, title
    if issubclass(type(vals), ares_pandas.DataFrame):
      if globalFilter:
        globalFilter = {'jsId': vals.htmlCode, 'colName': dfColumn}
      vals = vals[dfColumn].unique().tolist()
    if isinstance(vals, list) and not isinstance(vals[0], dict):
      tmpVals = [ {'value': str(v)} for v in vals]
      tmpVals[0]['checked'] = True
      vals = tmpVals

    for rec in vals:
      rec['__radio'] = radioVisible
      if not 'checked' in rec and checked is not None and rec['value'] == checked:
        rec['checked'] = True
      if 'event' in rec:
        hasJsEvents = True
    if withRemoveButton:
      vals.append( {'value': '_remove'} )
    super(Radio, self).__init__(aresObj, vals, htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, globalFilter=globalFilter)

    self._jsStyles = {'tooltip': tooltip}
    cssMod = self.aresObj.cssObj.get("CssRadioButton")
    self.addPyCss("CssRadioButton")
    self._jsStyles['normal'] = cssMod().classname
    cssMod = self.aresObj.cssObj.get("CssRadioButtonSelected")
    self.addPyCss("CssRadioButtonSelected")
    self._jsStyles['selected'] = cssMod().classname
    if htmlCode is not None:
      self.aresObj.htmlCodes[self.htmlCode] = self
    self.css({'display': 'inline-block', 'margin': '5px 0 0 0', 'padding': 0, 'text-align': align})
    for evts in ['click', 'change']:
      # Add the source to the different events
      self.jsFrg(evts, '''
        var data = %(jsQueryData)s;
        $(this).parent().children().attr('class', '%(cssNormalStyle)s');
        $(this).attr('class', '%(cssSelectedStyle)s');
        $(this).find('input').prop('checked', true);
        if ('%(htmlCode)s' != 'None') { %(breadCrumVar)s['params']['%(htmlCode)s'] = %(jsVal)s } ;
        ''' % {'jsVal': self.val, "htmlId": self.htmlId, 'htmlCode': self.htmlCode, 'jsQueryData': self.jsQueryData,
               'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'cssSelectedStyle': self._jsStyles['selected'],
               'cssNormalStyle': self._jsStyles['normal']} )

    if event is not None:
      self.change(aresObj.jsPost(event['script'], event.get('htmlCodes'), event.get('success', '')))
    elif hasJsEvents:
      for rec in self.vals:
        if 'event' in rec:
          if 'script' in rec['event']:
            self.click(rec['value'], aresObj.jsPost(rec['event']['script'], None, isPyData=rec['event'].get('isPyData', True) ))
          elif 'url' in rec['event']:
            if rec['event'].get('method', 'POST') == 'POST':
              self.click( aresObj.jsPost(rec['event']['url'], None, isPyData=rec['event'].get('isPyData', True), isDynUrl=rec['event'].get('isDynUrl', False) ), rec['value'])
            elif rec['event'].get('method', 'POST') == 'GET':
              self.click(aresObj.jsGet(rec['event']['url'], None, isPyData=rec['event'].get('isPyData', True), isDynUrl=rec['event'].get('isDynUrl', False)), rec['value'])
            elif rec['event'].get('method', 'POST') == 'LINK':
              self.click( aresObj.jsGoTo( rec['event']['url'], isPyData=rec['event'].get('isPyData', False), urlName=rec['event'].get('urlName', '_self') ), rec['value'] )

  def tooltip(self, value, location='top'):
    self._jsStyles['tooltip'] = value
    return self

  def initVal(self, val):
    for rec in self.vals:
      rec['checked'] = True if rec['value'] == val else False

  @property
  def jsQueryData(self):
    """
    :category: Javascript features
    :dsc: Python function to define the Javascript object to be passed in case of Ajax call internally or via external REST service with other languages
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    return "{ event_val: $(this).find('input').val(), event_code: '%s'}" % self.htmlId

  @property
  def jqIdChecked(self): return  "$('input[name=input_%s]:checked') " % self.htmlId

  @property
  def val(self): return "$('input[name=input_%s]:checked').val()" % self.htmlId

  def click(self, jsFnc, radioVal=None):
    if radioVal is None:
      self.jsFrg('click', "%(jsFnc)s" % {'jsFnc': jsFnc})
    else:
      self.jsFrg('click', "if ( data['event_val'] == %(radioVal)s ) { %(jsFnc)s };" % {"radioVal": json.dumps(radioVal), 'jsFnc': jsFnc})

  @property
  def jqId(self): return "$('#%s label')" % self.htmlId

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    self.jsUpdateDataFnc = '''%(pyCls)s($('#%(htmlId)s'), %(htmlId)s_data, %(jsStyles)s) ; 
      if(%(htmlCode)s != null) { %(breadCrumVar)s['params'][%(htmlCode)s] = %(jsVal)s}
      ''' % {'pyCls': self.__class__.__name__, 'jqId': self.jqId, 'htmlId': self.htmlId, 'htmlCode': json.dumps(self.htmlCode),
             'jsVal': self.val, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, "jsStyles": json.dumps(self._jsStyles)}
    if self.dataSrc is None or self.dataSrc.get('type') != 'url':
      self.aresObj.jsOnLoadFnc.add(self.jsUpdateDataFnc)

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' htmlObj.empty() ; 
      var htmlId = htmlObj.attr('id'); var withRemoveButton = false;
      data.forEach(function(rec){
        if (rec.value.indexOf('_remove') >= 0 ) {withRemoveButton = true}
        else {
          var style = jsStyles.normal; var label = rec.value; var radioDisplay = "style='margin-left:5px;'"; var tooltip = "";
          if (rec.tooltip != undefined) {tooltip = rec.tooltip};
          if (rec.label != undefined) {label = rec.label};
          if (!rec.__radio) {var radioDisplay = "style='display:none'"};
          if (rec.checked) {
            htmlObj.append("<label title='"+ tooltip+"' name='"+ htmlId +"' class='"+ jsStyles.selected + "'>"+ label +"<input checked type='radio' "+ radioDisplay +" name='input_"+ htmlId +"' value='" + rec.value + "'></label>" ) ;}
          else {htmlObj.append( "<label data-toggle='tooltip' title='"+ tooltip+"' name='"+ htmlId +"' class='"+ jsStyles.normal + "'>"+ label +"<input type='radio' "+ radioDisplay +" name='input_"+ htmlId +"' value='" + rec.value + "'></label>" ) } } }) ;
      htmlObj.find('label').tooltip();
      if (jsStyles.tooltip != ""){ 
        var tip = $('<i class="fas fa-info-circle" title="'+ jsStyles.tooltip +'"></i>');
        tip.tooltip(); htmlObj.append($("<div style='width:100%;text-align:right'></div>").append(tip))}
      if (withRemoveButton) {
        htmlObj.append( "<label name='"+ htmlId +"'><i class='fas fa-user-times'></i><input type='radio' style='display:none' name='input_"+ htmlId +"' value=''></label>");}''', 'Javascript Object builder')

  def __str__(self):
    cssMod, titleTag = self.aresObj.cssObj.get(self.cssTitle), ""
    if cssMod is not None:
      self.addPyCss(self.cssTitle)
      titleTag = "<div class='%s'>%s</div>" % (cssMod().classname, self.title)
    return '%(titleTag)s<div %(strAttr)s></div>' % {'strAttr': self.strAttr(pyClassNames=['CssDivNoBorder']), "titleTag": titleTag}

  def to_word(self, document):
    p = document.add_paragraph()
    p.add_run("Selected: ")
    runner = p.add_run( self.aresObj.http.get(self.htmlCode, self.vals) )
    runner.bold = True

  def to_xls(self, workbook, worksheet, cursor):
    """
    :link xlxWritter Documentation: https://xlsxwriter.readthedocs.io/format.html
    """
    worksheet.write(cursor['row'], 0, "Selected:")
    worksheet.write(cursor['row'], 1, self.aresObj.http.get(self.htmlCode, self.vals) )
    cursor['row'] += 2


class Switch(AresHtml.Html):
  """ Python wrapper to the HTML Switch component """
  references = {'Example 1': 'http://thecodeplayer.com/walkthrough/pure-css-on-off-toggle-switch',
                'Example 2': 'https://codepen.io/mburnette/pen/LxNxNg'}
  __reqCss, __reqJs = ['bootstrap', 'font-awesome'], ['bootstrap', 'font-awesome', 'jquery']
  name, category, callFnc, docCategory = 'Switch Buttons', 'Button', 'switch', 'Advanced'
  __pyStyle = ['CssRadioSwitch', 'CssRadioSwitchLabel', 'CssRadioSwitchChecked']

  def __init__(self, aresObj, recordSet, label, color, size, width, widthUnit, height, heightUnit, htmlCode):
    self.width, self.jsChange, self.label, self.size = width, '', label if label is not None else '', size
    super(Switch, self).__init__(aresObj, recordSet, htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.clicks = {'on': [], 'off': []}
    self.color = self.getColor('baseColor', 2) if color is None else color
    self.css( {"display": 'inline-block'})
    if htmlCode is not None:
      self.aresObj.htmlCodes[self.htmlCode] = self

  @property
  def val(self): return "$('#%(htmlId)s p').html()" % {'htmlId': self.htmlId}

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      var htmlId = htmlObj.attr('id') ; 
      if ( data.off == data.checked ) { $('#'+ htmlId +' input').prop('checked', false) ; $('#'+ htmlId +' p').html(data.off) ;}
      else { $('#'+ htmlId +' input').prop('checked', true); $('#'+ htmlId +' p').html(data.on) ; }; 
      window[htmlId + '_data'] = $('#'+ htmlId +' p').html();
      ''', 'Javascript Object builder')

  def click(self, onFncs=None, offFncs=None):
    if onFncs is not None:
      self.clicks['on'].extend(onFncs)
    if offFncs is not None:
      self.clicks['off'].extend(offFncs)

  def initVal(self, val): self.vals['checked'] = val

  def __str__(self):
    """ String representation of the HTML Switch component """
    self.aresObj.jsOnLoadFnc.add('''
      $('#%(htmlId)s label').click(function() { 
          if( !$('#%(htmlId)s input').is(':checked') ) { $('#%(htmlId)s input').prop('checked', true); %(jsVal)s = '%(val2)s'; %(offFncs)s}
          else { $('#%(htmlId)s input').prop('checked', false); %(jsVal)s = '%(val1)s' ; %(onFncs)s}
          %(jsChange)s ; $('#%(htmlId)s p').html(%(jsVal)s);
          if ( '%(htmlCode)s' != 'None') { %(breadCrumVar)s['params']['%(htmlCode)s'] = %(jsVal)s } ; } );
      ''' % {'jsVal': self.jsVal, "htmlId": self.htmlId, 'htmlCode': self.htmlCode, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar,
             'onFncs': ";".join(self.clicks['on']), 'offFncs': ";".join(self.clicks['off']),
             'val1': self.vals['off'], 'val2': self.vals['on'], 'jsChange': self.jsChange})
    if 'text' in self.vals:
      return '''
        <div %s>
            <div style="display:inline-block;height:25px;color:%s;font-size:%spx">%s</div>
            <input type="checkbox"/>
            <label style="width:50px;display:inline-block" for="switch">&nbdp;</label>
            <p style="display:inline-block;margin-left:3px;font-weight:bold" title="%s">%s</p>
        </div> ''' % (self.strAttr(pyClassNames=self.pyStyle), self.color, self.size, self.label, self.vals['text'], self.vals['off'])
    return '<div %s><input type="checkbox" /><label style="width:50px;display:inline-block" for="switch">&nbdp;</label></div>' % (self.strAttr(pyClassNames=self.pyStyle))

