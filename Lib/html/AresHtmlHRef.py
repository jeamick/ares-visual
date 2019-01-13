#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
import re

from ares.Lib.html import AresHtml
from ares.Lib import AresImports
from ares.Lib.AresImports import requires

# External package required
render_template_string = AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='render_template_string', raiseExcept=False, sourceScript=__file__)


class ExternalLink(AresHtml.Html):
  """ To display a reference to an external website """
  name, category, callFnc, docCategory = 'External link', 'Hyperlink', 'externallink', 'Standard'
  references = {'HyperLink W3C': 'https://www.w3schools.com/TagS/att_a_href.asp'}
  __pyStyle = ['CssDivNoBorder']

  def __init__(self, aresObj, recordSet, height, heightUnit, decoration, newPage, badgeContent):
    super(ExternalLink, self).__init__(aresObj, recordSet)
    if not 'url' in self.vals:
      self.vals['url'] = self.vals['text']
    self.vals['isJs'] = False
    self.decoration, self.newPage, self.badgeContent, self.__url,  = decoration, newPage, badgeContent, {}
    self.url = "/%s" % "http://%s" % self.vals['url'] if not self.vals['url'].startswith("http") else self.vals['url']
    if height is not None:
      self.css('height', '%s%s' % (height, heightUnit))

  def toUrl(self, key, val=None, isPyData=True):
    if val is None and issubclass(key, AresHtml.Html):
      self.__url[key.htmlCode] = "%s: function() { return %s }" % (key.htmlCode, key.val)
      self.vals['isJs'] = True
    else:
      if issubclass(val.__class__, AresHtml.Html):
        self.__url[key] = "%s: function() { return %s }" % (key, val.val)
        self.vals['isJs'] = True
      elif isPyData:
        self.__url[key] = "%s: function() { return %s }" (key, json.dumps(val))
      else:
        self.vals['isJs'] = True
        self.__url[key] = "%s: function() { return %s }" % (key, val)

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    self.jsUpdateDataFnc = '''
      %(htmlId)s_data['params'] = { %(params)s } ;
      %(pyCls)s(%(jqId)s, %(htmlId)s_data) ; 
      ''' % {'pyCls': self.__class__.__name__, 'jqId': self.jqId, 'htmlId': self.htmlId, 'htmlCode': json.dumps(self.htmlCode),
             'jsVal': self.val, 'params': ", ".join(self.__url.values())}
    self.aresObj.jsOnLoadFnc.add(self.jsUpdateDataFnc)

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' 
      if (data.icon != undefined) { htmlObj.append('<i class="'+ data.icon +'"></i>&nbsp;&nbsp;')}
      if (data.color != undefined) { htmlObj.css('color', data.color) ;}
      if (data.bold != undefined) { htmlObj.css('font-weight', 'bold') ;}
      if (data.size != undefined) { htmlObj.css('font-size', data.size + 'px') ;}
      htmlObj.append(data.text); 
      if (!data.isJs) {htmlObj.attr('href', data.url)}
      else {
        htmlObj.on('click', function(event) { 
          var urlParts = [];
          for(var key in data.params){urlParts.push(key + "=" + data.params[key]())}
          htmlObj.attr('href', data.url + "?" + urlParts.join('&'))
        }) ;
      } ''', 'Javascript Object builder')

  @property
  def jqId(self): return "$('#%s a')" % self.htmlId

  def __str__(self):
    """ Return the HTML representation of the hyperlink object """
    extraCss = 'style="text-decoration:none"' if not self.decoration else ''
    target = 'target="_blank"' if self.newPage else ''
    badge = self.aresObj.badge(self.badgeContent) if self.badgeContent is not None else ''
    return '<div %s><a %s %s></a>%s%s</div>' % (self.strAttr(pyClassNames=self.pyStyle), target, extraCss, badge, self.helper)

  @staticmethod
  def matchMarkDown(val):
    result = re.findall("\[([a-zA-Z 0-9]*)\]\(http([:a-zA-Z\/\.\ 0-9]*)\)", val)
    if not result:
      result = re.findall('\[([a-zA-Z 0-9]*)\]\(<a href\=\"http://([:a-zA-Z/.0-9]*)\">', val)
    return result

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj):
    print(regExpResult)
    for name, url in regExpResult:
      val = val.replace("[%s](http%s)" % (name, url), "aresObj.externallink('%s', 'http%s')" % (name, url))
      if aresObj is not None:
        getattr(aresObj, 'link')({'url': url, 'text': name})
    return [val]

  @classmethod
  def jsMarkDown(cls, vals): return "[%s](%s)" % (vals['text'], vals['url'])

  def to_word(self, document):
    """
    :category:
    :type:
    :dsc:

    """
    # Will automatically add the external library to be able to use this module
    ares_docx = requires("docx", reason='Missing Package', install='python-docx', autoImport=True, sourceScript=__file__)

    p = document.add_paragraph()
    hyperlink = ares_docx.oxml.shared.OxmlElement('w:hyperlink')
    r_id = p.part.relate_to(self.vals['url'], ares_docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink.set(ares_docx.oxml.shared.qn('r:id'), r_id, )
    new_run = ares_docx.oxml.shared.OxmlElement('w:r')
    new_run.append( ares_docx.oxml.shared.OxmlElement('w:rPr') )
    new_run.text = self.vals['text']
    hyperlink.append(new_run)
    p._p.append(hyperlink)

  def to_xls(self, workbook, worksheet, cursor):
    worksheet.write_url(cursor['row'], 0, self.vals['url'], string=self.vals['text'])
    cursor['row'] += 2


class Link(AresHtml.Html):
  """ Python interface to the common Hyperlink """
  reqCss, reqJs = ['bootstrap', 'font-awesome'], ['jquery', 'font-awesome']
  __pyStyle = ['CssHrefNoDecoration', 'CssDivNoBorder']
  name, category, callFnc, docCategory = 'Internal link', 'Hyperlink', 'link', 'Standard'

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit, align, decoration, badgeContent):
    super(Link, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    if self.vals['url'].startswith("#"): # Internal anchor in the page
      self.vals['url'] = self.vals['url']
    elif not self.vals['url'].startswith("/"):
      self.vals['url'] = "%s" % self.vals['url']
    self.vals['isJs'] = False
    self.decoration, self.badgeContent, self.__url = decoration, badgeContent, {}
    self.css({'display': 'inline-block', 'padding': '0px 5px', 'text-align': align})

  def toUrl(self, key, val=None, isPyData=True):
    if val is None and issubclass(key, AresHtml.Html):
      self.__url[key.htmlCode] = "%s: function() { return %s }" % (key.htmlCode, key.val)
      self.vals['isJs'] = True
    else:
      if issubclass(val.__class__, AresHtml.Html):
        self.__url[key] = "%s: function() { return %s }" % (key, val.val)
        self.vals['isJs'] = True
      elif isPyData:
        self.__url[key] = "%s: function() { return %s }" (key, json.dumps(val))
      else:
        self.vals['isJs'] = True
        self.__url[key] = "%s: function() { return %s }" % (key, val)

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    self.jsUpdateDataFnc = '''
      %(htmlId)s_data['params'] = {%(params)s}; %(pyCls)s(%(jqId)s, %(htmlId)s_data) ; 
      ''' % {'pyCls': self.__class__.__name__, 'jqId': self.jqId, 'htmlId': self.htmlId, 'htmlCode': json.dumps(self.htmlCode),
             'jsVal': self.val, 'params': ", ".join(self.__url.values())}
    self.aresObj.jsOnLoadFnc.add(self.jsUpdateDataFnc)

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' 
      if (data.icon != undefined) {htmlObj.append('<i class="'+ data.icon +'"></i>&nbsp')}
      if (data.color != undefined) {htmlObj.css('color', data.color)}
      htmlObj.append(data.text); 
      if (!data.isJs) {htmlObj.attr('href', data.url)}
      else {
        htmlObj.on('click', function(event) { 
          var urlParts = [];
          for(var key in data.params){urlParts.push(key + "=" + data.params[key]())}
          htmlObj.attr('href', data.url + "?" + urlParts.join('&'))
        })} ''', 'Javascript Object builder')

  @property
  def jqId(self): return "$('#%s a')" % self.htmlId

  def __str__(self):
    """ """
    extraCss = 'style="margin:auto;display:inline-block"' if not self.decoration else ''
    badge = self.aresObj.badge(self.badgeContent) if self.badgeContent is not None else ''
    return '<div %s><a href="" %s></a>%s%s</div>' % (self.strAttr(pyClassNames=self.pyStyle), extraCss, badge, self.helper)

  @staticmethod
  def matchMarkDown(val): return re.findall("\[([a-zA-Z 0-9]*)\]\(/([:a-zA-Z\/\.\ 0-9]*)\)", val)

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj):
    for name, url in regExpResult:
      val = val.replace("[%s](/%s)" % (name, url), "aresObj.link('%s', '/%s')" % (name, url))
      if aresObj is not None:
        getattr(aresObj, 'link')({'url': "/%s" % url, 'text': name})
    return [val]

  @classmethod
  def jsMarkDown(cls, vals): return "[%s](%s)" % (vals['text'], vals['url'])

  def to_word(self, document):
    """
    :category:
    :type:
    :dsc:

    """

    # Will automatically add the external library to be able to use this module
    ares_docx = requires("docx", reason='Missing Package', install='python-docx', autoImport=True)

    p = document.add_paragraph()
    hyperlink = ares_docx.oxml.shared.OxmlElement('w:hyperlink')
    r_id = p.part.relate_to(self.vals['url'], ares_docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink.set(ares_docx.oxml.shared.qn('r:id'), r_id, )
    new_run = ares_docx.oxml.shared.OxmlElement('w:r')
    new_run.append( ares_docx.oxml.shared.OxmlElement('w:rPr') )
    new_run.text = self.vals['text']
    hyperlink.append(new_run)
    p._p.append(hyperlink)

  def to_xls(self, workbook, worksheet, cursor):
    worksheet.write_url(cursor['row'], 0, self.vals['url'], string=self.vals['text'])
    cursor['row'] += 2
