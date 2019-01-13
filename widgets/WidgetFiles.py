#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.widgets import Widget

# Special external imports
Widget.requires('ares.AresTransfer', 'Set up the file transfer with the server', 'pip install flask')


class WidgetFileManager(Widget.Widget):
  """
  :category: Widget
  :rubric: PY
  :type: Files
  :dsc:
    Widget displaying a table with the available tables and also some features to upload new files.
    This interface will allow you to manage the input files but also ensure the security around the data uploaded.
    Indeed only the persons allowed (the data owner) will see the data.
  """
  name, label = 'Widget File', 'Files Module to store and see the available data in the environment'

  def html(self, params):
    dropZone = self.aresObj.dropfile(tooltip="Drag and drop your input files here").drop("%s/upload/%s/%s" % (self.aresObj._urlsApp['ares-transfer'], "OUTPUTS", self.aresObj.run.report_name))
    list = self.aresObj.list(height=params.get('height', 100), dataSrc={"type": "flask", "on_init": True, 'blueprint': 'ares-transfer',
                             "fnc": AresTransfer.getFiles, "pmts_def": ['report_name', 'folder_code'],
                             'pmts': [self.aresObj.run.report_name, params.get('folder_code', "OUTPUTS")] },
                             htmlCode="file_monitoring", searchable=True )
    list.template("%(filename)s, last update %(lst_update)s size %(size)sKo")

    popup = self.aresObj.popup()
    popup + self.aresObj.button("Test")

    popupGrp = self.aresObj.popup()
    popupGrp + self.aresObj.button("Update")

    # Add some useful actions to the file object
    list._jsStyles['close'] = "<i onclick='DeleteItem(event, this)' style='position:absolute;right:5px;color:#C00000' class='far fa-times-circle'></i>"
    # list.jsAction("fas fa-user-shield", 'OutputFileGroup', popupGrp.show())
    list.delete(jsFncs=[
      "var url = '%s/remove/file/%s/%s/'+ data.split(',')[0]" % (self.aresObj._urlsApp['ares-transfer'], params.get('folder_code', "OUTPUTS"), self.aresObj.run.report_name),
      self.aresObj.jsPost('url' , jsFnc=[], isDynUrl=True)])
    list.jsItemAction("fas fa-file-download", 'DownloadOutput', [
      "var fileName = data.split(',')[0]",
      self.aresObj.jsGoTo('"%s/download/%s/%s/" + fileName' % (self.aresObj._urlsApp['ares-transfer'], params.get('folder_code', "OUTPUTS"), self.aresObj.run.report_name ) ) ] )
    # list.jsItemAction("far fa-eye", 'ViewOuputFile', popup.show() )
    # jsData="%(filename)s, last update %(lst_update)s"
    col = self.aresObj.col( [dropZone, list] ).css( {"margin-bottom": "10px" } )
    return (col, list)