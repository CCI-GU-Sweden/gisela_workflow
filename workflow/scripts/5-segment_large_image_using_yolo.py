from ultralytics import YOLO
from ultralytics.engine.results import Results

from PIL import Image
import numpy as np
import os
import dask as da
from dask.array import image
#import dask.bag as db
from dask import array
from pathlib import Path
import random
from functools import partial
from threading import Lock
from shapely.affinity import translate
import threading
import skimage.color
from timeit import default_timer as timer

import config

model_mutex = threading.Lock()
#all_coords_mutex = threading.Lock()
#overlaps_mutex = threading.Lock()

random.seed()

IMG_SIZE = config.IMG_SIZE
OVERLAP = 2

import threading
class IntGenerator:
    def __init__(self):
        self.lock = threading.Lock()
        self.cnt : np.uint32 = 100

    def __iter__(self): return self

    def getNext(self):
        self.lock.acquire()
        try:
            self.cnt += 1
            return self.cnt
        finally:
            self.lock.release()

intGen = IntGenerator()

def merge_border_segments(data, block_id, img_size, scan_vertical, border_distance):

    print(f"computing chunk {block_id}")
    local_coords_mod = (0,0)
    neighbour_coords_mod = (0,0)
    if scan_vertical: 
        if data.shape[0] <= img_size:
            return data
        else:
            local_coords_mod = (-(border_distance + 1),0)
            neighbour_coords_mod =  (border_distance,0)
            x = img_size
    else:
        if data.shape[1] <= img_size:
            return data
        else:
            local_coords_mod = (0,-1)
            neighbour_coords_mod =  (0,border_distance)
            y = img_size
    
    for coord in range(img_size):
        if scan_vertical:
            y = coord 
        else:
            x = coord

        local_indices     = (x + local_coords_mod[0],     y + local_coords_mod[1])
        neighbour_indices = (x + neighbour_coords_mod[0], y + neighbour_coords_mod[1])
        id_local = data[local_indices]
        id_neighbour =  data[neighbour_indices]
        if  id_local != 0 and id_neighbour != 0 and id_neighbour != id_local:
            print(f"merging with id: {id_local} {id_neighbour} {block_id} {scan_vertical}")
            idxs = np.where(data == id_local)
            data[idxs] = id_neighbour

    return data


@da.delayed
def segment_with_yolo(model, data):
    results = model.predict(source=np.ascontiguousarray(data), imgsz=IMG_SIZE,show_boxes=False,show_labels=False, verbose=False)
    return results

def segment_wrapper(model, out_path, data, block_id):
    with model_mutex:
        print(f"computing chunk {block_id}, {data.shape}")

        rgb_data = skimage.color.gray2rgb(data)
        result = segment_with_yolo(model,rgb_data)
        computed_result = result.compute()
             
    all_masks = np.zeros(shape=(IMG_SIZE,IMG_SIZE), dtype=np.uint32)
    if computed_result is None or computed_result[0].masks is None:
        return all_masks
    
    result_masks = computed_result[0].masks
    masks = result_masks.data.cpu().numpy()
    shape = computed_result[0].masks.shape
    
    sh1 = shape[1]
    sh2 = shape[2]
    #all_masks = np.zeros(shape=config.CHUNK_SHAPE, dtype=np.uint32)
    tmp_id = intGen.getNext()

    for n in range(shape[0]):
        mask = masks[n,:,:] * intGen.getNext()# random.randint(1,255)
        #mask = masks[n,:,:] * tmp_id# random.randint(1,255)
        mask = np.expand_dims(mask,axis=2)
        
        mask = np.squeeze(mask).astype(np.uint32)
        if shape[1] != IMG_SIZE or shape[2] != IMG_SIZE: 
            #all_masks[:sh1, :sh2,:] = np.where(all_masks[:sh1, :sh2,:] == 0, mask, all_masks[:sh1, :sh2,:])
            all_masks[:sh1, :sh2] = np.where(all_masks[:sh1, :sh2] == 0, mask, all_masks[:sh1, :sh2])
        else:
            all_masks = np.where(all_masks == 0, mask, all_masks)
        

    return all_masks

base = os.getcwd()
out_data_dir = Path(str(base) + "/output")
Path(out_data_dir).mkdir(parents=True, exist_ok=True)

model = YOLO(str(base) + "/latest_model.pt")

#large_image_tmp = da.array.image.imread(str(base) + "/cropped_rgb.png")
large_image_tmp = da.array.image.imread(str(base) + "/cropped_3904x3904.png")

s = large_image_tmp.shape
large_image = large_image_tmp.reshape((s[1],s[2])).rechunk((config.CHUNK_D_SIZE,config.CHUNK_D_SIZE,1))

bound_f = partial(segment_wrapper, model, str(out_data_dir))
#segment_results = large_image.map_blocks(bound_f, dtype=np.uint32,chunks=config.CHUNK_SHAPE)
segment_results = da.array.map_overlap(bound_f, large_image, dtype=np.uint32, chunks=(config.CHUNK_D_SIZE,config.CHUNK_D_SIZE) ,depth=config.OVERLAP, boundary='reflect', trim=True)

border_distance_to_check = 0

merge_horizontal = partial(merge_border_segments,img_size = config.CHUNK_D_SIZE, scan_vertical = False, border_distance = border_distance_to_check)
horizontal_result = segment_results.map_overlap(merge_horizontal,dtype=np.uint32,depth={0: (0,2),1: (0,2)}, boundary=None)

merge_vertical = partial(merge_border_segments,img_size = config.CHUNK_D_SIZE, scan_vertical = True, border_distance = border_distance_to_check)
combined_result = horizontal_result.map_overlap(merge_vertical,dtype=np.uint32,depth={0: (0,2),1: (0,2)}, boundary=None)

print("starting...")
start = timer()

#result = segment_results.compute(scheduler='single-threaded')
result = combined_result.compute(scheduler='single-threaded')

end = timer()
print("stopping: ",end - start)
save_im = Image.fromarray(result)
save_im.save("result_mask.png")

#save_im = Image.fromarray(list_of_all_coords.coords)
#save_im.save("result_mask_new.png")
