#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import re
import json

from ares.Lib.html import AresHtml
from ares.Lib.AresImports import requires


DSC = {
    'eng':
'''
:dsc:
# HTML

## HTML Event Components

This below module is defining HTML components expecting Javascript events. Each of them are using specific function in 
order to update their content or to run some functions on the server side.

Components using Ajax functions will be fully working only if a server is defined. 

'''}


class TextArea(AresHtml.Html):
  """ Python interface to the TextArea HTML component

  :example aresObj.textArea('Date')
  """
  references = {'Textarea W3C': 'https://www.w3schools.com/tags/tag_textarea.asp'}
  name, category, callFnc, docCategory = 'Text Area', 'Text', 'textArea', 'Standard'
  __pyStyle = ['CssDivNoBorder']

  def __init__(self, aresObj, text, title, label, width, widthUnit, rows, readOnly, backgroundColor, spellcheck, htmlCode, docBlock, placeholder):
    super(TextArea, self).__init__(aresObj, text, htmlCode=htmlCode, width=width, widthUnit=widthUnit, docBlock=docBlock)
    self.spellcheck, self.placeholder, self.label = spellcheck, placeholder, label
    self.width, self.title, self.rows, self.readOnly, self.backgroundColor, self.widthUnit = width, title, rows, readOnly, backgroundColor, widthUnit
    if self.htmlCode is not None:
      self.change('')
    self.css( {"margin": "5px 0 10px 0"} )

  def onDocumentLoadFnc(self): self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.html( data ); ''', 'Javascript Object builder')

  @property
  def empty(self):
    """
    :category: Javascript features
    :example: myObj.empty
    :returns: Javascript string with the function to remove the content of the Textarea
    :dsc:
      Property to write a function to remove the content of a Textarea. This can be trigger during a javascript event.
      Even if this function does not have a js, this should be written to be used in the Javascript
    """
    return '%s.val("")' % self.jqId

  @property
  def jqId(self):
    """
    :category: Javascript features
    :example: myObj.jqId
    :dsc: Python property to get a unique Jquery ID function for a given AReS Object
    :return: Javascript String of the variable used to defined the Jquery object in Javascript
    """
    return "$('#%s textarea')" % self.htmlId

  def __str__(self):
    """ Return the item with a text area and a button """
    readOnlyAttr = 'onfocus="this.blur()" readonly' if self.readOnly else ''
    readOnlyAttr = '%s spellcheck="true"' % readOnlyAttr if self.spellcheck else '%s spellcheck="false"' % readOnlyAttr
    if self.title is not None:
      return '<div %s><a class="anchorjs-link" style="font-size:%s;color:%s;font-weight:bold;">%s</a>%s<textarea rows="%s" style="resize:none;margin-bottom:10px;width:%s%s;background-color:%s;border:1px solid grey" %s></textarea></div>' % (self.strAttr(pyClassNames=self.pyStyle), self.aresObj.pyStyleDfl['headerFontSize'], self.getColor('baseColor', 2), self.title, self.helper, self.rows, self.width, self.widthUnit, self.backgroundColor, readOnlyAttr)
    if self.label is not None:
      return '<div %s><a class="anchorjs-link" style="color:%s;">%s</a>%s<textarea rows="%s" style="resize:none;margin-bottom:10px;width:%s%s;background-color:%s;border:1px solid grey" %s></textarea></div>' % (
        self.strAttr(pyClassNames=self.pyStyle), self.getColor('baseColor', 2), self.label, self.helper, self.rows, self.width, self.widthUnit, self.backgroundColor, readOnlyAttr)

    return '''
      <div %(strAttr)s>
        <textarea rows="%(rows)s" style="resize:none;margin-bottom:10px;width:100%%;background-color:%(backgroundColor)s" class="form-control" %(readOnlyAttr)s placeholder="%(placeholder)s"></textarea>
      </div>''' % {"strAttr": self.strAttr(pyClassNames=self.pyStyle), "rows": self.rows,
                   "backgroundColor": self.backgroundColor, "readOnlyAttr": readOnlyAttr, "placeholder": self.placeholder}


class ProgressBar(AresHtml.Html):
  """ Python wrapper for the Html and javascript progress bar

  :example
  aresObj.progressbar(10)
  """
  references = {'Progress Bar Jquery' :'https://jqueryui.com/progressbar/'}
  __reqCss, __reqJs = ['jqueryui'], ['jquery']
  name, category, callFnc, docCategory = 'Progress Bar', 'Event', 'progressbar', 'Standard'
  __pyStyle= ['CssDivNoBorder']

  def __init__(self, aresObj, number, width, widthUnit, height, heightUnit):
    super(ProgressBar, self).__init__(aresObj, number, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self._jsStyles = {"background": self.getColor('blueColor', 2)}

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__,
      ''' htmlObj.progressbar( {value: parseFloat(data) } ).find('div').css( jsStyles ) ; ''', 'Javascript Object builder')

  @property
  def val(self):
    """
    :category: Javascript features
    :rubric: JS
    :example: >>> myObj.val
    :returns: Javascript string with the function to get the current value of the component
    :dsc:
      Property to get the jquery value of the HTML object in a python HTML object.
      This method can be used in any jsFunction to get the value of a component in the browser.
      This method will only be used on the javascript side, so please do not consider it in your algorithm in Python
    """
    return '%s.progressbar("value")' % self.jqId

  def addAttr(self, key, val):
    self._jsStyles[key] = val

  def __str__(self):
    """
    :category: HTML features
    :rubric: HTML
    :example: >>> str( myObj )
    :returns: The String HTML Container of the object
    """
    return '<div %s></div>' % self.strAttr(pyClassNames=self.pyStyle)

  @staticmethod
  def matchMarkDown(val):
    return re.match("%%%%([0-9]*)%", val)

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj):
    if aresObj is not None:
      getattr(aresObj, 'progressbar')(regExpResult.group(1))
    return ["aresObj.progressbar(%s)" % regExpResult.group(1)]

  @classmethod
  def jsMarkDown(self, vals):
    return "%%%%" + str(vals) + "%"


class Slider(AresHtml.Html):
  """ Python wrapper for the Html and javascript Slider

  """
  references = {'Slider Jquery': 'https://jqueryui.com/slider/'}
  __reqCss, __reqJs = ['bootstrap', 'jqueryui'], ['bootstrap', 'jqueryui']
  name, category, callFnc, docCategory = 'Slider', 'Others', 'slider', 'Advanced'

  def __init__(self, aresObj, value, title, type, range, animate, step, min, max, width, widthUnit, height, heightUnit, htmlCode):
    if type == 'integer':
      try:
        int(value)
      except:
        aresObj.log("Slider is expected type as a number by default - value = %s " % value)
        raise Exception("Slider is expected type as a number by default - value = %s " % value)

    super(Slider, self).__init__(aresObj, value, htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.type, self._jsStyles, self.title = type, {'type': type}, title
    self.vals = {'animate': animate, 'min': min, 'max': max, 'step': step}
    if range is not None:
      self.vals['range'] = range
    if isinstance(value, list) and len(value) == 2:
      self.vals['range'] = True
      self.vals['values'] = value
    else:
      self.vals['value'] = value
    self.css({'text-align': 'center', 'padding-top': '-50px', 'padding': '10px', 'margin-bottom': '10px'})
    self.setColor(self.getColor('blueColor', 2))
    if self.htmlCode is not None:
      self.aresObj.htmlCodes[self.htmlCode] = self
      if 'values' in self.vals:
        if type == 'date':
          self.jsFrg('slidechange', self.jsAddUrlParam(self.htmlCode, '[ FormatDate( ui.values[0] ), FormatDate( ui.values[1] )]', isPyData=False))
        else:
          self.jsFrg('slidechange', self.jsAddUrlParam(self.htmlCode, "ui.values", isPyData=False))
      else:
        if type == 'date':
          self.jsFrg('slidechange', self.jsAddUrlParam(self.htmlCode, "FormatDate(ui.value)", isPyData=False))
        else:
          self.jsFrg('slidechange', self.jsAddUrlParam(self.htmlCode, "ui.value", isPyData=False))

    if type == 'date':
      self.change( '''var value = new Date(ui.value); 
        if(ui.handleIndex == 0) { $(ui.handle).html("<div style='margin-top:12px'>" + FormatDate(value) + "</div>" )}
        else { $(ui.handle).html("<div style='margin-top:-17px'>" + FormatDate(value) + "</div>" ) }; ''' )
    else:
      self.change('''
        if(ui.handleIndex == 0) { $(ui.handle).html("<div style='margin-top:12px'>" + ui.value.formatMoney(0, ",", ".") + "</div>" )}
        else { $(ui.handle).html("<div style='margin-top:-17px'>" + ui.value.formatMoney(0, ",", ".") + "</div>" ) }; ''')

    if type == 'date':
      self.addGlobalFnc('DateToTimeStamp(date)', '''
        var splitDt = date.split("-") ; var dateTime = new Date(splitDt[0], parseInt(splitDt[1])-1, splitDt[2]);
        return dateTime.getTime(); ''', 'Javascript function to convert a string date YYYY-MM-DD to a Javascript timestamp')
      self.addGlobalFnc('FormatDate(timeStamp)', '''
        var d = new Date(timeStamp), month = '' + (d.getMonth() + 1), day = '' + d.getDate(), year = d.getFullYear();
        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;
        return [year, month, day].join('-'); ''', 'Javascript function to convert a Js timestamp to a string date YYYY-MM-DD')
    #self.change("var data = {event_val: ui.value, event_code:'%(htmlId)s'}; $('#%(htmlId)s_val').html(data.event_val);" % {'htmlId': self.htmlId } )

  def jsEvents(self):
    if hasattr(self, 'jsFncFrag'):
      for eventKey, fnc in self.jsFncFrag.items():
        if self.htmlCode is not None:
          fnc.insert(0, self.jsAddUrlParam(self.htmlCode, self.val, isPyData=False))
          self.aresObj.jsOnLoadEvtsFnc.add('''
              %(jqId)s.on('%(eventKey)s', function(event, ui) {
                var useAsync = false; var data = %(data)s ;
                if (!$('#body_loading').length){ 
                  var bodyLoading2 = $('<div id="body_loading" name="ares_loading" style="bottom:20px;left:0;position:fixed;background-color:%(lightGreyColor)s;padding:5px"><i class="fas fa-spinner fa-spin" style="margin-left:10px;margin-right:10px"></i><div style="display:inline" id="loading_count">0</div> process running...</div>') ; 
                } ; $('body').append(bodyLoading2) ; $('#loading_count').html( parseInt($('#loading_count').html()) + 1) ;
                %(jsFnc)s ;
                if (!useAsync) {
                $('#loading_count').html( parseInt($('#loading_count').html()) - 1) ;
                if ($('#loading_count').html() == '0') { $('#body_loading').remove() ;} }
              }) ;
            ''' % {'jqId': self.eventId, 'eventKey': eventKey, 'data': self.jsQueryData, 'lightGreyColor': self.getColor("greyColor", 2),
                   'jsFnc': ";".join([f for f in fnc if f is not None]) })

  # data.slide: function( event, ui ) {  $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] ); }
  def onDocumentLoadFnc(self): self.addGlobalFnc("%s(htmlObj, data, jsStyle)" % self.__class__.__name__, '''
    if ( jsStyle.type == 'date') {
      data.step = data.step * 86400000 ;
      data.min = DateToTimeStamp(data.min);
      data.max = DateToTimeStamp(data.max);
      if (data.values != undefined) { data.values = [DateToTimeStamp(data.values[0]), DateToTimeStamp(data.values[1]) ]; }
      else { data.value = DateToTimeStamp(data.value)}};
    htmlObj.slider(data);
    $('#' + htmlObj.attr('id') + ' .ui-slider-range').css("background-color", jsStyle.backgroundColor);
    $('#' + htmlObj.attr('id') + ' .ui-state-default, .ui-widget-content .ui-state-default' ).css( "background-color", jsStyle.backgroundDotColor );
    ''', 'Javascript Object builder')

  def addAttr(self, key, val):
    """
    :category: Javascript features
    :rubric: JS
    :example: >>> myObj.change( aresObj.addAttr('value', 20) )
    :returns: Javascript string with the function to define some slider properties
    :dsc:
      This function will change or add some javascript attributes attached to the slider object
    :link Jquery documentation: https://jqueryui.com/slider/
    """
    self.vals[key] = val

  def setColor(self, color, colorDot=None):
    """
    :category: Color Change
    :rubric: CSS
    :type: Style
    :dsc:
      Set the color of the Slider object
    :return: The Python object
    """
    if colorDot is None:
      colorDot = color
    self._jsStyles['backgroundColor'] = color
    self._jsStyles['backgroundDotColor'] = colorDot
    return self

  def __str__(self):
    """ Return the HTML object of for div """
    return '''
      <div %(strAttr)s>
        <p style="width:100%%;text-align:left;height:25px;margin-bottom:10px;font-size:14px;font-weight:bold;font-variant:small-caps;">%(title)s</p>
        <div style="width:100%%;height:20px">
          <span style="float:left;display:inline-block">%(min)s</span>
          <span style="float:right;display:inline-block">%(max)s</span>
        </div>
        <div id="%(htmlId)s"></div>
      </div>''' % {"strAttr": self.strAttr(withId=False), "min": self.vals['min'], 'title': self.title,
                   "htmlId": self.htmlId, "max": self.vals['max']}

  def change(self, jsFnc):
    """
    :category: Javascript event
    :rubric: JS
    :example: myObj.change( aresObj.jsAlert() )
    :returns: Javascript string with the function to trigger other functions with the slider value is changed
    :dsc:
      Python wrapper to a javascript function to trigger events on slider changes
    :link Jquery documentation: https://api.jqueryui.com/slider/
    """
    self.jsFrg('slidechange', jsFnc)

  def jsUpdate(self, jsData, isPyData=True):
    """
    :category: Javascript function
    :rubric: JS
    :example: myObj.jsUpdate( 20 )
    :example: myObj.jsUpdate( "2018-07-21" )
    :example: myObj.jsUpdate( ["2018-07-21", "2018-07-22"] ) # if the type is a date
    :return: Javascript string with the function to change the value of the component
    :dsc:
      Python wrapper to a javascript function to change the value of a Jquery slider object
    :link Jquery documentation: https://jqueryui.com/slider/
    """
    if isPyData:
      if 'values' in self.vals and not isinstance(jsData, list):
        self.aresObj.log("Problem in Slider jsUpdate expect a list")
        raise Exception("Problem in Slider jsUpdate expect a list")

      jsData = json.dumps(jsData)
    if 'values' in self.vals:
      if self.type == 'date':
        return "%(jqId)s.slider('values', 0, DateToTimeStamp(%(jsData)s[0])); %(jqId)s.slider('values', 1, DateToTimeStamp(%(jsData)s[1]));" % {'jqId': self.jqId, 'jsData': jsData}
      else:
        return "%(jqId)s.slider('values', 0, %(jsData)s[0]); %(jqId)s.slider('values', 1, %(jsData)s[1]);" % {'jqId': self.jqId, 'jsData': jsData}

    if self.type == 'date':
      return "%s.slider('value', DateToTimeStamp(%s)); " % (self.jqId, jsData)
    else:
      return "%s.slider('value', %s); " % (self.jqId, jsData)

  @property
  def val(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: myObj.val
    :returns: Javascript string with the function to get the current value of the component
    :dsc:
      Property to get the jquery value of the HTML object in a python HTML object.
      This method can be used in any jsFunction to get the value of a component in the browser.
      This method will only be used on the javascript side, so please do not consider it in your algorithm in Python
    """
    if 'values' in self.vals:
      if self.type == 'date':
        return '[ FormatDate( %(jqId)s.slider("values")[0] ), FormatDate( %(jqId)s.slider("values")[1] )]' % {'jqId': self.jqId }

      return '%(jqId)s.slider("values")' % { 'jqId': self.jqId}

    if self.type == 'date':
      return 'FormatDate( %(jqId)s.slider("value") ) ' % {'jqId': self.jqId}

    return '%(jqId)s.slider("value")' % {'jqId': self.jqId }

  @property
  def jsQueryData(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsQueryData
    :dsc:
      Python function to define the Javascript object to be passed in case of Ajax call internally or via external REST service with other languages
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    if 'values' in self.vals:
      if self.type == 'date':
        return "{ event_val: [FormatDate(ui.values[0]), FormatDate(ui.values[1])], event_code: '%(htmlId)s', event_min: %(min)s, event_max: %(max)s, event_range: '%(range)s' }" % {"htmlId":  self.htmlId, 'min': self.vals['min'], 'max': self.vals['max'], 'range': self.vals.get('range') }
      else:
        return "{ event_val: ui.values, event_code: '%(htmlId)s', event_min: %(min)s, event_max: %(max)s, event_range: '%(range)s' }" % {"htmlId":  self.htmlId, 'min': self.vals['min'], 'max': self.vals['max'], 'range': self.vals.get('range') }

    if self.type == 'date':
      return "{ event_val: FormatDate(ui.value), event_code: '%(htmlId)s', event_min: %(min)s, event_max: %(max)s, event_range: '%(range)s' }" % {"htmlId":  self.htmlId, 'min': self.vals['min'], 'max': self.vals['max'], 'range': self.vals.get('range') }

    return "{ event_val: ui.value, event_code: '%(htmlId)s', event_min: %(min)s, event_max: %(max)s, event_range: '%(range)s' }" % {"htmlId":  self.htmlId, 'min': self.vals['min'], 'max': self.vals['max'], 'range': self.vals.get('range') }

  def to_word(self, document):
    label = self.title if self.title != "" else 'Input'
    p = document.add_paragraph("%s: %s [%s, %s]" % (label, self.aresObj.http.get(self.htmlCode, ''), self.vals['min'], self.vals['max']))

  def to_xls(self, workbook, worksheet, cursor):
    """
    :link xlxWritter Documentation: https://xlsxwriter.readthedocs.io/format.html
    """
    cellTitle = self.title if self.title != "" else 'Input'
    cell_format = workbook.add_format({'bold': True})
    worksheet.write(cursor['row'], 0, cellTitle, cell_format)
    cursor['row'] += 1
    worksheet.write(cursor['row'], 0, self.aresObj.http.get(self.htmlCode, ''))
    worksheet.write(cursor['row'], 1, "[%s, %s]" % (self.vals['min'], self.vals['max']))
    cursor['row'] += 2


class SkillBar(AresHtml.Html):
  """ Python interface for the HTML Skill bars, simple bars chart done in pure Javascript and CSS
  :category:
  :type:
  :example
      aresObj.skillbars([{'value': 30, 'label': 'youpi', 'color': 'red'}, {'value': 50, 'label': 'youpi2', 'url': 'google'}])
  """
  references = {'Skill Bar W3C': 'https://www.w3schools.com/howto/howto_css_skill_bar.asp'}
  name, category, callFnc, docCategory = 'Skill Bars', 'Chart', 'skillbars', 'Standard'
  __pyStyle = ['CssTableBasic', 'CssText']

  @property
  def eventId(self): return "#%s tr td p" % self.htmlId

  @property
  def jsQueryData(self):
    """
    :category: Javascript features
    :dsc: Python function to define the Javascript object to be passed in case of Ajax call internally or via external REST service with other languages
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    return "{ event_val: $(this).text(), event_code: '%s' }" % (self.htmlId)

  def __init__(self, aresObj, data, title, width, widthUnit, height, heightUnit, color, htmlCode, globalFilter):
    if data.dataFncs == []:
      data.dataFncs.append('AggSeries')
    super(SkillBar, self).__init__(aresObj, data, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, htmlCode=htmlCode, globalFilter=globalFilter)
    color, self.title = self.getColor('baseColor', 2) if color is None else color, title
    #self.data = self.vals.data
    #self.vals.attach(self)
    self._jsStyles = {'color': self.getColor('blueColor', 12), 'fontColor': self.getColor('greyColor', 0)}
    if self.htmlCode is not None:
      self.jsFrg('click', ''' 
        $('#%(htmlCode)s').find('p').css('color', '%(font)s') ; 
        if ( '%(htmlCode)s' != 'None') { 
          if ( %(breadCrumVar)s['params']['%(htmlCode)s'] === data['event_val'] ) { %(breadCrumVar)s['params']['%(htmlCode)s'] = '' ;}
          else { %(breadCrumVar)s['params']['%(htmlCode)s'] = data['event_val']; $(this).css('color', '%(selectedColor)s') ;} 
        } ''' % {"htmlCode": self.htmlCode, 'selectedColor': self.getColor('blueColor', 6), 'font': self.getColor('greyColor', 14),
                 "breadCrumVar": self.aresObj.jsGlobal.breadCrumVar})

  def jsEvents(self):
    if hasattr(self, 'jsFncFrag'):
      for eventKey, fnc in self.jsFncFrag.items():
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

  def onDocumentLoadVar(self):
    self.addGlobalVar(self.jsVal, self.vals.jsData)

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' htmlObj.empty() ;
      data.data[0].data.forEach(function(rec, i){
          var valPerc = rec / data.stats['sum'] * 100;
          if (rec.dsc != undefined) {var tooltip = 'title="' + rec.dsc + '"' ;} else { var tooltip = ''; } ;
          if (rec.url != undefined) {var content ='<a href="'+ rec.url +'" style="color:white">' + valPerc.toFixed( 2 ) + '%</a>' ;} else { var content = valPerc.toFixed( 2 ) + "%"; }
          htmlObj.append('<tr ' + tooltip + '><td style="width:100px;"><p style="word-wrap:break-word;cursor:pointer">'+ data.labels[i] +'</p></td><td style="width:100%"><div style="margin:2px;display:block;height:100%;padding-bottom:5px;padding-top:5px;width:' + parseInt( valPerc ) + '%;background-color:'+ jsStyles.color +';color:'+ jsStyles.fontColor +'">' + content + '</div></td></tr>');
          htmlObj.find('tr').tooltip() ; }) ; ''', 'Javascript Object builder')

  def __str__(self):
    """ String representation of the HTML element """
    return '''
      <div class="%s" style="margin:5px 0">
        <p style="height:25px;margin-bottom:10px;font-size:14px;font-weight:bold;font-variant:small-caps;">%s</p>
        <table %s></table>
      </div>
    ''' % (self.getPyCss('CssDivWithBorder'), self.title, self.strAttr(pyClassNames=self.pyStyle))

  @classmethod
  def matchMarkDownBlock(cls, data): return True if data[0].strip() == "---SkillBar" else None

  @staticmethod
  def matchEndBlock(data): return data.endswith("---")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj):
    """
    :category:
    :rubric:
    :example:
      ---SkillBar
      label|value|color
      Test 1|35|yellow
      Test 2|25|blue
      ---
    :dsc:

    """
    recordSet = []
    header = data[1].strip().split("|")
    for val in data[2:-1]:
      label, value, color = val.strip().split("|")
      recordSet.append( {'value': value, 'label': label, 'color': color} )
    if aresObj is not None:
      getattr(aresObj, 'skillbars')(recordSet)
    return ["aresObj.skillbars(%s)" % json.dumps(recordSet)]

  @classmethod
  def jsMarkDown(self, vals):
    recordSet = ["---SkillBar", 'label|value|color']
    for rec in vals:
      recordSet.append("%(label)s|%(value)s|%(color)s" % rec)
    recordSet.append("---")
    return "&&".join(recordSet)

  def to_img(self):
    """

    :return:
    """
    ares_matplotlib = requires("matplotlib.pyplot", reason='Missing Package', install='matplotlib', autoImport=True, sourceScript=__file__)
    ares_numpy = requires("numpy", reason='Missing Package', install='numpy', autoImport=True, sourceScript=__file__)

    ares_matplotlib.rcdefaults()
    fig, ax = ares_matplotlib.subplots()

    # Example data
    aggDf = self.vals.data.groupby([self.vals.xAxis])[self.vals.seriesNames[0]].sum().reset_index()
    labels = aggDf[self.vals.xAxis]
    values = aggDf[self.vals.seriesNames[0]]

    y_pos = ares_numpy.arange(len(labels))
    performance = values
    error = ares_numpy.random.rand(len(labels))
    ax.barh(y_pos, performance, xerr=error, align='center', color=self.getColor('blueColor', 12), ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(self.vals.xAxis)
    ax.set_title(self.title)
    return fig

  def to_word(self, document):
    """

    :param document:
    :return:
    """
    ares_matplotlib = requires("matplotlib.pyplot", reason='Missing Package', install='matplotlib', autoImport=True, sourceScript=__file__)
    import os

    fig = self.to_img()
    imgsPath = os.path.join(self.aresObj.run.local_path, "imgs")
    if not os.path.exists(imgsPath):
      os.mkdir(imgsPath)

    # Add the picture to the document
    ares_matplotlib.savefig( os.path.join(imgsPath, "%s.png" % id(fig)) )
    document.add_picture( os.path.join(imgsPath, "%s.png" % id(fig)) )
    os.remove( os.path.join(imgsPath, "%s.png" % id(fig)) )

  def filter(self, aresDf=None, colName=None, caseSensitive=False, multiVals=False, exactMath=False, allSelected=True, filterGrp=None):
    if aresDf is None:
      aresDf = self.vals.data
    if colName is None:
      colName = self.vals.xAxis
    strFilter = ["( aresObj('%s') == rec['%s'] )" % (self.htmlCode, colName)]
    if allSelected:
      strFilter.append("( aresObj('%s') == '')" % self.htmlCode)
    aresDf.link("click", self.htmlCode, " || ".join(strFilter), filterGrp if filterGrp is not None else "filter_%s" % aresDf.htmlCode, colNames=[colName])
    return self


class ContextMenu(AresHtml.Html):
  """
  :category: HTML Component
  :rubric: PY
  :type: HTML
  :dsc:
    Set a bespoke Context Menu on an Item. This will create a popup on the page with action.
    This component is generic is need to be added to a component to work
  """
  references = {'Documentation': ''}
  name, category, callFnc, docCategory = 'Context Menu', 'Event', 'menu', 'Standard'
  source = None # The container

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit, visible):
    super(ContextMenu, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.css({'display': 'block' if visible else 'none', 'position': 'absolute',
              'padding': 0, 'margin': 0, 'background-color': self.getColor('greyColor', 0),
              'box-shadow': '1px 1px 5px #555', 'border-radius': '2px'})
    for rec in recordSet:
      if "icon" in rec:
        self.aresObj.jsImports.add("font-awesome")
        self.aresObj.cssImport.add("font-awesome")
    self.addGlobalVar("CONTEXT_MENU_VAL", "{}")
    self._jsStyles = {'liStyles': self.addPyCss("CssTextItem", toMainStyle=False)}

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, '''
      var jsList = htmlObj.find('ul'); jsList.empty();
      data.forEach(function(rec){ 
        if(rec.icon != undefined) {var li = $('<li>').addClass(jsStyles.liStyles).html("<i class='"+ rec.icon +"' style='margin-right:5px'></i>" + rec.text)}
        else {var li = $('<li>').addClass(jsStyles.liStyles).html(rec.text)};
        li.click(function(event){var data = CONTEXT_MENU_VAL; eval(rec.jsFnc)}); jsList.append(li)})
      ''', 'Javascript Object builder')

  def __str__(self):
    self.aresObj._scroll.add("$('nav[name=context_menus]').hide()")
    # TODO: Add a condition in the init to display the context menu only for some columns or rows when table for example
    self.aresObj.jsOnLoadFnc.add('''
      $('html').click(function(){$('nav[name=context_menus]').hide()});
      %s.on('contextmenu', function(event) {CONTEXT_MENU_VAL = %s;
        event.stopPropagation(); %s.css({left: event.pageX + 1, top: event.pageY + 1, display: 'block'}); event.preventDefault()
      })''' % (self.source.jqDiv, self.source.contextVal, self.jqId))
    return '''
      <nav %(attr)s name='context_menus'>
        <ul style='list-style:none;padding:0px;margin:0'></ul>
      </nav>''' % {'attr': self.strAttr(pyClassNames=self.pyStyle)}

