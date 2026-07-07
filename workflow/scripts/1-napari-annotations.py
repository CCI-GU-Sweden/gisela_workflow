from PIL import Image
import numpy as np
import webknossos as wk
from skimage import measure
from skimage.io import imread
import dask.array as da
from dataclasses import dataclass
from pathlib import Path
import matplotlib.pyplot as plt
import os
import glob
import config

# USE_MYELIN = True

@dataclass(frozen=True)
class Pixel_size:
    x: float
    y: float
    z: float
    MAG: object
    unit: str = "nm"


label_str = config.ANNOTATION_LAYER_NAME

if config.SHOW_IMAGES:
    import matplotlib.pyplot as plt

img_dl_path = config.DL_PATH + "images/"
annot_dl_path = config.DL_PATH + "annotations/"

Path(config.DL_PATH).mkdir(parents=True, exist_ok=True)
Path(img_dl_path).mkdir(parents=True, exist_ok=True)
Path(annot_dl_path).mkdir(parents=True, exist_ok=True)
if config.CLEAR_OUTPUT_DIR:
    files = glob.glob(img_dl_path + "/*.*")
    files += glob.glob(annot_dl_path + "/*.*")
    for f in files:
        os.remove(f)

ann_folder = '/home/noema/Documents/Gisela/test/annotations/'
img_folder = '/home/noema/Documents/Gisela/test/images/'

idx = 0
for annotation in os.listdir(ann_folder):
    for image in os.listdir(img_folder):
        if annotation.split('.')[0][-7:] == image.split('.')[0][-7:]:
            print(annotation.split('.')[0][-7:], image.split('.')[0][-7:])
            lbl_data = imread(os.path.join(ann_folder, annotation))
            img_data = imread(os.path.join(img_folder, image))
            #            plt.imshow(images, cmap="gray")
            #            plt.imshow(annotations > 0, alpha=0.3, cmap="Reds")
            #            plt.show()

            bh, bw = lbl_data.shape

            if config.SHOW_IMAGES:
                from matplotlib.patches import Rectangle

                ax = plt.gca()

            properties = ['label', 'bbox', 'centroid']

            im_size = config.IMG_SIZE
            img_x_div = bw // im_size
            img_y_div = bh // im_size
            lbl_dask_cropped = lbl_data[0:img_y_div * im_size, 0:img_x_div * im_size]
            img_dask_cropped = img_data[0:img_y_div * im_size, 0:img_x_div * im_size]

            for y in range(img_y_div):
                for x in range(img_x_div):
                    print(f"x: {x}, y: {y}")
                    start_x = x * im_size
                    start_y = y * im_size
                    end_x = start_x + im_size
                    end_y = start_y + im_size
                    active_lbl_chunk = lbl_dask_cropped[start_y:end_y, start_x:end_x]
                    active_img_chunk = img_dask_cropped[start_y:end_y, start_x:end_x]

                    regions = measure.regionprops(label_image=active_lbl_chunk)

                    tot_elems = len(regions)

                    if tot_elems == 0:
                        continue

                    im = Image.fromarray(active_img_chunk.astype(np.uint8))
                    im.save(img_dl_path + str(config.DIR_PREFIX) + "_" + str(idx) + '.png')

                    ann = Image.fromarray(active_lbl_chunk.astype(np.uint32))
                    ann.save(annot_dl_path + str(config.DIR_PREFIX) + "_" + str(idx) + '.tif')
                    idx += 1

print("Done!")