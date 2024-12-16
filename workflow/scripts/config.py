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


ANNOTATION_LAYER_NAME = jconf['layer_name']
WK_ID_LIST = jconf['image_id_list']

IMG_SIZE = jconf['img_size']
NETWORK_SIZE = IMG_SIZE
OVERLAP = jconf['overlap']
CHUNK_D_SIZE = IMG_SIZE - (2 * OVERLAP)
CHUNK_SHAPE = (CHUNK_D_SIZE,CHUNK_D_SIZE,1)

BASE_PATH = str(os.getcwd())
DL_PATH = BASE_PATH + "/dl/" + jconf['short_name'] + "/"

MIN_LABELS_PER_IMAGE = 2
MIN_COVERAGE = 0.2

SHOW_IMAGES = False
CLEAR_OUTPUT_DIR = DEBUGGING

ORG_ID = os.getenv("ORG_ID")
WK_TOKEN = os.getenv("WK_TOKEN")

TRAINING_DATASET_FILE = "datasets/" + jconf['prefix'] + "dataset.yaml"
TRAINING_EPOCHS = 300

MODEL_SAVE_DIR = "models/" + jconf['prefix']
MODEL_SAVE_FILE_NAME = "latest_model.pt"


TEST_DATA_DIR = DL_PATH + "test_data/"
TEST_IMAGE_RESULT_FILE_NAME = jconf['prefix'] + "_result.png"
        
