import cv2
import os
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
import _pickle as cp
from PIL import Image, ImageFont, ImageDraw, ImageOps
import matplotlib.pyplot as plt
import codecs
from colorpair import getColorText

import matplotlib.font_manager

from poisson_reconstruct import blit_images

if not os.path.exists('./word_valid_dataset'):
    os.mkdir('./word_valid_dataset')
created = os.listdir('./word_valid_dataset')
created = ['_'.join(i.split('.')[0].split('_')[:-1]) for i in created if i.split('.')[-1] == 'jpg']  # if not i.split('.')[-1] == 'txt']
if len(created) >= 2500:
    exit()

win_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

with open('font_finall.txt', 'r') as f:
    fonts = f.read().splitlines()
f.close()


with codecs.open('codec_mine2.txt', 'r', 'utf-8') as f:
    allowed_chars = f.readline()
f.close()
print(allowed_chars)

fonts_ok = []
for f in fonts:
    try:
        f = os.path.join('./384.Font.Farsi', f)
        tmpFont = ImageFont.truetype(f, 30, encoding='unic')
        fonts_ok.append(f)
    except:
        tmp = 0
print(len(fonts_ok))
fonts = fonts_ok

with codecs.open('newsgroup.txt', 'r', "utf-8") as f:
    all_text = []
    for line in f:
        all_text.append(line.strip())
print(len(all_text))



def getRndTxt():
    news = all_text[np.random.randint(0, len(all_text))]
    while news == [] or len(news.split()) < 5:
        news = all_text[np.random.randint(0, len(all_text))]


    num_word = 1  # np.random.randint(2, 6)
    news_words = news.split()
    try:
        ithWord = np.random.randint(0, len(news_words)-5)
    except:
        print(news)
        exit()
    n_con_words = ' '.join(news.split()[ithWord:ithWord+num_word])
    return n_con_words

imfolder_path = 'bg_img'


with open('imnames.cp', 'rb') as f:
  filtered_imnames = set(cp.load(f))
print(len(filtered_imnames))

images = os.listdir(imfolder_path)
os.makedirs('./word_valid_dataset', exist_ok=True)
created = os.listdir('./word_valid_dataset')
created = ['_'.join(i.split('.')[0].split('_')[:-1]) for i in created if i.split('.')[-1] == 'txt']
format = [".jpg", ".png", ".jpeg"]
num_using_img = 1
print('start...')
for im_name in images:
    files = os.listdir('./word_valid_dataset')
    imgs_valid = ['_'.join(i.split('.')[0].split('_')[:-1]) for i in files if i.split('.')[-1] == 'jpg']  # if not i.split('.')[-1] == 'txt']
    # print(len(imgs_valid))
    if len(imgs_valid) >= 2500:
        exit()
    if im_name in ("mesh_42.jpg", "steel_8.jpg", "hubble_44.jpg", "leather_90.jpg", "leather_125.jpg"):
        continue
    if not im_name.lower().endswith(tuple(format)):
        continue
    if im_name not in filtered_imnames:
        continue
    if im_name.split('.')[0] in created:
        continue
    print(im_name)
    im_path = os.path.join(imfolder_path, im_name)
    for j in range(num_using_img):
        image = Image.open(im_path)
        if image.mode in ("RGBA", "P", "CMYK"):
            image = image.convert("RGB")
        if image.mode in ("L",):
            im = np.array(image)
            im = np.repeat(im[:, :, None], 3, axis=2)
            image = Image.fromarray(im)
        image_h = np.array(image).shape[0]
        image_w = np.array(image).shape[1]

        nTextOnImage = 10


        rects = []
        iter = 0
        all_annot_text = ''
        num_trying = 0
        while iter < nTextOnImage:
            txt_fn = './word_valid_dataset/{}_{}.txt'.format(im_name.split('.')[0], j)
            img_fn = '{}_{}.jpg'.format(im_name.split('.')[0], j)
            num_trying += 1
            if num_trying > nTextOnImage * 3:
                break


            angle = np.random.randint(-20, 21)
            min_fs, max_fs = (image_w/18, image_w/9)
            font_size = np.random.randint(min_fs, max_fs)

            rndm = np.random.randint(0, len(fonts))
            font = ImageFont.truetype(fonts[rndm], font_size, encoding='unic')

            draw = ImageDraw.Draw(image)

            text = getRndTxt()
            text = ''.join([i for i in text if i in allowed_chars])
            while len(text) < 3:
                text = getRndTxt()
                text = ''.join([i for i in text if i in allowed_chars])


            bidi_text = text

            reshaped_text = arabic_reshaper.reshape(text)  # correct its shape
            bidi_text = get_display(reshaped_text) # correct its direction


            x0, y0 = [np.random.randint(0, image_w),
                      np.random.randint(0, image_h)]

            w, hgetsize = font.getsize(bidi_text)
            margin = 0
            ascent, descent = font.getmetrics()
            w, h = font.getmask(bidi_text).getbbox()[2], font.getmask(bidi_text).getbbox()[3]


            txt = Image.new('L', (w, h))
            d = ImageDraw.Draw(txt)
            d.text((0, h-hgetsize), bidi_text,  font=font, fill=255)

            words = bidi_text.split()

            Image_rotated_txt = txt.rotate(angle,  expand=1, center=None)
            hh, ww = np.array(Image_rotated_txt).shape


            rect = ((x0+ww/2, y0+hh/2), (w, h), -angle)
            rect_AA = ((x0+ww/2, y0+hh/2), (ww, hh), 0)
            image_rect = ((image_w/2,image_h/2), (image_w,image_h), 0)


            box = cv2.boxPoints(rect)
            box = np.int0(box)

            if not cv2.rotatedRectangleIntersection(rect_AA, image_rect)[0] == 2:
                continue


            from rotated_rect_crop import crop_rotated_rectangle
            imageeee = cv2.imread(im_path)
            image_cropped = crop_rotated_rectangle(imageeee, rect)


            rec_avg_color = np.flip(np.mean(image_cropped, axis=(0,1)))
            stdd = np.std(image_cropped, axis=(0,1))
            if np.max(stdd) > 30:
                continue



            no_intersect = True
            for rectangle in rects:
                stat = cv2.rotatedRectangleIntersection(rect_AA, rectangle)[0]
                if not stat == 0:
                    no_intersect = False
                    break
            if no_intersect:
                iter += 1
                rects.append(rect_AA)
            else:
                continue

            textColor = getColorText(rec_avg_color)

            # image.paste(ImageOps.colorize(Image_rotated_txt, (0,0,0), textColor),
            #             (x0,y0),  Image_rotated_txt)
            # word_im = image.crop((x0, y0, x0+Image_rotated_txt.size[0], y0+Image_rotated_txt.size[1]))

            image_arr = np.array(image)
            im_back = image_arr[y0:y0 + hh, x0:x0 + ww, :]
            im_top = np.array(ImageOps.colorize(Image_rotated_txt, (0, 0, 0), textColor))
            l_out = blit_images(im_top, im_back.copy(), mode='src', scale_grad=3.)
            # image_arr[y0:y0 + hh, x0:x0 + ww, :] = l_out
            word_im = Image.fromarray(l_out)


            img_fn = '{}_{}.jpg'.format(im_name.split('.')[0], iter)
            word_im.save('./word_valid_dataset/{}'.format(img_fn))
            with codecs.open('./word_valid_dataset/'+img_fn[:-3]+'txt', 'w', 'utf-8') as f:
                f.write(text)
            f.close()
