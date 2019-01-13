#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


INPUTS = {
  'select': [{'name': 'Python', 'value': 'python', 'category': 'Script', 'selected': True},
             {'name': 'C#', 'value': 'c#', 'category': 'code'}],
  'selectmulti': [{'value': 'Python', 'category': 'Script', 'selected': True}, {'value': 'C#', 'category': 'code'}],
  'dropdown': [{'value': 'code', 'subItems': [{'value': 'France'}, {'value': 'Germany'}]},
               {'value': 'scripting', 'subItems': [{'value': 'Python', 'url': 'google'}, {'value': 'R'}]}],
  'text': 'Text section example',
  'list': [
    {"label": 'Python', 'url': "https://www.python.org/"},
    {"label": 'R', 'url': "https://www.r-project.org/"},
    {"label": 'Javascript', 'url': "https://www.javascript.com/"},
    {"label": 'C#'}],
  'code': "Code section example",
  'preformat': 'Preformatted text example',
  'paragraph': 'Example of Paragraph',
  'blockquote' : '''
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
''',
  'title': 'Example of Default Title',
  'number': 240985,
  'update': 'Last Update:',
  'highlights': 'Text section example',
  'searchr': [],
  'search': '',
  'checkbox': [ {"value": 'Python', 'checked': True}, {"value": 'C#'}],
  'checkbutton': [  ],
  'textArea': 'textArea',
  'progressbar': 60,
  'slider': [10, 70],
  'skillbars': [
    {"label": 'Java', 'value': 24.96, 'url':  "https://www.tiobe.com/tiobe-index/", 'dsc': 'Rating from https://www.tiobe.com/tiobe-index/'},
    {"label": 'C', 'value': 21.32, 'dsc': 'Rating from https://www.tiobe.com/tiobe-index/'},
    {"label": 'C++', 'value': 10.78, 'dsc': 'Rating from https://www.tiobe.com/tiobe-index/'},
    {"label": 'Python', 'value':	9.80, 'dsc': 'Rating from https://www.tiobe.com/tiobe-index/', 'color': 'red'},
    {"label": 'C#', 'value':	8.46, 'dsc': 'Rating from https://www.tiobe.com/tiobe-index/'},
    {"label": 'Visual Basic .NET', 'value':	6.82, 'dsc': 'Rating from https://www.tiobe.com/tiobe-index/'},
    {"label": 'PHP', 'value':	6.70, 'dsc': 'Rating from https://www.tiobe.com/tiobe-index/'},
    {"label": 'JavaScript', 'value':	6.54, 'dsc': 'Rating from https://www.tiobe.com/tiobe-index/'},
    {"label": 'Ruby', 'value':	4.58, 'dsc': 'Rating from https://www.tiobe.com/tiobe-index/'},
  ],
  'externallink': {'url': 'https://www.python.org/', 'text': 'Python', 'icon': 'fab fa-python', 'color': 'green'},
  'link': {'url': '#', 'text': 'Python', 'icon': 'fab fa-python', 'color': 'green'},
  'img': 'risklab_logo.png',
  'animatedimg': {'title': 'Title', 'text': "Content", 'image': "saturn-dashboard.PNG", 'url': "http://www.google.fr"},
  'input': '',
  'pwd': '',
  'inputInt': '',
  'date': 'Date',
  'hr': 1,
  'newline': 1,
  'stars': 4,
  'help': 'RiskLab',
  'media': '',
  'button': 'Example',
  'buttonicon': 'Example',
  'delimiter': 1,
  'radio': [ {"value": 'Python', 'checked': True}, {"value": 'C#'}, {"value": 'R'} ],
  'switch': {'on': 'Python', 'off': 'R', 'checked': 'Python', 'text': 'Scripting language'},
  'countdown': '2018-09-01',
  'tick': True,
  'table': [{'A': 1, 'B': 2}],
  'inputRange': {'label': 'Label', 'number': 56, 'min': 0, 'max': 100, 'step': 1, 'placeholder': 'Put a text here'}
}