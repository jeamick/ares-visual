#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
import logging


from ares.Lib.html import AresHtml
from ares.Lib import AresImports

# External package required
render_template_string = AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='render_template_string', raiseExcept=False, sourceScript=__file__)


class HtmlNavBar(AresHtml.Html):
  __reqCss, __reqJs = ['bootstrap', 'font-awesome'], ['bootstrap', 'font-awesome']
  lenght = 45
  name, category = 'Nav Bar', 'System'

  def __init__(self, aresObj, value, color, selected, size, breadcrum, logo, logoLink, backgroundColor):
    self.selected, self.extraLinks, self.breadcrum, self.logo = selected, None, breadcrum, logo
    aresObj.marginTop, self.categories, self.definedOrder = self.lenght, {}, ['Report', 'Archives', 'Export', 'Notebook']
    super(HtmlNavBar, self).__init__(aresObj, value)
    self.backgroundColor = self.getColor('greyColor', 0) if backgroundColor is None else backgroundColor
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) + 2 if size is None else size
    self.logoLink = logoLink if logoLink is not None else self.aresObj._urlsApp['ares-index']
    self.color = self.getColor('greyColor', 4) if color is None else color
  # --------------------------------------------------------------------------------------------------------------
  #                                     DROPDOWN SECTIONS
  #
  def dropDown(self, name, definition):
    self.categories[name] = definition
    if not name in self.definedOrder:
      self.definedOrder.append(name)
    return self

  def dropDownReport(self,  report_name, script_name):
    return self.dropDown('Report', [
      {"name": "Clear Parameters", 'url': '%s/run/%s/%s' % (self.aresObj._urlsApp['ares-report'], report_name, script_name)},
      {"diviser": True},
      {"name": "Documentation Report", 'url': '%s/dsc/%s/%s' % (self.aresObj._urlsApp['ares-report'], report_name, script_name)},
      {"name": "Documentation Env", 'url': '%s/dsc/%s/__main__' % (self.aresObj._urlsApp['ares-report'], report_name)},
      {"diviser": True},
      {"name": "Quick Share", 'url': '#', 'action': "onclick=\"FormGoTo('%s/quick/%s/%s', 'POST')\"" % (self.aresObj._urlsApp['ares-transfer'], report_name, script_name)},
      #{"name": "Sign off report", 'url': ''},
      {"name": "Info / Logs", 'url': '%s/view/%s/%s' % (self.aresObj._urlsApp['ares-report'], report_name, script_name)},
      {"diviser": True},
      {"name": "Download Env", 'url': '%s/download/report/%s' % (self.aresObj._urlsApp['ares-transfer'], report_name)},
      {"name": "Download Page", 'url': ''},
    ])

  def dropDownExport(self, report_name, script_name):
    return self.dropDown('Export', [
      {"name": "Copy URL", 'url': '#', 'action': "onclick='CopyToClipboard()'"},
      {"diviser": True},
      {"name": "HTML 5", 'url': '#', 'action': "onclick=\"FormGoTo('%s/html/%s/%s', 'POST')\"" % (self.aresObj._urlsApp['ares-transfer'], report_name, script_name)},
      {"name": "Excel", 'url': '#', 'action': "onclick=\"FormGoTo('%s/xls/%s/%s', 'POST')\"" % (self.aresObj._urlsApp['ares-transfer'], report_name, script_name)},
      {"name": "Word", 'url': '#', 'action': "onclick=\"FormGoTo('%s/doc/%s/%s', 'POST')\"" % (self.aresObj._urlsApp['ares-transfer'], report_name, script_name)},
      #{"name": "Power Point", 'url': '#', 'action': "onclick=\"FormGoTo('%s/ppt/%s/%s', 'POST')\"" % (self.aresObj._urlsApp['ares-transfer'], report_name, script_name)}
    ])

  def dropDownDesigner(self, report_name, report=None, contributors=None):

    if (contributors is not None and self.aresObj.user in contributors) or self.aresObj.run.is_local:
      notebooks = [
        {"name": "Contributors", 'target': '_blank', 'url': '%s/contrib/%s' % (self.aresObj._urlsApp['ares-notebook'], report_name)},
        {"name": "Contact Dev", 'target': '_blank', 'url': '%s/contact/%s' % (self.aresObj._urlsApp['ares-notebook'], report_name)},
        {"diviser": True},
        {"name": "Files", 'target': '_blank', 'url': '%s/viewer/files/%s' % (self.aresObj._urlsApp['ares-transfer'], report_name) },
        {"name": "Database", 'target': '_blank', 'url': '%s/%s' % (self.aresObj._urlsApp['ares-db'], report_name)},
        {"diviser": True},
        {"name": "Functions", 'target': '_blank',  'url': '%s/functions/%s' % (self.aresObj._urlsApp['ares-notebook'], report_name)},
        {"name": "Services", 'target': '_blank',  'url': '%s/services/%s' % (self.aresObj._urlsApp['ares-notebook'], report_name)}]
      if report is None:
        notebooks.append( {"name": "Reports", 'url': '%s/reports/%s' % (self.aresObj._urlsApp['ares-notebook'], report_name)} )
      else:
        notebooks.append( {"name": "Reports", 'url': '%s/reports/%s?select=%s.py' % (self.aresObj._urlsApp['ares-notebook'], report_name, report)})
    else:
      notebooks = [
        {"name": "Contact Dev", 'target': '_blank', 'url': '%s/contact/%s' % (self.aresObj._urlsApp['ares-notebook'], report_name)}]
    return self.dropDown('Editor', notebooks)

  def dropDownHistory(self, htmlReports):
    tmps = []
    for report in htmlReports:
      tmps.append( {"name": "Contributors", 'url': ''} )
    return self.dropDown('Archives', tmps)

  def __str__(self):
    items = ['<nav id="report_nav_bar" class="navbar navbar-expand-sm fixed-top navbar-light" style="height:40px;margin:0;padding:0;background-color:%s;padding-left:5px;border-bottom:1px solid %s">' % (self.backgroundColor, self.getColor('greyColor', 4))]
    items.append( '<button class="navbar-toggler" style="height:27px" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon" style="height:20px;margin-top:-5px"></span></button>')
    # Common part with the logo and the link to the main page
    items.append('<a class="navbar-brand" href="%s" style="color:%s">' % (self.logoLink, self.getColor('textColor', 0)))
    if self.logo is not None:
      items.append(render_template_string('<img src="{{ url_for(\'static\',filename=\'images/logo/%s\') }}" width="85px" height="auto" style="margin-top:5px" class="d-inline-block align-top" alt="">' % self.logo))
    items.append('</a>' )
    items.append('<div class="collapse navbar-collapse" id="navbarTogglerDemo02" style="background-color:%s;height:27px">' % self.backgroundColor)
    items.append('<ul class="navbar-nav ml-auto">')
    items.append('<li class="nav-item active"><a class="nav-link" href="%s" style="font-size:16px;color:%s;font-weight:bold;margin-right:20px;white-space:nowrap;">%s</a></li>' % (self.aresObj.run.url, self.color, self.aresObj.run.title))
    for name in self.definedOrder:
      section = self.categories.get(name, [])
      if len(section) > 0:
        items.append('<li class="nav-item dropdown">')
        items.append('<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="font-size:14px;height:27px;padding-left:5px;white-space:nowrap;padding-top:10px;height:100%%;display:inline-block">%s</a>' % name)
        items.append('<div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">')
        for s in section:
          if 'diviser' in s:
            items.append('<div class="dropdown-divider"></div>')
          else:
            if not 'action' in s:
              s['action'] = ""
            if not 'target' in s:
              s['target'] = '_self'
            items.append('<a class="dropdown-item" target="%(target)s" href="%(url)s" %(action)s style="font-size:12px;">%(name)s</a>' % s)
        items.append('</div></li>')
    items.append('</ul>')
    items.append('''
      <li class="nav-item">
        <a href="%(urlQuestions)s/index" class="fas fa-question-circle" title="Create a question" style="color:%(blackColor)s;margin:4px 10px 0 5px;font-size:18px;cursor:pointer;"></a>
      </li>
      <form class="form-inline my-2 my-md-0" style="position:relative">
        <span onclick="GoToReport('%(urlSearch)s/index?value=' + $('#search_input').val(), true, false)" class="fas fa-search my-2 my-sm-0" style="color:%(blackColor)s;position:absolute;font-size:15px;left:7px;top:6px;cursor:pointer;"></span>
        <input onkeydown="if (event.keyCode == 13) { GoToReport('%(urlSearch)s/index?value=' + $(this).val(), true, false) } " class="form-control" type="search" id="search_input" placeholder="Search" aria-label="Search" style="text-indent:30px;height:27px;margin-right:5px">
      </form> ''' % {"urlSearch": self.aresObj._urlsApp['ares-search'], "urlQuestions": self.aresObj._urlsApp['ares-questions'], 'blackColor': self.getColor("greyColor", 8)})
    items.append('</div>')
    # To add the login page
    rec =  {"divIcon": "<i class='fas fa-sign-out-alt'></i>", 'navBarColor': self.getColor('greyColor', 2),
            'onMouseColor': '#29293d', 'outMouseColor': self.getColor("blueColor", 12), 'color':  self.getColor('textColor', 0), 'fontSize': self.size + 5 }
    items.append('</nav>')
    self.aresObj.jsOnLoadFnc.add('$("body").css("padding-top", "%spx") ;' % self.lenght)
    return "".join(items)

  def to_word(self, document):
    pass


class HtmlNavBar1(AresHtml.Html):
  """ Python Wrapper to the HTML Navigation bar

  This component is not supposed to be changed from the Javascript layer so the build is fully done
  in the str method on the python side.

  Those Navigation bar should be either defined in the core python Apps

  :example
  htmlRecordSet = [{'url': '#', 'text': 'Consulting'}, {'url': '#', 'text': 'Master Classes'}, {'url': 'saturn', 'text': 'Schedule'},
                   {'text': 'Products', 'links':[
                     {'url': 'reports', 'text': 'Environments'}, {'url': 'designer', 'text': 'Designer'},
                     {'url': 'dashboard', 'text': "Dashboards'Minute3"}]},
                  ]
  aresObj.nav(htmlRecordSet)
  """
  __reqCss, __reqJs = ['bootstrap', 'font-awesome'], ['bootstrap', 'font-awesome']
  lenght = 45
  mocks = None # System component
  name, category = 'Nav Bar (Slide)', 'System'

  def __init__(self, aresObj, value, selected, size, breadcrum, logo):
    """ Instantiate a Nav Bar object

    :param aresObj: The aresObj report corresponding to the Report definition
    :param value: The value of the link to be displayed in the page
    :param selected: The selected value to highlight in the Nav Bar
    :param cssCls:
    """
    self.selected, self.extraLinks, self.breadcrum, self.logo = selected, None, breadcrum, logo
    aresObj.marginTop = self.lenght
    super(HtmlNavBar, self).__init__(aresObj, value)
    self.size = int(self.aresObj.pyStyleDfl['fontSize'][:-2]) + 2 if size is None else size

  def add(self, dataRec):
    """ This will allow to get a common pattern and to add extra features in the global Navigation Bar on the top of the framework

    :param dataRec: The dictionary with the data to be added to the navBar
    :return:
    """
    if self.extraLinks is None:
      self.extraLinks = []
    self.extraLinks.append(dataRec)

  def click(self, htmlCode, jsFnc):
    """ Wrapper to the onlick method of the different components

    :param htmlCode: The HTML code of the tab
    :return:
    """
    self.aresObj.jsOnLoadFnc.add(''' $('#%s').on('click', function(){ %s }); ''' % (htmlCode, jsFnc))

  def change(self, val):
    """ """
    return "$('#navbar_breadcrum p').html(%s)" % val

  def __str__(self):
    if self.vals is None:
      # Default NavBar in the Frameworl
      self.vals = [{'url': 'masterclass', 'text': 'Master Classes'},
                   {'url': 'saturn', 'text': 'Schedule'},
                   {'url': 'reports', 'text': 'Reports'},
                   {'url': 'dashboard', 'text': 'Dashboards'},
                   {'url': 'transfer', 'text': 'Packages'}]
      self.vals = []
    if self.extraLinks is not None:
      self.vals.append("||")
      self.vals.extend(self.extraLinks)

    items = ['<nav class="navbar navbar-expand-lg fixed-top navbar-light" style="margin:0;padding:0;background-color:%s;padding-left:5px;">' % self.getColor('greyColor', 5)]
    items.append('<button style="font-size:14px;margin-top:4px" class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>')

    # Common part with the logo and the link to the main page
    items.append('<a class="navbar-brand" href="\index" style="color:%s">' % self.getColor('textColor', 0))
    if self.logo is not None:
      items.append(render_template_string('<img src="{{ url_for(\'static\',filename=\'images/logo/%s\') }}" width="85px" height="auto" style="margin-top:5px" class="d-inline-block align-top" alt="">' % 'ares_logo_nav_bar.png'))
    items.append('</a>')

    # Dynamic part in the different environments
    items.append('<div class="collapse navbar-collapse" id="navbarTogglerDemo02">')
    items.append('<ul class="navbar-nav  mr-auto">')
    for i, rec in enumerate(self.vals):
      if rec == '||':
        items.append("<div style='width:70px'></div>")
        continue

      rec['color'] = self.getColor('textColor', 0) if not 'color' in rec else rec['color']
      rec['onMouseColor'] = '#29293d'
      rec['outMouseColor'] = '#29293d'
      if self.selected == rec['text']:
        rec['color'] = 'white'
        rec['background'] = self.getColor('baseColor', 7)
      rec['fontSize'] = self.size
      rec['divIcon'] = '' if not 'icon' in rec else "<i class='%s'></i> " % rec['icon']
      rec['navBarColor'] = self.getColor('greyColor', 2)
      rec['background'] = rec['background'] if 'background' in rec else self.getColor('greyColor', 5)
      if 'links' in rec:
        items.append('<li class="nav-item dropdown" style="padding-top:8px;background-color:%(background)s" onmouseover="this.style.backgroundColor=\'%(navBarColor)s\';" onmouseout="this.style.backgroundColor=\'%(background)s\';">' % rec)
        items.append('<a class="nav-link dropdown-toggle" href="#" style="color:%(color)s;font-size:%(fontSize)spx;" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">%(divIcon)s%(text)s</a>' % rec)
        items.append('<div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">')
        for j, link in enumerate(rec['links']):
          link['htmlCode'] = link['htmlCode'] if 'htmlCode' in link else '%s_%s_%s' % (self.htmlId, i, j)
          link['href'] = link['url'] if link['url'].startswith('#') else "\%s" % link['url']
          link['color'] = '#29293d' if 'color' not in link else link['color']
          if link['text'] == '<hr />':
            # This is just to display a separator in the menu
            items.append('<div style="font-size:14px;color:%(color)s">%(text)s</div>' % link)
          else:
            if 'title' in link:
              items.append('''<a id="%(htmlCode)s" title="%(title)s" class="dropdown-item" href="%(href)s" style="font-size:14px;color:%(color)s">%(text)s</a>''' % link)
            else:
              items.append('''<a id="%(htmlCode)s" class="dropdown-item" href="%(href)s" style="font-size:14px;color:%(color)s">%(text)s</a>''' % link)
        items.append('</div>')
        items.append('</li>')
      else:
        # Simple case when the record do not have any sub items
        rec['htmlCode'] = rec['htmlCode']  if 'htmlCode' in rec else '%s_%s' % (self.htmlId, i)
        rec['href'] = rec['url'] if rec['url'].startswith('#') else "\%s" % rec['url']
        rec['background'] = rec['background'] if 'background' in rec else self.getColor('greyColor', 5)

        if 'ajax' in rec:
          items.append('<li class="nav-item" onmouseover="this.style.backgroundColor=\'#959EAE\';" onmouseout="this.style.backgroundColor=\'%(background)s\';" style="background-color:%(background)s"><a class="nav-link" id="%(htmlCode)s" href="#" style="color:%(color)s;font-size:%(fontSize)spx;">%(divIcon)s%(text)s</a></li>' % rec)
          self.aresObj.jsOnLoadFnc.add('''
            $('#%(htmlCode)s').on('click', function (event){
              $.ajax({
                  url: "/%(url)s".replace('#', ''), method: "POST", data: {}, contentType: false, cache: false, processData: false, async: false})
                  .done(function(data) { %(ajaxResult)s; }) }); ''' % rec)
        else:
          if not rec.get('active', True):
            rec['a'] = '<div class="nav-link" style="color:#e0e0e0;font-size:%(fontSize)spx;background-color:%(background)s">%(divIcon)s%(text)s</div>' % rec
          else:
            rec['a'] = '<a class="nav-link" id="%(htmlCode)s" href="%(href)s" style="color:%(color)s;font-size:%(fontSize)spx;">%(divIcon)s%(text)s</a>' % rec
          items.append('<li class="nav-item" onmouseover="this.style.backgroundColor=\'%(navBarColor)s\';" onmouseout="this.style.backgroundColor=\'%(background)s\';" style="background-color:%(background)s">%(a)s</li>' % rec)

    items.append('</ul><ul class="navbar-nav">')
    if self.breadcrum is not None:
      rec = { 'text': self.breadcrum, 'color': self.getColor('textColor', 0), 'fontSize': self.size }
      items.append('''
        <li class='nav-item' id='navbar_breadcrum' style='float:right' title="Copy report URL">
          <div class='nav-link' style='color:%(color)s;font-size:%(fontSize)spx;'>
            <i class='fas fa-share-alt'></i>
          </div>
          <div style='display:none'>%(text)s</div>
        </li>''' % rec)
      div = self.aresObj.div("Report Parameters copied to ClickBoard !")
      div.css({'display': 'none', 'position': 'absolute', 'top': '40px', 'right': '20px',
                'text-align': 'center', 'padding': '5px', 'color': 'white',
                'border-radius': '.4em;', 'background-color': self.getColor('baseColor', 2), 'z-index': 10010, "width": '200px' })

      self.aresObj.jsOnLoadFnc.add('''
        $('#navbar_breadcrum').disableSelection(); 
        $('#navbar_breadcrum').on('click', function(e) {
          if (window.clipboardData) {
            window.clipboardData.setData('Text', '%(url_root)s' + %(jsBreadCrumb)s);
          } else {
            var selection = window.getSelection();
            $('#navbar_breadcrum div').last().html('%(url_root)s' + %(jsBreadCrumb)s) ;
            $('#navbar_breadcrum div').last().show() ;
            var range = document.createRange();
            range.selectNodeContents($('#navbar_breadcrum div').last().get(0));
            selection.removeAllRanges();
            selection.addRange(range);
            document.execCommand("Copy") ;
          }
          %(jqId)s.show().delay(2000).fadeOut("slow");
          $('#navbar_breadcrum div').last().hide() ; })''' % {'jsBreadCrumb': self.aresObj.jsBreadCrum(), 'jqId': div.jqId, 'url_root': self.aresObj.run.url_root} )

    # To add the login page
    rec =  {"divIcon": "<i class='fas fa-user-circle'></i>&nbsp;", 'text': "Login", 'navBarColor': self.getColor('greyColor', 2),
            'onMouseColor': '#29293d', 'outMouseColor': '#29293d', 'color':  self.getColor('textColor', 0), 'fontSize': self.size }
    rec['background'] = self.getColor('baseColor', 7) if self.selected == rec['text'] else self.getColor('greyColor', 5)
    items.append('<li class="nav-item dropdown" style="padding-top:8px;background-color:%(background)s" onmouseover="this.style.backgroundColor=\'%(navBarColor)s\';$(this).find(\'a\').css(\'color\', \'%(onMouseColor)s\')" onmouseout="this.style.backgroundColor=\'%(background)s\';$(this).find(\'a\').css(\'color\', \'%(outMouseColor)s\')">' % rec)
    items.append('<a class="nav-link dropdown-toggle" href="#" style="color:%(color)s;font-size:%(fontSize)spx" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">%(divIcon)s%(text)s</a>' % rec)
    items.append('<div class="dropdown-menu  dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">')
    items.append('<a id="%(htmlCode)s" class="dropdown-item" href="/admin/account" style="font-size:14px">User Account</a>')
    items.append('<a id="%(htmlCode)s" class="dropdown-item" href="/admin/logout" style="font-size:14px">Log Out</a>')
    items.append('</div></li>')

    items.append('</ul></div></nav>')
    # To add the extra padding to the rest of this page
    #self.aresObj.jsOnLoadFnc.add('$("body").css("padding-top", "%spx") ;' % self.lenght)
    return "".join(items)


class HtmlParamsBar(AresHtml.Html):
  """ Python wrapper of the Parameters Bar

  :example
  aresParameter = [{'htmlComponent': 'date', 'code': 't', 'label': 'COB T', 'yyyy_mm_dd': '2017-02-01'},
                   {'htmlComponent': 'date', 'code': 't_1', 'label': 'COB T-1', 'yyyy_mm_dd': '2017-03-01'},
                   {'htmlComponent': 'input', 'code': 'input', 'text': 'google'},
                   {'htmlComponent': 'slider', 'code': 'slider', 'number': 40},
                   {'htmlComponent': 'input', 'code': 'input2', 'text': 'Youpi'},]
  aresObj.paramsbar(aresParameter)
  """
  __reqCss, __reqJs = ['bootstrap'], ['bootstrap']
  __pyStyle = ['CssDivNoBorder']
  allowedComponents = ['date', 'input', 'radio', 'button', 'select', 'title', 'slider', 'dropdown', 'switch',
                       'selectmulti', 'delimiter', 'checkbutton', 'inputRange', 'slider', 'inputInt']
  name, category = 'Parameters Bar', 'System'

  def __init__(self, aresObj, vals, top, logFiles, height):
    """ Instanciate a container object """
    self.__components, self.__order, self.logFiles = {}, [], logFiles
    self.jsUpdateFnc, self.inCookies = True, {}
    vals = list(vals)
    for component in vals:
      if component['htmlComponent'] not in self.allowedComponents:
        logging.error('%s is not allowed in the parameters bar' % component['htmlComponent'])
        raise Exception('%s is not allowed in the parameters bar' % component['htmlComponent'])

      aresFnc = getattr(aresObj, component['htmlComponent'])
      parameters = dict(component)
      if 'inCookies' in parameters and aresObj.withCookies:
        self.inCookies[component['htmlCode']] = parameters['inCookies']
        del parameters['inCookies']

      del parameters['htmlComponent']

      if not component['htmlComponent'] in ['delimiter']:
        htmlCode = component['htmlCode']
        if htmlCode in self.__order:
          raise Exception('code in the Parameters bar - %s - duplicated' % htmlCode)

      htmlObj = aresFnc(**parameters)
      if htmlObj.category == "Select":
        htmlObj.container = "#ares_page_content"
      if hasattr(htmlObj, 'initVal') and htmlCode in aresObj.http:
        htmlObj.initVal(aresObj.http[htmlCode])
      if component['htmlComponent'] in ['delimiter']:
        htmlObj.htmlCode = "component_%s" % id(self)
      self.__add__(htmlObj)
    self.height, self.top = height, top
    aresObj.marginTop += height
    super(HtmlParamsBar, self).__init__(aresObj, [])
    self.css({'margin': '0', 'display': 'inline-block'})

  def __add__(self, htmlObj):
    """ Add items to a container """
    htmlObj.inReport = False # Has to be defined here otherwise it is set to late
    htmlObj.css({'display': 'inline-block', 'margin-left': '10px'})
    htmlObj.change(htmlObj.jsToUrl())
    # The component added must have a htmlCode class variable defined
    self.__order.append(htmlObj.htmlCode)
    self.__components[htmlObj.htmlCode] = htmlObj
    return self

  def getHtmlCodes(self):
    return self.__order

  def get(self, htmlCode):
    """ Return the Html component in the parameter bar """
    return self.__components[htmlCode]

  def toCookies(self, htmlCode):
    return self.inCookies.get(htmlCode, True)

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    vals = [self.__components[comp].html() for comp in self.__order]
    self.aresObj.jsOnLoadFnc.insert(0, 'NavBar(%s, %s)' % (self.jqId, json.dumps(vals)))

  def onDocumentLoadFnc(self):
    """ Pure Javascript onDocumentLoad Function """
    self.addGlobalFnc("NavBar(htmlObj, data)", ''' htmlObj.empty() ; $('#report_nav_bar').css('border-bottom', 'none'); data.forEach(function(rec){ htmlObj.append(rec) ; });  ''')

  def jsToUrl(self): return ''

  def __str__(self):
    """ Returns the HTML representation of the parameter bar """
    # Change the margin of the body as the Parameter bar will take some extra space on the top of the page
    self.aresObj.jsOnLoadFnc.add('$("body").css("margin-top", "%spx")' % (self.aresObj.marginTop - self.height))
    self.aresObj.jsOnLoadFnc.add('''
      $("#report_side_bar").css("top", "40px"); $("#side_bar_envs").css("top", "40px");
      $('#nav_bar_reset').on('click', function(event) {%(jsPost)s});
      ''' % {'jsPost': self.aresObj.jsPost("%s/locals/clean/%s" % (self.aresObj._urlsApp['ares-transfer'], self.aresObj.run.report_name), None, self.jsGoTo(self.jsToUrlReset(), isPyData=False), isPyData=False)} )
    self.addPyCss("CssParamsBar")
    return '''
      <div id="param_bar" class="%(clsParamBar)s" style="top:%(top)spx">
        <div %(strAttr)s></div>
      </div> ''' % {'top': self.aresObj.marginTop - self.height - 5, 'clsParamBar': self.getPyCss("CssParamsBar"),
                    'strAttr': self.strAttr(pyClassNames=['CssBasicList'])}
