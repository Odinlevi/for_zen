import urllib.request
from urllib.parse import quote
#from PIL import Image, ImageOps
import ssl
ssl.match_hostname = lambda cert, hostname: True

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
    return (href)
print(change_st_part('центр-регион-кфскольцова.рф'))
'''
resource = urllib.request.urlopen(img_href)
out = open('imgg.jpg', 'wb') # 'imgg.jpg' -> page url
out.write(resource.read())
out.close()
img = Image.open('imgg.jpg')
img = img.convert("RGB")
w, h = img.size
hh = 300 * h / w
avatar_size = (300, int(hh))

method = Image.NEAREST if img.size == avatar_size else Image.ANTIALIAS
formatted_img = ImageOps.fit(img, avatar_size, method = method, centering = (1.0,0.0))
formatted_img.save("imgg.jpg")
'''
