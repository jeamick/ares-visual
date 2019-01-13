#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DSC = {
  'eng': '''
Generic page to store all the major and minor framework changes. This page will help on getting a view on the different upgrade and new components in the framework.
Please do not hesitate to use also the Feedback / Ideas link to share your comments and help us improve this.
'''
}


RELEASES = {
  "2018-12-17": {'data': [
    'Table - Add the use of _index to retrieve the df.index.get_values() data',
    'DataFrame - correct metadata to remove the error message',
    'Ares Package - Move the Apps to a dedicated app folder',
    'Ares - Add variable htmlRefs to control the unicity of the HTML Codes in a report',
    'Table - Remove folder table in Html',
    'Table - Add footer',
    'Table - Clean up Javascript and CSS Extensions',
    'Chart - Add the variable jsType for defining output common javascript processes',
    'Chart - Update of Plotly to allow the parcats chart type',
    'Chart - Allow the use of _index in the xAxis to refer to the dataframe index (this will be the default)',
    'Chart - Vis upgrade',
    'Chart - C3 upgrade and revamping',
    'Script - Example ChartJs',
    'Script - Example Billboard',
    'Script - Example C3',
    'Script - Example Vis',
    'Merge - Report and Script section to the default user folder',
    'Configuration - Add the default user repository to the config.py file if Flask',
    'Scripting - New function mapPackage to allow the external packages (css and js) upgrade test',
    'Scripting - Simplify the toHtml() function',
    'Scripting - C3, Vis, Plotly Examples',
    'Ajax - Test Ajax set up from the scripting interface',
    'Ajax - Function serverFile to write service data to a local cached file in server folder',
    'Html - Revamp the Notification. Add height, bespoke background colors...'
  ]},
  "2018-11-26": {'data': [
    "Documentation - Add links to the Cheatsheets of the different important components",
    "Documentation - Improve Documentation for Javascript functions, Charts and Tables",
    "Error handling - Improve the way error notifications in connectors are displayed in the interface",
    "Charts - Improve the consistency between the charting libraries (ChartJs, C3, Plotly and NVD3",
    "Charts - Guarantee the standard Charting Library to be ChartJs and get a attribute translation with the other libraries",
    "Charts - Merge function onDocumentReady and jsGenerate() to simplify the Javascript",
    "Charts - Remove the specific entries for chart like plotC3, plotNVD3, plotly....",
    "Charts - Review of the configs part dedicated to the chart to get something only based on static configurations",
    "Charts - Review of the Example Dashboard to be generic accross families",
    "Charts - Add entry point addConfig(configCls, chartFam) to add new configurations on the fly - ChartJs only",
    "Databases - Add MongoDb and Noe4J database wrappers",
    "Pivot - Implement the Pivot table from PivotTable.js",
    "Pivot - Use standard functions",
    "Pivot - Add external Aggregator hook to be extended by users",
    "Data - Improve the Javascript framework to be more modular and accept the profiling in the browser",
    "Data - new AReS function dataSrc() to retrieve data from a service on demand",
    "Ajax - Add debug mode to the usual function jsPost and jsGet to get details in the browser",
    "Style - New Ares function addStyleSheet() to create a CSS like stylesheet for a report",
    "Style - Create a Green colors stylesheet",
    "Style - Add childKinds properties to CSS Framework to handle style with nth-child(even)",
    "Html - HtmlCode naming convention checks",
    "Tables - Simplify the table styles",
    "Tables - Create Js function to allow a dynamic way to buckets rows and compute total",
    "Tables - Merge function onDocumentReady and jsGenerate() to simplify the Javascript",
    "Tables - Remove the function jsLoad() and replace by a generic jsGenerate() function",
    "Tables - Add System options like ageing and quality values to the records",
    "Tables - Improve the Python table interface to simplify the usual operation (styling and formatting)",
    "Select / MultiSelect - Add possibility to set an Icon and to retrieve it in an js event",
    "Select / MultiSelect - Enable the globalfilter if use of a dataframe",

  ], 'backward': (0, "Major changes in the charts and table definition"), 'major': (True, "Most of the modules are impacted by this release")},

  "2018-11-03": {'data': [
    "Improve the Parameter bar Display",
    "Add the Markup function to the function aresOb.text()",
    "Create new source entry aresOb.dataSrc(...) to get data from Ajax call",
    "New valid input type for qresObj.list(). Dictionary can be used in the same way than in the aresOjb.selct()"
  ], 'backward': (1, ""), 'major': (False, "")},

  "2018-10-29": {'data': [
    "New function setSeriesColor() to change the chart colors for all the javascript charting libraries",
    "Integration of the globalFilter in all the charting libraries (C3, NVD3, ChartJs...)",
    "New entry Quick Share in the Report section, to share 'static' reports with external users for 5 days",
    "New chart() interface in the aresObj to create a chart without having to build the dc() object",
    "Improve format and display of the release section with flags",
    "Improve display and markdown of the blockquote object",
    "Change in the user setting to register to receive the emails",
    "Change the tick object to receive flag in input (True, 0, False)"
  ], 'backward': (0, 'Changes in the tick and light interface'),
     'major': (True, 'Lot of modules impacted by the new features')},

  "2018-10-22": {"data": [
    "Implementation of the tutorial section",
    "Create the main templates for the Excel to Pandas workshop",
    "Fix the HTML export and use the correct name for the D3 javascript module on CDNjs",
    "Some progresses on the Excel export of some components",
    "Creation of two branch Master and Dev to simplify the releases",
    "Creation of new connectors"
  ], 'backward': False, 'major': True},

  "2018-10-21": {"data": [
    "Add the globalFilter parameter in order to easily create link between events and data",
    "Introduce the breadcrumb for documentation",
    "Documentation framework improvement for external packages",
    "Bug fixes on some components (tables, title...)",
    'Facilitate the link between the files and the databases'
  ], 'backward': True, 'major': False},

  "2018-10-15": {"data": [
    "Introduction of the scripting API for data transformation only",
    "Implementation of the Database framework",
    "Introduction of Plotly.js charting library"
  ], 'backward': True, 'major': False},

  "2018-10-08": {"data": [
    "Improvement of the CSS Python framework",
    "Creation of the Python CSS Color module",
    "Creation of a dedicate module for colors in order to create themes (Dark mode)"
  ], 'backward': True, 'major': False},

  "2018-10-01": {"data": [
    "Improve Report documentation",
    "Add the Change Logs page",
    "Improve the connector error message when credential needed"
  ], 'backward': True, 'major': False}
}

BUG_FIXES = {
  "2018-10-29": [
    {"text": "Fix in Vis Family", "author": "Olivier"},
    {"text": "Fix in the admin section to change password", "author": "Olivier"},
  ],
  "2018-10-01": [
    {"text": "Select and MultiSelect issue in the Parameters bar", "author": "Olivier"}
  ],
  "2018-09-28": [
    {"text": "Input issue in the Parametes bar", "author": "Olivier"}
  ]
}

OPEN_ISSUES = [
  "Documentation - To be reviewed",
  "Use of SSO in AReS to remove the use of password",
  "Export in Pdf, word and Excel",
  'Add grid to the markdowns',

  "Cheatsheets - Interaction with connectors",
  "Cheatsheets - Javascript",
  "Cheatsheets - Plotly",
  "Cheatsheets - Ajax and WebWorker",

  'Import - Add Proxy configuration for Python and web packages',

  "settings, admin improvement",
  'Integration with Jupyter for the scripting part and the workshop',

  'Database - Improvement of the architecture to get share databases for users across env - Network',
  'Database - Activate the sharing of logs across the network',

  'Factory - Restrict to the report the use of bespoke Aggregator or Chart Types',

  "Charts - Add events and filters in Vis",

  'Js - Include workers and real time features',
  'Js - Add Js MarkDown conversion fncs for the exports',

  'Data - Migrate the underlying recordSets to a list of lists instead of a list of dictionaries',
  'Data - Remove cols not used in tables and charts',

  'Table - Add Buttons',
  'Table - Hierarchy',
  'Table - Container',
  'Table - Add more options to the footer',
  'Table - Default col to rows when String',

  'Apps - Add the market store',
  'Apps - Saturn',
]

REJECTED = [
  'Creation of a scheduler in AReS without server'
]