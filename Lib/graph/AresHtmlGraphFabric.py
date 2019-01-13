#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


# http://jsfiddle.net/andycooper/PcjUR/1/

import os
import inspect
import logging
import importlib

from ares.Lib.html import AresHtml
from ares.Lib.js.configs import JsConfig

# The list of charting libraries used in the framework and considered in the plot aresObk entry point
JS_CHARTS = [
  {"chart": 'ChartJs', 'dsc': {'eng': 'The ChartJS Javacript Framework'} },
  {"chart": 'Plotly', 'dsc': {'eng': 'The Plotly.js Javacript Framework'} },
  {"chart": 'Billboard', 'dsc': {'eng': 'The Billboard.js Javascript Framework'} },
  {"chart": 'C3', 'dsc': {'eng': 'The C3.js Javascript Framework'} },
  {"chart": 'D3', 'dsc': {'eng': 'The base library for most of the charting ones'} },
  {"chart": 'Vis', 'dsc': {'eng': 'The Vis.js Javascript Framework'} },
  {"chart": 'NVD3', 'dsc': {'eng': 'The NVD3 Javascript Framework'} },
  {"chart": 'DC', 'dsc': {'eng': 'The DC Javascript Framework'} }
]

DSC = {
    'eng':
'''
:category: Charts
:rubric: PY
:type: Factory
:dsc:
The preferred Charting library is ChartJs but as mentioned in this module most of the javascript frameworks are available in order to ensure a good coverage.
Thus by leveraging on those modules it will be easy to build screens to visualise the data.
** Do not forget to prototype first by using the user_scripts framework. This will avoid the pain of creating both at the same time the data sets and the screens. **

The main libraries available in this framework are the one listed below. The Python user interface should allow performing any usual charting transformations. The only differences will be if some extra specific parameters are needed.

## Chart Object creation

The best way to create a chart is to rely on the factory by using the generic ares function chart().

```python
aresObj.chart('area', sourceFile, seriesNames=seriesNames, xAxis='Date')
aresObj.chart('pie', sourceFile, seriesNames=seriesNames, xAxis='Date')
aresObj.chart('line', sourceFile, seriesNames=seriesNames, xAxis='Date')
aresObj.chart('bar', sourceFile, seriesNames=seriesNames, xAxis='Date')
aresObj.chart('scatter', sourceFile, seriesNames=seriesNames, xAxis='Date')
```

## Charts Properties

it is possible to add / remove charts properties by either using to **common bespoke functions** or by setting directly a parameter based on the **generic functions**.
In this section both examples will be detailled in order to get a good knowledge in the way this should be used. 
**Do not hesitate to get in touch with your IT team if you thing that some settings should be wrapper to a bespoke function to help the community and avoid the copy pasting of lines of code**

#### Common bespoke functions

>>>List
Function and definition
showLabels, to set the chart attribute to display the labels to the chart 
showGrid, to set the chart attribute to display the grid lines
setSeriesColor, to set a specific color for a series
yFormat, to change the format of the y axis
<<<

#### Generic functions

Generic function will be added in the right place of the chart definition both languages (Python and Javascript) can be used to set correctly those parameter.
To pass a Javascript parameter the flag isPyData should be set to False. Thus no conversion of the data will be done and javascript function can be passed.

>>>List
Function and definition
addSeriesAttr, generic function to set an bespoke attribute to a series
addAttr, generic function to set a attribute to the chart definition
delAttr, generic function to delete an attribute to the chart definition
<<<

## Charts Styling

#### Change in the CSS properties

```python
c1. = aresObj.chart('bar', sourceFile, seriesNames=seriesNames, xAxis='Date')
c1.addAttr('stacked', True)

cjs = aresObj.chart('area', [], seriesNames=['a', 'c'], xAxis='b', htmlCode='multiChart', chartFamily=chartFam)
cjs.addSeriesAttr(None, {'label': 'Youpi', 'pointStyle': 'triangle', 'pointRadius': 10})
cjs.setSeriesColor(['#008000', '#FFC0CB'])
```
 
#### Change the color series

```python
barSeries = aresObj.chart('bar', myList, seriesNames=['B', 'C'], xAxis='A', chartFamily=chartFam)
barSeries.addSeriesAttr(1, {"backgroundColor": 'red'} ).addSeriesAttr(0, {"backgroundColor": 'green'})

# For a bespoke series
barSeries.setSeriesColor(['#008000', '#FFC0CB'])

# By using a stylesheet file
aresObj.addStyleSheet("TableCssOvr")
# The stylesheet file should have to parameter charts defined
charts = ['#00e626','#00CC22','#00b31e', '#8B98E8', '#005566', '#269493', '#66bbaa', '#bbeeee', '#4e1c72',
          '#bb88ff', '#d1b3ff','#d15f32','#ffccaa','#ffeebb','#485d8c']
```

## Charts event management

It is possible to reuse most of the events defined for the AReS Html components. Basically to add a click event on a chart, the only thing to do is to add the below lines of codes to the chart

#### Click events

```python
lineChart = aresObj.chart('line', myList, seriesNames=['B', 'C'], xAxis='A', chartFamily=chartFam)
lineChart.click( aresObj.jsConsole() )
```

#### Filters

It is only possible to add an event on a data filter to refresh the chart if the underlying data has change. This can be done with the below lines of code.
**Please notice the use of the parameter None in the jsGenerate function**. This will remove the use of the usual data and it will point to its original data source (which has been filtered).
Also a global filter can only be used if there is a valid htmlCode attached to this object. Indeed the htmlCode should not be dynamic in order to share your view settings with other users.

```python
sourceFile = aresObj.file('filename.csv')
c2 = aresObj.chart('area', sourceFile, htmlCode='myChart2', seriesNames=seriesNames, xAxis='Date', globalFilter=True)
aresObj.select(sourceFile, dfColumn='direction', htmlCode="select_filter", globalFilter=True).change(c2.jsGenerate(None))
```

In the above example, because the two containers are linked to the same data ** sourceFile ** any event on one will add a filtering rule to the data.
The function *.change(c2.jsGenerate(None))* will then force the update. 

## Chart modules specificities

Even if as part of this wrapper the target is to create a common interface to be able to change the library without having to perform any change on the Python side, some specific functions can be not implemented yet.
So if you need further details about what is possible on the different Charting libraries, the best is to go on the library documentation online and to then use the common function presented above to inject as a javascript sting the missing information.
This is easy to perform by please make sure you discussed with your IT team first to ensure that it is not already available ad overall to make sure this might be added to the common interface properly.  
__
The community is definitely the main driver for changes and improvements but please make sure your report is not using not sustainable piece of javascript. This might in the furture caue problems if it is not properly flagged.
__
To get more pratical examples, please have a look at the existing reports and the examples [here](/reports/run/examples/DashBoardChartJS)
'''
}


# The main charting factory. This will reuse by the different interface dedicated to the different javascript frameworks
CHARTS_FACTORY = None

def loadFactory():
  """
  :category: Charting Factory
  :rubric: PY
  :type: Factory
  :dsc:
    This function will load in memory the different charts configurations available in each javascript charting libraries.
    This function will retrieve the different configurations from the different location and allow the mapping between an
    alias and its object.
  :return: The content of the factory
  """
  tmp, chartLibs = {}, []
  for jsChart in JS_CHARTS:
    chartLibs.append(jsChart["chart"])
    if jsChart["chart"] in ['Vis', 'Billboard', 'DC']:
      continue

    try:
      chartMod = importlib.import_module('ares.configs.%(chart)s' % jsChart)
      for script in os.listdir(os.path.dirname(chartMod.__file__)):
        if script.startswith(jsChart['chart']) and script.endswith('py'):
          for name, obj in inspect.getmembers(importlib.import_module("ares.configs.%s.%s" % (jsChart['chart'], script.replace(".py", ""))), inspect.isclass):
            if getattr(obj, 'chartCall', None) is not None:
              tmp.setdefault(jsChart['chart'], {})[getattr(obj, 'chartCall')] = obj
    except Exception as err:
      logging.warning("%s, error %s" % (jsChart['chart'], err))
  # Add the configurations attached to the new configuration framework
  for chartFam, chartDef in JsConfig.getConfigs(chartLibs).items():
    for chartAlias, chartCls in chartDef.items():
      tmp.setdefault(chartFam, {})[chartAlias] = chartCls
  return tmp


class Chart(AresHtml.Html):
  """
  :category: Generic Chart Fabric
  :rubric: PY
  :dsc:
    This class will be used in order to return the preferred Chart Python interface to the user.
    Indeed each Javascript Chart framework has its own specificities and this method will only renderer the preferred one.
    It will be then possible to use all the available method of the specific object received from this Factory.
    Methods between the different frameworks will tend to be aligned.

    To get more details it is possible to use the help method on the object (or the help method on the aresObj to get something in Html)

  """
  name, category, callFnc = 'Chart', 'Charts', 'plot'

  @staticmethod
  def create():
    """
    :category: Chart Interface
    :rubric: PY
    :type: Factory
    :dsc:
      Call the internal module function to load the charting factory and return the content. This wrapper will also
      store the results in order to avoid having to reload it multiple times. This will guarantee a unique parsing
      of the different modules for efficiency purposes.
    :return: The Charting factory
    """
    global CHARTS_FACTORY
    if CHARTS_FACTORY is None:
      CHARTS_FACTORY = loadFactory()  # atomic function to store all the different table mapping
    return CHARTS_FACTORY

  @staticmethod
  def addConfig(configCls, chartFamily):
    """
    :category: Chart Interface
    :rubric: PY
    :type: Framework Extension
    :dsc:
        Entry point in the framework in order to create bespoke charts configurations on the fly.
        Existing charts definition cannot be overriden. This is only designed to allow the creation of new classes in
        the reports without expecting a release of the whole framework
    """
    factory = Chart.create()
    if factory is not None and not configCls.alias in factory:
      newChart = JsConfig.getConfig(configCls, chartFamily)
      if newChart is not None:
        factory[chartFamily][newChart.alias] = newChart
    return newChart

  @staticmethod
  def get(aresObj, chartType, chartFamily):
    """
    :category: Charts
    :rubric: PY
    :type: Chart fabric
    :dsc:
        Return the chart object according to the chartType selected by the user.
        This will go throught the different javascript frameworks and try to find the preferred one.
        The priority will be set using the order of the frameworks in the global variable JS_CHARTS
    :return: The chart object
    """
    factory = Chart.create()
    if chartFamily is not None:
      return chartFamily

    for chartFam in JS_CHARTS:
      if chartType in factory[chartFam['chart']]:
        return chartFam['chart']

  @staticmethod
  def html(chartObj, strAttr, strChart):
    """
    :category: Charts
    :rubric:
    :type:
    :dsc:
      <i style="margin:0 5px;cursor:pointer" class="far fa-comment-alt"></i>
      <i style="margin:0 5px;cursor:pointer" class="fas fa-table"></i>
      <a href="" style="margin:0 5px;cursor:pointer" class="fas fa-download" onclick="this.href = window['%(htmlId)s_chart'].toBase64Image()" download></a>
      <i style="margin:0 5px;cursor:pointer" class="fas fa-redo-alt"></i>
    """
    options = []
    for pyFnc, icon, aType in [('toTsv', 'fa fa-file-excel', 'download="data.tsv"'), ('toImg', 'fas fa-download', 'download'), ('toImg', 'fas fa-search-plus', '')]:
      if hasattr(chartObj, pyFnc):
        options.append('<a href="" style="margin:0 5px;cursor:pointer" class="%(icon)s" onclick="this.href = %(fnc)s" %(aType)s></a>' % {'icon': icon, 'fnc': getattr(chartObj, pyFnc)().replace('"', "'"), 'aType': aType})
    return '''
      <div %(strAttr)s id="%(htmlId)s_container">  
        %(strChart)s
        <span style="bottom:0;margin:0 0 5px 0;width:100%%">
          <i style="margin:0 5px 0 0" class="fas fa-clock"></i>Last update: <div id="%(htmlId)s_time" style="display:inline-block"></div>
          <div style="display:inline-block;float:right;margin-right:0px">
            %(options)s
          </div>
        </span>
      </div>
      ''' % {'htmlId': chartObj.htmlId, 'strAttr': strAttr, 'strChart': strChart, 'options': "".join(options)}

  @staticmethod
  def jsLastUpdate(htmlId):
    return 'var d = new Date(); $("#%(htmlId)s_time").html( d.getFullYear() + "-" + d.getMonth() + "-" + d.getDate() + " " + d.getHours() + ":" +  d.getMinutes() + ":" + d.getSeconds() );' % {"htmlId": htmlId}

  @classmethod
  def resolveList(cls, currDict, currList, listResult):
    for item in currList:
      if isinstance(item, dict):
        subList = []
        cls.resolveDict(item, subList)
        listResult.append("{ %s }" % (", ".join(subList)))
      elif isinstance(item, list):
        subList = []
        cls.resolveList(currDict, item, subList)
        listResult.append("[%s]" % (",".join(subList)))
      else:
        listResult.append(item)

  @classmethod
  def resolveDict(cls, currDict, listResult):
    for key, item in currDict.items():
      if isinstance(item, dict):
        subList = []
        cls.resolveDict(item, subList)
        listResult.append("%s: {%s}" % (key, ", ".join(subList)))
      elif isinstance(item, list):
        subList = []
        cls.resolveList(currDict, item, subList)
        if key == 'data':
          listResult.append("%s: [%s]" % (key, ",".join(map(lambda x: str(x), subList))))
        else:
          listResult.append("%s: [%s]" % (key, ",".join(subList)))
      else:
        listResult.append("%s: %s" % (key, item))


def docEnum(aresObj, outStream, lang='eng'):
  """
  :category: Chart
  :rubric: PY:
  :type: Configuration
  """
  chartFactory = Chart.create()
  for alias in JS_CHARTS:
    outStream.link(" **%s - %s**" %  (alias['chart'], alias['dsc'].get(lang, alias['dsc']['eng'])), "api?module=import&enum=package-%s" % alias['chart'], cssPmts={"margin": "5px"})
  outStream.hr()
  outStream.title("Chart Factory", cssPmts={"margin-left": "5px", "font-size": "30px", "font-variant": "small-caps"})
  outStream.append([
    'The Chart factory will return the best charting library. Those modules are obviously wrapped in the AReS layer but any specific feature from the javascript library can be implemented.',
    'The **aresObj** function used to benefit from the factory is **chart**. To override it the parameter to supply in this call is **chartFamily**'])
  chartTable = {}
  for jsChart in JS_CHARTS:
    for chartType in sorted(chartFactory[jsChart['chart']]):
      chartTable.setdefault(chartType, []).append(jsChart['chart'])
  data = []
  for chartType in sorted(chartTable):
    row = ["<b>%s</b>" % chartType]
    for c in JS_CHARTS:
      if c['chart'] in chartTable[chartType]:
        if chartTable[chartType][0] == c['chart']:
          row.append('<font color="green" style="font-weight:bold">Default</font>')
        else:
          row.append('Supported')
      else:
        row.append('')
    data.append(row)
  outStream.title("Prority orders in the factory", level=2)
  outStream.table(['Chart Type'] + [c['chart'] for c in JS_CHARTS], data, pmts={"rowsPerPage": -1})
  outStream.title("Alternative options", level=2)
  outStream.append([
    'The factory logic can be overriden and you can get the chart from an other framework by overriding the parameter **chartFamily** with the expected charting alias',
    'If you force to use a charting library, please keep in mind that it might be removed as part of the continous releases process of AReS.',
    'You will be able to follow the changes by looking at the [releases page](releases) or by contacting your IT team'
  ])
