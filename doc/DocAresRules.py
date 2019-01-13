#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DSC = {
  'eng': '''
:category: Framework rules
:rubric: PY
:type: Documentation
:dsc:
Here will be set the good citizen rules. Most of the rules could be already derived from the official rules available as part of the famous PEP (Python enhancement  Proposals).
The only one not followed, only for cosmetic reasons, is the number of spaces for the indentation. Here we do use 2 indents instead of the 4 officially defined.
Please have a look at the [rules](https://www.python.org/dev/peps/) if you have any doubt about a style or even a syntax

## Data Extraction

+++Get the correct amount of data from the source system

Data is the heart of your dashboard so it deserves to be considered careully. Extracting the right level of data will simplify a lot the logic.
It will help us also to get the right metric regarding your report and to ensure that you will be informed is there is any change / improvement in this area.
Having too many data will make this analysis more difficult.

---Avoid the extraction of more data (just in case)

This is a very bad practise as this will slow down your program. Ensuring the right level of information will reduce toe clean up and processing of your data.
THe best would be to push the maximum of your logic (aggregation, count, sum...) to your source system as there is always more efficient ways to do it closer to the source.
Anyway if some pre precessing is needed ensure it is done on the right set of data. At the end to get a fluid display you need to send a minimum of data to your borwser

## Coding Standards in 10 rules

The below points are not really there to teach Python but more to ensure we are following the same coding convention within the framework.
If you need to get more details about the Python language do not hesitate to follow some online trainings or to ask us questions. 
The main pillars of Python are all summarised in the Zen of Python (import this). Do not hesitate to have a look at those simple but very often useful and relevant sentences. 
__

>>>Quote:Tim Peters
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
<<<

+++Use 2 spaces instead of the 4 standard ones

In the whole framework this rule has been used please make sure you are following the same standards. Even if this is against the PEP8, for a pure cosmetic aspect this has been decided.

+++Variables, functions and classes naming convention

Within this framework we are using the Javascript standard - **camelcase88 to write function names and variable names. Again on this point the Python standard are not followed.
Please make sure you follow this rules to facilitate the reading of your script.
The only place where the Python naming convention is followed is in the naming of information related to SQL. Table names, columns are in snake case

+++Rely on the Ares.py Interface

Do not hesitate to let us know if there is anything you believe missing as part of this interface.
It is important to go thought this as this interface is not supposed to change during the releases and any change will be flagged in the release documentation page.
Any other internal change might happen without any further communication

+++Document your work

AReS comes with its own embedded documentation generation. Be sure to comment thoroughly your report as something that might be obvious to you
will not be to others. Since this is a collaborative platform it would be a shame that your reports could only be understandable by you.

+++Multi-Threading

The AReS Framework does not support multi-threading as it is embedded in a Flask application and the two don't work well together.
If you try this in your report it would break the application so we added a security to prevent such cases.

+++Check and Use AresUtilities

Some basic operations are embedded in the AresUtilities module. Be sure to check the module before re-implementing something. 
To access anything exposed in AresUtilities you only need to use aresObj.function_name where function_name is the function exposed in AresUtilities.

+++Use the Feedback interface

The Feedback interface is the place where all the AReS users ask their question. Remember, before you ask a question be sure to look for topics similar to yours as someone might 
have asked about it before you did.

+++Keep the secret

Security and confidentiality is very important. Do not commit any personal information such as passwords or anything like that in your reports.
If you do and this is spotted the report will be deleted without notice and a security incident will be reported. In any case you will be asked to change those passwords immediately.
So be carreful with your commit (always check the differences) and do not hesitate to ask if you have any doubts.

+++Javascript hardcoded strings

Although it is possible and it is allowed to embed your own javascript in reports, you should first check with us whether we do not provide the feature you're trying to implement.
This will ensure we have a consistent framework within the reports of the application.
If it is not there and we find it is actually something that needs to be - we have no problem adding it to the library !

#### Useful links

[PEP 8  the - Style Guide for Python Code](https://pep8.org/)
[Learn Python](https://www.w3schools.com/python/default.asp)
'''}



def docEnum(aresObj, outStream, lang='eng'):
  pass