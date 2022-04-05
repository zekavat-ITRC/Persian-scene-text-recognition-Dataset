import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
import codecs
import arabic_reshaper
from bidi.algorithm import get_display
from matplotlib.pyplot import figure

import argparse
parser = argparse.ArgumentParser(description='Process some integers.')

# Adding Arguments
parser.add_argument('--path', type=str, default='./word_final_dataset',
                    help='path to folder containing images and annotation files')

args = parser.parse_args()

path_valid = args.path

cntr = 0
for img in os.listdir(path_valid):
    if not img.lower().endswith(('.jpg',)):
        continue
    print(img)
    cntr += 1
    print(cntr)


    im = Image.open(os.path.join(path_valid, img))
    if im.mode == 'L':
        print(im.mode)
        im = im.convert('RGB')
    d = ImageDraw.Draw(im)

    with codecs.open(os.path.join(path_valid, img.split('.')[0]+'.txt'), 'r', "utf-8") as f:
        ann = f.read().splitlines()[0]

    txt = ann.split(',')
    print(txt)


    figure(figsize=(8, 6), dpi=80)
    plt.imshow(im)
    plt.show()

    if cntr >= 3:
        break
