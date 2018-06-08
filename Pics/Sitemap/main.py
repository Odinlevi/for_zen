import os
import json
import crawler
import sys
import ssl
import urllib.request
from urllib.parse import quote
from PIL import Image, ImageOps
from bs4 import BeautifulSoup
import numpy
ssl.match_hostname = lambda cert, hostname: True

BLOCK_SIZE = 20
TRESHOLD = 60
config = {}

def load_image(selfy):
    img = Image.open(selfy)
    small = img.resize( (BLOCK_SIZE, BLOCK_SIZE),
    Image.BILINEAR )
    t_data = numpy.array(
        [sum(list(x)) for x in small.getdata()]
    )
    del img, small
    return t_data

def mul(self, other):
    self = load_image(self)
    other = load_image(other)
    return sum(1 for x in self - other if abs(x) > TRESHOLD)

def load_dir(dirname):
    imagenames = []
    for filename in os.listdir(dirname):
        if filename.endswith('.jpg'):
            imagenames += [filename]
    return(imagenames)
def comparer(dir1, dir2):
    equals = []
    for img1 in load_dir(dir1):
        for img2 in load_dir(dir2):
            if mul(dir1+'/'+img1, dir2+'/'+img2) < 220:
                equals += [img1+' and '+img2+', dist = '+str(mul(dir1+'/'+img1, dir2+'/'+img2))+' ']
    return(equals)

def check_cyrill(href):
    try:
        href.encode('ascii')
        return(1)
    except:
        return(0)
def http(href):
    try:
        check = urllib.request.urlopen('http://'+href)
        return(1)
    except:
        try:
            check = urllib.request.urlopen('https://'+href)
            return(0)
        except:
            return(-1)
def change_st_part(hrefv1):
    #hrefv1 = 'кфс-кольцова-центр-регион.рф'
    href = hrefv1
    if check_cyrill(href) == 0:
        parts = href.split('.')
        href = ''
        for part in parts:
            href += str(part.encode('punycode')).replace("b'", "xn--").replace("'", ".")
        href = href[:-1]
    if http(href):
        href = 'http://'+href
    elif http(href) == 0:
        href = 'https://'+href
    else:
        print('BAD URL: '+href)
        href = '-1'
    return (href)

try:
    file = open('hrefs.txt', 'r', encoding="utf-8")
    hrefs_list = file.read().replace('\ufeff', '').replace('\n\n\n', '').replace('\n\n', '').split('\n')
    file.close
except:
    print('The reference database was not added / was deleted, YOU HAVE TO ADD A NEW ONE! (Or there is a trouble with file hrefs.txt)')
    sys.exit()

#href_list = {'http://kfs-ok.com', 'http://kfskorektor.cz', 'http://кфс-кольцова-центр-регион.рф'}
x = 1

for href in hrefs_list:
    sitemap_name = 'Sitemaps_Folder/sitemap'+str(x)+'.xml'
    x+=1
    #href = 'центр-регион-кфскольцова.рф'
    hrefv1 = href
    href = change_st_part(href)
    print(href)
    dict_arg = {'skipext': [], 'parserobots': False, 'debug': False, 'verbose': False, 'output': sitemap_name, 'exclude': [], 'drop': [], 'report': False, 'images': False, 'config': None, 'domain': href}

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
    #print('Sitemaps are made!')
    file = open(sitemap_name, 'r', encoding="utf-8")
    fold = 'Service_Folder/'
    soup = BeautifulSoup(file, "html.parser")
    locs = soup.find_all("loc")
    for loc in locs:
        loc = loc.get_text()
        xx = 0
        #print(loc)
        try:
            page = urllib.request.urlopen(loc)
        except:
            print('Page 404: '+loc)
            continue
        sup = BeautifulSoup(page.read(), "html.parser")
        img_hrefs = sup.findAll('img')
        for img_href in img_hrefs:
            xx += 1
            img_href = '{0}'.format(quote(img_href.get('src'), '?/%=:;'))
            try:
                resource = urllib.request.urlopen(img_href)
            except:
                try:
                    img_href = href+'/'+img_href
                    resource = urllib.request.urlopen(img_href)
                except:
                    try:
                        if loc[-1] == '/':
                            img_href = loc+img_href
                        else:
                            img_href = loc+'/'+img_href
                        resource = urllib.request.urlopen(img_href)
                    except:
                        print('Bad image: '+img_href)
                    continue
                
            #print(img_href)
            img_name = loc+str(xx)+".jpg"
            img_name = img_name.replace('/', '')
            img_name = fold+img_name
            out = open(img_name, 'wb') # 'imgg.jpg' -> page url
            out.write(resource.read())
            out.close()
            img = Image.open(img_name)
            img = img.convert("RGB")
            w, h = img.size
            hh = 300 * h / w
            avatar_size = (300, int(hh))

            method = Image.NEAREST if img.size == avatar_size else Image.ANTIALIAS
            formatted_img = ImageOps.fit(img, avatar_size, method = method, centering = (1.0,0.0))
            formatted_img.save(img_name)

print(comparer('Folder_For_Pics_IN_JPG', 'Service_Folder'))