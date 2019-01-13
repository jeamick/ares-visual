#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import re
import json

from ares.Lib.html import AresHtml


class Tick(AresHtml.Html):
  """ Wrapper for a numerical component with a up and down arrow

  :example
  aresObj.tick(34)
  """
  name, category, callFnc, docCategory = 'Tick', 'Number', 'tick', 'Preformatted'
  __reqCss, __reqJs = ['font-awesome'], ['font-awesome']
  references = {"Icon": "https://fontawesome.com/icons/check?style=solid"}
  __pyStyle = ['CssNumberCenter']

  def __init__(self, aresObj, value, label, size, color, tooltip):
    super(Tick, self).__init__(aresObj, value)
    self.label = label
    color = self.getColor('baseColor', 3) if color is None else color
    size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    self.css({'font-size': size, 'color': color})
    self.addAttr('title', tooltip)
    if tooltip != '':
      self.css('cursor', 'pointer')

  @property
  def val(self): return "$('#%s span').html()" % self.htmlId

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
       if (data) { htmlObj.append("<i class='fas fa-check' aria-hidden='true' style='color:green'></i>"); }
       else if (data === 0) { 
        htmlObj.append("<i class='fas fa-exclamation-triangle' aria-hidden='true' style='color:orange'></i>"); }
       else { htmlObj.append("<i class='fas fa-times' aria-hidden='true' style='color:red'></i>"); }  ''')

  def __str__(self):
    """ Return the String representation of a line tag """
    if self.label is not None:
      self.css({'display': 'inline-block', 'width': '20px'})
      return '''
        <div style="margin:5px 0">
          <div %s></div>
          <span style="height:100%%;display:inline-block;padding-right:5px;margin-bottom:2px">%s</span>
          %s
        </div>''' % (self.strAttr(pyClassNames=self.__pyStyle), self.label, self.helper)

    return "<div %s></div>" % self.strAttr(pyClassNames=self.pyStyle)

  @staticmethod
  def matchMarkDown(val):
    return re.match("\+\+\+(.*)", val) or re.match("\-\-\-(.*)", val)

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj):
    param = True if val.startswith("+") else False
    if aresObj is not None:
      getattr(aresObj, cls.callFnc)(param, regExpResult.group(1))
    return ["aresObj.%s(%s, %s)" % (cls.callFnc, param, regExpResult.group(1))]

  @classmethod
  def jsMarkDown(self, vals):
    if vals:
      return "+++" % self.label

    return "---%s" % self.label


class UpDown(AresHtml.Html):
  """ Up and down Text component

  :example
  aresObj.updown(34, -3)
  """
  name, category, callFnc, docCategory = 'Up and Down', 'Number', 'updown', 'Preformatted'
  __reqCss, __reqJs = ['font-awesome'], ['font-awesome']
  __pyStyle = ['CsssDivBoxMargin']
  references = {'Icon': "https://fontawesome.com/"}
  mocks = {'delta': 100, 'value': 240985}

  def __init__(self, aresObj, recordSet, size, color):
    """

    :param aresObj:
    :param recordSet:
    :param size:
    :param color:
    """
    super(UpDown, self).__init__(aresObj, recordSet)
    self.vals['color'] = self.getColor('baseColor', 3) if color is None else color
    size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    self.css( {'font-size': size} )

  @property
  def val(self): return '$("#%s span").html()' % self.jqId

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
      if (data.delta < 0) { htmlObj.append("<i class='fas fa-arrow-down' aria-hidden='true' style='color:green'></i>"); }
      else { htmlObj.append("<i class='fas fa-arrow-up' aria-hidden='true' style='color:%(greenColor)s'></i>"); } ;
      htmlObj.append("<span style='padding:5px;color:"+ data.color +"'>"+ FormatNumber(data.value, 0, ',', ',') +"</span>") ; 
      ''' % {"greenColor": self.getColor("greenColor", 0) })

  def __str__(self):
    """ Return the String representation of a line tag """
    self.addGlobalFnc("FormatNumber(n, decPlaces, thouSeparator, decSeparator)", '''
      decPlaces = isNaN(decPlaces = Math.abs(decPlaces)) ? 2 : decPlaces,
      decSeparator = decSeparator == undefined ? "." : decSeparator,
      thouSeparator = thouSeparator == undefined ? "," : thouSeparator,
      sign = n < 0 ? "-" : "",
      i = parseInt(n = Math.abs(+n || 0).toFixed(decPlaces)) + "",
      j = (j = i.length) > 3 ? j % 3 : 0;
      return sign + (j ? i.substr(0, j) + thouSeparator : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thouSeparator) + (decPlaces ? decSeparator + Math.abs(n - i).toFixed(decPlaces).slice(2) : "");
    ''')
    return '<div %s></div>' % self.strAttr(pyClassNames=self.pyStyle)


class TextBubble(AresHtml.Html):
  """ Python wrapper for a text element with a figure in a bubble and a title

  :example
  aresObj.textbubble("title", 10, size=40)
  """
  name, category, callFnc, docCategory = 'Bubble text', 'Text', 'textbubble', 'Preformatted'
  __pyStyle = ['CssDivBox', 'CssDivBubble', 'CssTitle']
  mocks = {"url": "", "title": "Python", 'value': 100, 'color': 'green'}

  def __init__(self, aresObj, recordSet, width, widthUnit, color, size, backgroundColor):
    """

    :param aresObj:
    :param recordSet:
    :param width:
    :param widthUnit:
    :param color:
    :param size:
    :param backgroundColor:
    """
    super(TextBubble, self).__init__(aresObj, recordSet)
    self.color = self.getColor('baseColor', 3) if color is None else color
    self.backgroundColor = 'white' if backgroundColor is None else backgroundColor
    self.size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    self.css( {'width': "%s%s" % (width, widthUnit), 'padding-top': '5px', 'margin-left': '5px',
               'text-align': 'center', 'background-color': self.getColor('greyColor', 0)})

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    if 'url' in self.vals is None:
      return '$("#%s > div").first().find("div").html()' % self.htmlId

    return '$("#%s > div").first().find("a").html()' % self.htmlId

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      htmlObj.find('div').first().empty() ; htmlObj.find('div').first().append(data.value); 
      if (data.url != undefined) { htmlObj.find('div').last().find('a').attr('href', data.url);} 
      else { htmlObj.find('div').last().find('a').attr('href', '#') ;} ;
      if (data.color != undefined) {htmlObj.find('div').last().find('a').css('color', data.color);} ;
      htmlObj.find('div').last().find('a').html(data.title); ''')

  def __str__(self):
    """ String representation of the HTML complex object """
    items = ['<div %s>' % self.strAttr(pyClassNames=['CssDivBox'])]
    items.append(
      '<div %s style="background-color:%s;font-size:%spx"></div><div class="py_csstitle"><a style="text-decoration:none"></a></div></div>' % (
        self.aresObj.cssObj.getClsTag(['CssDivBubble', 'CssTitle']), self.backgroundColor, self.size))
    return "".join(items)


class BlockText(AresHtml.Html):
  """ Python wrapper for a complex HTML object with several div elements

  :example

  """
  __reqCss = ['font-awesome']
  name, category, callFnc, docCategory = 'Block text', 'Text', 'blocktext', 'Preformatted'
  __pyStyle = ['CssTitle', 'CssHrefNoDecoration', 'CssButtonBasic', 'CssText', 'CsssDivBoxMargin']
  mocks = {"text": 'Ares the new Python Web framework', "title": 'RiskLab', 'btext': 'Get Started', 'bUrl': '/getStarted', 'color': 'green'}

  def __init__(self, aresObj, recordSet, color, size, border, width, widthUnit, height, heightUnit):
    super(BlockText, self).__init__(aresObj, recordSet)
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) if size is None else size
    self.color = color if color is not None else self.getColor('baseColor', 2)
    self.css( {'color': self.color, 'padding': '5px', 'width': '%s%s' % (width, widthUnit)})
    if border != 'auto':
      self.css('border', str(border))
    if height is not None:
      self.css('height', '%s%s' % (height, heightUnit))

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("toAresMarkup(text)",
        '''
        text = text.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
        text = text.replace(/\*(.*?)\*/g, "<i>$1</i>");
        text = text.replace(/__(.*?)__/g, "<u>$1</u>");
        text = text.replace(/~~(.*?)~~/g, "<i>$1</i>");
        text = text.replace(/--(.*?)--/g, "<del>$1</del>");
        text = text.replace(/<<(.*?)>>/g, "<a href='$1'>Link</a>");
        return text ; ''')
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      htmlObj.find('div').first().html(data.title) ;
      htmlObj.find('div').last().empty() ;
      var content;
      if (typeof data.text === 'string' || data.text instanceof String) {content = data.text.split("\\n") ;}
      else { content = data.text ; }
      content.forEach(function(line){ htmlObj.find('div').last().append('<p class="py_csstext">' + line + '</a>') ; }) ;
      htmlObj.find('div').last().html(toAresMarkup(data.text));
      if (data.color != undefined) { htmlObj.find('div').last().css('color', data.color) ; } ;
      htmlObj.find("a").html(data.btext) ;
      htmlObj.find("a").attr('href', data.bUrl) ;''')

  def __str__(self):
    """ String representation of the HTML Object """
    pyStyles = [style for style in self.pyStyle if not style in ['CssTitle', 'CssText', 'CssHrefNoDecoration', 'CssButtonBasic']]
    items = ['<div %s>' % self.strAttr(pyClassNames=pyStyles)]
    items.append('<div id="%s_title" %s style="font-size:%spx;text-align:left"><a class="anchorjs-link"></a></div>' % (self.htmlId, self.aresObj.cssObj.getClsTag(['CssTitle']), self.size+3))
    items.append('<div id="%s_p" %s style="color:%s:font-size:%spx;width:100%%;text-justify:inter-word;text-align:justify;"></div>' % (self.htmlId, self.aresObj.cssObj.getClsTag(['CssText']), self.color, self.size))
    if self.vals['btext'] is not None:
      items.append('<a href="#" %s><i></i></a>' % (self.aresObj.cssObj.getClsTag(['CssHrefNoDecoration', 'CssButtonBasic'])))
    items.append('</div>')
    return ''.join(items)


class TextWithBorder(AresHtml.Html):
  """ Python Wrapper to the HTML Block qutoe Bootstrap object


  """
  __pyStyle = ['CssTextWithBorder']
  __reqCss, __reqJs = ['font-awesome'], ['font-awesome']
  name, category, callFnc, docCategory = 'Text with Border and Icon', 'Text', 'textborder', 'Preformatted'
  mocks = {"title": "RiskLab", 'value': "A new Python Web Framework", 'color': 'green', 'icon': 'fab fa-python', 'colorTitle': 'darkgreen'}

  def __init__(self, aresObj, recordSet, width, withUnit, height, heightUnit, size, align):

    super(TextWithBorder, self).__init__(aresObj, recordSet)
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) if size is None else size
    self.align = align
    if not 'colorTitle' in self.vals:
      self.vals['colorTitle'] = self.getColor('baseColor', 2)
    if not 'color' in self.vals:
      self.vals['color'] = self.getColor('baseColor', 0)
    self.css( {'width': '%s%s' % (width, withUnit), "border-color": self.vals['colorTitle'], 'margin-top': '20px', 'font-size': '%spx' % self.size} )
    if height is not None:
      self.css( "height", "%s%s" % (height, heightUnit) )

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      htmlObj.find('legend').html(data.title) ; 
      htmlObj.find('span').html(data.value) ; 
    ''')

  @property
  def jqId(self): return "$('#%s fieldset')" % self.htmlId

  def __str__(self):
    """  String representation of the HTML object """
    item = ['<div %s>' % self.strAttr(pyClassNames=['CssTextWithBorder'])]
    item.append('<fieldset style="color:%s">' % self.vals['color'])
    if 'icon' in self.vals:
      self.vals['align'] = self.align
      item.append('<i class="%(icon)s fa-5x" style="width:100%%;text-align:%(align)s;margin:2px 0 10px 0;color:%(color)s"></i>' % self.vals)
    if 'url' in self.vals:
      item.append('<legend style="font-size:%spx;color:%s"></legend><span></span><br><a style="float:right" href="%s">+ more details</a></fieldset>' % (self.size + 10, self.vals['colorTitle'], self.vals['url']) )
    else:
      item.append('<legend style="font-size:%spx;color:%s"></legend><span></span></fieldset>' % (self.size + 10, self.vals['colorTitle']))
    item.append('</div>')
    return "".join(item)


class Vignet(AresHtml.Html):
  """ Python wrapper for the HTML vignet element

  :example
  aresObj.vignet('title', 24, 'content')
  """
  name, category, callFnc, docCategory = 'Vignet', 'Text', 'vignet', 'Preformatted'
  __pyStyle = ['CssDivBox', 'CssText', 'CssNumberCenter', 'CsssDivBoxMargin']
  __reqCss, __reqJs = ['font-awesome', 'jqueryui'], ['font-awesome', 'jquery']
  mocks = {'title': 'Python', 'number': 100, 'text': 'Ares new Python web framework', 'color': 'green', 'url': 'https://www.python.org/',
           'icon': 'fab fa-python', 'tooltip': 'Python Fondation', 'urlTitle': 'WebSite'}

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit, size, colorTitle):
    super(Vignet, self).__init__(aresObj, recordSet)
    colorTitle = colorTitle if colorTitle is not None else self.getColor('baseColor', 2)
    if not 'color' in self.vals:
      self.vals['color'] = self.getColor('baseColor', 0)
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) if size is None else size
    self.css( {"width": "%s%s" % (width, widthUnit), "height": "%s%s" % (height, heightUnit),
               "padding-left": "5px", "color": colorTitle, "margin-top": "20px"} )

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      if (data.urlTitle != undefined  || data.urlTitle != null) {  htmlObj.find('div').find('p').first().html('<a href="'+ data.urlTitle +'" style="text-decoration:none;color:%(blackColor)s">' + data.title + '</a>'); }
      else { htmlObj.find('div').find('p').first().html(data.title) ;}
      htmlObj.find('div').find('p').eq(2).html(data.value) ;
      if (data.url != undefined || data.url != null) { htmlObj.find('div').find('p').last().html('<a href="'+ data.url +'" style="text-decoration:none;color:%(blackColor)s">' + data.number + '</a>') ; }
      else { htmlObj.find('div').find('p').last().html(FormatNumber(data.number, 0, ',', ',')) ;}
      if (data.tooltip != undefined) {htmlObj.find('div').find('p').last().tooltip( ) ;};
      if (data.text != undefined) {  htmlObj.find('p').last().html(data.text) ;}
      ''' % {"blackColor": self.getColor('greyColor', 8) })

  def figureClick(self, jsData='data'):
    """
    Add on click function to update the number variable if need be
    :return:
    """
    self.aresObj.jsOnLoadFnc.add("""
      $('#%(htmlId)s').find('div').find('p').last().on('click', function (event) {
        var data = %(htmlId)s_data;
        if (data.url != undefined) {data.number++; $(this).html('<a href="'+ data.url +'">' + data.number + '</a>') ; }              
      }) """ % {"htmlId": self.htmlId, 'data': jsData})

  def __str__(self):
    """ Return the String representation of a Vignet """
    self.addGlobalFnc("FormatNumber(n, decPlaces, thouSeparator, decSeparator)", '''
      decPlaces = isNaN(decPlaces = Math.abs(decPlaces)) ? 2 : decPlaces,
      decSeparator = decSeparator == undefined ? "." : decSeparator,
      thouSeparator = thouSeparator == undefined ? "," : thouSeparator,
      sign = n < 0 ? "-" : "",
      i = parseInt(n = Math.abs(+n || 0).toFixed(decPlaces)) + "",
      j = (j = i.length) > 3 ? j % 3 : 0;
      return sign + (j ? i.substr(0, j) + thouSeparator : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thouSeparator) + (decPlaces ? decSeparator + Math.abs(n - i).toFixed(decPlaces).slice(2) : "");
    ''')

    items = ["<div %s>" % (self.strAttr(pyClassNames=['CssDivBox']))]
    tooltip = ' title="%s"' % self.tooltip if self.tooltip is not None else ' '
    if 'icon' in self.vals:
      items.append('<div style="position:relative;float:left;font-size:3em"><i class="%(icon)s"></i></div>' % self.vals)
      items.append('<div ><p style="font-size:%spx;margin-left:50px;font-weight:bold"></p>' % (self.size + 6))
      items.append('<p %s %s data-placement="bottom" style="color:%s;font-size:%spx;margin-left:50px;text-align:center;margin-top:-20px;"></p></div>' % (self.aresObj.cssObj.getClsTag(['CssText']), self.vals.get('tooltip', ''),
                                                                                                     self.vals['color'], self.size + 30))
    else:
      items.append('<div ><p %s style="font-size:%spx;margin-left:50px;font-weight:bold"></p>' % (self.aresObj.cssObj.getClsTag(['CssSubTitle']), self.size + 6))
      items.append('<p %s style="color:%s;font-size:%spx;margin-left:50px;text-align:center;margin-top:-20px;"></p></div>' % (self.aresObj.cssObj.getClsTag(['CssText']), self.vals['color'], self.size + 30))
    items.append('<p %s style="font-size:%spx;margin-top:-10px;"></p></div>' % (tooltip, self.size))
    return "".join(items)


class Delta(AresHtml.Html):
  """

  """
  __pyStyle = ['CssDivNoBorder']
  references = {'progress Bar': 'https://jqueryui.com/progressbar/',
                'Icons': 'https://fontawesome.com/icons?d=gallery'}
  __reqCss, __reqJs = ['font-awesome', 'bootstrap'], ['font-awesome', 'jquery']
  name, category, callFnc, docCategory = 'Delta Figures', 'Text', 'delta', 'Preformatted'
  mocks = {'number': 100, 'prevNumber': 60, 'color': "", 'url': '', 'icon': '', 'tooltip': '', 'thresold1': 100, 'thresold2': 50}

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit, size):
    """

    :param aresObj:
    :param width:
    :param widthUnit:
    :param height:
    :param heightUnit:
    :param size:
    """
    super(Delta, self).__init__(aresObj, recordSet)
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) if size is None else size
    if not 'color' in self.vals:
      self.vals['color'] = self.getColor('baseColor', 0)
    if not 'thresold1' in self.vals:
      self.vals['thresold1'] = 100
    if not 'thresold2' in self.vals:
      self.vals['thresold2'] = 50
    self.css( {"width": "%s%s" % (width, widthUnit), "height": "%s%s" % (height, heightUnit), "color": self.vals['color']})

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
       var htmlId = htmlObj.attr('id') ;
       var variation = 100 * (data.number - data.prevNumber) / data.prevNumber ;
       var warning = ''; var currVal = FormatNumber(data.number, 0, ',', ','); 
       if (variation > data.thresold1) { warning = '<i style="color:%(recColod)s;" title="'+ variation +' increase" class="fas fa-exclamation-triangle"></i>&nbsp;&nbsp;' ;};
       if (data.url != null) { currVal = '<a style="text-decoration:none;color:'+ data.color +'" href="' + data.url+ '">'+ currVal + '</a>' ;}
       $("#"+ htmlId + "_progress").progressbar({value: variation});
       if (variation > data.thresold1){ $("#"+ htmlId + "_progress").children().css({ 'background': 'Red' }); } 
       else if (variation > data.thresold2){ $("#"+ htmlId + "_progress").children().css({ 'background': 'Orange' }); } 
       else{ $("#"+ htmlId + "_progress").children().css({ 'background': 'LightGreen' });}
       htmlObj.find('div').first().html(warning + currVal);
       htmlObj.find('div').last().html('compare to previous number ' + FormatNumber(data.prevNumber, 0, ',', ','));
      ''' % {"recColod": self.getColor('redColor', 2) })

  def __str__(self):
    self.addGlobalFnc("FormatNumber(n, decPlaces, thouSeparator, decSeparator)", '''
          decPlaces = isNaN(decPlaces = Math.abs(decPlaces)) ? 2 : decPlaces,
          decSeparator = decSeparator == undefined ? "." : decSeparator,
          thouSeparator = thouSeparator == undefined ? "," : thouSeparator,
          sign = n < 0 ? "-" : "",
          i = parseInt(n = Math.abs(+n || 0).toFixed(decPlaces)) + "",
          j = (j = i.length) > 3 ? j % 3 : 0;
          return sign + (j ? i.substr(0, j) + thouSeparator : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thouSeparator) + (decPlaces ? decSeparator + Math.abs(n - i).toFixed(decPlaces).slice(2) : "");
      ''')

    return '''<div %(strAttr)s>
      <div style="width:100%%;text-align:right;font-size:%(size)spx;"></div>
      <div id="%(htmlId)s_progress" style="height:10px;color:%(color)s"></div>
      <div style="font-size:10px;font-style:italic;color:%(greyColor)s;padding-bottom:5px;text-align:left"></div>
      </div>''' % {"strAttr": self.strAttr(pyClassNames=self.pyStyle), "size": self.size+12, 'htmlId': self.htmlId, "color": self.vals['color'],
                   "greyColor": self.getColor("greyColor", 4)}

  @staticmethod
  def matchMarkDown(val):
    return True if val.startswith("@delta ") else None

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj=None):
    curr, prev = val[6:].split(':')
    if aresObj is not None:
      getattr(aresObj, cls.callFnc)( {'number': float(curr), 'prevNumber': float(prev)})
    return ["aresObj.%s( {'number': %s, 'prevNumber': %s} )" % (cls.callFnc, float(curr,), float(prev))]

  @classmethod
  def jsMarkDown(self, vals): return "@delta %s:%s" % (vals['number'], vals['prevNumber'])


class DocScript(AresHtml.Html):
  """ Python Wrapper for a Static view of the scripts

  This interface is a bit special in the way it is supposed to interact with the production code.
  Indeed it will:
    - In production read a text file and display the data that will be produced from the system (Python, R, ....)
    - In test mode try to get it from the code directly using a REST Service

  Security checks are done in the script to ensure they are TAGS as open
  """
  docTypes = set(['documentation', 'code'])
  __pyStyle = ['CssDivNoBorder']
  __reqCss, __reqJs = ['font-awesome', 'bootstrap'], ['font-awesome', 'jquery']
  name, category, callFnc, docCategory = 'Script Documentation', 'Text', 'doc', 'Preformatted'
  mocks = ''

  def __init__(self, aresObj, title, scriptName, clssName, functionName, docType, color, size):
    if not docType in self.docTypes:
      raise Exception('The docType %s does not exist' % docType)

    clssName = clssName if clssName is not None else 'NOT_SET'
    super(DocScript, self).__init__(aresObj, {'title': title, 'clssName': clssName, 'functionName': functionName,
                                              'docType': docType, 'scriptName': scriptName.replace('.py', '') })
    self.size = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size
    self.color = self.getColor('textColor', 0) if color is None else color

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      var request = "/reports/doc/"+ data.docType +"/"+ data.scriptName +"/"+ data.clssName +"/" + data.functionName;
      if ( data.functionName == '') { request = "/reports/doc/"+ data.docType +"/" + data.scriptName + "/" + data.clssName; }
      $.post( request, function( data ) { JSON.parse(data).forEach(function(rec) { htmlObj.find('pre').append('<code>' + rec + '</code><br />') ; }) ;}); ''')

  def __str__(self):
    """ Return the String representation of the Script Documentation Standard Component """
    label = "from script <b>%s</b>" % self.vals['scriptName']
    if self.vals['clssName'] != 'NOT_SET':
      label = "%s, class <b>%s</b>" % (label, self.vals['clssName'])
    if self.vals['functionName'] != '':
      label = "%s, function <b>%s</b>" % (label, self.vals['functionName'])
    return '''
      <div %s>
        <div style="color:%s;font-size:%s;font-weight:bold;">%s</div>
        <pre style="padding:5px"></pre>
        <span style="font-style:italic;width:100%%;text-align:right;display:block;margin-top:-15px">%s</span>
      </div> ''' % (self.strAttr(pyClassNames=self.pyStyle), self.color, self.size, self.vals['title'], label)


class Prism(AresHtml.Html):
  """ Python Wrapper to the FONT HTNL Tag """
  references = {'W3C Definition': 'https://www.w3schools.com/tags/tag_font.asp'}
  __reqCss, __reqJs = ['prism'], ['prism', 'jqueryui']
  name, category, callFnc, docCategory = 'Code Viewer', 'Text', 'prism', 'Preformatted'
  mocks = 'print("Hello World")'

  def __init__(self, aresObj, vals, language, size, width, widthUnit, height, heightUnit, isEditable, trimSpaces, align):
    super(Prism, self).__init__(aresObj, vals)
    self.size, self.isEditable = self.aresObj.pyStyleDfl['fontSize'] if size is None else "%spx" % size, isEditable
    self.trimSpaces = trimSpaces
    self.css( {'font-size': self.size, "width": "%s%s" % (width, widthUnit), "height": "%s%s" % (height, heightUnit)} )
    self.addClass('language-%s' % language)
    if align == 'center':
      self.css('margin', 'auto')

  def __str__(self):
    """ Return the String representation of a Text HTML tag onKeyUp="Prism.highlightAll();" """
    copy = self.aresObj.awesome("fas fa-clipboard", tooltip="Copy to clipboard")
    copy.click(
      '''if (window.clipboardData) { window.clipboardData.setData('Text', %(vals)s); } 
         else {
            var $temp = $("<textarea>");
            $("body").append($temp);
            $temp.val(%(vals)s).select();
            document.execCommand("copy");
            $temp.remove();  } ;         
          $('body').append("<div id='info' style='position:fixed;left:50;bottom:10px;z-index:100;background:#293846;padding:10px;color:%(whiteColor)s'>Data copied to clipboard</div>"); 
          $('#info').fadeOut(6000, function() { $('#info').remove() } ) ;
          ''' % {"vals": json.dumps(self.vals), 'whiteColor': self.getColor("greyColor", 0) } )
    lab = self.aresObj.awesome("fas fa-flask", tooltip="Experiment further in a notebook")
    lab.click( self.aresObj.jsSubmitForm( "%s/run/lab/AresLabNoteBook" % self.aresObj._urlsApp['ares-report'], [('content', self.vals)])  )
    if self.trimSpaces:
      content = "".join(['<code style="width:100%%;">%s</code><br />' % line.strip() for line in self.vals.split("\n")])
    else:
      content = "".join(['<code style="width:100%%;">%s</code><br />' % line for line in self.vals.split("\n")])
    return '''
      <div %(strAttr)s> 
        <table style="table-layout: fixed;width:100%%" id="%(htmlId)s_code">
          <tr>
            <td style="width:100%%;overflow:auto;vertical-align:top">
              <div contenteditable="%(isEditable)s" style="width:100%%;overflow:auto;display:block;margin-top:0">
                <pre>%(content)s</pre>%(helper)s
              </div>
            </td>
            <td  style="width:25px;vertical-align:top">
              <div style="height:100%%">%(copy)s %(lab)s</div>
            </td>
          </tr>
        </table>
        <div style="display:inline-block;margin:0;padding:0;width:100%%;text-align:right"><p style="display:inline:block;float:right;width:80px;white-space:nowrap;cursor:pointer" onclick="$('#%(htmlId)s_code').toggle()">[hide / show]</p></div>
      </div>''' % {"strAttr": self.strAttr(), "copy": copy.html(), "isEditable": self.isEditable,
                   "lab": lab.html(),
                   "content": content,
                   "helper": self.helper, "htmlId": self.htmlId}

  @staticmethod
  def matchMarkDownBlock(data):
    return re.match("```", data[0])

  @staticmethod
  def matchEndBlock(data):
    return data.endswith("```")

  @classmethod
  def convertMarkDownBlock(cls, data, aresObj=None):
    language = data[0].replace("```", "").strip()
    if aresObj is not None:
      getattr(aresObj, 'prism')("\n".join(data[1:-1]), language)
    return ["aresObj.prism('%s', '%s')" % ("\n".join(data[1:-1]).replace("'", '"'), language) ]

  @classmethod
  def jsMarkDown(self, vals):
    return ["```", vals, "```"]

  def to_word(self, document):
    from docx.oxml.ns import nsdecls
    from docx.oxml import parse_xml

    table = document.add_table(rows=1, cols=1)
    table.style = 'TableGrid'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "\n%s\n" % self.vals

    shading_elm_1 = parse_xml(r'<w:shd %s w:fill="F4F4F4"/>' % (nsdecls('w')) )
    hdr_cells[0]._tc.get_or_add_tcPr().append(shading_elm_1)


class Formula(AresHtml.Html):
  """ Python Wrapper to the FONT HTNL Tag """
  references = {'W3C Definition': 'https://www.w3schools.com/tags/tag_font.asp'}
  __pyStyle, __reqJs = ['CssText'], ['mathjs']
  name, category, callFnc, docCategory = 'Latex Formula', 'Text', 'formula', 'Preformatted'
  mocks = '$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$'

  def __init__(self, aresObj, text, size, width, widthUnit, color):
    super(Formula, self).__init__(aresObj, text)
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) if size is None else size
    self.color = color if color is not None else self.getColor('greyColor', 8)
    self.css({'color': self.color, 'font-size': self.size, "width": "%s%s" % (width, widthUnit)})
    #self.aresObj.jsGlobal.addJs("MathJax.Hub.Config({tex2jax: {inlineMath: [['$', '$'], ['\\(', '\\)']]}})")

  @property
  def val(self):
    """ Property to get the jquery value of the HTML objec in a python HTML object """
    return '%s.html()' % self.jqId

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''htmlObj.html(data)''')

  def __str__(self):
    """ Return the String representation of a Text HTML tag """
    return '<font %s></font>%s' % (self.strAttr(pyClassNames=self.__pyStyle), self.helper)

  @staticmethod
  def matchMarkDown(val): return True if val.startswith("$$") and val.strip().endswith("$$") else None

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj):
    if aresObj is not None:
      getattr(aresObj, 'formula')(val.strip())
    return ["aresObj.formula('%s')" % val.strip()]

  @classmethod
  def jsMarkDown(self, vals): return vals


class TrafficLight(AresHtml.Html):
  """ Python wrapper for a simple Traffic light object

  Colour is passed as parameter when this object is used in Ares
  """
  name, category, callFnc, docCategory = 'Light', 'Text', 'light', 'Preformatted'
  __pyStyle = ['CsssDivBoxMargin']

  def __init__(self, aresObj, color, label, height, heightUnit, tooltip):
    # Small change to allow the direct use of boolean and none to define the color
    # Those standards will simplify the creation of themes going forward
    if color is None:
      color = 'Orange'
    elif color is True:
      color = 'green'
    elif not color:
      color = 'red'
    super(TrafficLight, self).__init__(aresObj, color, width=height, widthUnit=heightUnit, height=height, heightUnit=heightUnit)
    self.css( {'border-radius': '50px', 'background-color': self.vals, 'display': 'block'} )
    self.addAttr("title", tooltip)
    self.label = label
    if tooltip != "":
      self.aresObj.jsOnLoadFnc.add("%s.tooltip()" % self.jqId)
    self.jsVal = "%s.css('background-color')" % self.jqId

  def jsColor(self, color):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsColor("red")
    :dsc:
      Function to change the color of the component from an event
    :return: The javascript string corresponding to the action of changing the color
    """
    return "%s.css('background-color', '%s')" % (self.jqId, color)

  @property
  def val(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.val
    :dsc:
      Function to return the value of the component
    :return: The javascript string to get the component value
    """
    return self.jsVal

  def __str__(self):
    """ Return the String representation of a Text HTML tag """
    if self.label is not None:
      self.css({'display': 'inline-block'} )
      return '<div style="margin:5px 0"><p style="height:100%%;display:inline-block;padding-right:5px;margin-bottom:2px;font-weight:bold">%s</p><div %s></div>%s</div>' % (self.label, self.strAttr(pyClassNames=self.__pyStyle), self.helper)

    return '<div %s></div>%s' % (self.strAttr(pyClassNames=self.__pyStyle), self.helper)

  @staticmethod
  def matchMarkDown(val): return re.match("-\(\((.*)\)\)-", val)

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj=None):
    if aresObj is not None:
      getattr(aresObj, cls.callFnc)(regExpResult.group(1))
    return ["aresObj.%s('%s')" % (regExpResult.group(1), cls.callFnc)]

  @classmethod
  def jsMarkDown(self, val):
    return "-((%s))-" % val


class TextVignet(AresHtml.Html):
  name, category, callFnc, docCategory = 'Text Vignet', 'Text', 'textvignet', 'Preformatted'
  __pyStyle = ['CssDivNoBorder']
  mocks = {'text': 'This is an example', 'title': 'Title', 'icon': 'fab fa-accusoft'}

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit, size):
    super(TextVignet, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    if not 'color' in self.vals:
      self.vals['color'] = self.getColor('baseColor', 0)
    if not 'colorTitle' in self.vals:
      self.vals['colorTitle'] = self.getColor('baseColor', 3)
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) if size is None else size
    self.css( {'color': self.vals['color'], "padding-left": "5px", "margin-top": "5px", "text-align": "justify", "margin": 'auto'} )

  def __str__(self):
    return '''
      <div %s>
        <div style="font-size:22px;color:%s;width:100%%;text-align:center"><i class="%s" style="display-inline"></i>&nbsp;%s</div>
        %s <br />
        <div style="width:100%%;text-align:right"><a href="%s">+ more details</a></div>
      </div> ''' % (self.strAttr(pyClassNames=self.__pyStyle), self.vals['colorTitle'], self.vals['icon'], self.vals['title'], self.vals['text'], self.vals.get('url', '#'))


class ContentsTable(AresHtml.Html):
  name, category, callFnc, docCategory = 'Contents Table', 'Text', 'contents', 'Preformatted'
  __pyStyle = ['CssDivTableContent']

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit):
    recordSet = [] if recordSet is None else recordSet
    self.indices, self.firstLevel, self.entriesCount, self.extLinks = [], None, 0, {}
    super(ContentsTable, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)

  def add(self, text, level, name=None):
    if self.firstLevel is None:
      self.firstLevel = level

    adjLevel = level - self.firstLevel + 1
    self.indices.append( adjLevel )

    if name is None:
      name = self.entriesCount
    self.vals.append( {'text': text, 'level': adjLevel, 'name': name} )
    self.entriesCount += 1
    return name

  def addExtReport(self, text, level, scriptName, folderName=None, name=None):
    self.extLinks[self.entriesCount] = {"scriptName": scriptName, "folderName": folderName if folderName is not None else self.aresObj.run.report_name}
    self.add(text, level, name)

  def __str__(self):
    entries = []
    for i, v in enumerate(self.vals):
      try:
        v['classname'] = self.addPyCss('CssHrefContentLevel%(level)s' % v)
      except:
        raise Exception("Missing css class CssHrefContentLevel%(level)s" % v)

      if i in self.extLinks:
        v.update( self.extLinks[i] )
        entries.append("<a href='/reports/run/%(folderName)s/%(scriptName)s' class='%(classname)s'>%(text)s</a>" % v)
      else:
        entries.append("<a href='#%(name)s' class='%(classname)s'>%(text)s</a>" % v)
    self.addGlobalFnc("ChangeContents(src, htmlId)", '''
        $("#contents_vals_"+ htmlId).toggle() ;
        if( $("#contents_vals_"+ htmlId).css('display') == 'none') {
          $(src).text("Show") ;
          $("#contents_title_"+ htmlId).css( "text-align", 'left') ;}
        else { $(src).text("Hide") ;$("#contents_title_"+ htmlId).css( "text-align", 'center') ;} 
      ''')
    return '''
      <div %(attr)s>
        <div id='contents_title_%(htmlId)s' style="text-align:center;margin-bottom:10px;font-size:16px;font-weight:bold">Contents [<a href='#' onclick='ChangeContents(this, "%(htmlId)s")' >hide</a>] </div>
        <div id='contents_vals_%(htmlId)s'>%(contents)s</div>
      </div> ''' % {'attr': self.strAttr(pyClassNames=self.__pyStyle), 'contents': "<br />".join(entries), 'htmlId': self.htmlId}
