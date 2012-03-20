#! /usr/bin/env python
# encoding: utf-8

import sys, os, string, re, codecs, sqlparse

sys.path.append(os.getcwd()+"/lib/")
#from docgreSQL import DocGreSQL
from dataBase import *

docgreSQL=DocGreSQL(os.getcwd())
root=os.getcwd()+"/test/"
test=DataBase(root, docgreSQL)

query = test.tablesDoc[0].query


