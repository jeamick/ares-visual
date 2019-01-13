#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
    'eng':
'''
:dsc:
Python module to define all the HTML buttons

Definition of all the different HTML button wrappers.
From this module lot of different sort of HTML buttons can be displayed like:
  - ButtonDownload, the button dedicated to download files
  - ButtonRefresh, the button dedicated to query another script in the framework and then to refresh data
  - ButtonOk, to validate something and return a notification
  - GeneratePdf, to generate a Pdf report

Also it is possible to use the generic and basic button object - Button - to then change it to a specific one in your report.
Some based functions are available in order to change more or less everything in the python

[button url="http://www.google.com"]
'''}


import re
import json


from ares.Lib.html import AresHtml


class Button(AresHtml.Html):
  """ Python wrapper for the HTML button """
  references = {'Button W3C': 'https://www.w3schools.com/tags/tag_button.asp',
                'Button Bootstrap': 'http://www.kodingmadesimple.com/2015/04/custom-twitter-bootstrap-buttons-icons-images.html'}
  __reqCss, __reqJs = ['font-awesome', 'bootstrap'], ['font-awesome', 'bootstrap', 'jquery']
  name, category, callFnc, docCategory = 'Generic Button', 'Button', 'button', 'Advanced'
  __pyStyle = ['CssButtonBasic']

  def __init__(self, aresObj, text, width, widthUnit, height, heightUnit, disable, color, icon, align, internalLink, htmlCode, groupId, docBlock, tooltip):
    self.isJs = False
    if docBlock is not None:
      if not isinstance(docBlock, dict):
        docBlock = {"id": docBlock}
      docBlock['params'] = "'%s'" % text
      if icon is not None:
        docBlock['params'] = "%s, icon='%s'" % icon
    super(Button, self).__init__(aresObj, text, htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit, docBlock=docBlock)
    self._jsStyles = {'icon': icon}
    self.disable, self.__battr, self.groupId = disable, {}, groupId
    self.color, self.align = color, align
    if self.color is None:
      self.color = self.getColor('textColor', 1)
    if internalLink is not None:
      self.click(self.jsGoTo(internalLink))
    if groupId is not None:
      self.attr['name'] = groupId
      self.jsFrg('click', '''
        var count = $(this).data('count')+1; $(this).data('count', count);
        $("button[name='%(groupId)s']").css( {'background-color': 'white', 'color': '%(color)s'} ); 
        $(this).css( {'background-color': '%(color)s', 'color': 'white'}); ''' % {"color": self.color, 'groupId': groupId})
    else:
      self.jsFrg('click', "var count = $(this).data('count')+1; $(this).data('count', count);")
    if tooltip is not None:
      self.tooltip(tooltip)

  @property
  def jsQueryData(self):
    """
      :category: Javascript features
      :example: myObj.jsQueryData()
      :return: A String which represents a Javascript dictionary
      :dsc:
        Python function used in the javascript side to get an object with all the information of the component during an event.
        Basically this function will allow to get all the mandatory detail for an Ajax call
    """
    return "{ event_val: $(this).html(), event_groupId: '%s', event_count_click: $(this).data('count')+1 }" % self.groupId

  def jsDisable(self, bool=None, isPyData=True):
    """
    :category: Javascript features
    :example: myObj.jsDisable(True)
    :return: A string defining / setting the disable of the button on the javascript side
    :dsc:
      Python function to write the piece of code in charge of defining or changing the disable state of a button.
      This can be set in the Python but also used in any jsEvent function
    """
    if bool is None:
      return "%s.disabled ;" % self.jqId

    if isPyData:
      bool = json.dumps(bool)
    return '%s.attr("disabled", %s) ;' % (self.jqId, bool)

  def addAttr(self, key, val=None, isPyData=True):
    if val is None and issubclass(key, AresHtml.Html):
      self.__battr[key.htmlCode] = key.val
      self.isJs = True
    else:
      if isPyData:
        val = json.dumps(val)
      else:
        self.isJs = True
      self.__battr[key] = val

  def addStyles(self, cssAttrIcon=None, cssAttr=None):
    """
    :category: Javascript Builder function
    :rubric: JS
    :dsc:
      Add style properties to be used in the definition of the component in the Javascript layer
    :return: The object itself
    """
    if cssAttrIcon is not None:
      self._jsStyles.setdefault('styleIcon', {}).update(cssAttrIcon)
    if cssAttr is not None:
      self._jsStyles.setdefault('styles', {}).update(cssAttr)
    return self

  def mouseOverColor(self, color):
    """
      :category: Javascript features
      :example: myObj.mouseOverColor('green')
      :return: The python object itself
      :dsc:
        Change the color of the button background when the mouse is hover
    """
    self.addAttr("onmouseover", "this.style.backgroundColor='%s';this.style.color='white'" % color)
    self.addAttr("onmouseout", "this.style.backgroundColor=\'white\';this.style.color=\'%s\';" % color)
    return self

  def onDocumentLoadFnc(self):
    """
    :category: Javascript features
    :example: myObj.onDocumentLoadFnc()
    :dsc:
      Create a Javascript function to build the object
    """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' htmlObj.empty();
      if( jsStyles.icon != undefined) { 
        var iconItem = $('<i class="' + jsStyles.icon +'" style="margin-right:5px"></i>') ;
        if (jsStyles.styleIcon != undefined) { iconItem.css( jsStyles.styleIcon ); } ;
        htmlObj.append(iconItem) ;  };
      htmlObj.append(data) ; 
      if (jsStyles.styles != undefined) { htmlObj.css(jsStyles.styles) } ;
    ''', 'Javascript Object builder')

  def goTo(self, url=None, isPyData=True):
    """
    :category: Javascript Event
    :example: myObj.goTo('www.google.fr', isPyData=True)
    :dsc:
      Create a javasscript click event on the button to go to a new URL.
      This will create a link to open a new external web page or an internal report
    """
    self.click( self.jsGoTo(url, isPyData))
    return self

  def __str__(self):
    """
    :category: Output function
    :dsc:
      Return the String representation of HTML button
    """
    disFlag = "disabled" if self.disable else ''
    if self.align is None:
      return '<button data-count=0 %s %s></button>' % (self.strAttr(pyClassNames=self.pyStyle), disFlag)

    return '<div style="clear:both;width:100%%;text-align:%s"><button data-count=0 %s %s></button></div>' % (self.align, self.strAttr(pyClassNames=self.pyStyle), disFlag)

  @staticmethod
  def matchMarkDown(val):
    return val.startswith("[button ")

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj):
    res = re.search('\[button url="(.*)"\]\((.*)\)', val)
    if res is not None:
      if aresObj is not None:
        getattr(aresObj, 'button')(res.group(2)).goTo(res.group(1))
      return ["aresObj.button('%s').goTo('%s')" % (res.group(2), res.group(1))]

  @classmethod
  def jsMarkDown(self, vals):
    return '[button url=""](%s)' % vals

  def to_word(self, document):
    pass


class ButtonIcon(Button):
  """

  """
  name, category, callFnc, docCategory = 'Button Icon', 'Button', 'buttonicon', 'Advanced'
  mocks = 'fas fa-adjust'

  def __init__(self, aresObj, icon, text, color, align, internalLink, backgroundColor, htmlCode):
    super(ButtonIcon, self).__init__(aresObj, text, False, color, icon, align, internalLink=internalLink, htmlCode=htmlCode)
    self._jsStyles = {'icon': icon}
    if backgroundColor is not None:
        self._jsStyles['backgroundColor'] = backgroundColor
    self.css( {"text-align" : "center", 'padding': '5px 0px 5px 10px', 'font-size': '18px'})

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' htmlObj.empty();
      if( jsStyles.icon != undefined) { htmlObj.append('<i class="' + jsStyles.icon +'" style="margin-right:5px"></i>') ; };
      if( jsStyles.backgroundColor != undefined) { htmlObj.css( 'background-color', jsStyles.backgroundColor) ; }
      htmlObj.append(text) ; ''', 'Javascript Object builder')


class IconEdit(AresHtml.Html):
  name, category, callFnc, docCategory = 'Icon Edit', 'Button', 'iconEdit', 'Advanced'
  mocks, icon, title = "Edit", 'far fa-edit', 'Edit'
  inReport = False

  def __init__(self, aresObj, position, icon, tooltip):
    self.icon = icon if icon is not None else self.icon
    self.title = tooltip if tooltip is not None else self.title
    if position is None:
      position = 'right'
    super(IconEdit, self).__init__(aresObj, '')
    self.css( {"margin-top": "5px", "margin-bottom": "5px", "float": position, "margin-left": "4px", "margin-right": "4px",
               "color": "%s" % self.getColor('border', 0), 'font-size': '18px', 'cursor': 'pointer' } )
    self.attr.update( {'class': set([self.icon]), 'data-original-title': self.title, 'name': "tooltip", 'data-toggle': 'tooltip', 'data-placement': 'top'} )
    # Add the different mouse event in the Html definition
    self.addAttr("onmouseover", "this.style.color='%s'" % self.getColor('border', 1))
    self.addAttr("onmouseout", "this.style.color='%s'" % self.getColor('border', 0))

  @property
  def jsQueryData(self): return "{}"

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, 'htmlObj.tooltip()', 'Javascript Object builder')

  def __str__(self): return "<div %s></div>" % (self.strAttr(pyClassNames=self.pyStyle))


class IconRefresh(IconEdit):
  name, category, callFnc, docCategory = 'Icon Refresh', 'Button', 'refresh', 'Advanced'
  mocks, icon, title = "Refresh", 'fas fa-sync-alt', 'Refresh Component'


class IconPdf(IconEdit):
  name, category, callFnc, docCategory = 'Icon Pdf', 'Button', 'pdf', 'Advanced'
  mocks, icon, title = "Pdf", 'far fa-file-pdf', 'Convert to PDF'


class IconPlus(IconEdit):
  name, category, callFnc, docCategory = 'Icon Plus', 'Button', 'plus', 'Advanced'
  mocks, icon, title = "Plus", 'fas fa-plus-square', 'Add line'

  def __init__(self, aresObj, position, icon, tooltip):
    if position is None:
      position = 'right'
    super(IconEdit, self).__init__(aresObj, '', icon, tooltip)
    self.css( {"margin-top": "3px", "margin-bottom": "5px", "float": position, "margin-left": "4px", "margin-right": "4px",
               "color": "%s" % self.getColor('baseColor', 2), 'font-size': '20px', 'cursor': 'pointer' } )
    self.attr.update( {'class': set([self.icon]), 'data-original-title': self.title, 'name': "tooltip", 'data-toggle': 'tooltip', 'data-placement': 'top'} )


class IconExcel(IconEdit):
  name, category, callFnc, docCategory = 'Icon Excel', 'Button', 'excel', 'Advanced'
  mocks, icon, title = "Excel", 'far fa-file-excel', 'Convert to Excel'


class IconThumbtack(IconEdit):
  name, category, callFnc, docCategory = 'Icon Thumbtack', 'Button', 'thumbtack', 'Advanced'
  mocks, icon, title = "Comment", 'fas fa-thumbtack', 'Add comment'

  def __init__(self, aresObj, parentJqId, position, icon, tooltip):
    if position is None:
      position = 'right'
    super(IconEdit, self).__init__(aresObj, '', icon, tooltip)
    self.css( {"margin-top": "5px", "margin-bottom": "5px", "float": position, "margin-left": "4px", "margin-right": "4px",
               "color": "%s" % self.getColor('border', 0), 'font-size': '18px', 'cursor': 'pointer'} )
    self.attr.update({'class': set([self.icon]), 'data-original-title': self.title, 'name': "tooltip", 'data-toggle': 'tooltip', 'data-placement': 'top'})
    # Add the different mouse event in the Html definition
    self.addAttr("onmouseover", "this.style.color='%s'" % self.getColor('border', 1))
    self.addAttr("onmouseout", "this.style.color='%s'" % self.getColor('border', 0))
    self.parentJqId = parentJqId
    self.addGlobalVar('thumbtack_counter', 0)

  def __str__(self):
    self.aresObj.jsOnLoadFnc.add('''
      %(jqId)s.on('click', function(event) { 
          var posX = $(this).offset().left; var posY = $(this).offset().top;
          var comment = $('<div name="thumbtack" id="'+ thumbtack_counter +'"></div>');
          comment.append('<div autocorrect="off" spellcheck="false" placeholder="comment" contenteditable=true style="float:left;margin-left:5px;margin-right:10px;">Comment</div>') ;
          comment.append('<span style="color:%(color)s;margin-left:4px" onmouseover="this.style.color=\\\'grey\\\'" onmouseout="this.style.color=\\\'%(color)s\\\'"  class="far fa-edit" onclick="$(this).prev().focus()"></span>');
          comment.append('<span id="lock_' + thumbtack_counter + '" onclick="$(this).parent().draggable(\\\'disable\\\'); $(this).remove() ;" style="color:%(color)s;margin-left:4px" onmouseover="this.style.color=\\\'grey\\\'" onmouseout="this.style.color=\\\'%(color)s\\\'" class="fas fa-lock"></span>');
          comment.append('<span style="color:%(color)s;margin-left:4px" onmouseover="this.style.color=\\\'red\\\'" onmouseout="this.style.color=\\\'%(color)s\\\'"  class="far fa-trash-alt" onclick="$(this).parent().remove()"></span>');
          %(parent)s.append(comment) ;
          comment.css({'position': 'absolute', 'top':  event.pageY - posY+10, 'right': event.pageX - posX + 10}) ;
          comment.draggable() ; 
      }) ;''' % {'jqId': self.jqId, 'parent': self.parentJqId, 'color': self.getColor('baseColor', 3)})
    # self.aresObj.jsOnLoadFnc.add(''' %(jqId)s.on('click', function(event) { $('#%(htmlId)s_content').focus() ; }) ''' % {"jqId": self.jqId, 'htmlId': self.htmlId})
    return "<div %s></div>" % (self.strAttr(pyClassNames=self.pyStyle))


class IconDownload(IconEdit):
  name, category, callFnc, docCategory = 'Icon Upload', 'Button', 'upButton', 'Advanced'
  mocks, icon, title = "Download", 'fas fa-download', 'Download'


class IconDelete(IconEdit):
  name, category, callFnc, docCategory = 'Icon Delete', 'Button', 'delete', 'Advanced'
  mocks, icon, title = "Delete", 'far fa-trash-alt', 'Delete Component on the page'

  def __init__(self, aresObj, position, icon, tooltip):
    super(IconDelete, self).__init__(aresObj, position, icon, tooltip)
    self.addAttr("onmouseover", "this.style.color='red'")


class IconLock(IconEdit):
  name, category, callFnc, docCategory = 'Icon Lock', 'Button', 'lock', 'Advanced'
  mocks, icon, iconLock, title = "Lock", 'fas fa-unlock', 'fas fa-lock', 'Lock Comment'

  def click(self, jsListFncLock, jsListFncUnLock):
    self.aresObj.jsOnLoadFnc.add('''
      %(jqId)s.on('click', function(event) {
        if ($(this).hasClass('fa-unlock') == true) {%(jsFncLock)s; $(this).addClass('fa-lock'); $(this).removeClass('fa-unlock'); }
        else { %(jsFncUnLock)s; $(this).removeClass('fa-lock'); $(this).addClass('fa-unlock'); } ;
      } ); ''' % { "jqId": self.jqId, "jsFncLock": ";".join(jsListFncLock), "jsFncUnLock": ";".join(jsListFncUnLock)})


class IconZoom(IconEdit):
  name, category, callFnc, docCategory = 'Icon Zoom', 'Button', 'zoom', 'Advanced'
  mocks, icon, title = "Zoom", 'fas fa-search-plus', 'Zoom on Component'


class IconCapture(IconEdit):
  name, category, callFnc, docCategory = 'Icon Capture', 'Button', 'capture', 'Advanced'
  mocks, icon, title = "Save", '', 'Save to clipboard'


class IconClock(IconEdit):
  name, category, callFnc, docCategory = 'Icon Clock', 'Button', 'clock', 'Advanced'
  mocks, icon, title = "Last updated Time", 'fas fa-clock', 'Last Updated Time'
  inReport = False

  def __str__(self): return "<div %s></div>" % self.strAttr(pyClassNames=self.pyStyle)


class IconRemove(IconEdit):
  name, category, callFnc, docCategory = 'Icon Remove', 'Button', 'remove', 'Advanced'
  mocks, icon, title = "Save", 'fas fa-times-circle', 'Remove Item'

  def __init__(self, aresObj, position, icon, tooltip):
    super(IconRemove, self).__init__(aresObj, position, icon, tooltip)
    self.addAttr("onmouseover", "this.style.color='red'")


class IconTable(IconEdit):
  name, category, callFnc, docCategory = 'Icon Table', 'Button', 'icontable', 'Advanced'
  mocks, icon, title = "Table", 'fas fa-table', 'Convert to Table'


class IconWrench(IconEdit):
  name, category, callFnc, docCategory = 'Icon Wrench', 'Button', 'wrench', 'Advanced'
  mocks, icon, title = "Processing Time", 'fas fa-wrench', 'Processing Time'


class IconSum(IconEdit):
  name, category, callFnc, docCategory = 'Icon Sum', 'Button', 'calculator', 'Advanced'
  mocks, icon, title = "Sum", 'fas fa-calculator', 'Simple Calculator'

  def __init__(self, aresObj, parentJqId, icon, tooltip):
    self.parentJqId = parentJqId
    super(IconSum, self).__init__(aresObj, '', icon, tooltip)

  def __str__(self):
    self.aresObj.jsOnLoadFnc.add('''
      %(jqId)s.on('click', function(event) { 
         if($("#icon_sum").length == 0) {
          $('table[name="aresTable"] td').bind( "click", function( event ) { 
              var sum = parseFloat($("#icon_sum").find('#floating_sum').text().replace(',', '') ) + parseFloat( $(this).text().replace(',', '') ); 
              var count = parseFloat($("#icon_sum").find('#floating_count').text().replace(',', '') ) + 1 ; 
              var average = sum / count ; 
              var absSum = parseFloat($("#icon_sum").find('#floating_abs_sum').text().replace(',', '') ) + Math.abs( parseFloat( $(this).text().replace(',', '')) ) ; 
              
              $("#icon_sum").find('#floating_sum').text(sum.formatMoney(2, ',', '.'));
              $("#icon_sum").find('#floating_count').text(count.formatMoney(0, ',', '.'));
              $("#icon_sum").find('#floating_average').text(average.formatMoney(2, ',', '.'));
              $("#icon_sum").find('#floating_abs_sum').text(absSum.formatMoney(2, ',', '.'));
              
           } ) ;
          var comment = $('<div id="icon_sum" class="ui-widget-content" style="z-index:100;width:150px;border-radius:5px 5px 0 0;padding:5px"></div>');
          comment.append("<div style='float:left;font-weight:bold'>Sum:</div><div style='width:100%%;text-align:center;font-size:14px' id='floating_sum'>0</div>") ; 
          comment.append("<div style='float:left;font-weight:bold'>Count:</div><div style='width:100%%;text-align:center;font-size:14px' id='floating_count'>0</div>") ; 
          comment.append("<div style='float:left;font-weight:bold'>Average:</div><div style='width:100%%;text-align:center;font-size:14px' id='floating_average'>0</div>") ; 
          comment.append("<div style='float:left;font-weight:bold'>Abs Sum:</div><div style='width:100%%;text-align:center;font-size:14px' id='floating_abs_sum'>0</div>") ; 
          $('body').append(comment) ;
          comment.css( {'position': 'fixed', 'left': 200, 'top': 90} ) ; comment.draggable() ; 
        } else {
          $("#icon_sum").remove() ; $('table[name="aresTable"] td').unbind( "click" ) ;}
      }) ; ''' % {'jqId': self.jqId, 'color': self.getColor('border', 0)})
    return "<div %s></div>" % (self.strAttr(pyClassNames=self.pyStyle))

