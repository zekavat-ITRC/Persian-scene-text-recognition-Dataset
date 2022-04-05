import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.neighbors import NearestNeighbors
import pickle

def getColorText(back_color):
    with open("pairs.txt", "rb") as fp:   # Unpickling
        b = pickle.load(fp)
    b = np.array(b)
    b = b.reshape(10000, 3)


    neigh = NearestNeighbors(n_neighbors=1)
    neigh.fit(b)


    dist, idx = neigh.kneighbors([back_color], n_neighbors=1)
    mod = np.mod(idx, 2)


    if mod == 0:
        color = b[idx+1, :]
    else:
        color = b[idx-1, :]

    return tuple(map(tuple, color.reshape(1, 3)))[0]

if __name__ == "__main__":
    back_color = [119.13379228, 148.43300409, 153.61289035]
    color = getColorText(back_color=back_color)
    print(color)

