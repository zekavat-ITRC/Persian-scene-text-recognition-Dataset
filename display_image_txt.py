# import cv2
import os, shutil
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from PIL import Image, ImageFont, ImageDraw, ImageOps
import matplotlib.pyplot as plt
# from itertools import chain
# import matplotlib.font_manager
import pickle
import codecs
import arabic_reshaper
from bidi.algorithm import get_display
# from colorpair import getColorText


imgs = ['aquarium_24_0.jpg', 'ballet_26_0.jpg', 'bay+area_68_0.jpg' ,
        'birds_135_0.jpg', 'cambridge_32_0.jpg', 'cambridge_63_0.jpg', 'city_0_0.jpg',
        'coffee_26_0.jpg', 'coffee_77_0.jpg', 'concert_140_0.jpg', 'concert_55_0.jpg',
        'cows_86_0.jpg', 'delhi_81_0.jpg', 'desert_4_0.jpg', 'dog_55_0.jpg', 'empty+street_43_0.jpg' ,
        'farm_28_0.jpg', 'flowers_30_0.jpg', 'fruits_32_0.jpg', 'hedge_48_0.jpg',
        'horse_10_0.jpg', 'house+cat_50_0.jpg', 'kathmandu_22_0.jpg', 'kerala_58_0.jpg',
        'kite_10_0.jpg', 'leopard_48_0.jpg', 'mesh_60_0.jpg']

# path = os.path.join(r'D:\ITRC\sw\valid_dataset\valid_dataset', 'goods')
# # if not os.path.exists(path):
# #     os.mkdir(path)
# for im in imgs:
#     # shutil.copy(os.path.join(r'D:\ITRC\sw\valid_dataset\valid_dataset', im), path)
#     shutil.copy(os.path.join(r'D:\ITRC\sw\eval\eval', 'res_'+im+'.txt'), path)
# exit()


























path_eval = r'D:\ITRC\sw\valid_dataset\valid_dataset\goods'  #  r'D:\ITRC\sw\eval\eval'
path_valid = r'D:\ITRC\sw\valid_dataset\valid_dataset\goods'     # r'D:\ITRC\sw\valid_dataset\valid_dataset'

cntr = 0
for img in os.listdir(path_valid):
    if not img.lower().endswith(('.jpg',)):
        continue
    print(img)
    cntr += 1
    print(cntr)
    # if cntr < 268:
    #     continue

    im = Image.open(os.path.join(path_valid, img))
    if im.mode == 'L':
        print(im.mode)
        im = im.convert('RGB')
    d = ImageDraw.Draw(im)

    with codecs.open(os.path.join(path_eval, 'res_'+img+'.txt'), 'r', "utf-8") as f:
        ann = f.read().splitlines()

    for i in ann:
        splits = i.split(',')
        print(i)
        # print(i.split(',')[:-1])
        # print([max(1, int(cor)) for cor in i.split(',')[:8]])
        d.polygon([int(cor) for cor in i.split(',')[:8]], outline=(100, 100, 40), )
        txt = i.split(',')[-1]
        # print(txt)
        # txt = ' "#&;=>?@_`\|~ ¼é،ءآأؤخىيًٌٍَُِّْپچژکگ‌‍‎‏–…'
        reshaped_text = arabic_reshaper.reshape(txt)  # correct its shape
        bidi_text = get_display(reshaped_text)  # correct its direction
        # print(bidi_text)
        font = ImageFont.truetype(r'D:\uni\skills\machine learning\second project\synthtext\384.Font.Farsi\koodakB.ttf',
                                  im.size[1] // 15, encoding='unic')

        d.text((int(splits[2]), int(splits[3]) + im.size[0]//20), bidi_text, font=font, fill=255)
        # d.text((0,0), bidi_text, font=font, fill=255)

        # break
    plt.figure(1)
    plt.imshow(im)
    plt.show()
    # plt.close(1)
    a = input('input')
    if not a == 'y':
        plt.close('all')
    else:
        print(img)

# im.save('bbox.jpg')
