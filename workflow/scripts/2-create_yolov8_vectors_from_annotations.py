from pathlib import Path
import os
import glob
from PIL import Image
from skimage import measure
import numpy as np
from pathlib import Path
import scipy.spatial as ssp
import config
import donuts


#TODO: read path from confg? And if it does not exist, do magic below
# file_dir = Path(__file__).parent.resolve()
# base = file_dir
cwd = os.getcwd()
base = cwd
path = str(base) + "/dl/"
annot_dl_path = path + "annotations/"
vector_path = path + "vectors/"
annotations = glob.glob(annot_dl_path+"/*.*")
Path(vector_path).mkdir(parents=True, exist_ok=True)

if config.CLEAR_OUTPUT_DIR:
    old_vectors = glob.glob(vector_path+"/*.*")
    for v in old_vectors:
        os.remove(v)

def filter_small(x):
    return 0.000 if x < 0.002 else x

vec_filt = np.vectorize(filter_small)

for ann in annotations:
    im = np.asarray(Image.open(ann)).swapaxes(0,1)
    props = measure.regionprops(label_image=im)
    with open(vector_path + str(Path(ann).stem) + '.txt',"x") as targets_file:
        for prop in props:
            coords = prop.coords
            if prop.area < 80:
                continue
            donut = donuts.generate_contour(prop.image)
            x_offs = prop.bbox[0]
            y_offs = prop.bbox[1]
            points = np.add(donut,(x_offs,y_offs))
            points = np.divide(points,config.IMG_SIZE)
            
            points = vec_filt(points)
            targets_file.write("0 ")
            np.savetxt(targets_file,points, newline=' ', fmt='%1.3f')
            targets_file.write("\n")
