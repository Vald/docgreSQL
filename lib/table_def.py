#! /usr/bin/env python
# encoding: utf-8
# imports
import sys, os, string, re, codecs


# TODO : gérer les champs qui peuvent être plusieurs ... (genre field :)  )
# TODO : ne pas traiter les repertoires et fichiers cachés
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
		# list of all subdirectories
		paths = [root+'/'+ x for x in os.listdir(root) if os.path.isdir(root+'/'+x)]
		# list of all files
		files = [p+'/'+x for p in paths for x in os.listdir(p)]
		
		# read every tables from every files
		self.tablesDoc = {}
		for file in files:
			self.tablesDoc = self.readTables(file, self.tablesDoc)
		# nécessité de vérifier l'unicité des tables ?
		# interpretaion de la doc
		# complétion des inheritances


	def readTables(self, file, tables):
		"""
		Extract all tables from file and add them to tables
		"""
		if not os.path.exists(file):
			raise NameError("File '"+file+"' doesn't exist.")
		in_doc=False		# lors du parcours du fichier, permet de savoir si le curseur
					# est dans une partie de documentation ou de requete.
		table={}
		query=""
		file=codecs.open(file,'r','utf8')
		for line in file:
			# si on est au début d'une partie de doc on sauve la derniere table lue
			if re.match("--#", line) is not None and not in_doc:
				if 'name' in table.keys():
					table['query']=query
					tables[table['name']]=table
				in_doc=True
				table={}
				query=""
			# si on est au début d'un espace de requete
			elif re.match("--#", line) is None and in_doc:
				in_doc=False
			# recherche du champ name dans la doc
			if in_doc:
				if self.isFirstLineOfField(line):
					field_name=self.getNameOfField(line)
					table[field_name]=self.getValueOfField(line)
				else:
					tmp=table[field_name]
					table[field_name]=tmp+'\n'+self.getValueOfField(line)
			# lecture de la requete
			else:
				query=query+'\n'+line

		# integration de la derniere table
		if 'name' in table.keys():
			table['query']=query
			tables[table['name']]=table
		file.close()
		return tables

	def isFirstLineOfField (self, line):
		return re.match(u"--# @", line) is not None
	def getNameOfField (self, line):
		return line.replace(u"--# @", u"").split()[0]
	def getValueOfField (self, line):
		return re.sub(u"--# @.*? ", '', line)


class TableDoc:
	"""
	Classe utilisée pour la représentation des définitions de table\n\
	\n\
	--> contient tous les attributs possibles (avec éventuellement des valeurs None) :\n\
	titre, description, dependances, requête"""
	
	def __init__(self, titre,description,dependances,champs,requete):
		self.titre=titre		# chaine de caracteres, titre dans l'aide
		self.description=description	# chaine de caracteres, descriptions detaillees
		self.dependances=dependances	# dictionnaire contenant en clé les noms des namespace
						# et en valeur une liste avec les tables
		self.champs=champs		# dictionnaire, cle=nom, valeur=type (?)
		self.requete=requete
	
