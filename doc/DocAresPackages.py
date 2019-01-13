#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
  "eng": '''
:category: Packages
:rubric: PY
:type: Documentation
:dsc:
Display the list of Python packages used in the framework. Those packages are wrapped within the aresObj in order to have a sinple interface for each of them.

If some packages are missing or not correctly wrapper please do not hesitate to liaise with your IT Team.
All the Python packages automatically loaded to the framework are in the file requirements.txt.

#### How to add a Python Package locally

It is possible to add an extra package to the framework but be **careful this will not work on the server**.
Below you can get the details on the different steps required in the integration of a new Python package.

#### How Python are imported in the Framework

Nothing specific in the import, all external packages are loaded by Flask when the server is started. Flask will rely on the file **requirements.txt** in the root of the framework.
In this file all the modules (with their respective version) are defined. They are then loaded from the folder **packages/**. Any new package should be added in both places to be correctly installed.
In order to be compatible with the different versions of Python the folder packages/ should contain all the version defined for the different Python distributions

Then the function requires() is used in each modules in order to not break the framework if the package is not available. This function can also try to install the package from the define source (default is pip on internet) is it is missing in the distribution.
In each modules using any external package the import is wrapped like shown below

```python
ares_pyodbc = requires("pyodbc", reason='Missing Package', install='pyodbc', autoImport=True)

# Any odbc class or function can be used from ares_pyodbc
# This script will fail only when this module is calling a specific function as in case of failure ares_pyodbc is none
```

'''
}


PY_PACKAGES = {
  'pandas': "https://pandas.pydata.org/",
  'numpy': "http://www.numpy.org/",
  'scipy': "https://www.scipy.org/",
  'pywin32': 'https://pypi.org/project/pywin32/',
  'zeep': 'https://python-zeep.readthedocs.io/en/master/'
}

