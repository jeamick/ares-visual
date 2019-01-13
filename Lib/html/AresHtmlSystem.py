#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

"""
This section is dedicated to group all the components created for the Ares main web pages.
They are all in this module to ensure that any change of them will not impact the user section.

If you are a user and for some reason you are looking at this module please talk to your IT team they should be able to
help you to get the right component.
"""

import os
from ares.Lib.html import AresHtml


class HtmlAresLinks(AresHtml.Html):
  """

  """
  __reqCss, __reqJs = ['bootstrap'], ['bootstrap']

  def __init__(self, aresObj, aresClass):
    """ """
    self.cls = aresClass
    self.aresObj = aresObj

  def __str__(self):
    #self.aresObj.jsOnLoadFnc.add("$(\"div[name='system']\").tooltip()")
    splitModuleName = self.cls.__module__.split('.')
    badge = self.aresObj.badge('New') if getattr(self.cls, 'isNew', False) else ''
    return '<div title="%s" name="system"><a href="/doc/%s/%s/%s" style="word-wrap:break-word">%s</a>%s</div>' % (self.cls.__doc__, splitModuleName[-2], splitModuleName[-1], self.cls.__name__, self.cls.name, badge)


class DbAresLinks(AresHtml.Html):
  """

  """
  __reqCss, __reqJs = ['bootstrap'], ['bootstrap']

  def __init__(self, aresObj, fncName):
    """ """
    self.fncName = fncName
    self.aresObj = aresObj

  def __str__(self):
    return '<div title="%s" name="system"><a href="/doc/db/%s" style="word-wrap:break-word">%s</a></div>' % (self.fncName.__doc__, self.fncName, self.fncName)


class FilesAresLinks(AresHtml.Html):
  """

  """
  __reqCss, __reqJs = ['bootstrap'], ['bootstrap']

  def __init__(self, aresObj, fncName):
    """ """
    self.fncName = fncName
    self.aresObj = aresObj

  def __str__(self):
    return '<div title="%s" name="system"><a href="/doc/files/%s" style="word-wrap:break-word">%s</a></div>' % (self.fncName.__doc__, self.fncName, self.fncName)


class HtmlAresLinksCharts(AresHtml.Html):
  """

  """

  def __init__(self, aresObj, aresClass, chartType):
    """ """
    self.cls, self.chartType = aresClass, chartType
    self.aresObj = aresObj

  def __str__(self):
    #self.aresObj.jsOnLoadFnc.add("$(\"div[name='system']\").tooltip()")
    splitModuleName = self.cls.__module__.split('.')
    badge = self.aresObj.badge('New') if getattr(self.cls, 'isNew', False) else ''
    return '<div title="%s" name="system"><a href="/doc/%s/%s/%s" style="word-wrap:break-word">%s %s</a>%s</div>' % (self.cls.__doc__, splitModuleName[-2], splitModuleName[-1], self.chartType, self.cls.name, self.chartType, badge)


class Loading(AresHtml.Html):
  """

  """
  name, category = 'Loading', 'Others'
  __pyStyle = ['CssDivLoading']
  __reqCss, __reqJs = ['font-awesome'], ['font-awesome']
  inReport = False

  def __str__(self):
    """ Return the String representation of a help HTML item """
    self.loadStyle()
    if self.vals is None:
      return '<div %s><i style="margin:auto;font-size:20px" class="fas fa-spinner fa-spin"></i><br />Loading...</div>' % ( self.strAttr(withId=False, pyClassNames=self.pyStyle))

    return '<div %s><i style="margin:auto;font-size:20px" class="fas fa-spinner fa-spin"></i><br />%s...</div>' % (self.strAttr(withId=False, pyClassNames=self.pyStyle), self.vals)


class TextInput(AresHtml.Html):
  """ special HTML object in charge of changing properties when double clicked """
  __reqJs, __reqCss = ['jquery'], ['bootstrap', 'font-awesome']
  name, category = 'Editable Text', 'Text'
  __pyStyle = ['CssDivBoxWithDotBorder', 'CssText']
  references = {'Example': 'http://css.mammouthland.net/border-css.php'}

  def __init__(self, aresObj, text, width, widthUnit, size, color):
    """ Instantiate the Python object

    :param aresObj: The ares report object
    :param text: The default value when the editable div is empty
    :param width: The size of the div
    :param size: The font size
    :param color: The font color
    :param cssCls: (Optional) The optional CSS classes
    """
    super(TextInput, self).__init__(aresObj, text, None)
    size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    color = color if color is not None else 'black'
    self.css( {'color': color, 'font-size': '%spx' % size, 'width': '%s%s' % (width, widthUnit)} )

  def __str__(self):
    """ Return the html string representation """
    items = ['<div ondblclick="$(\'#in_%(htmlId)s\').show(); $(\'#in_%(htmlId)s\').focus(); $(this).hide();" %(attr)s>%(val)s</div>' % {'htmlId': self.htmlId, 'attr': self.strAttr(pyClassNames=['CssDivBoxWithDotBorder', 'CssText']), 'val': self.vals}]
    items.append('<input type="text" id="in_%(htmlId)s" value="%(val)s" style="display:none;margin:5px">' % {'htmlId': self.htmlId, 'val': self.vals})
    self.aresObj.jsOnLoadFnc.add('''
      $( "#in_%(htmlId)s" ).blur(function() {
        if($(this).val() != "") { $(\'#%(htmlId)s\').html($(this).val()); } else { $(\'#%(htmlId)s\').html(\'%(val)s\'); }; $(\'#%(htmlId)s\').show() ; $(this).hide()
      }); ''' % {'htmlId': self.htmlId, 'val': self.vals})
    return "".join(items)


class Wiki(AresHtml.Html):
  """
  This object is very special and this is dedicated to manage comments
  People using this object will be able to create simpe json text file with comments for each line

  The idea of this report is to expose some information and then to alloww users to be able to update it
  The extra information will be done on dedicated files and later they can be included to the scripts
  """
  alias = 'wiki'

  def __init__(self, aresObj, dataSourceName, vals):
    """ Init override in order to store the Ares Object (only the parameters"""
    super(Wiki, self).__init__(aresObj, vals)
    self.http = aresObj.http
    self.dataSourceName = dataSourceName

  def __str__(self):
    """ Return the html string representation """
    items = ['<div class="page" style="margin-left:25%;margin-right:25%">']
    commentFiles = {}
    configPath = os.path.join(self.http['DIRECTORY'], 'config', self.dataSourceName)
    if not os.path.exists(configPath):
      os.makedirs(configPath)
    for pyFile in os.listdir(configPath):
      configFile = open(os.path.join(configPath, pyFile))
      content = configFile.read()
      if content != '':
        commentFiles[pyFile.replace(".cfg", "")] = content
      configFile.close()
    for i, val in enumerate(self.vals):
      objectId = "%s_%s" % (self.htmlId, i)
      items.append(
        '<div style="white-space: pre;" ondblclick="$(\'#in_%s\').show() ; $(\'#in_cmmt_%s\').focus()" id="%s">%s</div>' % (
        objectId, objectId, objectId, val))
      inCmmtId = 'in_cmmt_%s' % objectId
      if inCmmtId in commentFiles:
        items.append('<div id="in_%s">' % objectId)
        items.append(
          '<textarea class="bubble_cmmt" id="%s" onblur="leaveBox($(\'#in_%s\'), $(this)) ;">%s</textarea>' % (
          inCmmtId, objectId, commentFiles[inCmmtId]))
      else:
        items.append('<div id="in_%s" style="display:none;">' % objectId)
        items.append('<textarea class="bubble_cmmt" id="%s" onblur="leaveBox($(\'#in_%s\'), $(this)) ;"></textarea>' % (
        inCmmtId, objectId))
      items.append(
        '<button type="button" class="btn btn-success" style="margin-bottom:10px;margin-left:5px" onclick="save_cmmt($(this), $(\'#in_cmmt_%s\')) ;">Save</button>' % objectId)
      items.append(
        '<button type="button" id="in_cmmt_%s_cl" class="btn btn-danger" style="margin-bottom:10px;" onclick="wikiCancelComments($(\'#in_%s\'), $(\'#in_cmmt_%s\')) ;">Cancel</button>' % (
        objectId, objectId, objectId))
      items.append('</div>')
    items.append('</div>')
    self.aresObj.jsOnLoadFnc.add("function wikiCancelComments(box, cmmt) {cmmt.val('');box.hide() ;}")

    return "".join(items)

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return None

  def onLoadFnc(self):
    """

    """
    return """
            function leaveBox(box, cmmt) {
              if (cmmt.val() == '') { box.hide() ; }
            } ;

            function save_cmmt(button, cmmt) {
              $.post("/reports/json/%s", {val: cmmt.val(), key: cmmt.attr('id'), source: '%s'}, function(data) {
                button.hide();
                $('#'+ cmmt.attr('id')).attr('readonly','readonly');
                $('#'+ cmmt.attr('id') +'_cl').hide();
              } );
            } ;

            function cancel_cmmt(box, cmmt) {cmmt.val('');box.hide() ;}
           """ % (self.http['REPORT_NAME'], self.dataSourceName)


class Comments(AresHtml.Html):
  """ Python wrapper to a div item composed to several sub html items to display message """
  name, category, callFnc = 'Comment', 'Text', 'comments'
  __pyStyle = ['CssDivComms', 'CssButtonBasic']
  references = {'Example': 'https://leaverou.github.io/bubbly/',
                'scrollbar': 'http://manos.malihu.gr/jquery-custom-content-scroller/'}

  __reqCss, __reqJs = ['jquery-scrollbar'], ['jquery-scrollbar']

  def __init__(self, aresObj, recordset, width, widthUnit, height, heightUnit, size, color):
    """ Instantiate the object and store the different values """
    super(Comments, self).__init__(aresObj, recordset)
    self.color = self.getColor('baseColor', 9) if color is None else color
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) if size is None else size
    self.css( {'width': '%s%s' % (width, widthUnit), 'height': '%s%s' % (height, heightUnit)})

  def jsLoad(self, jsData='data', jsDataKey='comments', isPyData=False):
    # This is a bit more complicated
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return '''
          var height = $('#comments_%(htmlId)s').css('height') ;
          $('#comments_%(htmlId)s').empty() ;
          %(jsData)s.forEach( function (rec) {
            rec['color'] = '#2B4B84' ;
            if ( rec['category'] == 'Incident' ) { rec['color'] = '#C61818' ; }
            $('#comments_%(htmlId)s').append('<div %(cls)s style="font-size:12px;border:1px solid '+ rec['color'] +'"><b>' + rec['subject'] + '</b><br />'+ rec['comment'] +'<div style="text-align:right;width:100%%;font-style:italic;">'+ rec['author'] +', '+ rec['date'] + '</div></div>') ;
          }) ;
          $('#comments_%(htmlId)s').css( {'height': height, 'overflow': 'auto', 'margin': '0 10px 0 10px', 'padding': '5px 0 5px 0' }) ;
          $(".content").mCustomScrollbar("update"); 
          ''' % { 'htmlId': self.htmlId, 'jsData': jsData, 'cls': self.aresObj.cssObj.getClsTag([' CssDivComms']) }

  def jsAdd(self, jsData='data', jsDataKey='comments', isPyData=False):
    return '''
      $('#comments_%(htmlId)s').append('<div %(cls)s style="font-size:12px;border:1px solid '+ rec['color'] +'"><b>' + rec['subject'] + '</b><br />'+ rec['comment'] +'<div style="text-align:right;width:100%%;font-style:italic;">'+ rec['author'] +', '+ rec['date'] + '</div></div>') ;
      '''

  def __str__(self):
    """ String representation of the Comment section """
    self.aresObj.jsOnLoadFnc.add('''
      $(window).on("load",function(){  $(".content").mCustomScrollbar(); });
      ''')

    items = ["<div style='margin:5px;width:100%;display:block;padding:5px 5px 5px 0;'>"]
    items.append("<div style='width:100%%;font-size:%spx;background-color:#F4F4F4;padding:5px;font-weight:bold'>Recent Comments - %s comments</div>" % (self.size, len(self.vals)))
    items.append('<div id="comments_%s" style="margin:0 10px 0 10px;height:300px;padding:5px 0 5px 0" class="mCustomScrollbar" data-mcs-theme="3d">' % self.htmlId)

    for comm in self.vals:
      comm['cls'] = self.aresObj.cssObj.getClsTag(['CssDivComms'])
      comm['size'] = self.size - 2
      comm['color'] = '#C61818' if comm['category'] in ['Bug', 'Incident'] else '#2B4B84'
      items.append('''
         <div %(cls)s style="font-size:%(size)spx;border:1px solid %(color)s"><b>%(subject)s</b><br /> 
            %(comment)s
        <div style="text-align:right;width:100%%;font-style:italic;">%(author)s, %(date)s</div>
         </div>''' % comm )
    items.append("</div>")
    items.append("</div>")
    return "".join(items)


class Message(AresHtml.Html):
  name, category, callFnc = 'Comment', 'Text', 'comments'
  __pyStyle = ['CssDivWithBorder']

  def __init__(self, aresObj, title, width, widthUnit, height, heightUnit, size, color, htmlCode, send_to):
    """ Instantiate the object and store the different values """
    super(Message, self).__init__(aresObj, None, htmlCode=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.color = self.getColor('baseColor', 9) if color is None else color
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) if size is None else size
    self.title, self.height = title, height
    self.send_to = send_to
    if self.send_to:
      if not self.htmlCode:
        raise Exception('You need to provide an htmlCode if you want to use this feature')

  @property
  def val(self):
    return '''$('#' + htmlId).find("[name='message']").text()'''

  def __str__(self):
    """ String representation of the Comment section """
    pyButton = self.addPyCss('CssButtonBasic')
    if self.send_to:
      self.addGlobalFnc('StoreMessage(htmlId)', '%s; location.reload();' % self.aresObj.jsPost(self.send_to, ''''data': %s''' % self.val, "alert('Report Bug Sent');", isPyData=False))
    else:
      self.addGlobalFnc('StoreMessage(htmlId)', '''
        alert( $('#' + htmlId).find("[name='message']").text() ) ;
        ''')
    return """
      <div %(strAttr)s>
        <label style="width:90%%;text-align:left;font-weight:bold;font-size:15px">Comment</label>
        <div name="message" contenteditable="true" placeholder="Put your comment here" style="margin:auto;resize:none;width:100%%;height:%(height)spx;border:1px solid black;margin-bottom:5px;background:white;text-align:left;padding:2px"></div>
        <div style="width:99%%;text-align:right;padding-right:5px"><div style="width:100%%;text-align:middle"><button onclick="StoreMessage('%(htmlId)s')" class="%(pyButton)s">Send</button></div></div>
      </div>
      """ % {'strAttr': self.strAttr(pyClassNames=['CssDivWithBorder']), 'pyButton': pyButton,'cssButton': self.aresObj.cssObj.getClsTag(['CssButtonBasic']),
             'height': self.height-100, 'htmlId': self.htmlId }

