#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


from ares.Lib.AresImports import requires
import traceback


class AresNeo4j(object):
  """
  :category: Connector
  :rubric: PY
  :type: Class
  :dsc:

  :link Documentation: https://neo4j.com/developer/python/
  https://community.neo4j.com/?_ga=2.69585106.394662973.1539480121-615400289.1539480121
  """

  ALIAS = 'NEO4J'
  _extPackages = [("neo4j", 'neo4j-driver')]

  def __init__(self, host=None, port=None, usr=None, pwd=None):
    self.pkgs = {}
    if self._extPackages is not None:
      for name, package in self._extPackages:
        self.pkgs[name] = requires(name, reason='Missing Package', install=package, autoImport=True, sourceScript=__file__)
    self.driver = self.pkgs["neo4j"].GraphDatabase.driver('bolt://%s:%s' % (host, port), auth=(usr, pwd))
    self.query = []


  def raw_query(self, query):
    try:
      with self.driver.session() as session:
        for rec in session.run(query):
          yield rec

    except:
      print(traceback.format_exc())
      raise StopIteration


  def create(self):
    self.query.append('CREATE')
    return self


  def match(self):
    self.query.append('MATCH')
    return self


  def foreach(self, conditions):
    """

    """
    raise NotImplemented


  def where(self, condition):
    return self


  def delete(self, node_names, detach=False):

    if detach:
      self.query.append('DETACH')
    self.query.append('DELETE %s' % ','.join(node_names))
    try:
      with self.driver.session() as session:
        session.run(self.compose(self.query))
        self.query = []
        return True

    except:
      print(traceback.format_exc())
      self.query = []
      return False


  def retreive(self, names):
    self.query.append('RETURN')
    self.query.append(','.join(names))
    return self


  def clear(self):
    """
    :dsc: Clears all nodes and edges from the Database
    """
    return self.match().node('n').delete(['n'], detach=True)


  def node(self, name='', labels=None, attr=None):
    """
    :dsc: adds the node patern to the query
    """
    if not labels:
      labels = []
    else:
      labels[0] = ':%s' % labels[0]
    if not attr:
      attr = ''
    else:
      tmp_attr_list = []
      for attr_key, attr_value in attr.items():
        tmp_attr_list.append('%s: "%s"' % (attr_key, attr_value))
      attr = '{%s}' % ','.join(tmp_attr_list)
    self.query.append("(%s%s %s)" % (name, ':'.join(labels), attr))
    return self


  def link(self, labels='', attr=None, direction="from"):
    """
    :dsc: adds the edge definition to the query
    """
    if direction == 'from':
      self.query.append('-[%s]->' % labels)
    else:
      self.query.append('<-[%s]-' % labels)
    return self


  def alias(self, aliases):
    """
    :dsc: defines a set of aliases that will appear as WITH a, b, c, d as count(id)
    The aliases argument will be defined as follows: ['a', 'b', 'c', {'d': 'count(id)'}]
    """
    self.query.append('WITH')
    tmp_query = []
    for expression in aliases:
      if isinstance(expression, dict):
        for expr, alias in expression.items():
          tmp_query.append('%s as %s' % (expr, alias))
      else:
        tmp_query.append(expression)
    self.query.append(', '.join(tmp_query))
    return self


  def compose(self, query):
    """
    :dsc: Simply joins the query clauses all together
    """
    return ' '.join(query)


  def execute(self):
    try:
      with self.driver.session() as session:
        for rec in session.run(self.compose(self.query)):
          yield rec

    except:
      print(traceback.format_exc())
      raise StopIteration



