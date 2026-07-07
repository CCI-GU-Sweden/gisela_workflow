from ultralytics import YOLO

# Load a YOLOv8n PyTorch model
model = YOLO("/home/noema/code/gisela_workflow/workflow/scripts/models/unaxon/unaxon_model_1126.pt")

# Export the model
model.export(format="openvino", task="segment", imgsz=1024)