from __future__ import print_function, division, absolute_import
from PIL import Image
import numpy
import os

BLOCK_SIZE = 20
TRESHOLD = 60

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
print(comparer('qwe1', 'qwe2'))
