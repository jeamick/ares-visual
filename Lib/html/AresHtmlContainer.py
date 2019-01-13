#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json

from ares.Lib.html import AresHtml
from ares.Lib.html import AresHtmlSelect
from ares.Lib import AresImports


# External package required
render_template_string = AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='render_template_string', raiseExcept=False, sourceScript=__file__)


class Panel(AresHtml.Html):
  """ Python wrapper for several items with toggle event

  Add Html Component by using + to this object and you will be able to switch between them.
  """
  __pyStyle = ['CssDivNoBorder']
  name, category, callFnc, docCategory = 'Multi Panel', 'Container', 'panel', 'Standard'
  mocks = []

  def __init__(self, aresObj, htmlObjs, width, widthUnit, height, heightUnit):
    if htmlObjs is None:
      htmlObjs = self.mocks
    super(Panel, self).__init__(aresObj, [], width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.__htmlOrder, self.__htmlRef, self.htmlMaps = [], {}, {}
    for htmlObj in htmlObjs:
      self.__add__(htmlObj)
    self.css( {"padding": "5px"} )

  def __add__(self, htmlObj):
    """ Add an Html Object to this object"""
    htmlObj.inReport = False
    self.__htmlRef[htmlObj.htmlId] = htmlObj
    self.__htmlOrder.append(htmlObj.htmlId)
    self._addToContainerMap(htmlObj)

  @property
  def jqId(self):
    """ Refer to the internal select item """
    return "$('#%s_select')" % self.htmlId

  def onDocumentLoadVar(self):
    """ Return the variable to store in the global section of the javacript part """
    self.jsVal = "%s_data" % self.htmlId
    self.addGlobalVar(self.jsVal, json.dumps(self.__htmlOrder))

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
     data.forEach(function(item){
        htmlObj.append('<option value="' + item + '">' + item + '</option>') ; }) ; ''', 'Javascript Object builder')

  def __str__(self):
    """ Return the onload, the HTML object and the javascript events """
    # No string method for a container, it will add its data in the html directly
    # The below part is the string representation
    items = ['<div %s>' % self.strAttr(pyClassNames=self.pyStyle)]
    items.append('<div class="form-group py_csssdivboxmargin"><select class="form-control" id="%s_select"></select></div>' % (self.htmlId))
    for name in self.__htmlOrder:
      obj = self.__htmlRef[name].html()
      items.append('<div style="display:none" id="%s" >%s</div>' % (name, obj))
    items.append('</div>')

    # The function to change the display according to the item name selected
    self.aresObj.jsOnLoadFnc.add('''
        $('#%(htmlId)s_select').on('change', function (event){ 
          DisplayItem( $('#%(htmlId)s_select option:checked').val(), %(htmlItems)s ) }); 
      ''' % {'htmlId': self.htmlId, 'htmlItems': json.dumps(self.__htmlOrder)})

    # The global function to hide and show components based on a list
    # This is global as some other components might want to use it and there is no need to rewrite it every time
    self.addGlobalFnc('DisplayItem(htmlIdToDisplay, idListToHidde)', '''
        idListToHidde.forEach(function(htmlId) { $('#' + htmlId).hide() ; }); $('#' + htmlIdToDisplay).show() ; ''',
                      'The global function to hide and show components based on a list. This is global as some other components might want to use it and there is no need to rewrite it every time')
    return "".join(items)


class PanelSplit(AresHtml.Html):
  """ Python wrapper for a resizable panel
  """
  references = {'Example': 'https://codepen.io/rstrahl/pen/eJZQej'}
  name, category, callFnc, docCategory = 'Panel Split', 'Container', 'panelsplit', 'Advanced'
  mocks = []

  def __init__(self, aresObj, width, widthUnit, height, heightUnit, leftObj, rightObj):
    super(PanelSplit, self).__init__(aresObj, None, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.htmlMaps = {}
    if leftObj is not None:
      self.left(leftObj)
    if rightObj is not None:
      self.right(rightObj)

  def left(self, htmlObj):
    """ Add the left component to the panel """
    htmlObj.inReport = False
    self.htmlLeft = htmlObj
    self._addToContainerMap(htmlObj)

  def right(self, htmlObj):
    """ Add the right component to the panel """
    htmlObj.inReport = False
    self.htmlRight = htmlObj
    self._addToContainerMap(htmlObj)

  def html(self):
    """ Return the onload, the HTML object and the javascript events """
    # Update the HTML element with the values defined in the function call in the report
    if hasattr(self, 'jsUpdateFnc'):
      self.__addUpdtMethod(self.pyToJsData(self.vals))

    # No string method for a container, it will add its data in the html directly
    # The below part is the string representation
    self.css( {'display': 'flex', 'flex-direction': 'row', 'border': '1px solid silver', 'overflow': 'hidden', 'xtouch-action': 'none' })

    items = ['<div %s>' % self.strAttr(pyClassNames=self.pyStyle)]
    items.append('<div style="flex:0 0 auto;padding:10px;width:300px;width:60%%;white-space:nowrap;" id="%s_left" class="panel-left">%s</div>' % (self.htmlId, self.htmlLeft.html()))
    items.append('<div style="flex:0 0 auto;width:5px;min-height:200px;cursor:col-resize;background:#F8F8F8;" class="splitter">&nbsp;</div>')
    items.append('<div style="flex:1 1 auto;padding:10px;width:100%%;min-width:200px;" id="%s_right" class="panel-right">%s</div>' % (self.htmlId, self.htmlRight.html()))
    items.append('</div>')
    self.aresObj.jsOnLoadFnc.add('''
       $("#%(htmlId)s_left").resizable({ handleSelector: ".splitter", resizeHeight: false });
       $("#%(htmlId)s_right").resizable({ handleSelector: ".splitter-horizontal", resizeWidth: false });
      ''' % {'htmlId': self.htmlId})

    return "".join(items)


class PanelDisplay(AresHtml.Html):
  __pyStyle = ['CssDivNoBorder']
  name, category, callFnc, docCategory = 'Display Panel', 'Container', 'paneldisplay', 'Standard'
  mocks = []

  def __init__(self, aresObj, htmlObjs, title, width, widthUnit, height, heightUnit, showPanel):
    if htmlObjs is None:
      htmlObjs = self.mocks
    super(PanelDisplay, self).__init__(aresObj, [], width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.__htmlOrder, self.__htmlRef, self.htmlMaps, self.title, self.showPanel = [], {}, {}, title, showPanel
    for htmlObj in htmlObjs:
      self.__add__(htmlObj)
    self.css( {"padding": "5px"} )
    self.addGlobalVar("panel_show_%s" % self.htmlId, len(self.vals))

  def __add__(self, htmlObj):
    """ Add an Html Object to this object"""
    htmlObj.inReport = False
    self.__htmlRef[htmlObj.htmlId] = htmlObj
    self.__htmlOrder.append(htmlObj.htmlId)
    self._addToContainerMap(htmlObj)

  def __str__(self):
    items = ['<div %s>' % self.strAttr(pyClassNames=self.pyStyle)]
    visible, arrow = ("show", 'down') if self.showPanel else ('none', 'up')
    items.append('<div class="form-group" onselectstart="return false" style="color:%s;font-weight:bold;font-size:16px;border-bottom:1px solid black">%s<i onclick="PanelDisplay(this, \'%s\')" style="cursor:pointer;none;none;float:right" class="fas fa-chevron-circle-%s"></i></div>' % (self.getColor('baseColor', 0), self.title, self.htmlId, arrow))
    items.append("<div id='%s_toggle' style='display:%s'>" % (self.htmlId, visible))
    self.addGlobalFnc("PanelDisplay(srcObj, htmlId)", '''
      $('#'+ htmlId + '_toggle').toggle() ; 
      if ( $('#'+ htmlId + '_toggle').css('display') == 'block') { $(srcObj).attr('class', 'fa fa-chevron-circle-down fa-w-16') ; }
      else { $(srcObj).attr('class', 'fa fa-chevron-circle-up fa-w-16') ; }
      ''', 'Javascript function to monitor the display of the sliding panel.')
    for name in self.__htmlOrder:
      obj = self.__htmlRef[name].html()
      items.append('<div id="%s" >%s</div>' % (name, obj))
    items.append("</div>")
    items.append('</div>')
    return "".join(items)


class Div(AresHtml.Html):
  """ Python Wrapper for a simple DIV tag
  """
  references = {'Div W3C': 'https://www.w3schools.com/tags/tag_div.asp'}
  # the below methods should not be overriden
  __pyStyle = ['CssDivNoBorder']
  __reqCss, __reqJs = ['bootstrap'], ['jquery']
  name, category, callFnc, docCategory = 'Simple Container', 'Container', 'div', 'Standard'
  mocks = ''

  def __init__(self, aresObj, htmlObj, color, size, width, widthUnit, icon, height, heightUnit, editable, align, padding, htmlCode):
    if isinstance(htmlObj, list) and htmlObj:
      for obj in htmlObj:
        if hasattr(obj, 'inReport'):
          obj.inReport = False
    elif htmlObj is not None and hasattr(htmlObj, 'inReport'):
      htmlObj.inReport = False # Has to be defined here otherwise it is set to late
    super(Div, self).__init__(aresObj, htmlObj, code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    size = self.aresObj.pyStyleDfl['fontSize']if size is None else "%spx" % size
    color = color if color is not None else 'black'
    self.icon, self.htmlMaps = icon, {}
    self.css( {"color": color, "font-size": size, 'text-align': align } )
    if padding is not None:
      self.css('padding', '%s' % padding)
    if editable:
      self.addAttr('contenteditable', "true")
      self.css('overflow', 'auto')

  def __add__(self, htmlObj):
    """ Add items to a container """
    htmlObj.inReport = False # Has to be defined here otherwise it is set to late
    if not isinstance(self.vals, list):
      self.vals = [self.vals]
    self.vals.append(htmlObj)
    self._addToContainerMap(htmlObj)
    return self

  @property
  def jsQueryData(self): return "{ event_val: '', event_code: '%s' }" % self.htmlId

  def jsAdd(self, data='data', isPyData=False):
    if isPyData:
      data = json.dumps(data)
    return '''
      %(jqId)s.append("<div style='margin:0;padding:0;white-space:nowrap;padding:0px 5px 0px 5px;'>" + %(data)s + "<i style='margin-left:10px;cursor:pointer' onclick='$(this).parent().remove()' class='far fa-times-circle'></i></div>") ;
      ''' % {'data': data, 'jqId': self.jqId}

  def load(self, url, htmlId=None):
    if htmlId is None:
      return "%(jqId)s.load('%(url)s');" % {"jqId": self.jqId, 'url': url, "htmlId": htmlId}

    return "%(jqId)s.load('%(url)s #%(htmlId)s');" % {"jqId": self.jqId, 'url': url, "htmlId": htmlId}

  def html(self):
    """ Return the HTML display of a split container"""
    self.loadStyle()
    self.jsEvents()
    icon = ''
    if self.icon is not None:
      icon = '<i style="display:inline-block;margin-right:5px;float:left" class="%s"></i>' % self.icon
    if isinstance(self.vals, list):
      if hasattr(self.vals[-1], 'inReport'):
        innerHtml = '\n'.join([val.html() for val in self.vals if val])
      else:
        innerHtml = '\n'.join([val for val in self.vals])
    else:
      if hasattr(self.vals, 'inReport'):
        innerHtml = self.vals.html()
      elif self.vals is not None:
        if hasattr(self.vals, 'decode'):
          innerHtml = self.vals.decode('utf8')
        else:
          innerHtml = self.vals
      else:
        innerHtml = ''
    return '<div %s>%s%s</div>' % (self.strAttr(pyClassNames=self.pyStyle), icon, innerHtml)

  def to_word(self, document):
    if isinstance(self.vals, list):
      for val in self.vals:
        if hasattr(val, 'inReport'):
          val.to_word(document)
    else:
      if hasattr(self.vals, 'inReport'):
        self.vals.to_word(document)

  @property
  def val(self):
    """ Return the Javascript Value """
    return '$("#%s").html()' % self.htmlId

  @property
  def text(self):
    """ Return the Javascript Value """
    return '$("#%s").text()' % self.htmlId

  @property
  def innerText(self):
    """ Allows to return text with formatted return carriage which jquery doesn't allow yet"""
    return '''document.getElementById('%s').innerText''' % self.htmlId

  def jsContentChildUpdate(self, data=''):
    """
    Allows to dynamically update the child of the div
    TODO: Change the handling of the htmlObj to be stored in a dict with htmlCode
    :return:
    """

    return '%s.html(%s)' % (self.vals.jqId, data)


  def getChild(self, indexObj=0):
    return self.vals[indexObj].jqId


  def jsUpdate(self, data=''):
    """ """
    return '$("#%s").html(%s)' % (self.htmlId, data)


class DivFixed(Div):

  name, category, callFnc, docCategory = 'Warning', 'Text', 'fixeddiv', 'Preformatted'
  mocks = ' This is a warning'

  def __init__(self, aresObj, text, top, left, right, color, size, width, widthUnit, icon, height, heightUnit, editable, align, backgroundColor, zindex, padding, htmlCode):
    super(DivFixed, self).__init__(aresObj, [], color, size, width, widthUnit, icon, height, heightUnit, editable, align, padding, htmlCode)
    self.css( {'position': 'fixed', 'top': "%spx" % top, ' white-space': 'nowrap'} )
    if zindex is not None:
      self.css('z-index', zindex)
    if text is None:
      text = self.mocks
    if isinstance(text, list):
      for subTxt in text:
        self + self.aresObj.text(subTxt, size=size)
    else:
      self + self.aresObj.text(text, size=size)
    if left is not None:
      self.css('left', "%spx" % left)
    elif right is not None:
      self.css('right', "%spx" % right)
    if backgroundColor is not None:
      self.css('background-color', backgroundColor)


class DragDiv(Div):

  name, category, callFnc, docCategory = 'Mark', 'Text', 'dragdiv', 'Preformatted'
  mocks = ' This is a mark'

  def __init__(self, aresObj, text, top, left, right, color, size, width, widthUnit, icon, height, heightUnit, editable, align, backgroundColor, padding, htmlCode):
    super(DragDiv, self).__init__(aresObj, [], color, size, width, widthUnit, icon, height, heightUnit, editable, align, padding, htmlCode)
    self.css( {'position': 'absolute', 'top': "%spx" % top, 'border-radius': '10px'} )
    self.size = 10 if size is None else size
    if text is None:
      text = self.mocks
    self + self.aresObj.text(text, size=self.size)
    if left is not None:
      self.css('left', "%spx" % left)
    elif right is not None:
      self.css('right', "%spx" % right)
    if backgroundColor is not None:
      self.css('background-color', backgroundColor)

  def jsFocus(self):
    return '$("#%s_content").focus()' % self.htmlId

  def html(self):
    """ Return the HTML display of a split container"""
    self.loadStyle()
    self.jsEvents()
    icon = ''
    self.aresObj.jsOnLoadFnc.add("%s.draggable()" % self.jqId)
    self.aresObj.jsOnLoadFnc.add("%s.bind('dragstop', function(){  } )" % self.jqId)

    if self.icon is not None:
      icon = '<i class="%s"></i>&nbsp;' % self.icon
    val = self.vals.html() if hasattr(self.vals, 'inReport') else self.vals

    edit = self.aresObj.edit()
    edit.click([self.jsFocus()])

    save = self.aresObj.lock()
    save.click(["%s.draggable( 'disable' );" % self.jqId], ["%s.draggable( 'enable' );" % self.jqId])
    delete = self.aresObj.delete()
    delete.click([self.jsRemove()])

    return '''
      <div %(attr)s>%(icon)s
        <div id="%(htmlId)s_content" autocorrect="off" spellcheck="false" contenteditable=true style="float:left;margin-left:5px;margin-right:10px;">%(content)s</div>
        %(options)s  
      </div>
      ''' % {'attr': self.strAttr(pyClassNames=self.pyStyle), 'icon': icon,
             'content': self.vals.html(), 'htmlId': self.htmlId, 'options': "".join([str(delete), str(save),str(edit)])}


class Popup(AresHtml.Html):
  """ Python Wrapper for a simple DIV tag

  :example
  popup = aresObj.popup(aresObj.title('Youpi'), color="red")
  popup + aresObj.paragraph('Test')
  """
  references = {'Popup W3C': 'https://www.w3schools.com/tags/tag_div.asp'}
  # the below methods should not be overriden
  __reqCss, __reqJs = ['bootstrap'], ['jquery']
  name, category, callFnc, docCategory = 'Popup Container', 'Container', 'popup', 'Advanced'
  dashboards = ['DashBoardPopup']

  def __init__(self, aresObj, htmlObj, title, color, size, width, widthUnit, height, heightUnit, withBackground, draggable):
    super(Popup, self).__init__(aresObj, [], width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.inputs, self.height = [], "%s%s" % (height, heightUnit)
    if htmlObj is not None:
      if isinstance(htmlObj, list):
        for obj in htmlObj:
          self.__add__(obj)
      else:
        self.__add__(htmlObj)
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) if size is None else size
    color = color if color is not None else 'black'
    self.title, self.withBackground, self.draggable = title, withBackground, draggable
    self.css( {"color": color, "font-size": "%spx" % size} )
    if self.withBackground:
      self.css({'width': '100%', 'position': 'fixed', 'height': '100%', 'background-color': 'rgba(0,0,0,0.4)', 'left': 0, 'top': 0,  'margin': 'auto'})
      self.css({'display': 'none', 'z-index': '10000', 'text-align': 'center', 'padding-top': '50px', 'padding-left': '10%', 'padding-right': '10%'})
      if draggable:
        self.aresObj.jsOnLoadFnc.add("$('#%s table').draggable();" % self.htmlId)
    else:
      self.css({'width': '90%','position': 'absolute', 'border': '1px solid black', 'margin': 0, 'padding': 0, 'display': 'none', 'z-index': '10000'})
      if draggable:
        self.aresObj.jsOnLoadFnc.add("%s.draggable();" % self.jqId)

  def __add__(self, htmlObj):
    """ Add items to a container """
    htmlObj.inReport = False # Has to be defined here otherwise it is set too late
    #htmlObj.css( {"height": "100%"} )
    if htmlObj.category in ['Input']:
      self.inputs.append( (htmlObj.jqId, htmlObj.placeholder, htmlObj.val, htmlObj.__class__.__name__) )
    self.vals.append(htmlObj)
    return self

  def jsSetInputVals(self, jsData):
    jsFncs = []
    for input in self.inputs:
      jsFncs.append("%s(%s, %s['%s'])" % (input[3], input[0], jsData, input[1]))
    return jsFncs

  def jsInputData(self, typeRow='dict'):
    if typeRow == 'dict':
      vals = []
      for input in self.inputs:
        if input[1] is not None:
          vals.append( "'%s': %s" % (input[1], input[2]) )
      return " [ {%s} ]" % ",".join(vals)

    return " [ %s ]" % ",".join([input[2] for input in self.inputs])

  def submit(self, jsFncs, label='Submit'):
    button = self.aresObj.button(label)
    self.__add__( button )
    button.jsFrg('click', "%s;%s" % (";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs, self.jsHide() ) )

  def show(self):
    fncs = []
    for htmlObj in self.vals:
      if getattr(htmlObj, 'dataSrc') is not None and htmlObj.dataSrc['type'] == 'script':
        fncs.append(htmlObj.jsLoadFromSrc(htmlObj.dataSrc.get('jsDataKey')))
      elif getattr(htmlObj, 'dataSrc') is not None and htmlObj.dataSrc['type'] == 'url':
        fncs.append( self.aresObj.jsPost(htmlObj.dataSrc['url']))
    fncs.append("$('#%s').show()" % self.htmlId)
    return ";".join(fncs)

  def hide(self): return "$('#%s').hide()" % self.htmlId

  def html(self):
    """ Return the HTML display of a split container"""
    self.loadStyle()
    self.jsEvents()
    logo = render_template_string('<img src="{{ url_for(\'static\',filename=\'images/logo/ares_logo_nav_bar.png\') }}" />')
    onmouseOver = 'style="margin:0;padding:0;border-collapse:collapse;background-color:%s;border:1px solid %s;cursor:pointer"' % (self.getColor('blueColor', 12), self.getColor('blueColor', 12)) if self.draggable else 'style="margin:0;padding:0;border-collapse:collapse;background-color:#213B68;border:1px solid #213B68"'
    content = '''
          <table style="border-spacing:0;border-collapse:collapse;margin:0;padding:0;width:100%%;background-color:white;box-shadow:0 0 1px 1px #213B68;-webkit-box-shadow:0 0 1px 1px #213B68;-moz-box-shadow:0 0 1px 1px #213B68;border-radius: 5px ">
            <tr %(onmouseOver)s>
              <td style="vertical-align:top;border-collapse:collapse;text-align:left">%(logo)s</td>
              <td style="vertical-align:middle;border-collapse:collapse;text-align:right;color:white;font-size:%(titleSize)spx">%(title)s <i onclick="$('#%(htmlId)s').hide()" style="margin-left:10px;cursor:pointer" class="fas fa-window-close"></i></td>
            </tr>
            <tr><td colspan=2 style="padding:10px;height:%(height)s">%(objects)s</td></tr>
          </table>''' % {'logo': logo, 'onmouseOver': onmouseOver, 'titleSize': self.size, 'title': self.title, 'htmlId': self.htmlId,
                         'objects': "\n".join([val.html() for val in self.vals]), 'height': self.height}
    self.aresObj.jsOnLoadFnc.add(''' $('#%(htmlId)s').on('click', function (e) { if (e.target == this) {$('#%(htmlId)s').hide() ;} }) ''' % {"htmlId": self.htmlId})
    return '''<div %s>%s</div>''' % (self.strAttr(pyClassNames=self.pyStyle), content)

  @property
  def val(self):
    """aresDoc
    :example: myObj.val
    :dsc:
    Property to get the jquery value of the HTML object in a python HTML object.
    This method can be used in any jsFunction to get the value of a component in the browser.
    This method will only be used on the javascript side, so please do not consider it in your algorithm in Python
    """
    return '$("#%s").html()' % self.htmlId

  def jsUpdate(self, data=''): return '$("#%s").html(%s)' % (self.htmlId, data)

  def to_word(self, document):
    pass


class Row(AresHtml.Html):
  """ Python wrapper for a row of HTML items """
  references, __cssCls = {}, []
  name, category, callFnc, docCategory = 'Row', 'Container', 'row', 'Standard'
  mocks = [] # No point to display an empty container

  def __init__(self, aresObj, htmlObjs, width, widthUnit, height, heightUnit, aresData, align, valign, colsWith, closable, resizable, titles):
    if aresData is not None:
      # Load the different HTML components from a static list
      # This mode will automatically add the inReport to the new components
      htmlObjs = []
      for component in aresData:
        aresFnc = getattr(aresObj, component['htmlComponent'])
        parameters = dict(component)
        del parameters['htmlComponent']

        htmlObjs.append(aresFnc(**parameters))
    self.colsWith = [] if colsWith is None else colsWith
    self.htmlMaps = {}
    super(Row, self).__init__(aresObj, [], width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    if htmlObjs is None:
      htmlObjs = self.mocks
    for htmlObj in htmlObjs:
      self.__add__(htmlObj)
    self.align, self.valign, self.closable, self.resizable, self.titles = align, valign, closable, resizable, titles
    self.css({"padding": "5px 0 5px 0", "border-collapse": "collapse", 'table-layout': 'fixed' })

  def __add__(self, htmlObj):
    """ Add items to a container """
    htmlObj.inReport = False # Has to be defined here otherwise it is set to late
    self.vals.append(htmlObj)
    self._addToContainerMap(htmlObj)
    return self

  def get(self, htmlCode):
    """ Return the Html component in the parameter bar """
    return self.__components[htmlCode]

  def html(self):
    """ Return the HTML display of a split container"""
    self.loadStyle()
    self.jsEvents()
    items = ['<div style="width:100%%;display:block;"><table %s><tr>' % self.strAttr(pyClassNames=self.pyStyle)]
    widths = {}
    if self.colsWith:
      for i, _ in enumerate(self.vals):
        widths[i] = 'width:%s' % self.colsWith[i]

    if self.closable:
      if self.titles:
        for i, htmlObj in enumerate(self.vals):
          onclickEvent = "ResizableRow(this, 'col_%s_%s')" % (self.htmlId, i)  # if self.colsWith else "$(\'#col_%s_%s\').children().toggle()" % ( self.htmlId, i)
          items.append('<th style="text-align:left;padding:5px 0 5px 0;%s"><i onclick="%s" style="cursor:pointer;" class="far fa-minus-square"></i>&nbsp;<p style="font-size:16px;color:%s;display:inline">%s</p></th>' % (widths.get(i, ''), onclickEvent, self.getColor('textColor', 0), self.titles[i].upper()))
      else:
        for i, htmlObj in enumerate(self.vals):
          onclickEvent = "ResizableRow(this, 'col_%s_%s'))" % (self.htmlId, i)  # if self.colsWith else "$(\'#col_%s_%s\').children().toggle()" % ( self.htmlId, i)
          items.append( '<th style="text-align:left;%s"><i onclick="%s" style="cursor:pointer;" class="far fa-minus-square"></i></th>' % (
            widths.get(i, ''), onclickEvent))
      items.append('</tr><tr>')  # $(htmlId).parent().width()
      self.addGlobalFnc("ResizableRow(htmlId, targetId)", '''
         if ( $(htmlId).parent().data('size') == undefined) { $(htmlId).parent().data('size', $(this).parent().width() ) } ; 
         $('#' + targetId).children().toggle(); var styleDisplay = $('#' + targetId).children().css('display') ;
         if ( styleDisplay == 'block') { $(htmlId).parent().width($(htmlId).parent().data('size')) ; }
         else { $(htmlId).parent().width(10) ; } ''')

    for i, htmlObj in enumerate(self.vals):
      extraStyle = 'padding:0 0 0 5px' if i != 0 else 'padding:0'
      items.append( '<td id="col_%s_%s" style="font-size:inherit;line-height:inherit;vertical-align:%s;text-align:%s;%s;%s">%s</td>' % (self.htmlId, i, self.valign, self.align, widths.get(i, ''), extraStyle, htmlObj.html()))
    items.append('</tr></table></div>')
    if self.resizable:
      self.aresObj.jsImports.add('datatables-col-resizable')
      self.aresObj.jsOnLoadFnc.add("%s.colResizable({ liveDrag:true });" % self.jqId)
    return "".join(items)


class Col(AresHtml.Html):
  """ Python wrapper for a column of HTML elements from Bootstrap

  This component is a container and it is used to display multiple Ares components in column.
  You can first add a component in the data list then add the + operator to add more.

  Also please have a look at the CSS features to customize your component
  """
  references = {'Col Bootstrap': 'https://getbootstrap.com/docs/4.0/layout/grid/',
                'FlexBox': 'https://www.alsacreations.com/tuto/lire/1493-css3-flexbox-layout-module.html'}
  name, category, callFnc, docCategory = 'Column', 'Container', 'col', 'Standard'
  mocks = []

  def __init__(self, aresObj, htmlObjs, position, width, widthUnit, height, heightUnit, align):
    self.position, self.htmlMaps = position, {}
    super(Col, self).__init__(aresObj, [], width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    if htmlObjs is not None:
      for htmlObj in htmlObjs:
        self.__add__(htmlObj)
    if align == "center":
      self.css({'margin': 'auto', 'display': 'block'})
    else:
      self.css({'display': 'inline-block'})

  def __add__(self, htmlObj):
    """ Add items to a container """
    htmlObj.inReport = False # Has to be defined here otherwise it is set to late
    self.vals.append(htmlObj)
    self._addToContainerMap(htmlObj)
    return self

  def content(self):
    self.loadStyle()
    return "".join([htmlObj.html() for htmlObj in self.vals])

  def html(self):
    """ Return the HTML display of a split container"""
    self.loadStyle()
    self.jsEvents()
    divStyle = ''
    if self.position == 'bottom':
      self.position = 'center'
      divStyle = ' style="margin:auto"'
    elif self.position == 'middle':
      divStyle = ' style="margin:auto"'
    self.css( {"justify-content": self.position})
    return '<div %s><div%s>%s</div></div>' % (self.strAttr(), divStyle, "".join([htmlObj.html() for htmlObj in self.vals]))

  def to_word(self, document):
    for i, htmlObj in enumerate(self.vals):
      htmlObj.to_word(document)

  def to_xls(self, workbook, worksheet, cursor):
    for i, htmlObj in enumerate(self.vals):
      try:
        htmlObj.to_xls(workbook, worksheet, cursor)
      except Exception as err:
        cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
        worksheet.write(cursor['row'], 0, str(err), cell_format)
        cursor['row'] += 2


class Grid(AresHtml.Html):
  references, __cssCls = {}, ['container-fluid']
  name, category, callFnc, docCategory = 'Grid', 'Container', 'grid', 'Standard'
  mocks = [] # No point to display an empty container

  def __init__(self, aresObj, htmlObjs, width, widthUnit, height, heightUnit, colsDim, colsAlign, noGlutters, align):
    super(Grid, self).__init__(aresObj, [], width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.css( {'overflow-x': 'hidden'} )
    self.rowsStyle, self.colsStyle, self.noGlutters = {}, {}, noGlutters
    if align == 'center':
      self.css({'margin': 'auto'})
    self.colsDim, self.htmlMaps, self.colsAlign  = [], {}, []
    if colsDim is None:
      colsDim = len(htmlObjs) * [1]
    for i, htmlObj in enumerate(htmlObjs):
      self.__add__( (htmlObj, colsDim[i] ) )
    if colsAlign is not None:
      self.colsAlign = colsAlign

  def __add__(self, htmlObjWithDim):
    """ Add items to a container """
    if isinstance(htmlObjWithDim, tuple):
      htmlObj, dim = htmlObjWithDim
    else:
      htmlObj, dim = htmlObjWithDim, 1
    self._addToContainerMap(htmlObj)
    htmlObj.inReport = False # Has to be defined here otherwise it is set to late
    self.vals.append(htmlObj)
    self.colsDim.append(dim)
    self.colsAlign.append("left")
    return self

  def get(self, id):
    """ Return the Html component in the parameter bar """
    return self.vals[id]

  def html(self):
    self.loadStyle()
    self.jsEvents()
    items = ['<div %s>' % self.strAttr(pyClassNames=self.pyStyle)]
    items.append('<div class="row%s">' % (' no-gutters' if self.noGlutters else ''))
    dimRow, rowIndex = 0, 1
    for i, htmlObj in enumerate(self.vals):
      if dimRow == 12:
        items.append('</div><div class="row%s">' % (' no-gutters' if self.noGlutters else ''))
        dimRow = 0

      if isinstance(htmlObj, AresHtmlSelect.Select):
        htmlObj.container = "#%s" % self.htmlId # The container should be defined in this case to be visible
      htmlContent = htmlObj.content() if isinstance(htmlObj, Col) else htmlObj.html()
      items.append('<div class="col-md-%s text-%s">%s</div>' % (self.colsDim[i], self.colsAlign[i], htmlContent) )
      dimRow += 1 if self.colsDim[i] == 'auto' else self.colsDim[i]
      rowIndex += 1
      if dimRow > 12:
        raise Exception("BootStrap allow a max of 12 columns per Row")

    items.append('</div></div>')
    return "".join(items)

  def to_word(self, document):
    for i, htmlObj in enumerate(self.vals):
      try:
        htmlObj.to_word(document)
      except Exception as err:
        from docx.shared import RGBColor

        errotTitle = document.add_heading().add_run("Error")
        errotTitle.font.color.rgb = RGBColor(255, 0, 0)
        errotTitle.font.italic = True
        errorParagraph = document.add_paragraph().add_run((str(err)))
        errorParagraph.font.color.rgb = RGBColor(255, 0, 0)
        errorParagraph.font.italic = True

  def to_xls(self, workbook, worksheet, cursor):
    for i, htmlObj in enumerate(self.vals):
      try:
        htmlObj.to_xls(workbook, worksheet, cursor)
      except Exception as err:
        cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
        worksheet.write(cursor['row'], 0, str(err), cell_format)
        cursor['row'] += 2

  @staticmethod
  def matchMarkDown(val): return True if val == "[" else None

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj=None):
    print(val)

  @classmethod
  def jsMarkDown(self, vals):
    return '''
      '''


class Tabs(AresHtml.Html):
  """ Python wrapper for a multi Tabs component
  """
  cssCls = ['nav', 'nav-tabs']
  name, category, callFnc, docCategory = 'Tabs', 'Container', 'tabs', 'Advanced'
  __reqCss = ['bootstrap']
  references = {'Tabs Bootstrap': 'https://getbootstrap.com/docs/4.0/components/navs/'}
  __pyStyle = ['CssDivNoBorder']
  htmlObj = None
  mocks = [{'value': 'Main'}, {'value': 'Sensi 1', 'isActive': True}, {'value': 'Sensi 2'},]
  dashboards = ['DashBoardTabs']

  def __init__(self, aresObj, htmlObjs, width, widthUnit, height, heightUnit, tabNames, rowsCss, colsCss, closable,
               selectedTab, htmlCode, alwaysReload, encoding):
    super(Tabs, self).__init__(aresObj, [], htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.rowsStyle, self.colsStyle, self.selectedTab = {}, {}, selectedTab
    self.tabNames, self.htmlMaps = [], {}
    if tabNames is None:
      tabNames = len(htmlObjs) * [1]
    for i, htmlObj in enumerate(htmlObjs):
      tanValue = htmlObj.get('name', tabNames[i])
      if hasattr(tanValue, 'decode'):
        tanValue = tanValue.decode(encoding)
      if isinstance(htmlObj, dict):
        self.__add__((self.aresObj.paragraph(htmlObj['value']), tanValue))
        if htmlObj.get('isActive', False):
          self.selectedTab = tanValue
      else:
        self.__add__((htmlObj, tabNames[i]))
    self.css({'cursor': 'pointer', 'overflow-y': 'hidden', 'overflow-x': 'hidden', 'margin-top': '5px'})
    self.addGlobalVar("tabs_counts_%s" % self.htmlId, len(self.vals))
    for evts in ['click', 'change']:
      # Add the source to the different events
      self.jsFrg(evts, ''' 
        $('#%(htmlId)s li div').css( {'background-color': '%(whiteColor)s', 'color': '%(darkColor)s'} );
        $(this).find('div').css( {'background-color': '%(lightGreyColor)s', 'color': '%(whiteColor)s' } ) ;
        $('div[name="panel_%(htmlId)s"]').hide() ; var tabIndex = $(this).data('index') ; var data = %(jsQueryData)s;
        if ( '%(htmlCode)s' != 'None') { %(breadCrumVar)s['params']['%(htmlCode)s'] = data.event_val } ; 
        ''' % {'jsQueryData': self.jsQueryData, 'htmlId': self.htmlId, 'htmlCode': self.htmlCode,
               'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'darkColor': self.getColor('greyColor', 10),
               'lightGreyColor': self.getColor('blueColor', 2), 'whiteColor': self.getColor("greyColor", 0)})
    if self.htmlCode is not None:
      if self.htmlCode in self.aresObj.http:
        self.selectedTab = self.aresObj.http[self.htmlCode]
      if self.selectedTab is not None:
        self.aresObj.jsOnLoadFnc.add("%(breadCrumVar)s['params']['%(htmlCode)s'] = '%(selectedTab)s'" % {'selectedTab': self.selectedTab, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar,
                                                                                                         'htmlCode': self.htmlCode} )
    # Check the tab reloading
    self.alwaysReload = alwaysReload
    self.addGlobalVar("reload_%s" % self.htmlId)

  def jsRefreshTab(self, jsTabName=None, isPyData=True):
    if jsTabName is not None:
      if isPyData:
        jsTabName = json.dumps(jsTabName)
      return 'delete %(htmlId)s_TAB_LOAD[%(jsTabName)s]' % {'htmlId': self.htmlId, 'jsTabName': jsTabName}

    return '%(htmlId)s_TAB_LOAD = {}' % {'htmlId': self.htmlId}

  def jsEvents(self):
    if hasattr(self, 'jsFncFrag'):
      for eventKey, fnc in self.jsFncFrag.items():
        if self.htmlCode is not None:
          fnc.insert(0, self.jsAddUrlParam(self.htmlCode, self.val, isPyData=False))
        jsFnc = self.jsLoading(fnc)
        self.aresObj.jsOnLoadEvtsFnc.add("$('#%(htmlId)s').delegate('li.tab_comp', '%(eventKey)s', function(event) { %(jsFnc)s }) ;" % {'htmlId': self.htmlId, 'eventKey': eventKey, 'jsFnc': jsFnc})

  def jsShowPanel(self, panelIndex='tabIndex', jsData='data'):
    return " $('#%(htmlId)s_panel_' + %(panelIndex)s ).show() ; " % {'panelIndex': panelIndex, 'htmlId': self.htmlId}

  def jsUpdatePanel(self, panelIndex='tabIndex', jsData='data', unLockOthers=False):
    return '''
          if (typeof %(panelIndex)s === 'undefined') {
              var dummy = $('<div/>'); $(dummy).css('color', "%(whiteColor)s");
              $('#%(htmlId)s').children('li').each(function () {
                  if ($(this).find("div").css("background-color") != dummy.css("color")) { 
                      %(panelIndex)s = $(this).data('index') ; }}) } ;
                      
          for (var key in %(jsData)s) {
            if( %(htmlId)s_MAP_COMPONENTS[key] != undefined) {
              var htmlObj;
              if ( %(htmlId)s_MAP_COMPONENTS[key][1].startsWith('$') ) { htmlObj = eval(%(htmlId)s_MAP_COMPONENTS[key][1]) ; }
              else { htmlObj = window[%(htmlId)s_MAP_COMPONENTS[key][1]] ; }
              window[%(htmlId)s_MAP_COMPONENTS[key][0]]( htmlObj, data[key] ) ; } }
          
          if ( %(unLockOthers)s ) { %(htmlId)s_TAB_LOAD = {} ; }
          $('#%(htmlId)s_panel_' + %(panelIndex)s ).show() ; %(panelIndex)s = undefined ;    
      ''' % {'panelIndex': panelIndex, 'htmlId': self.htmlId, 'jsData': jsData, 'whiteColor': self.getColor('greyColor', 0),
             'unLockOthers': json.dumps(unLockOthers)}

  @property
  def jqId(self): return "$('#%s li.tab_comp')" % self.htmlId

  @property
  def jsQueryData(self): return "{ event_val: $(this).find('div').text(), event_code: '%s'}" % self.htmlId

  def jsAddTab(self, tabName):
    return '''
      tabs_counts_%(htmlId)s ++;
      $('#%(htmlId)s').append('<li class="nav-item tab_comp" data-index=tabs_counts_%(htmlId)s><div class="nav-link" style="font-size:%(fontSize)s;font-variant:small-caps;font-weight:bold">%(tabName)s</div></li>') ;
      ''' % {'tabName': tabName, 'htmlId': self.htmlId, 'fontSize': self.aresObj.pyStyleDfl['headerFontSize']}

  def jsDelTab(self, tabName):
    return '''
      var pos = -1;
      $('#%(htmlId)s li').each(function( index ) {
         if( $( this ).text() == '%(tabName)s') { pos = index ;} });
      if (pos != -1) { $('#%(htmlId)s li')[pos].remove(); }
      '''  % {'tabName': tabName, 'htmlId': self.htmlId, 'tabName': tabName}

  def __add__(self, htmlObjWithDim):
    """ Add items to a container """
    if isinstance(htmlObjWithDim, tuple):
      htmlObj, name = htmlObjWithDim
    else:
      htmlObj, name = htmlObjWithDim, 1
    self._addToContainerMap(htmlObj)
    if hasattr(htmlObj, 'inReport'):
      htmlObj.inReport = False # Has to be defined here otherwise it is set to late
    self.vals.append(htmlObj)
    self.tabNames.append(name)
    return self

  def jsLoading(self, jsFnc):
    return " var loading = $('#%(htmlId)s_panel_loading'); loading.show() ; %(jsFnc)s " % {'jsFnc': ";".join(jsFnc), 'htmlId': self.htmlId}

  def click(self, jsFnc, tabName=None):
    if tabName is not None:
      self.jsFrg('click', '''
        if ( data['event_val'] == %(tabName)s ) { 
          if( (%(htmlId)s_TAB_LOAD[data['event_val']] == undefined) ||  %(alwaysReload)s ) { 
            %(htmlId)s_TAB_LOAD[data['event_val']] = 1; 
            %(jsFnc)s; $('#%(htmlId)s_panel_' + tabIndex).show(); loading.hide(); }  else { $('#%(htmlId)s_panel_' + tabIndex).show(); loading.hide(); } 
        }; ''' % {'alwaysReload': json.dumps(self.alwaysReload), "tabName": json.dumps(tabName), 'jsFnc': jsFnc, 'htmlId': self.htmlId})
    else:
      self.jsFrg('click', ''' 
       if( ( %(htmlId)s_TAB_LOAD[data['event_val']] == undefined) ||  %(alwaysReload)s ) {
          %(htmlId)s_TAB_LOAD[data['event_val']] = 1; %(jsFnc)s; $('#%(htmlId)s_panel_' + tabIndex).show(); loading.hide()} 
       else { $('#%(htmlId)s_panel_' + tabIndex).show(); loading.hide(); } 
       ''' % {'alwaysReload': json.dumps(self.alwaysReload), 'htmlId': self.htmlId, 'jsFnc': jsFnc})

  def html(self):
    """ Return the HTML representation of a Tabular object """
    self.loadStyle()
    if len(self.jsFncFrag['click']) == 1:
      self.click(' ') # Because otherwise the display will not work
    self.jsEvents()
    self.addGlobalVar("%s_MAP_COMPONENTS" % self.htmlId, json.dumps(self.htmlMaps))
    self.addGlobalVar("%s_TAB_LOAD" % self.htmlId, json.dumps( { } ))
    items, tabs = ['<ul %s>' % self.strAttr(pyClassNames=self.pyStyle)], []
    for i, htmlObj in enumerate(self.vals):
      if self.tabNames[i] == self.selectedTab:
        items.append(''' 
            <li id="tab_%(htmlId)s_selected" class="nav-item tab_comp" data-index=%(i)s>
              <div class="nav-link" style="background-color:%(lightGreyColor)s;color:%(whiteColor)s;font-size:%(fontSize)s;font-variant:small-caps;font-weight:bold;margin:0;padding:2px 15px">%(tabNames)s</div>
            </li>''' % {'htmlId': self.htmlId, "i": i, 'tabNames': self.tabNames[i], 'fontSize': self.aresObj.pyStyleDfl['headerFontSize'],
                        'whiteColor': self.getColor('greyColor', 0), 'lightGreyColor': self.getColor('blueColor', 0)})
        self.aresObj.jsOnLoadEvtsFnc.add("$('#tab_%s_selected').trigger('click')" % self.htmlId)
      else:
        items.append('<li class="nav-item tab_comp" style="padding:0" data-index=%s><div class="nav-link" style="margin:0;font-size:%s;font-variant:small-caps;font-weight:bold;padding:2px 15px">%s</div></li>' % (i, self.aresObj.pyStyleDfl['headerFontSize'], self.tabNames[i]))
      tabs.append(htmlObj)
    items.append('</ul>')
    self.aresObj.jsOnLoadFnc.add("$('#%(htmlId)s').delegate('span', 'click', function(event) {event.stopPropagation()})" % {'htmlId': self.htmlId })
    for i, tab in enumerate(tabs):
      if self.tabNames[i] == self.selectedTab:
        items.append('<div id="%(htmlId)s_panel_%(index)s" name="panel_%(htmlId)s" style="text-align:center;border:1px solid %(lightColor)s;padding:10px">%(obj)s</div>' % {'lightColor': self.getColor('blueColor', 0), 'htmlId': self.htmlId, 'index': i, 'obj': tab.html() if hasattr(tab, 'html') else tab})
      else:
        items.append('<div id="%(htmlId)s_panel_%(index)s" name="panel_%(htmlId)s" style="text-align:center;display:none;border:1px solid %(lightColor)s;padding:10px">%(obj)s</div>' % {'lightColor': self.getColor('blueColor', 0), 'htmlId': self.htmlId, 'index': i, 'obj': tab.html() if hasattr(tab, 'html') else tab})
    items.append('<div id="%(htmlId)s_panel_loading" style="text-align:center;display:none;border:1px solid %(lightColor)s;padding:10px;font-size:18px"><i class="fas fa-spinner fa-spin"></i><br />Loading...</div>' % {'lightColor': self.getColor('blueColor', 0), 'htmlId': self.htmlId})
    return "".join(items)


class Pills(Tabs):
  """ Python wrapper to the Bootstrap Pills interface """
  cssCls = ['nav', 'nav-pills']
  name, category, callFnc, docCategory = 'Pills', 'Container', 'pills', 'Advanced'
  __reqCss = ['bootstrap']
  references = {'Pills Bootstrap': 'https://getbootstrap.com/docs/4.0/components/navs/'}
  __pyStyle = ['CssDivNoBorder']


class IFrame(AresHtml.Html):
  name, category, callFnc, docCategory = 'IFrame', 'Container', 'iframe', 'Advanced'
  __reqCss = ['bootstrap']
  __pyStyle = ['CssDivNoBorder']

  def __init__(self, aresObj, url, width, widthUnit, height, heightUnit):
    super(IFrame, self).__init__(aresObj, url, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.css( {"overflow-x": 'hidden'} )

  def __str__(self):
    return "<iframe src='%s' %s frameborder='0' scrolling='no'></iframe>" % (self.vals, self.strAttr(pyClassNames=self.pyStyle))


class Dialog(AresHtml.Html):
  name, category, callFnc, docCategory = 'DialogMenu', 'Container', 'dialogs', 'Advanced'
  __reqCss, __reqJs = ['jqueryui', 'datatables', 'datatables-export'], ['jquery', 'datatables', 'datatables-export']

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit):
    super(Dialog, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.css( {"border": '2px solid #F4F4F4'} )

  def jsAdd(self, title='data.event_val', isPyData=False):
    if isPyData :
      title = json.loads(title)

    return ''' 
    var dialogWindow = $("<div>");
    var table = $("table");
    dialogWindow.append(table) ;
    dialogWindow.append('<input type="text">') ;
    var d = dialogWindow.dialog( { modal: false, title: %(title)s, show: 'puff', fluid: true,
        close: function () { $(this).remove() } , appendTo: "#%(htmlId)s", resizable: false,
        buttons: [ { text: "Update", click: function() { $( this ).dialog( "close" ); } } ]
    } ) ;
    d.parent().draggable( {containment: '#%(htmlId)s'} ) ; 
    event.preventDefault();
    ''' % {'title': title, 'htmlId': self.htmlId}

  def __str__(self):
    return "<div %s></div>" % self.strAttr()


class IconsMenu(AresHtml.Html):
  name, category, callFnc, docCategory = 'Icons Menu', 'Container', 'menu', 'Advanced'
  __reqCss, __reqJs = ['jqueryui', 'datatables', 'datatables-export'], ['jquery', 'datatables', 'datatables-export']

  def __init__(self, aresObj, width, widthUnit, height, heightUnit, htmlCode):
    super(IconsMenu, self).__init__(aresObj, None, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, code=htmlCode)
    self._jsActions, self._definedActions = {}, []
    self.css( {"margin": "5px 0"})
    self.addGlobalVar("%s_items" % self.htmlId, "{}")

  @property
  def val(self):
    return "%s_items" % self.htmlId

  def jsAction(self, action, icon, tooltip, pyCssCls="CssBigIcon", url=None, jsData=None, jsFncs=None, httpCodes=None):
    if not isinstance(jsFncs, list):
      jsFncs = [jsFncs] if jsFncs is not None else []

    # Add this to an ajax POST call if an URL is defined
    fnc = self.aresObj.jsPost(url=url, jsData=jsData, jsFnc=jsFncs, httpCodes=httpCodes) if url is not None else ";".join(jsFncs)
    self._jsActions[action] = "<span id='%(htmlId)s_%(action)s' title='%(tooltip)s' class='%(cssStyle)s %(icon)s'></span>" % {
      "icon": icon, "cssStyle": self.addPyCss(pyCssCls), "htmlId": self.htmlId, 'tooltip': tooltip, 'action': action}
    self.aresObj.jsOnLoadFnc.add("$('#%(htmlId)s_%(action)s').on('click', function(event) { %(jsFncs)s; %(htmlId)s_items['%(action)s'] = true; })" % {"htmlId": self.htmlId, "jsFncs": fnc, 'action': action})
    if action not in self._definedActions:
      self._definedActions.append(action)
    return self

  def addSelect(self, action, data, width=150):
    options = []
    for d in data:
      options.append("<option>%s</option>" % d)
    self._jsActions[action] = '<select id="inputState" class="form-control" style="width:%spx;display:inline-block;font-size:12px;">%s</select>' % (width, "".join(options))
    self._definedActions.append(action)
    return self

  def __str__(self):
    htmlIcons = []
    for action, htmlDef in self._jsActions.items():
      htmlIcons.append(htmlDef)
    return "<div %s>%s</div>" % (self.strAttr(), "".join(htmlIcons))
