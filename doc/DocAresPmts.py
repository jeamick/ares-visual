#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
    'eng': '''

:dsc:
Especially because Python is not types and it more base on the concept of "duck typing" it is very important to keep the same name for the same concept. A cat should always be called a cat !
This discipline will make the code easier to read and it will also allow you to enjoy more this spirit as you will see that any kind of cats will then be automatically allowed without changing the code. 

The naming convention of those variables is camel case (in order to align with Javascript convention).
We only use the snake case convention for variables only interacting and used by pure Python modules.
''',

}


PARAMETERS = {
    'htmlObjs': {'eng': 'A list of Ares objects'},
    'vals': {'eng': 'The component value - Type will differ by component, please check the mocks data'},
    'recordSet': {'eng': 'The component input dictionary - The content will differ by component, please check the mocks data'},
    'author': {'eng': 'Set a reference to the author name'},
    'location': {'eng': 'The CSS position of the item'},
    'cssCls': {'eng': 'The CSS Classname (it can be Python or external class name coming from a Web package)'},
    'cssModuleName': {"eng": 'The CSS Python module used to override the existing configurations'},
    'colorRange': {'eng': ''},

    'rubric': {'eng': 'Filter on the rubric in the documentation'},
    'zindex': {'eng': 'The CSS layer dimension of the AReS HTML component'},
    'withUnit': {'eng': 'The CSS unit used for the width of an AReS HTML component, usual it is either px or %'},
    'changeMonth': {"eng": "Boolean Flag on the date object in order to enable the user to click to see the previous or next month"},
    'changeYear': {"eng": "Boolean Flag on the date object in order to enable the user to click to see the previous or next year"},
    'showOtherMonths': {"eng": "Boolean Flag on the date object to see full weeks even if some days are in between months"},
    'asyncCall': {"eng": "Boolean Flag to specify if the javascript event should be (or not) asynchroned. Set to true by default for the AJAX calls"},
    'radioVisible': {"eng": "Boolean flag to specify if the radio style should be wisible in the AReS HTML radio component"},
    'resizable': {'eng': 'Boolean flag available in some AReS HTML components to set the resizable property from the user'},
    'delimiter': {'eng': 'The line delimiter, the default one is the tab'},
    'showGrid': {'eng': 'Boolean flag to display the borders of a component'},
    'calculator': {'eng': 'Boolean flag to add a new icon in charge of displaying a calculator with some basic maths features (sum, average...)'},
    'excel': {'eng': 'Boolean flag to add a new icon in charge of exporting to Excel the data of the Ares HTML component'},

    'top': {'eng': 'Filter on the Nth first items'},
    'online': {'eng': 'Boolean flag to mention if the framework is using an internet connection'},
    'position': {'eng': 'The CSS position of the content of an Ares HTML component. This can be left, center or right'},
    'noGlutters': {'eng': 'Boolean flag to use the bootstrap no glutters class or not'},
    'zoom': {'eng': 'Boolean flag to enable to zoom feature on the AReS HTML component'},
    'orders': {'eng': ''},
    'spellcheck': {'eng': 'A boolean to set or not the automatic HTML spell check, https://www.w3schools.com/Tags/att_global_spellcheck.asp'},
    'colName': {'eng': 'A column name from a table or dataframe as a string'},
    'colNames': {'eng': 'A list of column names'},
    'pyMod': {'eng': 'A Python module return from a dynamic import'},
    'clsName': {'eng': 'A String defining a class name'},
    'clsNames': {'eng': 'A List of clsName'},
    'duration': {'eng': 'Set the duration of an event in milliseconds'},
    'delay': {'eng': 'Add A delay before performing a Javascript event, time expected in milliseconds'},
    'colorCode': {'eng': 'A valid color code. Can be a color name, a hexadecimal code or a rgb one'},
    'ajaxParam': {'eng': "A dictionary with the input parameters of a Ajax call in Ares. Namely { 'url': 'script.py', 'success': 'successFileName', 'jsData': [aresObjs], 'httpCodes': ['cob'] } "},
    'params': {'eng': 'A Python dictionary'},
    'paramsCss': {'eng': 'A Python dictionary with at least two keys: attr and value '},
    'env': {'eng': 'The code for the environment in the connector: LIVE, '},
    'htmlCodeSrc': {'eng': '''
            The htmlCode code for the source component. This code will be the one used on the Javascript side to reference the object.
            If not defined a random one will be used and it will be impossible to create any interaction with it.
            HtmlCodes can also be store in the database to be able to reference their meaning to be used in different reports or environments, like httpCodes
            '''},
    'timeInMilliSeconds': {'eng': 'Integer representing a time in milliseconds'},
    'urlName': {'eng': 'Optional. Specifies the target attribute or the name of the window. The following values are supported'},
    'intervalId': {'eng': 'Unique added returned from the function jsInterval int the aresObj'},
    'source': {'eng': 'The connector source code'},
    'toPandas': {'eng': 'To get a AReS Dataframe back from a function call'},
    'exactMath': {'eng': ''},
    'jsFnc': {'eng': 'Any AReS Python functions starting by js or a string which represent a javascript fragment'},
    'jsFncs': {'eng': 'A Javascript function or a list of Javascript functions'},
    'caseSensitive': {'eng': ''},
    'jsData': {'eng': 'The javascript data object used in each event and service calls. Typically this is a javascript dictionary'},
    'jsDataKey': {'eng': 'The key in the jsData object where the data relevant to the javascript function are stored.'},
    'uniqKey': {'eng': 'The list of key in the dictionary which are used to get unique records in a table for example'},
    'xlDate': {'eng': 'A excel date'},
    'htmlId': {'eng': 'The htmlId of the table component. Optional and it will default to itself'},
    'fromDt': {'eng': 'The current date on which the logic should start in a AReS format YYYY-MM-DD'},
    'weekdays': {'eng': 'Boolean flag to specify if the weekend should be excluded'},
    'allSelected': {'eng': 'Allow the fact that all items are selected'},
    'text': {'eng': 'The text to be displayed in the component - A String'},
    'level': {'eng': 'Pre formatted levels used in the title HTML object'},
    'url': {'eng': 'The link if clicked (This has to be a registered url in the framework)'},
    'size': {'eng': 'The Font Size in pixel of the text, please refer to the CSS module to get the default value'},
    'number': {'eng': 'The number used in the HTML component'},
    'iconName': {'eng': ''},
    'count': {'eng': ''},
    'maxSelections': {'eng': ''},
    'title': {'eng': 'The text used as a title in the HTML component'},
    'tableStyle': {'eng': 'The datatable style: order-column, display, cell-border, hover, stripe, table table-striped table-bordered'},
    'valOn': {'eng': 'The on value in the switch component'},
    'valOff': {'eng': 'The off value in the switch component'},
    'video': {'eng': 'The name of the video in the static/video folder'},
    'sizeIcon': {'eng': ''},
    'name': {'eng': 'The Ares HTML component internal name to be used in the Javascript side to find a group of components'},
    'label': {'eng': 'The static label to be display on the Ares Html component'},
    'value': {'eng': 'The value to be displayed when the Ares Html component is created'},
    'tooltip': {'eng': 'Defined the text to be displayed when the mouse is on the Ares Html component'},
    'searchable': {'eng': 'Boolean to set the searchable aspect of the Ares HTML component'},
    'selectable': {'eng': 'Boolean to set the unique selection of the Ares HTML component'},
    'multiselectable': {'eng': 'Boolean to set the multi selection of the Ares HTML component'},
    'placeholder': {'eng': 'The default text to be displayed in an empty input box'},
    'notifType': {'eng': 'The bootstrap type of notification can be (SUCCESS, INFO, WARNING, DANGER)'},
    'width': {'eng': 'The width of the Html component in the page as an Integer'},
    'widthUnit': {'eng': 'The unit of the width (can be in px or in %)'},
    'height': {'eng': 'The height of the Html component in the page as a Integer'},
    'heightUnit': {'eng': 'The unit of the height (can be in px or in %)'},
    'color': {'eng': 'The Color used for the text in the component, please refer to the CSS module to get the default value'},
    'backgroundColor': {'eng': 'Set the Background color of this component, please refer to the CSS module to get the default value'},
    'icon': {'eng': 'The awesome Icon reference from the website https://fontawesome.com/'},
    'align': {'eng': 'Align the content of a component using the usual CSS property text-align, possible value: center, left, or right'},
    'picture': {'eng': 'The path to a picture - no default value'},
    'marginTop': {'eng': 'Set the top margin of a component in pixel - no default value'},
    'htmlCode': {'eng': 'Fix the component id in a report, used to be able to store report filters and selections'},
    'internalLink': {'eng': 'The internal link url for example /reports/documentation to go to the documentation'},
    'newPage': {'eng': 'Open the page on a new page in the browser'},
    'decoration': {'eng': 'Remove the automatic underlying on link'},
    'isRow': {'eng': 'Special flag to mention if the values are coming from a row in a table'},
    'httpCodes': {'eng': 'The list of http codes passed to a service during a external call (Ajax or REsT)'},
    'htmlCodes': {'eng': 'Deprecated and replaced by httpCodes'},
    'dataSrc': {'eng': 'The REST service to call to get the data {"type": "url", "url": "url", "htmlCodes": ["the list of the different codes"], "on_init": False, "time_out": "Update time in seconds"}'},
    'checked': {'eng': ''},
    'bool': {'eng': 'The boolean value to set a True / False value'},
    'isPyData': {'eng': 'The flag to mention if the value is coming from Python or Javascript'},
    'disable': {'eng': 'Flag to disable a component like a button'},
    'border': {'eng': 'Boolean flag to set a default border to a component'},
    'edit': {'eng': 'Boolean flag to change a component to be editable'},
    'deleteCol': {'eng': 'Display the standard column to delete rows. Can be a boolean or a Url Data Source'},
    'addCol': {'eng': 'Display the standard column to add rows. Can be a boolean or a Url Data Source'},
    'send_to': {'eng': 'The list of email addresses separated by a ; '},
    'digits': {'eng': 'The number of digits displayed for a number'},
    'language': {'eng': 'The name of the programming language, default Python'},
    'lang': {'eng': 'The name of the language, default English (Other languages might be missing or not updated)'},
    'chartDesc': {'eng': ''},
    'chartType': {'eng': ''},
    'fileFamily': {'eng': 'Variable in chart of defining the class to read the file. By default it is none and it is based on the filename'},
    'chartFamily': {'eng': "The code of the charting library, could be none or something from the list ['ChartJs', 'Plotly', 'C3', 'D3', 'Vis', 'NVD3'] "},
    'xAxis': {'eng': 'The name of the x axis from a data chart object'},
    'subChart': {'eng': 'Boolean flag used in some charting framework to add an extra small chart below to zoom or filter (https://c3js.org/samples/options_subchart.html)'},
    'filename': {'eng': 'The filename to be used. Just the filename and not the fullpath. By default the framework will try to get the file from the internal outputs folder in the selected report'},
    'skiprows': {'eng': 'The number of rows to be ignored during a file loading'},
    'seriesNames': {'eng': 'The list of seriesName to be used from an Ares Dataframe'},
    'context': {'eng': 'A static Python dictionary to be added to an Ajax call'},
    'datatype': {'eng': 'The type of data passed from one language to another (Python to Js). In an Ajax function the default is json'},
    'dataFncs': {'eng': 'The list of javascript functions to be applied to the data to be used by the AReS HTML component'},
    'editable': {'eng': 'Boolean flag to set the component editable. This flag is mainly used with div component and set the HTML attribute contenteditable'},
    'decimal': {'eng': "The character used for the decimal. By default the framework will use the . (This is mainly used when the file is loaded to parse the data and get the right format)"},

    "n": {'eng': 'An number', 'type': 'integer'},
    "fnc": {'eng': 'A python callable object', 'type': 'function'},

    # Parameters more dedicated to the SQL Framework
    'tableName': {'eng': 'A table name from the database', 'type': 'string'},
    'tableNames': {'eng': 'A list of table names from the database', 'type': 'list'},
    'columnName': {'eng': 'A column name from a table in the database', 'type': 'string'},
    'withCheck': {'eng': 'Flag to activate or not a control', 'type': 'boolean'},
    'stmts': {'eng': 'The where clause SQL statement', 'type': 'string'},
    'records': {'eng': 'A list of dictionaries', 'type': 'list'},
    'commit': {'eng': 'Commit the event', 'type': 'boolean'},
    'colUserName': {'eng': 'The column name for the user_name in the database. This will then be updated automatically by the framework during a insert', 'type': 'string'},
    'globalFilter': {
        'eng': '''
            Variable used to mention if the parameter should be watching events on a data source
            Can be either a boolean for a dictionary with the data on which the filter should be applied and also the column on which the filter should be applied.
            For some containers like charts or tables the boolean can be used as it will by default refer to the one attached to the component.
            
            ```python 
                
            ```
            
            This can also be done later one in the code by use the function filter() 
            '''
    }

  }


def docEnum(aresObj, outStream, lang='eng'):
  """
  :category: Datatable
  :rubric: PY:
  :type: Configuration
  """
  header, data = ['Category', 'Type', 'Description'], []
  for alias, dsc in PARAMETERS.items():
    data.append( [alias, dsc.get('type', 'String'), dsc.get(lang, dsc.get('eng', ''))] )
  outStream.table( header, data, pmts={"searching": True} )
