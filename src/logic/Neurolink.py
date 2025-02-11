from PIL import Image

from src.utils import constants
from src.logic.onnx_inference import OnnxObjectDetection, ObjectPrediction
from src.logic import digit_recognition


class _NeurolinkClass:
    field_aspects_model: OnnxObjectDetection
    inventory_aspects_model: OnnxObjectDetection

    # Make it singleton
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_NeurolinkClass, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def __init__(self):
        with open(constants.FIELD_CLASS_NAMES_PATH) as file:
            self.field_aspects_model = OnnxObjectDetection(
                model_path=constants.FIELD_OBJECT_DETECTION_PATH,
                class_names=file.read().strip().split(),
                img_size=640,
            )
        with open(constants.INVENTORY_CLASS_NAMES_PATH) as file:
            self.inventory_aspects_model = OnnxObjectDetection(
                model_path=constants.INVENTORY_OBJECT_DETECTION_PATH,
                class_names=file.read().strip().split(),
                img_size=640,
            )

    def predict_field_aspects(self, image: Image.Image) -> list[ObjectPrediction]:
        """Находит расположение аспектов на изображении рабочей зоны"""
        return self.field_aspects_model.predict(image)

    def predict_inventory_aspects(self, image: Image.Image) -> list[ObjectPrediction]:
        """Находит расположение аспектов на изображении инвентаря"""
        return self.inventory_aspects_model.predict(image)

    def predict_inventory_aspects_count(self, image: Image.Image) -> dict[str, int]:
        """
        По изображению инвентаря определяет количество аспектов.
        Возвращает словарь "Название аспекта - Его количество"
        """
        predictions = self.inventory_aspects_model.predict(image)
        return digit_recognition.aspects_count(predictions)


Neurolink = _NeurolinkClass()
