#! /usr/bin/env python
# encoding: utf-8

import sqlite3

class DocDefDB:
	'''
	Class defining a connection to the sqlite db
	where some rules of definition are set'''
	def __init__(self, file):
		self.docDefDB=sqlite3.connect(file)
	def authorizedFields (self):
		c = self.docDefDB.cursor()
		c.execute("select * from doc_fields")
		tmp = c.fetchall()
		authorizedFields = {}
		for i in tmp:
			authorizedFields[i[0]] = i[1]
		del c,tmp
		return authorizedFields
	def fieldArgs (self):
		c = self.docDefDB.cursor()
		c.execute("select * from doc_field_args")
		tmp = c.fetchall()
		fieldArgs = {}
		for i in tmp:
			if i[0] in fieldArgs.keys():
				fieldArgs[i[0]].append(i[1])
			else:
				fieldArgs[i[0]] = [i[1]]
		del tmp,c
		return fieldArgs

