#! /usr/bin/env python
# encoding: utf-8
# imports
import sys, os, string, re, codecs
sys.path.append("/home/vladislav/src/docgreSQL/lib/")
from docgreSQL import DocGreSQL
from table_def import *

docgreSQL=DocGreSQL("/home/vladislav/src/docgreSQL/")
root="/home/vladislav/src/docgreSQL/test/"
test=DataBase(root)

self=test
file="/home/vladislav/src/docgreSQL/test/commune.sql"
tables={}
self.readTables(file, tables)
