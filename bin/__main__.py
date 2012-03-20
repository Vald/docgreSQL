#! /usr/bin/env python
# encoding: utf-8

import sys, os, string, re, codecs

sys.path.append(os.getcwd()+"/lib/")
#from docgreSQL import DocGreSQL
from dataBase import *

docgreSQL=DocGreSQL(os.getcwd())
root=os.getcwd()+"/test/"
test=DataBase(root, docgreSQL)

self=test
file=os.getcwd()+"/test/commune.sql"
tablesDoc=[]
self.tablesDoc = self.readTables(file, tablesDoc)
description = self.tablesDoc[0]
doc = description['doc']
