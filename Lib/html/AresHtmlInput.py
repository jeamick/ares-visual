#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
    'eng':
'''
:dsc:

'''}


import json
import datetime

from ares.Lib.html import AresHtml


class InputText(AresHtml.Html):
  """ Python wrapper for the Html input text element

  """
  references = {'Input Tutorial': 'https://openclassrooms.com/courses/decouvrez-la-puissance-de-jquery-ui/l-autocompletion-1'}
  __pyStyle = ['CssDivNoBorder']
  __reqCss, __reqJs = ['bootstrap', 'font-awesome', 'jqueryui'], ['bootstrap', 'font-awesome', 'jquery']
  name, category, inputType, callFnc, docCategory = 'Input Text', 'Input', "text", 'input', 'Advanced'

  def __init__(self, aresObj, text, placeholder, label, icon, width, widthUnit, height, heightUnit, color, size, align, htmlCode,
               withRemoveButton, autocompleteSrc, tooltip, docBlock, lettersOnly, globalFilter):
    self.autocompleteSrc, self.align, self.label, self.withRemoveButton = autocompleteSrc, align, label, withRemoveButton
    self.placeholder, self._disabled, self.icon = placeholder, '', icon
    super(InputText, self).__init__(aresObj, text, htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, docBlock=docBlock, globalFilter=globalFilter)
    self.color = self.getColor('textColor', 1) if color is None else color
    self.size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    self.css({'clear': 'both', "vertical-align": "middle"})
    if self.htmlCode is not None:
      self.aresObj.htmlCodes[self.htmlCode] = self
      self.change('') # Add the onchange method to update the breadcrumb
      if self.htmlCode in self.aresObj.http:
        self.vals = self.aresObj.http[self.htmlCode]
    if tooltip != '':
      self.tooltip(tooltip)
    if lettersOnly:
      self.keydown("returnVal = ( (event.keyCode >= 65 && event.keyCode <= 90) || event.keyCode == 8 || event.key == '_');")

  def autocomplete(self, dataSrc):
    if isinstance( dataSrc, list):
      dataSrc = {"type": 'static', 'minLength': 1, 'data': dataSrc}
    self.autocompleteSrc = dataSrc
    return self

  def emtpy(self): return '$("#%s input").val("")' % self.htmlId

  @property
  def val(self): return '$("#%s input").val()' % self.htmlId

  @property
  def disabled(self):
    self._disabled = 'disabled'
    return self

  @property
  def jsQueryData(self): return "{ event_val: $(this).find('input').val() }"

  def onDocumentLoadFnc(self): self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, "htmlObj.find('input').val(data);", 'Javascript Object builder')

  def enter(self, jsFncs):
    """
    :category: Javascript Event
    :rubric: JS
    :example: >>> myObj.input(placeholder="Put your tag").enter( " alert() " )
    :dsc:
        Add an javascript action when the key enter is pressed on the keyboard
    :return: The python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    self.jsFrg("keydown", "if (event.keyCode  == 13) { var data = %(data)s; event.preventDefault(); %(jsFnc)s } " % {"jsFnc": ";".join(jsFncs), 'data': self.jsQueryData})
    return self

  def filter(self, aresDf, colName, caseSensitive=False, multiVals=False, exactMath=False, allSelected=True, filterGrp=None):
    """
    :category: Javascript Features - Filter Input
    :rubric: JS
    :type: Front End
    :example: htmlObj.filter(data, 'Country')
    :dsc:
      Wrapper to filter data on the exact content
    """
    if caseSensitive:
      srcObj = "aresObj('%s').split(', ')" % self.htmlCode if multiVals else "aresObj('%s')" % self.htmlCode
      recObj = "rec['%s']" % colName
    else:
      srcObj = "aresObj('%s').split(', ').toLowerCase()" % self.htmlCode if multiVals else "aresObj('%s').toLowerCase()" % self.htmlCode
      recObj = "rec['%s'].toLowerCase()" % colName
    if exactMath:
      if multiVals:
        strFilter = ["( %s.indexOf(%s) >= 0 ) " % (srcObj, recObj)]
      else:
        strFilter = ["( %s == %s )" % (srcObj, recObj)]
    else:
      if multiVals:
        strFilter = ["( %s.indexOf(%s) >= 0 ) " % (srcObj, recObj)]
      else:
        strFilter = ["( %s.indexOf(%s) >= 0 ) " % (recObj, srcObj)]
    if allSelected:
      strFilter.append("( aresObj('%s') == '')" % self.htmlCode)
    if multiVals:
      aresDf.link("change", self.htmlCode, " || ".join(strFilter), filterGrp if filterGrp is not None else "filter_%s" % aresDf.htmlCode, colNames=[colName])
    aresDf.link("input", self.htmlCode, " || ".join(strFilter), filterGrp if filterGrp is not None else "filter_%s" % aresDf.htmlCode, colNames=[colName])
    return self

  def __str__(self):
    """ Return the String representation of a HTML Input object """
    htmlData, textIndent = [], 0
    if self.autocompleteSrc is not None:
      if self.autocompleteSrc['type'] == 'static':
        if self.autocompleteSrc.get('multiple', False):
          src = {'source': 'function( request, response ) { response( $.ui.autocomplete.filter( %s, request.term.split( /,\s*/ ).pop() ) ) }' % self.autocompleteSrc['data'],
                 'minLength': self.autocompleteSrc.get('minLength', 3), 'focus': 'function() { return false ; }',
                 'select': 'function(event, ui){ var terms = this.value.split( /,\s*/ ); terms.pop(); terms.push( ui.item.value ); terms.push( "" );this.value = terms.join( ", " ); %s; return false; }' % self.autocompleteSrc.get('success', '')}
        else:
          src = { 'source': json.dumps(self.autocompleteSrc['data']), 'minLength': self.autocompleteSrc.get('minLength', 3),
                  'select': 'function(event, ui){ %s; }' % self.autocompleteSrc.get('success', '') }
        src = "{ %s }" % ",".join(["%s: %s" % (key, val) for key, val in src.items()])
      self.aresObj.jsOnLoadFnc.add("$('#%(htmlId)s input').autocomplete( %(dataSrc)s )" % {'htmlId': self.htmlId, 'dataSrc': src })

    self.addGlobalFnc('RemoveFilter(htmlId)', "$('#' + htmlId + ' input').val(''); $('#' + htmlId + ' input').change() ;", 'Javascript function to remove the content of an element and trigger a change event')
    if self.label:
      htmlData.append('''<label style='height:25px;color:%s;font-size:%s;margin-bottom:-10px;padding-bottom:0px;'>%s</label>''' % (self.color, self.size, self.label))
    htmlData.append('<div %(strAttr)s><div style="height:100%%;width:100%%;">' % {'strAttr': self.strAttr(pyClassNames=['CssDivNoBorder'])})
    if self.icon:
      htmlData.append('<span class="%s" style="position:absolute;font-size:15px;left:7px;top:5px;"></span>' % self.icon)
      textIndent = 30
    htmlData.append('<input type="%(inputType)s" %(disabled)s placeholder="%(placeholder)s" class="form-control" value="%(vals)s" style="text-indent:%(textIndent)spx;height:27px;width:100%%"/>' % {'inputType': self.inputType, 'disabled': self._disabled, 'placeholder': self.placeholder, 'textIndent': textIndent, 'vals': self.vals})
    htmlData.append('</div>')
    if self.withRemoveButton:
      htmlData.append('''<div onclick="RemoveFilter('%(htmlId)s')" style="margin-top:-27px;z-index:1;float:right;width:25px;height:100%%;padding:5px;cursor:pointer;position:relative;color:%(darkRed)s" title="Remove filter" class="fas fa-user-times">&nbsp;</div>''' % {'htmlId': self.htmlId, 'darkRed': self.getColor('redColor', 4)})
    htmlData.append('</div>')
    return ''.join(htmlData)

  def to_word(self, document):
    p = document.add_paragraph()
    p.add_run("Input: ")
    runner = p.add_run( self.aresObj.http.get(self.htmlCode, self.vals) )
    runner.bold = True

  def to_xls(self, workbook, worksheet, cursor):
    """

    :param workbook:
    :param worksheet:
    :param cursor:
    :return:
    :link xlxWritter Documentation: https://xlsxwriter.readthedocs.io/format.html
    """
    cell_format = workbook.add_format({'bold': True, 'font_color': self.color, 'font_size': self.size})
    worksheet.write(cursor['row'], 0, self.vals, cell_format)
    cursor['row'] += 2


class InputPass(InputText):
  """ Python rapper for the Html input password element """
  references = {'Input Password': 'https://developer.mozilla.org/fr/docs/Web/HTML/Element/Input/password',
                'Input Password W3C': 'https://www.w3schools.com/howto/howto_js_password_validation.asp',
                'Input Password Event': 'https://www.w3schools.com/howto/howto_js_toggle_password.asp'}
  inputType = "password"
  name, category, callFnc, docCategory = 'Input Password', 'Input', 'pwd', 'Advanced'


class InputInt(InputText):
  """ Python wrapper for the Html input integer element """
  references = {'Input Forms': 'https://www.alsacreations.com/tuto/lire/1409-formulaire-html5-type-number.html'}
  inputType = "number"
  __pyStyle = ['CssInput', 'CssInputInt', 'CssInputLabel']
  name, category, callFnc, docCategory = 'Input Integer', 'Input', 'inputInt', 'Advanced'


class InputRange(AresHtml.Html):
  """ Python wrapper for the HTML input range element

  :example
  aresObj.inputRange('Coucou', number=11)
  """
  references = {'Input Range': 'https://www.alsacreations.com/tuto/lire/1410-formulaire-html5-type-range.html'}
  name, category, callFnc, docCategory = 'Input Range', 'Input', 'inputRange', 'Advanced'
  __pyStyle = ['CssInput', 'CssInputText', 'CssInputLabel']

  def __init__(self, aresObj, recordSet, color, size, align, width, widthUnit, height, heightUnit, htmlCode):
    self.align = align
    super(InputRange, self).__init__(aresObj, recordSet, htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    if not 'step' in self.vals:
      self.vals['step'] = 1
    self.color = self.getColor('baseColor', 2) if color is None else color
    self.size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    self.css( {"display": 'inline-block'})
    if self.htmlCode is not None:
      self.aresObj.htmlCodes[self.htmlCode] = self
      self.change('')

  @property
  def val(self): return '$("#%s input").val()' % self.htmlId

  @property
  def data(self): return "{ event_val: $(this).find('input').val() }"

  def change(self, jsFncs):
    if isinstance(jsFncs, list):
      for jsFnc in jsFncs:
        self.jsFrg('change', jsFnc)
    else:
      self.jsFrg('change', jsFncs)

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
      if ( data.label != undefined) {htmlObj.append("<label for='" + data.label + "' style='display:inline-block;vertical-align:middle;text-align:%s;padding-left:6px;color:%s;font-size:%s;font-weight:bold;'>" + data.label + "</label>") } ;
      htmlObj.append("<input oninput='range_weight_disp.value=this.value' min="+ data.min + " max="+ data.max + " step="+ data.step + " type='range' placeholder='" + data.placeholder + " ' value=" + data.text + ">");
      htmlObj.append("<output id='range_weight_disp'></output>");
      ''' % (self.align, self.color, self.size), 'Javascript Object builder')

  def __str__(self):
    """ Return the String representation of a HTML Input object """
    return '<div %s></div>' % self.strAttr(pyClassNames=self.__pyStyle)


class DatePicker(AresHtml.Html):
  """ Python Wrapper for the Html and Jquery UI datepicker object

  """
  references = {'Date Picker Jquery': 'https://jqueryui.com/datepicker/'}
  __reqCss, __reqJs = ['bootstrap', 'font-awesome'], ['bootstrap', 'jquery', 'font-awesome']
  name, category, callFnc, docCategory = 'Date Picker', 'Input', 'date', 'Advanced'
  __pyStyle = ['CssDivNoBorder', 'CssDivCursor']

  def __init__(self, aresObj, label, color, size, yyyy_mm_dd, htmlCode, frequency, placeholder, changeMonth,
               changeYear, showOtherMonths, selectOtherMonths, selectedDts, selectedCss, excludeDts, useDefault, withRemoveButton,
               width, widthUnit, height, heightUnit):
    if frequency is not None:
      # Get the next days (to check if we are not in a particular date
      cobDate = datetime.datetime.today()
      if len(frequency) > 1:
        fType, fCount = frequency[0], frequency[2]
      else:
        fType, fCount = frequency[0], 0
      if not fType in ['T', 'W', 'M', 'Y']:
        raise Exception("%s frequence not in the list T, W, M and Y" % frequency)

      if fType == 'T':
        for i in range(0, int(fCount) + 1):
          cobDate = cobDate - datetime.timedelta(days=1)
          while cobDate.weekday() in [5, 6]:
            cobDate = cobDate - datetime.timedelta(days=1)
        self.value = cobDate.strftime('%Y-%m-%d')
      elif fType == 'M':
        endMontDate = datetime.datetime(cobDate.year, cobDate.month - int(fCount), 1)
        endMontDate = endMontDate - datetime.timedelta(days=1)
        while endMontDate.weekday() in [5, 6]:
          endMontDate = endMontDate - datetime.timedelta(days=1)
        self.value = endMontDate.strftime('%Y-%m-%d')
      elif fType == 'W':
        cobDate = cobDate - datetime.timedelta(days=1)
        while cobDate.weekday() != 4:
          cobDate = cobDate - datetime.timedelta(days=1)
        cobDate = cobDate - datetime.timedelta(days=(int(fCount) * 7) )
        self.value = cobDate.strftime('%Y-%m-%d')
      elif fType == 'Y':
        endYearDate = datetime.datetime(cobDate.year - int(fCount), 1, 1)
        endYearDate = endYearDate - datetime.timedelta(days=1)
        while endYearDate.weekday() in [5, 6]:
          endYearDate = endYearDate - datetime.timedelta(days=1)
        self.value = endYearDate.strftime('%Y-%m-%d')
    else:
      if yyyy_mm_dd == '':
        cobDate = datetime.datetime.today() - datetime.timedelta(days=1)
        while cobDate.weekday() in [5, 6]:
          cobDate = cobDate - datetime.timedelta(days=1)
        self.value = cobDate.strftime('%Y-%m-%d')
      else:
        self.value = yyyy_mm_dd

    super(DatePicker, self).__init__(aresObj, {'label': label, 'date': self.value, 'selectedDts': []}, htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.color = self.getColor('baseColor', 2) if color is None else color
    self.css( {"display": "inline-block", "vertical-align": "middle", "font-size": self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size, "clear": "both"})
    self.placeholder, self.changeMonth, self.changeYear, self.showOtherMonths, self.selectOtherMonths = placeholder, changeMonth, changeYear, showOtherMonths, selectOtherMonths
    self.selectedCss, self.withRemoveButton = selectedCss, withRemoveButton
    self.vals['options'] = {'dateFormat': 'yy-mm-dd', 'changeMonth': json.dumps(self.changeMonth),
                            'changeYear': json.dumps(self.changeYear), 'excludeDts': excludeDts,
                            'showOtherMonths': json.dumps(self.showOtherMonths),
                            'selectOtherMonths': json.dumps(self.selectOtherMonths)}
    self.vals['selectedDts'] = [] if selectedDts is None else selectedDts
    if self.htmlCode is not None:
      self.aresObj.htmlCodes[self.htmlCode] = self
      if self.htmlCode in self.aresObj.http:
        self.vals['date'] = self.aresObj.http[self.htmlCode]
      else:
        if useDefault:
          # Add to the http parameteres if missing and as there is always a default value
          # This parameter will never block a report by default (by using the variable useDefault)
          self.aresObj.http[self.htmlCode] = self.vals['date']
      self.change('')

  @property
  def val(self): return '$("#%s input").val()' % self.htmlId

  @property
  def jsQueryData(self): return "{ event_val: $('#%s input').val() }" % self.htmlId

  def jsSetVal(self, jsVal, isPyData=False):
    if isPyData:
      jsVal = json.dumps(jsVal)
    return '$("#%s input").datepicker("setDate", %s)' % (self.htmlId, jsVal)

  def initVal(self, val): self.vals['date'] = val

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      var htmlId = htmlObj.attr('id') ;
      data.options.changeMonth = (data.options.changeMonth === 'true');
      data.options.changeYear = (data.options.changeYear === 'true');
      data.options.showOtherMonths = (data.options.showOtherMonths === 'true');
      data.options.selectOtherMonths = (data.options.selectOtherMonths === 'true');
      $("#"+ htmlId +" p").html(data.label) ; $("#"+ htmlId +" input").datepicker( data.options ).datepicker('setDate', data.date) ;
      if (data.selectedDts.length > 0) {
        var selectedDt = {} ;
        data.selectedDts.forEach( function(dt) { var jsDt = new Date(dt); selectedDt[jsDt.toISOString().split('T')[0]] = jsDt;  }) ;
        if (data.options.excludeDts === true) { 
          function renderCalendarCallbackExc(intDate) {var utc = intDate.getTime() - intDate.getTimezoneOffset()*60000; var newDate = new Date(utc); var Highlight = selectedDt[newDate.toISOString().split('T')[0]]; if (Highlight) { return [false, '', '']; } else { return [true, '', '']; } } ; 
          $("#"+ htmlId +" input").datepicker("option", "beforeShowDay", renderCalendarCallbackExc ); }
        else { 
          function renderCalendarCallback(intDate) {var utc = intDate.getTime() - intDate.getTimezoneOffset()*60000; var newDate = new Date(utc); var Highlight = selectedDt[newDate.toISOString().split('T')[0]]; if (Highlight) { return [true, "%s", '']; } else { return [false, '', '']; } } ; 
          $("#"+ htmlId +" input").datepicker("option", "beforeShowDay", renderCalendarCallback );}
      } ''' % self.selectedCss, 'Javascript Object builder')

  def addAttr(self, key, val, isPyData=True):
    if isPyData:
      val = json.dumps(val)
    self.vals['options'][key] = val

  def selectedDates(self, dts, css='CssLabelDates'):
    self.selectedCss = self.addPyCss(css)
    self.vals['selectedDts'].extend(dts)

  def __str__(self):
    """ Return the String representation of a Date picker object """
    self.aresObj.jsOnLoadFnc.add('$("#%(htmlId)s div#show").click(function() { var visible = $("#%(htmlId)s input").datepicker("widget").is(":visible"); if( visible ) { $("#%(htmlId)s input").datepicker("hide"); } else { $("#%(htmlId)s input").datepicker("show"); $("#%(htmlId)s input").datepicker("widget").css("z-index", 600);} }); ' % {"htmlId": self.htmlId})
    removeOpt = ''
    if self.withRemoveButton:
      removeOpt = '<div id="remove_%s" style="height:16px;color:%s;display:inline-block;margin-left:5px;font-size:16px" title="remove selection" class="far fa-calendar-times"></div>' % (self.htmlId , self.getColor('redColor', 4))
      self.aresObj.jsOnLoadFnc.add('''
        $('#remove_%(htmlId)s').on('click', function(event) {
          $('#%(htmlId)s input').datepicker('setDate', null); 
          $('#%(htmlId)s input').change() ;
        }) ''' % {'htmlId': self.htmlId} )

    return '''
          <div %s>
            <p style='vertical-align:middle;padding-left:6px;color:%s;display:inline-block;margin:0;text-align:center;height:25px'></p>
            <input type="text" class="datepicker form-control" style="padding:0px;display:inline;text-align:center;width:110px;height:27px">
            <div id="show" style="height:32px;display:inline-block"><i style="padding-top:8px;font-size:16px" class="far fa-calendar-alt"></i></div>
            %s
          </div>''' % (self.strAttr(pyClassNames=self.pyStyle), self.color, removeOpt)


class TimePicker(AresHtml.Html):
  references = {'Source Code': 'https://github.com/jonthornton/jquery-timepicker'}
  __reqCss, __reqJs = ['timepicker'], ['timepicker']
  name, category, callFnc, docCategory = 'Time Picker', 'Input', 'date', 'Advanced'
  __pyStyle = ['CssDivNoBorder', 'CssDivCursor']

  def __init__(self, aresObj, value, label, color, size, htmlCode):
    if isinstance(value, str):
      value = {"time": value}
    self.label = label
    if 'options' not in value:
      value['options'] = {'timeFormat': 'H:i:s'}
    super(TimePicker, self).__init__(aresObj, value, htmlCode=htmlCode)
    self.color = self.getColor('baseColor', 2) if color is None else color
    self.size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    if self.htmlCode is not None:
      self.aresObj.htmlCodes[self.htmlCode] = self
      if self.htmlCode in self.aresObj.http:
        self.vals['date'] = self.aresObj.http[self.htmlCode]
      self.change('')

  @property
  def val(self): return '$("#%s input").val()' % self.htmlId

  @property
  def jsQueryData(self): return "{ event_val: $('#%s input').val() }" % self.htmlId

  def addAttr(self, key, val, isPyData=True):
    if isPyData:
      val = json.dumps(val)
    self.vals['options'][key] = val

  def initVal(self, val): self.vals['time'] = val

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      var htmlId = htmlObj.attr('id') ;
      if (data.time == '') { data.time = new Date() } ;
      $("#"+ htmlId +" input").timepicker( data.options ) ;
      $("#"+ htmlId +" input").timepicker( 'setTime', data.time) ; 
      ''', 'Javascript Object builder')

  def jsSetVal(self, jsVal, isPyData=False):
    if isPyData:
      jsVal = json.dumps(jsVal)
    return '$("#%s input").timepicker("setTime", %s)' % (self.htmlId, jsVal)

  def __str__(self):
    return '''
      <div %s>
        <p style='vertical-align:middle;padding-left:6px;color:%s;font-size:%s;display:inline-block;margin:0;text-align:center;height:25px'>%s</p>
        <input type="text" class="time" style="margin-top:5px;text-align:center;width:80px;height:27px" />
      </div> ''' % (self.strAttr(pyClassNames=self.pyStyle), self.color, self.size, self.label)


class Search(AresHtml.Html):
  references = {'Search': 'https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_anim_search'}
  name, category, callFnc, docCategory = 'Search', 'Input', 'search', 'Advanced'
  __pyStyle = []

  def __init__(self, aresObj, text, placeholder, color, size, align, height, heightUnit, htmlCode, tooltip, extensible):
    self.placeholder, self.extensible = placeholder, extensible
    super(Search, self).__init__(aresObj, text, htmlCode=htmlCode, height=height, heightUnit=heightUnit)
    if self.htmlCode is not None:
      self.aresObj.htmlCodes[self.htmlCode] = self
      self.change('') # Add the onchange method to update the breadcrumb
      if self.htmlCode in self.aresObj.http:
        self.vals = self.aresObj.http[self.htmlCode]
    if tooltip != '':
      self.tooltip(tooltip)

  @property
  def val(self): return '$("#%s input").val()' % self.htmlId

  @property
  def jsQueryData(self): return "{ event_val: $(this).parent().find('input').val() }"

  def onDocumentLoadFnc(self): self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, "htmlObj.find('input').val(data);", 'Javascript Object builder')

  @property
  def eventId(self): return '$("#%s_button")' % self.htmlId

  def __str__(self):
    """ Return the String representation of a HTML Input object """
    pyCssCls = self.addPyCss('CssSearch') if not self.extensible else self.addPyCss('CssSearchExt')
    return '''
      <div %(attr)s style="width:100%%;display:block">
          <input class="%(pyCssCls)s" type="text" name="search" placeholder="%(placeholder)s">
          <span id="%(htmlId)s_button" class="fas fa-search" style="margin-top:-30px;font-size:20px;right:30px;z-index:1;float:right;width:25px;cursor:pointer;position:absolute;color:%(blueColor)s"></span>
      </div>''' % {"attr": self.strAttr(pyClassNames=self.__pyStyle), "pyCssCls": pyCssCls, "placeholder": self.placeholder, 'htmlId': self.htmlId, 'blueColor': self.getColor("blueColor", 13)}

