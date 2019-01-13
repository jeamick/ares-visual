#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DSC = {
  'eng': '''
:category: CSS Framework Design
:rubric: PY
:dsc:
  ## CSS Framework
  
  ![image](css3.png)
  
  CSS generator, this module will make easier the addition of CSS classes and also will allow the creation of themes
  4 CSS Levels according to the need. None all of them can be overridden without impacting the whole framework.
  
  All the CSS configurations are using Python dictionaries based on any existing keys and values defined in the CSS standards [CSS W3C Documentation](https://www.w3schools.com/css/)
  You can also get more details about this [here](https://www.w3.org/standards/webdesign/htmlcss)

  **Please do not override or change any function starting with __**. If it is really needed please contact us before working on
  your report. Those functions are intended to be internal functions that any child class should never need directly

  ### CSS Level 1 

  Parameters defined in the signature of the methods calls in Ares.py
  This level of CSS is very bespoke and users are invited to override them in the report directly by using the different
  standardised keywords. For example:
    - Color is used for the font-color CSS properties
    - size for the font-size
    ...
  
  You can validate your CSS Style [here](https://validator.w3.org/#validate_by_input)
  Default values are common in the framework anyway. Those parameter are optional.

  For example the below will change the color in the first record and the font size on the second one.

  ```python
    aresObj.tabs([{'value': 'Fraise', 'key': 'Fraise', 'color': 'blue', 'isActive': True}, {'value': 'Apple', 'key': 'Apple', 'size': 20}])
  ```

  ### CSS Level 2 

  Parameters defined in the HTML Structure. please have a look at the documation in AresHtml.py for more details
  about the HTML framework. The idea of this layer is not to be overridden. Basically here it mainly style attributes in the
  different HTML tags and those attributes are mandatory for the correct display of the HTML element.
  Usually this CSS layer is not used in the simple HTML components. It is more likely used in the nested component to ensure
  a correct structure

  For example in the textBubble HTML String function it is defined:

  ```markdown
    style="padding-top:5px;margin-left:5px;text-align:center;background-color:white" 
  ```

  ### CSS Level 3 
  
  Python classes defined in the different CSS modules. Those modules can be used dynamically from the HTML component
  using the method addPyCss then be defining the class in the corresponding HTML element. Those CSS style will be written directly by
  python and it will add on the fly the needed CSS classes in the report header. This in the future will help use in selecting the
  correct style (and it should be the most often used)

  For example in the Slider class it is added the Python CSS Style CssSubTitle
  
  ```python
      self.aresObj.jsOnLoadFnc.add('%s.slider({value: %s});' % (self.jqId, self.vals))
      if self.title is not None:
        self.aresObj.cssObj.add('CssSubTitle')
  ```
  
  ### CSS Level 4 
  
  Pure CSS Style coming from existing framework. For example [Bootstrap](https://getbootstrap.com/docs/3.3/css/) is coming with its complete suite of styles
  and you can directly use then by defined the class name in the method addClass of your HTML component. Going forward this 4th CSS
  usage should be reduced and the python layer should automatically generate CSS Styles for each report

  For example in List ze use the Bootstrap styles
  
  ```python
      class List(AresHtml.Html):
          cssCls = ['list-group']
  ```
'''
}


import os
import sys
import json
import collections
import logging

from ares.Lib import AresMarkDown
from ares.Lib.css import CssBaseColor

# The factor with all the different CSS classes available
# This can be reloaded if a new one is added
factory = None

def load(forceReload=False):
  """ Load the factory with the all the different CSS classes defined in the framework """
  global factory

  if factory is None or forceReload:
    path = os.path.abspath(__file__)
    dirPath = os.path.dirname(path)
    sys.path.append(dirPath)
    tmpFactory = {}
    for pyFile in os.listdir(dirPath):
      if pyFile == 'CssBase.py':
        continue

      if pyFile.endswith(".py") and pyFile != '__init__.py':
        try:
          pyMod = __import__(pyFile.replace(".py", ""))
          for name in dir(pyMod):
            if name.startswith("Css"):
              tmpFactory[str(name)] = {'class': getattr(pyMod, name), 'file': pyFile}
        except Exception as e:
          # unexpected issue in the factor (A new class might be wrong)
          logging.warning(e)

    # TODO: Think about a better implementation
    # Atomic action to update the factor
    # the above if statement should remain very quick as it might be a source of synchronisation issues in the future
    factory = tmpFactory
  return factory

def convertCss(content, isMin=False, fomatted=False):
  """
  :category: CSS Converter
  :type: Style
  :rubric: PY
  :dsc:
    Translate the CSS structure to the CSS Ares expected format.
    The result of this function is done in the console. This function should not be used if you cannot see the print on the console.
  """
  import re

  cssResults = collections.defaultdict(list)
  pattern = re.compile("[\n\t ]*([a-zA-Z-0-9:\\n\\t\,._ ]*){([a-zA-Z0-9;:()/\\n\\t-._ ]*)}", re.IGNORECASE | re.DOTALL | re.MULTILINE)
  for match in pattern.finditer(content):
    cssIdRaw, cssContent = match.groups()
    cssIds = cssIdRaw.split(',')
    cssContent = cssContent.replace("\t", " ")
    for line in cssContent.split("\n"):
      cleanLine = line.strip()
      if cleanLine:
        attr, value = cleanLine.split(":")
        value = value.strip().replace(";", "")
        for cssId in cssIds:
          cssResults[cssId.strip()].append({'attr': attr, 'value': value})
  for key, vals in cssResults.items():
    print(key)
    if fomatted:
      for val in vals:
        print(val)
    else:
      print(key, vals)


class CssStyle(list):
  """
  :category: CSS
  :rubric: PY
  :type: constructor
  :dsc:
    This is proxy class to a list dedicated to monitor the CSS classes
    The use of this class will help to manage the different possible attributes
    but also to be able going forward to add more flexibility
  """
  attrs = None

  def append(self, paramsCss):
    """
    :category: CSS Style Builder
    :rubric: PY
    :type: style
    :example: >>> cssObj.append( {'attr': 'color'} )
    :dsc:
      Add parameters to the CSS Style generated from Python
    :link CSS Class Documentation: https://www.w3schools.com/html/html_classes.asp
    """
    if self.attrs is None:
      self.attrs = set()
    self.attrs.add(paramsCss['attr'])
    super(CssStyle, self).append(paramsCss)

  def update(self, params):
    """
    :category: CSS Style Builder
    :rubric: PY
    :type: style
    :example: >>> cssObj.update( {"color": "red"} )
    :dsc:
      Update an existing attribute to a Python CSS class
    :link CSS Class Documentation: https://www.w3schools.com/html/html_classes.asp
    """
    if self.attrs is None:
      for attr, val in params.items():
        self.append({'attr': attr, 'value': val})
    else:
      for attr, val in params.items():
        if attr in self.attrs:
          for rec in self:
            if rec['attr'] == attr:
              rec['value'] = val
              break

        else:
          self.append({'attr': attr, 'value': val})


class CssObj(object):
  """
  :category: CSS / Python Collection
  :rubric: PY
  :dsc:
    CSS Object is the main Python wrapper used to create the on the fly CSS files
    The idea will be to use this as the bespoke CSS file in a report. There will be nothing done outside of python in this
    framework. Everything like CSS or Javascript will be automatically generated and defined from the components used in the
    reports.
  """

  minify = False # https://en.wikipedia.org/wiki/Minification_(programming)

  def __init__(self, aresObj=None):
    """ Instantiate the object and also load the CSS Python factory """
    self.__factory, self.aresObj = load(), aresObj
    self.cssStyles, self.cssBespoke = {}, {}
    # The below dictionary is the only one used in the CSS Framework to set the colors
    # This can be changed in order to get different color charts in a bespoke environment
    self.colorCharts, self.cssMaker = {}, CssBaseColor.CssColorMaker(aresObj)
    # TODO: Remove this special logic
    self._charts = list(self.cssMaker.charts)
    for color in self.cssMaker.colors:
      self.colorCharts.setdefault( color['type'], []).append( color['color'])
    self.__bespokeAttr = collections.defaultdict(dict)

  def help(self, category=None, rubric=None, type=None, value=None, enum=None, section=None, function=None, lang='eng', outType=None):
    outStream = AresMarkDown.DocCollection(self.aresObj)
    if enum == 'colors':
      outStream.title("Pre defined colors", cssPmts={"margin-left": "5px", "font-size": "30px", "font-variant": "small-caps"})
      outStream.append("Colors used in AReS are based on hexadecimal codes. You can find the definition here: [W3C colors website](https://www.w3schools.com/colors/colors_hexadecimal.asp)")
      outStream.hr()
      CssBaseColor.docEnum(self.aresObj, outStream, lang)
      outStream.hr()
      outStream.title("Definition", level=2)
      if hasattr(CssBaseColor, 'DSC'):
        docSection = AresMarkDown.AresMarkDown.loads(
          CssBaseColor.DSC.get('eng', CssBaseColor.DSC.get('eng', '')))
        outStream.add(docSection, 'dsc')
    elif enum == 'styles':
      outStream.title("CSS Styles in AReS Components", level=2)
      data = []
      for alias, cssCls in load().items():
        docDetails = AresMarkDown.AresMarkDown.loads(cssCls['class'].__doc__)
        data.append( [alias, cssCls['file'], docDetails.getAttr('dsc').strip()] )
      outStream.table(['pyCSS Class', 'Module', 'Description'], data, pmts={"searching": 'True'})
      outStream.src(__file__)
    outStream.export(outType)

  def ovr(self, pyMod):
    """
    :category: CSS / Python Overrides
    :rubric: PY
    :dsc:
      This will go thought all the classes in the module to try to override the ones defined in the framework.
      This entry is a shortcut to change CSS Styles without having to update the main framework.
      Those changes will only impact the current report.
    :tip:
      If you create a module CssOvr.py in the root of your environment, all the CSS Classes will be automatically
      loaded and if some already existing in the framework, they will be overridden.
    """
    for name in dir(pyMod):
      if name.startswith("Css") and name != 'CssBase':
        self.cssBespoke[str(name)] = getattr(pyMod, name)

  def addPy(self, pyCssCls):
    """
    :category: Css Classes
    :rubric: PY
    :type: Framework Extension
    :dsc:
      Add a bespoke class to the CSS Style Factory. This class is added on the fly and it cannot override an existing one.
    """
    cssCls = type(pyCssCls.__name__, (pyCssCls, CssCls), {})
    if not pyCssCls.__name__ in self.__factory:
      self.__factory[pyCssCls.__name__] = {'class': cssCls, 'file': 'external (%s)' % self.aresObj.run.report_name}
    self.add(pyCssCls.__name__)

  def addCls(self, clsName, params):
    """
    :category: CSS / Python Collection
    :rubric: PY
    :dsc:
      Function to define a CSS class on the fly from the Python layer.
    :return: The Python CssCls object
    """
    styles = [{'attr': key, 'value': val} for key, val in params.items()]
    self.cssBespoke[clsName] = type(clsName, (CssCls, ), dict(__style=[]))()
    self.cssBespoke[clsName].style = styles
    self.cssStyles.update(self.cssBespoke[clsName].getStyles())
    return self.cssBespoke[clsName]

  def change(self, cssCls, name, value):
    """
    :category: CSS / Python Overrides
    :rubric: PY
    :dsc:
      Store the attributes to be changed / overridden for a given class
    """
    self.__bespokeAttr[cssCls][name] = value

  def reload(self):
    """
    :category: CSS function
    :rubric: PY
    :dsc:
      Force the CSS cache to be refreshed.
      This should never be used locally as a simple change in the code will refresh all the caches as Flask will automatically restart
    """
    self.__factory = load(forceReload=True)

  def get(self, clsName):
    """
    :category: CSS function
    :rubric: PY
    :dsc:
      Returns the CSS attributes for a given Python class Name
    :return: The Python CSS Object
    """
    pyCss = self.cssBespoke[clsName] if clsName in self.cssBespoke else self.__factory.get(clsName, {}).get('class', None)
    return pyCss

  def add(self, clsName, htmlId=None, htmlTag=None, htmlType=None, cssRef=None):
    """
    :category: CSS function
    :rubric: PY
    :dsc:
      Add the Python Class to the report CSS objects. The bespoke style overrides will be applied first. The default are the
      standard styles defined in the root of the CSS module
    :return: The Python CSS Id (defined from the method setId in CssCls)
    """
    cssMod = self.__factory.get(clsName, {}).get('class', None) if not clsName in self.cssBespoke else self.cssBespoke[clsName]
    if cssMod is None:
      return None

    pyCss = cssMod(htmlId=htmlId, htmlTag=htmlTag, htmlType=htmlType, cssRef=cssRef)
    pyCss.colorCharts = self.colorCharts
    if clsName in self.__bespokeAttr:
      for name, value in self.__bespokeAttr[clsName].items():
        pyCss.update(name, value)
    self.cssStyles.update(pyCss.getStyles())
    return pyCss.cssId

  def __str__(self):
    """
    :category: CSS function
    :rubric: PY
    :dsc:
      This function will be in charge of producing the best CSS content according to the need.
      If minify is set to true it will have to try to create groups and to aggregate the data before writing a one liner
    :return: The String with all the CSS classes and definition
    """
    if self.minify:
      return "".join([ "%s %s" % (key, val) for key, val in self.cssStyles.items() if val != '{}'])

    # no need for performance in the web report, certainly an investigation
    return "\n".join(["%s %s" % (key, val) for key, val in self.cssStyles.items() if val != '{}'])

  def getStyle(self, clsName):
    """
    :category: CSS function
    :rubric: PY
    :dsc:
      Get the CSS Attributes for a given Python CSS Class Name
    :return: Return a String representing the CSS Attributes for a given Python CSS Class Name
    """
    if clsName in self.cssBespoke:
      return self.cssBespoke[clsName](None).getStyles().values()[0][1:-1]

    return self.__factory[clsName]['class'](None).getStyles().values()[0][1:-1]

  def pyRef(self, clsName):
    """
    :category: CSS function
    :rubric: PY
    :dsc:
      Convert the CSS Class Name to a standardized Class Name within this Python Framework
    :return: A string with the CSS converted name
    """
    return 'py_%s' % clsName.lower()

  def getClsTag(self, clsNames):
    """
    :category: HTML function
    :rubric: PY
    :dsc:
      Create the CSS Tag to be added to the HTML Element to consider the different classes.
      This will only add a class tag with the list of class names defined.
    :return: A string with the HTML Class information to add to the element
    """
    return 'class="%s"' % " ".join([self.pyRef(clsName) for clsName in clsNames])


class CssCls(object):
  """ CSS Base class of all the derived styles
  :category: CSS Class
  :rubric: CSS
  :dsc:
    Main class to create from the Python CSS Framework well defined CSS Fragment which will be added to the page.
    Each CSS Class create will produce a Class Name and it will be the one used in all the AReS components to set the Style.
    This module will only consider the Static CSS classes and all the bespoke CSS Style used to defined more specifically a component will
    be defined either in the string method of the component (old way) or in the jsStyle variable of the component (new way)
  :TODO:
    work on a way to optimize the CSS String generated in the header
    example: http://www.cssportal.com/css-optimize/
  """

  # This is a private function and it is not supposed to be updated
  # please use the variable style in the class for any change
  # It should be transformed ONLY in this class
  # The structure of the dictionaries is using attr and value to be able to add some special
  # keys in the future.
  __style = None

  reqCss = None # List of CSS Configurations required
  preceedTag, parentTag, childrenTag, directChildrenTag, htmlTag = None, None, None, None, None
  cssId = None # CSS Id

  # Default values for the style in the web portal
  colors10 = ['#5dd45d'] # the different colors used as reference in the framework
  fontSize, headerFontSize = '14px', '18px'

  # State variables, should have the same structure than __style
  # Those variables are the ones used directly so please do not change then
  # we usse static variables to nake it easier to retrieve in the editor
  # target is not implemented and this feature is done in the javascript
  hover, active, checked, disabled, empty, enabled, focus, link, visited = 9 * [None]

  # Item CSS selector, should also have the sa,e structure than __style
  before, after = None, None
  childKinds = None

  def __init__(self, htmlId=None, htmlTag=None, htmlType=None, cssRef=None):
    """ Instantiate a CSS object with the different possible classes to be used in the style of the components

    """
    if self.htmlTag is not None:
      htmlTag = self.htmlTag
    self.setId(htmlId=htmlId, htmlTag=htmlTag, htmlType=htmlType, cssRef=cssRef)
    self.style = CssStyle()
    for l in getattr(self, "_%s__style" % self.__class__.__name__, {}):
      self.style.append(dict(l))
    # To add some special features required for this component.
    # This is to avoid having to put multiple times the same line of CSS in each class
    # This will simplify a lot the testing
    if self.reqCss is not None:
      for css in self.reqCss:
        for l in getattr(css, "_%s__style" % css.__name__, []):
          self.style.append(dict(l))

    # Store the different CSS Styles defined in the python layer to dictionaries
    # This will allow the fact that some bespoke configuration can inherit from the main configuration
    # but some special attributes might be overidden.
    # It is not possible to change this differently from the components as it is supposed to be
    # static and it will be used as a text file in the future
    # If more overrides are needed please use the function .css() available in the components
    # or talk to your IT team in charge of this framework
    self.eventsStyles = {}
    for state in  ['hover', 'active', 'checked', 'disabled', 'empty', 'enabled', 'focus', 'link', 'visited', 'after', 'before']:
      if getattr(self, state, None) is not None:
        self.eventsStyles[state] = CssStyle()
        for rec in getattr(self, state):
          self.eventsStyles[state].append(dict(rec))

    # To add CSS Style link tr:nth-child(even)
    if self.childKinds is not None:
      if not isinstance(self.childKinds, list):
        self.childKinds = [self.childKinds]
      for childKind in self.childKinds:
        childValue = "%(type)s%(value)s" % childKind
        self.eventsStyles[childValue] = CssStyle()
        for rec in childKind['style']:
          self.eventsStyles[childValue].append(dict(rec))

  def customize(self, style, eventsStyles):
    """
    :category: CSS Class override
    :rubric: CSS
    :dsc:
      Function defined to override or define the static CSS parameters when an CSS Style python object is instanciated.
      This will allow for example to define the color according to the standard ones without hard coding them.
      In the base class this method is not defined
    """
    pass

  # -------------------------------------------------------------------------------
  #                                    CSS SELECTORS
  #
  # https://www.w3schools.com/cssref/css_selectors.asp
  # -------------------------------------------------------------------------------

  def __states(self):
    """
    :category: CSS Class Style Builder
    :rubric: CSS
    :dsc:
      Function used to define for a given class name all the different mouse and event properties that the CSS could allowed.
      This private method will check the static definition and create the entry in the Python CSS Class.
      This will allow to define in the framework some events like hover, focus...
      Only the following selector are defined so far ('hover', 'active', 'checked', 'disabled', 'empty', 'enabled', 'focus', 'link', 'visited', 'after', 'before')
    :link W3C Documentation: https://www.w3schools.com/cssref/css_selectors.asp
    :link W3C Hover example: https://www.w3schools.com/cssref/sel_hover.asp
    """
    cssEvent = {}
    for state, cssRecord in self.eventsStyles.items():
      if state in ['before', 'after']:
        cssEvent["%s::%s" % (self.cssId, state)] = self.cssData(cssRecord)
      else:
        cssEvent["%s:%s" % (self.cssId, state)] = self.cssData(cssRecord)
    return cssEvent

  # -------------------------------------------------------------------------------
  #                                    CSS ID SYNTHAX
  #
  # https://www.w3schools.com/css/css_syntax.asp
  # -------------------------------------------------------------------------------
  def ispreceedBy(self, tag):
    """
    :category: CSS Class Style Builder
    :rubric: CSS
    :dsc:
      Tag at the same level but defined just before this one
    """
    self.preceedTag = tag

  def hasParent(self, parentTag):
    """
    :category: CSS Class Style Builder
    :rubric: CSS
    :dsc:
      HTML tag parent of this one. For example TR is parent of TD
    """
    self.parentTag = parentTag

  def addChildrenTags(self, tags):
    """
    :category: CSS Class Style Builder
    :rubric: CSS
    :dsc:
      HTML tags children of this one. For example TR is parent of TD
    """
    if self.childrenTag is None:
      self.childrenTag = tags
    else:
      self.childrenTag.extend(tags)

  @property
  def classname(self):
    """
    :category: CSS function
    :rubric: PY
    :dsc:
      Property to convert the CSS Class Name to a standardized Class Name within this Python Framework
    :return: A string with the converted name
    """
    return "py_%s" % self.__class__.__name__.lower()

  def setId(self, htmlId=None, htmlTag=None, htmlType=None, cssRef=None):
    """
    :category: CSS function
    :rubric: PY
    :dsc:
      Global method to define the CSS ID for a given CSS Configuration class
    :return: The CSS Id as a String
    """
    if cssRef:
      # Shortcut to set direcly the name of the CSS class
      self.cssId = cssRef
      return cssRef

    cssIdParts = []
    if self.parentTag is not None:
      cssIdParts.append("%s > " % self.parentTag)
    elif self.preceedTag is not None:
      cssIdParts.append("%s ~ " % self.preceedTag)
    # Special case when the style is very specific to one item in the page
    if htmlId is not None:
      cssIdParts.append("#%s" % htmlId)
    else:
      # Default behaviour as the framework will directly attach html classes
      # to CSS styles defined in this python framework
      if htmlTag is not None:
        if htmlTag.startswith(":"):
          cssIdParts.append(".%s%s" % (self.classname, htmlTag))
        else:
          cssIdParts.append("%s.%s" % (htmlTag, self.classname))
      else:
        cssIdParts.append(".%s" % self.classname)
    # Extra feature if a HTML tag type is defined
    # for example all the html objects with a name defined as youpi [name=youpi]
    if htmlType is not None:
      cssIdParts.append("[%s=%s]" % (htmlType[0], htmlType[1]))
    self.cssId = ''.join(cssIdParts)
    return self.cssId

  def add(self, attr, value):
    """
    :category: CSS Style Builder
    :rubric: PY
    :example: add('color', 'blue')
    :dsc:
      Add a Style to the CSS object
    """
    self.style.append({'attr': attr, 'value': value})

  def update(self, cssObj):
    """
    :category: CSS Style Builder
    :rubric: PY
    :dsc:
      Override the CSS style attributes with the new CSS object
    """
    self.style.update(cssObj.style)

  def cssData(self, paramsCss):
    """
    :category: CSS Style Builder
    :rubric: PY
    :dsc:
      Convert a Python CSS Class to a well defined CSS Class
    :return: Returns the Python dictionary in a CSS format
    """
    # Function to override some parameters
    self.customize(self.style, self.eventsStyles)
    return "{%s}" % "; ".join(["%(attr)s:%(value)s" % css for css in paramsCss])

  def getStyles(self, cssId=True):
    """
    :category: CSS Style Builder
    :rubric: PY
    :dsc:
      Function to process the Static CSS Python configuration and to convert it to String fragments following the CSS Web standard.
    :return: A Python dictionary with all the different styles and selector to be written to the page for a given Python CSS Class
    """
    res = {}
    if self.childrenTag is not None:
      res["%s %s" % (self.cssId, self.childrenTag)] = self.cssData(self.style)
      for key, val in self.__states().items():
        skey = "::" if "::" in key else ":"
        splitKey = key.split(skey)
        res["%s %s%s%s" % (splitKey[0], self.childrenTag, skey, splitKey[1])] = val
    elif self.directChildrenTag is not None:
      res["%s > %s" % (self.cssId, self.directChildrenTag)] = self.cssData(self.style)
      for key, val in self.__states().items():
        skey = "::" if "::" in key else ":"
        splitKey = key.split(skey)
        res["%s > %s%s%s" % (splitKey[0], self.directChildrenTag, skey, splitKey[1])] = val
    else:
      res[self.cssId] = self.cssData(self.style)
      res.update(self.__states())
    return res

  def getStyleId(self, htmlRef):
    """
    :category: CSS Style Builder
    :rubric: PY
    :dsc:
      Produce based on the CSS Python classes the correct CSS Name
    return: Returns the CSS part to be written in the page by HTML tag
    """
    htmlId = "#%s" % htmlRef
    cssData = str(self)
    if htmlId in self.cssObj.cssStyles:
      if self.cssObj.cssStyles[htmlId] != cssData:
        raise Exception("CSS style conflict for %s" % htmlRef)

    self.cssObj.cssStyles[htmlId] = cssData

  def getStyleTag(self, htmlTag):
    """
    :category: CSS Style Builder
    :rubric: PY
    :dsc:
      Produce based on the CSS Python classes the correct CSS Name
    return: Returns the CSS part to be written in the page by HTML tag
    """
    self.cssObj.cssStyles[htmlTag] = self.cssData(self.style)

  def getStyleCls(self, clss, htmlType=None):
    """
    :category: CSS Style Builder
    :rubric: PY
    :dsc:
      Produce based on the CSS Python classes the correct CSS Name with the right class selector
    return: Returns the CSS part to be written in the page by class name
    :link W3C Documentation: https://www.w3schools.com/cssref/sel_class.asp
    """
    if htmlType is not None:
      self.cssObj.cssStyles["%s.%s" % (htmlType, clss)] = self.cssData(self.style)
    else:
      self.cssObj.cssStyles[".%s" % clss] = self.cssData(self.style)

  def getStyleName(self, htmlType, name):
    """
    :category: CSS Style Builder
    :rubric: PY
    :dsc:
      Add the CSS Fragment for a very bespoke CSS configuration based on HTML item names.
      This can be used when only some components with the tag (or not) are impacting by a CSS Style
    :return: Returns the CSS part to be written in the page by class name
    """
    self.cssObj.cssStyles["%s[name='%s']" % (htmlType, name)] = self.cssData(self.style)

  def update(self, name, value):
    """
    :category: CSS Style Builder
    :rubric: PY
    :dsc:
      Update or extend the CSS attribute of a python CSS class.
      Please make sure that the properties you want to override are not part of the object signature.
      The object parameters are the last overrides, so they will remove your changes
    """
    for attrDate in self.style:
      if attrDate['attr'] == name:
        attrDate['value'] = value
        break

    else: # Append a new property
      self.style.append( {"attr": name, 'value': value})

  def __str__(self):
    """
    :category: CSS
    :rubric: JS
    :dsc:
      Return je CSS dictionary which could be used by the Jquery module directly.
    :return: A Javascript dictionary as a string python object
    """
    return "{%s}" % ", ".join([ "%s: %s" % (s['attr'], json.dumps(s['value'])) for s in self.style])

  def to_dict(self):
    """
    :category: CSS
    :rubric: PY
    :dsc:
      Return the Python dictionary with the CSS attributes
    :return: The Style dictionary
    """
    return dict([(s['attr'], s['value']) for s in self.style])

