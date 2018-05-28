import os
import json
import crawler
import sys
'''
try:
    file = open('hrefs.txt', 'r', encoding="utf-8")
    hrefs_list = file.read().replace('\ufeff', '').replace('\n\n\n', '').replace('\n\n', '').split('\n')
    file.close
except:
    print('The reference database was not added / was deleted, YOU HAVE TO ADD A NEW ONE! (Or there is a trouble with file hrefs.txt)')
    sys.exit()
config = {}
#href_list = {'http://kfs-ok.com', 'http://kfskorektor.cz', 'http://кфс-кольцова-центр-регион.рф'}
x = '1'
for href in hrefs_list:
    if href.find('https') == -1:
        href = 'http://'+href
    print(href)'''
config = {}
#sitemap_name = 'sitemap'+x+'.xml'
#x=str(int(x)+1)
dict_arg = {'skipext': [], 'parserobots': False, 'debug': False, 'verbose': False, 'output': 'sitemap.xml', 'exclude': [], 'drop': [], 'report': False, 'images': False, 'config': None, 'domain': 'http://центр-регион-кфскольцова.рф'}

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

file = open(sitemap_name, 'r', encoding="utf-8")


    
