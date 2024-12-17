import dotenv
import os
import json
import pathlib

DEBUGGING = True

dotenv.load_dotenv()


ldir = pathlib.Path(__file__).parent.resolve()


with open(str(ldir) + '/layers_config.json') as f:
    jconfs = json.load(f)

fp = os.getcwd() +'/current_config.txt'
has_layer_conf = os.path.isfile(fp)
jconf = jconfs[0]

if has_layer_conf:
    with open(fp) as c:
        active_layer = c.readline()
        active_layer = active_layer.replace('\n','')

    tc = [c for c in jconfs if c['short_name'] == active_layer]
    
    if len(tc) > 0:
        jconf = tc[0]


USE_DOUGHNUTS = jconf['generate_doughnuts'] if 'generate_doughnuts' in jconf else False
USE_CONTOURS = jconf['use_contours'] if 'use_contours' in jconf else False

ANNOTATION_LAYER_NAME = jconf['layer_name']
WK_ID_LIST = jconf['image_id_list']

IMG_SIZE = jconf['img_size']
NETWORK_SIZE = IMG_SIZE
OVERLAP = jconf['overlap']
CHUNK_D_SIZE = IMG_SIZE - (2 * OVERLAP)
CHUNK_SHAPE = (CHUNK_D_SIZE,CHUNK_D_SIZE,1)

BASE_PATH = str(os.getcwd())
DIR_PREFIX = jconf['short_name']

DL_PATH = BASE_PATH + "/dl/" + DIR_PREFIX + "/"

MIN_LABELS_PER_IMAGE = 2
MIN_COVERAGE = 0.2

SHOW_IMAGES = False
CLEAR_OUTPUT_DIR = DEBUGGING
#CLEAR_OUTPUT_DIR = False

ORG_ID = os.getenv("ORG_ID")
WK_TOKEN = os.getenv("WK_TOKEN")


DATASET_PATH = BASE_PATH + "/datasets/" + DIR_PREFIX 
TRAINING_DATASET_FILE = "dataset.yaml"
TRAINING_EPOCHS = 300

MODEL_SAVE_DIR = "models/" + DIR_PREFIX
MODEL_SAVE_FILE_NAME = "latest_model.pt"

TEST_DATA_DIR = DL_PATH + "test_data/" + DIR_PREFIX + "/"
TEST_IMAGE_RESULT_FILE_NAME = TEST_DATA_DIR + "_result.png"
        
RESULT_OUTPUT_DIR = BASE_PATH + "/result/" + DIR_PREFIX
RESULT_OUTPUT_MASK_IMAGE = RESULT_OUTPUT_DIR + "/result_mask.png"
