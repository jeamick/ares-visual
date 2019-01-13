#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DSC = {
    'eng':
'''
:dsc:

'''}


from ares.Lib.html import AresHtml


class DangerAlert(AresHtml.Html):
  """ Python wrapper for the display of Danger notification in the report

  :example
  aresObj.notification('#1','WARNING', 'Alerrt', 'Code bafoue')
  """
  level, cssCls = 'Danger', ['alert', 'alert-danger']
  closeButton = False
  reqJs, reqCss = ['bootstrap'], ['bootstrap']
  name, category = 'Alert', 'Notification'
  marginTop = 80

  def __init__(self, aresObj, title, value, countNotif, width, widthUnit, height=None, heightUnit=None, closeButton=False, backgroundColor=None):
    """ Instantiate the Danger notification box """
    super(DangerAlert, self).__init__(aresObj, value, width=width, widthUnit=widthUnit, height=height, heightUnit=heightUnit)
    self.title, self.closeButton, self.countNotif = title, closeButton, countNotif
    heightSpace = 70 if self.closeButton else 10
    self.css({'position': 'absolute', 'z-index': '290', 'right': '5px',
              'background': backgroundColor if backgroundColor is not None else self.bgColor(),
              'top': '%spx' % (self.marginTop + self.countNotif * heightSpace)})

  def bgColor(self): return self.getColor('redColor', 7)

  def __str__(self):
    """ Return the string representation for an alert """
    if self.closeButton:
      self.addClass(['alert-dismissable', 'notif'])
      item = ['<div %s>' % self.strAttr(withId=False)]
      item.append('<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>')
    else:
      item = ['<div %s>' % self.strAttr(withId=False)]
    item.append('<strong>%s!</strong> %s </div>' % (self.title, self.vals))
    return "".join(item)


class SuccessAlert(DangerAlert):
  """ Python wrapper for the display of Success notification in the report  """
  level = 'Success'
  closeButton = True
  cssCls = ['alert', 'alert-success']
  name, category = 'Success', 'Notification'

  def bgColor(self): return self.getColor('greenColor', 3)


class WarningAlert(DangerAlert):
  """ Python wrapper for the display of Warning notification in the report  """
  level = 'Info'
  closeButton = True
  cssCls = ['alert', 'alert-warning']
  name, category = 'Warning', 'Notification'

  def bgColor(self): return self.getColor('redColor', 6)


class InfoAlert(DangerAlert):
  """ Python wrapper for the display of Info notification in the report """
  level = 'Warning'
  closeButton = True
  cssCls = ['alert', 'alert-info']
  name, category = 'Info', 'Notification'

  def bgColor(self): return self.getColor('blueColor', 10)


