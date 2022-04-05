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


win_fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')

with open('font_finall.txt', 'r') as f:
    fonts = f.read().splitlines()
f.close()

# fonts = os.listdir('./384.Font.Farsi')
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


    num_word = np.random.randint(2, 6)
    news_words = news.split()
    try:
        ithWord = np.random.randint(0, len(news_words)-5)
    except:
        print(news)
        exit()
    n_con_words = ' '.join(news.split()[ithWord:ithWord+num_word])
    return n_con_words

imfolder_path = './bg_img'


with open('imnames.cp', 'rb') as f:
  filtered_imnames = set(cp.load(f))
print(len(filtered_imnames))

images = os.listdir(imfolder_path)
os.makedirs('./final_dataset', exist_ok=True)
created = os.listdir('./final_dataset')
created = ['_'.join(i.split('.')[0].split('_')[:-1]) for i in created if i.split('.')[-1] == 'txt']  # if not i.split('.')[-1] == 'txt']
format = [".jpg", ".png", ".jpeg"]
num_using_img = 1
print('start...')
for im_name in images:
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
        try:
            image = Image.open(im_path)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            image_h = np.array(image).shape[0]
            image_w = np.array(image).shape[1]

            nTextOnImage = np.random.randint(2, 6)


            rects = []
            iter = 0
            all_annot_text = ''
            num_trying = 0
            while iter < nTextOnImage:
                txt_fn = './final_dataset/{}_{}.txt'.format(im_name.split('.')[0], j)
                img_fn = '{}_{}.jpg'.format(im_name.split('.')[0], j)
                num_trying += 1
                if num_trying > nTextOnImage * 20:
                    break


                angle = np.random.randint(-90, 91)
                min_fs, max_fs = (image_w/18, image_w/9)
                font_size = np.random.randint(min_fs, max_fs)

                rndm = np.random.randint(0, len(fonts))
                font = ImageFont.truetype(fonts[rndm], font_size, encoding='unic')

                draw = ImageDraw.Draw(image)

                text = getRndTxt()
                text = ''.join([i for i in text if i in allowed_chars])
                # print(text)

                # bidi_text = text

                reshaped_text = arabic_reshaper.reshape(text)  # correct its shape
                bidi_text = get_display(reshaped_text) # correct its direction
                not_bidi_text = text
                text = bidi_text


                x0, y0 = [np.random.randint(0, image_w),
                          np.random.randint(0, image_h)]

                w, hgetsize = font.getsize(text)
                margin = 0
                ascent, descent = font.getmetrics()
                w, h = font.getmask(text).getbbox()[2], font.getmask(text).getbbox()[3]


                txt = Image.new('L', (w, h))
                d = ImageDraw.Draw(txt)
                d.text((0, h-hgetsize), text,  font=font, fill=255)

                words = text.split()

                Image_rotated_txt = txt.rotate(angle,  expand=1, center=None)
                hh, ww = np.array(Image_rotated_txt).shape


                rect = ((x0+ww/2, y0+hh/2), (w, h), -angle)
                image_rect = ((image_w/2,image_h/2), (image_w,image_h), 0)


                box = cv2.boxPoints(rect)
                box = np.int0(box)

                if not cv2.rotatedRectangleIntersection(rect, image_rect)[0] == 2:
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
                    stat = cv2.rotatedRectangleIntersection(rect, rectangle)[0]
                    if not stat == 0:
                        no_intersect = False
                        break
                if no_intersect:
                    iter += 1
                    rects.append(rect)
                else:
                    continue

                textColor = getColorText(rec_avg_color)

                image.paste(ImageOps.colorize(Image_rotated_txt, (0,0,0), textColor),
                            (x0,y0),  Image_rotated_txt)


                img_fn = '{}_{}.jpg'.format(im_name.split('.')[0], j)
                image.save('./final_dataset/{}'.format(img_fn))

                im = cv2.imread('./final_dataset/{}.jpg'.format(img_fn))
                cv2.rectangle(im, pt1=(x0,y0), pt2=(ww+x0,hh+y0), color=200, thickness=2)


                start = 0
                start_n = 0

                for i, word in enumerate(text.split()):
                    if i == 0:
                        ll = box[0, :]
                        ul = box[1, :]
                        lr = ll + np.array([font.getsize(word)[0] * np.cos(np.deg2rad(-angle)),
                                            font.getsize(word)[0] * np.sin(np.deg2rad(-angle))])
                        ox, oy = (ul + lr) / 2
                        indx = text.find(word, start_n)

                        w, _ = font.getsize(text[0:indx])
                        x0new, y0new = (0 + w, 0)
                        w, _ = font.getsize(word)

                        rectt = ((ox,oy), (w, h), -angle)
                        boxx = cv2.boxPoints(rectt)
                        boxx = np.int0(boxx)
                        cv2.drawContours(im, [boxx], 0, (0, 0, 255), 2)
                    else:
                        indx = text.find(word, start_n)

                        w, _ = font.getsize(text[0:indx])
                        after_word_idx = indx + len(word)
                        w = font.getsize(text[0:after_word_idx])[0] - font.getsize(word)[0]

                        ll = box[0, :] + np.array([w * np.cos(np.deg2rad(-angle)), w * np.sin(np.deg2rad(-angle))])
                        ul = box[1, :] + np.array([w * np.cos(np.deg2rad(-angle)), w * np.sin(np.deg2rad(-angle))])

                        # ll = box[0, :] + np.array([-w * np.cos(np.deg2rad(-angle)), -w * np.sin(np.deg2rad(-angle))])
                        # ul = box[1, :] + np.array([w * np.cos(np.deg2rad(-angle)), w * np.sin(np.deg2rad(-angle))])

                        # ur = box[2, :] + np.array([-w * np.cos(np.deg2rad(-angle)), -w * np.sin(np.deg2rad(-angle))])
                        # lr = box[3, :] + np.array([-w * np.cos(np.deg2rad(-angle)), -w * np.sin(np.deg2rad(-angle))])

                        w, _ = font.getsize(word)
                        lr = ll + np.array([w * np.cos(np.deg2rad(-angle)), w * np.sin(np.deg2rad(-angle))])
                        ox, oy = (ul + lr) / 2
                        # ll = lr + np.array([-w * np.cos(np.deg2rad(-angle)),
                        #                     -w * np.sin(np.deg2rad(-angle))])
                        # ox, oy = (ll + ur) / 2

                        rectt = ((ox, oy), (w, h), -angle)
                        boxx = cv2.boxPoints(rectt)
                        boxx = np.int0(boxx)
                        cv2.drawContours(im, [boxx], 0, (0, 0, 255), 2)

                    start_n = indx + len(word)

                    annot_list = boxx.reshape(-1).astype(str).tolist()
                    annot_list.append(not_bidi_text.split()[-i-1])
                    annot_text = ','.join(annot_list)

                    all_annot_text += annot_text + os.linesep  # '\n'
                    txt_fn = './final_dataset/{}_{}.txt'.format(im_name.split('.')[0], j)


            with codecs.open(txt_fn, 'w', "utf-8") as f:
                f.write(all_annot_text)


        except:
            import sys, traceback
            # print(text)
            traceback.print_exc(file=sys.stdout)
            continue
