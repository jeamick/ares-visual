#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import re
import os
import time
import json
import sys
import inspect
import importlib
import logging

import ares.doc

DSC = {
  'eng': '''
:category: Markdown
:rubric: PY
:type: Base class
:dsc:
## Markdown Framework

This framework is following the Markdown standard in order to write static documentation.
As part of the creation of the different components some extended rules have been added in order to ensure the use of very bespoke components and also allow a great flexibility.
This documentation will show you the different markdowns rules already in place.

If you have any questions regarding the principle of Markdowns, please have a quick look at the [wikipage](https://fr.wikipedia.org/wiki/Markdown)
Also the below link could be quite interesting to get more examples:
[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

Markdown syntax is a standard used in many programming language but also by website to make the first implementation much easier
'''}


class DocCollection(list):
  """
  :category: Doc String
  :rubric: DOC
  :type:
  :dsc:

  """
  def __init__(self, aresObj):
    self.aresObj = aresObj

  def breadcrumb(self, paths, options=None, lang="eng"):
    """

    :return:
    """
    bubbles = []
    rows = ["<a href='/api'>Framework</a> / <a href='/api?module=local'>Scripting API</a>"]
    if len(paths) > 1:
      rows[0] = "%s / ... <a href=''>%s</a>" % (rows[0], paths[0])
    if options is not None:
      for key, val in options.items():
        if paths[-1] == key:
          bubbles.append(
            "<div title='%s' style='cursor:pointer;padding:1px 5px;border:1px solid black;display:inline-block;margin:0 2px;border-radius:5px;color:white;background-color:%s'>%s</div>" % (val[lang], self.aresObj.getColor("blueColor", 4), key))
        else:
          bubbles.append("<a href='/api?enum=%s' title='%s' style='cursor:pointer;padding:1px 5px;border:1px solid black;display:inline-block;margin:0 2px;border-radius:5px;color:black;text-decoration:none'>%s</a>" % (key, val[lang], key) )
      rows.append("<div style='margin:3px 0'>%s</div>" % "".join(bubbles))
    self.append("<div>%s</div>" % "".join(rows))

  def breadcrumb2(self, levels, selecPath):
    rows = []
    for i, vals in enumerate(levels):
      bubbles = []
      for val in vals:
        if val.lower() == selecPath[i].lower():
          bubbles.append("<div style='cursor:pointer;padding:1px 5px;border:1px solid black;display:inline-block;color:white;background-color:%s;margin:0 2px;border-radius:5px'>%s</div>" % (self.aresObj.getColor("blueColor", 5), val) )
        else:
          bubbles.append("<div style='cursor:pointer;padding:1px 5px;border:1px solid black;display:inline-block;margin:0 2px;border-radius:5px'>%s</div>" % val)
      rows.append("<div style='margin:3px 0'>%s</div>" % "".join(bubbles))
    self.append("<div>%s</div>" % "".join(rows))

  def title(self, val, level=1, cssPmts=None):
    if val != '':
      self.append("%s %s" % ("".join(['#'] * level), val), cssPmts)

  def formula(self, val):
    if val != '':
      self.append('$$ %s $$' % val)

  def link(self, val, url, icon='fas fa-chevron-circle-right', cssPmts=None):
    self.append("&nbsp;&nbsp;[!(%s) %s](%s)" % (icon, val, url), cssPmts)

  def hr(self):
    self.append("***")

  def table(self, header, records, tableType='base', cssPmts=None, pmts=None):
    data = ["|".join(header)]
    for rec in records:
      if isinstance(rec, dict):
        row = []
        for h in header:
          row.append( rec[h] )
      else:
        row = rec
      data.append( "|".join( row ))

    if pmts is not None:
      data.append("--%s" % ";".join(["%s:%s" % (k, v) for k, v in pmts.items()]))
    if cssPmts is not None:
      data.append("@%s" % ";".join(["%s:'%s'" % (k, v)   for k, v in cssPmts.items()]))
    self.append("\n".join(["---Table:%s" % tableType] + data + ["---"]))

  def append(self, val, cssPmts=None):
    if isinstance(val, list):
      val= "\n".join(val)
    if cssPmts is not None:
      val = "%s css%s" % (val, json.dumps(cssPmts).replace('"', ''))
    for v in val.split("\n\n"):
      super(DocCollection, self).append("%s\n" % v)

  def add(self, docStrObj, key):
    self.append(docStrObj.getAttr(key))
    if docStrObj.source is not None:
      self.src(docStrObj.source)

  def src(self, source):
    self.append("<div style='width:100%%;color:%s;font-style:italic;text-align:right;font-size:12px;padding-right:5px'>Source: %s</div>" % (self.aresObj.getColor('greyColor', 3), source))

  def params(self, param, lang='eng'):
    return ares.doc.DocAresPmts.PARAMETERS.get(param, {}).get(lang, 'Missing %s version' % lang)

  def code(self, vals, language='python'):
    if isinstance(vals, list):
      vals= "\n".join(vals)
    if vals != '':
      match = re.search(">>>\((.*)\)", vals)
      if match:
        vals = vals.replace(match.group(0), '')
        vals = "%s\n>>> %s" % (vals, match.group(1))
      self.append("\n".join(["```%s" % language, vals.strip(), "```"]))

  # ---------------------------------------------------------------------------------------------------------
  #                                           OUTPUT FUNCTIONS
  #
  def to_txt(self):
    print("\n".join(self))

  def to_ppt(self):
    from pptx import Presentation

    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    docName = '%s_%s.pptx' % (self.aresObj.run.script_name, timestamp)
    prs = Presentation()
    currentSlide = prs.slides.add_slide(prs.slide_layouts[6])
    AresMarkDown().convertStr(self, self.aresObj)
    for objId in self.aresObj.content:
      if self.aresObj.htmlItems[objId].inReport:
        try:
          self.aresObj.htmlItems[objId].to_ppt(prs, currentSlide)
        except Exception as err:
          logging.warning(err)
    prs.save(docName)

  def to_word(self):
    from docx import Document
    from docx.shared import RGBColor

    timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    docName = '%s_%s.docx' % (self.aresObj.run.script_name, timestamp)
    document = Document()
    AresMarkDown().convertStr(self, self.aresObj)
    for objId in self.aresObj.content:
      if self.aresObj.htmlItems[objId].inReport:
        try:
          self.aresObj.htmlItems[objId].to_word(document)
        except Exception as err:
          errotTitle = document.add_heading().add_run("Error")
          errotTitle.font.color.rgb = RGBColor(255, 0, 0)
          errotTitle.font.italic = True
          errorParagraph = document.add_paragraph().add_run( (str(err)) )
          errorParagraph.font.color.rgb = RGBColor(255, 0, 0)
          errorParagraph.font.italic = True
    document.save(os.path.join(self.aresObj.run.local_path, docName))

  def to_html(self):
    AresMarkDown().convertStr(self, self.aresObj)

  def export(self, outType):
    if outType in ['ppt', 'pptx']:
      self.to_ppt()
    elif outType in ['doc', 'docx', 'word']:
      self.to_word()
    elif outType in ['HTML', 'html']:
      self.to_html()
    else:
      self.to_txt()


class DocString(dict):
  """
  :category: Doc String
  :rubric: DOC
  :type:
  :dsc:

  """
  source = None

  def getAttr(self, dsc):
    return "\n".join(self.get(dsc, ['']))


class AresMarkDown(object):
  """
  :category: AReS Markdown
  :rubric: DOC
  :type: constructor
  :dsc:

  """
  markDownMappings, markDownBlockMappings = None, None

  def __init__(self, fullFilePath=None):
    sys.path.append(os.path.join(os.getcwd(), 'ares', 'Lib'))
    if fullFilePath is not None:
      content = ""
      if fullFilePath.endswith('amd'):
        pyFile = open(fullFilePath)
        content = pyFile.read()
        pyFile.close()
      self.content = content.split("\n\n")
    self.loadModules()

  def loadModules(self):
    """ Fabric to load all the components in memory and use the match logic
    :category: Bespoke User Functions
    :rubric: DOC
    :type:
    :dsc:

    :return:
    """
    # Store the modules
    from ares.Lib import html
    from ares.Lib import graph

    self.markDownMappings, self.markDownBlockMappings = [], []
    for alias, mod in [('html', html), ('graph', graph)]:
      for script in os.listdir(os.path.dirname(mod.__file__)):
        if script.endswith(".py"):
          for name, obj in inspect.getmembers(importlib.import_module("ares.Lib.%s.%s" % (alias, script.replace(".py", ""))), inspect.isclass):
            try:
              if inspect.isclass(obj):
                if hasattr(obj, 'matchMarkDown'):
                  self.markDownMappings.append({'match': obj.matchMarkDown, 'convert': obj.convertMarkDown, 'name': name})
                elif hasattr(obj, 'matchMarkDownBlock'):
                  self.markDownBlockMappings.append({'match': obj.matchMarkDownBlock, 'convert': obj.convertMarkDownBlock, 'name': name, 'endBlock': obj.matchEndBlock})
            except Exception as err:
              logging.warning("%s, error %s" % (script, err))


  def findBlock(self, blockSplitted):
    """ Function used to recognize block component

    :param blockSplitted: The list of line which represents a component
    :return: The Ares Object
    """
    for blockMapping in self.markDownBlockMappings:
      if blockMapping['match'](blockSplitted) is not None:
        return blockMapping

  def findLine(self, line, aresObj):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    :example:
    :return:
    """
    for lineMapping in self.markDownMappings:
      regExpResult = lineMapping['match'](line)
      if regExpResult:
        return lineMapping['convert'](line, regExpResult, aresObj)

  def convert(self, outAresFilePath):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    :example:
    :return:
    """
    outFile = open(outAresFilePath, 'w')
    convertedData = self.convertStr(self.content)
    for line in convertedData:
      outFile.write("%s\n" % line)
    for block in self.content:
      lines = block.split("\n")
    outFile.close()

  def load(self, aresObj, data):
    """
    :category: Markdown Converted to Python
    :rubric: PY
    :type: Markdown
    :dsc:
      Convert the markdown static string to Python object.
    :return: The Python object created
    """
    htmlObjs, j, spareLines = [], 0, []
    if not isinstance(data, list):
      data = data.strip().split("\n\n")
    for i, block in enumerate(data):
      if j > 0:
        j -= 1
        continue

      lines = block.strip().split("\n")
      convertBlock = self.findBlock(lines)
      if convertBlock is None:
        j = 0
        convertLine = self.findLine(lines[0].strip(), aresObj)
        if convertLine is None:
          htmlObjs.append(aresObj.paragraph(block))
        else:
          htmlObjs.append(aresObj.htmlItems[aresObj.content[-1]])
      else:
        blockData = lines
        for j, block in enumerate(data[i+1:]):
          if convertBlock['endBlock'](lines[-1].strip()):
            break

          blockData.append("")
          lines = block.strip().split("\n")
          blockData.extend(lines)

        for v in convertBlock['convert'](blockData, aresObj):
          blockData.append(v)
        htmlObjs.append(aresObj.htmlItems[aresObj.content[-1]])
    return htmlObjs

  def convertStr(self, data, aresObj=None, title=''):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    :example:
    :return:
    """
    outFile, j = ["TITLE='%s'" % title, "def report(aresObj):"], 0
    for i, block in enumerate(data):
      if j > 0:
        j -= 1
        continue

      lines = block.strip().split("\n")
      convertBlock = self.findBlock(lines)
      if convertBlock is None:
        j = 0
        convertLine = self.findLine(lines[0], aresObj)
        if convertLine is None:
          outFile.append("  aresObj.paragraph(%s)" % (json.dumps(block)))
          if aresObj is not None:
            aresObj.paragraph(block)
        else:
          for v in convertLine:
            outFile.append("  %s" % v)
      else:
        blockData = lines
        for j, block in enumerate(data[i+1:]):
          if convertBlock['endBlock'](lines[-1].strip()):
            break

          blockData.append("")
          lines = block.strip().split("\n")
          blockData.extend(lines)

        complexComp = convertBlock['convert'](blockData, aresObj)
        for v in complexComp:
          blockData.append(v)
        outFile.append("  %s" % "".join(complexComp))
    return outFile

  @classmethod
  def loadsDsc(cls, moduleName, lang='eng'):
    """
    :category: Markdown Parser
    :rubric: PY
    :type: Loader
    :dsc:
      Load the documentation from the DSC variable of a given module.
    :return: The AReS docString object
    """
    if hasattr(moduleName, 'DSC'):
      docStrObj = cls.loads(moduleName.DSC.get(lang, moduleName.DSC['eng']))
    else:
      docStrObj = cls.loads("")
    docStrObj.source = "/%s.py" % moduleName.__name__.replace(".", "/")
    return docStrObj

  @staticmethod
  def loads(docStr, section=None):
    """
    :category: Markdown Parser
    :rubric: PY
    :type: Loader
    :dsc:
      Load the documentation from a bespoke String variable.
      The string variable should have the expected labels in order to be correctly loaded and then parsed as a Markdown string
    :return: The ARes docString object
    """
    if docStr is None:
      return DocString()

    docStr =  docStr.replace("https:", "https\\:").replace("http:", "http\\:")
    data, category = {}, None
    for com in docStr.split("\n"):
      line = com.strip()
      if line.startswith(":"):
        match = re.search(":([a-zA-Z 0-9]*):(.*)", line)
        if match is not None:
          results = match.groups()
          category = results[0]
          if not category in data:
            data[category] = []
          docLine = results[1].strip()
      else:
        docLine = line
      if category is not None:
        data[category].append(docLine)
    if section is not None:
      return DocString(data).getAttr(section)

    return DocString(data)

