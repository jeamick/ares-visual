#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

from ares.configs.NVD3 import NVD3Base


class NVD3ForceDirected(NVD3Base.NVD3):
  """ """
  name, chartObj, chartCall = 'Forced Directed', 'forceDirectedGraph', 'network'
  convertFnc = ["NVD3XYFormat"]

  mocks = {
    "nodes":[
    {"name":"A","group":1},
    {"name":"B","group":2},
    {"name":"C","group":2}],
        "links":[
            {"source":0,"target":1,"value":1},
            {"source": 0, "target": 2, "value": 1}

        ]
  }

  def config(self):
    """ """

    self.addAttr('color', 'function(d) { return d3.scale.category20()(d.group)}', isPyData=False)
    self.addAttr('nodeExtras', 'function(node) { node.append("text").attr("dx", 12).attr("dy", ".35em").text(function(d) { return d.name }); }', isPyData=False)

