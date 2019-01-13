#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


class OrderedSet(list):
  """
  :category: Sets
  :rubric: PY
  :type: System
  :dsc:
    Create a ordered set object
  """

  def __init__(self):
    super(OrderedSet, self).__init__()

  def add(self, key):
    """

    :param key:
    :return:
    """
    if key not in self:
      self.append(key)
