#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
import io
import zipfile
from ares.Lib import AresImports

from ares.Lib.html import AresHtml

# External package required
render_template_string = AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='render_template_string', raiseExcept=False, sourceScript=__file__)
url_for = AresImports.requires(name='flask', reason='URL remappings', install='No need to install', package='url_for', raiseExcept=False, sourceScript=__file__)


class DownloadMemoryZip(AresHtml.Html):
  """

  TODO Find a way to send the in memory file form a report: data: %(archive)s,
  """
  alias, cssCls = 'anchorFMemory', ['btn', 'btn-success']
  references = ['https://newseasandbeyond.wordpress.com/2014/01/27/creating-in-memory-zip-file-with-python/']
  reqCss = ['bootstrap', 'font-awesome']
  file_location = 'data'

  def __init__(self, aresObj, vals, fileName, cssCls=None, cssAttr=None):
    super(DownloadMemoryZip, self).__init__(aresObj, vals,  cssCls, cssAttr)
    self.fileName = fileName
    self.memory_file = io.BytesIO()
    self.zf = zipfile.ZipFile(self.memory_file, mode='w', compression=zipfile.ZIP_DEFLATED)

  def add(self, data, filename):
    """ Add the content of string to a file in the in-memory package

    :param data: The data
    :param filename: The filename
    :return:
    """
    self.zf.writestr(filename, data)

  def namelist(self):
    """ Return the list of files in the in-memory zip archive

    :return:
    """
    return self.zf.namelist()

  def __str__(self):
    """ The HTML object representation """
    url = render_template_string('''{{ url_for(\'ares.downloadMemory\') }}''')
    self.aresObj.jsOnLoadFnc.add('''
        $('#%(htmlId)s').click(function() {
            $.ajax({
              url: %(url)s,
              type: "POST",
              contentType: attr( "enctype", "multipart/form-data" ),
              data: %(archive)s,
              success: success
            });
        });
      ''' % {'htmlId': self.htmlId, 'url': url, 'archive': self.zf})
    return '<button %s>%s</button>' % (self.strAttr(), self.vals)


class DropFile(AresHtml.Html):
  __reqCss, __reqJs = ['bootstrap', 'font-awesome'], ['bootstrap']
  __pyStyle =  ['CssDropFile']
  name, category, inputType, callFnc, docCategory = 'Drop File Area', 'Input', "file", 'dropfile', 'Advanced'

  def __init__(self, aresObj, vals, tooltip, report_name, fileType):
    super(DropFile, self).__init__(aresObj, vals)
    self.tooltip(tooltip, location='bottom')
    self.report_name, self.dataType = report_name if report_name is not None else self.aresObj.run.report_name, fileType
    for action in ["dragover", "dragleave", "dragenter"]:
      self.jsFrg(action, "event.originalEvent.preventDefault(); event.originalEvent.stopPropagation(); event.originalEvent.dataTransfer.dropEffect = 'copy';")
    self.css( {"display": "inline-block", "width": '100%'})

  @property
  def jsQueryData(self): return {}

  def drop(self, url=None, jsData=None, jsFncs=None, httpCodes=None, isPyData=True, refresh=True, extensions=None):
    data = []
    if url is None:
      url = "%s/upload/OUTPUTS/%s" % (self.aresObj._urlsApp['ares-transfer'], self.report_name)
    if jsFncs is None:
      jsFncs = [ self.aresObj.jsReloadPage() ]
    elif not isinstance(jsFncs, list):
      jsFncs = [jsFncs]

    if jsData is not None:
      for rec in jsData:
        if isinstance(rec, tuple):
          if isPyData:
            data.append( "data.append('%s', %s)" % (rec[0], json.dumps(rec[1])) )
          else:
            data.append("data.append('%s', %s)" % (rec[0], rec[1]))
        else:
          data.append("data.append('%s', %s)" % (rec.htmlCode, rec.val))
    super(DropFile, self).drop('''
      event.originalEvent.preventDefault(); event.originalEvent.stopPropagation();
      var files = event.originalEvent.dataTransfer.files; var data = new FormData();
      $.each(event.originalEvent.dataTransfer.files, function(i, file) { 
        var fileExt = '.' + file.name.split('.').pop() ;
        if ( %(extensions)s == null ) { data.append(file.name, file) ; } else {
          if (%(extensions)s.indexOf( fileExt ) >= 0) { data.append(file.name, file) ; } } });
      %(jsData)s; %(ajax)s; ''' % {"jsData": ";".join(data), "extensions": json.dumps(extensions),
                                   "ajax": self.aresObj.jsAjax(url, success=";".join(jsFncs) if refresh else '' ) })
    return self

  def __str__(self):
    return '''
      <div %(strAttr)s><b><i class="fas fa-cloud-upload-alt" style="font-size:20px"></i>&nbsp;&nbsp;%(vals)s</b></div>
      <input id="%(htmlId)s_report" style="display:none;" value="%(envs)s"/>
      ''' % {'htmlId': self.htmlId, 'strAttr': self.strAttr(pyClassNames=self.__pyStyle), 'vals': self.vals, 'envs': self.report_name}


