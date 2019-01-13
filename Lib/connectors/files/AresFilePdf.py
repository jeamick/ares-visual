#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import logging
from ares.Lib.connectors.files import AresFile



class FilePdf(AresFile.AresFile):
  """
  :category: Ares File
  :rubric: PY
  :type: class
  :label: Connector to read a bespoke PDF file.
  :dsc:
      Connector to read a bespoke PDF file.
      From this connector there is also some features in order to ask the framework to "digest" the files in order to enrich the search engine with metadata.

      At this stage we are more working on the collection of metadata but the search engine will then leverage on all these information

      This module to work need a Python package called PyMuPDF. To install it you can run the command pip install PyMuPDF.
      Once this available to your Python environment this connector will work fine.
      If you want to check the connector please click [here](/api?module=connector&alias=PDF)
  :link PyMuPDF Documentation: https://pymupdf.readthedocs.io/en/latest/tutorial/
  """
  __fileExt = ['.pdf']
  label = "Interface to deal with PDF files"
  _extPackages = [("fitz", 'PyMuPDF')]

  def _read(self, toPandas=False, **kwargs):
    doc = self.pkgs["fitz"].open(self.filePath)
    if kwargs['pageNumber'] >= doc.pageCount:
      logging.debug("Page number %s does not exist, max value %s in file %s" % (kwargs['pageNumber'], doc.pageCount - 1, self.filePath))
      return ''

    return doc[kwargs['pageNumber']].getText()


if __name__ == '__main__':
  pdfObj = FilePdf(filePath=r'C:\Users\HOME\Downloads\easyBus769586.pdf')
  print( pdfObj.read(pageNumber=0) )