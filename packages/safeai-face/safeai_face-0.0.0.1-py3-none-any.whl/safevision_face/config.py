
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

DEFAULT_YOLO_MODEL_PATH = "/home/research/paradise/Face/face_project/safevision_face/model"

DEFAULT_DB_PATH = "./"
DEFAULT_COLLECTION_NAME = "face_collection"
DEFAULT_DIMENSION = 512
DEFAULT_METRIC = "COSINE"
DEFAULT_CONFIDENCE_THRESHOLD = 0.4
DEFAULT_IOU_THRESHOLD = 0.4

DEFAULT_PADDING = 5
