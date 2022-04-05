# import cv2
import os, shutil
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from PIL import Image, ImageFont, ImageDraw, ImageOps
import matplotlib.pyplot as plt
import pickle
import codecs
import arabic_reshaper
from bidi.algorithm import get_display


path_valid = './final_dataset'

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
        ann = f.read().splitlines()

    for i in ann:
        splits = i.split(',')
        print(i)

        # d.polygon([int(cor) for cor in i.split(',')[:8]], outline=(100, 100, 40), )
        d.line([int(cor) for cor in i.split(',')[:8]] + [int(cor) for cor in i.split(',')[:2]], fill="red",
               width=min(im.size[0], im.size[1]) // 250)
        txt = i.split(',')[-1]

        reshaped_text = arabic_reshaper.reshape(txt)  # correct its shape
        bidi_text = get_display(reshaped_text)  # correct its direction

        font = ImageFont.truetype('384.Font.Farsi/KoodakB.ttf',
                                  im.size[1] // 15, encoding='unic')

        d.text((int(splits[2]), int(splits[3]) + im.size[0]//20), bidi_text, font=font, fill=255)


    figure(figsize=(8, 6), dpi=80)
    plt.imshow(im)
    plt.show()

    if cntr >= 3:
        break
