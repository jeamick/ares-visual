#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.configs.D3 import D3Base


class D3WorldCloud(D3Base.D3Base):
  name, chartCall, chartType = 'WorldCloud', 'worldcloud', 'worldcloud'
  mocks = [
    {"key": "One", "value": 29},
    {"key": "Four", "value": 96},
    {"key": "Other", "value": 30}
  ]

  def config(self): self.aresObj.jsImports.add('cloud')

  def jsBuild(self):
    return '''   
      var width = parseInt($('#%(htmlId)s').parent().css("width"))  ;
      var height = parseInt($('#%(htmlId)s').parent().css("height"))  ;
    
      var text_string = "Olivier fifty fifty fifty fifty fifty fifty fifty fifty fifty fifty fifty fifty in late charges at the public library";
      drawWordCloud(text_string);

      function drawWordCloud(text_string){
        var common = "poop,i,me,my,myself,we,us,our,ours,ourselves,you,your,yours,yourself,yourselves,he,him,his,himself,she,her,hers,herself,it,its,itself,they,them,their,theirs,themselves,what,which,who,whom,whose,this,that,these,those,am,is,are,was,were,be,been,being,have,has,had,having,do,does,did,doing,will,would,should,can,could,ought,i'm,you're,he's,she's,it's,we're,they're,i've,you've,we've,they've,i'd,you'd,he'd,she'd,we'd,they'd,i'll,you'll,he'll,she'll,we'll,they'll,isn't,aren't,wasn't,weren't,hasn't,haven't,hadn't,doesn't,don't,didn't,won't,wouldn't,shan't,shouldn't,can't,cannot,couldn't,mustn't,let's,that's,who's,what's,here's,there's,when's,where's,why's,how's,a,an,the,and,but,if,or,because,as,until,while,of,at,by,for,with,about,against,between,into,through,during,before,after,above,below,to,from,up,upon,down,in,out,on,off,over,under,again,further,then,once,here,there,when,where,why,how,all,any,both,each,few,more,most,other,some,such,no,nor,not,only,own,same,so,than,too,very,say,says,said,shall";
        var word_count = {};
        var words = text_string.split(/[ '\-\(\)\*":;\[\]|{},.!?]+/);
          if (words.length == 1){
            word_count[words[0]] = 1;
          } else {
            words.forEach(function(word){
              var word = word.toLowerCase();
              if (word != "" && common.indexOf(word)==-1 && word.length>1){
                if (word_count[word]){word_count[word]++;} 
                else {word_count[word] = 1;}
              }
            })
          };

        var fill = d3.scale.category20();
        var word_entries = d3.entries(word_count);
        var xScale = d3.scale.linear().domain([0, d3.max(word_entries, function(d) {return d.value;})]).range([10, 100]);

        function draw_worldcloud(words) {
          d3.select( $('#%(htmlId)s').get(0) ).attr("width", width).attr("height", height)
            .append("g").attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
            .selectAll("text").data(words)
            .enter().append("text")
              .style("font-size", function(d) { return xScale(d.size) + "px"; })
              .style("font-family", "Impact")
              .style("fill", function(d, i) { return fill(i); })
              .attr("text-anchor", "middle")
              .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
              .text(function(d) { return d.text; });
        }
        
        d3.layout.cloud().size([width, height]).timeInterval(20)
          .words(word_entries).fontSize(function(d) { return xScale(+d.value); })
          .text(function(d) { return d.key; }).rotate(function() { return ~~(Math.random() * 2) * 90; })
          .font("Impact").on("end", draw_worldcloud).start();
          
        d3.layout.cloud().stop();
      } ''' % {"htmlId": self.chartId}
