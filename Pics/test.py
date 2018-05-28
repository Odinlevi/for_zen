import urllib.request
from PIL import Image, ImageOps
import ssl
ssl.match_hostname = lambda cert, hostname: True
img_href = 'https:///кфс-кольцова-центр-регион.рфwp-content/uploads/kfs-kolcova-centr-region-sait.png'.encode('idna')
print(img_href)
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
