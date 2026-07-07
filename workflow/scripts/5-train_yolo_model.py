from ultralytics import YOLO
import config
import os
from pathlib import Path
import torch
import shutil

# TODO: read path from confg? And if it does not exist, do magic below
# file_dir = Path(__file__).parent.resolve()
# base = file_dir
# base = os.getcwd()
dataSetFile = config.DATASET_PATH + "/" + config.TRAINING_DATASET_FILE

if not os.path.exists(config.MODEL_SAVE_DIR):
    os.makedirs(config.MODEL_SAVE_DIR)

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

model = YOLO("/home/noema/Documents/Gisela/models/unmyelinated_axons/unaxon_model_1125.pt")

results = model.train(data=dataSetFile,
                      epochs=config.TRAINING_EPOCHS,
                      patience=30,
                      imgsz=config.IMG_SIZE,
                      show_boxes=False,
                      show_labels=False,
                      batch=6,
                      device='cpu',
                      project="/home/noema/code/gisela_workflow/runs",
                      name="unaxon",
                      exist_ok=True
                      )

results = model.val()

torch.cuda.empty_cache()

best_path = Path(model.trainer.best)
target_path = Path(config.MODEL_SAVE_DIR) / config.MODEL_SAVE_FILE_NAME

target_path.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(best_path, target_path)

