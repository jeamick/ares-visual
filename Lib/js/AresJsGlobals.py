#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DSC = {
  'eng': """
:category: JS Framework
:rubric: JS
:dsc:
Python wrapper to produce a String with all the Global variables
__
The purpose of this module is to isolate the monitoring of the global javascript variables.
Here all the variables will be stored during the report run and it will order the variables to be correctly defined in the javascript (once the html text file is generated from the python).
__
Ares.py will use this module and it will create one object which will be updated in each HTML component.
At the end of the Ares.py runs, this variable will then produce the string which will be used to define all the global javascript variables
__
As a reminder a global variable in javascript is something set at the beginning using the var keyword which can be then used in each function in the report. The scope of those variables are global and no need normally to mention the use of a global variable in a function. There is no need for special keyword.
__
To add a variable, please use the function add by only adding the varName, the function definition (without the ; at the end. It is not necessary as it will be added anyway).
"""}


import json
import logging
from ares.Lib import AresMarkDown


PROTOTYPE_FNC = [
  'String.prototype.leftTrim = function() { return this.replace(/^\s+/, ""); } ;',
  'if (!String.prototype.startsWith) {String.prototype.startsWith = function(searchString, position){ return this.substr(position || 0, searchString.length) === searchString; };}',
  '''
  Number.prototype.formatMoney = function(decPlaces, thouSeparator, decSeparator) {
    var n = this, decPlaces = isNaN(decPlaces = Math.abs(decPlaces)) ? 2 : decPlaces,
        decSeparator = decSeparator == undefined ? "." : decSeparator,
        thouSeparator = thouSeparator == undefined ? "," : thouSeparator,
        sign = n < 0 ? "-" : "",
        i = parseInt(n = Math.abs(+n || 0).toFixed(decPlaces)) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return sign + (j ? i.substr(0, j) + thouSeparator : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thouSeparator) + (decPlaces ? decSeparator + Math.abs(n - i).toFixed(decPlaces).slice(2) : "");
  };
  ''',
  '''
  String.prototype.formatMoney = function(decPlaces, thouSeparator, decSeparator) {
    var n = parseFloat(this); return n.formatMoney(decPlaces, thouSeparator, decSeparator);
  };
  ''',
  # '''
  # Array.prototype.unique = function() {
  #   var result = [];
  #   this.forEach(function(item) {if(result.indexOf(item) < 0) { result.push(item)}});
  #   return result;
  # };
  # ''',
  # '''
  # Array.prototype.contains = function(obj) {
  #   var i = this.length;
  #   while (i--) {if (this[i] === obj) {return true}}
  #   return false;
  # }
  # '''
]


class JsGlobalVars(object):
  """
  :category: JS Framework
  :rubric: JS
  :fnc fnc:
  :fnc add:
  :fnc addJs:
  :fnc __str__:
  :dsc:
    Dedicated class to monitor the global variables in the Javascript layer

    This module will store the global variables defined in Python but it will also monitor the dependencies.
    Basically if a variable needs another one in its definition, this should be mentioned in the python layer and this
    module will take care of the ordering.

    Then at the end it will return all the global variable as a string in the function __str__
  """
  breadCrumVar = 'breadCrumUrl'

  def __init__(self, aresObj=None):
    """ Create an object to monitor the definition of the global variables """
    self.jsGlobals, self.jsVarOrder, self.jsFragments, self.reportHtmlCode = {}, [], set(), set([])
    self.aresObj = aresObj
    self.jsGlobalsFnc = {'buildBreadCrum()': '''
        var params = [] ; for(var key in %(breadCrumVar)s['params']) { params.push(key + "=" + %(breadCrumVar)s['params'][key]) ;  }
        var breadCrumResult = %(breadCrumVar)s['url'] ;
        if (params.length > 0) { breadCrumResult = breadCrumResult + "?" + params.join("&")  ;}
        return breadCrumResult; ''' % {'breadCrumVar': self.breadCrumVar}}
    self.jsGlobalsFnc['aresObj(htmlCode)'] = 'if (htmlCode in %(breadCrumbVar)s.params) {return %(breadCrumbVar)s.params[htmlCode];} else { return null }' % {'breadCrumbVar': self.breadCrumVar}
    self.jsGlobalsFnc['FormatFilterDt(filterVal)'] = "var dt = filterVal.split('-') ; return dt[2] + '/' + dt[1] + '/'+ dt[0] ; "
    self.jsGlobalsFnc['GetClipBoardData(event)'] = "if (window.clipboardData == undefined) { alert('this only works with IE') ; } else { return window.clipboardData.getData('text')}; "
    self.jsGlobalsFnc['LoadingPopup(reportName)'] = '''$('#popup_loading').find("div").html("Loading " + reportName + "..."); $('#popup_loading_back').show(); $('#popup_loading').show(); '''
    self.jsGlobalsFnc['GoToReport(url, newWindows, widthLoading)'] = '''
        if(newWindows) { window.open(url, '_blank') ; } 
        else { 
          if ( widthLoading ){
            $('#popup_loading').find("div").html("Loading " + url + "..."); 
            $('#popup_loading_back').show(); $('#popup_loading').show(); }
          window.location.href = url;} '''
    self.jsGlobalsFnc['Today()'] = ''' 
      now = new Date();
      year = "" + now.getFullYear();
      month = "" + (now.getMonth() + 1); if (month.length == 1) { month = "0" + month; }
      day = "" + now.getDate(); if (day.length == 1) { day = "0" + day; }
      hour = "" + now.getHours(); if (hour.length == 1) { hour = "0" + hour; }
      minute = "" + now.getMinutes(); if (minute.length == 1) { minute = "0" + minute; }
      second = "" + now.getSeconds(); if (second.length == 1) { second = "0" + second; }
      return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second; '''
    self.jsGlobalsFnc['CleanText(text)'] = "return text.trim().replace(/\W+/g, '');"
    self.jsGlobalsFnc['CssStyleBuilder(params)'] = '''
      cssParams = [] ;
      for( var i in params) { cssParams.push( i +":"+ params[i]) ; }
      return cssParams.join(";");
      '''
    self.jsGlobalsFnc['CopyToClipboard()'] = '''
      var url = window.location.href.split('?')[0];
      if (url.slice(-1) == '#') { url = url.slice(0, -1); };
      var splitParams = buildBreadCrum().split('?') ; var params = "";
      if (splitParams.length > 1 ) { params = splitParams.slice(1, splitParams.length); }
      if (window.clipboardData) { window.clipboardData.setData('Text', url + '?' + params); } 
      else {
        var selection = window.getSelection();
        $("body").append("<div id='breadcrumb_url'>"+ url + '?' + params +"</div>");
        var range = document.createRange();
        range.selectNodeContents($('#breadcrumb_url').get(0));
        selection.removeAllRanges(); selection.addRange(range);
        document.execCommand("Copy") ; $('#breadcrumb_url').remove() ; 
        var div = $('<div>Report Parameters copied to ClickBoard !</div>').css({'display': 'block', 'position': 'fixed', 'top': '40px', 'right': '200px',
                'text-align': 'center', 'padding': '5px', 'color': 'white', 'border-radius': '.4em', 'z-index': 10010, 'background-color': '%s', "width": '200px'});
        $('body').append(div); setTimeout(function() {div.remove()}, 2000) } ''' % self.aresObj.getColor('baseColor', 2)
    self.jsGlobalsFnc['FormGoTo(url, method)'] = '''
      var form = $('<form method="'+ method +'" action='+ url +'></form>') ; NO_UNLOAD = true;
      for(var key in %(breadCrumVar)s['params']) {
        form.append( '<input type="hidden" name="'+ key +'" value="' + %(breadCrumVar)s['params'][key] + '">' ) } ; 
      form.appendTo('body').submit();
      ''' % {'breadCrumVar': self.breadCrumVar}
    self.jsGlobalsFnc['toAresMarkup(text)'] = '''
      text = text.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
      text = text.replace(/\*\*\*(.*?)\*\*\*/g, "<b><i>$1</i></b>");
      text = text.replace(/\*(.*?)\*/g, "<i>$1</i>");
      text = text.replace(/__(.*?)__/g, "<u>$1</u>");
      text = text.replace(/~~(.*?)~~/g, "<i>$1</i>");
      text = text.replace(/--(.*?)--/g, "<del>$1</del>");
      text = text.replace(/<<(.*?)>>/g, "<a href='$1'>Link</a>");
      text = text.replace(/\!\((.*?)\)/g, "<i class='$1'></i>");
      text = text.replace(/\[(.*?)\]\(https\\\:(.*?)\)/g, "<a href='$2' target='_blank'>$1</a>");
      text = text.replace(/\[(.*?)\]\(http\\\:(.*?)\)/g, "<a href='$2' target='_blank'>$1</a>");
      text = text.replace(/\[(.*?)\]\((.*?)\)/g, "<a href='$2'>$1</a>");
      if ( (text == '') || ( text == '__' ) ) { text = '<br />'; }
      return text ;'''
    self.jsGlobalsFnc['getDict(object, key, defaultValue)'] = '''
        var result = object[key];
        return (typeof result !== "undefined") ? result : defaultValue;
      '''

  def help(self, category=None, rubric=None, type=None, value=None, enum=None, section=None, lang='eng', outType=None):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    :return:
    """
    outStream = AresMarkDown.DocCollection(self.aresObj)
    outStream.title("Javascript Bespoke Functions")
    outStream.hr()
    for key in self.jsGlobalsFnc:
      outStream.append( key )
    outStream.hr()
    outStream.title('Javascript Framework', level=2)
    docAres = AresMarkDown.AresMarkDown.loads(DSC[lang])
    outStream.add(docAres, 'dsc')
    outStream.src(__file__)
    outStream.export(outType)

  def fnc(self, fncName, jsFncDef):
    """
    :category: JS Framework
    :rubric: JS
    :example: fnc('Display(value)', 'alert(value)' )
    :dsc:
      Set Global functions in the Javascript header. Even if this function is set multiple times in the Python layer as a
      dictionary is used, this will be written only once on the Javascript side.
    :link W3C Documentation: https://www.w3schools.com/js/js_functions.asp
    """
    self.jsGlobalsFnc[fncName] = jsFncDef

  def add(self, varName, stringDefinition=None, varDeps=None, pyDefinition=None):
    """
    :category: JS Framework
    :rubric: JS
    :dsc:
      Add a variable to the registering in jsGlobals but also check its location in the variable jsVarOrder

    :param varName: The variable name
    :param stringDefinition: The Javascript variable definition
    :param pyDefinition:
    :param varDeps: the list of variable names which are required
    """
    if pyDefinition is not None:
      stringDefinition = json.dumps(pyDefinition)
    if varDeps is None:
      if not varName in self.jsVarOrder:
        # it can append that a dependency is defined after the main variable so we do not add it to this list
        self.jsVarOrder.append(varName)
    else:
      min = len(self.jsVarOrder)
      for var in varDeps:
        if not var in self.jsVarOrder:
          # it can append that a dependency is defined after the main variable so we do not add it to this list
          self.jsVarOrder.append(var)
          min += 1
          continue

        # check the position in the list jsVarOrder to see where the new variable should be added
        # We will add the new variable before the smallest index number
        # No need to monitore the exception if the variable is not in the list (the report should fail as there is a problem)
        pos = self.jsVarOrder.index(var)
        if pos < min:
          min = pos
      # add the variable in the middle to correctly handle the dependencies
      self.jsVarOrder = self.jsVarOrder[:min] + [varName] + self.jsVarOrder[min:]
    if varName in self.jsGlobals:
      # even if the variable has already be used as dependency in an already defined variable, it is weird that this is
      # present in the main dictionary self.jsGlobals. It seems tha the variable definition is overriden
      logging.info("Javascript global variable %s will be overriden" % varName)
    self.jsGlobals[varName] = stringDefinition

  def addJs(self, jsFnc):
    """
    :category: JS Framework
    :rubric: JS
    :dsc:
      Add complete Javascript fragments to the header in the page.
      This can be used to add some extra lines to initialise a component (for example in the Formula object to set up the Prism framework).
    """
    self.jsFragments.add(jsFnc)

  def __str__(self):
    """
    :category: JS Framework
    :rubric: JS
    :dsc:
      return the String fragment to be added to a page to
    :return: The string with all the Javascript global variable and function
    """
    items = []
    for var in self.jsVarOrder:
      if self.jsGlobals[var] is None:
        # This global variable is not really defined and it is only used as a reference for some other functions
        # later in the page
        items.append('var %s ;' % var)
      else:
        items.append('var %s = %s;' % (var, self.jsGlobals[var]))
    for fncName, fnctDef in self.jsGlobalsFnc.items():
      items.append("function %s { %s ;};" % (fncName, ''.join([line.strip() for line in fnctDef.split('\n')])))
    for jsFragments in self.jsFragments:
      items.append(jsFragments)

    # Add prototype functions
    items.extend(PROTOTYPE_FNC)
    items.append('var %s = {url: "", params: {} } ;' % self.breadCrumVar)
    return "".join(items)
