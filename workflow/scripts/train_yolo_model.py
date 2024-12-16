from ultralytics import YOLO
import config
import os
from pathlib import Path
import torch


#TODO: read path from confg? And if it does not exist, do magic below
#file_dir = Path(__file__).parent.resolve()
#base = file_dir
#base = os.getcwd()
dataSetFile = config.BASE_PATH + "/" + config.TRAINING_DATASET_FILE

os.environ["PYTORCH_CUDA_ALLOC_CONF"]="expandable_segments:True"
import gc



model = YOLO("yolov8n-seg.pt")
results = model.train(data=dataSetFile,epochs=config.TRAINING_EPOCHS, imgsz=config.IMG_SIZE, show_boxes=False, show_labels=False, batch=6)
results = model.val()

torch.cuda.empty_cache()

model.save(config.MODEL_SAVE_DIR + "/" + config.MODEL_SAVE_FILE_NAME)

