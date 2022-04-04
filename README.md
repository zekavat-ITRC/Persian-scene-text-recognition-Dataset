# Persian-scene-text-recognition

We provide a persian synthetic scene text images which can be used for text detection, text recognition, and end-to-end text recognition model.
We provide two kinds of datasets:
a) cropped word images (for text recognition)
b) scene text images (for text detection and end-to-end text recognition)

The "demo.ipynb" is provided to get background images and using them to create dataset. at the end of this file images and annotation files are read and use to display images and add a bounding box for each word.


# Download our dataset
We have two datasets:
a) cropped word images (for text recognition)
use scene_word_dataset.zip for images and annotation files. An attotan file (gt.txt) is also provided. Each line of this file includes one of cropped word images and the text in that image in double quotation and are separated with comma.
b) scene text images (for text detection and end-to-end text recognition)
unzip scene_text_dataset.zip (scene_text_dataset.z01 is needed too) for images and annotation files

# Create your own scene text images dataset
To create your own dataset you can run synthText.py and if the shape of text in images is incorrect you can run synthText_forLinux.py instead.
You can also provide different background images, text source, fonts, and colors.

# Create your own cropped word images dataset
To create your own dataset you can run cropped_word_synthText.py
You can also provide different background images, text source, fonts, and colors.
