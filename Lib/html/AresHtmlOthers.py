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
render_template_string = AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='render_template_string', raiseExcept=False, sourceScript=__file__)


class Hr(AresHtml.Html):
  """ HTML object for the HR tags

  :example
  aresObj.hr()
  """
  name, category, callFnc, docCategory = 'Line delimiter', 'Others', 'hr', 'Standard'
  __pyStyle = ['CssHr']
  references = {'W3C Definition': 'https://www.w3schools.com/tags/tag_hr.asp'}

  def __init__(self, aresObj, color, count, size, backgroundColor, height, heightUnit, align):
    super(Hr, self).__init__(aresObj, count, height=height, heightUnit=heightUnit)
    if color is not None:
      self.css('color', color)
    if align == "center":
      self.css('margin', "auto")
    self.size, self.backgroundColor = size, backgroundColor if backgroundColor is not None else self.aresObj.getColor('greyColor', 2)

  def __str__(self):
    hr = '<hr style="height:%spx;background-color:%s">' % (self.size, self.backgroundColor) if self.size is not None else '<hr style="background-color:%s" />' % self.backgroundColor
    return '<div %s>%s</div>' % (self.strAttr(pyClassNames=self.pyStyle), "".join(self.vals * [hr]))

  @staticmethod
  def matchMarkDown(val): return True if val.strip() == '***' else None

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj=None):
    if aresObj is not None:
      getattr(aresObj, cls.callFnc)()
    return ["aresObj.%s()" % cls.callFnc]

  @classmethod
  def jsMarkDown(self, vals): return "***"

  def to_word(self, document):
    document.add_paragraph("_________________________________")


class Newline(AresHtml.Html):
  """ Python Wrapper to the HTML BR tag

  :example
  aresObj.newline(count=2)
  """
  references = {'W3C Definition': 'https://www.w3schools.com/tags/tag_br.asp'}
  name, category, callFnc, docCategory = 'New line', 'Others', 'newline', 'Standard'

  def html(self):
    """ Return the String representation of a new line tag """
    return "".join(['<br />' for i in range(self.vals)])

  @staticmethod
  def matchMarkDown(val): return True if val.strip() == '' else None

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj=None):
    if aresObj is not None:
      getattr(aresObj, cls.callFnc)()
    return ["aresObj.%s()" % cls.callFnc]

  @classmethod
  def jsMarkDown(self, vals): return ""

  def to_word(self, document):
    document.add_page_break()


class Stars(AresHtml.Html):
  """

  """
  references = {'W3C Definition': 'https://www.w3schools.com/howto/howto_css_star_rating.asp'}
  name, category, callFnc, docCategory = 'Stars', 'Others', 'stars', 'Standard'
  __reqCss, __reqJs = ['font-awesome'], ['font-awesome']

  def __init__(self, aresObj, count, color):
    super(Stars, self).__init__(aresObj, count)
    self.color = self.getColor("greenColor", 0) if color is None else color

  def html(self):
    """ Return the String representation of a new line tag """
    stars = []
    for i in range(5):
      if i < self.vals:
        stars.append('<span class="fa fa-star" style="color:%s"></span>' % self.color)
      else:
        stars.append('<span class="fa fa-star"></span>')
    return "".join(stars)


class Help(AresHtml.Html):
  """ Python wrapper for the HTML help component

  :example
  aresObj.help('Youpiiiii')
  """
  __reqCss, __reqJs = ['font-awesome'], ['font-awesome', 'jquery']
  name, category, callFnc, docCategory = 'Info', 'Text', 'help', 'Standard'
  references = {'Icons': 'https://fontawesome.com/icons/question-circle?style=solid',
                'Jquery Tooltips': 'https://api.jqueryui.com/tooltip/'}

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    self.aresObj.jsOnLoadFnc.add('%(jqId)s.attr("title", %(jsVal)s); %(jqId)s.tooltip() ;' % {"jqId": self.jqId, "jsVal": self.jsVal} )

  def onDocumentLoadFnc(self): return True

  def __str__(self):
    """ Return the String representation of a help HTML item """
    return '<div id="%s" style="width:10px"><i class="fas fa-question-circle"></i></div>' % self.htmlId

  def to_word(self, document):
    pass


class Media(AresHtml.Html):
  """ Python wrapper for the HTML media player component

  """
  references = {'W3C Definition': 'https://www.w3schools.com/html/html5_video.asp'}
  name, category, callFnc, docCategory = 'Video', 'Image', 'media', 'Advanced'

  def __init__(self, aresObj, video, width, widthUnit, height, heightUnit):
    self.path = render_template_string("{{ url_for('static', filename='%s') }}" % video).replace("/%s" % video, "")
    super(Media, self).__init__(aresObj, video, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.vals = {'path': self.path, 'video': self.vals}

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      htmlObj.empty(); htmlObj.append("<source src=\'" + data.path + "/video/" + data.video + "\' type='video/mp4'/>")''',
                      'Javascript Object builder')

  def __str__(self):
    """ The html representation of the component """
    return '''<div><video %s controls></video></div>''' % self.strAttr(pyClassNames=self.pyStyle)


class Delimiter(AresHtml.Html):
  """

  """
  inReport = False
  name, category, callFnc, docCategory = 'Border Delimiter', 'Others', 'delimiter', 'Standard'

  def __init__(self, aresObj, size, color):
    super(Delimiter, self).__init__(aresObj, size)
    color = color if color is not None else 'grey'
    self.css( {'display': 'inline-block', 'width': '%spx' % size, 'background-color': color} )
    self.htmlCode = "delimiter_%s" % id(self)

  def change(self, val): pass

  def __str__(self):
    """ The html representation of the component """
    return '<div %s>&nbsp</div>' % self.strAttr(pyClassNames=self.pyStyle)

  def to_word(self, document):
    document.add_paragraph(" ")


class CountDownDate(AresHtml.Html):
  """
  :category: HTML Component
  :rubric: HTML
  :example: aresObj.countdown('2018-07-23')
  :dsc:
      Add a countdown to the page and remove the content if the page has expired.
  :link W3C Documentation: https://www.w3schools.com/howto/howto_js_countdown.asp
  """
  name, category, callFnc, docCategory = 'Countdown', 'Others', 'countdown', 'Standard'
  references = {
    'Javascript Date': 'https://www.w3schools.com/js/js_date_methods.asp',
    'W3C Definition': 'https://www.w3schools.com/howto/howto_js_countdown.asp'}

  def __init__(self, aresObj, date, timeInMilliSeconds, color, width, widthUnit, height, heightUnit, htmlCode):
    super(CountDownDate, self).__init__(aresObj, date, code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    color = color if color is not None else self.getColor("greyColor", 0)
    self._jsStyles = {"delete": True}
    self.timeInMilliSeconds = timeInMilliSeconds
    self.css( {'display': 'inline-block', 'color': color, 'padding': '5px', 'background-color': self.getColor("blueColor", 2)} )

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data, jsStyles)" % self.__class__.__name__, ''' 
      var splitDt = data.split("-") ; 
      var endDate = new Date(splitDt[0], parseInt(splitDt[1])-1, splitDt[2]) ;
      var now = new Date().getTime();
      var distance = endDate.getTime() - now;
      
      var days = Math.floor(distance / (1000 * 60 * 60 * 24));
      var hours = Math.floor((distance %% (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var minutes = Math.floor((distance %% (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance %% (1000 * 60)) / 1000);
      
      htmlObj.html("Report available for: <b>" + days + "d " + hours + "h " + minutes + "m " + seconds + "s </b><a style='color:white;margin-left:10px;font-style:italic;' href='/reports/run/%(report_name)s/%(script_name)s'>Live report</a>" ); 
      if ( (distance < 0) && (jsStyles.delete)) {
        clearInterval(htmlObj.attr('id') + "_interval" );
        $("#ares_page_content").html( "DOCUMENT EXPIRED - validity date: " + data );
      }
    ''' % {"report_name": self.aresObj.run.report_name, "script_name": self.aresObj.run.script_name}, 'Javascript Object builder')

  def onDocumentReady(self):
    self.jsUpdateDataFnc = '''var %(htmlId)s_interval = setInterval( 
      function() { %(pyCls)s(%(jqId)s, %(htmlId)s_data, %(jsStyles)s ) }, 
        %(timeInMilliSeconds)s); ''' % {'htmlId': self.htmlId, 'pyCls': self.__class__.__name__, 'jqId': self.jqId,
                                        "jsStyles": json.dumps(self._jsStyles), 'timeInMilliSeconds': self.timeInMilliSeconds}
    self.aresObj.jsOnLoadFnc.add(self.jsUpdateDataFnc)

  def __str__(self):
    """ The html representation of the component """
    return '<div %s>&nbsp;</div>' % self.strAttr(pyClassNames=self.pyStyle)

