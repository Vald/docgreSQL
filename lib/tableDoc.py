#! /usr/bin/env python
# encoding: utf-8

import string, re, sqlparse
from docgreSQL import *
from docDefDB import *

class TableDoc:
	"""
	Class used for the representation of tables (doc if exist and query)

	Slots:
	'doc' is a dictionnary containing all documenting fieldsin the format :
		nameOfField : <list>
		where <list> contains one or more elements (depending on what is defined
		in docDefDB). Each element is (also) a list containing
		the parameters used for the documentation of the field.
	'query' is a string containing the query(ies) used to build the table.
		Later, it will be a structure containing (a) parsed query(ies).
	"""
	
	def __init__(self, description, docgreSQL):
		self.doc	= self.parseDoc(description['doc'], docgreSQL)
		self.query	= self.parseQuery(description['query'])

		# when parsing query will be implemented, don't
		# forget to check coherence between doc and query

	def __str__(self):
		pretty=''
		for field in self.doc.keys():
			pretty=pretty+(unicode(field)+' :\n')
			pretty=pretty+'\n'.join(['\t'+' - '.join(x) for x in self.doc[field]])+'\n'
		pretty=pretty+'\n'
		return unicode(pretty).encode('utf-8')

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
		query=query.replace('\n', '')
		queries = sqlparse.split(query)
		qParsed = [sqlparse.parse(x) for x in queries]
		return query
	

