#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


DATA = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=EDGE" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Cache-control" content="no-cache">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ title }}</title>
{{ cssImports|safe }}
{{ jsImports|safe }}

<style>
{{ cssStyle|safe }}
</style>

<script>
{{ jsGlobal|safe }}

$(document).ready(function() { {{ jsDocumentReady|safe }} });

window.onload = function() { {{ jsWindowLoad|safe }} };

$(window).bind("pageshow", function(event) { $("div[name='ares_loading']").hide() });

$(window).on('beforeunload', function(){
    if (typeof NO_UNLOAD === 'undefined') {$("div[name='ares_loading']").show()}
    else {
        if (NO_UNLOAD == true) { NO_UNLOAD=false;}
        else { $("div[name='ares_loading']").show() } }
});
</script>

</head>
<body onclick="$('#popup').hide()">

<div id="ares_page_content">
{{ content|safe }}
</div>

<div id="popup_loading_back" name="ares_loading" style="display:none;">&nbsp;</div>

<div id="popup_loading" name="ares_loading" style="display:none;">
    <span class="fas fa-spinner fa-spin" style="padding:auto;margin:auto;font-size:65px;"></span>
    <div style="font-size:20px;">Loading...</div>
</div>
<br />
<footer class="footer" style="position:relative;bottom:0;width:100%;" id="footer">
  <div style="text-align:center">
  <span style="display:inline-block;float:left;">
      2017-2018 Open Source platform
  </span>
  <span style="display:inline-block;float:right;text-align:right;"><a href="mailto:{{mailTo|safe}}">Contact Us</a></span>
  </div>
  <div >
      <span style="display:inline-block;text-align:justify;width:100%;margin-bottom:15px;margin-top:20px">
        This platform is not an Official Production platform and shouldn't be used as such. It is available as a complimentary tool but it is not intended to be the framework to be used for budgeted projects. Using this platform as such could result in project cancellation or delays as sign-off couldn't be made for those projects. <br>
        This platform's development team cannot take responsibility or support any projects started and based on it if not priorly approved by Management.
        <br /><br />
        Proudly powered by <a href='/index'>AReS</a>
      </span>
  </div>
</footer>
<script>
{{ jsGraphs|safe }}
</script>
</body>
</html>
'''