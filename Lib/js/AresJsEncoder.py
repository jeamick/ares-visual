#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès


import json
import datetime
from ares.Lib.AresImports import requires

# Will automatically add the external library to be able to use this module
ares_pandas = requires("pandas", reason='Missing Package', install='pandas', autoImport=True, sourceScript=__file__)
ares_numpy = requires("numpy", reason='Missing Package', install='numpy', autoImport=True, sourceScript=__file__)


class AresEncoder(json.JSONEncoder):
  """
  :category: Encoding
  :rubric: PY / JS
  :type: system
  :dsc:
    Class in charge of encoding the data to be written on the Javascript side.
    In most of the function the simple json module is used but this module is there to encode more complex object
    frenquently coming from Pandas
  :return: A serialisable item
  """

  def default(self, obj):
    if isinstance(obj, ares_pandas.core.series.Series):
      return list(obj)

    if isinstance(obj, (ares_numpy.int_, ares_numpy.intc, ares_numpy.intp, ares_numpy.int8, ares_numpy.int16, ares_numpy.int32, ares_numpy.int64, ares_numpy.uint8,
                        ares_numpy.uint16, ares_numpy.uint32, ares_numpy.uint64, ares_numpy.integer)):
      return int(obj)
    elif isinstance(obj, (ares_numpy.float_, ares_numpy.float16, ares_numpy.float32, ares_numpy.float64, ares_numpy.floating)):
      return float(obj)
    elif isinstance(obj, ares_numpy.ndarray):
      return obj.tolist()
    elif isinstance(obj, datetime.datetime):
      if isinstance(obj, type(ares_pandas.NaT) ):
        return ''

      return obj.strftime('%Y-%m-%d')
    else: return super(AresEncoder, self).default(obj)

