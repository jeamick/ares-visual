#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.html import AresHtml


class HtmlSideBarBasic(AresHtml.Html):
  references = {'W3C Definition': 'https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_sidenav'}
  name, category, callFnc = 'Side bar', 'Others', 'sidebar'
  __pyStyle = ['CssSideBarFixed']
  __reqCss, __reqJs = ['bootstrap', 'font-awesome', 'jquery-scrollbar'], ['bootstrap', 'font-awesome', 'jquery-scrollbar']
  onMouseOverColor = 'black'

  def __init__(self, aresObj, links, color, size, dataSrc, servers):
    super(HtmlSideBarBasic, self).__init__(aresObj, links)
    self.color = self.getColor('greyColor', 0) if color is None else color
    self.size, self.dataSrc, self.servers = "20px" if size is None else "%spx" % size, dataSrc, servers
    self.css({'color': self.color, 'font-size': self.size, 'z-index': 5, 'margin': 0})
    self._actions = []

  def jsToUrl(self): return ""

  @property
  def htmlId(self): return 'report_side_bar'

  def onDocumentReady(self):
    if self.aresObj.run.report_name is not None:
      self.aresObj.jsOnLoadFnc.add(
        self.aresObj.jsPost('"%s/is_favourite/%s/%s"' % (self.aresObj._urlsApp['ares-report'], self.aresObj.run.report_name, self.aresObj.run.script_name), None,
                            'if (data) { $("#ares_reports_favourites").addClass("fas")  } else { $("#ares_reports_favourites").hasClass("far") } ', isDynUrl=True))

  def onDocumentLoadFnc(self):
    self.addGlobalFnc("%s(htmlObj, data)" % self.__class__.__name__, ''' $('#side_bar_explorer').empty() ;
      var group = $('<ul style="padding:0;margin:0;list-style:none"></ul>'); 
      var sidebarState = JSON.parse(window.sessionStorage.getItem('SIDEBAR_STATE'));
      if (sidebarState === null) { sidebarState = {} } ;
      data.folders.forEach(function(rec, index){
        var li = $('<li onclick="GetFolder(this);"></li>'); var display = 'none' ; var chevron = 'fas fa-folder';
        if ('env_' + index in sidebarState) { display = sidebarState['env_' + index] ; }
        if (display != 'none') { chevron = 'fas fa-folder-open'; }
        li.append('<a href="#" style="color:%(darkBlue)s;font-weight:bold;text-decoration:none;display:inline-block;padding-left:5px;margin-right:5px;font-size:14px;font-variant:small-caps;"><b><i id="chevron" class="fa ' + chevron + '"></i>&nbsp;'+ rec.name +'</a></b>') ;
        var sub = $('<ul id="env_' + index + '" style="padding:0 0 0 20px;margin:0;list-style:none;display:'+ display +'"></ul>') ;
        eventLi = $('<li onclick="event.stopPropagation();" style="margin-bottom:10px">') ;
        sub.append(eventLi) ;
        
        rec.items.forEach(function(data){
          var icons = '<i onclick=\\'GoToReport("%(urlReport)s/run/'+ rec.name +'/'+ data.script +'", true, false)\\' style="display:inline-block;margin-right:10px" title="Open in new tab" class="far fa-arrow-alt-circle-right"></i><i onclick=\\'GoToReport("%(urlReport)s/view/'+ rec.name +'/'+ data.script +'", true, false)\\' style="display:inline-block;font-size:14px;margin-right:10px" title="View Statistics" class="far fa-chart-bar"></i>' ;
          if (data.color == undefined) { data.color = '%(darkBlue)s' ; };
          if (data.doc) { icons = icons + '<i onclick=\\'GoToReport("%(urlReport)s/dsc/'+ rec.name +'/'+ data.script +'", true, false)\\' style="display:inline-block;margin-right:10px" title="Documentation" class="far fa-file-alt"></i>' ; }
          if (data.inFavorite) {sub.append('<li onclick="event.stopPropagation();"><a href="#" title="'+ data.script + '" style="display:inline-block;margin-right:10px;color:'+ data.color + '" onclick="BreadCrumbClick(this, \\''+ data.url.replace(/\\\\/g, '\\\\\\\\')  +'\\')">'+ data.name +'</a></li>') ; } 
          else { sub.append('<li style="white-space:nowrap; overflow-x: hidden;margin-right:10px" onclick="event.stopPropagation();"><a href="#" title="'+ data.script + '" style="display:inline-block;margin-right:10px;color:'+ data.color + '" onclick="BreadCrumbClick(this, \\''+ data.url.replace(/\\\\/g, '\\\\\\\\')  +'\\')">'+ data.name +'</a><i style="color:%(darkBlue)s;cursor:pointer;font-size:14px;margin-right:10px" onclick="Favorites(this, \\'' + rec.name + '\\', \\'' + data.script + '\\', \\'div\\', true)" title="Add to favorites" class="far fa-heart"></i></li>') ; }});
          
        /* sub.append('<li><i class="far fa-plus-square" style="margin-right:5px"></i>Add new script</li>') ; */
        li.append(sub); group.append(li); });
      /* group.append('<li onclick="GetFolder(this);"></li>Add new env'); */
      
      $('#side_bar_explorer').append( group ) ;
      $('#side_bar_explorer').css( {'height': parseInt($('#side_bar_envs').css('height'),10) - 250 + 'px'} ) ;
      if (data.favorites.length > 0){
        htmlObj.find('#side_bar_favorite').empty() ;
        var groupFav = $('<ul style="padding:0;margin:0;list-style:none"></ul>');
        data.favorites.forEach(function(rec, index){
          var li = $('<li onclick="GetFolder(this);"></li>'); var display = 'none' ; var chevron = 'fas fa-folder';
          if ('env_' + index in sidebarState) { display = sidebarState['env_' + index] ; }
          if (display != 'none') { chevron = 'fas fa-folder-open'; }
          li.append('<a href="#" style="color:%(darkBlue)s;font-weight:bold;font-variant:small-caps;text-decoration:none;display:block;font-size:14px;padding-left:5px"><b><i id="chevron" class="fa ' + chevron + '"></i>&nbsp;'+ rec.name +'</a></b>') ;
          var sub = $('<ul id="env_' + index + '" style="padding:0 0 0 20px;margin:0;list-style:none;display:'+ display +'"></ul>') ;
          rec.items.forEach(function(data){
            if (data.color == undefined) { data.color = '%(darkBlue)s' ; };
            sub.append('<li onclick="event.stopPropagation();"><a href="#" title="'+ data.script + '" style="color:'+ data.color + '" onclick="BreadCrumbClick(this, \\''+ data.url.replace(/\\\\/g, '\\\\\\\\')  +'\\')">'+ data.name +'</a><div style="color:%(darkBlue)s;cursor:pointer;margin-left:5px;font-size:10px" onclick="Favorites(this, \\'' + rec.name + '\\', \\'' + data.script + '\\', \\'div\\', false)" title="Remove from favorites" class="fas fa-times"></div></li>') ; 
          });
          li.append(sub); groupFav.append(li); });
        $('#side_bar_favorite').append(groupFav); }
      $("#nav_link_title").tooltip() ;
      ''' % {'reportName': self.aresObj.run.report_name, 'hoverColor': self.onMouseOverColor, 'urlReport': self.aresObj._urlsApp['ares-report'],
             'cssLinks': self.aresObj.cssObj.getClsTag(['CssSideBarLinks']), 'darkBlue': self.getColor('baseColor', 0)})

  def to_word(self, document): pass

  def addAction(self, icon, url, tooltip='', color=None, isPyData=True):
    """
    :dsc:

    """
    actionDef = ['<div style="position:relative;cursor:pointer;display:block;pointer-events:auto;margin-bottom:10px;">']
    if isPyData:
      actionDef.append('<i onclick="GoToReport(\'%(url)s\')" class="%(icon)s" title="%(tooltip)s" style="color:%(color)s"></i>' % {"url": url, "icon": icon, "url": url, "color": color, "tooltip": tooltip})
    else:
      actionDef.append('<i onclick="%(url)s" class="%(icon)s" title="%(tooltip)s" style="color:%(color)s"></i>' % {"url": url, "icon": icon, "url": url, "color": color, "tooltip": tooltip})
    actionDef.append('</div>')
    self._actions.append("".join(actionDef))
    return self

  def __str__(self):
    if self.dataSrc is not None:
      if self.dataSrc['type'] == 'url':
        self.addGlobalFnc("UpdateSideBar(evt)", '''
           $(evt).addClass('fa-spin'); $.getJSON( "%(url)s", function( data ) { %(jsVal)s = data ; %(pyCls)s(%(jqId)s, %(jsVal)s) ; $(evt).removeClass('fa-spin'); });
           ''' % {'pyCls': self.__class__.__name__, 'jsVal': self.jsVal, 'jqId': self.jqId, 'url': self.dataSrc['url']} )

    self.addGlobalFnc("BreadCrumbClick(evt, url)", '''
          $('#popup_loading').find("div").html("Loading " + url + "...") ;
          $('#popup_loading_back').show(); $('#popup_loading').show();
          var params = [] ;
          for(var key in %(breadCrumVar)s['params']) { params.push(key + "=" + %(breadCrumVar)s['params'][key]) ;  }
          if (params.length > 0) { breadCrumResult = url + "?" + params.join("&")  ;} else { breadCrumResult = url; };
          window.location.href = "/" + breadCrumResult ; ''' % {'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar})

    self.addGlobalFnc("GetFolder(evt)", '''
          if ($(evt).find('#chevron').hasClass('fas fa-folder-open') ) { $(evt).find('#chevron').attr('class', 'fas fa-folder') ; } 
          else { $(evt).find('#chevron').attr('class', 'fas fa-folder-open') ; }; 
          $(evt).find('ul').toggle(); 
          if ( window.sessionStorage.getItem('SIDEBAR_STATE') == null) { window.sessionStorage.setItem('SIDEBAR_STATE', JSON.stringify({})) ; }
          var sidebarState = JSON.parse(window.sessionStorage.getItem('SIDEBAR_STATE'));
          sidebarState[$(evt).find('ul').attr('id')] = $(evt).find('ul').css('display');
          window.sessionStorage.setItem('SIDEBAR_STATE', JSON.stringify(sidebarState)) ; ''')

    self.addGlobalFnc("Favorites(src, reportName, scriptName, type, flag)",
        '''if (type == 'div' && !flag) { $(src).parent().remove() }; %s ;
        ''' %self.aresObj.jsPost('"%s/switch_favorites/" + reportName + "/" + scriptName' % self.aresObj._urlsApp['ares-report'], None, 'if (data) { $(src).addClass("fas")  } else { $(src).addClass("far")} ', isDynUrl=True))

    self.addGlobalFnc("RunTask(urlParam)", self.aresObj.jsPost("urlParam", None, '', isDynUrl=True))

    # Add some specific styles for the sidebar items
    cssDef = self.addPyCss('CssSideBarBubble')
    cssSideBarMenu = self.addPyCss('CssSideBarMenu')
    return '''
      <div id="side_bar_envs" style='height:100%%;display:none;position:fixed;z-index:5;width:300px;top:0;background-color:%(lightBlue)s;left:0;padding:50px 5px 5px 45px;'>
        <a href="%(urlNotebook)s/environments/create" style="display:inline-block;margin-bottom:10px;font-weight:bold"> + Create a new environment</a>
        <span style="font-weight:bold;display:inline-block;text-transform:uppercase;margin-top:10px;width:100%%">Favorites</span>
        <div id="side_bar_favorite" style="width:100%%;display:inline-block"></div>
        
        <hr />
        <input type="text" style="width:100%%;display:inline-block" placeholder="search a report" />
        <span style="font-weight:bold;display:inline-block;text-transform:uppercase;margin-top:10px;width:100%%">Environments</span>
        <div id="side_bar_explorer" style="margin-right:20px;width:100%%;overflow-y:scroll"></div>
      </div>
      
      <div %(strAttr)s>                
        <div style="position:relative;cursor:pointer;display:inline-block;pointer-events:auto;" onclick="$('#side_bar_envs').toggle()">
          <i class="fas fa-users" title="Public folders"></i>
        </div>
        
        <hr style="background-color:white;margin:10px 5px 15px 5px" />
        %(actions)s
        
        <div style="position:fixed;bottom:5px;cursor:pointer;width:40px">
          <div style="position:relative;display:inline-block;pointer-events:auto;" title="Settings" onmouseout="$(this).find('div').hide()" onmouseover="$(this).find('div').show();">
            <i onclick="GoToReport('%(urlAdmin)s/account', false, false)" style="margin-right:2px" class="fas fa-wrench"></i>
          </div>

          <br />
          <!--
          <div style="position:relative;display:inline-block;pointer-events:auto;" title="The Script scheduler" onmouseout="$(this).find('div').hide()" onmouseover="$(this).find('div').show();">
            <i onclick="GoToReport('%(urlReport)s/run/scheduler/index', false, false)"  class="far fa-clock"></i>
          </div> 
          <div style="position:relative;display:inline-block;pointer-events:auto;" title="The lab" onmouseout="$(this).find('div').hide()" onmouseover="$(this).find('div').show();">
            <i onclick="GoToReport('%(urlReport)s/run/lab/index', false, false)"  class="fas fa-flask"></i>
          </div> --!>
          <div style="position:relative;display:inline-block;pointer-events:auto;" title="Log off" onmouseout="$(this).find('div').hide()" onmouseover="$(this).find('div').show();">
            <i onclick="GoToReport('%(urlAdmin)s/logout', false, false)" style="margin-right:2px" class="fas fa-power-off"></i>
          </div>

        </div>
      </div>''' % {"strAttr": self.strAttr(pyClassNames=['CssSideBarFixed']), 'report_name': self.aresObj.run.report_name, 'urlReport': self.aresObj._urlsApp['ares-report'],
                   'cssDef': cssDef, 'cssSideBarMenu': cssSideBarMenu,'script_name': self.aresObj.run.script_name, 'urlAdmin': self.aresObj._urlsApp['ares-admin'],
                   'urlNotebook': self.aresObj._urlsApp['ares-notebook'], 'lightBlue': self.getColor('blueColor', 11), "actions": "".join(self._actions)}


