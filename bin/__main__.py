#! /usr/bin/env python
# encoding: utf-8
# imports
import sys, os, string, re, codecs
sys.path.append("/home/vladislav/src/postdoc/lib/")
from postdoc import PostDoc
from table_def import *

postdoc=PostDoc("/home/vladislav/src/postdoc/")
root="/home/vladislav/src/postdoc/test/"
test=DataBase(root)

self=test
file="/home/vladislav/src/postdoc/test/commune.sql"
tables={}
self.readTables(file, tables)
