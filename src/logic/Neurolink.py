from dataclasses import dataclass

from PIL import Image

from src.logic import onnx_inference


@dataclass
class Prediction:
    x: float
    y: float
    width: float
    height: float
    predictionName: str
    confidence: float


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
        pass

    def predict(self, image: Image.Image):
        image = image.convert("RGB")
        preproc_image, returned_metadata = onnx_inference.preprocess(image)
        predicted_arrays = onnx_inference.predict(preproc_image)
        postprocessed = onnx_inference.postprocess(predicted_arrays, returned_metadata)[0]

        result = list(map(lambda prediction: Prediction(
            x=prediction[0] + abs(prediction[0] - prediction[2]) / 2,
            y=prediction[1] + abs(prediction[1] - prediction[3]) / 2,
            width=abs(prediction[0] - prediction[2]),
            height=abs(prediction[1] - prediction[3]),
            predictionName=onnx_inference.class_names[int(prediction[6])],
            confidence=prediction[4],
        ), postprocessed))

        return result


Neurolink = _NeurolinkClass()
