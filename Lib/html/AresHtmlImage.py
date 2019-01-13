#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import re
import os

from ares.Lib.html import AresHtml
from ares.Lib import AresImports

# External package required
render_template_string = AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='render_template_string', raiseExcept=False, sourceScript=__file__)


class Figure(AresHtml.Html):
  name, category, callFnc, docCategory = 'MatPlotLin Figure', 'Image', 'img', 'Standard'

  def __init__(self, aresObj, matPlotLibFig, htmlCodes, position, width, widthUnit, height, heightUnit, fixedName):
    fileName = []
    if htmlCodes is not None:
      for htmlCode in htmlCodes:
        fileName.append(AresHtml.cleanData(aresObj.http.get(htmlCode, '')))
      self.path = render_template_string("{{ url_for('static', filename='images/users/%s_%s%s_%s.png') }}" % (aresObj.run.report_name, aresObj.run.script_name, fixedName, "_".join(fileName)))
    else:
      self.path = render_template_string("{{ url_for('static', filename='images/users/%s_%s%s.png') }}" % (aresObj.run.report_name, aresObj.run.script_name, fixedName))
    directory = os.path.dirname(os.path.abspath(".%s" % self.path))
    if not os.path.exists(directory):
      os.makedirs(directory)
    if not os.path.exists(".%s" % self.path):
      matPlotLibFig.savefig(".%s" % self.path)
    super(Figure, self).__init__(aresObj, self.path, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.position = position
    self.css( {'text-align': self.position, 'display': 'inline-block'} )

  def __str__(self):
    """ Return the HTML representation of a Tabular object """
    return '<div %s><img src="%s" style="max-height:100%%;max-width:100%%;display:block;margin:0 auto;clear:both;" /></div>%s' % (self.strAttr(pyClassNames=self.pyStyle), self.path, self.helper)


class Image(AresHtml.Html):
  """ Python wrapper for a simple image element
  :category: HTML Component
  :rubric: PY
  :dsc:
    Main class to add an image to the page. By default the image has to be saved in the static repository of the server.
    It is possible to supply a path in order to define a specific path
  :example: aresObj.img('sample_img.jpg')
  """
  references = {'Image W3C': 'https://www.w3schools.com/bootstrap/bootstrap_ref_css_images.asp',
                'Border Style W3C': 'https://www.w3schools.com/cssref/css3_pr_border-radius.asp'}
  __pyStyle = ['CssImgBasic']
  name, category, callFnc, docCategory = 'Picture', 'Image', 'img', 'Standard'

  def __init__(self, aresObj, image, position, htmlCode, folder, width, widthUnit, height, heightUnit):
    if folder is None:
      self.path = render_template_string("{{ url_for('static', filename='%s') }}" % image).replace("/%s" % image, "")
    else:
      self.path = "/img/%s/%s" % (aresObj.run.report_name, folder)
    super(Image, self).__init__(aresObj, image, code=htmlCode, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.vals = {'path': self.path, 'image': self.vals}
    self.css({'text-align': position})

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty();
      if (data.path == undefined) {data.path = "%(imgPath)s"}
      htmlObj.append("<img style='height:auto;max-height:100%;max-width:100%;display:inline-block;position:relative;' src=\'" + data.path + "/images/" + data.image + "\' />") ''',
                      'Javascript Object builder')

  @property
  def val(self): return '$("#%s img").prop("src")' % self.htmlId

  def __str__(self):
    """ Return the HTML representation of a Tabular object """
    return '<div %s></div>%s' % (self.strAttr(pyClassNames=self.pyStyle), self.helper)

  @staticmethod
  def matchMarkDown(val): return re.findall("!\[([a-zA-Z 0-9]*)\]\(([:a-zA-Z \-\"/.0-9]*)\)", val)

  @classmethod
  def convertMarkDown(cls, val, regExpResult, aresObj=None):
    for name, image in regExpResult:
      val = val.replace("![%s](%s)" % (name, image), "aresObj.img('%s')" % image)
      if aresObj is not None:
        getattr(aresObj, 'img')(image)
    return [val]

  @classmethod
  def jsMarkDown(cls, vals):
    return "![alt text](%s/images/%s)" % (vals['path'], vals['image'])


class AnimatedImage(AresHtml.Html):
  """ Python Wrapper for an animated picture element

  :example
  aresObj.animatedimg('sample_img.jpg').display({'title': 'Title', 'text': "Content", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"})
  """

  # List with all the CSS Style to be applied to this component
  # This should never be updated, please use the variable without the double underscores intead
  __pyStyle = ['CssImg', 'CssImgAInfo', 'CssImgMask', 'CssImgH2', 'CssImgParagraph', 'CssContent', 'CssView']
  references = {'Example': 'https://tympanus.net/Tutorials/OriginalHoverEffects/'}
  cssCls = ['view']
  name, category, callFnc, docCategory = 'Animated Picture', 'Image', 'animatedimg', 'Advanced'
  __reqCss, __reqJs = ['bootstrap', 'font-awesome'], ['bootstrap', 'font-awesome', 'jquery']

  def __init__(self, aresObj, recordSet, width, widthUnit, height, heightUnit):
    super(AnimatedImage, self).__init__(aresObj, recordSet, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.vals['path'] = render_template_string("{{ url_for(\'static\',filename=\'%s\') }}" % self.vals['image']).replace("/%s" % self.vals['image'], "")
    self.width = width

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' 
      if (data.path == undefined) { data.path = data.path ; }
      htmlObj.find('img').attr('src', data.path + "/images/" + data.image) ;
      htmlObj.find('div').find('h2').html(data.title); htmlObj.find('div').find('p').html(data.text); htmlObj.find('a').attr('href', data.url); ''',
                      'Javascript Object builder')

  def __str__(self):
    """ Return the String represation of the HTML Image component """
    return '<div %s><img /><div class="mask"><h2></h2><p></p><a class="info">Enter</a></div></div>' % self.strAttr(pyClassNames=self.pyStyle)


class ImgCarrousel(AresHtml.Html):
  """ Python Wrapper for a Img carrousel element

  :example
  aresObj.carrousel([{'image': 'risklab-dashboard.PNG', 'title': 'designer'}, {'image': 'saturn-dashboard.PNG', 'title': 'Dashboard'}])
  """
  __pyStyle = ['CssCarrousel', 'CssCarrouselImg', 'CssCarrouselLi', 'CssCarrouselH2', 'CssDivLabelPoint', 'CssDivBoxCenter']
  references = {'Example': 'https://www.cssscript.com/basic-pure-css-slideshow-carousel/'}
  name, category, callFnc, docCategory = 'Picture Carrousel', 'Image', 'carrousel', 'Advanced'

  def __init__(self, aresObj, images, width, widthUnit, height, heightUnit):
    self.path = render_template_string("{{ url_for(\'static\',filename=\'%s\') }}" % images[0]['image']).replace("/%s" % images[0]['image'], "")
    for rec in images:
      if not 'path' in rec:
        rec['path'] = self.path
    super(ImgCarrousel, self).__init__(aresObj, images, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.css( {'padding-top': '20px', 'display': 'block'} )

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, '''
      var i = 0 ;
      var htmlId = htmlObj.attr('id') ;
      data.forEach(function(rec){
        if (rec.path == undefined) { rec.path = "%(imgPath)s" ; };
        if ( i == 0 ) {
          htmlObj.append( '<li style="display:inline-block;" id="'+ htmlId +'_picture_' + i + '"><img style="width:100%%;height:auto" src="' + rec.path + '/images/' + rec.image + '" /><h2>' + rec.title + '</h2></li>' ) ;
          $('#'+ htmlId +'_bullets').append( "<label style='background:%(color)s' for='" + i + "' name='img-selector'></label>" ) ;
        } else {  
          htmlObj.append( '<li style="display:none" id="'+ htmlId +'_picture_' + i + '"><img style="width:100%%;height:auto" src="' + rec.path + '/images/' + rec.image + '" /><h2>' + rec.title + '</h2></li>' ) ;
          $('#'+ htmlId +'_bullets').append( "<label for='" + i + "' name='img-selector'></label>" ) ;}
      i = i + 1 ; }) ;''' % {'imgPath': self.path, 'color': self.getColor('baseColor', 7)}, 'Javascript Object builder')

  def __str__(self):
    """ String representation of the Carrousel element """
    items = ['<ul %s></ul>' % self.strAttr(pyClassNames=['CssCarrousel', 'CssCarrouselImg', 'CssCarrouselLi', 'CssCarrouselH2'])]
    items.append('<div id="%s_bullets" %s></div>' % (self.htmlId, self.aresObj.cssObj.getClsTag(["CssDivBoxCenter", "CssDivLabelPoint"])))
    self.aresObj.jsOnLoadFnc.add('''
      $("label[for][name=img-selector]").click(function() {
        for (var i=0; i < %(count)s; i++) {$('#%(htmlId)s_picture_' + i ).css('display', 'none') ;}
        $("label[for][name=img-selector").css('background', '%(grey)s') ;
        $('#%(htmlId)s_picture_' + parseInt( $(this).attr('for') )).css('display', 'inline-block') ; 
        $("label[for='"+ $(this).attr('for') + "'][name=img-selector").css('background', '%(color)s') ; }) ;
    ''' % {'htmlId': self.htmlId, 'count': len(self.vals), 'color': self.getColor('baseColor', 7), 'grey': self.getColor('greyColor', 2)})
    return "".join(items)


class ImgGrid(AresHtml.Html):
  """ Python Wrapper for a row of animated Images

  :example
  aresObj.gridImg(aresData=[
    {'title': 'Title', 'text': "Firefox ne peut etablir de connexion avec le serveur a l adresse 127.0.0.1:5000", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"},
    {'title': 'Title', 'text': "Firefox ne peut etablir de connexion avec le serveur a l adresse 127.0.0.1:5000", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"},
    {'title': 'Title', 'text': "Firefox ne peut etablir de connexion avec le serveur a l adresse 127.0.0.1:5000", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"},
    {'title': 'Title', 'text': "Firefox ne peut etablir de connexion avec le serveur a l adresse 127.0.0.1:5000", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"},
    {'title': 'Title', 'text': "Firefox ne peut etablir de connexion avec le serveur a l adresse 127.0.0.1:5000", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"},
    {'title': 'Title', 'text': "Firefox ne peut etablir de connexion avec le serveur a l adresse 127.0.0.1:5000", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"},
    {'title': 'Title', 'text': "Firefox ne peut etablir de connexion avec le serveur a l adresse 127.0.0.1:5000", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"},
    {'title': 'Title', 'text': "Firefox ne peut etablir de connexion avec le serveur a l adresse 127.0.0.1:5000", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"}],

    title='Youpi')
  """
  __reqCss, __reqJs = ['bootstrap', 'font-awesome'], ['bootstrap', 'font-awesome', 'jquery']
  __pyStyle = ['CssImg', 'CssImgAInfo', 'CssImgMask', 'CssImgH2', 'CssImgParagraph', 'CssContent', 'CssView']
  unit, row = 'px', 6

  def __init__(self, aresObj, aresData, title, width, widthUnit, height, heightUnit):
    """ Instantiate the Grid of Images components. By default 6 images per row

    :param aresObj: The Ares.py object, the report
    :param aresData: The python recordSet for this HTML component
    :param width: the width in pixel
    :param cssCls: (optional) the CSS static classes - CSS Level 4
    """
    for img in aresData:
      img['path'] = render_template_string("{{ url_for(\'static\',filename=\'%s\') }}" % img['image']).replace("/%s" % img['image'], "")
      img['url'] = img['url'] if 'url' is  img else '#'
    self.width, self.title = width, title
    super(ImgGrid, self).__init__(aresObj, aresData, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' htmlObj.empty() ;
      var table = $('<table></table>') ;
      var tr = $('<tr>'); var count = 0 ;
      data.forEach(function(item){
        if (item.text == undefined) {item.text = ''; }
        var td = $('<td></td>') ;
        var divItem = $('<div %(cssCls)s style="width:%(width)s%(unit)s;height:auto;display:inline;"></div>') ;
        divItem.append('<img src="'+ item.path + '/images/' + item.image+ '" />') ;
        divItem.append('<div class="mask"><h2>' + item.title + '</h2><p class="content">' + item.text + '</p><a class="info" href="' + item.url + '">Enter</a></div>'); ;
        td.append(divItem) ;
        tr.append(td) ;
        count = count + 1 ;
        if (count %% %(row)s == 0) { table.append(tr); tr = $('<tr>');}
      }); table.append(tr); htmlObj.append(table) ;
      ''' % {'cssCls': self.aresObj.cssObj.getClsTag(self.pyStyle), 'row': self.row, 'width': self.width, 'unit': self.unit,},
                      'Javascript Object builder')

  def __str__(self):
    """ Write the String main component in the page """
    return "<div><a class='anchorjs-link' style='font-size:%s;color:%s;font-weight:bold;'>%s</a><div %s style='display:inline;'></div></div>" % (self.aresObj.pyStyleDfl['headerFontSize'], self.getColor('baseColor', 2), self.title, self.strAttr())


class Icon(AresHtml.Html):
  """ Wrapper for the HTML awesome icons """
  references = {'W3C Definition': 'https://fontawesome.com/icons?m=free'}
  __reqCss, __reqJs = ['font-awesome'], ['font-awesome']
  __pyStyle = ['CssDivBoxCenter']
  name, category, callFnc, docCategory = 'Icon', 'Image', 'icon', 'Standard'
  mocks = {'icon': 'fab fa-python', 'sizeIcon': 1, "url": "https://fontawesome.com/icons?d=gallery&m=free"}

  def __init__(self, aresObj, recordSet, marginTop):
    if not isinstance(recordSet, dict):
      recordSet = {"icon": recordSet}
    super(Icon, self).__init__(aresObj, recordSet)
    self.stack = None # variable used to stack two awesome icons
    if not 'sizeIcon' in self.vals:
      self.vals['sizeIcon'] = 1
    self.css( {'margin-top': '%spx' % marginTop})

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    self.aresObj.jsOnLoadFnc.add("%(jsId)s.attr('class', ''); %(jsId)s.addClass('%(icon)s fa-%(sizeIcon)sx')" % {'jsId': self.jqId, 'icon': self.vals['icon'], 'sizeIcon': self.vals['sizeIcon']} )

  def onDocumentLoadFnc(self): return True

  def jsUpdate(self, data=None):
    """  Return some special Javascript code to update the HTML object """
    if data is None:
      # In this case we assume that we are in a javascript method and the javascript will produce the relevant data
      return self.aresObj.jsOnLoadFnc.add('%s.addClass(data[0] + ' ' + data[1])' % self.jqId)

    content = data if isinstance(data, (tuple, list)) else (data, 1)
    # Python know before the completion of the report that the call will be required
    return self.aresObj.jsOnLoadFnc.add("%s.attr('class', ''); %s.addClass('%s fa-%sx')" % (self.jqId, self.jqId, content[0], content[1]))

  @property
  def jqId(self): return "$('#%s i')" % self.htmlId

  def __str__(self):
    """ Return the String representation of a line tag """
    if self.stack is not None:
      # aresObj.icon("fas fa-file").stack = {"icon": "fab fa-python", "class": "fa-stack-1x fa-inverse"}
      # https://fontawesome.com/how-to-use/on-the-web/styling/stacking-icons
      return '''
        <span class="fa-stack fa-2x">
          <i class="%(icon)s fa-stack-%(sizeIcon)sx"></i>
          <i class="%(icon2)s %(clss2)s"></i>
        </span>
        ''' % {"strAttr": self.strAttr(pyClassNames=self.pyStyle), 'icon': self.vals['icon'], "sizeIcon": self.vals['sizeIcon'], "icon2": self.stack['icon'], 'clss2': self.stack.get('class', '') }

    return '<div %s><i style="cursor:pointer" aria-hidden="true" class="%s fa-%sx"></i></div>' % (self.strAttr(pyClassNames=self.pyStyle), self.vals['icon'], self.vals['sizeIcon'])


class Emoji(AresHtml.Html):
  """

  """
  inReport = False
  name, category, callFnc, docCategory = 'Emoji', 'Image', 'emoji', 'Standard'
  mocks = 'heart_eyes'
  references = {'Source code': 'https://github.com/wedgies/jquery-emoji-picker'}

  def __init__(self, aresObj, iconName, marginTop):
    """

    :param aresObj:
    :param iconName:
    :param marginTop:
    """
    super(Emoji, self).__init__(aresObj, iconName)
    self.vals.lower().replace('.png', '')
    self.css( {'margin-top': '%spx' % marginTop} )

  def __str__(self):
    return '<img src="/static/images/emojis/%s.png" style="width:25px;height:auto"/>' % self.vals


class Badge(AresHtml.Html):
  inReport = False
  name, category, callFnc, docCategory = 'Badge', 'Image', 'badge', 'Standard'
  references = {'Bootstrap Badges': 'https://getbootstrap.com/docs/4.0/components/badge/'}
  __reqCss, __reqJs = ['font-awesome'], ['bootstrap']
  mocks = 'New'

  def __init__(self, aresObj, text, backgroundColor, color):
    super(Badge, self).__init__(aresObj, text)
    color = 'white' if color is None else color
    backgroundColor = 'red' if backgroundColor is None else backgroundColor
    self.css( {'background-color': backgroundColor} )

  def __str__(self):
    return '&nbsp;<span class="badge" %s>%s</span>' % (self.strAttr(withId=False), self.vals)
