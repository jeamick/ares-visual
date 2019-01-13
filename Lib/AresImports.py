#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DSC = {
  'eng': '''
:category: Import Manager
:rubric: PY
:type: System
:dsc:
#### The Backbone of AReS

This module is the central point of this framework. Indeed the main concept in this framework is to create simple and light bridges between the different web technologies.
Today AReS will encompass most of the famous Javascript and CSS frameworks in order to get the best of them during the conception of a project.
By integrating this within the Python layer, it will benefit from the Python ecosystem but also the speed of this language to preprocess the data.

#### Python Module to generate the CSS and javascript import according to the users needs

This simple module will generate the list of external module to be imported taking into account the order and the
dependencies. New modules can be added easily in this list and they need to be attached in the component of the html/ framework
by adding the alias to the class variables reqCss and reqJs. Here AReS is using javascript and CSS libraries in order to simplify the javascript generation. This Python framework is not dependant of any other Javascript framework like ReactJs or Angular.
**This design will make sure that the logic is not duplicated accross the languages and it will also reinforce the specificities (and the need) of each layer !**
__
The external modules currently used in this framework are all defined here.
  - [Bootstrap](https://getbootstrap.com)
  - [Font awesome](http://fontawesome.io)
  - [Datatable](https://datatables.net) with some plugings
  - [CrossFilter](http://square.github.io/crossfilter)
  - [PivotTable](https://pivottable.js.org/examples)
  - [Jquery](https://jquery.com)
  - [D3](https://d3js.org)
  - [NVD3](http://nvd3.org)
__
All those external modules will be added to your report header automatically when they are needed. This will help on having
a minimum of imports to speed up the web page run. Also it make easier the tested as it is very simple to link a python component
to its Js or CSS dependency to test the changes (for example an upgrade).
__
This design will also allow to run potentially multiple versions in parallel
__
It is nevertheless possible to load on demand bespoke CSS or Javascript package from a report by using the methods addCss and addJs
in the module Ares.py (please have a look at the [documentation](/api) if you need further details about the Ares (Advanced Reporting Suite) Interface
'''
}


import os
import sys
import json
import importlib

from io import open

from ares.utils import OrderedSet
from ares.doc import DocAresPackages

# To fully disable the automatic pip install request when a package is missing
AUTOLOAD = False
PROXY = None


def requires(name, reason='Missing Package', install=None, package=None, raiseExcept=False, autoImport=False, sourceScript=None, pipAttrs=None):
  """
  :category: AReS System
  :rubric: PY
  :type: system
  :dsc:
    Import the necessary external packages and provide explicit message to find a way to solve this error message.
    This method should also explain why this module is required to make sure this is really expected to get an error.
  """
  if install is None:
    install = name
  try:
    mod = importlib.import_module(name)
    if package is not None:
      return getattr(mod, package)

    return mod

  except Exception as err:
    if str(err).startswith("Missing required dependencies") and (autoImport or AUTOLOAD):
      print("Error with %s in script %s, autoload set to %s" % (name, sourceScript, AUTOLOAD))
      deps = json.loads(str(err).replace("Missing required dependencies ", "").replace("'", '"'))
      import subprocess

      for d in deps:
        exe = subprocess.Popen('python.exe -m pip install --proxy="%s" --upgrade %s' % (PROXY, d))
        exe_out = exe.communicate()
        print(exe_out)
      return requires(name, reason, install, package=package, raiseExcept=raiseExcept, autoImport=False)

    if autoImport or AUTOLOAD:
      print("Error with %s in script %s, autoload set to %s" % (name, sourceScript, AUTOLOAD))
      import subprocess

      if pipAttrs is None:
        pipAttrs = []

      # We should use subProcesses instead of the pip module as this is not maintained
      if not install in DocAresPackages.PY_PACKAGES:
        print("Package %s missing from the ones defined in the framework in DocAresPackages.PY_PACKAGES" % install)
      if PROXY is not None:
        subprocess.call([sys.executable, '-m', "pip", 'install', '--proxy="%s"' % PROXY] + pipAttrs + [install])
      else:
        subprocess.call([sys.executable, '-m', "pip", 'install'] + pipAttrs + [install])

      return requires(name, reason, install, package=package, raiseExcept=raiseExcept, autoImport=False)

    if raiseExcept:
      print("Error with %s in script %s, autoload set to %s" % (name, sourceScript, AUTOLOAD))
      print("*** Module %s required ***" % name)
      print(reason)
      if install:
        print("Command to fix this error:")
        print(">>> pip install %s" % install)
      print('')
      raise Exception(err)


# External package required
render_template_string = requires(name='flask', reason='URL remappings', install='No need to install', package='render_template_string', raiseExcept=False, sourceScript=__file__)


def loadPackage(packageName, pipAttrs=None, action='install'):
  """
  :category: AReS System
  :rubric: PY
  :type: system
  :dsc:
    Force the package to be installed manually to the currenty python distribution.
    This will run a pip command to the running python set up
  """
  import subprocess

  if not packageName in DocAresPackages.PY_PACKAGES:
    print("Package %s missing from the ones defined in the framework in DocAresPackages.PY_PACKAGES" % packageName)

  if pipAttrs is None:
    pipAttrs = ['--ignore-installed', '--upgrade'] if action == 'install' else []
  if PROXY is not None:
    subprocess.call([sys.executable, '-m', "pip", action, '--proxy="%s"' % PROXY] + pipAttrs + [packageName])
  else:
    subprocess.call([sys.executable, '-m', "pip", action] + pipAttrs + [packageName])

def installedPackages():
  """
  :category: AReS System
  :rubric: PY
  :type: system
  :dsc:
    Returns the list of packages installed on the running Python distribution
  """
  import subprocess

  subprocess.call(["pip", 'list', '-o'])


JS_IMPORTS = {
  # module are written from the first one to load to the last one
  'bootstrap': {
    'req': [
      {'alias': 'jquery'},
      {'alias': 'popper'},],
    'modules': [
      #{'script': 'tether.min.js', 'version': '1.4.4', 'path': 'tether/%(version)s/js/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      #{'script': 'popper.min.js', 'version': '1.12.9', 'path': 'popper.js/%(version)s/umd/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'bootstrap.min.js', 'version': '4.2.1', 'path': 'bootstrap/%(version)s/js/', 'cdnjs': 'https://stackpath.bootstrapcdn.com'},
      {'script': 'bootstrap.bundle.min.js', 'version': '4.2.1', 'path': 'bootstrap/%(version)s/js/', 'cdnjs': 'https://stackpath.bootstrapcdn.com'},
    ],
    'website': 'https://getbootstrap.com/'},

  # module for the awesome icons
  'font-awesome': {
    'package': {'zip': 'https://use.fontawesome.com/releases/v%(version)s/fontawesome-free-%(version)s-web.zip',
                'root': 'fontawesome-free-%(version)s-web', 'folder': 'releases', 'path': 'v%(version)s'},
    'modules': [
      {'script': 'fontawesome.js', 'version': '5.1.0', 'path': 'releases/v%(version)s/js/', 'cdnjs': 'https://use.fontawesome.com'}],
    'website': 'https://fontawesome.com/'},

  # Javascript packages to handle DataTables
  'datatables': {
    'req': [
      {'alias': 'jquery'},
      {'alias': 'bootstrap'}],
    'modules': [
      {'script': 'jquery.dataTables.min.js', 'version': '1.10.19', 'path': 'datatables/%(version)s/js/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'dataTables.buttons.min.js', 'version': '1.0.1', 'path': 'buttons/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'dataTables.responsive.min.js', 'version': '2.1.1', 'path': 'responsive/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'}]},

  # Datatable group rows
  'datatables-rows-group': {
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'dataTables.rowsGroup.js', 'version': '1.0.0', 'path': 'datatables-rowsgroup/v%(version)s/', 'cdnjs': 'https://cdn.rawgit.com/ashl1'}],
       'website': 'https://datatables.net/forums/discussion/29319/new-rowsgroup-plugin-merge-cells-vertically-rowspan'},

  # Datatable group row
  'datatables-row-group': {
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'dataTables.rowGroup.min.js', 'version': '1.0.4', 'path': 'rowgroup/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'}],
    'website': 'https://datatables.net/extensions/rowgroup/'},

  # Datatable fixed column
  'datatables-fixed-columns': {
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'dataTables.fixedColumns.min.js', 'version': '3.2.2', 'path': 'fixedcolumns/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'}],
    'website': 'https://datatables.net/extensions/fixedcolumns/'},

  # Datatable Fixed header
  'datatables-fixed-header': {
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'dataTables.fixedHeader.min.js', 'version': '3.1.3', 'path': 'fixedheader/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'}],
    'website': 'https://datatables.net/extensions/fixedheader/'},

  # Datatable data export
  'datatables-export': {
    'req': [
      {'alias': 'datatables'}, {'alias': 'jszip'}, {'alias': 'pdfmake'}],
    'website': 'https://datatables.net/extensions/buttons/',
    'modules': [
      {'script': 'buttons.colVis.min.js', 'version': '1.5.2', 'path': 'buttons/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'buttons.bootstrap4.min.js', 'version': '1.5.2', 'path': 'buttons/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'buttons.foundation.min.js', 'version': '1.5.2', 'path': 'buttons/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'buttons.colVis.min.js', 'version': '1.5.2', 'path': 'buttons/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'buttons.html5.min.js', 'version': '1.5.2', 'path': 'buttons/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'buttons.jqueryui.min.js', 'version': '1.5.2', 'path': 'buttons/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'buttons.print.min.js', 'version': '1.5.2', 'path': 'buttons/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'buttons.semanticui.min.js', 'version': '1.5.2', 'path': 'buttons/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'}]},

  # Datatable column reordering modules
  'datatables-col-order': {
    'req': [{'alias': 'datatables'}],
    'website': 'https://datatables.net/extensions/colreorder/',
    'modules': [
      {'script': 'dataTables.colReorder.min.js', 'version': '1.5.1', 'path': 'colreorder/%(version)s/js/', 'cdnjs': 'https://cdn.datatables.net'}]},

  #
  'jszip': {
    'website': 'https://datatables.net/extensions/buttons/',
    'modules': [
      {'script': 'jszip.min.js', 'version': '3.1.5', 'path': 'jszip/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
    ]},

  #
  # # Datatable column reordering modules
  # 'dataTables-select': {
  #   'req': [{'alias': 'dataTables'}], "status": 'deprecated',
  #                       'website': 'https://datatables.net/extensions/select/', 'version': '1.2.5',
  #                       'modules': ['dataTables.select.min.js'],
  #                       'cdnjs': ['https://cdn.datatables.net/select/1.2.5/js/']},

  # Datatable column resizable
  # 'dataTables-colResizable': {
  #   'req': [{'alias': 'dataTables'}],
  #   'modules': [
  #     {'script': 'dataTables.colResize.js', 'version': '0.0.11', 'path': 'ColResize/%(version)s/js/', 'cdnjs': 'https://cdn.rawgit.com/smasala'}],
  #   'website': 'https://github.com/Silvacom/colResize'},

  # Datatable pivot
  'pivot': {
    'website': 'https://github.com/nicolaskruchten/pivottable',
    'modules': [
      {'script': 'pivot.min.js', 'version': '2.21.0', 'path': 'pivottable/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Datatable pivot C3 renderer
  'pivot-c3': {
    'req': [{'alias': 'pivot'}],
    'website': 'https://github.com/nicolaskruchten/pivottable',
    'modules': [
      {'script': 'c3_renderers.min.js', 'version': '2.21.0', 'path': 'pivottable/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Jquery package width CDN links
  'jquery': {
    'website': 'http://jquery.com/',
    'modules': [
      {'script': 'jquery.min.js', 'version': '3.3.1', 'path': 'jquery/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Jquery UI package width CDN links
  'jqueryui': {
    'req': [{'alias': 'jquery'}],
    'website': 'http://jquery.com/',
    'modules': [
      {'script': 'jquery-ui.min.js', 'version': '1.12.1', 'path': 'jqueryui/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'jquery.ui.position.min.js', 'version': '1.9.2', 'path': 'jqueryui/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Jquery-brackets package width CDN links
  'jquery-brackets': {
    'website': 'http://www.aropupu.fi/bracket/',
    'req': [{'alias': 'jquery'}],
    'modules': [
      {'script': 'jquery.bracket.min.js', 'version': '0.11.1', 'path': 'jquery-bracket/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Jquery UI package
  # Attempt to try to solve conflict with Bootstrap
  #'jquery-ui': {'req': ['jquery', 'bootstrap'], 'modules': ['jquery-ui.min.js']},

  # Jquery timepicker width CDN links
  'timepicker': {
    'website': 'https://timepicker.co/',
    'req': [
      {'alias': 'jquery'},
      {'alias': 'jqueryui'}],
    'modules': [
      {'script': 'jquery.timepicker.min.js', 'version': '1.3.5', 'path': 'timepicker/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # To display a context menu when right click on an item
  'jquery-context-menu': {
    'website': 'http://swisnl.github.io/jQuery-contextMenu/demo.html',
    'req': [
      {'alias': 'jquery'},
      {'alias': 'jqueryui'}],
    'modules': [
      {'script': 'jquery.contextMenu.min.js', 'version': '2.6.4', 'path': 'jquery-contextmenu/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # To customize the scrollbar width CDN links
  # https://github.com/malihu/malihu-custom-scrollbar-plugin
  # http://manos.malihu.gr/repository/custom-scrollbar/demo/examples/complete_examples.html
  'jquery-scrollbar': {
    'website': 'http://manos.malihu.gr/jquery-custom-content-scroller/',
    'req': [{'alias': 'jquery'}],
    'modules': [
      {'script': 'jquery.mCustomScrollbar.concat.min.js', 'version': '3.1.5', 'path': 'malihu-custom-scrollbar-plugin/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Javascript packages for the PDF transformation width CDN links
  'pdfmake': {
    'website': '',
    'modules': [
      {'script': 'pdfmake.min.js', 'version': '0.1.37', 'path': 'pdfmake/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'vfs_fonts.js', 'version': '0.1.37', 'path': 'pdfmake/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Clipboard features width CDN links
  'clipboard': {
    'website': 'https://clipboardjs.com/',
    'modules': [
      {'script': 'clipboard.min.js', 'version': '2.0.1', 'path': 'clipboard.js/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Javascript dependencies for D3 and NVD2 components width CDN links
  'd3': {
    'website': 'https://d3js.org/',
    'req': [{'alias': 'jquery'}],
    'modules': [
      {'script': 'd3.min.js', 'version': '5.7.0', 'path': 'd3/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'd3-tip.min.js', 'version': '0.9.1', 'path': 'd3-tip/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Javascript dependencies for Plotly width CDN links
  'plotly': {
    'website': 'https://plot.ly/javascript/',
    'req': [{'alias': 'd3'}],
    'modules': [
      {'script': 'plotly.min.js', 'version': '1.43.1', 'path': 'plotly.js/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # NVD3 Components width CDN links
  'nvd3': {
    'req': [{'alias': 'd3', 'version': '3.5.17'}],
    'modules': [
      {'script': 'nv.d3.min.js', 'version': '1.8.6', 'path': 'nvd3/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # C3 modules width CDN links
  'c3': {
    'website': 'https://c3js.org/',
    'req': [{'alias': 'd3'}],
    'modules': [
      {'script': 'c3.min.js', 'version': '0.6.12', 'path': 'c3/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # DC modules width CDN links
  'dc': {
    'website': 'https://dc-js.github.io/dc.js/examples/',
    'req': [{'alias': 'd3'}],
    'modules': [
      {'script': 'dc.min.js', 'version': '3.0.9', 'path': 'dc/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # billboard modules width CDN links
  'billboard': {
    'website': 'https://naver.github.io/billboard.js/release/latest/doc/',
    'req': [{'alias': 'd3'}],
    'modules': [
      {'script': 'billboard.min.js', 'version': '1.7.1', 'path': 'billboard.js/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # ChartJs modules width CDN links
  'chartjs': {
    'website': 'https://www.chartjs.org/',
    'req': [{'alias': 'd3'}],
    'modules': [
      {'script': 'Chart.bundle.min.js', 'version': '2.7.3', 'path': 'Chart.js/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'Chart.min.js', 'version': '2.7.3', 'path': 'Chart.js/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # ChartJs addon to add label width CDN links
  'chartjs-pie-labels': {
      'website': 'https://chartjs-plugin-datalabels.netlify.com/',
      'req': [{'alias': 'chartjs'}],
      'modules': [
        {'script': 'chartjs-plugin-datalabels.min.js', 'version': '0.5.0', 'path': 'chartjs-plugin-datalabels@%(version)s/dist/', 'cdnjs': 'https://cdn.jsdelivr.net/npm'}]},

  # Cannot add properly the dependency in this one as my algorithm does not work for shared dependencies ....
  # 'meter': {'req': ['d3'], 'modules': ['d3.meter.js'], 'website': '', 'version': '', "status": 'deprecated'},

  # Popper tooltips used by bootstrap in the dropdown components
  'popper': {
    'req': [
      {'alias': 'jquery'},],
    'website': 'https://popper.js.org/',
    'modules': [
      {'script': 'popper.min.js', 'version': '1.14.6', 'path': 'popper.js/%(version)s/umd/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Javascript module for the simple select component. issue with Bootstrap 4 width CDN links
  'select': {
    'website': 'http://silviomoreto.github.io/bootstrap-select/',
    'req': [
      {'alias': 'jquery'},
      {'alias': 'bootstrap'}],
    'modules': [
      {'script': 'bootstrap-select.min.js', 'version': '1.13.0', 'path': 'bootstrap-select/%(version)s/js/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # javascript package for the Venn chart
  # 'venn': {'req': ['d3'], 'modules': ['venn.js'], 'website': '', 'version': '',},

  # Vis Javascript Packages
  'vis': {
    'website': 'http://visjs.org/',
    'modules': [
      {'script': 'vis.min.js', 'version': '4.21.0', 'path': 'vis/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # javascript library to style the content of a paragrap according to the type of code displayed
  'prism': {
    'website': 'https://prismjs.com/',
    'modules': [
      {'script': 'prism.js', 'version': '1.11.0', 'path': 'prism/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Javascript package to display mathematical formulas
  # https://codingislove.com/display-maths-formulas-webpage/
  # https://github.com/mathjax/mathjax
  'mathjs': {
    'website': 'https://www.mathjax.org/',
    'package': {'zip': 'https://github.com/mathjax/MathJax/archive/%(version)s.zip', 'root': 'MathJax-%(version)s', 'folder': 'mathjax'},
    'modules': [
      {'script': 'MathJax.js', 'version': '2.7.5', 'path': 'mathjax/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}],
    # To use the full module online
    #'url': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/',
    'config': "config=TeX-AMS-MML_HTMLorMML"},

  # jquery emoji
  'emoji': {
    'website': 'https://mervick.github.io/emojionearea/',
    'req': [{'alias': 'jquery'}],
    'modules': [
      {'script': 'emojionearea.min.js', 'version': '3.4.1', 'path': 'emojionearea/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Socket IO
  'socket.io': {
    'website': 'https://github.com/socketio/socket.io',
    'req': [{'alias': 'jquery'}],
    'modules': [
      {'script': 'socket.io.js', 'version': '2.1.0', 'path': 'socket.io/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Code mirror
  'codemirror': {
    'website': 'https://codemirror.net/',
    'modules': [
      {'script': 'codemirror.js', 'version': '5.42.2', 'path': 'codemirror/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'python.js', 'version': '5.42.2', 'path': 'codemirror/%(version)s/mode/python/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'r.js', 'version': '5.42.2', 'path': 'codemirror/%(version)s/mode/r/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'markdown.js', 'version': '5.42.2', 'path': 'codemirror/%(version)s/mode/markdown/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'placeholder.js', 'version': '5.42.2', 'path': 'codemirror/%(version)s/addon/display/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},
}


CSS_IMPORTS = {
  'jqueryui': {
    'website': 'http://jquery.com/',
    'modules': [
      {'script': 'jquery-ui.min.css', 'version': '1.12.1', 'path': 'jqueryui/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'jquery-ui.structure.min.css', 'version': '1.12.1', 'path': 'jqueryui/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
      {'script': 'jquery-ui.theme.min.css', 'version': '1.12.1', 'path': 'jqueryui/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Jquery-brackets package width CDN links
  'jquery-brackets': {
    'req': [{'alias': 'jqueryui'}],
    'modules': [
      {'script': 'jquery.bracket.min.css', 'version': '0.11.1', 'path': 'jquery-bracket/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # To display a context menu when right click on an item width CDN links
  # http://swisnl.github.io/jQuery-contextMenu/demo.html#jquery-context-menu-demo-gallery
  'jquery-context-menu': {
    'website': 'https://github.com/swisnl/jQuery-contextMenu/blob/master/dist/jquery.contextMenu.min.css.map',
    'req': [{'alias': 'jqueryui'}],
    'modules': [
      {'script': 'jquery.contextMenu.min.css', 'version': '2.6.4', 'path': 'jquery-contextmenu/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Jquery timepicker width CDN links
  'timepicker': {
    'website': 'https://timepicker.co/',
    'req': [{'alias': 'jqueryui'}],
    'modules': [
      {'script': 'jquery.timepicker.min.css', 'version': '1.3.5', 'path': 'timepicker/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # To customize the scrollbar width CDN links
  'jquery-scrollbar': {
    'website': 'http://manos.malihu.gr/jquery-custom-content-scroller/',
    'req': [{'alias': 'jqueryui'}],
    'modules': [
      {'script': 'jquery.mCustomScrollbar.min.css', 'version': '3.1.5', 'path': 'malihu-custom-scrollbar-plugin/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  'datatables': {
    'website': 'https://datatables.net/',
    'req': [{'alias': 'bootstrap'}],
    'modules': [
      {'script': 'jquery.dataTables.min.css', 'version': '1.10.19', 'path': '%(version)s/css/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'responsive.dataTables.min.css', 'version': '2.1.1', 'path': 'responsive/%(version)s/css/', 'cdnjs': 'https://cdn.datatables.net'},
      {'script': 'buttons.dataTables.min.css', 'version': '1.5.2', 'path': 'buttons/%(version)s/css/', 'cdnjs': 'https://cdn.datatables.net'}]},

  # Datatable group row
  'datatables-row-group': {
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'rowGroup.dataTables.min.css', 'version': '1.0.4', 'path': 'rowgroup/%(version)s/css/', 'cdnjs': 'https://cdn.datatables.net'}]},

  # Datatable fixed column
  'datatables-fixed-columns': {
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'fixedColumns.bootstrap4.min.css', 'version': '3.2.2', 'path': 'fixedcolumns/%(version)s/css/', 'cdnjs': 'https://cdn.datatables.net'}]},

  # Datatable fixed header
  'datatables-fixed-header': {
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'fixedHeader.bootstrap4.min.css', 'version': '3.1.3', 'path': 'fixedheader/%(version)s/css/', 'cdnjs': 'https://cdn.datatables.net'}]},

  # Datatable export module
  'datatables-export': {
    'website': 'https://datatables.net/',
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'buttons.bootstrap4.min.css', 'version': '1.5.2', 'path': 'buttons/%(version)s/css/', 'cdnjs': 'https://cdn.datatables.net'}]},

  # Datatable column ordering
  'datatables-col-order': {
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'colReorder.bootstrap4.min.css', 'version': '1.5.1', 'path': 'colreorder/%(version)s/css/', 'cdnjs': 'https://cdn.datatables.net'}]},

  # Datatable column reordering modules
  'datatables-select': {
    'req': [{'alias': 'datatables'}],
    'modules': [
      {'script': 'select.bootstrap4.min.css', 'version': '1.2.5', 'path': 'select/%(version)s/css/', 'cdnjs': 'https://cdn.datatables.net'}]},

  # # Datatable column resizable
  # 'dataTables-colResizable': {
  #   'req': [{'alias': 'dataTables'}],
  #   'modules': ['dataTables.colResize.css'], 'version': '2.6',
  #                             'cdnjs': ['https://cdn.rawgit.com/smasala/ColResize/v2.6.0/css/'],
  #                             'website': 'https://smasala.github.io/ColResize/', "status": 'deprecated'},

  # Bootstrap style width CDN links
  'bootstrap': {
    'website': 'https://getbootstrap.com/',
    'req': [{'alias': 'font-awesome'}],
    'modules': [
      {'script': 'bootstrap.min.css', 'version': '4.2.1', 'path': 'bootstrap/%(version)s/css/', 'cdnjs': 'https://stackpath.bootstrapcdn.com'}]},

  # Font awesome style width CDN links
  'font-awesome': {
    'website': 'https://fontawesome.com/',
    'package': {'zip': 'https://use.fontawesome.com/releases/v%(version)s/fontawesome-free-%(version)s-web.zip',
                    'root': 'fontawesome-free-%(version)s-web', 'folder': 'releases', 'path': 'v%(version)s'},
    'modules': [
      {'script': 'all.css', 'version': '5.1.0', 'path': 'releases/v%(version)s/css/', 'cdnjs': 'https://use.fontawesome.com'}]},

  # NVD3 Components width CDN links
  'nvd3': {
    'website': 'http://nvd3.org/',
    'modules': [
      {'script': 'nv.d3.min.css', 'version': '1.8.6', 'path': 'nvd3/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # C3 modules width CDN links
  'c3': {
    'website': 'https://c3js.org/',
    'modules': [
      {'script': 'c3.min.css', 'version': '0.6.12', 'path': 'c3/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # DC modules width CDN links
  'dc': {
    'website': 'https://dc-js.github.io/dc.js/examples/',
    'modules': [
      {'script': 'dc.min.css', 'version': '3.0.9', 'path': 'dc/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # billboard modules width CDN links
  'billboard': {
    'modules': [
      {'script': 'billboard.min.css', 'version': '1.7.1', 'path': 'billboard.js/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}],
    'website': 'https://naver.github.io/billboard.js/release/latest/doc/'},

  #'ares': {'req': ['bootstrap'], 'modules': ['bdi.css'], 'website': 'internal lib', 'version': '0'},

  # Javascript module for the simple select component. issue with Bootstrap 4 width CDN links
  'select': {
    'website': 'https://github.com/silviomoreto/bootstrap-select',
    'req': [
      {'alias': 'jqueryui'},
      {'alias': 'bootstrap'}],
    'modules': [
      {'script': 'bootstrap-select.min.css', 'version': '1.13.0', 'path': 'bootstrap-select/%(version)s/css/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Pivot table style with CDN Links
  'pivot': {
    'website': 'https://github.com/nicolaskruchten/pivottable',
    'modules': [
      {'script': 'pivot.min.css', 'version': '2.21.0', 'path': 'pivottable/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Vis style with CDN Links
  'vis': {
    'website': 'http://visjs.org/',
    'modules': [
      {'script': 'vis.min.css', 'version': '4.21.0', 'path': 'vis/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Prism style with CDN Links
  'prism': {
    'website': 'https://prismjs.com/',
    'modules': [
      {'script': 'prism.css', 'version': '1.11.0', 'path': 'prism/%(version)s/themes/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # jquery emoji
  # https://github.com/mervick/emojionearea
  'emoji': {
    'website': 'https://mervick.github.io/emojionearea/',
    'modules': [
      {'script': 'emojionearea.min.css', 'version': '3.4.1', 'path': 'emojionearea/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},

  # Code mirror
  'codemirror': {
    'website': 'https://codemirror.net/',
    'modules': [
      {'script': 'codemirror.css', 'version': '5.39.2', 'path': 'codemirror/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'}]},
  }


class ImportManager(object):
  """
  :category: Import Class
  :rubric: PY
  :type: System
  :dsc:
    The main class in charge of defining the order of the imports in the header.

    There is no check on the presence of the modules on the server. The only purpose of this module is to produce the
    string with the module names and the correct paths to your final HTML report.
  """

  def __init__(self, online=False, aresObj=None):
    """ Load the hierarchy of modules """
    self.aresObj = aresObj
    self.jsImports, self.cssImports, self.moduleConfigs, self.reqVersion = {}, {}, {}, {}
    for folder, importDic, importType in [('js', self.jsImports, JS_IMPORTS), ('css', self.cssImports, CSS_IMPORTS)]:
      for alias, definition in importType.items():
        main, versions = OrderedSet.OrderedSet(), OrderedSet.OrderedSet()
        for i, mod in enumerate(definition['modules']):
          versions.add(mod['version'])
          script = "".join([mod['path'] % mod, mod['script']])
          if online:
            main.add("%s/%s" % (mod['cdnjs'], script))
          elif 'url' in definition:
            main.add("%s%s" % (definition['url'], script))
          else:
            main.add("{{ url_for(\'static\',filename=\'%s\') }}" % script)
        modules = OrderedSet.OrderedSet()
        self.getModules(modules, alias, folder, importType)
        if 'config' in definition:
          self.moduleConfigs[alias] = definition['config']
        importDic[alias] = {'main': main, 'dep': modules, 'versions': versions}

  def getModules(self, modules, alias, folder, defModule):
    """ Return the list of modules for a given entry """
    if isinstance(alias, dict):
      alias = alias['alias']
    for mod in defModule[alias]['modules']:
      script = "".join([mod['path'] % mod, mod['script']])
      if 'url' in defModule[alias]:
        modules.add("%s/%s" % (defModule[alias]['url'], script))
      else:
        modules.add("{{ url_for(\'static\',filename=\'%s\') }}" % script)
    for req in defModule[alias].get('req', []):
      self.getModules(modules, req, folder, defModule)

  def getReq(self, mod, modList, importHierarchy):
    """ Returns the list pf reuired modules for a given alias """
    if isinstance(mod, dict):
      # This will allow different versions of packages according to the modules
      # For example NVD3 cannot use any recent version of D3
      if 'version' in mod:
        self.reqVersion[mod['alias']] = mod['version']
        for i, path in enumerate(self.jsImports[mod['alias']]['main']):
          for v in self.jsImports[mod['alias']]['versions']:
            path = path.replace(v, mod['version'])
          self.jsImports[mod['alias']]['main'][i] = path
        for i, path in enumerate(self.jsImports[mod['alias']]['dep']):
          for v in self.jsImports[mod['alias']]['versions']:
            path = path.replace(v, mod['version'])
          self.jsImports[mod['alias']]['dep'][i] = path
      mod = mod['alias']
    modList.append(mod)
    for req in importHierarchy.get(mod, {}).get("req", []):
      self.getReq(req, modList, importHierarchy)

  def cleanImports(self, imports, importHierarchy):
    """ Remove the underlying imports to avoid duplicated entries """
    importResolve = []
    for mod in imports:
      self.getReq(mod, importResolve, importHierarchy)
    setImport = set(importResolve)
    for a in setImport:
      occurences = [j for j, x in enumerate(importResolve) if x == a]
      if len(occurences) > 1:
        for j in occurences[::-1][1:]:
          importResolve.pop(j)
    return importResolve[::-1]

  def cssResolve(self, cssAliases, localCss=None):
    """ Return the list of CSS modules to add to the header """
    cssList = []
    cssAliases = self.cleanImports(cssAliases, CSS_IMPORTS)
    for cssAlias in cssAliases:
      for urlModule in list(self.cssImports[cssAlias]['main']):
        cssList.append('<link rel="stylesheet" href="%s" type="text/css">' % urlModule)
    if localCss is not None:
      for localCssFile in localCss:
        cssList.append('<link rel="stylesheet" href="{{ url_for(\'static\',filename=\'users/%s\') }}" type="text/css">' % localCssFile)
    return "\n".join([render_template_string(css) for css in cssList])

  def jsResolve(self, jsAliases, localJs=None):
    """ Return the list of Javascript modules to add to the header """
    jsList = []
    jsAliases = self.cleanImports(jsAliases, JS_IMPORTS)
    for jsAlias in jsAliases:
      extraConfigs = "?%s" % self.moduleConfigs[jsAlias] if jsAlias in self.moduleConfigs else ""
      for urlModule in list(self.jsImports[jsAlias]['main']):
        if '/mode/' in urlModule:
          jsList.append('<script type="module" language="javascript" src="%s%s"></script>' % (urlModule, extraConfigs))
        else:
          jsList.append('<script language="javascript" type="text/javascript" src="%s%s"></script>' % (urlModule, extraConfigs))
    if localJs is not None and len(localJs) > 0:
      extraConfigs = "?%s" % self.moduleConfigs[jsAlias] if jsAlias in self.moduleConfigs else ""
      for localJsFile in localJs:
        jsList.append('<script language="javascript" type="text/javascript" src="{{ url_for(\'static\',filename=\'users/%s\') }}%s"></script>' % (localJsFile, extraConfigs))
    return "\n".join([render_template_string(js) for js in jsList])

  def getFiles(self, cssAlias, jsAlias):
    files = {'css': [], 'js': []}
    modCss, modJs = {}, {}
    for alias, details in CSS_IMPORTS.items():
      modCss[alias] = []
      for module in details['modules']:
        modCss[alias].append( {'version': details.get('version', ''), 'alias': alias, 'file': module, 'website': details.get('website', ''), 'status': details.get('status', '')} )
    for alias, details in JS_IMPORTS.items():
      modJs[alias] = []
      for module in details['modules']:
        modJs[alias].append( {'version': details.get('version', ''), 'alias': alias, 'file': module, 'website': details.get('website', ''), 'status': details.get('status', '')} )

    for cssFile in self.cleanImports(cssAlias, CSS_IMPORTS):
      files['css'].extend(modCss[cssFile])

    for jsFile in self.cleanImports(jsAlias, JS_IMPORTS):
      files['js'].extend(modJs[jsFile])
    return files

  def cssGetAll(self):
    """ To retrieve the full list of available modules on the server """
    return self.cssResolve(set(CSS_IMPORTS.keys()))

  def jsGetAll(self):
    """ To retrieve the full list of available modules on the server """
    return self.jsResolve(set(JS_IMPORTS.keys()))

  def getPackage(self, alias, version=None, staticPath=None, withDep=False, reload=True):
    """
    :category: Package Installer
    :rubric: PY
    :type: System
    :dsc:
      Function in charge of downloading the different external CSS and JS packages locally.
      This will guarantee the install without having to get any extra features saved on a repository.
      Saved copies of the modules can be done in order to guarantee a off line mode
    """
    ares_requests = requires('requests', reason='CDNJS request', install='requests', raiseExcept=True, autoImport=True, sourceScript=__file__)

    packages = {}
    _staticPath = os.path.join(os.path.dirname(__file__), '..', '..', 'static')if staticPath is None else staticPath
    for pckg in [JS_IMPORTS, CSS_IMPORTS]:
      if withDep:
        for depAlias in self.cleanImports([alias], pckg):
          if depAlias != alias:
            self.getPackage(depAlias, reload=reload)

      if 'package' in pckg.get(alias, {}):
        packages[alias] = os.path.join(_staticPath, pckg[alias]['package']['folder'])

      for mod in pckg.get(alias, {}).get('modules', []):
        _version = self.reqVersion.get(alias, mod['version']) if version is None else version
        script = "".join([mod['path'] % {'version': _version}, mod['script']])
        path = os.path.join(_staticPath, mod['path'] % {'version': _version})
        if not os.path.exists(path):
          os.makedirs(path)

        reloadModule = True
        extFilePath = r"%s\%s" % (path, mod['script'])
        if os.path.exists(extFilePath) and not reload:
          reloadModule = False

        if reloadModule:
          page = ares_requests.get("%s/%s" % (mod['cdnjs'], script))
          if page.status_code == 404:
            print(" # Error - %s: Script %s/%s not found "% (alias, mod['cdnjs'], script))
            continue

          try:
            extFileName = open(extFilePath, "w", encoding='utf8')
            extFileName.write(page.text)
            extFileName.close()
            print("  > %s - %s, version %s. Done !" % (alias, mod['script'], _version))
          except Exception as err:
            print(" # Exception - %s: %s/%s, %s" % (alias, mod['script'], _version, err))
            print(err)
        else:
          print("  > %s - %s, version %s. Already defined !" % (alias, mod['script'], _version))

    if len(packages) > 0:
      print("")
      print("Downloading %s packages, this might take few minutes" % len(packages))
      for pckg, folder in packages.items():
        self.getFullPackage(pckg, version=version, staticPath=staticPath, reload=reload)

  def getFullPackage(self, alias, version=None, staticPath=None, reload=False):
    """
    :category: Package Installer
    :rubric: PY
    :type: System
    :dsc:
      Download a full package (CSS and JS) locally for a server or full offline mode
    https://use.fontawesome.com/releases/v5.6.3/fontawesome-free-5.6.3-web.zip
    https://github.com/mathjax/MathJax/archive/v2.6-latest.zip
    """
    import zipfile
    import shutil
    import io
    import os

    ares_requests = requires('requests', reason='CDNJS request', install='requests', raiseExcept=True, autoImport=True, sourceScript=__file__)
    if 'package' in JS_IMPORTS[alias]:
      versionDict = {'version': JS_IMPORTS[alias]['modules'][0]['version'] if version is None else version}
      packagePath = JS_IMPORTS[alias]['package']['zip'] % versionDict
      if staticPath is None:
        staticPath = os.path.join(os.path.dirname(__file__), '..', '..', 'static', JS_IMPORTS[alias]['package']['folder'])
      if not os.path.exists(staticPath):
        # Create the destination folders if missing
        os.makedirs(staticPath)
      dstPath = os.path.join(staticPath, JS_IMPORTS[alias]['package'].get('path', '%(version)s') % versionDict)
      vReloadPath = True
      if os.path.exists(dstPath):
        if not reload:
          vReloadPath = False
        else:
          shutil.rmtree(dstPath)

      if vReloadPath:
        print("  > Downloading package %s" % packagePath)
        r = ares_requests.get(packagePath, stream=True)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(staticPath)
        if JS_IMPORTS[alias]['package']['root'] is not None:
          root = JS_IMPORTS[alias]['package']['root'] % versionDict
          shutil.copytree(os.path.join(staticPath, root), dstPath)
          shutil.rmtree(os.path.join(staticPath, root))
        print("  < Package %s. Done ! " % alias)
      else:
        print("  < Package %s already loaded " % alias)
    return self

  def addPackage(self, alias, config):
    """
    :category: New External Package
    :rubric: PY
    :type: Framework Extension
    :example:
      i.addPackage('test',
        {
          'req': [{'alias': 'd3'}],
          'modules': [
            {'script': 'dc.min.css', 'version': '3.0.9', 'path': 'dc/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
            {'script': 'dc.min.js', 'version': '3.0.9', 'path': 'dc/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
          ]},
        )
    :dsc:
      Add a new package or update an existing one with new parameters.
      Only few parameters are available here in order to limit the changes
    """
    global CSS_IMPORTS
    global JS_IMPORTS

    modEntry = {'css': {}, 'js': {}}
    for mod in config['modules']:
      if mod['script'].endswith(".css"):
        modEntry['css'].setdefault('modules', []).append(mod)
        if 'req' in config:
          for req in config['req']:
            if req['alias'] in CSS_IMPORTS:
              modEntry['css'].setdefault('req', []).append(req)
      elif mod['script'].endswith(".js"):
        modEntry['js'].setdefault('modules', []).append(mod)
        if 'req' in config:
          for req in config['req']:
            if req['alias'] in JS_IMPORTS:
              modEntry['js'].setdefault('req', []).append(req)
    if len(modEntry['css']) > 0:
      CSS_IMPORTS.setdefault(alias, {}).update(modEntry['css'])
    if len(modEntry['js']) > 0:
      JS_IMPORTS.setdefault(alias, {}).update(modEntry['js'])
    return self

  def setPackages(self, staticPath=None, reload=False):
    """
    :category: All Packages install
    :rubric: PY
    :type: System
    :dsc:
      Download all the CSS and Js packages from the official CDNJS configured in the configuration.
      It is possible to get the configuration settings by calling the function getPackageInfo(aliasName) attached to
      the aresObj
    """
    aliases = list(set(list(CSS_IMPORTS.keys()) + list(JS_IMPORTS.keys())))
    for alias in aliases:
      self.getPackage(alias, staticPath=staticPath, reload=reload)
    return self


if __name__ == "__main__":
  """ """
  #loadPackage('pandas')
  i = ImportManager()
  #loadPackage('ARES', action='uninstall')
  #i.getPackage('d3', version='3.5.17')
  # i.getFullPackage('font-awesome', reload=True)
  # i.getFullPackage()
  # i.getPackage('c3', version='0.5.1', staticPath=r"K:\Dev\statics")
  #
  # i.addPackage('test',
  #   {
  #     'req': [{'alias': 'd3'}],
  #     'modules': [
  #       {'script': 'dc.min.css', 'version': '3.0.9', 'path': 'dc/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
  #       {'script': 'dc.min.js', 'version': '3.0.9', 'path': 'dc/%(version)s/', 'cdnjs': 'https://cdnjs.cloudflare.com/ajax/libs'},
  #     ]},
  #   )

  installedPackages()