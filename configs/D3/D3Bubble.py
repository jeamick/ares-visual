#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
from ares.configs.D3 import D3Base


class D3Bubble(D3Base.D3Base):
  """

  :example:
    import random
    data = []
    for i in range(100):
      data.append({'text': "Allagash", 'size': random.randint(1, 10), 'group': i})
    aresObj.plot('gravity', data, height=400)
  """
  name, chartCall, chartType = 'Bubble Chart', 'gravity', 'bubble'

  def jsBuild(self):
    return ''' 
      var padding = 1.5; 
      var clusterPadding = 6;
      var maxRadius = 12;
      var color = d3.scale.ordinal().range(["#334D6B", "#bbeeee"]);
      var data = %(jsData)s; 
      var cs = [];
      var width = parseInt($('#%(htmlId)s').parent().css("width"))  ;
      var height = parseInt($('#%(htmlId)s').parent().css("height"))  ;
      
      data.forEach(function(d){cs.push(d.group);});
      var n = data.length, m = cs.length; 
      var clusters = new Array(m);
      var nodes = []; for (var i = 0; i<n; i++){ nodes.push(create_nodes(data, i)) };
      var force = d3.layout.force().nodes(nodes).size([width, height]).gravity(.02).charge(0).on("tick", tick).start();
      var svg = d3.select( $('#%(htmlId)s').get(0) ).attr("width", width).attr("height", height);
      var node = svg.selectAll("circle").data(nodes).enter().append("g").call(force.drag);
      node.append("circle").style("fill", function (d) {return color(d.cluster);}).attr("r", function(d){return d.radius});
      node.append("text").attr("dy", ".3em").style("text-anchor", "middle").text(function(d) { return d.text.substring(0, d.radius / 3); } );

      function create_nodes(data, node_counter) {
        var i = cs.indexOf(data[node_counter].group),
            r = Math.sqrt((i + 1) / m * -Math.log(Math.random())) * maxRadius,
            d = { cluster: i, radius: data[node_counter].size*1.5, text: data[node_counter].text,
              x: Math.cos(i / m * 2 * Math.PI) * 200 + width / 2 + Math.random(),
              y: Math.sin(i / m * 2 * Math.PI) * 200 + height / 2 + Math.random() };
        if (!clusters[i] || (r > clusters[i].radius)) {clusters[i] = d;};
        return d;
      };
      
      function tick(e) {
          node.each(cluster(10 * e.alpha * e.alpha)).each(collide(.5)).attr("transform", function (d) {var k = "translate(" + d.x + "," + d.y + ")"; return k;}) }

      function cluster(alpha) {
          return function (d) {
              var cluster = clusters[d.cluster];
              if (cluster === d) return;
              var x = d.x - cluster.x,
                  y = d.y - cluster.y,
                  l = Math.sqrt(x * x + y * y),
                  r = d.radius + cluster.radius;
              if (l != r) {
                  l = (l - r) / l * alpha;
                  d.x -= x *= l;
                  d.y -= y *= l;
                  cluster.x += x;
                  cluster.y += y;
              }
          };
      } ;
      var quadtree = d3.geom.quadtree(nodes);

      function collide(alpha) {
        var quadtree = d3.geom.quadtree(nodes);
        return function (d) {
            var r = d.radius + maxRadius + Math.max(padding, clusterPadding),
                nx1 = d.x - r,
                nx2 = d.x + r,
                ny1 = d.y - r,
                ny2 = d.y + r;
            quadtree.visit(function (quad, x1, y1, x2, y2) {
                if (quad.point && (quad.point !== d)) {
                    var x = d.x - quad.point.x,
                        y = d.y - quad.point.y,
                        l = Math.sqrt(x * x + y * y),
                        r = d.radius + quad.point.radius + (d.cluster === quad.point.cluster ? padding : clusterPadding);
                    if (l < r) {
                        l = (l - r) / l * alpha;
                        d.x -= x *= l;
                        d.y -= y *= l;
                        quad.point.x += x;
                        quad.point.y += y;
                    }
                }
                return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
            });
        };
    }; ''' % {'htmlId': self.chartId, "jsData": json.dumps(self.data) }