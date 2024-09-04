import logging
import time

import roboflow
from PIL import Image

from utils.constants import ROBOFLOW_API_KEY, ROBOFLOW_PROJECT_NAME, ROBOFLOW_MODEL_VERSION, IMAGE_TMP_PATH
from utils.utils import createDirByFilePath

class Prediction:
    x: float
    y: float
    width: float
    height: float
    predictionName: str
    confidence: float
    def __init__(self, x: float, y: float, width: float, height: float, predictionName: str, confidence: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.predictionName = predictionName
        self.confidence = confidence
    def __repr__(self):
        return f"Prediction(\"{self.predictionName}\": ({self.x}, {self.y}) [{self.width} x {self.height}], conf: {round(self.confidence * 100, 1)}%)"

class _NeurolinkClass:
    model: roboflow.models.inference.InferenceModel
    isConnectionError: bool
    minConfidence: float = 40
    overlap: float = 30

    # Make it singleton
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_NeurolinkClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


    def __init__(self):
        while self.init() is not True:
            logging.debug("Connection error. Trying to reconnect after 3 seconds...")
            time.sleep(3)
        logging.debug("Successfully initialized Roboflow neurolink project")

    def init(self):
        try:
            rf = roboflow.Roboflow(api_key=ROBOFLOW_API_KEY)
            logging.debug(f"Roboflow successfully initialized")
            project = rf.workspace().project(ROBOFLOW_PROJECT_NAME)
            logging.debug(f"Roboflow project successfully initialized")
            self.model = project.version(ROBOFLOW_MODEL_VERSION).model
            logging.debug(f"Roboflow model successfully initialized")
            self.isConnectionError = False
            return True
        except ConnectionError as err:
            logging.debug(f"Error when connecting to roboflow: {err}")
            self.isConnectionError = True
            return False


    def predict(self, image: Image.Image):
        imagePath = IMAGE_TMP_PATH
        createDirByFilePath(imagePath)
        image.save(imagePath)
        logging.debug(f"Tmp image saved to {IMAGE_TMP_PATH}")
        predictions = self.model.predict(imagePath, confidence=self.minConfidence, overlap=self.overlap).json()
        logging.debug(f"Gotten predictions from original neurolink: {predictions}")
        predictions = predictions['predictions']
        result = list(map(lambda prediction: Prediction(
            prediction['x'],
            prediction['y'],
            prediction['width'],
            prediction['height'],
            prediction['class'],
            prediction['confidence'],
        ), predictions))
        return result

Neurolink = _NeurolinkClass()
