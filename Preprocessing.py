import os
from icecream import ic
import matplotlib.image as mpimg

ABS_PATH = os.path.abspath("")
DOWNLOAD_PATH = os.path.join(ABS_PATH, "downloads")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)


def process_image(path):
    
    img = mpimg.imread(path)
    res = list(map(lambda res: int(res/3), list(img.shape[:-1])))
    x_res, y_res = res[0], res[1]

    img_list = []
    for i in range(3):
        for j in range(3):
            img_split = img[i*x_res:(i+1)*x_res, j*y_res:(j+1)*y_res]
            img_list.append(img_split)
    
    SPLIT_PATH = os.path.join(os.path.dirname(path), "split")
    os.makedirs(SPLIT_PATH, exist_ok=True)

    for i, img_split in enumerate(img_list):
        mpimg.imsave(os.path.join(SPLIT_PATH, f"{i}.jpg"), img_split)


for root, dirs, files in os.walk(DOWNLOAD_PATH):
    for name in files:
        if name.endswith(".jpg"):
            process_image(path=os.path.join(root, name))
   