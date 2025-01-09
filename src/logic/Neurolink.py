import numpy as np
from PIL import Image
from src.utils import constants
from src.logic.onnx_inference import OnnxClassification, OnnxObjectDetection, ObjectPrediction


class _NeurolinkClass:
    field_aspects_model: OnnxObjectDetection
    inventory_aspects_model: OnnxObjectDetection
    digits_model: OnnxClassification

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
                img_height=640,
                img_width=640,
            )
        with open(constants.INVENTORY_CLASS_NAMES_PATH) as file:
            self.inventory_aspects_model = OnnxObjectDetection(
                model_path=constants.INVENTORY_OBJECT_DETECTION_PATH,
                class_names=file.read().strip().split(),
                img_height=640,
                img_width=640,
            )
        with open(constants.DIGITS_CLASS_NAMES_PATH) as file:
            self.digits_model = OnnxClassification(
                model_path=constants.DIGITS_CLASSIFICATION_PATH,
                class_names=file.read().strip().split(),
                img_height=17,
                img_width=12,
            )

    def predict_field_aspects(self, image: Image.Image) -> list[ObjectPrediction]:
        """Находит расположение аспектов на изображении рабочей зоны"""
        return self.field_aspects_model.predict(image)

    def predict_inventory_aspects(self, image: Image.Image) -> list[ObjectPrediction]:
        """Находит расположение аспектов на изображении инвентаря"""
        return self.inventory_aspects_model.predict(image)

    def predict_inventory_aspects_count(self, image: Image.Image) -> dict[str, int]:
        """
        По изображению инвентаря определяет количество аспектов
        Возвращает словарь "Название аспекта - Его количество"
        """
        result = dict()

        inv_aspects_predictions = self.inventory_aspects_model.predict(image)
        image = image.convert("L")  # Переводим в чёрно-белое. Классификатор цифр работает в ЧБ
        image = np.array(image)
        for pred in inv_aspects_predictions:
            x, y, h, w = map(int, [pred.x, pred.y, pred.height, pred.width])
            x = x - w // 2
            y = y - h // 2
            aspect_img = image[y: y + h, x: x + w]
            result[pred.predictionName] = self.__get_aspect_number(aspect_img)
        return result

    def __get_aspect_number(self, aspect_img: np.ndarray) -> int:
        """Распознаёт число на изображении аспекта в инвентаре"""
        digit_width_fraction = 1 / 5    # Размеры цифр по отношению ко всему размеру аспекта
        digit_height_fraction = 1 / 3   # Прикинул на глаз, возможно стоит уточнить
        h, w = aspect_img.shape
        digit_h = h * digit_height_fraction
        digit_w = w * digit_width_fraction
        digits = []
        for i in range(4):
            x = w - digit_w * i
            y = h - digit_h
            digit_img = aspect_img[int(y): int(y + digit_h), int(x): int(x + digit_w)]
            if (digit_img == 255).sum() > 0:  # Простая проверка на наличие цифры на картинке. Цифры содержат белые пиксели
                digit_img = Image.fromarray(digit_img, "L")
                digits.append(self.digits_model.predict(digit_img))
        num = list(reversed(digits))
        num = "".join(map(str, num))
        if num == "":
            return 0
        else:
            return int(num)


Neurolink = _NeurolinkClass()
