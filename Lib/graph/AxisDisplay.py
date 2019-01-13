#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

DISPLAYS = {'TIMESTAMP': {'tickFormat': "function(d) { return d3.time.format('%%x')(new Date(d)) }"},
       'FLOAT': {'tickFormat': "function(d) { return d3.format(',.%(digits)sf')(d) }"},
       'K': {'tickFormat': "function(d) { return d3.format(',.%(digits)sf')(d / 1000) + 'K' }", 'labelString': '1K = 1000'},
       'M': {'tickFormat': "function(d) { return d3.format(',.%(digits)sf')(d / 1000000) + 'Mio'}", 'labelString': '1Mio = 1000000'},
       'G': {'tickFormat': "function(d) { return d3.format(',.%(digits)sf')(d / 1000000000) + 'G'}", 'labelString': '1G = 1000000000'},
       '%': {'tickFormat': "function(d) { return d3.format(',.%(digits)s%')(d) }"},
       'INT': {'tickFormat': "function(d) { return d3.format(',')(d) }"},
       'MONTH': {'tickValues': "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]",
                 'tickFormat': 'function(d){ return months[d] }'},
       'DAYS': {'tickValues': "[0, 1, 2, 3, 4, 5, 6]",
                'tickFormat': 'function(d){ return months[d] }'},
}