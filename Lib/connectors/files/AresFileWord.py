#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.connectors.files import AresFile
from ares.Lib.AresImports import requires

# Will automatically add the external library to be able to use this module
ares_docx = requires("docx", reason='Missing Package', install='python-docx', sourceScript=__file__)


class FileWord(AresFile.AresFile):
  """
  :category: Connector
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
  __fileExt = ['.doc', '.docx']
  label = "Interface to deal with Word documents"

  def _read(self, **kwargs):
    doc = open(self.filePath, 'rb')
    document = ares_docx.Document(doc)
    doc.close()
    return [para.text for para in document.paragraphs]


if __name__ == '__main__':
  pdfObj = FileWord(r'D:\ficheProjet.docx')
  print( pdfObj.read() )
