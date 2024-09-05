import logging
import time

# For correctly build by "pyinstaller". By default this package not included in build
import scipy._lib.array_api_compat.numpy.fft
import scipy.special._special_ufuncs
#---------------------------------------------

from inference import get_model
from PIL import Image

from utils.constants import ROBOFLOW_API_KEY, ROBOFLOW_PROJECT_NAME, ROBOFLOW_MODEL_VERSION


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
    model: any
    inputModelName: str
    outputModelName: str
    isConnectionError: bool
    minConfidence: float = 0.6
    overlap: float = 0.3

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
            # Run with "roboflow"
            # rf = roboflow.Roboflow(api_key=ROBOFLOW_API_KEY)
            # logging.debug(f"Roboflow successfully initialized")
            # project = rf.workspace().project(ROBOFLOW_PROJECT_NAME)
            # logging.debug(f"Roboflow project successfully initialized")
            # self.model = project.version(ROBOFLOW_MODEL_VERSION).model
            # logging.debug(f"Roboflow model successfully initialized")

            # Run with "inference"
            self.model = get_model(model_id=f"{ROBOFLOW_PROJECT_NAME}/{ROBOFLOW_MODEL_VERSION}", api_key=ROBOFLOW_API_KEY)
            logging.debug(f"Inference model successfully initialized")

            # Run with onnxruntime
            # self.model = onnxruntime.InferenceSession(
            #     path_or_bytes=MODEL_ONNX_PATH,
            #     providers=[],
            # )
            # self.inputModelName = self.model.get_inputs()[0].name
            # self.outputModelName = self.model.get_outputs()[0].name

            self.isConnectionError = False
            return True
        except ConnectionError as err:
            logging.debug(f"Error when connecting to roboflow: {err}")
            self.isConnectionError = True
            return False


    def predict(self, image: Image.Image):
        # Run with "roboflow"
        # imagePath = IMAGE_TMP_PATH
        # createDirByFilePath(imagePath)
        # image.save(imagePath)
        # logging.debug(f"Tmp image saved to {IMAGE_TMP_PATH}")
        # predictions = self.model.predict(imagePath, confidence=self.minConfidence, overlap=self.overlap).json()
        # logging.debug(f"Gotten predictions from original neurolink: {predictions}")
        # predictions = predictions['predictions']
        # result = list(map(lambda prediction: Prediction(
        #     prediction['x'],
        #     prediction['y'],
        #     prediction['width'],
        #     prediction['height'],
        #     prediction['class'],
        #     prediction['confidence'],
        # ), predictions))

        # Run with "inference"
        predictions = self.model.infer(image=image, confidence=self.minConfidence, overlap=self.overlap)
        # logging.debug(f"Gotten predictions from original neurolink: {predictions}")
        predictions = predictions[0].predictions
        result = list(map(lambda prediction: Prediction(
            prediction.x,
            prediction.y,
            prediction.width,
            prediction.height,
            prediction.class_name,
            prediction.confidence,
        ), predictions))

        # Run with "onnxruntime"
        # image = image.copy().convert("RGB").resize(size=(640, 640), resample=Image.Resampling.LANCZOS)
        # arrayImage = np.asarray(image)
        # preparedImage = [[], [], []]
        # for channelIdx in range(0, 3):
        #     for stringPixels in arrayImage:
        #         preparedImage[channelIdx].append([])
        #         for pixel in stringPixels:
        #             preparedImage[channelIdx][-1].append(pixel[channelIdx])
        # result = self.model.run(
        #     output_names=[self.outputModelName],
        #     input_feed={self.inputModelName: [preparedImage]},
        # )
        # predictions = list(result[0][0].argmax(0))

        return result

Neurolink = _NeurolinkClass()
