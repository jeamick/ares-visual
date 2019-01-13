#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import re
import sys
import os
import json
import importlib
import collections
import functools
import logging

from ares.Lib.js import AresJsEncoder
from ares.Lib import AresImports

try:  # For python 3
  import urllib.request as urllib2
  import urllib.parse as parse
except:  # For Python 2
  import urllib2
  import urllib as parse


regex = re.compile('[^a-zA-Z0-9_]')

# External package required
render_template_string = AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='render_template_string', raiseExcept=False, sourceScript=__file__)
url_for =  AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='url_for', raiseExcept=False, sourceScript=__file__)

DSC = {
  'eng': '''
:category: HTML Framework
:rubric: PY
:dsc:
  ## HTML Components
  
  Lot of HTML components standard and bespoke are already available and attached to the aresObj.
  They are all coming from the module AresHtml and they have the same set of functions.
  Please have a look at the signature of the aresObj function and the documentation of you object.

  There is also the possibility to create your own HTML component directly copying something from the web.
  Do not hesitate to liaise with your IT team do so and to ensure that your work on the framework is shared. This will benefit the framework and the community.
  
  
  ### Different types of predefined HTML components
  
  [DataTables](/doc/ares.Lib.html.AresHtmlDataTable/DataTable)
  
  [Button](/doc/ares.Lib.html.AresHtmlButton)
  
  [Image](/doc/ares.Lib.html.AresHtmlImage)
  
  [Checkbox](/doc/ares.Lib.html.AresHtmlCheckBox)
  
  [Pivot Table](/doc/ares.Lib.html.AresHtmlDataPivot)
  
  [Table](/doc/ares.Lib.html.AresHtmlDataTable)
  
  [Event](/doc/ares.Lib.html.AresHtmlEvent)
  
  [Link](/doc/ares.Lib.html.AresHtmlHRef)
  
  [Input](/doc/ares.Lib.html.AresHtmlInput)
  
  [List](/doc/ares.Lib.html.AresHtmlList)
  
  [Radio](/doc/ares.Lib.html.AresHtmlRadio)
  
  [Select](/doc/ares.Lib.html.AresHtmlSelect)
  
  [Text](/doc/ares.Lib.html.AresHtmlText)
  
  ### Different types of predefined HTML Charts
  
  [ChartJs](/doc/ares.Lib.graph.AresHtmlGraphChartJs/Chart)
  
  [Billboard](/doc/ares.Lib.graph.AresHtmlGraphBillboard/Chart)
  
  [C3](/doc/ares.Lib.graph.AresHtmlGraphC3/Chart)
  
  [Vis](/doc/ares.Lib.graph.AresHtmlGraphVis/Chart)
  
  [NVD3](/doc/ares.Lib.graph.AresHtmlGraphNVD3/Chart)
  
  [Plotly](/doc/ares.Lib.graph.AresHtmlGraphPlotly/Chart)
  
'''
}

def deprecated(func):
  """This is a decorator which can be used to mark functions
  as deprecated. It will result in a warning being emmitted
  when the function is used."""

  @functools.wraps(func)
  def new_func(*args, **kwargs):
    logging.warn('#########################################')
    logging.warn("Call to deprecated function {}.".format(func.__name__))
    logging.warn('#########################################')
    return func(*args, **kwargs)
  return new_func

def inprogress(func):
  @functools.wraps(func)
  def new_func(*args, **kwargs):
    # warnings.simplefilter('always', DeprecationWarning)  # turn off filter
    # warnings.warn('############################################################################')
    # warnings.warn("Call to a test function {}.".format(func.__name__), category=DeprecationWarning, stacklevel=2)
    # warnings.warn('############################################################################')
    # warnings.simplefilter('default', DeprecationWarning)  # reset filter
    return func(*args, **kwargs)

  return new_func

def cleanData(value):
  """ Function to clean the javascript data to allow the use of variables """
  return regex.sub('', value.strip())


class Html(object):
  """
  :function val:
  :function jsQueryData:
  :function htmlId:
  :function jqId:
  :function addAttr:
  :function jsGenerate:
  :function tooltip:
  :function info:
  :function addClass:
  :function getColor:
  :function to_word:
  :function to_xls:
  :function __str__:
  :function initVal:
  :dsc:
  Parent class for all the Ares HTML components. All the function defined here are availabe in the children classes.
  Child class can from time to time re implement the logic but the function will always get the same meaning (namely the same signature and return)
  """
  alias, jsEvent, cssCls, __css = None, None, None, None
  incIndent, helper, jsVal, jsUpdateDataFnc = 0, '', '', ''
  # Those variables should not be used anymore and should be replaced by the __ ones
  # This is done in order to avoid having users to change them. Thanks to the name
  # mangling technique Python will make the change more difficult and easier to see
  reqJs, reqCss = ['jquery'], [] # Jquery is already needed
  references, htmlCode, dataSrc, _code = None, None, None, None
  hidden, inReport, isLoadFnc = False, True, True
  dashboards = [] # Static definition of usefull dashboards to get more example of an component

  # Variable dedicated to the documentation of this class
  # This cannot and should not be using or accessing by other classes derived from this one
  __doc__enums = {}

  def __init__(self, aresObj, vals, htmlCode=None, code=None, width=None, widthUnit=None, height=None, heightUnit=None, docBlock=None, globalFilter=None):
    """ Create an python HTML object """
    self.docBlockId, self._triggerEvents = None, set()
    if docBlock is not None:
      if isinstance(docBlock, dict):
        docBlockId = docBlock['id']
        if 'dsc' in docBlock:
          docBlock['dsc'] = "# %s" % docBlock['dsc']
        if 'var' in docBlock:
          docBlock['var'] = "%s = " % docBlock['var']
        if not 'params' in docBlock:
          docBlock['params'] = json.dumps(vals)
        docBlockText = "%saresObj.%s( %s )%s %s" % (docBlock.get('var', ''), self.callFnc, docBlock['params'], docBlock.get("attr", ""), docBlock.get('dsc', '') )
      else:
        docBlockId = docBlock
        docBlockText = "aresObj.%s( %s )" % (self.callFnc, json.dumps(vals))
      self.docBlockId = docBlockId
      if not docBlockId in aresObj.docBlocks:
        aresObj.docBlocks[docBlockId] = aresObj.prism( "\n%s\n" % docBlockText )
      else:
        aresObj.docBlocks[docBlockId].vals += "%s\n" % docBlockText

    self.aresObj = aresObj # The html object ID
    self.aresObj.aresUsage['ares'].setdefault(self.category, {})[self.name] = self.aresObj.aresUsage['ares'].setdefault(self.category, {}).get(self.name, 0) + 1
    self.attr = {'class': set([])} if self.cssCls is None else {'class': set(self.cssCls)} # default HTML attributes
    self.jsFncFrag, self._code, self._jsStyles = {}, code, None
    if code is not None:
      # Control to ensure the Javascript problem due to multiple references is highlighted during the report generation
      if code in self.aresObj.htmlRefs:
        raise Exception("Duplicated Html Code %s in the script !" % code)

      self.aresObj.htmlRefs[code] = True
      if code[0].isdigit() or cleanData(code) != code:
        raise Exception("htmlCode %s cannot start with a number or contain, suggestion %s " % (code, cleanData(code)))

    if htmlCode is not None:
      self.aresObj.htmlRefs[htmlCode] = True
      if htmlCode[0].isdigit() or cleanData(htmlCode) != htmlCode:
        raise Exception("htmlCode %s cannot start with a number or contain, suggestion %s " % (htmlCode, cleanData(htmlCode)))

      self.aresObj.htmlCodes[htmlCode] = self
      try:
        int(htmlCode[0])
        raise Exception("htmlCode cannot start with a number - %s" % htmlCode)

      except: pass

      self.htmlCode = htmlCode
      self.aresObj.jsGlobal.reportHtmlCode.add(htmlCode)
      if htmlCode in self.aresObj.http:
        self.vals = self.aresObj.http[htmlCode]
    css = getattr(self, '_%s__css' % self.__class__.__name__, None)
    self.pyStyle = list(getattr(self, '_%s__pyStyle' % self.__class__.__name__, []))
    if hasattr(self, '_%s__reqJs' % self.__class__.__name__):
      self.reqJs = list(getattr(self, '_%s__reqJs' % self.__class__.__name__, []))
    if hasattr(self, '_%s__reqCss' % self.__class__.__name__):
      self.reqCss = list(getattr(self, '_%s__reqCss' % self.__class__.__name__, []))
    if hasattr(self, '_%s__table_name' % self.__class__.__name__):
      self.createObjectTables()
    self.pyCssCls = set()
    if css is not None:
      # we need to do a copy of the CSS style at this stage
      self.attr['css'] = dict(css)
    self.jsOnLoad, self.jsEvent, self.jsEventFnc = set(), {}, collections.defaultdict(set)
    self.vals = vals
    self.jsVal = "%s_data" % self.htmlId
    if self.aresObj is not None:
       # Some components are not using aresObj because they are directly used for the display
       if self.reqJs is not None:
         for js in self.reqJs:
           self.aresObj.jsImports.add(js)

       if self.reqCss is not None:
         for css in self.reqCss:
           self.aresObj.cssImport.add(css)
    # Add the CSS dimension
    if width is not None:
      self.css({'width': "%s%s" % (width, widthUnit) })
    if height is not None:
      self.css('height', "%s%s" % (height, heightUnit))
    if htmlCode is not None and globalFilter is not None:
      self.filter(**globalFilter)

  @property
  def htmlId(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.htmlId
    :dsc:
      Python property to get a unique HtmlId for a given AReS Object
    :return: Javascript String of the variable used to defined the variable in Javascript
    """
    if self._code is not None:
      # This is a special code used to update components but not to store the results to the breadcrumb
      # Indeed for example for components like paragraph this does not really make sense to use the htmlCode
      return self._code

    if self.htmlCode is not None:
      return self.htmlCode

    return "%s_%s" % (self.__class__.__name__.lower(), id(self))

  @property
  def jqId(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jqId
    :dsc:
      Python property to get a unique Jquery ID function for a given AReS Object
    :return: Javascript String of the variable used to defined the Jquery object in Javascript
    """
    return "$('#%s')" % self.htmlId

  @property
  def jqDiv(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jqDiv
    :dsc:
      Python property to get a unique Jquery ID function for a given AReS Object (the div as the jqId might refer to the content)
    :return: Javascript String of the variable used to defined the Jquery object in Javascript
    """
    return "$('#%s')" % self.htmlId

  @property
  def val(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.val
    :returns: Javascript string with the function to get the current value of the component
    :dsc:
      Property to get the jquery value of the HTML object in a python HTML object.
      This method can be used in any jsFunction to get the value of a component in the browser.
      This method will only be used on the javascript side, so please do not consider it in your algorithm in Python
    """
    return '%s.val()' % self.jqId

  @property
  def contextVal(self):
    """
    :category: Javascript Event
    :rubric: JS
    :example: tableObj.contextVal
    :return: Javascript String with the value attached to the context menu
    :dsc:
      Set the javascript data defined when the context menu is created
    """
    return "{val: $(event.target).html()}"

  @property
  def jsQueryData(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsQueryData
    :dsc:
      Python function to define the Javascript object to be passed in case of Ajax call internally or via external REST service with other languages
    :return: Javascript String of the data to be used in a jQuery call
    :link ajax call: http://api.jquery.com/jquery.ajax/
    """
    return "{event_val: %s, event_code: '%s'}" % (self.jsVal, self.htmlId)

  @classmethod
  def jsMarkDown(cls, vals): return None

  def initVal(self, val):
    """
    :category: Python function
    :rubric: PY
    :example: >>> htmlObj.initVal( "Test" )
    :dsc:
      Python function to force the definition of the initial value of a component.
    The initial value should respect the self.vals expected by the object and this will vary accordingly
    """
    self.vals = val

  def attachMenu(self, contextMenuObj):
    """
    :category: Context Menu
    :rubric: PY
    :type: HTML
    :dsc:
      Attach a context menu to an existing component. A context menu must have a compnent attached to otherwise
      the report will not be triggered
    """
    contextMenuObj.source = self
    self.aresObj._contextMenu[self.jqDiv] = contextMenuObj

  # def contextMenu(self, pyData, isPyData=True):
  #   """ Display a context menu on the HTML component """
  #   #self.onDocumentLoadContextmenu()
  #   jsData = json.dumps(pyData) if isPyData else pyData
  #   self.aresObj.jsOnLoadFnc.add('''
  #     %(jqId)s.on('contextmenu', function(event) { event.stopPropagation(); $('#popup').css({ left: event.pageX + 1, top: event.pageY + 1 }) ; event.preventDefault();
  #         AresContextMenu(%(jqId)s, %(jsData)s, %(htmlId)s_markDownFnc ); }); ''' % {'pyCls': self.__class__.__name__, 'jqId': self.jqId, 'jsData': jsData, 'htmlId': self.htmlId})

  def addClass(self, cssCls):
    """
    :category: CSS function
    :rubric: CSS
    :example: myObj.addClass( 'btn-default' )
    :dsc:
      Add class to the AReS Html object. This function is used to add an existing CSS class to a component.
      Existing CSS class means that the definition is defined in one of the CSS external module used in the framework
    :links CSS class: https://www.w3schools.com/bootstrap/bootstrap_ref_all_classes.asp
    :return: The Python object itself
    """
    if not isinstance(cssCls, list):
      cssCls = [cssCls]
    for css in cssCls:
      if hasattr(css, 'classname'):
        css = css.classname
      self.attr['class'].add(css)
    return self

  def getClass(self):
    """
    :category: CSS function
    :rubric: CSS
    :example: myObj.getClass()
    :dsc:
      Returns a string with the CSS classes to be added to the HTML attribute. This will return all the HTML classes added to the component
      it can be Python Class generated from the CSS or internal CSS class coming from external modules
    :link HTML Classes: https://www.w3schools.com/html/html_classes.asp
    """
    return " ".join(self.attr['class'])

  def delClass(self, cssCls):
    """
    :category: CSS function
    :rubric: CSS
    :example: >>> myObj.delClass( 'btn-default' )
    :dsc:
      Remove a class from the list of CSS classes
    """
    self.attr['class'].pop(cssCls)

  def tooltip(self, value, location='top'):
    """
    :category: Javascript function
    :rubric: JS
    :example: htmlObj.tooltip("My tooltip", location="bottom")
    :dsc:
      Add the Tooltip feature when the mouse is over the component.
      This tooltip version is coming from Bootstrap
    :link Bootstrap: https://getbootstrap.com/docs/4.1/components/tooltips/
    :return: The Python object self
    """
    self.attr.update({'title': value, 'data-toggle': 'tooltip', 'data-placement': location})
    self.aresObj.jsFnc.add("%s.tooltip();" % self.jqId)
    return self

  def uitooltip(self, value, attrs=None, jsFncs=None, url=None, jsData=None, httpCodes=None, context=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: htmlObj.uitooltip(value)
    :example: t.uitooltip("Youpi", attrs={"position": { "my": "left+15 top", "at": "right center" }, "tooltipClass":'preview-tip'}, jsFncs=["alert() "])
    :example: t.uitooltip("Youpi", attrs={"position": { "my": "left+15 top", "at": "right center" }, "tooltipClass":'preview-tip'}, url="service.py")
    :example: t.uitooltip("Youpi", attrs={"track": True} )
    :dsc:
      Add the Tooltip feature when the mouse is over the component.
      This tooltip version is coming for Jquery UI.
      $.widget.bridge('uitooltip', $.ui.tooltip);
    :link Jquery: https://jqueryui.com/tooltip/#custom-content
    :link Ajax Jquery: https://stackoverflow.com/questions/13175268/ajax-content-in-a-jquery-ui-tooltip-widget
    :link Tooltip conflicts: https://stackoverflow.com/questions/13731400/jqueryui-tooltips-are-competing-with-twitter-bootstrap
    :return: The Python object self
    """
    self.attr.update({'title': value })
    if attrs is None:
      attrs = {}
    if jsFncs is not None:
      rec = ["k: %s" % json.dumps(v) for k, v in attrs.items()]
      rec.append("content: function(callback) { %s } " % ";".join(jsFncs))
      jsAttr = '{ %s }' % ", ".join(rec)
    elif url is not None:
      jsFncs = self.aresObj.jsPost(url, jsData, jsFnc="callback(data)", httpCodes=httpCodes, context=context)
      rec = ["k: %s" % json.dumps(v) for k, v in attrs.items()]
      rec.append("content: function(callback) { %s } " % jsFncs)
      jsAttr = '{ %s }' % ", ".join(rec)
    else:
      jsAttr = json.dumps(attrs)
    self.aresObj.jsFnc.add("%s.uitooltip( %s );" % (self.jqId, jsAttr ))
    return self

  def css(self, key, value=None):
    """
    :category: Javascript function
    :rubric: JS
    :param key: The key style in the CSS attributes (Can also be a dictionary)
    :param value: The value corresponding to the key style
    :return: The python object itself
    :link CSS Function: http://api.jquery.com/css/
    :dsc:
      Change the CSS Style of a main component. This is trying to mimic the signature of the Jquery css function
    """
    if value is None and isinstance(key, dict):
      # Do not add None value to the CSS otherwise it will break the page on the front end side
      cssVals = key if isinstance(key, dict) else {}
    else:
      cssVals = {key: value}
    for key, value in cssVals.items():
      if not 'css' in self.attr:
        # Convert the variable to something to be dump to javascript / CSS
        if isinstance(value, str):
          self.attr['css'] = {key: value}
        else:
          self.attr['css'] = {key: json.dumps(value)}
      else:
        self.attr['css'][key] = value
    return self

  def addAttr(self, name, value, isPyData=False):
    """
    :category: CSS function
    :rubric: CSS
    :example: myObj.addAttr("css', {'background-color': 'red'} )
    :example: myObj.addAttr("title", tooltip)
    :returns: The python object itself
    :dsc:
      Function to update the internal dictionary of object attributes. Those attributes will be used when the HTML component will be defined.
      Basically all sort of attributes can be defined here: CSS attributes, but also data, name...
    :link All Html attributes: https://www.w3schools.com/tags/ref_attributes.asp
    """
    if isPyData:
      value = json.dumps(value)
    if name == 'css':
      # Section for the Style attributes
      if not 'css' in self.attr:
        self.attr['css'] = dict(value)
      else:
        self.attr['css'].update(value)
    else:
      # Section for all the other attributes
      self.attr[name] = value
    return self

  def strAttr(self, withId=True, pyClassNames=None):
    """ Return the string line with all the attributes

    Important:
    all the attributes in the div should use double quote and not simple quote to be consistent everywhere in the framework
    and also in the javascript. If there is an inconsistency, the aggregation of the string fragments will not work
    """
    cssStyle, cssClass = '', ''
    if 'css' in self.attr:
      cssStyle = 'style="%s"' % ";".join(["%s:%s" % (key, val) for key, val in self.attr["css"].items()])
    classData = self.getClass()
    if 'class' in self.attr and classData:
      if pyClassNames is not None:
        # Need to merge in the class attrute some static classes coming from external CSS Styles sheets
        # and the static python classes defined on demand in the header of your report
        # self.aresObj.cssObj.getClsTag(pyClassNames)[:-1] to remove the ' generated in the module automatically
        cssClass = self.aresObj.cssObj.getClsTag(pyClassNames).replace('class="', 'class="%s ')
        cssClass %= classData
      else:
        cssClass = 'class="%s"' % classData
    elif pyClassNames is not None:
      cssClass = self.aresObj.cssObj.getClsTag(pyClassNames)
    if withId:
      return 'id="%s" %s %s %s' % (self.htmlId, " ".join(['%s="%s"' % (key, val) for key, val in self.attr.items() if key not in ('css', 'class')]), cssStyle, cssClass)

    return '%s %s %s' % (" ".join(['%s="%s"' % (key, val) for key, val in self.attr.items() if key not in ('css', 'class')]), cssStyle, cssClass)

  def info(self, text, icon="fa-question-circle"):
    """
    :category: HTML features
    :rubric: HTML
    :example: myObj.info('This will appear when the mouse is h')
    :returns: The python object itself
    :dsc:
      Set the html content to add a mak with some extra information when the mouse of hover
    :link awesome icon: https://fontawesome.com/icons
    :link bootstrap tooltip: https://getbootstrap.com/docs/4.1/components/tooltips/
    """
    self.aresObj.jsOnLoadFnc.add("$('sup').tooltip();")
    self.helper = '<sup title="%s" style="margin-left:5px;width:10px;display:inline"><i class="fas %s"></i></sup>' % (text, icon)
    return self

  def addGlobalVar(self, varName, jsDefinition=None, varDependencies=None, isPyData=None):
    """
    :category: Javascript Global variable
    :rubric: JS
    :wrap AresJsGlobals.JsGlobalVars: add
    :example: myObj.addGlobalVar('myVar', 'myValue', isPyData=True)
    :dsc:
      Add javascript global variables.
      Shortcut in each components to add global javascript variables. This is fully managed by the module AresJsGlobals but
      this shortcut is quite useful to add quickly variables
    """
    self.aresObj.jsGlobal.add(varName, jsDefinition, varDependencies, isPyData)

  def addGlobalFnc(self, fncName, fncDef, fncDsc=''):
    """
    :category: Javascript Global variable
    :rubric: JS
    :wrap AresJsGlobals.JsGlobalVars: fnc
    :dsc:
      Add a Javascript function in the global section in the report
      Important: all the attributes in the div should use double quote and not simple quote to be consistent everywhere in the framework
      and also in the javascript. If there is an inconsistency, the aggregation of the string fragments will not work. TO refer to
      an id with Jquery please use simple quotes to avoid clashes. for example use $('#id')
    """
    report_name = self.aresObj.run.report_name
    jsFnc = fncName.split('(')[0]
    if report_name in self.aresObj.aresFncs:
      if jsFnc in self.aresObj.aresFncs[report_name]:
        self.aresObj.aresFncs[report_name][jsFnc]['count'] += 1
        self.aresObj.aresFncs[report_name][jsFnc]['components'].add(self.__class__.__name__)
      else:
        moduleName = os.path.basename( sys.modules[self.__class__.__module__].__file__ )
        self.aresObj.aresFncs[report_name][jsFnc] = {'doc': fncDsc, 'time': 0, 'count': 1, 'language': 'javascript',
                                                     'components': set([self.__class__.__name__]), 'file': moduleName}
    else:
      moduleName = os.path.basename(sys.modules[self.__class__.__module__].__file__)
      self.aresObj.aresFncs.setdefault(report_name, {})[jsFnc] = {'doc': '', 'time': 0, 'count': 1, 'language': 'javascript',
                                                                  'components': set([self.__class__.__name__]), 'file': moduleName}
    self.aresObj.jsGlobal.fnc(fncName, fncDef)

  def onDocumentReady(self):
    """ Return the javascript calls to be returned to update the component """
    if self._jsStyles is not None:
      self.jsUpdateDataFnc = '''%(pyCls)s(%(jqId)s, %(htmlId)s_data, %(jsStyles)s) ; 
            if(%(htmlCode)s != null) { %(breadCrumVar)s['params'][%(htmlCode)s] = %(jsVal)s };
            ''' % {'pyCls': self.__class__.__name__, 'jqId': self.jqId, 'htmlId': self.htmlId, 'htmlCode': json.dumps(self.htmlCode),
                   'jsVal': self.val, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'jsStyles': json.dumps(self._jsStyles) }
    else:
      self.jsUpdateDataFnc = '''%(pyCls)s(%(jqId)s, %(htmlId)s_data) ; 
        if(%(htmlCode)s != null) { %(breadCrumVar)s['params'][%(htmlCode)s] = %(jsVal)s };
        ''' % {'pyCls': self.__class__.__name__, 'jqId': self.jqId, 'htmlId': self.htmlId, 'htmlCode': json.dumps(self.htmlCode),
               'jsVal': self.val, 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar}
    if self.dataSrc is None or self.dataSrc.get('type') != 'url':
      self.aresObj.jsOnLoadFnc.add(self.jsUpdateDataFnc)

  def onDocumentLoadVar(self):
    """ Return the variable to store in the global section of the javacript part """
    self.addGlobalVar(self.jsVal, json.dumps(self.vals, cls=AresJsEncoder.AresEncoder))
    if self.dataSrc is not None and self.dataSrc.get('type') == 'url':
      if 'time_out' in self.dataSrc:
        if self.dataSrc['time_out'] < 60:
          self.aresObj.notification('WARNING', 'Server Load',  'Process configured to run every %s seconds' % self.dataSrc['time_out'])

        self.aresObj.jsOnLoadFnc.add('''
          setInterval(function(){ 
            var params = {} ; for(var key in %(htmlCodes)s) { params[key] = %(breadCrumVar)s['params'][key] ;  }
            $.getJSON( "%(url)s", params, function( data ) { %(jsVal)s = data ; %(pyCls)s(%(jqId)s, %(htmlId)s_data) ; });
          }, %(time_out)s);
          ''' % {'pyCls': self.__class__.__name__, 'jqId': self.jqId, 'htmlId': self.htmlId, 'jsVal': self.jsVal,
                 'jsUpdateDataFnc': self.jsUpdateDataFnc, 'url': self.dataSrc['url'],
                 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'time_out': self.dataSrc['time_out'] * 1000,
                 'htmlCodes': json.dumps(self.dataSrc.get('htmlCodes', []))})
      else:
        self.aresObj.jsOnLoadFnc.add('''
          var params = {} ; for(var key in %(htmlCodes)s) { params[key] = %(breadCrumVar)s['params'][key] ;  }
          $.post( "%(url)s", params, function( data ) { %(jsVal)s = JSON.parse(data) ; %(pyCls)s(%(jqId)s, %(jsVal)s, %(jsStyles)s ) ; });
          ''' % {'pyCls': self.__class__.__name__, 'jqId': self.jqId, 'htmlId': self.htmlId, 'jsVal': self.jsVal,
                 'jsUpdateDataFnc': self.jsUpdateDataFnc, 'url': self.dataSrc['url'], 'jsStyles': json.dumps(self._jsStyles),
                 'breadCrumVar': self.aresObj.jsGlobal.breadCrumVar, 'htmlCodes': json.dumps(self.dataSrc.get('htmlCodes', [])) } )

  def onDocumentLoadFnc(self):
    """ Flag set to True by default to check if this function is overriden """
    self.isLoadFnc = False

  def onDocumentLoadContextmenu(self):
    """ Generic Javascript function to define a Contenxt Menu """
    self.aresObj.jsGlobal.fnc("AresContextMenu(htmlObj, data, markdownFnc)",
        '''
        $('#popup').empty() ; $('#popup').append('<ul style="width:100%%;height:100%%;margin:0;padding:0"></ul>') ;
        var listMenu = $('#popup').find('ul');
        data.forEach(function(rec){
          if ('title' in rec) {
            listMenu.append('<li class="list-group-item" style="cursor:cursor;width:100%%;display:inline-block;padding:5px 5px 2px 10px;font-weight:bold;color:white;background:%(color)s">' + rec.title + '</li> ');
          } else {
            if (rec.url != undefined) { var content = '<a href="' + rec.url + '" style="color:black">' + rec.label + '</a>' ;} else {var content = rec.label;};
            listMenu.append('<li class="list-group-item" style="cursor:pointer;width:100%%;display:inline-block;padding:2px 5px 2px 10px">' + content + '</li> '); }
        }) ;
        if (markdownFnc != false) {
          listMenu.append('<li class="list-group-item" style="cursor:cursor;width:100%%;display:inline-block;padding:5px 5px 2px 10px;font-weight:bold;color:white;background:%(color)s">MarkDown</li> ');
          listMenu.append('<li onclick="CopyMarkDown(\\''+ markdownFnc +'\\');" class="list-group-item" style="cursor:pointer;width:100%%;display:inline-block;padding:2px 5px 2px 10px"><i class="fas fa-thumbtack"></i>&nbsp;&nbsp;Copy MarkDown</li> ');};
        $('#popup').css({'padding': '0', 'width': '200px'}) ;
        $('#popup').show(); ''' % {'color': self.getColor('baseColor', 2)} )

  def notSelectable(self):
    """ Change the html Object to not be selectable """
    self.aresObj.jsOnLoadFnc.add(" %s.disableSelection();" % self.jqId)

  def onInit(self, htmlCode, dataSrc):
    if dataSrc['type'] == 'script':
      mod = importlib.import_module('%s.sources.%s' % (self.aresObj.run.report_name, dataSrc['script'].replace('.py', '')))
      httpParams = dict([(param, self.aresObj.http.get(param, '')) for param in dataSrc.get('htmlCodes', [])])
      recordSet = mod.getData(self.aresObj, httpParams)
      if 'jsDataKey' in dataSrc:
        recordSet = recordSet[dataSrc['jsDataKey']]
      return recordSet

    elif dataSrc['type'] == 'flask':
      if 'fncName' in dataSrc :
        mod = importlib.import_module('ares.%s' % dataSrc['module'])
        return json.loads(getattr(mod, dataSrc['fncName'])(*dataSrc.get('pmts', [])))
      else:
        return json.loads(dataSrc['fnc'](*dataSrc.get('pmts', []) ))

    elif dataSrc['type'] == 'url':
      # To think about the security here
      aresData = {'user_name': self.aresObj.user, 'report_name': self.aresObj.run.report_name, 'script_name': self.aresObj.run.script_name, 'host_name': self.aresObj.run.host_name}
      aresData.update( self.aresObj._run )
      response = urllib2.urlopen("%s%s" % (self.aresObj.run.url_root, dataSrc['url']), parse.urlencode( aresData ).encode("utf-8"))
      if dataSrc.get('jsDataKey') is not None:
        return json.loads(response.read().decode('utf_8'))['jsDataKey']
      try:
        return json.loads(response.read().decode('utf_8'))
      except Exception as err:
        self.aresObj.log("[%s] urlopen:%s%s" % (str(err), self.aresObj.run.url_root, dataSrc['url']), type='WARNING')
        return ""

  # ---------------------------------------------------------------------------------------------------------
  #                                          JAVASCRIPT STANDARD EVENTS
  #
  @property
  def eventId(self): return self.jqId

  def jsEvents(self):
    if hasattr(self, 'jsFncFrag'):
      for eventKey, fnc in self.jsFncFrag.items():
        if self.htmlCode is not None:
          fnc.insert(0, self.jsAddUrlParam(self.htmlCode, self.val, isPyData=False))
        self.aresObj.jsOnLoadEvtsFnc.add('''
          %(jqId)s.on('%(eventKey)s', function(event) {
            var useAsync = false; var data = %(data)s ; var returnVal = undefined;
            if (!$('#body_loading').length){ 
              var bodyLoading2 = $('<div id="body_loading" name="ares_loading" style="bottom:20px;left:70px;position:fixed;background-color:#F4F4F4;padding:5px"><i class="fas fa-spinner fa-spin" style="margin-left:10px;margin-right:10px"></i><div style="display:inline" id="loading_count">0</div> process running...</div>') ; 
            } ;
            $('body').append(bodyLoading2) ;
            $('#loading_count').html( parseInt($('#loading_count').html()) + 1) ;
            %(jsFnc)s ; 
            if (!useAsync) {
              $('#loading_count').html( parseInt($('#loading_count').html()) - 1) ;
              if ($('#loading_count').html() == '0') { $('#body_loading').remove() ;} }
            if (returnVal != undefined) { return returnVal } ; 
          }) ;''' % {'jqId': self.eventId, 'eventKey': eventKey, 'data': self.jsQueryData, 'jsFnc': ";".join([f for f in fnc if f is not None])})

  def click(self, jsFncs): return self.jsFrg('click', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def change(self, jsFncs): return self.jsFrg('change', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def drop(self, jsFncs): return self.jsFrg('drop', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def dragover(self, jsFncs): return self.jsFrg('dragover', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def dragleave(self, jsFncs): return self.jsFrg('dragleave', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def dragenter(self, jsFncs): return self.jsFrg('dragenter', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def dblclick(self, jsFncs): return self.jsFrg('dblclick', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def mouseup(self, jsFncs): return self.jsFrg('mouseup', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def blur(self, jsFncs): return self.jsFrg('blur', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def focusout(self, jsFncs): return self.jsFrg('focusout', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def keydown(self, jsFncs): return self.jsFrg('keydown', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def keypress(self, jsFncs): return self.jsFrg('keypress', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def keyup(self, jsFncs): return self.jsFrg('keyup', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)
  def hover(self, jsFncs): return self.jsFrg('hover', ";".join(jsFncs) if isinstance(jsFncs, list) else jsFncs)

  def trigger(self, event):
    """
    :category: Python event
    :rubric: PY
    :example: myObj.trigger('load')
    :dsc:
        Add the javascript code in order to trigger this event in the loading.
        Please be carreful as this event might not work as expected with on_init function as the service might return the data too late
    :link Jquery documentation: http://api.jquery.com/trigger/
    """
    self._triggerEvents.add('''%(jqId)s.trigger('%(event)s') ''' % {'jqId': self.eventId, 'event': event } )
    return self

  def paste(self, jsFnc):
    """ Generic click function """
    self.aresObj.jsOnLoadFnc.add('''%(jqId)s.on('paste', function(event) { 
       var data ;
       if (window.clipboardData && window.clipboardData.getData) { // IE
            data = window.clipboardData.getData('Text'); }
        else if (event.originalEvent.clipboardData && event.originalEvent.clipboardData.getData) { // other browsers
            data = event.originalEvent.clipboardData.getData('text/plain'); } 
        %(jsFnc)s 
      }) ;  ''' % {'jqId': self.jqId, 'jsFnc': jsFnc})

  def input(self, jsFnc): self.aresObj.jsOnLoadFnc.add("%(jqId)s.on('input', function(event) { %(jsFnc)s }) ; " % {'jqId': self.jqId, 'jsFnc': jsFnc})

  def filter(self, jsId, colName, allSelected=True, filterGrp=None):
    """
    :category: Data Transformation
    :rubric: JS
    :type: Filter
    :dsc:
      Link the data to the filtering function. The record will be filtered based on the composant value
    :return: The Python Html Object
    """
    if allSelected:
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {'allIfEmpty': []})[colName] = self.val
      self.aresObj.jsSources.setdefault(jsId, {})['filters']['allIfEmpty'].append(colName)
    else:
      self.aresObj.jsSources.setdefault(jsId, {}).setdefault('filters', {})[colName] = self.val
    return self

  # ---------------------------------------------------------------------------------------------------------
  #                                          JAVASCRIPT FRAGMENTS
  #
  @deprecated
  def ajax(self, url, data, method='POST', contentType='false', success=None, done=None, asyncCall=False):
    if method not in ['POST', 'GET']:
      raise Exception('Unsupported HTTP Method - %s - Please use only POST or GET')

    if not success:
      success = "alert('Request Successful !');"
    if contentType != 'false':
      contentType = "'%s'" % contentType

    dataLst = []
    if isinstance(data, dict):
      for key, val in data.items():
        dataLst.append("'%s' : %s" % (key, val))
      data = 'JSON.stringify([{%s}])' % ','.join(dataLst)
    return ''' 
              $.ajax({
                    url: "%s", method: "%s", data: %s, contentType: %s, cache: false, processData: false, async: %s
                }).done(function(data) {
                  %s
                }).fail(function(data) {
                  alert( "Request failed: " + data['statusText'] + ', Reason: ' + data['responseText'] );
                });''' % (url, method, data, contentType, json.dumps(asyncCall), success)

  def jsAddUrlParam(self, htmlCode=None, data=None, isPyData=True):
    """
    :category: Javascript function
    :rubric: JS
    :dsc:
      Add a parameter to the internal Javascript AReS object with all the object variables.
      THis will then be added to the URL when a new page is called
    """
    if htmlCode is None and data is None:
      htmlCode, data = self.htmlId, self.val
      # No Javascript conversion is done in this case as we are already in the Javascript
    else:
      if isPyData:
        data = json.dumps(data)
    return "%s['params']['%s'] = %s;" % (self.aresObj.jsGlobal.breadCrumVar, htmlCode, data)

  def jsToUrl(self):
    """
    :category: Javascript function
    :rubric: JS
    :dsc:
      Add the value of the existing HTML object to the internal Javascript AReS object with all the variables.
      THis will then be added to the URL when a new page is called.
      It is the same as jsAddUrlParam without parameters
    """
    return self.jsAddUrlParam(self.htmlId, self.val, isPyData=False )

  def jsToUrlReset(self):
    """
    :category: Javascript function
    :rubric: JS
    :dsc:
      Get the current URL without any extra parameters added automatically by the AReS Javascript Internal component.
      This will then refresh a report call to allow a user to start from scratch, without any pre selected parameters
    :return: A String with the URL
    """
    return "window.%s['url']" % self.aresObj.jsGlobal.breadCrumVar

  def jsGenerate(self, jsData='data', jsDataKey=None, isPyData=False, jsParse=False, jsStyles=None):
    """
    :param jsData: The javascript data dictionnary (or Python)
    :param jsDataKey: The key in the javascript data dictionnary (or Python)
    :param isPyData: A flag to apply a javascript conversion if this is not called from a jsXXX() method
    :param jsParse: A flag to parse the javascript function is it is coming from a json string for some reason
    :example: htmlObj.jsGenerate( {"test": True}, jsDataKey="test", isPyData=True)
    :category: Javascript features
    :dsc: Python function used to build a HTML component based on a common javascript definition
    :return: Javascript String with the different pieces and functions calls used to build the component
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsParse:
      jsData = "JSON.parse(%s)" % jsData

    if self._jsStyles is not None:
      if jsStyles is None:
        jsStyles = json.dumps(self._jsStyles)
      return '''
            if (%(jsDataKey)s != null) {
              if ( %(jsData)s[%(jsDataKey)s] !== false) { %(fncName)s( %(jsId)s, %(jsData)s[%(jsDataKey)s], %(jsStyles)s ) } }
            else { %(fncName)s( %(jsId)s, %(jsData)s, %(jsStyles)s ) }
            ''' % {'jsDataKey': json.dumps(jsDataKey), 'fncName': self.__class__.__name__, 'jsId': self.jqId,
                   'jsData': jsData, 'jsStyles': jsStyles }

    return '''
      if (%(jsDataKey)s != null) {
        if ( %(jsData)s[%(jsDataKey)s] != false) { %(fncName)s( %(jsId)s, %(jsData)s[%(jsDataKey)s] ) } }
      else { %(fncName)s( %(jsId)s, %(jsData)s ) }
      ''' % {'jsDataKey': json.dumps(jsDataKey), 'fncName': self.__class__.__name__, 'jsId': self.jqId, 'jsData': jsData}

  def jsUpdate(self, data, isPyData=True):
    """ Javascript function to update a component with a new val """
    self.onDocumentReady()
    self.onDocumentLoadVar()
    if isPyData:
      data = json.dumps(data)
    return "var %s = %s ; %s; " % (self.jsVal, data, self.jsUpdateDataFnc)

  def jsToggleAttr(self, type, value1, value2):
    """
    :category: Javascript function
    :rubric: JS
    :example: myObj.jsToggleAttr('class', 'alert-info', 'alert-danger')
    :dsc:
      Python wrapper to the javascript method to toggle the display of a component from an event
    :return: String representing the Javascript fragment with the event
    """
    return '''
      if ( $('#%(htmlId)s').attr('%(type)s') == '%(value1)s' ) { $('#%(htmlId)s').attr('%(type)s', '%(value2)s') }
      else { $('#%(htmlId)s').attr('%(type)s', '%(value1)s') }
      ''' % {'htmlId': self.htmlId, 'type': type, 'value1': value1, 'value2': value2}

  def jsToggle(self, delay=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: myObj.jsToggle(3000)
    :dsc:
      Python wrapper to the javascript method to change the display of the component using Jquery.
      The example will change change the display on an event after 3 seconds
    :link Jquery Documentation: http://api.jquery.com/toggle/
    :return: String representing the Javascript fragment with the event
    """
    return "%s%s.toggle()" % (self.jqId, '' if delay is None else '.delay(%s)' % delay)

  def jsSlideToggle(self, duration=None, delay=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: myObj.jsSlideToggle(5000)
    :dsc:
      Python wrapper to the javascript method to display or hide the matched elements with a sliding motion.
    :link Jquery Documentation: http://api.jquery.com/slidetoggle/
    :return: String representing the Javascript fragment with the event
    """
    jsDelay = '' if delay is None else '.delay(%s)' % delay
    if duration is None:
      return "%s%s.slideToggle()" % (self.jqId, jsDelay)

    return "%s%s.slideToggle(%s)" % (self.jqId, jsDelay, duration)

  def jsAnimate(self, duration, opacity=None, witdh=None, left=None, height=None, fontSize=None, top=None, delay=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: myObj.jsAnimate(0.25, "+=50")
    :dsc:
      Python wrapper to the javascript method to animate the object based on the attributes selected.
    :link Animate examples: https://www.w3schools.com/jquery/jquery_animate.asp
    :return: String representing the Javascript fragment with the event
    """
    prop = {}
    jsDelay = '' if delay is None else '.delay(%s)' % delay
    for name, attr in [("opacity", opacity), ("witdh", witdh), ("left", left), ("height", height), ("fontSize", fontSize),
                       ("top", top)]:
      if attr is not None:
        prop[name] = attr

    return "%s%s.animate( %s , '%s')" % (self.jqId, jsDelay, json.dumps(prop), duration)

  def jsHtml(self, jqId, jsData, isPydata=False):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.html("<b>My Test</b>")
    :dsc:
        Function to set on the Javascript side (during an event) the content of a component.
        With this function HTML content is possible and it will be correctly displayed
    :link W3C Documentation: https://www.w3schools.com/jquery/html_html.asp
    :return: String with the html function to set the HTML content of an element
    """
    if isPydata:
      jsData = json.dumps(jsData)
    return '''%s.html(%s)''' % (jqId, jsData)

  def jsSlideDown(self, duration=None, delay=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsSlideDown()
    :dsc:
      Python wrapper to the javascript method to change the display of the component using Jquery
    :return: A string representing the Javascript fragment to be added to the page
    :link W3C Documentation: https://www.w3schools.com/jquery/eff_slidedown.asp
    :link JQuery Documentation: http://api.jquery.com/slidedown/
    """
    jsDelay = '' if delay is None else '.delay(%s)' % delay
    if duration is None:
      return "%s%s.slideDown()" % (self.jqId, jsDelay)

    return "%s%s.slideDown(%s)" % (self.jqId, jsDelay, duration)

  def jsShow(self, duration=None, delay=None, inNestedStr=False):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsShow()
    :dsc:
        Function to show HTML elements with the javascript methods show()
    :return: A string representing the Javascript fragment to be added to the page
    :link W3C Documentation: https://www.w3schools.com/jquery/jquery_hide_show.asp
    :link JQuery Documentation: http://api.jquery.com/show/
    """
    jsDelay = '' if delay is None else '.delay(%s)' % delay
    if duration is None:
      val = "%s%s.show()" % (self.jqId, jsDelay)
    else:
      val = "%s%s.show(%s)" % (self.jqId, jsDelay, duration)
    if inNestedStr:
      val = val.replace('\'', '\\\'')
    return val

  def jsFadeIn(self, duration=None, delay=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsFadeIn()
    :dsc:
      Function to gradually change the opacity, for selected elements, from hidden to visible
    :return: A string representing the Javascript fragment to be added to the page
    :link W3C Documentation: https://www.w3schools.com/jquery/eff_fadein.asp
    :link JQuery Documentation: http://api.jquery.com/fadein/
    """
    jsDelay = '' if delay is None else '.delay(%s)' % delay
    if duration is None:
      return "%s%s.fadeIn()" % (self.jqId, jsDelay)

    return "%s%s.fadeIn(%s)" % (self.jqId, jsDelay, duration)

  def jsFadeOut(self, duration=None, delay=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsFadeOut()
    :dsc:
       Function to gradually change the opacity, for selected elements, from visible to hidden
    :return: A string representing the Javascript fragment to be added to the page
    :link W3C Documentation: https://www.w3schools.com/jquery/eff_fadeout.asp
    :link JQuery Documentation: http://api.jquery.com/fadeout/
    """
    jsDelay = '' if delay is None else '.delay(%s)' % delay
    if duration is None:
      return "%s%s.fadeOut()" % (self.jqId, jsDelay)

    return "%s%s.fadeOut(%s)" % (self.jqId, jsDelay, duration)

  def jsHide(self, duration=None):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsHide()
    :dsc:
        Function to hide HTML elements with the javascript methods hide()
    :return: A string representing the Javascript fragment to be added to the page
    :link W3C Documentation: https://www.w3schools.com/jquery/jquery_hide_show.asp
    :link JQuery Documentation: http://api.jquery.com/hide/
    """
    if duration is None:
      return "%s.hide()" % self.jqId

    return "%s.hide(%s)" % (self.jqId, duration)

  def jsAlert(self):
    """
    :category: Javascript function
    :example: >>> myObj.jsAlert()
    :rubric: JS
    :dsc:
      Function to wrap the Javascript method alert to display alert popup messages dedicating to this element.
      This will never be used during the Python run time. It can only be used in a Javascript event on the browser side
    :return: A String corresponding to the Javascript function to display alert popups
    :link Javascript documentation: https://www.w3schools.com/jsref/met_win_alert.asp
    """
    return "alert(%s)" % self.val

  def jsCopyClipboard(self):
    """
    :category: Javascript function
    :example: >>> aresObj.jsCopyClipboard()
    :rubric: JS
    :dsc:
      Get the element content copied to the clipboard.
    :return: A string representing the Javascript fragment to be added to the page
    :link Documentation: https://developer.mozilla.org/fr/docs/Web/API/Document/execCommand
    """
    return "document.execCommand('copy'); "

  def jsRemove(self):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsRemove()
    :dsc:
      Function to fully delete the element on the browser. The component will re appear when the report is refreshed
    :return: A string representing the Javascript fragment to be added to the page
    :link W3C Documentation: https://www.w3schools.com/jquery/jquery_dom_remove.asp
    :link JQuery Documentation: https://api.jquery.com/remove/
    """
    return '%s.remove()' % self.jqId

  def jsFrg(self, typeEvent, jsFnc):
    if typeEvent not in self.jsFncFrag:
      self.jsFncFrag[typeEvent] = []
    if isinstance(jsFnc, list):
      self.jsFncFrag[typeEvent].extend(jsFnc)
    else:
      self.jsFncFrag[typeEvent].append(jsFnc)
    return self

  def jsGoTo(self, url=None, isPyData=True):
    """
    :category: Javascript function
    :rubric: JS
    :example: >>> myObj.jsGoTo()
    :dsc:
      The href property sets or returns the entire URL of the current page.
    :return: A string representing the Javascript fragment to be added to the page to go to another web page
    :link W3C Documentation: https://www.w3schools.com/jsref/prop_loc_href.asp
    """
    if url is not None and isPyData:
      url = json.dumps(url)
    if url is None:
      return '%s location.href=buildBreadCrum() ;' % self.jsToUrl()

    return 'location.href=%s' % url

  # ---------------------------------------------------------------------------------------------------------
  #                                             CSS SECTION
  #
  def loadStyle(self):
    """
    :category: CSS function
    :rubric: CSS
    :dsc:
      Internal function in charge of loading the different CSS Python Styles attached to a component
    """
    if getattr(self, 'pyStyle', []) != []:
      for cssStyle in self.pyStyle:
        # Remove the . or # corresponding to the type of CSS reference
        # TODO think about a more efficient way to retrieve the CSS classes
        self.pyCssCls.add(self.aresObj.cssObj.add(cssStyle)[1:])

  @deprecated
  def jsProcess(self):
    return "%s.empty(); %s.append('%s')" % (self.jqId, self.jqId, self.aresObj.loading())

  def getColor(self, typeChart, i):
    """
    :category: CSS function
    :rubric: CSS
    :dsc:
      Python function to get the different pre defined color codes in the Framework
    :return: the hexadecimal code of the CSS color used in the CSS framework
    :link hexadecimal color: https://www.w3schools.com/colors/colors_picker.asp
    """
    return self.aresObj.cssObj.colorCharts[typeChart][i]

  def emptyStyle(self):
    """
    :category: CSS function
    :rubric: PY
    :dsc:
      CSS Style function to remove the default styles on a component
    """
    self.pyStyle = []

  def addCssStyle(self, clsNames):
    """
    :category: CSS function
    :rubric: CSS
    :dsc:
      Loads the extra CSS python classes - based on the CSS Classe Names - for this HTML object
    """
    self.pyStyle.extend(clsNames)
    return self

  def addPyCss(self, clsName, toMainStyle=True):
    """
    :category: CSS function
    :rubric: PY
    :example: myObj.addPyCss("PyCssClassName")
    :example: myObj.addPyCss("PyCssClassName", toMainStyle=False)
    :wrap CssBase.CssObj: add
    :dsc:
      This function will attached the CSS Python Class to the HTML element. It will return the component name.
      If the toMainStyle flag is set to true this class will be added to the container by default. Otherwise it will
      only create the CSS definition and the use has to be specified
    :return: A string with the CSS converted name
    """
    self.aresObj.cssObj.add(clsName)
    if toMainStyle:
      self.pyStyle.append(clsName)
    return self.aresObj.cssObj.pyRef(clsName)

  def getPyCss(self, clsName):
    """
    :category: CSS function
    :rubric: PY
    :wrap CssBase.CssObj: pyRef
    :example: >>> myObj.getPyCss('PyCssClassName')
    :dsc:
      Python Class to get the reference of a CSS Python class. This reference will be the one set in the CSS Section and the component should refer to it
    :return: A string with the CSS converted name
    """
    return self.aresObj.cssObj.pyRef(clsName)

  def _addToContainerMap(self, htmlObj):
    if hasattr(self, 'htmlMaps'):
      if hasattr(htmlObj, 'htmlMaps'):
        # It is a container and we need to get the mapping of the different components inside
        self.htmlMaps.update(htmlObj.htmlMaps)
      else:
        if getattr(htmlObj, 'htmlCode', None) is not None:
          if htmlObj.category == 'Table':
            self.htmlMaps[htmlObj.htmlCode] = (htmlObj.__class__.__name__, '%s_table' % htmlObj.htmlCode)
          elif htmlObj.category == 'Charts':
            self.htmlMaps[htmlObj.htmlCode] = ('PyChartJs', '$("#%s")' % htmlObj.htmlCode)
          else:
            self.htmlMaps[htmlObj.htmlCode] = (htmlObj.__class__.__name__, htmlObj.jqId)
        elif getattr(htmlObj, '_code', None) is not None:
          if htmlObj.category == 'Table':
            self.htmlMaps[htmlObj._code] = (htmlObj.__class__.__name__, '%s_table' % htmlObj._code)
          elif htmlObj.category == 'Charts':
            self.htmlMaps[htmlObj._code] = ('PyChartJs', '$("#%s")' % htmlObj._code)
          else:
            self.htmlMaps[htmlObj._code] = (htmlObj.__class__.__name__, htmlObj.jqId)

  # -------------------------------------------------------------------------------------------------------------------
  #                    OUTPUT METHODS
  # -------------------------------------------------------------------------------------------------------------------
  def __str__(self):
    """
    :category: Output function
    :rubric: PY
    :dsc:
      Apply the corresponding function to build the HTML result.
      This function is very specific and it has to be defined in each class.
    """
    raise NotImplementedError('subclasses must override __str__()!')

  def to_word(self, document):
    """
    :category: Output function
    :rubric: PY
    :link Python Module Documentation: http://python-docx.readthedocs.io/en/latest/
    :dsc:
      Apply the corresponding function to produce the same result in a word document.
      This function is very specific and it has to be defined in each class.
    """
    raise NotImplementedError('''
      subclasses must override to_word(), %s !
      Go to http://python-docx.readthedocs.io/en/latest/user/quickstart.html for more details  
    ''' % self.__class__.__name__)

  def to_xls(self, workbook, worksheet, cursor):
    """
    :category: Output function
    :rubric: PY
    :link Python Module Documentation: https://xlsxwriter.readthedocs.io/
    :dsc:
      Apply the corresponding function to produce the same result in a Excel document.
      This function is very specific and it has to be defined in each class.
    """
    raise NotImplementedError('''
      subclasses must override to_xls(), %s !
      Go to https://xlsxwriter.readthedocs.io/working_with_tables.html for more details  
    ''' % self.__class__.__name__)

  def html(self):
    """ Return the onload, the HTML object and the javascript events """
    self.loadStyle()
    self.jsEvents()
    # Update the HTML element with the values defined in the function call in the report
    self.onDocumentLoadFnc()
    if self.isLoadFnc:
      self.onDocumentLoadVar()
      self.onDocumentReady()

    contextlinks = []
    if self.references is not None:
      contextlinks.append( {'title': 'Useful Links'} )
      for label, url in self.references.items():
        contextlinks.append( {"label": label, "url": url} )

    # This is not needed in the pages by default
    markDown = None # self.jsMarkDown()
    if markDown is not None:
      self.addGlobalVar("%s_markDownFnc" % self.htmlId, json.dumps(markDown) )

      self.aresObj.jsGlobal.fnc("CopyMarkDown(jsMarkDown)",
          ''' 
          var textArea = $('<textarea />') ;
          $('body').append(textArea) ;
          textArea.text(jsMarkDown.split('&&').join('\\n')) ;
          $('body').append(textArea) ;
          textArea.select();
          document.execCommand('copy');
          textArea.remove(); 
          ''')
    else:
      self.addGlobalVar("%s_markDownFnc" % self.htmlId, json.dumps(False))

    #self.contextMenu(contextlinks)
    if self._triggerEvents:
      self.aresObj.jsOnLoadEvtsFnc.add(";".join(self._triggerEvents))
    if self.hidden == True:
      self.addAttr('css', {'display': 'none'})
    return str(self)

  def htmlContainer(self, component, flags):
    """
    :type: System
    """
    iconTable = self.aresObj.iconTable()
    iconTable.click([
                      "if( $('#%(htmlId)s_table').css('display') == 'none' ) { $('#%(htmlId)s_table').show() ; $('#%(htmlId)s').hide() ; } else { $('#%(htmlId)s_table').hide() ; $('#%(htmlId)s').show() ;} ;" % {
                        "htmlId": self.htmlId}])
    options = [iconTable.html()]
    if self.refresh:
      if self.scriptSrc is not None:
        r = self.aresObj.refresh()
        r.click(self.jsLoadFromSrc(''))
        options.append(r.html())
    if self.comment:
      t = self.aresObj.thumbtack("$('#%s_container')" % self.htmlId)
      options.append(t.html())
    if self.download:
      options.append(self.aresObj.upButton().html())
    if self.pdf:
      options.append(self.aresObj.pdf().html())
    if self.iconExcel:
      options.append(self.aresObj.excel().html())
    if self.magnify:
      options.append(str(self.aresObj.zoom()))
    remove = self.aresObj.remove()
    remove.click([self.jsRemove()])
    options.append(remove.html())
