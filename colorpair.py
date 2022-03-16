import cv2
import os
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
import pandas as pd
# from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
# from itertools import chain
# import matplotlib.font_manager
import pickle

def getColorText(back_color):
    if not os.path.exists('./pairs.txt'):
        pairs = []
        im_names = []
        im_path = r'D:\ITRC\dataset\IIIT5K-Word_V3.0'
        for im_filename in os.listdir(im_path):
            # quantization (k-means)
            k = 2
            img = cv2.imread(os.path.join(im_path, im_filename))
            (h, w) = img.shape[:2]
            image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            # reshape the image into a feature vector so that k-means
            # can be applied
            image = image.reshape((image.shape[0] * image.shape[1], 3))
            # apply k-means using the specified number of clusters and
            # then create the quantized image based on the predictions
            clt = MiniBatchKMeans(n_clusters=k)
            labels = clt.fit_predict(image)
            quant = clt.cluster_centers_.astype("uint8")[labels]
            pair = clt.cluster_centers_.astype("uint8")
            # print(pair[0, :].reshape(1, 1, 3))
            pair1 = cv2.cvtColor(pair[0, :].reshape(1, 1, 3), cv2.COLOR_Lab2RGB).reshape(1, 3)
            # print(pair1)
            # print(pair[1, :].reshape(1, 1, 3))
            pair2 = cv2.cvtColor(pair[1, :].reshape(1, 1, 3), cv2.COLOR_Lab2RGB).reshape(1, 3)
            # print(pair2)
            # print(pair)
            pairs.append(pair1)
            pairs.append(pair2)
            im_names.append(im_filename)
            im_names.append(im_filename)
            # # print(np.unique(quant, axis=0))
            # # print(quant)
            # # reshape the feature vectors to images
            # quant = quant.reshape((h, w, 3))
            # image = image.reshape((h, w, 3))
            # # convert from L*a*b* to RGB
            # quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
            #
            #
            # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            # plt.show()
            #
            #
            # fig = plt.figure()
            # plt.imshow(cv2.cvtColor(quant, cv2.COLOR_BGR2RGB))
            # plt.title('quant')
            # plt.axis('off')
            # # plt.savefig('quant.png')
            # plt.show()

        df = pd.DataFrame(columns=['fn','color'])
        df['fn'] = im_names
        df['color'] = pairs

        df.to_excel("colorPairs.xlsx", header=None)


        with open("pairs.txt", "wb") as fp:   #Pickling
            pickle.dump(pairs, fp)

    with open("pairs.txt", "rb") as fp:   # Unpickling
        b = pickle.load(fp)
    b = np.array(b)
    b = b.reshape(10000, 3)

    # flatten_list = list(chain.from_iterable(b))
    # flatten_array = np.array(flatten_list)
    # print(flatten_array)
    # print(flatten_list)

    neigh = NearestNeighbors(n_neighbors=1)
    neigh.fit(b)

    # im_path = './nature.jpg'
    # image = Image.open(im_path)
    # back_color = [119.13379228, 148.43300409, 153.61289035]
    dist, idx = neigh.kneighbors([back_color], n_neighbors=1)
    # print(dist, 'index = ', idx)
    mod = np.mod(idx, 2)

    color = b[idx, :]
    # print('khodesh', color)

    if mod == 0:
        color = b[idx+1, :]
    else:
        color = b[idx-1, :]
    # print('match color', color)


    return tuple(map(tuple, color.reshape(1, 3)))[0]

if __name__ == "__main__":
    # print('hi')
    back_color = [119.13379228, 148.43300409, 153.61289035]
    a = getColorText(back_color=back_color)
    # print(a)

