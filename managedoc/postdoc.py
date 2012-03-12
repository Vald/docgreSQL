#! /usr/bin/env python
# encoding: utf-8

import ConfigParser, sys

class PostDoc:
	"""
	This the main class of the program.

	It defines links between the program and the reste of the world
	such as defined in the postdoc.ini at the root of the project.
	"""
	def __init__(self, root):
		self.root=root
		config=ConfigParser.SafeConfigParser()
		config.read('postdoc.ini')
		self.docDefDB=config.get('files', 'docDefDB').replace('./', self.root, 1)


if __name__ == "__main__":
	postdoc=PostDoc(sys.argv[1])
	# later may define an interactive shell ...
