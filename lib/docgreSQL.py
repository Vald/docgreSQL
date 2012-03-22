#! /usr/bin/env python
# encoding: utf-8

import ConfigParser, sys

class DocGreSQL:
	"""
	This the main class of the program.

	It defines links between the program and the reste of the world
	such as defined in the setup.cfg at the root of the project.
	"""
	def __init__(self, root):
		self.root=root
		config=ConfigParser.SafeConfigParser()
		config.read('setup.cfg')
		self.docDefDB=config.get('files', 'docDefDB').replace('./', self.root+'/', 1)


if __name__ == "__main__":
	docgreSQL=DocGreSQL(sys.argv[1])
	# later may define an interactive shell ...
