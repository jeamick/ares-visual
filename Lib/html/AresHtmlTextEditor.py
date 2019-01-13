#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import json

from ares.Lib.html import AresHtml


class Editor(AresHtml.Html):
  name, category, callFnc, docCategory = 'Code Editor', 'Text', 'editor', 'Preformatted'
  __pyStyle = ['CssDivEditor']
  __reqCss, __reqJs = ['codemirror'], ['codemirror']

  def __init__(self, aresObj, vals, size, language, width, widthUnit, height, heightUnit, isEditable, htmlCode):
    super(Editor, self).__init__(aresObj, vals, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, code=htmlCode)
    self.size, self.isEditable = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size, isEditable
    self._jsStyles, self._jsActions, self._definedActions = {'language': language}, {}, ['run', 'load', 'auto', 'clone', 'save', 'delete']
    self.css( {'font-size': self.size } )
    self.addGlobalVar('%s_editor' % self.htmlId)

  @property
  def val(self):
    """ Property to get the jquery value of the HTML object in a python HTML object """
    return '%(htmlId)s_editor.getValue()' % {"htmlId": self.htmlId}

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
    return "{ event_val: %(htmlId)s_editor.getValue(), event_code: '%(htmlId)s' }" % {"htmlId": self.htmlId}

  @property
  def jsClear(self):
    return "%(htmlId)s_editor.setValue('')" % {"htmlId": self.htmlId}

  def trigger(self, event):
    if event in ['load', 'run']:
      self._triggerEvents.add("$('#%(htmlId)s_%(action)s').trigger('click')" % {"htmlId": self.htmlId, "action": event})
    else:
      return super(Editor, self).trigger(event)

  def onDocumentReady(self):
    self.jsUpdateDataFnc = '''
      %(pyCls)s(%(jqId)s, %(htmlId)s_data, %(jsStyles)s) ; 
      if(%(htmlCode)s != null) { %(breadCrumVar)s['params'][%(htmlCode)s] = %(jsVal)s };
      ''' % {'pyCls': self.__class__.__name__, 'jqId': self.jqId, 'htmlId': self.htmlId, 'htmlCode': json.dumps(self.htmlCode),
             'jsVal': self.val, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'jsStyles': json.dumps(self._jsStyles)}
    if self.dataSrc is None or self.dataSrc.get('type') != 'url':
      self.aresObj.jsOnLoadFnc.add(self.jsUpdateDataFnc)

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' 
      if (window[htmlObj.attr('id') + '_editor'] == undefined) {
        window[htmlObj.attr('id') + '_editor'] = CodeMirror.fromTextArea( htmlObj.get(0), {lineNumbers: true, mode: jsStyles.language} ) ; } 
      window[htmlObj.attr('id') + '_editor'].setValue(data); 
      if ($('#'+ htmlObj.attr('id') +'_save').length != 0) {
        window[htmlObj.attr('id') + '_editor'].on('keydown', function(i, e) { 
            if (e.ctrlKey && e.keyCode == 83) { 
              e.preventDefault(); 
              $('#'+ htmlObj.attr('id') +'_save').trigger('click'); } 
        }) ;
      } ;
      $('#'+ htmlObj.attr('id') +'_updated').text('Last update: ' + Today() ) ;
      window[htmlObj.attr('id') + '_editor'].getWrapperElement().style["overflow"] = "hidden"; 
      window[htmlObj.attr('id') + '_editor'].getWrapperElement().style["height"] = "100%"; ''')

  def jsAction(self, jsFncs, icon, pyCssCls, tooltip, action):
    """
    :category: Python function
    :rubric: PY
    :example: >>>
    :dsc:
      Define the event on the editor when the save is clicked.
      This will call a Ajax service.
    :return: The object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    if action not in self._definedActions:
      self._definedActions.append(action)
    self._jsActions[action] = "<span id='%(htmlId)s_%(action)s' title='%(tooltip)s' class='%(cssStyle)s %(icon)s'></span>" % {
      "icon": icon, "cssStyle": self.addPyCss(pyCssCls), "htmlId": self.htmlId, 'tooltip': tooltip, 'action': action}
    self.aresObj.jsOnLoadFnc.add("$('#%(htmlId)s_%(action)s').on('click', function(event) { %(jsFncs)s; })" % {"htmlId": self.htmlId, "jsFncs": ";".join(jsFncs), 'action': action})
    return self

  # --------------------------------------------------------------------------------------------------------------
  #                                   EDITOR STANDARD EVENTS
  #
  # None of those functions are based on an Ajax call as I do not thing they are supposed to do something special in case of
  # success or failure of an internal event. Problems are tackled in the standard way using the ares popup message (and the status for the color)
  def save(self, jsFncs, icon='fas fa-save', pyCssCls="CssSmallIcon", tooltip='click to save changes'):
    """
    :example: >>> editor.save( aresObj.jsPost( "/reports/create/script", [editor]) )
    :wrap jsAction:
    :return:
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    jsFncs = ["var data = %(data)s;" % {"data": self.jsQueryData}] + jsFncs
    return self.jsAction(jsFncs, icon, pyCssCls, tooltip, 'save')

  def delete(self, jsFncs, icon='fas fa-times-circle', pyCssCls="CssSmallIconRed", tooltip='click to delete the function'):
    return self.jsAction(jsFncs, icon, pyCssCls, tooltip, 'delete')

  def run(self, jsFncs, icon='fas fa-play', pyCssCls="CssSmallIcon", tooltip='Run button on the Editor Component'):
    return self.jsAction(jsFncs, icon, pyCssCls, tooltip, 'run')

  def clone(self, jsFncs, icon='fas fa-copy', pyCssCls="CssSmallIcon", tooltip='Create a copy of the script'):
    return self.jsAction(jsFncs, icon, pyCssCls, tooltip, 'clone')

  def load(self, jsFncs, icon='fas fa-sync', pyCssCls="CssSmallIcon", tooltip='Load button on the Editor Component', interval=5000):
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    jsFncs.append( "$('#%s_updated').text('Last update: ' + Today() )" % self.htmlId)
    self.jsAction(jsFncs, icon, pyCssCls, tooltip, 'load')
    jsFncsAuto = ['''
          $(this).toggleClass('fa-pulse');
          if ( window['%(htmlId)s_interval'] == undefined) { window['%(htmlId)s_interval']  = setInterval(  function() { $("#%(htmlId)s_load").trigger('click'); }, %(interval)s ); }
          else {
            if( $(this).hasClass('fa-pulse') ) { window['%(htmlId)s_interval']  = setInterval( function() { $("#%(htmlId)s_load").trigger('click'); }, %(interval)s ); }
            else { clearInterval( window['%(htmlId)s_interval'] ) ;}} ; ''' % {'interval': interval, "htmlId": self.htmlId}]
    return self.jsAction(jsFncsAuto, "fas fa-clock", pyCssCls, "Auto Update button on the Editor Component", 'auto')

  def download(self, jsFncs='', icon='fas fa-file-download', pyCssCls="CssSmallIcon", tooltip='Download temporary version of the script'):
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs]
    jsFncs.append("event.stopPropagation(); %s; return false;" % self.aresObj.jsDownload( fileName="tempScript.py", jsData="window['%s_editor'].getValue()" % self.htmlId))
    return self.jsAction(jsFncs, icon, pyCssCls, tooltip, 'clone')

  def __str__(self):
    events = []
    for action in self._definedActions:
      if action in self._jsActions:
        events.append( self._jsActions[action] )
    return '''
      <div style="display:inline-block;width:100%%;padding:5px 5px 5px 25px">
        %(events)s 
        <span id='%(htmlId)s_updated' style='float:right;font-style:italic;margin-right:10px;display:inline-block:width:100%%'></span>
      </div>
      <textarea %(attr)s>%(vals)s</textarea>
    ''' % {'attr': self.strAttr(pyClassNames=self.__pyStyle), "vals": self.vals, 'htmlId': self.htmlId, 'events': "".join(events)}


class Console(AresHtml.Html):
  """

  """
  name, category, callFnc, docCategory = 'Python Cell Runner', 'Text', 'pytestcell', 'Preformatted'
  __reqCss, __reqJs = ['codemirror'], ['codemirror']

  def __init__(self, aresObj, vals, size, width, widthUnit, height, heightUnit, isEditable, htmlCode):
    super(Console, self).__init__(aresObj, vals, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, code=htmlCode)
    self.size, self.isEditable = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size, isEditable
    self._jsRun, self._jsSave = '', ''
    self.addGlobalVar("%s_count" % self.htmlId, "0")
    self.css({'font-size': self.size, 'padding': '10px', "min-height": "30px", "font-family": "Arial, monospace"})

  @property
  def val(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.val
    :dsc:
      Return the value of the In[] section of the editor.
    :return: A String with the javascript function to get the value
    """
    return '%(htmlId)s_editor.getValue()' % {"htmlId": self.htmlId}

  @property
  def jsQueryData(self):
    """
    :category: Javascript features
    :rubric: JS
    :dsc:
      String with the javascript feature to get the data to send when a event is triggered from this object.
      Basically when the run or saved is triggered
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    return "{ event_out: $('#%(htmlId)s_result_data').text(), event_val: %(htmlId)s_editor.getValue(), event_code: '%(htmlId)s' }" % {'htmlId': self.htmlId}

  # --------------------------------------------------------------------------------------------------------------
  #                                   EDITOR STANDARD EVENTS
  #
  # Those are already embedding an ajax call as b default the return of those call will change the display
  # Make sure you are not calling a Ajax call within an AJax call, event engine should remain simple
  # Remember PEP20: Simple is better than complex.
  def run(self, url=None, jsData=None, jsFncs=None, httpCodes=None, tooltip="Run the line"):
    """
    :category: Javascript Event
    :rubric: JS
    :example: >>> myObj.run( "/reports/fncs/run/%s" % report_name )
    :dsc:
        Add an event action to the console object.
    :return: The python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs] if jsFncs is not None else []
    jsFncs = [
      "if (!data.status){ $('#%(htmlId)s_result_data').css('color', '%(redColor)s') ; } else { $('#%(htmlId)s_result_data').css('color', '%(blackColor)s') }" % {"htmlId": self.htmlId, 'redColor': self.getColor('redColor', 4), 'blackColor': self.getColor('greyColor', 8) },
      "%(htmlId)s_count ++; $('#%(htmlId)s_counter').text( 'In [ '+ %(htmlId)s_count +']'   )" % {"htmlId": self.htmlId},
      "$('#%(htmlId)s_result_data').text(data.output); $('#%(htmlId)s_print_data').text(data.print);" % {"htmlId": self.htmlId}] + jsFncs + ["$('#%(htmlId)s_result').show();$('#%(htmlId)s_print').show();" % {"htmlId": self.htmlId} ]
    self._jsRun = (self.aresObj.jsPost(url=url, jsData=jsData, jsFnc=jsFncs, httpCodes=httpCodes) if url is not None else ";".join(jsFncs), tooltip)
    return self

  def save(self, url=None, jsData=None, jsFncs=None, httpCodes=None, tooltip="Save the run"):
    """
    :category: Javascript Event
    :rubric: JS
    :example: >>> myObj.run( "/reports/fncs/test/%s" % report_name )
    :dsc:
        Add an event action to the console object to save the result of the In and out.
    :return: The python object itself
    """
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs] if jsFncs is not None else []
    self._jsSave = (self.aresObj.jsPost(url=url, jsData=jsData, jsFnc=jsFncs, httpCodes=httpCodes) if url is not None else ";".join(jsFncs), tooltip)
    return self

  def __str__(self):
    runButton, saveButton = '', ''
    if self._jsRun != '':
      self.aresObj.jsOnLoadFnc.add('''
        var %(htmlId)s_editor = CodeMirror.fromTextArea( $('#%(htmlId)s').get(0), {placeholder: "aresObj.myFncs()", lineNumbers: true, mode: 'python'} ) ;
        %(htmlId)s_editor.setSize(null, 30); %(htmlId)s_editor.getWrapperElement().style["line-height"] = "1.5"; %(htmlId)s_editor.refresh() ;
        %(htmlId)s_editor.on('keydown', function(i, e) { 
            if (e.keyCode  == 13) { var data = %(data)s ; e.preventDefault(); %(run)s ;} 
            else {
              $('#%(htmlId)s_result_data').text(''); $('#%(htmlId)s_print_data').text('');
              $('#%(htmlId)s_result').hide(); $('#%(htmlId)s_print').hide();}
        }) ;
        $('#%(htmlId)s_run').on('click', function(event) {  var data = %(data)s ; %(run)s ; })''' % {"htmlId": self.htmlId, "run": self._jsRun[0], 'data': self.jsQueryData})
      runButton = '<i title="%(tooltip)s" id="%(htmlId)s_run" class="%(iconCss)s fas fa-caret-right"></i>' % {'tooltip': self._jsRun[1], "htmlId": self.htmlId, "iconCss": self.addPyCss('CssStdIcon')}
    if self._jsSave != '':
      self.aresObj.jsOnLoadFnc.add('''
        $('#%(htmlId)s_save').on('click', function(event) {  var data = %(data)s ; %(save)s ; })''' % {
        "htmlId": self.htmlId, "save": self._jsSave[0], 'data': self.jsQueryData})
      saveButton = '<i title="%(tooltip)s" id="%(htmlId)s_run" class="%(iconCss)s far fa-save"></i>' % {'tooltip': self._jsSave[1], "htmlId": self.htmlId, "iconCss": self.addPyCss('CssOutIcon')}
    return '''
      <table style="width:100%%;margin-top:10px;padding:5px 0 5px 10px">
        <tr>
          <td style="height:100%%;width:100px;border-left:5px solid %(blueColor)s;vertical-align:middle;color:%(blueColor)s"> 
            <span title="count number of runs" id="%(htmlId)s_counter" >In [ 0 ]</span> 
            %(runButton)s
          </td>
          <td class="%(tdRunCss)s"><textarea %(attr)s></textarea></td>
        </tr>
        <tr style="height:3px;display:inline-block"></tr>
        <tr style="display:none" id="%(htmlId)s_result">
          <td style="padding-top:10px;padding-bottom:10px;height:100%%;width:100px;border-left:5px solid blue;vertical-align:middle;color:red"> 
            <span title="Number of store results">Out [ 0 ]</span>  
            %(saveButton)s
          </td>
          <td class="%(tdRunCss)s" id="%(htmlId)s_result_data"></td>
        </tr>
        <tr style="display:none;" id="%(htmlId)s_print">
          <td colspan=2 style="height:100px;">
            <div style="width:100%%;height:100%%;background-color:%(blackColor)s;color:%(whiteColor)s;text-align:left;padding:5px;margin-top:10px" id="%(htmlId)s_print_data" >
              Server logs generated from the print command
            </div>
          </td>
        </tr>
      </table>
      ''' % {'attr': self.strAttr(), 'htmlId': self.htmlId, 'runButton': runButton, 'tdRunCss': self.addPyCss('CssTdEditor'), 'saveButton': saveButton,
             'blackColor': self.getColor('greyColor', 8), 'whiteColor': self.getColor('greyColor', 0),
             'redColor': self.getColor('redColor', 2), 'blueColor': self.getColor('blueColor', 8)}


class Tags(AresHtml.Html):
  name, category, callFnc, docCategory = 'Tags', 'Text', 'tags', 'Preformatted'
  __pyStyle = ['CssDivNoBorder']
  """
  check unicity
  remove all items
  
  """

  def __init__(self, aresObj, vals, title, icon, width, widthUnit, height, heightUnit, htmlCode):
    super(Tags, self).__init__(aresObj, vals, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, code=htmlCode)
    self.title, self.icon = title, icon
    self.css( {"margin-top": "5px"})

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
    return "%(breadCrumVar)s['params']['%(htmlId)s']" % {"htmlId": self.htmlId, "breadCrumVar": self.aresObj.jsGlobal.breadCrumVar}

  @property
  def json(self):
    return "JSON.stringify(%(breadCrumVar)s['params']['%(htmlId)s'])" % {"htmlId": self.htmlId, "breadCrumVar": self.aresObj.jsGlobal.breadCrumVar}

  def jsEmpty(self):
    return "%(breadCrumVar)s['params']['%(htmlId)s'] = []; $('#%(htmlId)s_tags').text('')" % {"htmlId": self.htmlId, "breadCrumVar": self.aresObj.jsGlobal.breadCrumVar}

  def jsAdd(self, jsData='data', jsDataKey=None, isPyData=False):
    if isPyData:
      jsData = json.dumps(jsData)
    else:
      if jsDataKey is not None:
        jsData = "%s['%s']" % (jsData, jsDataKey)
    self.addGlobalFnc('RemoveSelection(srcObj, htmlId)', ''' 
       const index = %(breadCrumVar)s['params'][htmlId].indexOf(srcObj.parent().text());
       %(breadCrumVar)s['params'][htmlId].splice(index, 1);
       srcObj.parent().remove(); ''' % {'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar},
       fncDsc="Remove the item from the Tags Html component but also from the underlying javascript variable")
    return '''
      if (%(breadCrumVar)s['params']['%(htmlId)s'] == undefined) {%(breadCrumVar)s['params']['%(htmlId)s'] = [] ;}
      if (! %(breadCrumVar)s['params']['%(htmlId)s'].includes( %(jsData)s ) ) { %(breadCrumVar)s['params']['%(htmlId)s'].push(%(jsData)s);
      $('#%(htmlId)s_tags').append("<span style='margin:2px;background:%(baseColor)s;color:%(whiteColor)s;border-radius:8px;1em;vertical-align:middle;display:inline-block;padding:0 2px 1px 10px;cursor:pointer'>"+ %(jsData)s +"<i onclick='RemoveSelection($(this), \\\"%(htmlId)s\\\")' style='margin-left:10px' class='far fa-times-circle'></i></span>");} ;
      ''' % {"htmlId": self.htmlId, "jsData": jsData, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'whiteColor': self.getColor('greyColor', 0), "baseColor": self.getColor("baseColor", 0)}

  def __str__(self):
    return '''
      <div %(attr)s>
        <div style='margin:0;display:inline-block;vertical-align:middle;width:90px;float:left;padding:2px 5px 0 5px;height:30px;border:1px solid %(greyColor)s'>
          <i class="%(icon)s" style="margin-right:10px"></i>%(title)s</div>
        <div id='%(htmlId)s_tags' style='padding:2px 5px 0 5px;border:1px solid %(greyColor)s;height:30px'></div>
      </div>''' % {"attr": self.strAttr(pyClassNames=self.pyStyle), "title": self.title, 'icon': self.icon, 'htmlId': self.htmlId, 'greyColor': self.getColor("greyColor", 2) }