#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
  'eng': '''
# Documentation Rules

In order to help the internal search engine and also to make easy the framework extension for the community some rules and tags are pre defined.
Type and Rubric sections are a bit specific as they are used to index the search, please have see below the meaning of those mandatory sections  


## Rubric


## Type


'''
}


_CATEGORIES = {
  'AJAX': {'eng': ''},
  'Dataframe': {'eng': ''},
  'AReS System': {'eng': 'All functions requireds only by AReS in order to simplify the use of the platform'},
  'Bespoke User Functions': {'eng': ''},
  'SQL Framework': {"eng": ""}
}

_TYPE = {

}

_RUBRICS = {
  'JS': 'Used only on the Front end side in the browser',
  'PY': 'Used on the server side in the Python layer - Pre report',
  'CSS': 'Used on the Front end side to change the display of the components',
  'System': 'Specific item used by the Framework in different components or processes'
}



def docEnum(aresObj, outStream, lang='eng'):
  """
  :category: Datatable
  :rubric: PY:
  :type: Configuration
  """
  header, data = ['Category', 'Description'], []
  for alias, dsc in _CATEGORIES.items():
    data.append( [alias, dsc.get(lang, dsc.get('eng', ''))] )
  outStream.table( header, data, pmts={"searching": True} )

