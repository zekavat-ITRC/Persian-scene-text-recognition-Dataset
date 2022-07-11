# Persian-scene-text-recognition

We provide a persian synthetic scene text images which can be used for text detection, text recognition, and end-to-end text recognition model.
We provide two kinds of datasets:

**a) cropped word images (for text recognition)**

![sample image of cropped word images](scene_word_images.jpg)

**b) scene text images (for text detection and end-to-end text recognition)**

![sample image of scene text images](scene_text_image.jpg)


## Demo for getting background images, creating dataset, reading images and annotation files, and displaying images
The "demo.ipynb" is provided to get background images and using them to create dataset. At the end of this file, images and annotation files are read and use to display images and add a bounding box for each word.
You can open it in google colab openning [this link](https://colab.research.google.com/drive/1f9-zoJnxzmfKoffOPG4bTbDQAJ4o9E_h?usp=sharing).


## Download our dataset
We have two datasets:

**a) cropped word images (for text recognition)**

The scene_word_dataset.tar.gz can be accessed [this google drive link](https://drive.google.com/file/d/1VrcwsgXlBYcWk6ZNj8u4mWlWvhlGiCvj/view?usp=sharing).
Unzip scene_text_dataset.zip for images and annotation files.

You can get the file this way:
```
pip install --upgrade gdown
gdown 1VrcwsgXlBYcWk6ZNj8u4mWlWvhlGiCvj
```


The scene_word_dataset.tar.gz includes images and annotation files. An annotation file (gt.txt) is also provided. Each line of this file includes the name of one of the cropped word images and the text in that image in double quotation. The name and the text are separated with comma.

you can also access to our validation dataset using [this google drive link](https://drive.google.com/file/d/1GIh5_RGOz1g5161vB0FTNIjaal-CRkif/view?usp=sharing).
You can get the file this way:
```
gdown 1GIh5_RGOz1g5161vB0FTNIjaal-CRkif
```

**b) scene text images (for text detection and end-to-end text recognition)**

The scene_text_dataset.tar.gz can be accessed [this google drive link](______________).
Unzip scene_text_dataset.zip for images and annotation files.

You can get the file this way:
```
gdown 1V-_____________________gvfw
```

you can also access to our validation dataset using [this google drive link](https://drive.google.com/file/d/1HV2GMkh8S1UeckzpELb1rCrUJPr5XpQu/view?usp=sharing).
You can get the file this way:
```
gdown 1HV2GMkh8S1UeckzpELb1rCrUJPr5XpQu
```

## Requirements
If you want to create your own dataset please install following packages:
```
opencv-python
numpy
arabic-reshaper
python-bidi
matplotlib
Pillow
scikit-learn
```
## Create your own scene text images dataset
To create your own dataset you can run synthText.py and if the shape of text in images is incorrect you can run synthText_forLinux.py instead.
You can also provide different background images, text source, fonts, and colors.
If you want to use same background images that we used and provided from [this repository](https://github.com/ankush-me/SynthText), you can try:
```
sudo apt-get install aria2 -q
aria2c https://academictorrents.com/download/2dba9518166cbd141534cbf381aa3e99a087e83c.torrent --allow-overwrite=true --select-file=1 --seed-time=0 -q
tar -zxvf ./SynthText/bg_data/bg_img.tar.gz
```

## Create your own cropped word images dataset
To create your own dataset you can run cropped_word_synthText.py
You can also provide different background images, text source, fonts, and colors.
If you want to use same background images that we used, see [here](https://github.com/zekavat-ITRC/Persian-scene-text-recognition-Dataset#create-your-own-scene-text-images-dataset).

## Display images and reading annotation file
To display images you can run one of these commands:
```
python display_image_txt.py --path 'final_dataset'          # for displaying scene text dataset that you have created running synthText.py
python display_image_txt.py --path 'scene_text_dataset'     # for displaying our scene text dataset that you have downloaded
python display_cropped_word.py --path 'word_final_dataset'  # for displaying cropped word dataset that you have created running cropped_word_synthText.py
python display_cropped_word.py --path 'scene_word_dataset'  # for displaying our cropped word dataset that you have downloaded

```
