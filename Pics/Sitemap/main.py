import os

import json

import crawler
config = {}

dict_arg = {'skipext': [], 'parserobots': False, 'debug': False, 'verbose': False, 'output': 'sitemap.xml', 'exclude': [], 'drop': [], 'report': False, 'images': False, 'config': None, 'domain': 'http://kfskorektor.cz'}
for argument in config:
	if argument in dict_arg:
		if type(dict_arg[argument]).__name__ == 'list':
			dict_arg[argument].extend(config[argument])
		elif type(dict_arg[argument]).__name__ == 'bool':
			if dict_arg[argument]:
				dict_arg[argument] = True
			else:
				dict_arg[argument] = config[argument]
		else:
			dict_arg[argument] = config[argument]
del(dict_arg['config'])

crawl = crawler.Crawler(**dict_arg)
crawl.run()

