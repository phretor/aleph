#!/usr/bin/env python
import os
import sys

# Fix path for importing modules
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
sys.path.append(PACKAGE_DIR)

from aleph.webui.models import *
from aleph.datastore import es

try:
    db.reflect()
    db.drop_all()
    es.destroy()

    print "Database destroyed successfully"
except Exception, e:
    print "Error while destroying the DB: %s" % e
