#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import time
import logging
import inspect
import importlib
import os

from ares.Lib.AresImports import requires


DSC = {
  'eng': '''
:dsc:
## File reader

This section will detail how to handle files and also how to force a particular file loading is the extension is not correct. As defined above some file extension are pre defined to be loaded by a specific class. The default one will just open the file and return it.
Most of the files will be opened using the Pandas interface. Please have a look at the [Pandas wrapper](/api?module=import&enum=package-pandas) for more details.

```python
aresObj.file(filename="")
# The path will be set by default in the output folder of the environment

aresObj.file(filename="", path="")
# In this example the path will be set to a special directly.
# This will only work locally and cannot be used in server mode as the file locally might be different

aresObj.file(filename="", path="", fileFamily=".doc")
# In this example the module used to read the file is overriden. The framework will not rely on the extension anymore 
```

'''
}

# Factory for all the files
factory = None

def loadFactory(forceReload=False):
  """
  :category: Files
  :type: Factory
  :rubric: PY
  :dsc:
    This function will store all the different files parsers available in the Framework. The default file format used
    for the data is a Pandas [dataframe](https://fr.wikipedia.org/wiki/Pandas).
    In local runs this factory is reloaded after any change of script. On a server mode a variable forceReload will be
    used to refresh this factory.
  :return: The Python factory
  """
  global factory

  if forceReload or factory is None:
    tmp = {}
    for script in os.listdir(os.path.dirname(__file__)):
      try:
        if script.startswith("AresFile") and script.endswith('py') and script != "AresFile.py":
          for name, obj in inspect.getmembers(importlib.import_module("ares.Lib.connectors.files.%s" % script.replace(".py", "")), inspect.isclass):
            exts = getattr(obj, '_%s__fileExt' % name, None)
            if exts is not None:
              for ext in exts:
                tmp[ext] = obj
      except Exception as err:
        logging.warning("%s, error %s" % (script, err))
    factory = tmp
  return factory


class AresDataSource(object):
  """
  :category: Default
  :rubric: PY
  :type: Data Source
  :dsc:

  :return: A Python Ares Dataframe like object
  """

  __fileExt = None

  def __init__(self, dataSrc, htmlCode, aresObj=None):
    self.aresObj, self.htmlCode, self.headers = aresObj, htmlCode, []
    self.aresObj.jsSources[htmlCode] = {"data": self, 'containers': []}
    self.jsData, self.columns, self.dataSrc = "null", dataSrc.get('columns', []), dataSrc

  def sort_values(self, by, inplace): pass

  def attach(self, htmlObj):
    """
    :category: Dataframe
    :rubric: JS
    :type: Front End
    :dsc:
      Attach the Dataframe to a HTML Object. This function is normally used in the different components in order
      to guarantee the link of the data. This will also ensure that the same data set will be store only once in the page
    """
    self.aresObj.jsSources[self.htmlCode]['containers'].append(htmlObj)

  def tableHeader(self, forceHeader=None, headerOptions=None):
    if self.columns is None:
      return [{"data": "empty", 'title': "Empty table"}]

    return self.columns

  def jsEvent(self, debug=None):
    """
    :category: Dataframe
    :rubric: JS
    :type:
    :dsc:

    :return: The Javascript string corresponding to the refresh of the different components
    """
    jsGenerateFncs = []
    for obj in self.aresObj.jsSources[self.htmlCode]['containers']:
      jsGenerateFncs.append(obj.jsGenerate())
    return self.aresObj.jsPost(self.dataSrc['url'], jsFnc=["%s = data" % self.htmlCode] + jsGenerateFncs, debug=debug)

  def html(self):
    jsGenerateFncs = []
    for obj in self.aresObj.jsSources[self.htmlCode]['containers']:
      jsGenerateFncs.append(obj.jsGenerate())
    if self.dataSrc.get('on_init', False):
      self.aresObj.jsOnLoadFnc.add(self.aresObj.jsPost(self.dataSrc['url'], jsFnc=["%s = data" % self.htmlCode] + jsGenerateFncs))
    return ''


class AresFile(object):
  """
  :category: Default
  :rubric: PY
  :type: File
  :dsc:
    Unique interface for files in AReS. A factory will read the file according to the extension but
  """
  __fileExt, _extPackages = None, None
  label = ''

  def __init__(self, data=None, filePath=None, htmlCode=None, aresObj=None):
    self.pkgs = {}
    if self._extPackages is not None:
      for name, package in self._extPackages:
        self.pkgs[name] = requires(name, reason='Missing Package', install=package, autoImport=True, sourceScript=__file__)
    self.aresObj, self.filePath, self.htmlCode, self._ares_data = aresObj, filePath, htmlCode, data
    _, self.fileExtension = os.path.splitext(self.filePath) if filePath is not None else (None, None)
    self.path, self.filename = os.path.split(filePath) if filePath is not None else (None, None)

  @property
  def exists(self):
    return os.path.exists(self.filePath)

  @property
  def timestamp(self):
    if self.exists:
      return time.strftime("%Y%m%d_%H%M%S", time.gmtime())

  def get(self, fileFamily=None, delimiter=None, **kwargs):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    :return:
    """
    if delimiter == -1:
      return self

    facts = loadFactory()
    if self._ares_data is not None:
      # Force the use of Pandas in this case
      return facts[".csv"](data=self._ares_data, filePath=self.filePath, aresObj=self.aresObj, htmlCode=self.htmlCode, **kwargs)

    if fileFamily is not None:
      return facts[fileFamily](data=self._ares_data, filePath=self.filePath, aresObj=self.aresObj, htmlCode=self.htmlCode, **kwargs)

    if self.fileExtension.lower() in facts:
      return facts[self.fileExtension](data=self._ares_data, filePath=self.filePath, aresObj=self.aresObj, htmlCode=self.htmlCode, **kwargs)

    return self

  def _read(self, toPandas=False, **kwargs):
    """

    """
    return open(self.filePath)

  def read(self, toPandas=False, **kwargs):
    """

    """
    self._ares_data = self._read(toPandas, **kwargs)
    return self._ares_data

  def setFolder(self):
    """

    """
    if not os.path.exists(self.path):
      os.makedirs(self.path)

  def write(self, data, **kwargs):
    """
    :category:
    :rubric:
    :type:
    :dsc:

    :return:
    """
    pass

  def writeTo(self, fileFamily, filePath=None):
    """

    """
    facts = loadFactory()
    if fileFamily.lower() in facts:
      if filePath is None:
        filePath = self.filePath.replace( self.fileExtension, fileFamily)
      newFile = facts[fileFamily](filePath)

  def html(self):
    print(' Not yet implement for bespoke files')
    return ""


def docEnum(aresObj, outStream, lang='eng'):
  """
  """
  for ext, aresClass in loadFactory().items():
    outStream.link(
      " **%s** | %s" % (ext, aresClass.label.strip()), "api?module=file&alias=%s" % ext, cssPmts={"margin": "5px"})



if __name__ == '__main__':
  file = AresFile(r'D:\youpi.json').get()
  #value = {"grerg": "vergerg", "rvr": 2}
  #file.write(value)
  data = file.read()
  #file = AresFile(r'D:\testimports\testScript.py').get()
  #print file.read().DSC

  file = AresFile(r'D:\BitBucket\Youpi-Ares\user_reports\EFEE\doc\index.amd').get()
  data = file.read()
  file.write(data)
  #data = AresJsData.JsDataFrame(None, None, None, "\t", None, None, None, None, None, None, '.')
  #file.write(data)