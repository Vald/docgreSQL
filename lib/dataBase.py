#! /usr/bin/env python
# encoding: utf-8

import sys, os, string, re, codecs
from tableDoc import *

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


