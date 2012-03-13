#! /usr/bin/env python
# encoding: utf-8

import sys, os, string, re, codecs, sqlite3

# TODO : créer un .log pour que quand ça plante on puisse suivre ce qui se passe

class DataBase:
	"""
	Class containing TableDoc describing every tables of the database.
	"""
	def __init__(self,root):
		"""
		root is the path to the root of the documenting tree
		"""
		if not os.path.isdir(root):
			raise NameError(root+" is not defined")

		# list of all subdirectories from root.
		# TODO : remove hidden subdirectories

		paths = [root+'/'+ x for x in os.listdir(root) if os.path.isdir(root+'/'+x)]
		paths.append(root)

		# list of all files defined in the subtree from root
		# only sql files are kept

		files = [p+'/'+x for p in paths for x in os.listdir(p)]
		files = [file for file in files if re.search('\.sql$', file) is not None]
		
		# read every tables from every files

		self.tablesDoc = []
		for file in files:
			self.tablesDoc=self.readTables(file, self.tablesDoc)

		# format tablesDoc accordingly with what is in tablesDoc
		self.tablesDoc = [TableDoc(description) for in self.tablesDoc]

		# complétion des inheritances mais avant de faire ça, il faudra faire du parsing de requete...

	def readTables(self, file, tables):
		"""
		Extract all tables from file and add them to tables
		"""
		if not os.path.exists(file):
			raise NameError("File '"+file+"' doesn't exist.")
		in_doc	= False	# Boolean used to know if the line being read is in a documenting section or not
		doc	= ""	# used to store the documentation of the table
		query	= ""	# used to store the query definition of the table
		file	= codecs.open(file,'r','utf8')
		for line in file:
			# si on est au début d'une partie de doc on sauve la derniere table lue
			if re.match("--#", line) is not None and not in_doc:
				if len(query) > 0:
					tables.append({'doc':doc,'query':query})
				in_doc	= True
				doc	= ""
				query	= ""
			# si on est au début d'un espace de requete
			elif re.match("--#", line) is None and in_doc:
				in_doc	= False
			# recherche du champ name dans la doc
			if in_doc:
				doc=doc+line
			else:
				query=query+line
		# integration de la derniere table
		if len(query) > 0:
			tables.append({'doc':doc,'query':query})
		file.close()
		return tables

class TableDoc:
	"""
	Class used for the representation of tables (doc if exist and query)
	"""
	
	def __init__(self, description):
		doc	= self.parseDoc(description['doc'])
		query	= self.parseQuery(description['query'])

		# when parsing query will be implemented, don't
		# forget to check coherence between doc and query

	def parseDoc(self, doc):
		# if doc is empty, welle there's nothing to do
		if len(doc) == 0:
			return ''

		# A well structured doc string may have "\n",
		# a field may be constituted of several lines begining with "--#".
		# Let suppress them.
		# Every field of the documentation should start with "--# @", so 
		# the string doc is split on this string

		doc = [re.sub("--#", "", x) for x in doc.replace('\n', '').split('--# @')]
		doc = [x for x in doc if x != ""]

		# transforming each doc's field in dictionnary (the first part of the string,
		# before the first " ", should be the name)

		doc = [{'name':x,'value':y} for (x,y) in [z.split(' ', 1) for z in doc]]
		
		# for each 'name' defined, values are grouped



		# for each 'name', the possibility to use it is check
		# and the coherence between real number of values and 
		# authorized number of values is also checked (error or warn ans continu ?)
		# Those informations are given in the docDefDB.sql

		docDefDB= sqlite3.connect(postdoc.docDefDB)
		c	= docDefDB.cursor()
		c.execute("select * from doc_fields")
		authorizedFields = c.fetchall()

		# for each field, the number of args is checked

		# finally the 'doc' structure is returned
		
	def parseQuery(self, query):
		# will need a sqlparser ...
		return query
