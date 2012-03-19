#! /usr/bin/env python
# encoding: utf-8

import sys, os, string, re, codecs, sqlite3

# TODO : créer un .log pour que quand ça plante on puisse suivre ce qui se passe

class DataBase:
	"""
	Class containing TableDoc describing every tables of the database.
	"""
	def __init__(self,root, docgreSQL):
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
		self.tablesDoc = [TableDoc(description, docgreSQL) for description in self.tablesDoc]

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
	
	def __init__(self, description, docgreSQL):
		self.doc	= self.parseDoc(description['doc'], docgreSQL)
		self.query	= self.parseQuery(description['query'])

		# check consistency : are all dependencies available ?

		# when parsing query will be implemented, don't
		# forget to check coherence between doc and query

	def parseDoc(self, doc, docgreSQL):
		# if doc is empty, welle there's nothing to do
		if len(doc) == 0:
			return ''

		docDefDB = DocDefDB (docgreSQL.docDefDB)

		# A well structured doc string may have "\n",
		# a field may be constituted of several lines begining with "--#".
		# Let suppress them.
		# Every field of the documentation should start with "--# @", so 
		# the string doc is split on this string

		doc = [re.sub("--#", "", x) for x in doc.replace('\n', '').split('--# @')]
		doc = [x for x in doc if x != ""]

		# transforming each doc's field in dictionnary (the first part of the string,
		# before the first " ", should be the name)

		doc = {'key':[x for (x,y) in [z.split(' ', 1) for z in doc]] ,
				'value':[y for  (x,y) in [z.split(' ', 1) for z in doc]]}

		# for each 'name' defined, values are grouped

		definedFields = set (doc['key'])
		for df in definedFields :
			doc[df] = [doc['value'][i] for i in range(len(doc['key'])) if doc['key'][i]==df]

		del doc['key']
		del doc['value']
		del definedFields

		# for each 'name', the possibility to use it is check
		# and the coherence between real number of values and 
		# authorized number of values is also checked (error or warn ans continu ?)
		# Those informations are given in the docDefDB.sql

		authorizedFields = docDefDB.authorizedFields()

		for f in doc.keys():
			if f not in authorizedFields.keys():
				print f+' is not an authorized field name and so will be ignored.'
				del doc[f]
			elif len(doc[f]) > 1 and authorizedFields[f] == u'False':
				print 'Only one value is required for the "'+f+'" field. "'+doc[f][0]+'" is kept.'
				doc[f] = doc[f][0]

		del authorizedFields

		# for each field, the number of args is checked
		# the 'doc' structure is created at the same time

		fieldArgs = docDefDB.fieldArgs()

		for f in doc.keys():
			# number of fields
			nf = len(fieldArgs[f])
			for ff in range(len(doc[f])):
				if nf > 1:
					doc[f][ff] = doc[f][ff].split(' ', nf-1)
					if len (doc[f][ff]) != nf:
						raise NameError('One field is missing for '+' '.join(doc[f][ff]))
				else:
					doc[f][ff] = [doc[f][ff]]

		del nf
		return doc

		
	def parseQuery(self, query):
		# will need a sqlparser ...
		return query
	
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

