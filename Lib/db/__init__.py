#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This will trigger the automatic database update of the below SqlTables when the app will start
# Any new table will be automatically added to the database

from ares.Lib.db import SqlTableAres
from ares.Lib.db import SqlTableDbReports
from ares.Lib.db import SqlTableFiles
from ares.Lib.db import SqlTableQuestions
from ares.Lib.db import SqlTableDocs
from ares.Lib.db import SqlTableSecurity
from ares.Lib.db import SqlTablesIncidents