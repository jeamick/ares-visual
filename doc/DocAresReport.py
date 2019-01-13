#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DSC = {
  'eng': '''

:dsc:

## Report Structure

A valid Report should be defined in the folder user_reports of your local Ares version. This folder will group all the scripts available in the community.
Those committed scripts are public and as a consequence should not contain any **credentials**. Even if we are reviewing scripts from time to time please make sure that no sensitive information will be committed !

#### How to start a new project

The best to start a new project is to get inspired from an existing report. So first check within your team if some reports have been created.
If it is not the case, first create a subfolder for your team or activity and then create your first script

```python
# The below line will group the data transformation and the front end
def report(aresObj): pass
```

The best would be to start to write the data tranformation in the user_script section. This will allow the focus on the data and the different checks related to the algorithm.
Once this is done and validated, a simple copy paste of the code within the report function will work. No need to import the aresObj or even to create the it.
Also it is more convenient to work on the data transformation within the Web interface as it can be fully implemented in your locally IDE (which will bring a lot of help in the debugging of your code)

```python
# The below represent the best structure of a report in order to debug is easily
def report(aresObj): 
  # Data transformation
  # -------------------------
  # Front end Display
```

#### Important Report variables

Some variables specific to this environment will help you.
__
**TITLE** 
This is a simple and short text used to give a name of your report in the side bar. Thanks to this name the report will be visibles and other people will be able to use it.
If this is not defined, the name of the script will be displayed in the side bar

```python
TITLE = 'Home Page'
```

__
**CONNECTORS** 
Not yet available
__
**DSC**
This represent the short description with the keywords used to find the project. Those sentences will be the ones used by the search engine.
Please make sure this is updated and accurate.

The documentation of your report should have the below structure (as we are planing to have someting multi languages) and it can be written using the Markdown tags.
Do not hesitate to have a look [here](api?enum=Markdown) if you need further details

```python
DSC = {
  'eng': 'This documentation is just an example'
}
```

__
**PARAMS**
This report variable is used to add some extra parameters on top of the reports. Those parameters are mandatories and will be then added to the URL to fully be able to construct the report.
Those parameters are not just variables used to change some part of the reports, they are very specific and they are driven all the report.
__
You can get more details on the parameters bar here [Parameters Bar](api?module=htmlObj&callFnc=sidebar)
Not all the components are designed to be in the parameters bar, please go to the documentation of the component to get more details.

```python
PARAMS = [
  {'htmlComponent': 'input', 'htmlCode': 'quizz_id', 'width': 200,  'widthUnit': 'px', 'label': '<b>Quizz ID</b>', 'inCookies': False},
  {'htmlComponent': 'selectmulti', 'htmlCode': 'select', 'recordSet': [
    {'name': 'Python', 'value': 'python', 'category': 'Script', 'selected': True},
    {'name': 'C#', 'value': 'c#', 'category': 'code'}]},
]
```

'''
}

