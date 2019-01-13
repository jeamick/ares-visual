#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import os
import sys
import json
import importlib
import collections
import datetime
import time
import inspect
import logging
import types
import re

try:
  basestring
except NameError:
  basestring = str

from ares.Lib import AresImports
from ares.Lib.css import CssBase
from ares.Lib import html
from ares.Lib import js
from ares.Lib import graph
from ares.Lib import AresMarkDown
from ares.Lib.connectors import AresConn
from ares.Lib.connectors.files import AresFile
from ares.Lib.connectors.dbs import AresDbBase
from ares.Lib.AresImports import requires
from ares.widgets import Widget

import ares.doc
import ares.widgets
import ares.utils


def decFnc(fncUsed, language, fileFnc, reportName, fnc, env=None):
  fncUsed.setdefault( reportName, {})[ fnc.__name__ ] = {'doc': fnc.__doc__, 'time': 0, 'count': 0, 'language': language, 'components': set(),
                                                         'file': fileFnc, 'env': reportName if env is None else env}
  def wrapper(*args, **kwargs):
    startTime = time.time()
    res = fnc(*args, **kwargs)
    fncUsed[reportName][fnc.__name__]['time'] += time.time() - startTime
    fncUsed[reportName][fnc.__name__]['count'] += 1
    return res
  return wrapper


class Report(object):
  """
  :category: Ares Core
  :rubric: PY
  :type: class
  :dsc:
    ## ARES Report

    AReS is a suite of python Libraries allowing you to interact with any heterogeneous ecosystem in an **homogeneous** and **transparent** manner.
    No need to learn extra languages with Python and AReS you will be able to:

    >>>List
    &nbsp;&nbsp;AReS Interactions
    &nbsp;&nbsp;!(fas fa-check) Get data access from different sources (databases, text files, REST API...)
    &nbsp;&nbsp;!(fas fa-check) Transform your data using any mathematical libraries (Pandas, Numpy...)
    &nbsp;&nbsp;!(fas fa-check) Produce local and interactive web dashboards to visualise your data
    &nbsp;&nbsp;!(fas fa-check) Share your work on a server
    <<<

    The will of AReS is to stop fighting to slice and dice your data to prototype and then to get the good weapons to bring your work directly to production.

    #### Javascript and CSS Framework

    In AReS there is no need for extra Javascript and CSS modules everything is integrated.
    The AReS Python layer will allow you from Python to process your data but also transform your result to different **static** and **dynamic** formats.
    Thus if you want to share and centralise an interactive report it will generate rich HTML pages but it is also possible to share data in different format (ppt, word, csv, excel...)

    >>>List
    &nbsp;&nbsp;External Module Documentation
    &nbsp;&nbsp;[Jquery Documentation](https://jquery.com/)
    &nbsp;&nbsp;[Icons Documentation](https://fontawesome.com/icons?d=gallery)
    &nbsp;&nbsp;[ChartJs Documentation](https://www.chartjs.org/)
    &nbsp;&nbsp;[Plotly.js Documentation](https://plot.ly/javascript/)
    &nbsp;&nbsp;[C3.js Documentation](https://c3js.org/)
    &nbsp;&nbsp;[NVD3 Documentation](http://nvd3.org/)
    &nbsp;&nbsp;[D3 Documentation](https://d3js.org/)
    <<<

    #### Why this new Python Framework on top of Flask

    Python has a rich ecosystem, so it can be a glue to interact with different environments. Also the fact that the syntaxe is simple and easy it is much easier to get into this
    language. The learning curve of Python compared to other programming languages (Java, C++) is quite sharpe. If you are not really familliar with Python you can have a look at the below website to start with:

    >>>List
    &nbsp;&nbsp;Python Useful links
    &nbsp;&nbsp;[Python website](https://www.python.org/about/gettingstarted)
    &nbsp;&nbsp;[Python Tutorial](https://thehelloworldprogram.com/python/why-python-should-be-the-first-programming-language-you-learn/)
    <<<

    #### External Python Frameworks

    Also it is quite important to have a look at those websites to understand the underlying data object used in the Framework - jsDataFrame based on Pandas DataFrame.
    The documentation used to build the different components will be display in its documentation. This is just to ensure you can directly look for new features of bugs on internet.

    >>>List
    &nbsp;&nbsp;External Important Python libraries
    &nbsp;&nbsp;[SqlAlchemy Documentation](https://www.sqlalchemy.org/)
    &nbsp;&nbsp;[Pandas Tutorial](https://www.learnpython.org/en/Pandas_Basics)
    &nbsp;&nbsp;[Pandas to replace Excel](http://pbpython.com/excel-pandas-comp.html)
    &nbsp;&nbsp;[Pandas in 10 minutes](https://pandas.pydata.org/pandas-docs/stable/10min.html)
    <<<

    Then in this library, Flask Framework is used to allow the interactivity and the debugging of your code.
    The use of Javascript is very limited and embedded in the Python because it is just a way to translate the result of your code to be displayed to your Browser.

    Javascript is not considered in this framework, and by its author, as a programming language. It is used as CSS Style sheets like a way to display your final outputs.

    For any comments, feedbacks on the framework:

  :var cssObj: @doc<ares.Lib.css.CssBase.CssObj>
  :var jsOnLoadFnc: A list of javascript fragments which will be executed when the page will be loaded in the front end
  :var cache:
  :var run: @doc<AresCache.Run>

  """
  # This list should not be changed
  showNavMenu, withContainer = False, False

  def __init__(self, runDetails, appCache=None, sideBar=True, urlsApp=None):
    """ Instantiate the Ares object """
    self.run, self.user = runDetails, runDetails.current_user
    self.embedded_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'internal', 'db')
    self.cache, self._urlsApp = appCache, {'ares-incidents': '/incidents', 'ares-index': '/', 'ares-questions': '/questions', 'ares-notebook': '/notebook', 'ares-report': '/report', 'ares-transfer': '/transfer', 'ares-search': '/search'} if urlsApp is None else dict(urlsApp)
    self.timestamp, self.runTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), time.time() * 100
    self.countItems, self.countNotif, self.userGroups = 0, 0, {}
    self.content, self.shortcuts, self.exportCsv, self.jsSources = [], {}, {}, {}
    self.docBlocks, self._dbBindings, self._dbErrors, self._singleDb = {}, {}, collections.defaultdict(int), False
    self.currentTitleObj, self.navBarContent = {}, {'content': []}
    self.htmlItems, self.jsOnLoad, self.http, self.htmlCodes, self.htmlRefs = {}, [], {}, {}, {}
    self.notifications = collections.defaultdict(list)
    self.interruptReport, self._propagate = (False, None), []
    self.cssObj = CssBase.CssObj(self) # The variable with all the CSS style coming from the Python Framework
    self.cssObj.add('CssBody', cssRef='body')
    self.cssObj.add('CssAresContent', htmlId='ares_page_content')
    self.cssObj.add('CssAresLoadingBack', htmlId='popup_loading_back')
    self.cssObj.add('CssAresLoading', htmlId='popup_loading')

    self.dataSourceMonitor, self.aresUsage = {}, {'ares': {}}
    self.sourceDef, self.localFiles, self.libDef, self._run, self._scroll, self._contextMenu = {}, {}, {}, {}, set(), {}
    self.aresFncs = {}
    #
    self.jsGlobal, self.jsOnLoadFnc, self.jsWindowLoadFnc = js.AresJsGlobals.JsGlobalVars(self), ares.utils.OrderedSet.OrderedSet(), ares.utils.OrderedSet.OrderedSet()
    self.jsOnLoadEvtsFnc = ares.utils.OrderedSet.OrderedSet()

    self.jsGraphs, self.jsFnc, self.files = [], ares.utils.OrderedSet.OrderedSet(), {}
    self.jsImports, self.cssImport = set(), set()
    self.jsLocalImports, self.cssLocalImports = set(), set()
    self.workers, self.fileMap = {}, {}

    # Add Style default and Standard values in a given report
    self.ageReference, self.colorBase = 'red', 'green'
    self.pyStyleDfl = {'fontSize': '14px', 'headerFontSize': '16px'}

    # Automatically add the side bar if found for the current environment
    # The name of this moodule should follow the convention envName_sidebar.py
    # if report_name is not None:
    #
    # Try to load CSS Style overrides
    if self.run.report_name is not None:
      self.cssPyOvr()

    # Add generic framework AReS utilities
    for alias, fnc in ares.utils.AresFncs.create(self).items():
      argsFnc = fnc.__code__.co_varnames
      if 'aresObj' in argsFnc:
        setattr(self, alias, types.MethodType(decFnc(self.aresFncs, 'python', "", self.run.report_name, fnc), self))
      else:
        setattr(self, alias, decFnc(self.aresFncs, 'python', "", self.run.report_name, fnc))
    if sideBar and urlsApp is not None:
      self._sidebar = self.sidebar(links={}, dataSrc={'type': 'url', 'url': '%s/aresnavbar' % urlsApp['ares-report'], 'on_init': True}, servers=["http://127.0.0.1:5000/index"])
    else:
      self.jsOnLoadFnc.add("$('#footer').css('margin-left', '-35px')")
      self.jsOnLoadFnc.add("$('#ares_page_content').css('margin-left', '-35px')")

  def fncs(self, report_name=None, local_path=None):
    """
    :category: Bespoke User Functions
    :type: setter
    :rubric: PY
    :example: aresObj.youpi(3, 5) # direct call if the report is the current one
    :example: aresObj.fncs("examples").DataVals() # If the report is not the current one
    :dsc:
      Load the common functions available from an environments. Those injected functions are generic to the enviromnent and they
      can be used in both the service side and the report.
    :return: The aresObj with the enrich features
    """
    if report_name == self.run.report_name:
      return self

    # Load the set of functions from another folder
    if local_path is None:
      local_path = self.run.local_path
    fncsPath = os.path.join(local_path.replace(self.run.report_name, report_name), 'fncs')
    if os.path.exists(fncsPath):
      for fileFnc in os.listdir(fncsPath):
        if fileFnc.endswith('.py') and fileFnc != '__init__.py':
          mod = importlib.import_module('%s.fncs.%s' % (report_name, fileFnc.replace(".py", "")))
          functions_list = [o for o in inspect.getmembers(mod) if inspect.isfunction(o[1])]
          for fncName, fnc in functions_list:
            argsFnc = fnc.__code__.co_varnames
            if 'aresObj' in argsFnc:
              setattr(self, fncName, types.MethodType(decFnc(self.aresFncs, 'python', fileFnc, self.run.report_name, fnc), self))
            else:
              setattr(self, fncName, decFnc(self.aresFncs, 'python', fileFnc, self.run.report_name, fnc))
    return self

  def np(self):
    """
    :category: Numpy
    :rubric: PY
    :dsc:

    :return: Return the numpy module
    :link Numpy Documentation: https://docs.scipy.org/doc/numpy/user/quickstart.html
    """
    import numpy
    return numpy

  def db(self, dbFamily="sqlite", database=None, username=None, password=None, sharedDb=False, **kwargs):
    """
    :category: Databases
    :rubric: PY
    :dsc:
      Return the database available in each report. By default the database is specific for each user.
      Databases are not shared by default and this will ensure the security of the data.
      This interface is using SQLAlchemy
    :link SQLAlchemy: https://www.sqlalchemy.org/
    :example: >>> aresObj.db()
    :wrap class: ares.Lib.db.AresSql.SqlDb
    """
    if sharedDb:
      self._singleDb = True
    dbName = "SINGLEDB" if self._singleDb else database
    if database is None:
      if self.run.local_path is not None:
        if dbName is None:
          dbName = self.run.current_user
        database = '%s/%s_%s.db' % (self.run.local_path, self.run.report_name, self.hashId(dbName))
    if database not in self._dbBindings or kwargs.get('modelPath'):
      self._dbBindings[database] = AresDbBase.ConnDb(database=database, dbName=dbName, aresObj=self).get(dbFamily=dbFamily, username=username, password=password, **kwargs)
    # if not report_name in self._dbBindings:
    #   if self._singleDb:
    #     self._dbBindings[report_name] = AresSql.SqlDb(self, report_name, dbFamily, "SINGLEDB", database=database, username=username, password=password)
    #   else:
    #     self._dbBindings[report_name] = AresSql.SqlDb(self, report_name, dbFamily, database=database, username=username, password=password)
    return self._dbBindings[database]

  def imp(self, moduleName, report_name=None):
    """
    :category: Module loader
    :rubric: PY
    :type: import
    :dsc:
      dedicated function to import modules and check the security aspects.
      This function will allow the users restriction in some modules.
    :return: The python module
    """
    if report_name is None:
      return importlib.import_module(moduleName)

    return importlib.import_module('%s.%s' % (report_name, moduleName.replace(".py", "")))

  def breadCrumUrl(self, url, isPyData=True):
    """
    :category: BreadCrumb Definition
    :rubric: JS
    :dsc:
      Change the main url defined in the breacrumb. This will be the base url used when the
      url is requested from an HTML component.
    :example: >>> aresObj.breadCrumUrl("www.google.fr")
    """
    if isPyData:
      url = json.dumps(url)
    self.jsOnLoadFnc.add("%s['url'] = %s" % (self.jsGlobal.breadCrumVar, url))

  def jsScroll(self, htmlObj, animateAttrs, time=5000):
    """
    :category: Windows
    :rubric: JS
    :type: Event
    :dsc:
      Change the style of an object when the object appear on the viewPort in the browser

      window.onload = function() { $(window).scroll(function() {
      var position = $(window).scrollTop() + $(window).height();
      console.log($('#datatable_2194367215208').offset().top);
      console.log(">>" + position)})};
    :link Documentation: http://api.jquery.com/animate/
    """
    self._scroll.add("if(screenPos > %s.offset().top){%s.animate(%s, %s)};" % (htmlObj.jqDiv, htmlObj.jqDiv, json.dumps(animateAttrs), time))
    return self

  def jsBreadCrum(self):
    """
    :category: BreadCrumb Definition
    :rubric: JS
    :dsc:
      Return the javascript function to get the url from the breadcrumb.
      This url will be updated with all the selections performed in the report.
      This will allow the users to share the state of the report with other users
    :example: >>> aresObj.jsBreadCrum()
    """
    return 'buildBreadCrum()'

  def load(self, jsFnc, delay=None):
    if delay is not None:
      self.jsOnLoadFnc.add("setTimeout( function() { %s }, %s )" % ( jsFnc, delay) )
    else:
      self.jsOnLoadFnc.add(jsFnc)

  def notification(self, notifType, title, value, backgroundColor=None, closeButton=True, width=300, widthUnit='px', height=None, heightUnit=None):
    """
    :category: HTML function
    :example: >>> aresObj.notification('WARNING', 'Server URL not recognized', 'Please check')
    :rubric: HTML
    :dsc:
      Function to add when the python run some tags to put on the top of your report messages.
      The type of the messages can be different according to its criticallity.
      This is fully defined and driven in the Python and visible in the browser when the page is ready
    :return: Return the ARES Object corresponding to a notification
    :link Bootstrap documentation: https://getbootstrap.com/docs/4.0/components/alerts/
    """
    notif = notifType.upper()
    definedNotif = {'SUCCESS': 'SuccessAlert', 'INFO': 'InfoAlert', 'WARNING': 'WarningAlert', 'DANGER': 'DangerAlert'}
    if not notif in definedNotif:
      raise Exception("Notification Type should belong to one of the above category")

    alertObj = getattr(html.AresHtmlAlert, definedNotif[notif])(self, title, value, self.countNotif, width, widthUnit, height, heightUnit, closeButton, backgroundColor)
    self._propagate.append(alertObj)
    self.htmlItems[id(alertObj)] = alertObj
    self.content.append(id(alertObj))
    if notif == 'DANGER':
      self.interruptReport = (True, id(alertObj))  # we keep track of the object since this is the only thing we will display
    self.countItems += 1
    self.countNotif += 1
    return alertObj

  # Return the Python object
  def itemFromCode(self, htmlCode): return self.htmlCodes[htmlCode]

  def item(self, itemId): return self.htmlItems[itemId]

  def mocks(self, fncCall):
    """
    :category: Mock Data
    :rubric: PY
    :type: Documentation
    :example: aresObj.mocks('select')
    :dsc:
      Retrieve the mock data that an AReS HTML Component would expect.
      It it possible to call it and get the data by using the function call only. This will return an example (as complete as possible) that the component would expect
    """
    return ares.doc.docHtml.DocHtmlData.INPUTS.get(fncCall, None)


  # ---------------------------------------------------------------------------------------------------------
  #                                           PYTHON CACHING
  #
  # ---------------------------------------------------------------------------------------------------------
  def getCache(self, *args, **kwargs):
    """
    :category: Caching
    :rubric: PY
    :example: aresObj.getCache('test')
    :dsc:
      Get from the internal Flask Caching mechanism (Local files for the time being) the value stored.
      This cannot work perfectly locally as everytime that a script is updated the cache will be refreshed.
      So please used this feature only if you think that your code is nearly ready
    :return: The python object stored in the cache
    """
    return self.cache.get(*args, **kwargs)

  def addCache(self, *args, **kwargs):
    """
    :category: Caching
    :rubric: PY
    :example: aresObj.addCache('test', ['A', 'B'] )
    :dsc:
      Store to the internal Flask Caching mechanism (Local files for the time being) the value attached to the key.
      This cannot work perfectly locally as everytime that a script is updated the cache will be refreshed.
      So please used this feature only if you think that your code is nearly ready
    """
    self.cache.functionMap[args[0]] = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
    return self.cache.add(*args, **kwargs)

  def setCache(self, *args, **kwargs):
    """
    :category: Caching
    :rubric: PY
    :example: aresObj.setCache('test', ['A', 'B'] )
    :dsc:
      Function to update an existing cache
    """
    self.cache.functionMap[args[0]] = datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S')
    return self.cache.set(*args, **kwargs)


  # ---------------------------------------------------------------------------------------------------------
  #                                          DATA SOURCES OPERATIONS
  #
  # ---------------------------------------------------------------------------------------------------------
  def conn(self, source, **kwargs):
    """
    :category: Connector
    :rubric: PY
    :type: getter
    :dsc:
      Get the connector from the source.
      This allow the framework to interact with external systems.
    :return: The connector object
    """
    return AresConn.AresConn.getSource(source, self.run)(**kwargs)

  def getData(self, source, params=None, env='LIVE', htmlCode=None, toPandas=True, **kwargs):
    """
    :category: Connector
    :rubric: PY
    :rubric: Data retrieval
    :dsc:
      Retrieve data from a source system. The first parameter is the system code then the rest are parameters related to the
      request. Optional parameters like htmlCode and toPandas will store the results to a flat file in order to avoid
      having to get it from the source again. The temporary cached file will be store with the csv extention and the tab delimiter
    :return: A python object corresponding to the connector definition or a standard AReS Dataframe
    """
    if htmlCode is not None:
      df = self.file(filename="%s.csv" % htmlCode)
      if df.exists:
        try:
          self.localFiles[htmlCode] = {"subFolder": df.path.replace("\\", "/"), "filename": df.filename, 'timestamp': df.timestamp}
          return df.read(header=0, htmlCode=htmlCode, na_filter=False)

        except: pass

    startTime = time.time()
    # Normal way to retrieve a secured connector or some parameters
    sourceDef = self.sourceDef.get(source, {}).get(env, {})
    self.dataSourceMonitor.setdefault(source, {"count": 0, 'Total Run Time': 0, 'Read Time': 0, 'Write Time': 0})['count'] += 1
    kwargs['sourceDef'] = sourceDef
    kwargs['userContext'] = {"user": self.run.current_user, 'ip_address': self.run.host_name, 'mac_address': self.run.mac_address,
                             'lst_mod_dt': datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S'), 'groups': self.userGroups }
    try:
      kwargs['sourceDef']['is_local'] = self.run.is_local
      connCheck = AresConn.AresConn.getSource(source, self.run).isCompatible(kwargs['sourceDef'])
    except AttributeError:
      logging.exception('Source Not Defined: %s' % source)
      self.notification('DANGER', 'Source Call Failed', 'Source Not Defined: %s' % source)
      return self.df([])

    if connCheck[0]:
      data = AresConn.AresConn.getSource(source, self.run).getData(params, **kwargs)
      if data[0]:
        res = data[1]
        if toPandas:
          res = self.df(list(res), htmlCode=htmlCode)
          # Write only the data in a cached file if there is an htmlCode
          # No point to do this otherwise as the id generated will always be different
          if htmlCode is not None:
            res.save()
        self.dataSourceMonitor[source]['Total Run Time'] += (time.time() - startTime)
        self.dataSourceMonitor[source]['Read Time'] += (time.time() - startTime)
        return res

      # This return an empty list in case of issue and display the notification
      self.notification('DANGER', 'Source Call Failed', data[1])
    self.notification('DANGER', 'Source Call Failed', connCheck[1])
    return self.df([])

  def setData(self, source, table, records, updateRules=None, env='LIVE', **kwargs):
    """
    :category: Connector
    :rubric: PY
    :rubric: Data uploader
    :dsc:

    """
    sourceDef = self.sourceDef.get(source, {}).get(env)
    # Check some rules to ensure that the user is allowed to override the record
    # This is to ensure that the front end side cannot send non updated data to the server.
    discaredRows, rows = 0, []
    if updateRules is not None:
      for row in records:
        for col, val in updateRules.items():
          if row[col] != val:
            discaredRows += 1
            break

        else:
          rows.append(row)
    else:
      rows = records
    if source not in AresConn.AresConn.getSources() and sourceDef is not None:
      if '_ARES_TYPE' in sourceDef:
        source = sourceDef['_ARES_TYPE']
    self.dataSourceMonitor.setdefault(source, {"count": 0, 'Total Run Time': 0, 'Read Time': 0, 'Write Time': 0})['count'] += 1
    startTime = time.time()
    userContext = {"user": self.run.current_user, 'ip_address': self.run.host_name, 'mac_address': self.run.mac_address,
                   'lst_mod_dt': datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S'), 'groups': self.userGroups  }
    result = AresConn.AresConn.getSource(source, self.run).setData(table, rows, userContext, env, **kwargs)
    self.dataSourceMonitor[source]['Write Time'] += (time.time() - startTime)
    self.dataSourceMonitor[source]['Total Run Time'] += (time.time() - startTime)
    if not result[0]:
      self.notification('DANGER', 'Source Call Failed', result[1])

  def delData(self, source, table, condition, rowCount=1, env='LIVE'):
    """
    :category: Connector
    :rubric: PY
    :rubric: Data uploader
    :dsc:

    :return:
    """
    sourceDef = self.sourceDef.get(source, {}).get(env)
    if source not in AresConn.AresConn.getSources() and sourceDef is not None:
      if '_ARES_TYPE' in sourceDef:
        source = sourceDef['_ARES_TYPE']
    self.dataSourceMonitor.setdefault(source, {"count": 0, 'Total Run Time': 0, 'Read Time': 0, 'Write Time': 0})[
      'count'] += 1
    startTime = time.time()
    userContext = {"user": self.run.current_user, 'ip_address': self.run.host_name, 'mac_address': self.run.mac_address,
                   'lst_mod_dt': datetime.datetime.fromtimestamp( time.time() ).strftime('%Y-%m-%d %H:%M:%S') }
    result = AresConn.AresConn.getSource(source, self.run).delData(table, condition, rowCount, userContext)
    self.dataSourceMonitor[source]['Write Time'] += (time.time() - startTime)
    self.dataSourceMonitor[source]['Total Run Time'] += (time.time() - startTime)
    if not result[0]:
      self.notification('DANGER', 'Source Call Failed', result[1])


  # ---------------------------------------------------------------------------------------------------------
  #                                          JAVASCRIPT EVENTS SECTION
  #
  # ---------------------------------------------------------------------------------------------------------
  def jsAddToLocalStorage(self, key, jsData='data', jsDataKey=None, isPyData=False):
    """
    :category: Javascript function
    :example: >>> aresObj.jsAddToLocalStorage("lastname", "Smith", isPyData=True)
    :rubric: HTML5
    :dsc:
      Create a sessionStorage name/value pair with name="lastname" and value="Smith".
      This cache will be done in the javascript side directly in your browser
    :return: A String corresponding to the Javascript function to add a variable the session storage.
    :link Javascript documentation: https://www.w3schools.com/jsref/prop_win_sessionstorage.asp
    """
    if isPyData:
      jsData = json.dumps(jsData)
    if jsDataKey is not None:
      jsData = "%s.%s" % (jsData, jsDataKey)
    return "window.sessionStorage.setItem('%s', JSON.stringify(%s));" % (key, jsData)

  def jsClearLocalStorage(self):
    """
    :category: Javascript function
    :example: >>> aresObj.jsClearLocalStorage()
    :rubric: HTML5
    :dsc:
      Clear all the data stored in the browser.
    :return: A String corresponding to the Javascript function to clear a session storage.
    :link Javascript documentation: https://www.w3schools.com/jsref/prop_win_sessionstorage.asp
    """
    return "window.sessionStorage.clear();"

  def jsGetFromLocalStorage(self, key, jsDataKey=None):
    """
    :category: Javascript function
    :example: >>> aresObj.jsGetFromLocalStorage("lastname")
    :rubric: HTML5
    :dsc:
      Return on the browser side the value corresponding to the requested key in the session storage.
    :return: A String corresponding to the Javascript function to get value from the session storage.
    :link Javascript documentation: https://www.w3schools.com/jsref/prop_win_sessionstorage.asp
    """
    if jsDataKey is not None:
      return "JSON.parse(window.sessionStorage.getItem('%s'))['%s']" % (key, jsDataKey)

    return "JSON.parse(window.sessionStorage.getItem('%s'))" % key

  def jsWait(self, jsFnc, timeInMilliSeconds):
    """
    :category: Javascript function
    :example: >>> aresObj.jsWait( aresObj.jsConsole(), 3000)
    :type: javascript wrapper
    :rubric: JS
    :dsc:
      Function to delay an event by the number of milliseconds defined
    :return: A String corresponding to the Javascript function to delay an event
    :link Javascript documentation: https://www.w3schools.com/jsref/met_win_settimeout.asp
    """
    self.aresObj.jsOnLoadFnc.add( "setTimeout(function(){ %s }, %s);" % (jsFnc, timeInMilliSeconds) )

  def jsInterval(self, jsFnc, timeInMilliSeconds):
    """
    :category: Javascript function
    :example: >>> aresObj.jsInterval( aresObj.jsConsole(), 3000)
    :type: javascript wrapper
    :rubric: JS
    :dsc:
      This method calls a Javascript function at specified intervals (in milliseconds).
    :return: A String corresponding to the Javascript function to the interval function
    :link Javascript documentation: https://www.w3schools.com/jsref/met_win_setinterval.asp
    """
    self.aresObj.jsOnLoadFnc.add( "var interval_%s = setInterval(function(){ %s }, %s);" % (id(jsFnc), jsFnc, timeInMilliSeconds) )
    return id(jsFnc)

  def jsClearInterval(self, intervalId):
    """
    :category: Javascript function
    :example: >>> aresObj.jsClearInterval( intervalId )
    :type: javascript wrapper
    :rubric: JS
    :dsc:
      This method will definitely remove the repetitive call of a javascript method. This can be triggered by a button to
      stop checking the updates of something
    :return: A String corresponding to the Javascript function to clear the interval function defined.
    :link Javascript documentation: https://www.w3schools.com/jsref/met_win_setinterval.asp
    """
    return "interval_%s.clearInterval();" % intervalId

  def jsDownload(self, filename, jsData, jsDataKey=None, isPyData=False):
    """
    :category: Javascript function
    :example: >>> aresObj.click( aresObj.jsDownload("test.dat", "ddd\nefezfe\nfeff", isPyData=True)
    :type: javascript wrapper
    :rubric: JS
    :dsc:
      Function to download a file from the javascript layer. The content of the file might be comping from an ajax call
    :return:
    """
    if isPyData:
      jsData = json.dumps(jsData)
    elif jsDataKey is not None:
      jsData = "%s['%s']" % (jsData, jsDataKey)
    return '''
      $('body').append( $("<a id='js_download' download='%(fileName)s' type='text/csv'></a>" ) );  
      $('#js_download').attr('href', 'data:text/csv;base64,' + btoa(%(jsData)s) ).get(0).click() ;
    ''' % {"fileName": filename, 'jsData': jsData}

  def keyboard(self, jsCodeConditions, action, isKey=True):
    """
    :category: Keyboard
    :example: >>> aresObj.keyboard(39, aresObj.jsAlert() )
    :rubric: JS
    :type: javascript wrapper
    :dsc:
      Add a shortcut on some events in the report. The example will trigger an alert on click on the right arrow
    :link Javascript documentation: http://chief.over-blog.com/article-raccourcis-clavier-en-javascript-jquery-69187878.html
    :return: The Python object itself
    """
    if isKey is not None:
      self.shortcuts["(e.keyCode || e.which) == %s" % jsCodeConditions] = action
    else:
      self.shortcuts[jsCodeConditions] = action
    return self

  def jsMail(self, htmlObjTo, htmlObjSubject, htmlObjContent, HtmlMailCategory=None, jsFnc=''):
    """
    :category: Email
    :example: >>> aresObj.jsMail(  )
    :rubric: JS
    :dsc:
      Function to send emails directly from the platform
      For security reasons this function can only works on local instances of AReS.
      This function will trigger an Ajax call (POST) to the server to send an email.
    :return: The Javascript string corresponding to the Ajax call
    :link Ajax Documentation: https://api.jquery.com/jquery.post/
    """
    # Convert the different fields as they can be hard coded in the report
    to = htmlObjTo if isinstance(htmlObjTo, basestring) else htmlObjTo.val # Might be a javascript object
    subject = json.dumps(htmlObjSubject) if isinstance(htmlObjSubject, basestring) else htmlObjSubject.val
    content = json.dumps(htmlObjContent) if isinstance(htmlObjContent, basestring) else htmlObjContent.val

    if HtmlMailCategory is None:
      jsParameters = "to: %s, subject: %s, content: %s" % (to, subject, content)
    else:
      category = json.dumps(HtmlMailCategory) if isinstance(HtmlMailCategory, basestring) else HtmlMailCategory.val
      jsParameters = "to: %s, subject: %s, content: %s, category: %s" % (to, subject, content, category)
    return self.jsPost('/reports/mail/%s/%s' % (self.run.report_name, self.run.script_name), jsParameters, jsFnc, isPyData=False)

  def jsClipboard(self):
    """
    :category: Clipboard
    :example: >>> aresObj.jsClipboard()
    :restricted browser: IE
    :rubric: JS
    :dsc:
      Get the data copied to the clipboard from external sources.
      This only work with Internet explorer for the time being
    :link Compatibility issues: https://stackoverflow.com/questions/36270886/event-clipboarddata-setdata-in-copy-event
    :return: Returns within a Javascript event the data stored in the clipboard
    """
    return "GetClipBoardData(event)"


  # ---------------------------------------------------------------------------------------------------------
  #                                          AJAX SECTION
  #
  # The below three methods are dedicated to interactively query the server. So there is not way to test it
  # fully locally. The only way to get it would be to upload the ajax scripts to the server and to test the
  # call from the local report
  #   - The GET method to pass variables in the URL
  #   - The POST method to pass variables in the call
  #   - The Json when the transfer is done using json type of data
  # ---------------------------------------------------------------------------------------------------------
  def jsGet(self, url, jsData=None, jsFnc='', cacheObj=None, isPyData=True, isDynUrl=False, httpCodes=None,
            htmlCodes=None, datatype='json', context=None, debug=False):
    """
    :category: AJAX
    :example: >>> aresObj.jsGet('Test.py')
    :type: jquery wrapper
    :rubric: JS
    :dsc:
        Create a dedicated thread to query a specific function outside of the page (Internal to AReS by also external services).
        This will return some data which can then be used to update the existing HTML Objects.
        This is a way to update component in the page without having to reload the full page (it saves time and ressources)
    :link Ajax documentation: https://www.w3schools.com/xml/ajax_intro.asp
    :link Ajax Jquery Get: https://api.jquery.com/jquery.get/
    :return: A String with the Ajax Jquery function
    """
    return self.__jsQuery(url, jsData, jsFnc, 'get', cacheObj, isPyData, isDynUrl, httpCodes, htmlCodes, datatype, context, debug)

  def jsPost(self, url, jsData=None, jsFnc='', cacheObj=None, isPyData=True, isDynUrl=False, httpCodes=None,
             htmlCodes=None, datatype='json', context=None, debug=False):
    """
    :category: AJAX
    :example: >>> aresObj.jsPost('Test.py')
    :type: jquery wrapper
    :rubric: JS
    :dsc:
      Create a dedicated thread to query a specific function outside of the page (Internal to AReS by also external services).
      This will return some data which can then be used to update the existing HTML Objects.
      This is a way to update component in the page without having to reload the full page (it saves time and ressources)
    :link Ajax documentation: https://www.w3schools.com/xml/ajax_intro.asp
    :link Ajax Jquery POST: https://api.jquery.com/jquery.post/
    :return: A String with the Ajax Jquery function
    """
    return self.__jsQuery(url, jsData, jsFnc, 'post', cacheObj, isPyData, isDynUrl, httpCodes, htmlCodes, datatype, context, debug)

  def jsJson(self, url, jsData=None, jsFnc='', cacheObj=None, isPyData=True, isDynUrl=False, httpCodes=None,
             htmlCodes=None, datatype='json', context=None, debug=None):
    """
    :category: AJAX
    :example: >>> aresObj.jsJson('Test.py')
    :type: jquery wrapper
    :rubric: JS
    :dsc:
      Create a dedicated thread to query a specific function outside of the page (Internal to AReS by also external services).
      This will return some data which can then be used to update the existing HTML Objects.
      This is a way to update component in the page without having to reload the full page (it saves time and ressources)
    :link Ajax documentation: https://www.w3schools.com/xml/ajax_intro.asp
    :link Ajax Jquery JSON: https://api.jquery.com/jquery.getjson/
    :return: A String with the Ajax Jquery function
    """
    return self.__jsQuery(url, jsData, jsFnc, 'getJSON', cacheObj, isPyData, isDynUrl, httpCodes, htmlCodes, datatype, context, debug)

  def __jsQuery(self, url, jsData, jsFnc, jqFnc, cacheObj, isPyData, isDynUrl, httpCodes, htmlCodes, datatype, context, debug):
    """
    :category: AJAX
    :rubric: JS
    :type: System
    :dsc:
      Based function for all the different types of Ajax queries in the framework. In order to simplify the way events are handled and process only a single function has been created to allow both types (POST and GET).
      A standardise and common way to retrieve the data from the different methods is defined to make easier the link with the different components.
      Everything is dictionary based and some system keys are used to keep track of the request.
    """
    self._run['_ares_service_type'] = '"URL"'
    if isinstance(jqFnc, list):
      jqFnc = ";".join(jqFnc)

    if "/" not in url and url.endswith(".py"):
      url = "%s/data/%s/%s" % (self._urlsApp['ares-report'], self.run.report_name, url.split(".")[0])
      self._run['_ares_service_type'] = '"PYTHON_LOCAL"'
    jsResults = []
    if isinstance(jsFnc, list):
      jsFnc = ";".join(jsFnc)
    if isPyData and jsData is not None:
      jsResults = []
      for htmlObj in jsData:
        if htmlObj == 'data':
          jsResults.append("'event': JSON.stringify(data)")
          continue

        if htmlObj._code is not None:
          if hasattr(htmlObj, 'json'):
            jsResults.append("%s: %s" % (htmlObj._code, htmlObj.json))
          else:
            jsResults.append("%s: %s" % (htmlObj._code, htmlObj.val))
          continue

        if htmlObj.htmlCode is None:
          raise Exception('Please defined an HTML Code for this object %s' % htmlObj)

        if hasattr(htmlObj, 'json'):
          # This is a very special object like a datatable and we cannot store the results in the breadcrumb
          jsResults.append("%s: %s" % (htmlObj.htmlCode, htmlObj.json))
        else:
          jsResults.append("%s: %s['params']['%s']" % (htmlObj.htmlCode, self.jsGlobal.breadCrumVar, htmlObj.htmlCode))
    elif jsData is not None:
      jsResults.append(jsData)
    if context is not None:
      for key, val in context.items():
        jsResults.append("%s:%s" % (key, json.dumps(val)))
    if cacheObj is not None:
      for key, val in cacheObj.items():
        jsResults.append("%s:%s" % (key, json.dumps(val)) )
    if httpCodes is None:
      httpCodes = []
    jsResults.append("_ares_single_db: %s" % json.dumps(self._singleDb) )
    if htmlCodes is not None:
      logging.warn('#########################################')
      logging.warn('htmlCodes should not be used, replace by httpCodes')
      logging.warn('#########################################')
      httpCodes = htmlCodes

    # Add the integer ID of the current run
    for runKey, runVals in self._run.items():
      jsResults.append("%s:%s" % (runKey, runVals))
    jsData = " { %s }" % ','.join(jsResults)
    if not isDynUrl:
      url = '"%s"' % url
    startDebug, endDebug = '', ''
    if debug:
      debugTime = int(time.time())
      startDebug = [
        "console.log('')", "console.log('**************************')", "console.log('Ajax call: %s, input parameters')" % url,
        "console.log(data)", 'var t_%s = performance.now();' % debugTime]
      endDebug = ["console.log('Processing time: '+ (performance.now()-t_%s) + 'ms')" % debugTime, "console.log(data)"]
    return '''
      useAsync = true;
      if (typeof data === 'undefined') {data = {}};
      %(htmlCodes)s.forEach(function(code) {data[code] = %(breadCrumVar)s['params'][code]});
      var url = %(url)s; for (k in %(jsData)s) {data[k] = %(jsData)s[k]}; %(startDebug)s;
      if (url.startsWith("http")) {var dataToSend = %(jsData)s; dataToSend['url'] = url; $.%(jqFnc)s("%(urlReport)s/rest", dataToSend, function(data) { %(jsFnc)s } )}
      else {$.%(jqFnc)s(url, data, function(data) {var displayTime = 6000;
          if (data.popup_info != undefined) {
            if($("#info").length != 0) { $('#info').remove() }; colorPopup = '#293846' ; colorText = 'white';
            if(data.ares_status != undefined) { if (data.ares_status == 'error') { displayTime = 60000 ;  colorPopup = '#C00000' } else if (data.ares_status == 'warning') { colorPopup = '#FFA500'; colorText = 'black' ; } } ;  
            $('body').append("<div id='info' style='position:fixed;left:50;bottom:10px;z-index:100;background:" + colorPopup + ";padding:10px;color:"+ colorText +"'><i class='fas fa-times-circle' onclick='$(this).parent().remove()' style='cursor:pointer;margin-right:5px'></i>"+ data.popup_info +"</div>"); 
            $('#info').fadeOut(displayTime, function() {$('#info').remove()})}
          
          if (typeof loading != 'undefined') {loading.hide()};
          if (data.error != undefined) {alert(data.error)}
          else if(data.ares_status == 'error') {
            $('#loading_count').html(parseInt($('#loading_count').html()) - 1);
            if ($('#loading_count').html() == '0') {$('#body_loading').remove()};
            %(jsFnc)s}
          else if(data.ares_status == 'stop') {
            $('#loading_count').html( parseInt($('#loading_count').html()) - 1);
            if ($('#loading_count').html() == '0') { $('#body_loading').remove()}}
          else {%(jsFnc)s;
            $('#loading_count').html( parseInt($('#loading_count').html()) - 1);
            if ($('#loading_count').html() == '0') { $('#body_loading').remove()}};
          %(endDebug)s
          }, %(datatype)s)}
      ''' % {'url': url, 'jqFnc': jqFnc, 'jsData': jsData, 'jsFnc': jsFnc, 'htmlCodes': httpCodes, 'urlReport': self._urlsApp['ares-report'],
             'breadCrumVar': self.jsGlobal.breadCrumVar, 'datatype': json.dumps(datatype), "startDebug": ";".join(startDebug), "endDebug": ";".join(endDebug)}

  def preload(self, ajaxParams):
    """
    :category: AJAX
    :rubric: JS
    :dsc:
      Preload feature to be able to produce pre cached files.
      Those files will be produced in a asynchrone way and they will facilitate the fluidity in the web dashboard.
      The success file is only used as an indicator to check if the preload function has to be started. If the file is already present it will not be triggered.
      The status will be based on the return of the service in the query return (true / false
    :tip: Put a variable result to your service return in order to change the icon according to the status of your asynchronous call
    :example: aresObj.preload( [ { 'url': "Test.py", 'success': 'test.csv'} ] )
    :return: The Python object itself
    """
    filesUsed = []
    for i, ajaxParam in enumerate(ajaxParams):
      if not self.file(ajaxParam['success']).exists():
        filesUsed.append( '<div><i id="preload_%s" class="fas fa-spinner fa-spin" style="color:#56a2af"></i>&nbsp;&nbsp;Cache for <b>%s</b></div>' % (i, ajaxParam['success']) )
        self.jsOnLoadEvtsFnc.add( self.jsPost( ajaxParam['url'], ajaxParam.get("jsData"), "if (data.result) { $('#preload_%(id)s').attr('class', 'fas fa-check'); $('#preload_%(id)s').css('color', 'green') } else { $('#preload_%(id)s').attr('class', 'fas fa-times'); $('#preload_%(id)s').css('color', 'red') } " % {'id': i} , isPyData=ajaxParam.get('isPyData', True), httpCodes=ajaxParam.get('httpCodes')) )
    if len(filesUsed) > 0:
      self.notification('INFO', "Preload files", "".join(filesUsed), width=350 )
      if len(ajaxParams) > 1:
        self.countNotif += int(len(ajaxParams)/2)
    return self

  def jsAjax(self, url, data="data", success="", method='POST', contentType='false', asyncCall=False, isDynUrl=False):
    """
    :category: AJAX
    :rubric: JS
    :warning: Deprecated
    :dsc:

    :link Jquery Documentation: http://api.jquery.com/jquery.ajax/
    :return: A String with the Ajax Jquery function
    """
    if method not in ['POST', 'GET']:
      raise Exception('Unsupported HTTP Method - %s - Please use only POST or GET')

    if contentType != 'false':
      contentType = "'%s'" % contentType
    dataLst = []
    if isinstance(data, dict):
      for key, val in data.items():
        dataLst.append("'%s' : %s" % (key, val))
      data = 'JSON.stringify([{%s}])' % ','.join(dataLst)

    if not isDynUrl:
      url = '"%s"' % url
    return ''' 
      $.ajax({ url: %(url)s, method: "%(method)s", data: %(data)s, contentType: %(contentType)s, cache: false, processData: false, async: %(async)s })
       .done(function(data) { data = JSON.parse(data) ;
          if (data.popup_info != undefined) {
            if($("#info").length != 0) { $('#info').remove() }; colorPopup = '#293846' ; colorText = 'white';
            if(data.ares_status != undefined) { if (data.ares_status == 'error') { colorPopup = '#C00000' } else if (data.ares_status == 'warning') { colorPopup = '#FFA500'; colorText = 'black' ; } } ;  
            $('body').append("<div id='info' style='position:fixed;left:50;bottom:10px;z-index:100;background:" + colorPopup + ";padding:10px;color:"+ colorText +"'>"+ data.popup_info +"</div>"); 
            $('#info').fadeOut(6000, function() { $('#info').remove() } ) ; }
          
          if (typeof loading != 'undefined') { loading.hide() ; }
          if (data.error != undefined) { alert(data.error) ; }
          else { %(jsFnc)s }
          
          $('#loading_count').html( parseInt($('#loading_count').html()) - 1) ;
          if ($('#loading_count').html() == '0') { $('#body_loading').remove() ; }
          
      });
      ''' % {'url': url, "method": method, "data": data, "contentType": contentType, "async": json.dumps(asyncCall), 'jsFnc': success}

  def jsGoTo(self, url, urlName='_self', jsData='data', isRow=False, httpCodes=None, isPyData=False):
    """
    :category: Redirection
    :example: >>> aresObj.jsGoTo('/reports/run/timetracking/ChartTest', httpCodes=['COB'] )
    :rubric: JS
    :type: javascript wrapper
    :dsc:
        Return the Javascript string to go to another pages with all the expected get parameters.
        This will ensure that the new page will directly focus on the information highlighted by the first page.
    :link Javascript documentation: https://www.w3schools.com/jsref/met_win_open.asp
    :return: Return the javascript fragment to go to another web page
    """
    if isRow:
      jsData = "JSON.parse(%s.row)" % jsData
    if isPyData:
      url = json.dumps(url)
    return '''
      var htmlCodes = %(httpKeyCodes)s; var NO_UNLOAD = true;
      if (htmlCodes != null){
        var rowData = %(jsData)s; var urlPmts = [];
        for (var key in htmlCodes) { urlPmts.push( htmlCodes[key] + "="+ rowData[key] ) ; };
        window.open( %(url)s + '?' + urlPmts.join("&"), '%(urlName)s'); $("div[name='ares_loading']").hide() ;}
      else { window.open( %(url)s, '%(urlName)s') ; $("div[name='ares_loading']").hide() ; };
      ''' % {'httpKeyCodes': json.dumps(httpCodes), 'jsData': jsData, 'url': url, 'urlName': urlName }

  def jsReloadPage(self):
    """
    :category: Redirection
    :rubric: JS
    :type: javascript wrapper
    :example: >>> myObj.jsReloadPage()
    :dsc:
        The Javascript function to reload the page on the client side
    :return: The javascript function as a String
    :link W3C Documentation: https://www.w3schools.com/jsref/met_loc_reload.asp
    """
    return 'location.reload()'

  def jsSubmitForm(self, url, aresObjs=None, isPyData=True, method="POST"):
    """
    :category: Redirection
    :rubric: JS
    :type: javascript wrapper
    :example: >>> myObj.jsSubmitForm( "/reports/run/lab/AresNoteBook", [('content', self.vals)])  )
    :dsc:
      Create a HTML Like form before submitting the POST request and go to the next page.
      This will allow you to go to another page without having to pass all the parameters from a GET and make them visible in the url
    :return: Return the javascript fragment to go to another web page
    """
    if isPyData:
      url = json.dumps(url)

    inputs = []
    if aresObjs is not None:
      for aresObj in aresObjs:
        if isinstance(aresObj, tuple):
          if isinstance(aresObj[1], basestring):
            if isPyData:
              inputs.append('<input type="hidden" name="%s" value="%s">' % ( aresObj[0], aresObj[1].replace('"', "'").replace("'", "\\'").replace('\n', "|")))
            else:
              inputs.append('<input type="hidden" name="%s" value="\'+ %s +\' ">' % (aresObj[0], aresObj[1]))
          else:
            inputs.append('<input type="hidden" name="%s" value="\'+ %s +\'">' % (aresObj[0], aresObj[1].val))
        else:
          inputs.append('<input type="hidden" name="%s" value="\'+ %s +\'">' % (aresObj.htmlCode if aresObj.htmlCode is not None else aresObj._code, aresObj.val))
    return ''' $('<form method="%s" action=%s>%s</form>').appendTo('body').submit(); ''' % (method, url, "".join(inputs) )

  def jsAddImports(self, moduleAlias):
    """
    :category: Dynamic Imports
    :rubric: JS
    :type: Packages
    :dsc:

    :return: The Javascript String
    """
    jsData = []
    for alias in moduleAlias:
      for js in AresImports.JS_IMPORTS[alias]['modules']:
        jsData.append("import('%s')" % js)
    return ";".join(jsData)


  # --------------------------------------------------------------------------------------------------------------
  #                                   STANDARD HTML COMPONENTS SECTION
  #
  # --------------------------------------------------------------------------------------------------------------
  def add(self, htmlObj, fncName=None):
    """ Register the HTML component to the Ares object """
    self.htmlItems[id(htmlObj)] = htmlObj
    self.content.append(id(htmlObj))
    return htmlObj

  def contents(self, vals=None, width=None, widthUnit="%", height=None, heightUnit="px"): return self.add(html.AresHtmlTextComp.ContentsTable(self, vals, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def text(self, text=None, size=None, color=None, align='left', width=100, widthUnit="%", height=None, heightUnit="px", htmlCode=None, tooltip=''): return self.add(html.AresHtmlText.Text(self, text, size, color, align, width, widthUnit, height, heightUnit, htmlCode, tooltip), sys._getframe().f_code.co_name)
  def highlights(self, text=None, title=None, icon=None, type=None, size=None, color=None, width=100, widthUnit="%", height=None, heightUnit="px", htmlCode=None): return self.add(html.AresHtmlText.Highlights(self, text, title, icon, type, size, color, width, widthUnit, height, heightUnit, htmlCode), sys._getframe().f_code.co_name)
  def update(self, text=None, size=None, color=None, width=100, widthUnit="%", height=None, heightUnit="px", htmlCode=None): return self.add(html.AresHtmlText.LastUpdated(self, text, size, color, width, widthUnit, height, heightUnit, htmlCode), sys._getframe().f_code.co_name)
  def prism(self, text=None, language='python', size=None, width=100, widthUnit="%", height=None, heightUnit="px", isEditable=False, trimSpaces=True, align=None): return self.add(html.AresHtmlTextComp.Prism(self, text, language, size, width, widthUnit, height, heightUnit, isEditable, trimSpaces, align), sys._getframe().f_code.co_name)
  def editor(self, text="", size=None, language='python', width=100, widthUnit="%", height=None, heightUnit="px", isEditable=False, htmlCode=None): return self.add(html.AresHtmlTextEditor.Editor(self, text, size, language, width, widthUnit, height, heightUnit, isEditable, htmlCode), sys._getframe().f_code.co_name)
  def tags(self, vals=None, title="", icon="", width=100, widthUnit="%", height=None, heightUnit="px", htmlCode=None):
    return self.add(html.AresHtmlTextEditor.Tags(self, vals, title, icon, width, widthUnit, height, heightUnit, htmlCode), sys._getframe().f_code.co_name)
  def console(self, text=None, size=None, width=100, widthUnit="%", height=None, heightUnit="px", isEditable=False, htmlCode=None): return self.add(html.AresHtmlTextEditor.Console(self, text, size, width, widthUnit, height, heightUnit, isEditable, htmlCode), sys._getframe().f_code.co_name)
  def formula(self, text=None, size=None, width=100, widthUnit="%", color=None): return self.add(html.AresHtmlTextComp.Formula(self, text, size, width, widthUnit, color), sys._getframe().f_code.co_name)
  def code(self, text=None, size=None, color=None, width=90, widthUnit='%', height=None, heightUnit='px', edit=True, htmlCode=None): return self.add(html.AresHtmlText.Code(self, text, size, color, width, widthUnit, height, heightUnit, edit, htmlCode), sys._getframe().f_code.co_name)
  def paragraph(self, text=None, size=None, color=None, backgroundColor=None, border=False, width=100, widthUnit="%", height=None, heightUnit='px', htmlCode=None, encoding="UTF-8"): return self.add(html.AresHtmlText.Paragraph(self, text, size, color, backgroundColor, border, width, widthUnit, height, heightUnit, htmlCode, encoding), sys._getframe().f_code.co_name)
  def preformat(self, text=None, size=None, color=None, width=90, widthUnit='%', height=None, heightUnit='px', htmlCode=None): return self.add(html.AresHtmlText.Preformat(self, text, size, color, width, widthUnit, height, heightUnit, htmlCode), sys._getframe().f_code.co_name)
  def blockquote(self, text=None, author=None, size=None, color=None, width=None, widthUnit='%', height=None, heightUnit='px', align=None, htmlCode=None): return self.add(html.AresHtmlText.BlockQuote(self, text, author, size, color, width, widthUnit, height, heightUnit, align, htmlCode), sys._getframe().f_code.co_name)
  def textbubble(self, recordSet=None, width=250, widthUnit="px", color=None, size=25, backgroundColor=None): return self.add( html.AresHtmlTextComp.TextBubble(self, recordSet, width, widthUnit, color, size, backgroundColor), sys._getframe().f_code.co_name)
  def docScript(self, title, scriptName, className='NOT_SET', fncName='', docType='code', color=None, size=None): return self.add(html.AresHtmlTextComp.DocScript(self, title, scriptName, className, fncName, docType, color, size), sys._getframe().f_code.co_name)
  def sidebar(self, links=None, color=None, size=None, dataSrc=None, servers=None): return self.add(html.AresHtmlSideBar.HtmlSideBarBasic(self, links, color, size, dataSrc, servers), sys._getframe().f_code.co_name)
  def nav(self, value=None, color=None, selected=None, size=None, breadcrum=None, logo='ares_logo_nav_bar.png', logoLink=None, backgroundColor=None): return self.add(html.AresHtmlNavBar.HtmlNavBar(self, value, color, selected, size, breadcrum, logo, logoLink, backgroundColor), sys._getframe().f_code.co_name)
  def accordeon(self, categories=None, color=None, width=150, widthUnit='px', size=None): return self.add(html.AresHtmlList.HtmlListAccordeon(self, categories, color, width, widthUnit, size), sys._getframe().f_code.co_name)
  def info(self, text=None): return self.add(html.AresHtmlOthers.Help(self, text), sys._getframe().f_code.co_name)
  def delta(self, recordSet=None, width=200, widthUnit='px', height=80, heightUnit='px', size=None): return self.add( html.AresHtmlTextComp.Delta(self, recordSet, width, widthUnit, height, heightUnit, size), sys._getframe().f_code.co_name)
  def textvignet(self, recordSet=None, width=None, widthUnit='%', height=None, heightUnit='px', size=None): return self.add(html.AresHtmlTextComp.TextVignet(self, recordSet, width, widthUnit, height, heightUnit, size), sys._getframe().f_code.co_name)
  def vignet(self, recordSet=None, width=100, widthUnit='%', height=None, heightUnit='px', size=None, colorTitle=None): return self.add(html.AresHtmlTextComp.Vignet(self, recordSet, width, widthUnit, height, heightUnit, size, colorTitle), sys._getframe().f_code.co_name)
  def tableEvents(self, vals=None, title=None, width=None, height=None, color=None): return self.add(html.AresHtmlEvent.EventTable(self, vals, title, width, height, color), sys._getframe().f_code.co_name)
  def calendarday(self, title='', width=100, height=100, color='#398438'): return self.add(html.AresHtmlEvent.CalendarDay(self, title, width, height, color), sys._getframe().f_code.co_name)
  def progressbar(self, number=None, width=100, widthUnit='%', height=20, heightUnit='px'): return self.add(html.AresHtmlEvent.ProgressBar(self, number, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def tick(self, value=None, label=None, size=None, color=None, tooltip=''): return self.add(html.AresHtmlTextComp.Tick(self, value, label, size, color, tooltip), sys._getframe().f_code.co_name)
  def updown(self, recordSet=None, size=None, color=None): return self.add(html.AresHtmlTextComp.UpDown(self, recordSet, size, color), sys._getframe().f_code.co_name)
  def number(self, number=None, label=None, size=None, color=None, tooltip='', htmlCode=None): return self.add(html.AresHtmlText.Numeric(self, number, label, size, color, tooltip, htmlCode), sys._getframe().f_code.co_name)
  def newline(self, count=1): return self.add(html.AresHtmlOthers.Newline(self, count), sys._getframe().f_code.co_name)
  def delimiter(self, size=1, color=None): return self.add(html.AresHtmlOthers.Delimiter(self, size, color), sys._getframe().f_code.co_name)
  def stars(self, count=None, color=None): return self.add(html.AresHtmlOthers.Stars(self, count, color), sys._getframe().f_code.co_name)
  def hr(self, count=1, size=None, color=None, backgroundColor=None, height=None, heightUnit='px', align=None): return self.add(html.AresHtmlOthers.Hr(self, color, count, size, backgroundColor, height, heightUnit, align), sys._getframe().f_code.co_name)
  def icon(self, recordSet=None, marginTop=20): return self.add(html.AresHtmlImage.Icon(self, recordSet, marginTop), sys._getframe().f_code.co_name)
  def emoji(self, text=None, marginTop=20): return self.add(html.AresHtmlImage.Emoji(self, text, marginTop), sys._getframe().f_code.co_name)
  def badge(self, text=None, backgroundColor=None, color=None): return self.add(html.AresHtmlImage.Badge(self, text, backgroundColor, color), sys._getframe().f_code.co_name)
  def textborder(self, recordSet=None, width=None, withUnit='%', height=None, heightUnit="px", size=None, align='center'): return self.add(html.AresHtmlTextComp.TextWithBorder(self, recordSet, width, withUnit, height, heightUnit, size, align), sys._getframe().f_code.co_name)
  def title(self, text=None, size=None, level=None, name=None, aresContent=None, color=None, picture=None, icon=None, marginTop=5, htmlCode=None, width=100, widthUnit="%", height=None, heightUnit="px", align=None): return self.add(html.AresHtmlText.Title(self, text, size, level, name, aresContent, color, picture, icon, marginTop, htmlCode, width, widthUnit, height, heightUnit, align), sys._getframe().f_code.co_name)
  def radio(self, recordSet=None, checked=None, htmlCode=None, width=100, widthUnit='%', height=None, heightUnit="px", radioVisible=False, event=None, withRemoveButton=False, dfColumn=None, align='left', globalFilter=None, tooltip='', allSelected=False, title=''): return self.add(html.AresHtmlRadio.Radio(self, recordSet, checked, htmlCode, width, widthUnit, height, heightUnit, radioVisible, event, withRemoveButton, dfColumn, align, globalFilter, tooltip, title), sys._getframe().f_code.co_name)
  def switch(self, recordSet=None, label=None, color=None, size=16, width=150, widthUnit='px', height=20, heightUnit='px', htmlCode=None): return self.add(html.AresHtmlRadio.Switch(self, recordSet, label, color, size, width, widthUnit, height, heightUnit, htmlCode), sys._getframe().f_code.co_name)
  def checkbox(self, recordSet=None, title='', color=None, width=100, widthUnit="%", height=None, heightUnit="px", align='left', htmlCode=None, globalFilter=None, tooltip='', dfColumn=None): return self.add(html.AresHtmlCheckBox.HtmlCheckbox(self, recordSet, title, color, width, widthUnit, height, heightUnit, align, htmlCode, globalFilter, tooltip, dfColumn), sys._getframe().f_code.co_name)
  def checkbutton(self, text=None, title='', width=20, widthUnit="px", height=20, heightUnit="px", label=None, htmlCode=None, isChecked=False, isDisable=False): return self.add(html.AresHtmlCheckBox.HtmlCheckButton(self, text, title, width, widthUnit, height, heightUnit, label, htmlCode, isChecked, isDisable), sys._getframe().f_code.co_name)
  def skillbars(self, recordSet=None, title='', color=None, width=100, widthUnit='%', height=None, heightUnit='px', htmlCode=None, globalFilter=None): return self.add(html.AresHtmlEvent.SkillBar(self, recordSet, title, width, widthUnit, height, heightUnit, color, htmlCode, globalFilter), sys._getframe().f_code.co_name)
  def blocktext(self, recordSet=None, color=None, size=None, border='auto', width=200, widthUnit='px', height=None, heightUnit='px'): return self.add(html.AresHtmlTextComp.BlockText(self, recordSet, color, size, border, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def slider(self, value=0, title='', type="integer", range=None, animate=True, step=1, min=0, max=100, width=100, widthUnit='%', height=None, heightUnit='px', htmlCode=None): return self.add(html.AresHtmlEvent.Slider(self, value, title, type, range, animate, step, min, max, width, widthUnit, height, heightUnit, htmlCode), sys._getframe().f_code.co_name)
  def date(self, label=None, color=None, size=None, yyyy_mm_dd='', htmlCode=None, frequency=None, placeholder=None, changeMonth=True, changeYear=True, showOtherMonths=True, selectOtherMonths=True, selectedDts=None, selectedCss='CssLabelDates', excludeDts=False, useDefault=False, withRemoveButton=False, width=200, widthUnit='px', height=None, heightUnit='px'): return self.add(html.AresHtmlInput.DatePicker(self, label, color, size, yyyy_mm_dd, htmlCode, frequency, placeholder, changeMonth, changeYear, showOtherMonths, selectOtherMonths, selectedDts, selectedCss, excludeDts, useDefault, withRemoveButton, width, widthUnit, height, heightUnit ), sys._getframe().f_code.co_name)
  def timepicker(self, value, label='', color=None, size=None, htmlCode=None): return self.add(html.AresHtmlInput.TimePicker(self, value, label, color, size, htmlCode), sys._getframe().f_code.co_name)
  def countdown(self, date, color=None, timeInMilliSeconds=1000, width="100", widthUnit='%', height=None, heightUnit='px', htmlCode=None): return self.add(html.AresHtmlOthers.CountDownDate(self, date, timeInMilliSeconds, color, width, widthUnit, height, heightUnit, htmlCode), sys._getframe().f_code.co_name)
  def textArea(self, text='', title=None, label=None, width=100, widthUnit='%', rows=5, readOnly=False, backgroundColor='white', spellcheck=False, htmlCode=None, docBlock=None, placeholder='Write your text below'): return self.add(html.AresHtmlEvent.TextArea(self, text, title, label, width, widthUnit, rows, readOnly, backgroundColor, spellcheck, htmlCode, docBlock, placeholder), sys._getframe().f_code.co_name)
  def img(self, text=None, position="center", width=100, widthUnit="%", height=None, heightUnit="px", folder=None, htmlCode=None): return self.add(html.AresHtmlImage.Image(self, text, position, htmlCode, folder, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def figure(self, matPlotLibFig=None, htmlCodes=None, position="center", width=100, widthUnit="%", height=200, heightUnit="px", fixedName=''): return self.add(html.AresHtmlImage.Figure(self, matPlotLibFig, htmlCodes, position, width, widthUnit, height, heightUnit, fixedName), sys._getframe().f_code.co_name)
  def media(self, text=None, width=100, widthUnit='%', height=None, heightUnit='px'): return self.add(html.AresHtmlOthers.Media(self, text, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def animatedimg(self, recordSet=None, width=200, widthUnit="px", height=200, heightUnit="px"): return self.add(html.AresHtmlImage.AnimatedImage(self, recordSet, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def gridImg(self, aresData=None, title='', width=120, widthUnit='px', height=None, heightUnit='px'): return self.add(html.AresHtmlImage.ImgGrid(self, aresData, title, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def carrousel(self, images, width=100, widthUnit="%", height=None, heightUnit="px"): return self.add(html.AresHtmlImage.ImgCarrousel(self, images, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def input(self, text='', placeholder='', label=None, icon=None, width=100, widthUnit="%", height=27, heightUnit="px", color=None, size=None, align='left', htmlCode=None, withRemoveButton=False, autocompleteSrc=None, tooltip='', docBlock=None, lettersOnly=False, globalFilter=None): return self.add(html.AresHtmlInput.InputText(self, text, placeholder, label, icon, width, widthUnit, height, heightUnit, color, size, align, htmlCode, withRemoveButton, autocompleteSrc, tooltip, docBlock, lettersOnly, globalFilter), sys._getframe().f_code.co_name)
  def inputInt(self, text="", placeholder='', label='', icon=None, width=100, widthUnit="%", height=27, heightUnit="px", color=None, size=None, align='left', htmlCode=None, withRemoveButton=False, autocompleteSrc=None, tooltip='', docBlock=None, globalFilter=None): return self.add(html.AresHtmlInput.InputInt(self, text, placeholder, label, icon, width, widthUnit, height, heightUnit, color, size, align, htmlCode, withRemoveButton, autocompleteSrc, tooltip, docBlock, lettersOnly=False, globalFilter=globalFilter), sys._getframe().f_code.co_name)
  def pwd(self, text='', placeholder='', label='', icon=None, width=100, widthUnit="%", height=27, heightUnit="px", color=None, size=None, align='left', htmlCode=None, withRemoveButton=False, autocompleteSrc=None, tooltip='', docBlock=None, globalFilter=None): return self.add(html.AresHtmlInput.InputPass(self, text, placeholder, label, icon, width, widthUnit, height, heightUnit, color, size, align, htmlCode, withRemoveButton, autocompleteSrc, tooltip, docBlock, lettersOnly=False, globalFilter=globalFilter), sys._getframe().f_code.co_name)
  def inputRange(self, recordSet=None, color=None, size=None, align='left', width=100, widthUnit="%", height=27, heightUnit="px", htmlCode=None): return self.add(html.AresHtmlInput.InputRange(self, recordSet, color, size, align, width, widthUnit, height, heightUnit, htmlCode), sys._getframe().f_code.co_name)
  def brackets(self, recordSet=None, width=100, widthUnit='%', height=550, heightUnit='px', options=None): return self.add(html.AresHtmlList.ListTournaments(self, recordSet, width, widthUnit, height, heightUnit, options), sys._getframe().f_code.co_name)
  def contextmenu(self, recordSet=None, width=None, widthUnit='%', height=None, heightUnit='px', visible=False): return self.add(html.AresHtmlEvent.ContextMenu(self, recordSet, width, widthUnit, height, heightUnit, visible), sys._getframe().f_code.co_name)


  # BUTTONS ---------------------------------------------------------
  def button(self, text=None, width=None, widthUnit="%", height=26, heightUnit="px", disable=False, color=None, icon=None, align='left', internalLink=None, htmlCode=None, groupId=None, docBlock=None, tooltip=None): return self.add(html.AresHtmlButton.Button(self, text, width, widthUnit, height, heightUnit, disable, color, icon, align, internalLink, htmlCode=htmlCode, groupId=groupId, docBlock=docBlock, tooltip=tooltip), sys._getframe().f_code.co_name)
  def validate(self, text, width=None, widthUnit="%", height=26, heightUnit="px", disable=False, color=None, align='left', internalLink=None, htmlCode=None, groupId=None, docBlock=None, tooltip=None): return self.add(html.AresHtmlButton.Button(self, text, width, widthUnit, height, heightUnit, disable, color, icon='fas fa-check-circle', align=align, internalLink=internalLink, htmlCode=htmlCode, groupId=groupId, docBlock=docBlock, tooltip=tooltip), sys._getframe().f_code.co_name)
  def remove(self, text, width=None, widthUnit="%", height=26, heightUnit="px", disable=False, color=None, align='left', internalLink=None, htmlCode=None, groupId=None, docBlock=None, tooltip=None): return self.add(html.AresHtmlButton.Button(self, text, width, widthUnit, height, heightUnit, disable, color, icon='fas fa-trash-alt', align=align, internalLink=internalLink, htmlCode=htmlCode, groupId=groupId, docBlock=docBlock, tooltip=tooltip), sys._getframe().f_code.co_name)
  def phone(self, text, width=None, widthUnit="%", height=26, heightUnit="px", disable=False, color=None, align='left', internalLink=None, htmlCode=None, groupId=None, docBlock=None, tooltip=None): return self.add(html.AresHtmlButton.Button(self, text, width, widthUnit, height, heightUnit, disable, color, icon='fas fa-phone', align=align, internalLink=internalLink, htmlCode=htmlCode, groupId=groupId, docBlock=docBlock, tooltip=tooltip), sys._getframe().f_code.co_name)
  def mail(self, text, width=None, widthUnit="%", height=26, heightUnit="px", disable=False, color=None, align='left', internalLink=None, htmlCode=None, groupId=None, docBlock=None, tooltip=None): return self.add(html.AresHtmlButton.Button(self, text, width, widthUnit, height, heightUnit, disable, color, icon='fas fa-envelope', align=align, internalLink=internalLink, htmlCode=htmlCode, groupId=groupId, docBlock=docBlock, tooltip=tooltip), sys._getframe().f_code.co_name)
  def buttonicon(self, icon=None, text='', color=None, align='center', internalLink=None, backgroundColor=None, htmlCode=None, groupId=None, docBlock=None): return self.add(html.AresHtmlButton.ButtonIcon(self, icon, text, color=color, align=align, internalLink=internalLink, backgroundColor=backgroundColor, htmlCode=htmlCode, groupId=groupId, docBlock=docBlock), sys._getframe().f_code.co_name)

  # BUTTONS ICONS ---------------------------------------------------------
  def clock(self, position=None): return self.add(html.AresHtmlButton.IconClock(self, position, None, None), sys._getframe().f_code.co_name)
  def refresh(self, position=None): return self.add(html.AresHtmlButton.IconRefresh(self, position, None, None), sys._getframe().f_code.co_name)
  def iconTable(self, position=None): return self.add(html.AresHtmlButton.IconTable(self, position, None, None), sys._getframe().f_code.co_name)
  def thumbtack(self, htmlObj, position=None): return self.add(html.AresHtmlButton.IconThumbtack(self, htmlObj, position, None, None), sys._getframe().f_code.co_name)
  def upButton(self, position=None): return self.add(html.AresHtmlButton.IconDownload(self, position, None, None), sys._getframe().f_code.co_name)
  def iconExcel(self, position=None): return self.add(html.AresHtmlButton.IconExcel(self, position, None, None), sys._getframe().f_code.co_name)
  def pdf(self, position=None): return self.add(html.AresHtmlButton.IconPdf(self, position, None, None), sys._getframe().f_code.co_name)
  def plus(self, position=None): return self.add(html.AresHtmlButton.IconPlus(self, position, None, None), sys._getframe().f_code.co_name)
  def edit(self, position=None): return self.add(html.AresHtmlButton.IconEdit(self, position, None, None), sys._getframe().f_code.co_name)
  def delete(self, position=None): return self.add(html.AresHtmlButton.IconDelete(self, position, None, None), sys._getframe().f_code.co_name)
  def lock(self, position=None): return self.add(html.AresHtmlButton.IconLock(self, position, None, None), sys._getframe().f_code.co_name)
  def zoom(self, position=None): return self.add(html.AresHtmlButton.IconZoom(self, position, None, None), sys._getframe().f_code.co_name)
  def capture(self, position=None): return self.add(html.AresHtmlButton.IconCapture(self, position, None, None), sys._getframe().f_code.co_name)
  def wrench(self, position=None): return self.add(html.AresHtmlButton.IconWrench(self, position, None, None), sys._getframe().f_code.co_name)
  def remove(self, position=None): return self.add(html.AresHtmlButton.IconRemove(self, position, None, None), sys._getframe().f_code.co_name)
  def calculator(self, position=None): return self.add(html.AresHtmlButton.IconSum(self, position, None, None), sys._getframe().f_code.co_name)
  def awesome(self, icon, position=None, tooltip=None): return self.add(html.AresHtmlButton.IconEdit(self, position, icon, tooltip), sys._getframe().f_code.co_name)

  # LINKS ---------------------------------------------------------
  def externallink(self, recordSet=None, height=None, heightUnit='px', decoration=False, newPage=True, badgeContent=None): return self.add(html.AresHtmlHRef.ExternalLink(self, recordSet, height, heightUnit, decoration, newPage, badgeContent), sys._getframe().f_code.co_name)
  def link(self, recordSet=None, width=100, widthUnit='%', height=None, heightUnit='px', align='left', decoration=False, badgeContent=None): return self.add(html.AresHtmlHRef.Link(self, recordSet, width, widthUnit, height, heightUnit, align, decoration, badgeContent), sys._getframe().f_code.co_name)

  # PANELS ---------------------------------------------------------
  def panel(self, htmlObjs=None, width=100, widthUnit='%', height=None, heightUnit='px'): return self.add(html.AresHtmlContainer.Panel(self, htmlObjs, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def paneldisplay(self, htmlObjs=None, title='', width=100, widthUnit='%', height=None, heightUnit='px', showPanel=True): return self.add(html.AresHtmlContainer.PanelDisplay(self, htmlObjs, title, width, widthUnit, height, heightUnit, showPanel), sys._getframe().f_code.co_name)
  def panelsplit(self, width=100, widthUnit='%', height=500, heightUnit='px', left=None, right=None): return self.add(html.AresHtmlContainer.PanelSplit(self, width, widthUnit, height, heightUnit, left, right), sys._getframe().f_code.co_name)
  def col(self, htmlObjs=None, position='middle', width=100, widthUnit='%', height=None, heightUnit='px', align=None): return self.add(html.AresHtmlContainer.Col(self, htmlObjs, position, width, widthUnit, height, heightUnit, align), sys._getframe().f_code.co_name)
  def row(self, htmlObjs=None, width=100, widthUnit='%', height=None, heightUnit='px', aresData=None, align='left', valign='top', colsWith=None, closable=False, resizable=False, titles=None): return self.add(html.AresHtmlContainer.Row(self, htmlObjs, width, widthUnit, height, heightUnit, aresData, align, valign, colsWith, closable, resizable, titles), sys._getframe().f_code.co_name)
  def grid(self, htmlObjs=None, width=100, widthUnit='%', height=None, heightUnit='px', colsDim=None, colsAlign=None, noGlutters=False, align=None): return self.add(html.AresHtmlContainer.Grid(self, htmlObjs, width, widthUnit, height, heightUnit, colsDim, colsAlign, noGlutters, align), sys._getframe().f_code.co_name)
  def tabs(self, htmlObjs=None, width=100, widthUnit='%', height=None, heightUnit='px', tabNames=None, rowsCss=None, colsCss=None, closable=False, selectedTab=None, htmlCode=None, alwaysReload=False, encoding="UTF-8"): return self.add(html.AresHtmlContainer.Tabs(self, htmlObjs, width, widthUnit, height, heightUnit, tabNames, rowsCss, colsCss, closable, selectedTab, htmlCode, alwaysReload, encoding), sys._getframe().f_code.co_name)
  def pills(self, htmlObjs=None, width=100, widthUnit='%', height=None, heightUnit='px', colsDim=None, rowsCss=None, colsCss=None, closable=False): return self.add(html.AresHtmlContainer.Pills(self, htmlObjs, width, widthUnit, height, heightUnit, colsDim, rowsCss, colsCss, closable), sys._getframe().f_code.co_name)
  def div(self, htmlObjs=None, color=None, size=None, width=100, widthUnit="%", icon=None, height=None, heightUnit="px", editable=False, align='left', padding=None, htmlCode=None): return self.add(html.AresHtmlContainer.Div(self, htmlObjs, color, size, width, widthUnit, icon, height, heightUnit, editable, align, padding, htmlCode), sys._getframe().f_code.co_name)
  def fixeddiv(self, text=None, top=100, left=None, right=None, color=None, size=None, width=None, widthUnit="px", icon=None, height=None, heightUnit="px", editable=False, align='left', backgroundColor='white', zindex=None, padding=None, htmlCode=None): return self.add(html.AresHtmlContainer.DivFixed(self, text, top, left, right, color, size, width, widthUnit, icon, height, heightUnit, editable, align, backgroundColor, zindex, padding, htmlCode), sys._getframe().f_code.co_name)
  def dragdiv(self, text=None, top=100, left=None, right=None, color=None, size=None, width=None, widthUnit="px", icon=None, height=None, heightUnit="px", editable=False, align='left', backgroundColor='white', padding=None, htmlCode=None): return self.add(html.AresHtmlContainer.DragDiv(self, text, top, left, right, color, size, width, widthUnit, icon, height, heightUnit, editable, align, backgroundColor, padding, htmlCode), sys._getframe().f_code.co_name)
  def loading(self, value=None): return self.add(html.AresHtmlSystem.Loading(self, value), sys._getframe().f_code.co_name)
  def popup(self, htmlObj=None, title='Popup Title', color=None, size=None, width=100, widthUnit='%', height=None, heightUnit='px', withBackground=True, draggable=False): return self.add(html.AresHtmlContainer.Popup(self, htmlObj, title, color, size, width, widthUnit, height, heightUnit, withBackground, draggable), sys._getframe().f_code.co_name)
  def listbadge(self, recordSet=None, color=None, size=None, width=100, widthUnit="%", height=None, heightUnit='px', draggable=False, draggableGroupId=None, draggableMax=None, dfColumn=None): return self.add(html.AresHtmlList.ListBadge(self, recordSet, color, size, width, widthUnit, height, heightUnit, draggable, draggableGroupId, draggableMax, dfColumn), sys._getframe().f_code.co_name)
  def iframe(self, url, width=100, widthUnit="%", height=100, heightUnit="%"): return self.add(html.AresHtmlContainer.IFrame(self, url, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def dialogs(self, recordSet=None, width=100, widthUnit="%", height=500, heightUnit="px"): return self.add(html.AresHtmlContainer.Dialog(self, recordSet, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def menu(self, width=100, widthUnit="%", height=None, heightUnit="px", htmlCode=None): return self.add(html.AresHtmlContainer.IconsMenu(self, width, widthUnit, height, heightUnit, htmlCode), sys._getframe().f_code.co_name)

  # SELECT AND LIST -------------------------------------
  def select(self, recordSet=None, title='', htmlCode=None, dataSrc=None, event=None, selected=None, docBlock=None, allSelected=False, label="", width=None, widthUnit="%", height=None, heightUnit="%", dfColumn=None, globalFilter=None): return self.add(html.AresHtmlSelect.Select(self, recordSet, title, htmlCode, dataSrc, event, selected, docBlock, allSelected, label, width, widthUnit, height, heightUnit, dfColumn, globalFilter), sys._getframe().f_code.co_name)
  def selectmulti(self, recordSet=None, title='', maxSelections=2, htmlCode=None, dataSrc=None, event=None, selectedItems=None, docBlock=None, label="", width=None, widthUnit="%", height=None, heightUnit="%", dfColumn=None, globalFilter=None): return self.add(html.AresHtmlSelect.SelectMulti(self, recordSet, title, maxSelections, htmlCode, dataSrc, event, selectedItems, docBlock, label, width, widthUnit, height, heightUnit, dfColumn, globalFilter), sys._getframe().f_code.co_name)
  def list(self, categories=None, icon=None, title='', width=100, widthUnit="%", height=None, heightUnit='px', draggable=False, draggableGroupId=None, draggableMax=None, dfColumn=None, dataSrc=None, htmlCode=None, searchable=False, selectable=True, showGrid=True, template=None, globalFilter=None): return self.add(html.AresHtmlList.List(self, categories, icon, title, width, widthUnit, height, heightUnit, draggable, draggableGroupId, draggableMax, dfColumn, dataSrc, htmlCode, searchable, selectable, showGrid, template, globalFilter), sys._getframe().f_code.co_name)
  def tree(self, recordSet=None, width=100, widthUnit="%", height=None, heightUnit='px', title='', dataSrc=None, htmlCode=None, draggable=False): return self.add(html.AresHtmlList.ListTree(self, recordSet, width, widthUnit, height, heightUnit, title, dataSrc, htmlCode, draggable), sys._getframe().f_code.co_name)
  def listnumbers(self, recordSet=None, icon=None, level=None, marginTop=10, width=100, widthUnit='%', height=None, heightUnit='px', selectable=None, multiselectable=None, htmlCode=None): return self.add(html.AresHtmlList.NumberList(self, recordSet, marginTop, level, width, widthUnit, height, heightUnit, selectable=selectable, multiselectable=multiselectable, htmlCode=htmlCode), sys._getframe().f_code.co_name)
  def listletter(self, recordSet=None, icon=None, level=None, marginTop=10, width=100, widthUnit='%', height=None, heightUnit='px', selectable=None, multiselectable=None, htmlCode=None): return self.add(html.AresHtmlList.LetterList(self, recordSet, marginTop, level, width, widthUnit, height, heightUnit, selectable=selectable, multiselectable=multiselectable, htmlCode=htmlCode), sys._getframe().f_code.co_name)
  def checklist(self, recordSet=None, width=100, widthUnit='%', height=None, heightUnit='px'): return self.add(html.AresHtmlList.CheckList(self, recordSet, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)
  def points(self, recordSet=None, marginTop=10, level=None, width=100, widthUnit='%', height=None, heightUnit='px', selectable=None, multiselectable=None, htmlCode=None): return self.add(html.AresHtmlList.Bullets(self, recordSet, marginTop, level, width, widthUnit, height, heightUnit, selectable=selectable, multiselectable=multiselectable, htmlCode=htmlCode), sys._getframe().f_code.co_name)
  def squares(self, recordSet=None, marginTop=10, level=None, width=100, widthUnit='%', height=None, heightUnit='px', selectable=None, multiselectable=None, htmlCode=None): return self.add(html.AresHtmlList.Squares(self, recordSet, marginTop, level, width, widthUnit, height, heightUnit, selectable=selectable, multiselectable=multiselectable, htmlCode=htmlCode), sys._getframe().f_code.co_name)
  def dropdown(self, recordSet=None, title='', width=100, widthUnit='px', height=None, heightUnit='px', htmlCode=None, dataSrc=None, globalFilter=None): return self.add(html.AresHtmlSelect.SelectDropDown(self, title, recordSet, width, widthUnit, height, heightUnit, htmlCode, dataSrc, globalFilter), sys._getframe().f_code.co_name)
  def comments(self, recordset, width=100, widthUnit='%', height=100, heightUnit='%', size=None, color=None): return self.add(html.AresHtmlSystem.Comments(self, recordset, width, widthUnit, height, heightUnit, size, color), sys._getframe().f_code.co_name)
  def message(self, title, width=100, widthUnit='%', height=300, heightUnit='px', size=None, color=None, htmlCode=None, send_to=None): return self.add(html.AresHtmlSystem.Message(self, title, width, widthUnit, height, heightUnit, size, color, htmlCode, send_to), sys._getframe().f_code.co_name)

  def search(self, text='', placeholder='Search..', color=None, size=None, align='left', height=None, heightUnit="px", htmlCode=None, tooltip='', extensible=False): return self.add(html.AresHtmlInput.Search(self, text, placeholder, color, size, align, height, heightUnit, htmlCode, tooltip, extensible), sys._getframe().f_code.co_name)
  def searchr(self, recordSet, pageNumber=10, width=100, widthUnit="%", height=None, heightUnit="px"): return self.add(html.AresHtmlText.SearchResult(self, recordSet, pageNumber, width, widthUnit, height, heightUnit), sys._getframe().f_code.co_name)

  def paramsbar(self, htmlRecordSet=None, height=45, logFiles=None):
    return self.add(html.AresHtmlNavBar.HtmlParamsBar(self, htmlRecordSet, height, logFiles), sys._getframe().f_code.co_name)

  def light(self, color=None, height=25, heightUnit='px', label=None, tooltip=''):
    """
    :category: HTML
    :rubric:
    :type:
    :dsc:

    :example:
    :return:
    """
    return self.add(html.AresHtmlTextComp.TrafficLight(self, color, label, height, heightUnit, tooltip), sys._getframe().f_code.co_name)

  # TODO Not migrated yet
  #def wiki(self, dataSourceName, value): return self.add(html.AresHtmlSystem.Wiki(self, dataSourceName, value), sys._getframe().f_code.co_name)
  #def editable(self, width=98, widthUnit='%', size=None, color=None): return self.add(html.AresHtmlSystem.TextInput(self, 'Put your text here', width, widthUnit, size, color), sys._getframe().f_code.co_name)

  def dropfile(self, placeholder='Drop your files here', tooltip='', report_name=None, fileType="OUTPUTS"):
    """
    :category: File
    :type: constructor
    :rubric: JS
    :dsc:
      Add an HTML component to drop files. The files will be dropped by default to the OUTPUT folder of the defined environment.
      Files will also be recorded in the database in order to ensure that those data will not be shared.
      The data sharing is and should be defined only by the user from the UI.
    :return: The AReS HTML component
    """
    return self.add(html.AresHtmlFiles.DropFile(self, placeholder, tooltip, report_name, fileType), sys._getframe().f_code.co_name)

  # --------------------------------------------------------------------------------------------------------------
  #
  #                                   DATATABLE COMPONENTS SECTION
  # --------------------------------------------------------------------------------------------------------------
  def pivot(self, recordSet=None, rows=None, cols=None, vals=None, title='', aggOptions=None, rendererName="Table", width=100, widthUnit='%', height=None, heightUnit='px', htmlCode=None, debug=False):
    """
    :category: Pivot Tables
    :rubric: JS
    :type: constructor
    :dsc:
      Create a AReS HTML Pivot table
    :link Datatable Documentation: https://pivottable.js.org/examples/
    :return: The AReS HTML Table
    :wrap class: ares.Lib.html.AresHtmlDataPivot.PivotTable
    """
    if aggOptions is None:
      aggOptions = {'name': "Sum Agg", 'digits': 2}
    return self.add(ares.Lib.html.AresHtmlDataPivot.PivotTable(self, js.AresJs.Js(self, recordSet, debug=debug), rows, cols, vals, title, width, widthUnit, height, heightUnit, aggOptions, rendererName, htmlCode), sys._getframe().f_code.co_name)

  def table(self, recordSet=None, header=None, dataFncs=None, aggFnc='sum', cols=None, rows=None, title='',
            width=100, widthUnit='%', height=None, heightUnit='px', tableOptions=None, toolsbar=None, htmlCode=None,
            debug=False, tableTypes='base'):
    """
    :category: Tables
    :rubric: JS
    :type: constructor
    :dsc:
      Create a AReS HTML Table which is basically a javascript Datatable managed by the Python interface.
      The python layer will try as much as possible to structure the data in order to save time in the javascript layer.
    :link Datatable Documentation:
    :return: The AReS HTML Table
    :wrap class: ares.Lib.tables.AresHtmlDataTable.DataTable
    """
    if recordSet is not None and cols is None and rows is None:
      rows, cols = ['_index'], []
      for i, colType in enumerate(recordSet.dtypes):
        colName = recordSet.dtypes.index[i]
        if colType in ['float64', 'bool', 'int64']:
          cols.append(colName)
        else:
          rows.append(colName)

    if '_index' in rows:
      recordSet['_index'] = recordSet.index

    if tableOptions is None:
      tableOptions = {}
    if toolsbar is None:
      toolsbar = {}

    jsFncs, systemCols = [], {}
    if tableOptions.get('system', {}).get('age'):
      systemCols['age'] = []
      # TODO: Migrate to the new version of D3
      self.jsImports.add('nvd3')
      for colName in cols:
        systemCols['age'].append("%s.age" % colName)

    if tableOptions.get('system', {}).get('quality'):
      systemCols['quality'] = []
      for colName in cols:
        systemCols['quality'].append("%s.quality" % colName)

    if tableOptions.get('system', {}).get('intensity'):
      systemCols['intensity'] = []
      for colName in cols:
        systemCols['intensity'].append("%s.intensity" % colName)

    if tableTypes == 'hierarchy':
      rows = ['_id', '_level'] + rows

    if isinstance(aggFnc, str):
      if cols is None:
        cols = []
      jsFncs.append((aggFnc, rows, cols + systemCols.get('age', []) + systemCols.get('intensity', []) + systemCols.get('quality', [])))
    else:
      jsFncs.append(aggFnc)
    if isinstance(recordSet, list):
      recordSet = self.df(recordSet)
    if dataFncs is not None:
      jsFncs += dataFncs
    if header is None:
      header = {'_order': rows + cols}

    elif isinstance(header, list):
      tmpHeader = {'_order': []}
      for h in header:
        if isinstance(h, dict):
          tmpHeader[h['data']] = h.get('title', h['data'])
          tmpHeader['_order'].append(h['data'])
        else:
          tmpHeader[h] = h
          tmpHeader['_order'].append(h)
      header = tmpHeader

    if debug:
      self.jsOnLoadFnc.add(self.jsConsole("", isPyData=True))
      self.jsOnLoadFnc.add(self.jsConsole("************************", isPyData=True))
      self.jsOnLoadFnc.add(self.jsConsole("Debug mode for table", isPyData=True))
    return self.add(ares.Lib.html.AresHtmlDataTable.DataTable(self, tableTypes, js.AresJs.Js(self, recordSet, debug=debug).fncs(jsFncs, systemCols), header,
                                                              title, width, widthUnit, height, heightUnit, tableOptions, toolsbar, htmlCode), sys._getframe().f_code.co_name)

  def excel(self, recordSet=None, cols=None, rows=None, width=100, widthUnit='%', height=None, heightUnit='px', cellwidth=None, title='', delimiter='TAB', htmlCode=None):
    """
    :category: Excel Input table
    :rubric: PY
    :type: Constructor
    :dsc:
      Create an excel input file based on the copy pasted data. Only the ones corresponding to the columns will be kept
    """
    return self.add(ares.Lib.html.AresHtmlDataTable.DataExcel(self, recordSet, cols, rows, title, width, widthUnit, height, heightUnit, cellwidth, delimiter, htmlCode))


  # --------------------------------------------------------------------------------------------------------------
  #
  #                                   CHART COMPONENTS SECTION
  # --------------------------------------------------------------------------------------------------------------
  # Generic entry point for all the charts
  def plot(self, chartType=None, data=None, width=100, widthUnit="%", height=300, heightUnit='px', title='', chartOptions=None,
           toolsbar=None, htmlCode=None, globalFilter=None, chartFamily=None):
    """
    :category: Charts
    :rubric: PY
    :type: constructor
    :dsc:
      Return the preferred Chart library for the requested chartType.
      This can be overridden by defining the variable chartFamily
    :example: aresObj.plot()
    :wrap class: ares.Lib.graph.AresHtmlGraphFabric.Chart
    """
    chartFam = graph.AresHtmlGraphFabric.Chart.get(self, chartType, chartFamily)
    if chartFam is None:
      raise Exception("This type of chart %s does not exist in all the Js Charting families" % chartType)

    return self.add(getattr(graph, 'AresHtmlGraph%s' % chartFam).Chart(self, chartType, data, width, widthUnit, height, heightUnit, title, chartOptions,
                                                                       toolsbar, htmlCode, globalFilter), sys._getframe().f_code.co_name)

  def chart(self, chartType=None, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, title='',
            chartFamily=None, globalFilter=None, debug=False, **kwargs):
    """
    :category:
    :type:
    :rubric:
    :example: aresObj.chart(chartType, sourceFile, seriesNames=seriesNames, xAxis='direction', chartFamily=chartFam, sort_values={'by': ['Date'], 'ascending': False})
    :example: aresObj.chart(chartType, sourceFile, seriesNames=seriesNames, xAxis='direction', chartFamily=chartFam, dataFncs=[('sum', ['direction'], seriesNames), ('top', 2, 'AAPL.Open', 'ascending')])
    :dsc:

    """
    if not hasattr(aresDf, 'htmlCode'):
      if len(aresDf) > 0 and isinstance(aresDf[0], list):
        tmpAresDf = []
        for line in aresDf[1:]:
          tmpAresDf.append(dict(zip(aresDf[0], line)))
        aresDf = tmpAresDf
      aresDf = self.df(aresDf)
    if xAxis == '_index' or xAxis is None:
      xAxis = '_index'
      if seriesNames is None:
        seriesNames = list(aresDf.columns)
      aresDf['_index'] = aresDf.index
    if not 'sort_values' in kwargs:
      if xAxis is not None and not aresDf.empty:
        aresDf.sort_values(by=[xAxis], inplace=True)
    else:
      kwargs['sort_values']["inplace"] = True
      aresDf.sort_values(**kwargs['sort_values'])
      del kwargs['sort_values']

    if dataFncs is None:
      if otherDims is not None:
        dataFncs = [('sum', [xAxis], seriesNames + list(otherDims))]
      else:
        dataFncs = [('sum', [xAxis], seriesNames)]
    chartFam = graph.AresHtmlGraphFabric.Chart.get(self, chartType, chartFamily)
    params = (seriesNames, xAxis) if otherDims is None else tuple([seriesNames, xAxis] + list(otherDims))
    if debug:
      self.jsOnLoadFnc.add(self.jsConsole("", isPyData=True))
      self.jsOnLoadFnc.add(self.jsConsole("************************", isPyData=True))
      self.jsOnLoadFnc.add(self.jsConsole("Debug mode for %s" % chartType, isPyData=True))
    return self.plot(chartType, js.AresJs.Js(self, aresDf, debug=debug).fncs(dataFncs).output(chartFam, chartType, params),
                     title=title, chartFamily=chartFam, globalFilter=globalFilter, **kwargs)

  # Special charts
  #def wordcloud(self, chartType=None, data=None, width=500, widthUnit="%", height=500, heightUnit='px', title='', chartDesc=None, margin=None): return self.add(graph.AresHtmlGraphWordCloud.Chart(self, chartType, data, width, widthUnit, height, heightUnit, title, chartDesc, margin), sys._getframe().f_code.co_name)
  #def venn(self, chartType=None, data=None, width=500, widthUnit="%", height=200, heightUnit='px', title='', chartDesc=None, margin=None): return self.add(graph.AresHtmlGraphVenn.Chart(self, chartType, data, width, widthUnit, height, heightUnit, title, chartDesc, margin), sys._getframe().f_code.co_name)
  #def map(self, chartType=None, data=None, width=500, widthUnit="%", height=200, heightUnit='px', title='', chartDesc=None, margin=None): return self.add(graph.AresHtmlGraphMap.Chart(self, chartType, data, width, widthUnit, height, heightUnit, title, chartDesc, margin), sys._getframe().f_code.co_name)


  # --------------------------------------------------------------------------------------------------------------
  #
  #                                   DATA STRUCTURE SECTION
  # --------------------------------------------------------------------------------------------------------------
  def dataSrc(self, url=None, srcOptions=None, htmlCode=None):
    """
    :category: AReS Data Source
    :rubric: PY
    :type: constructor
    :dsc:
      Create a Data Source in the Javascript page. This data source will be updated by an event and then it will update the corresponding reports
    """
    htmlCode = 'source_%s' % '1' if htmlCode is None else htmlCode
    self.jsGlobal.add("%s = null" % htmlCode)
    if srcOptions is None:
      srcOptions = {}
    srcOptions.update({"type": "url", "url": url})
    return AresFile.AresDataSource(srcOptions, htmlCode=htmlCode, aresObj=self)

  def df(self, recordset, htmlCode=None, index=None, columns=None, dtype=None, copy=True, dataSrc=None):
    """
    :category: AReS Dataframe
    :rubric: PY
    :type: constructor
    :dsc:
      Create a AReS Dataframe which is based on a Pandas Dataframe. This will extend the Pandas Dataframe with some Javascript conversion.
      Indeed this component will be converted to Json and written in the front end.
      The framework will also try to optimise the data and clean up the dataframe in order to reduce the amount of useless data in the front end.
    :return: The AReS dataframe
    :link Pandas Documentation: http://pandas.pydata.org/pandas-docs/stable/
    :wrap class: ares.Lib.js.AresJsData.JsDataFrame
    """
    filePath = None
    if htmlCode is not None:
      splitCode = htmlCode.split("/")
      splitCode[-1] = "%s.csv" % splitCode[-1]  # csv file by default
      filePath = os.path.join(self.run.local_path, 'outputs', *splitCode)
    else:
      htmlCode = 'recordset_%s' % id(recordset)
    return AresFile.AresFile(data=recordset, filePath=filePath, htmlCode=htmlCode, aresObj=self).get(index=index, columns=columns, dtype=dtype, copy=copy)

  def doc(self, docBlockId, docBlockDsc=None, docBlockVal=None):
    docBlockText = []
    if docBlockVal is not None:
      docBlockText.append( docBlockVal )
    if docBlockDsc is not None:
      docBlockText.append("# " % docBlockDsc)
    if not docBlockId in self.docBlocks:
      self.docBlocks[docBlockId] = self.prism( "\n%s\n" % "".join(docBlockText) )
    else:
      self.docBlocks[docBlockId].vals += "%s\n" %  "".join(docBlockText)

  def file(self, filename=None, path=None, htmlCode=None, delimiter=None, fileFamily=None, **kwargs):
    """
    :category: File
    :rubric: PY
    :type: Pandas wrapper
    :dsc:
      Read a file
    :link Pandas Documentation: http://pandas.pydata.org/pandas-docs/stable/
    """
    if path is None:
      path = os.path.join(self.run.local_path, 'outputs')

    # This is the layer which will take care of the HTML Code. Indeed not need to add any extra reference as it will be in the filename
    # It is important to select carrefully the filename as a too generic one might lead to clashes
    # if the filename will be in sub directories, you can use the /
    if filename is None:
      if htmlCode is None:
        raise Exception("You must put either a filename or a htmlCode")

      splitCode = htmlCode.split("/")
      if len(splitCode) > 1:
        path = os.path.join(self.run.local_path, 'outputs', *splitCode[:-1])
      else:
        path = os.path.join(self.run.local_path, 'outputs')
      filename = "%s.csv" % splitCode[-1] # csv file by default
    if filename.endswith(".db") or filename.endswith(".mdb"):
      return self.db(self, dbFamily="sqlite", database=os.path.join(path, filename), username=None, password=None)

    # Add the local file to the notifications in the report
    self.localFiles[htmlCode] = {"subFolder": "", "filename": filename, 'timestamp': self.timestamp}
    delimiter = self.myFiles[filename]['delimiter'] if hasattr(self, 'myFiles') and filename in self.myFiles else delimiter
    return AresFile.AresFile(filePath=os.path.join(path, filename), aresObj=self, htmlCode=htmlCode).get(delimiter=delimiter, fileFamily=fileFamily, **kwargs)

  @html.AresHtml.deprecated
  def save(self, data, filename):
    """

    """
    # Register the file to the database
    self.jsOnLoadFnc.add( self.jsPost("%s/register/OUTPUTS/%s" % (self._urlsApp['ares-transfer'], self.run.report_name), jsData="filename: %s" % json.dumps(filename), isPyData=False ) )
    outputFolder = os.path.join(self.run.local_path, 'outputs')
    fileNameWithPath = os.path.join(outputFolder, filename)
    tmpFile = open(fileNameWithPath, "w")
    tmpFile.write(data)
    tmpFile.close()

  def dc(self, aresDf=None, seriesNames=None, xAxis=None, otherDims=None, dataFncs=None, seriesProperties=None, seriesTypes=None, sort_values=None):
    """
    :category: Charts
    :rubric: PY
    :type: constructor
    :dsc:

    :wrap class: ares.Lib.js.AresJsDataChart.JsChartFrame
    """
    if isinstance(aresDf, list):
      if isinstance(aresDf[0], list):
        tmpAresDf = []
        for line in aresDf[1:]:
          tmpAresDf.append(dict(zip(aresDf[0], line)))
        aresDf = self.df(tmpAresDf)
      else:
        aresDf = self.df(aresDf)
      if sort_values is None:
        if xAxis is not None:
          aresDf.sort_values(by=[xAxis], inplace=True)
      else:
        sort_values["inplace"] = True
        aresDf.sort_values(**sort_values)
    elif aresDf is None:
      aresDf = self.df([])
    if dataFncs is None:
      if otherDims is not None:
        dataFncs = [('sum', [xAxis], seriesNames + list(otherDims))]
      else:
        dataFncs = [('sum', [xAxis], seriesNames)]

    return js.AresJs.Js(self, aresDf).fncs(dataFncs)

  def getWidget(self, widgetName=None, **kwargs):
    """
    :category: Widget Retriever
    :rubric: PY
    :dsc:

    :example: aresObj.getWidget()
    :return: The Python Widget object
    """
    widgetNames = {}
    if not hasattr(self, 'widgets'):
      widgetPath = os.path.dirname(Widget.__file__)
      for file in os.listdir(widgetPath):
        if file.endswith(".py"):
          for name, obj in inspect.getmembers(importlib.import_module("ares.widgets.%s" % file.replace(".py", "")), inspect.isclass):
            if issubclass(obj, Widget.Widget):
              if obj.name is not None:
                if widgetName == obj.name:
                  return obj(self)._component(kwargs)
                elif widgetName is None:
                  widgetNames[obj.name] = obj.__doc__
    if widgetName is None:
      return widgetNames

  def markdown(self, markDown):
    """
    :category: Static generation
    :type: PY
    :rubric: Markdown
    :dsc:
      Construct the Python objects from pieces of string. The string definition should be based on the Markdown rules.
      Each class will have its Markdown definition based on a common set of static functions. Data are static.
      Use the cheatsheet to get more details about the Markdown.
    :return: Return the Python objects
    """
    return AresMarkDown.AresMarkDown().load(self, markDown)


  # --------------------------------------------------------------------------------------------------------------
  #
  #                                     CSS / JS WRAPPER DEFINITION
  # --------------------------------------------------------------------------------------------------------------
  def cssPyOvr(self, cssModuleName='CssOvr.py'):
    """
    :category: Style
    :rubric: CSS
    :type: Framework extension
    :example: aresObj.cssPyOvr()
    :dsc:
      Function to load bespoke AReS CSS class in order to override the ones defined in the css folder.
      This will allow the testing of a change in style of some components without impacting the other reports in the ecosystem.
    :return: The AresObj itself
    """
    if os.path.isfile(os.path.join(self.run.local_path, cssModuleName)):
      cssMod = importlib.import_module('%s.%s' % (self.run.report_name, cssModuleName.split('.')[0]))
      self.cssObj.ovr(cssMod)
    return self

  def addStyleSheet(self, moduleName, path=None):
    """
    :category: Table Style
    :rubric: CSS
    :type: Display
    :dsc:
      Override the style of the CSS for the list of class defined in the module. This will impact all the components using those
      styles in the framework only for this report.
    :return: The Table Python object
    """
    if path is not None:
      sys.path.append(path)

    cssMod = importlib.import_module("stylesheets.%s" % moduleName.replace(".py", ""))
    self.cssObj.ovr(cssMod)
    if hasattr(cssMod, 'charts'):
      self.cssObj._charts = cssMod.charts
    if hasattr(cssMod, 'colorHtml'):
      self.cssObj.colorCharts.update(cssMod.colorHtml)
    return self

  def cssCls(self, clsName, cssDict):
    """
    :category: Style
    :rubric: CSS
    :example: aresObj.cssCls('myCssClss', {"color": "Yellow"} ) ; => py_mycssclss
    :dsc:
      Create on the fly a CSS Class from a Python dictionary. The reference of the CSS Class is returned by this function.
      It is this reference that you should add to your HTML components
    :return: The reference of your CSS Class
    :link CSS Wikipedia definition: https://fr.wikipedia.org/wiki/Feuilles_de_style_en_cascade
    :link CSS Documentation: https://www.w3schools.com/css/
    """
    return self.cssObj.addCls(clsName, cssDict)

  def getCss(self, clsName, ovrData=None):
    """
    :category: Style
    :rubric: CSS
    :example: aresObj.getCss('CssTableRedCells')
    :example: aresObj.getCss('CssTableRedCells', {'font-weight': 'bold'})
    :dsc:
      Retrieve the CSS Class definition from the Python framework.
      This will also allow the definition update by defining some overrides.
      Overrides might be temporary changes in the class but the right practice will be to get them push to the core style framework
    :return: The Python CSS Object
    """
    if not hasattr(self.cssObj, 'cssOvr'):
      self.cssObj.cssOvr = {}
    cssCls = self.cssObj.cssOvr[clsName] if clsName in self.cssObj.cssOvr else self.cssObj.get(clsName)()
    if ovrData is not None:
      for name, value in ovrData.items():
        cssCls.update(name, value)
      self.cssObj.cssOvr[clsName] = cssCls
    return cssCls

  def cssUpdate(self, clsName, name, value):
    """
    :category: Style
    :rubric: CSS
    :example: >>> aresObj.cssUpdate("CssTitle", "background-color", "red")
    :dsc:
      Change the pre defined value of the Python CSS Classes defined in the CSS folder.
      This change will only be done for your active report. All the other reports will not be impacted.
      Please make sure that the properties you want to override are not part of the object signature.
      The object parameters are the last overrides, so they will remove your changes
    """
    self.cssObj.change(clsName, name, value)

  def setColor(self, category, index, colorCode):
    """
    :category: Color
    :rubric: CSS
    :dsc:
      Python function to override the defined colors
    :link hexadecimal color: https://www.w3schools.com/colors/colors_picker.asp
    """
    self.cssObj.colorCharts[category][index] = colorCode

  def setChartColors(self, colors):
    """
    :category: Color
    :rubric: CSS
    :type: PY
    :dsc:
      Change the default colors used in the Framework to display the different series in the charts.
      This change will impact the colors in all the charting libraries
    """
    self.cssObj._charts = colors

  def getColor(self, typeChart, i):
    """
    :category: Color
    :rubric: CSS
    :dsc:
      Python function to get the different pre defined color codes in the Framework
    :return: the hexadecimal code of the CSS color used in the CSS framework
    :link hexadecimal color: https://www.w3schools.com/colors/colors_picker.asp
    """
    return self.cssObj.colorCharts[typeChart][i]

  def addPyCls(self, pyCssCls):
    """
    :category: CSS Style
    :rubric: CSS
    :type: Framework Extension
    :dsc:
      Allow to add to the Framework bespoke CSS Configuration files.
    """
    if not isinstance(pyCssCls, list):
      self.cssObj.addPy(pyCssCls)
      return self.getCss(pyCssCls.__name__)

    clss = []
    for pyCss in pyCssCls:
      self.cssObj.addPy(pyCss)
      clss.append(self.getCss(pyCss.__name__))
    return clss


  # --------------------------------------------------------------------------------------------------------------
  #
  #                                     EXTERNAL CSS / JS LIBRARIES
  # --------------------------------------------------------------------------------------------------------------
  def addCss(self, filename):
    """
    :category: Style
    :type: Framework extension
    :rubric: HTML
    :example: aresObj.addCss("myLocalCss.css')
    :dsc:
      This will load your local CSS file when the report will be built. Then you will be able to use the new Styles in the different HTML Components
    :return: The Python object itself
    """
    self.cssLocalImports.add("%s/css/%s" % (self.run.report_name, filename))
    return self

  def addJs(self, filename):
    """
    :category: Javascript
    :type: Framework extension
    :rubric: HTML
    :example: aresObj.addJs("myLocalJs.js')
    :dsc:
      This will load your local javascript file when the report will be built. Then you will be able to use the new features in the different Javascript wrappers
    :return: The Python object itself
    """
    self.jsLocalImports.add("%s/js/%s" % (self.run.report_name, filename))
    return self


  # -----------------------------------------------------------------------------------------
  #                                    LOGGING AND DEBUGGING FUNCTIONS
  # -----------------------------------------------------------------------------------------
  def log(self, text, type='DEBUG'):
    """
    :category: Logs
    :type: Debug
    :rubric: PY
    :example: aresObj.log("This is a warning", type='WARNING')
    :dsc:
      This will write some logs to your local user.log file in \system\logs.
    :link Python Logging Documentation: https://docs.python.org/2/howto/logging.html
    """
    log = logging.getLogger('user')
    if type.upper() == 'INFO':
      log.info("| %s [ %s ] >> %s" % (self.run.report_name, self.run.script_name, text))
    elif type.upper() == 'WARNING':
      log.warning("| %s [ %s ] >> %s" % (self.run.report_name, self.run.script_name, text))
    else:
      log.debug("| %s [ %s ] >> %s" % (self.run.report_name, self.run.script_name, text))

  def jsConsole(self, jsFnc='data', isPyData=False):
    """
    :category: Javascript function
    :type: Debug
    :example: >>> aresObj.jsConsole() # This will display the internal data object in a javascript event
    :example: >>> aresObj.jsConsole('youpi', isPyData=True) # This will display the Python string in the browser console
    :rubric: JS
    :dsc:
      Function to wrap the Javascript method console.log to add messages to the browser console (F12).
      This will never be used during the Python run time. It can only be used in a Javascript event on the browser side
    :return: A String corresponding to the Javascript function to add messages to the console.
    :link Javascript documentation: https://www.w3schools.com/jsref/met_console_log.asp
    """
    if isPyData:
      jsFnc = json.dumps(jsFnc)
    return "console.log(%s)" % jsFnc

  def jsConsoleFnc(self, consoleFnc, jsFnc='data', isPyData=False):
    """
    :category: Javascript function
    :type: Debug
    :example: >>> aresObj.jsConsoleFnc('trace') # This will display a trace that show how the code ended up at a certain point
    :example: >>> aresObj.jsConsoleFnc('warn', 'Youpi', isPyData=True) # This will display the Python string in the browser console
    :rubric: JS
    :dsc:
      Generic Function to wrap all the Javascript methods available in the console visible in the browser console (F12).
      This will never be used during the Python run time. It can only be used in a Javascript event on the browser side
    :return: A String corresponding to the Javascript function.
    :link Javascript documentation trace: https://www.w3schools.com/jsref/met_console_trace.asp
    :link Javascript documentation clear: https://www.w3schools.com/jsref/met_console_clear.asp
    :link Javascript documentation count: https://www.w3schools.com/jsref/met_console_count.asp
    :link Javascript documentation time: https://www.w3schools.com/jsref/met_console_time.asp
    :link Javascript documentation timeEnd: https://www.w3schools.com/jsref/met_console_timeend.asp
    :link Javascript documentation trace: https://www.w3schools.com/jsref/met_console_trace.asp
    :link Javascript documentation warn: https://www.w3schools.com/jsref/met_console_warn.asp
    """
    if isPyData:
      jsFnc = json.dumps(jsFnc)
    if consoleFnc in ['trace', 'time', 'timeEnd', 'count', 'clear']:
      jsFnc = ''
    return "console.%s(%s)" % (consoleFnc, jsFnc)

  def jsAlert(self, jsFnc='data', toSource=False, isPyData=False):
    """
    :category: Javascript function
    :type: javascript wrapper
    :example: >>> aresObj.jsAlert() # This will display the internal data object in a javascript event
    :example: >>> aresObj.jsAlert('youpi', isPyData=True) # This will display the Python string
    :rubric: JS
    :dsc:
      Function to wrap the Javascript method alert to display alert popup messages.
      This will never be used during the Python run time. It can only be used in a Javascript event on the browser side
    :return: A String corresponding to the Javascript function to display alert popups
    :link Javascript documentation: https://www.w3schools.com/jsref/met_win_alert.asp
    """
    if isPyData:
      jsFnc = json.dumps(jsFnc)
    if toSource:
      return "alert(%s.toSource())" % jsFnc

    return "alert(%s)" % jsFnc


  # -----------------------------------------------------------------------------------------
  #                                    EXPORT OPTIONS
  # -----------------------------------------------------------------------------------------
  def to_word(self):
    """
    :category: Word
    :type: outputs
    :rubric: Export
    :example: aresObj.to_word()
    :dsc:
      Special output function used by the framework to export the report to a word document
      This function cannot be used directly as it will write the report on the server but some buttons are available on the top to trigger it
    """
    from docx import Document
    from docx.shared import RGBColor

    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    docName = '%s_%s.docx' % (self.run.script_name, timestamp)
    document = Document()
    for objId in self.content:
      if self.htmlItems[objId].inReport:
        try:
          self.htmlItems[objId].to_word(document)
        except Exception as err:
          errotTitle = document.add_heading().add_run("Error")
          errotTitle.font.color.rgb = RGBColor(255, 0, 0)
          errotTitle.font.italic = True
          errorParagraph = document.add_paragraph().add_run( (str(err)) )
          errorParagraph.font.color.rgb = RGBColor(255, 0, 0)
          errorParagraph.font.italic = True

    document.save(os.path.join(self.run.local_path, "saved", docName) )
    return docName

  def to_xls(self):
    """
    :category: Excel
    :rubric: export
    :example: aresObj.to_xls()
    :dsc:
      Special output function used by the framework to export the report to an Excel document
      This function cannot be used directly as it will write the report on the server but some buttons are available on the top to trigger it
    """
    ares_xls = requires("xlsxwriter", reason='Missing Package', install='xlsxwriter', autoImport=True, sourceScript=__file__)

    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    docName = '%s_%s.xlsx' % (self.run.script_name, timestamp)
    xlsDocument = os.path.join(self.run.local_path, "saved", docName)
    workbook = ares_xls.Workbook(xlsDocument)
    worksheet = workbook.add_worksheet()
    cursor = {'row': 0, 'col': 0}
    for objId in self.content:
      if self.htmlItems[objId].inReport:
        try:
          self.htmlItems[objId].to_xls(workbook, worksheet, cursor)
        except Exception as err:
          cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})
          worksheet.write(cursor['row'], 0, str(err), cell_format)
          cursor['row'] += 2

    workbook.close()
    return docName

  def to_ppt(self):
    """
    :category: PowerPoint
    :rubric: export
    :example: aresObj.to_ppt()
    :dsc:
      Special output function used by the framework to export the report to a PowerPoint document
      This function cannot be used directly as it will write the report on the server but some buttons are available on the top to trigger it
    """
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    docName = '%s_%s.pptx' % (self.run.script_name, timestamp)
    return docName

  def to_pdf(self):
    """
    :category: PDF
    :rubric: export
    :example: aresObj.to_pdf()
    :dsc:
    """
    docName = self.to_word()
    return docName

  def html(self, online=False):
    """
    :category: HTML
    :type: outputs
    :rubric: export
    :example: aresObj.html(online=False)
    :dsc:
      Special output function used by the framework to export the report to a isoldated HTML document
      This function cannot be used directly as it will write the report on the server but some buttons are available on the top to trigger it
    :return: The full HTML page (HTML tags and javascript definition)
    """
    if getattr(self, 'DEBUG', False):
      print("Debug mode activated, please press F12 in your browser to get Javascript details")

    # Add directly to the main page only components that are attached to the AresObj
    # All the components added to a container are not considered here.
    # The framework assume that the containers should take care of them
    if len(self.localFiles) > 0:
      self.jsGlobal.fnc('RemoveFile(src, fileName)', '$(src).parent().empty();%s' % self.jsPost("%s/remove/file/OUTPUTS/%s" % (self._urlsApp['ares-transfer'], self.run.report_name), "filename: fileName", isPyData=False))
      self.jsGlobal.fnc("RemoveLocalFiles(src, fileNames)", '$(src).parent().remove();%s' % self.jsPost('%s/locals/clean/%s' % (self._urlsApp['ares-transfer'], self.run.report_name), "filenames: fileNames", isPyData=False))
      self.jsGlobal.fnc("DownloadCachedFiles(filePath)", "NO_UNLOAD = true; %s " % self.jsSubmitForm('"%s/download/OUTPUTS/%s"' % (self._urlsApp['ares-transfer'], self.run.report_name), aresObjs=[("filename", "filePath")], isPyData=False, method='POST'))
      filesUsed, maxLenght, usedFileNames = [], 18, []
      for fileInfo in self.localFiles.values():
        fileInfo['full_path'] = "%(subFolder)s/%(filename)s" % fileInfo
        fileInfo['full_path_red'] = "%(subFolder)s/%(filename)s" % fileInfo
        usedFileNames.append(fileInfo['full_path'])
        if len( fileInfo['full_path'] ) > maxLenght:
          fileInfo['full_path_short'] = fileInfo['full_path'][-maxLenght:]
          fileInfo['full_path_red'] = "<div style='cursor:pointer;display:inline-block' title='%(full_path)s'>...%(full_path_short)s</div>" % fileInfo
        filesUsed.append( "<div>&nbsp;&nbsp;&bull; %(full_path_red)s - <b>%(timestamp)s</b>&nbsp;&nbsp;<i style='color:#C00000;cursor:pointer;margin-right:5px' class='fas fa-times' onclick='RemoveFile(this, \"%(full_path)s\")'></i> <i onclick='DownloadCachedFiles(\"%(full_path)s\")' style='cursor:pointer;' class='fas fa-file-download'></i> </div>" % fileInfo)
      self.notification('WARNING', "<b>%s</b> Cached Data Source Used" % len(self.localFiles),
                        '''
                        <br>Remove folder outputs/ to update your data <a href="%(urlTransfer)s/viewer/files/%(reportName)s" class="far fa-copy" style="color:#293846;margin-left:5px" target="_blank" title="Files management"></a>
                        <br>%(filesUsed)s<br>
                        <div style='color:#C00000;cursor:pointer' onclick='RemoveLocalFiles(this, JSON.stringify(%(usedFileNames)s))' ><b>&times;</b> Remove all temporary local files</div>''' % {"urlTransfer": self._urlsApp['ares-transfer'], "reportName": self.run.report_name, "filesUsed": "".join(filesUsed), "usedFileNames": json.dumps(usedFileNames) } )

    if len(self._dbErrors) > 0:
      errors = []
      for dbType, dbVals in self._dbErrors.items():
        errors.append("<div><strong>%s</strong>&nbsp;&nbsp;%s</div>" % (dbVals, dbType))
      self.notification('DANGER', 'Database errors', "".join(errors))

    onloadParts, windowLoadParts, htmlParts, jsGraphs, aresResult = [], [], [], [], {}
    for src in self.jsSources.values():
      if len(src['containers']) > 0:
        htmlParts.append(src['data'].html())

    for objId in self.content:
      if self.htmlItems[objId].inReport:
        htmlParts.append(self.htmlItems[objId].html())

    for jsFnc in self.jsOnLoadFnc:
      onloadParts.append(str(jsFnc))

    for jsFnc in self.jsFnc:
      onloadParts.append(str(jsFnc))

    for jsFnc in self.jsOnLoadEvtsFnc:
      onloadParts.append(str(jsFnc))

    if len(self._scroll) > 0:
      onloadParts.append('''
        $(window).scroll(function(event) {var screenPos = $(window).scrollTop() + $(window).height();%s})''' % ";".join(self._scroll))

    for jsFnc in self.jsWindowLoadFnc:
      windowLoadParts.append(str(jsFnc))
    #
    if self.shortcuts:
      onloadParts.append("$(document).on('keypress', 'body', function(e){var code = e.keyCode || e.which;")
      for key, action in self.shortcuts.items():
        onloadParts.append("if( %s ) { %s ; }" % (key, action) )
      onloadParts.append("});")

    # Section dedicated to the javascript for all the charts
    importMng = AresImports.ImportManager(online=online)
    if self.jsGraphs:
      jsGraphs.append("nv.addGraph(function() {\n %s \n});" % "\n\n".join(self.jsGraphs))
    self.aresUsage['ext'] = importMng.getFiles(self.cssImport, self.jsImports)
    aresResult['cssImports'] = importMng.cssResolve(self.cssImport, self.cssLocalImports)
    aresResult['jsImports'] = importMng.jsResolve(self.jsImports, self.jsLocalImports)
    aresResult['jsDocumentReady'] = "\n".join(onloadParts)
    aresResult['jsWindowLoad'] = "\n".join(windowLoadParts)
    aresResult['htmlParts'] = "\n".join(htmlParts)
    aresResult['jsGraphs'] = "\n".join(jsGraphs)
    aresResult['jsGlobal'] = str(self.jsGlobal)
    aresResult['exportData'] = self.exportCsv
    aresResult['cssStyle'] = str(self.cssObj)
    return aresResult


  # --------------------------------------------------------------------------------------------------------------
  #
  #                                     FRAMEWORK EXTENSIONS
  # --------------------------------------------------------------------------------------------------------------
  def addFileLoader(self, fileCls, fileExts, packages=None):
    """
    :category: Files
    :rubric: PY
    :type: Framework Extension
    :dsc:
      Add a bespoke file loader to the framework. This can be used to replace an existing mapping on a
      pre defined configuration
    """
    if AresFile.factory is None:
      AresFile.loadFactory()

    if not hasattr(fileCls, '_read'):
      raise Exception("File class %s cannot be loaded, function _read missing" % fileCls)

    pyFileCls = type("Ares%s" % fileCls.__name__, (fileCls, AresFile.AresFile), {})
    for ext in fileExts:
      pyFileCls.__fileExt = fileExts
      if packages is not None:
        pyFileCls._extPackages = packages
      AresFile.factory[ext] = pyFileCls

  def addChartConfig(self, configCls, chartFamily):
    """
    :category: Charts
    :rubric: PY
    :type: Framework Extension
    :dsc:
      Add an entry to the chart Fractory
    """
    newChart = graph.AresHtmlGraphFabric.Chart.addConfig(configCls, chartFamily)

  def addExternalConnector(self, connectorCls=None, fromFile=None):
    """
    :category: Connector
    :rubric: PY
    :type: Framework Extension
    :param connectorCls: the class in the connector if fromFile is not used and only a single cls is to be added
    :param fromFile: a file path pointing to a python module defining all the classes to be added
    :dsc:
      Add an external connector to the list of sources available to call (using aresObj.getData(alias))
    """

    if fromFile:
      if self.run.local_path:
        pass

      import sys, os, inspect
      folder = os.path.dirname(fromFile)
      moduleFile = os.path.basename(fromFile)
      sys.path.append(folder)
      mod = importlib.import_module(moduleFile.replace('.py', ''))
      for _, classDef in inspect.getmembers(mod, inspect.isclass):
        AresConn.AresConn.addDynamicConn(classDef)
    elif connectorCls:
      AresConn.AresConn.addDynamicConn(connectorCls)


  def addDatabaseConnector(self, databaseCls=None, fromFile=None):
    """
    :category: Database Connection
    :rubric: PY
    :type: Framework Extension
    :param databaseCls: the class in the connector if fromFile is not used and only a single cls is to be added
    :param sqlFamily: alias of the sqlFamily with which this database will be cable (i.e if the alias is 'newDb' -> aresObj.db('newDb') )
    :param fromFile: a file path pointing to a python module defining all the classes to be added
    :dsc:
      Add an external database connection to the list available to call (using aresObj.db() )
    """
    if fromFile:
      if self.run.local_path:
        pass

      import sys, os, inspect
      folder = os.path.dirname(fromFile)
      moduleFile = os.path.basename(fromFile)
      sys.path.append(folder)
      mod = importlib.import_module(moduleFile.replace('.py', ''))
      for _, classDef in inspect.getmembers(mod, inspect.isclass):
        AresDbBase.ConnDb.addDynamicDatabase(classDef)
    elif databaseCls:
      AresDbBase.ConnDb.addDynamicDatabase(databaseCls)


  def addTableFnc(self, datatableCls):
    """
    :category: Created Cell function
    :rubric: JS
    :type: Framework Extension
    :dsc:
      Allow the user to add new system functions which will be used in the Javascript to construct the table.
      This entry point can be used to define different javascript functions available in the Javascript.
    :link Documentation:
    :return: True if the class has been added to the factory, None otherwise
    """
    createdCell = type(datatableCls.__name__, (datatableCls, js.tables.JsTableCols.TableColsFrg), {})
    return js.tables.JsTableCols.extTableFactory(createdCell)

  def setHtml(self, htmlCls):
    """
    :category: New Html Object
    :rubric: PY
    :type: Framework Extension
    :dsc:
      Add a bespoke HTML configuration. This cannot override an existing one
    """
    fncCall = htmlCls.callFnc
    if hasattr(self, fncCall):
      raise Exception("Function already attached to the aresObj, please use a different callFnc name")

    aresCls = type("Html%s" % htmlCls.__name__, (htmlCls, html.AresHtml.Html), {})
    args = inspect.getargspec(aresCls.__init__).args[2:]
    def linkObj(*args):
      initArgs = [self] + list(args)
      return self.add(aresCls(*initArgs), sys._getframe().f_code.co_name)
    setattr(self, fncCall, linkObj)



class ReportAPI(Report):
  """
  :category: AReS Scripting API
  :rubric: PY
  :type: Local scripting API
  :dsc:
    Allow the local use of the different modules without any web interface. Implementation will be compatible with the projects but here only the data transformation will be the focus.
    It is possible from this API to reuse most of the AReS features to get and transform data.

    All the function dedicated to be applied in the JS or CSS layer will not be visible.
    It is also possible to export the data to different formats
  """

  class LocalRun(object):
    __slots__ = ['mac_address', 'host_name', 'current_user', 'report_name', 'script_name', 'local_path', 'url_root',
                 'title', 'is_local', 'url']

    def __init__(self):
      import __main__

      self.url = ''
      self.title = ''
      self.is_local = True
      self.current_user = 'local'
      self.report_name = 'script'
      self.host_name = 'Script'
      self.mac_address = ''
      self.script_name = 'documentation'
      self.local_path = os.path.dirname( __main__.__file__)

  def __init__(self, username=None, password=None, dbPath=None):
    #import logging
    #logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    super(ReportAPI, self).__init__(self.LocalRun())
    self.sourceDef = {}
    self.username = username
    self.password = password
    self.dbPath = os.path.join(os.getcwd(), '..', '..', 'system', 'sqlite') if dbPath is None else dbPath
    if username is not None and password is not None:
      self.refreshSource()

  def refreshSource(self):
    """
    :category: Security
    :rubric: PY
    :type: System
    :dsc:
        Refresh the dictionary of sources with the users credentials
    """
    dbAdmin = self.db(database=os.path.join(self.embedded_db, 'main_sqlite.db'),modelPath=os.path.join(self.embedded_db, 'models'))
    for rec in dbAdmin.select(['user_datasource_pmt']).where([dbAdmin.column("user_datasource_pmt", 'pmt_user') == self.username]).fetch():
      pmt_val = self.decrypt(rec['pmt_val'], self.password, rec['salt']) if rec['pmt_code'] == 'pwd' else rec['pmt_val']
      self.sourceDef.setdefault(rec['src_code'], {}).setdefault(rec['pmt_env'].upper(), {})[rec['pmt_code']] = pmt_val

  def addCredentials(self, alias, password, pmts, env='LIVE'):
    """
    :category: Security
    :rubric: PY
    :type: System
    :dsc:
        Allow the set up of credentials from the local scripting interface
    """
    import hashlib
    if not self.username and not self.password:
      raise Exception("You need to pass your Ares credentials (AresReportAPI(usr, pwd) so we can safely store your information")

    dbAdmin = self.db(database=os.path.join(self.embedded_db, 'main_sqlite.db'), modelPath=os.path.join(self.embedded_db, 'models'))
    encryptPwd = hashlib.sha256(bytes(self.password.encode('utf-8'))).hexdigest()
    userId = None
    for rec in dbAdmin.select(['user']).where([dbAdmin.column("user", 'email') == self.username]).fetch():
      userId = rec[0]
    # Check if the user exist other create the entry in the database
    if userId is None:
      dbAdmin.insert('user', {'email': self.username, 'password': encryptPwd}, commit=True)
      for rec in dbAdmin.select(['user']).where([dbAdmin.column("user", 'email') == self.username]).fetch():
        userId = rec[0]
    # Then add the credentials to user_datasource_pmt
    systEncPass, salt = self.crypt(password, self.password)
    for key, val in pmts.items():
      dbAdmin.insert('user_datasource_pmt', {'src_code': alias, 'pmt_user': self.username, 'pmt_env': env, 'pmt_code': key, 'pmt_val': val,
                                             'salt': None}, commit=True)
    dbAdmin.insert('user_datasource_pmt', {'src_code': alias, 'pmt_user': userId, 'pmt_env': env, 'pmt_code': 'pwd',
                                           'pmt_val': systEncPass, 'salt': salt}, commit=True)
    self.refreshSource()

  def addProxy(self, url, port, proxyUser='', proxyPass=''):
    """
    :category: Security
    :rubric: PY
    :type: System
    :dsc:
        Simplified function to set up proxy settings
    """
    self.addCredentials('PROXY', proxyPass, {'url': url, 'proxy_user': proxyUser, 'port': port})

  def fncs(self, reportName=None, reportPath=None, fileFullPath=None):
    if fileFullPath is not None:
      filename = os.path.basename(fileFullPath).replace(".py", "")
      sys.path.append( os.path.dirname(fileFullPath) )
      mod = importlib.import_module(filename)
      functions_list = [o for o in inspect.getmembers(mod) if inspect.isfunction(o[1])]
      for fncName, fnc in functions_list:
        argsFnc = fnc.__code__.co_varnames
        if 'aresObj' in argsFnc:
          setattr(self, fncName, types.MethodType(decFnc(self.aresFncs, 'python', filename, self.run.report_name, fnc), self, Report))
        else:
          setattr(self, fncName, decFnc(self.aresFncs, 'python', filename, self.run.report_name, fnc))
      return self

    else:
      if reportName is None or reportPath is None:
        raise Exception("reportName and reportPath should be defined to import functions")

      reportPath = os.path.join(reportPath, reportName)
      sys.path.append(os.path.dirname(reportPath))
      return super(ReportAPI, self).fncs(report_name=reportName, local_path=reportPath)

  def help(self, category=None, rubric=None, type=None, value=None, enum=None, section=None, lang='eng', outType=None):
    """
    :category: Python function
    :rubric: PY
    :dsc:
      Display the Python documentation of the requested object.
      This is done by reading all the documentation from the object.
      Documentation is by default displayed in the Python console but it can be also written to a static html page.
      It is possible to zoom in the documentation to get more details
    :example: >>> aresObj.help()
    """
    outStream = AresMarkDown.DocCollection(self)
    outStream.breadcrumb(["Scripting API"])
    docAres = AresMarkDown.AresMarkDown.loadsDsc(ares.doc.DocAresScriptAPI)
    outStream.add(docAres, 'dsc')
    outStream.export(outType)

  def services(self, params, reportName=None, scriptName=None, reportPath=None):
    """

    :return:
    """
    servicePath = os.path.join(reportPath, reportName, 'sources')
    sys.path.append(servicePath)
    mod = importlib.import_module(scriptName.replace(".py", ""))
    return mod.getData(None, params)

  def getStyles(self, htmlComponent, **kwargs):
    """
    :category: CSS Style
    :rubric: PY
    :type: Configuration
    :example: aresObj.getStyles("title", level=1)
    :dsc:
      Should retrieve the component style from the function calls and the parameters. The data is retrieved from
      the mock data and cannot be supplied. This is a easy shortcut to retrieve the configuration to override.
    :return: The full component Style definition (pyCss and CSS attributes added to the container)
    """
    htmlObj = getattr(self, htmlComponent)(self.mocks(htmlComponent), **kwargs)
    cssStyles = {}
    for cssStyle in htmlObj.pyStyle:
      cssStyles[cssStyle] = str(self.getCss(cssStyle))
    return {'pyCss': cssStyles, 'container': htmlObj.attr['css']}

  def css(self):
    """
    :category: CSS
    :rubric: PY
    :type: Styles
    :dsc:
      Return the CSS configuration attached to the report for all the components
    :return: The CSS String to be added to the HTML Page
    """
    return str(self.cssObj)

  def getMarkDown(self, htmlComponent, **kwargs):
    """
    :category: Markdown
    :rubric: PY
    :type: Configuration
    :example: aresObj.getMarkDown("title", level=1)
    :dsc:
      return the Markdown string of the selected entry point in AReS.
    :return:
    """
    htmlObj = getattr(self, htmlComponent)(self.mocks(htmlComponent), **kwargs)
    if hasattr(htmlObj, 'jsMarkDown'):
      return htmlObj.jsMarkDown(self.mocks(htmlComponent), **kwargs)

    return "No MarkDown defined"

  def markDownToAres(self, filePath):
    """
    :category: Markdown
    :rubric: PY
    :type: Conversion
    :dsc:
      Function defined to read a Markdown file and convert this to a valid report.
      This will produce the expected structure in a static mannner. No Javascript or event will be added and the
      style used will be the default one in the components.
    :return: A new file with the content of the report
    """
    # TODO: Test all the components using Markdown
    splitFile = filePath.split(".")
    AresMarkDown.AresMarkDown(filePath).convert("%s.py" % ".".join(splitFile[:-1]))

  def post(self, url, data):
    """
    ;category:
    :rubric:
    :type:
    :dsc:

    :example:
    """
    import requests
    import json

    r = requests.post(url, data)
    return json.loads(r.text)

  def mapPackage(self, alias, version=None, moduleMaps=None, reqMaps=None):
    """
    :category: External Packages
    :type: Framework extension
    :rubric: HTML
    :example: aresObj.mapPackage('nvd3', version='7.7.0')
    :example: aresObj.mapPackage('nvd3', reqMaps={'d3': {'version': '5.7.0'}})
    :dsc:
      Allows the test of packages upgrades locally by changing the link to use to load the external packages.
      This feature help test the new version on the official cdnjs links.
      Upgrade can be done only locally in the scripting layer and then should be proposed to your IT team.
    :example: aresObj.mapPackage('js', 'plotly', 'https://cdnjs.cloudflare.com/ajax/libs/plotly.js/1.43.1/')
    """
    for conf in [AresImports.CSS_IMPORTS, AresImports.JS_IMPORTS]:
      if alias in conf:
        if version is not None:
          for mod in conf[alias]['modules']:
            mod['version'] = version
        if moduleMaps is not None:
          for mod in conf[alias]['modules']:
            if mod['script'] in moduleMaps:
              mod.update(moduleMaps[mod['script']])
        if reqMaps is not None:
          if 'req' in conf[alias]:
            for req in conf[alias]['req']:
              if req['alias'] in reqMaps:
                req.update(reqMaps[req['alias']])

  def configFile(self, filePath):
    """
    :category: Report Settings
    :rubric: PY
    :type: Configuration
    :dsc:
        Add a configuration file to the report to override object configurations
    :example:
        {"ares_config": "Olivier", "select": { "value": "B" } }
        aresObj.configFile(r"examples\config\fileTest.json")
    """
    objAttrs = {}
    with open(filePath) as f:
      data = json.load(f)
      if not 'ares_config' in data:
          raise Exception("ares_config definition needed to be a valid report configuration")

      for k, v in data.items():
        if 'value' in v:
          self.http[k] = v['value']
        else:
          objAttrs[k] = v['attrs']
    return objAttrs

  def toHtml(self, fileName=None, filePath=None, title=None, serverUrl=None, template='base', withDoc=False):
    """
    :category: HTML
    :rubric: PY
    :type: Output
    :dsc:
      Produce an HTML file with the report. This HTML page will use external Javascript and external libraries either
      from a local server (if the URL is defined) or online otherwise
    :example: aresObj.toHtml(fileFullPath=r'C:\...\table.html', serverUrl='http://127.0.0.1:5000', title="Test table")
    """
    def render_template_string(val):
      """ Wrap the function to convert the URL """
      res = re.findall('<link rel="stylesheet" href="{{ url_for\(\'static\',filename=\'([a-zA-Z0-9-./]*)\'\) }}" type="text/css">', val)
      if res:
        resolvedCss = ['<link rel="stylesheet" href="%s/static/%s" type="text/css">' % (serverUrl, val.replace("\\", "/")) for val in res]
        return "\n".join(resolvedCss)

      res = re.findall('<script language="javascript" type="text/javascript" src="{{ url_for\(\'static\',filename=\'([a-zA-Z0-9-./]*)\'\) }}"></script>', val)
      if res:
        resolvedJs = ['<script language="javascript" type="text/javascript" src="%s/static/%s"></script>' % (serverUrl, val.replace("\\", "/")) for val in res]
        return "\n".join(resolvedJs)

      return val

    if filePath is None:
      filePath = os.path.join(os.getcwd(), 'html')
    if not os.path.exists(filePath):
      os.makedirs(filePath)
    if fileName is None:
      fileName = os.path.basename(sys.modules['__main__'].__file__)

    fileFullPath = os.path.join(filePath, fileName.replace(".py", '.html'))
    if fileFullPath:
      if os.path.exists(fileFullPath):
        os.remove(fileFullPath)

    AresImports.render_template_string = render_template_string
    data = self.html(online=serverUrl is None)
    data['title'] = 'Local Report' if title is None else title
    if not os.path.isfile(template):
      tmpFile = html.templates.AresHtmlTmplBase.DATA.replace("|safe", "").replace("%", "%%").replace("{{ ", "%(").replace(" }}", ")s")
    else:
      tmpFile = open(template).read().replace("|safe", "").replace("%", "%%").replace("{{ ", "%(").replace(" }}", ")s")
    data['content'] = data['htmlParts']
    with open(fileFullPath, "w") as f:
      f.write(tmpFile % data)

    if withDoc:
      fileName = fileName.replace(".py", "")
      docFile = os.path.join(os.getcwd(), "doc", "%s.amd" % fileName)
      if not os.path.exists(docFile):
        raise Exception("%s.amd Documentation file missing from doc/ folder" % fileName)

      docAresObj = ReportAPI()
      with open(docFile) as f:
        docAresObj.markdown(f.read())
      data = docAresObj.html(online=serverUrl is None)
      data['title'] = 'Local Report' if title is None else title
      if not os.path.isfile(template):
        tmpFile = html.templates.AresHtmlTmplBase.DATA.replace("|safe", "").replace("%", "%%").replace("{{ ", "%(").replace(" }}", ")s")
      else:
        tmpFile = open(template).read().replace("|safe", "").replace("%", "%%").replace("{{ ", "%(").replace(" }}", ")s")
      data['content'] = data['htmlParts']
      fileDocFullPath = os.path.join(filePath, "%s_doc.html" % fileName)
      with open(fileDocFullPath, "w") as f:
        f.write(tmpFile % data)

  # -----------------------------------------------------------------------------------------
  #                                    AJAX WRAPPER FUNCTIONS
  # -----------------------------------------------------------------------------------------
  def jsPost(self, url, jsData=None, jsFnc='', cacheObj=None, isPyData=True, isDynUrl=False, httpCodes=None,
             htmlCodes=None, datatype='json', context=None, debug=False):
    """
    :category: Local set up
    :rubric: JS
    :type: Ajax
    :dsc:
      Mimic an ajax query by reading locally a file. This does not work with Chrome as it will consider this as a
      cross origins request (a security breach). It is possible to run Chrome to remove this security check (but this
      should be done only if you run local files
    :example:
      aresObj.button('test').click(aresObj.jsPost("GetChartSeries.py", jsFnc=[aresObj.jsAlert()]))
      file GetChartSeries.json [{"my": "json"}]
    """
    serverFilePath = os.path.join(os.getcwd(), 'server', url.replace(".py", ".json"))
    if os.path.exists(serverFilePath):
      with open(serverFilePath) as f:
        if isinstance(jsFnc, list):
          jsFnc = ";".join(jsFnc)
        data = json.load(f)
        return '''data = %(data)s; %(jsFnc)s''' % {'data': json.dumps(data), 'jsFnc': jsFnc}

    self.notification("WARNING", "Server files missing", "Please produce the file %s" % os.path.join('.', 'server', url.replace(".py", ".json")).replace("\\", "/"))
    return ''

  def serverFile(self, scriptName, scriptPath, pmts=None):
    """
    :category: Cached files
    :rubric: PY
    :type: Ajax
    :dsc:
      function in the scripting layer to write text file from scripts used as services in the Ajax layer.
      This will produce local cached files which will be used in the Ajax functions.
      By default this write a file in the server folder in the scripting section
    """
    serverPath = os.path.join(os.getcwd(), 'server')
    if not os.path.exists(serverPath):
      os.makedirs(serverPath)
    sys.path.append(scriptPath)
    mod = importlib.import_module(scriptName.replace(".py", ""))
    if pmts is None:
      pmts = {}

    tmpFileName = "%s.json" % scriptName.replace(".py", "")
    with open(r'%s/%s' % (serverPath, tmpFileName), 'w') as outfile:
      json.dump(mod.getData(self, pmts), outfile)


  # -----------------------------------------------------------------------------------------
  #                                    INFO FUNCTIONS
  # -----------------------------------------------------------------------------------------
  def chartsInfo(self):
    """
    :category: Documentation
    :rubric: PY
    :type: System
    :dsc:
      Return the details of the chart factory
    :example: aresObj.chartsInfo()
    """
    for libChart, chartType in graph.AresHtmlGraphFabric.Chart.create().items():
      print("")
      print("Library: %s" % libChart)
      for chart, chartMod in chartType.items():
        print("  %s:%s" % (chart, chartMod.__doc__))

  def pivotsInfo(self):
    """
    :category: Documentation
    :rubric: PY
    :type: System
    :dsc:
      return the details of the pre defined aggregators.
      Only the official ones will be retrieve from this method.
    :example: aresObj.pivotsInfo()
    """
    for name, aggObj in dict(js.tables.JsPivotFncs.getAggFnc()).items():
      print("")
      print("Aggregator Name: %s" % name)
      print("Optional: %s" % json.dumps(getattr(aggObj, '_dflts', {})))
      print("Formula: %s" % aggObj.push)

  def tablesInfo(self):
    """
    :category: Documentation
    :rubric: PY
    :type: System
    :dsc:

    :example: aresObj.tablesInfo()
    """
    for name, objCol in js.tables.JsTableCols.TableCols().get().items():
      print("")
      print("Column Function Name (Alias): %s" % name)
      print("Class: %s" % objCol.__name__)
      print("Optional: %s" % json.dumps(getattr(objCol, '_dflts', {})))
      print("Description:")
      print(AresMarkDown.AresMarkDown.loads(objCol.__doc__, section='dsc').strip())

  def getPackageInfo(self, alias, version=None, inRecursion=False):
    """
    :category: Documentation
    :rubric: PY
    :type: System
    :example: aresObj.getPackageInfo('nvd3')
    :dsc:
      Return the documentation on the modules used. This is available to simplify the override of the different
      modules configurations in each scripts. This is available only on the scripting part for local runs.
    """
    for conf, impType in [(AresImports.CSS_IMPORTS, 'CSS'), (AresImports.JS_IMPORTS, 'JS')]:
      if not inRecursion:
        print("")
        print("")
        print("## %s Definition" % impType)
      if alias in conf:
        if 'req' in conf[alias]:
          for req in conf[alias]['req']:
            self.getPackageInfo(req['alias'], req.get('version'), inRecursion=True)
        print("")
        print("# %s " % alias)
        print("[Official Website](%s)" % conf[alias].get('website', ''))
        print("Mapped Modules")
        for mod in conf[alias].get('modules', []):
          _version = mod['version'] if version is None else version
          path = mod['path'] % {'version': _version}
          dtls = {'script': mod['script'], 'version': _version, 'cdnjs': '%s/%s/%s' % (mod['cdnjs'], path, mod['script'])}
          print("  %(script)s - version: %(version)s, [CDNJS](%(cdnjs)s) " % dtls)
