#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DSC = {
  'eng': '''
    
    '''
}

_TYPES = {
  'Framework extension': {'eng': '''
    Functions dedicated to add new modules to the existing framework.
    Those functions should be used in order to prototype the add of new CSS or Javascript pieces but once validated they should be added to the framework in a proper way.
    Those are bespoke entry points to allow to change the framework easily to perform very specific actions.
    '''},

  'outputs': {'eng': '''
    Functions dedicated to output data. Output might be logs but also the full reports in a specific format
    '''},

  'constructor': {"eng": ''}
}