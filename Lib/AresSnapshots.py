from selenium import webdriver
from flask import url_for
import os
import config

def takeSnapshot(report_name, root_path, script_name=None, *args, **kwargs):
  """ """

  options = webdriver.ChromeOptions()
  options.add_argument("headless")
  driver = webdriver.Chrome(os.path.join(root_path, 'system', 'webDrivers', 'chromedriver'), chrome_options=options)
  if not script_name:
    script_name = report_name

  url_str = url_for('ares.run_report', report_name=report_name, script_name=script_name, **kwargs)
  if report_name.startswith('_'):
    report_dir = os.path.join(root_path, config.ARES_FOLDER, 'reports', report_name)
    if report_name == '_AresTemplates':
      url_str = url_for('ares.run_template', template=script_name)
  else:
    report_dir = os.path.join(root_path, config.ARES_USERS_LOCATION, report_name)
  driver.get(url_str)
  driver.save_screenshot(os.path.join(report_dir, '%s.png' % script_name ))
  driver.quit()