import numpy as np
import onnxruntime
from PIL import Image


class OnnxClassification:
    def __init__(
            self,
            model_path: str,
            class_names: list[str],
            img_height: int,
            img_width: int,
    ):
        self.model = onnxruntime.InferenceSession(model_path)
        self.class_names = class_names
        inputs = self.model.get_inputs()
        outputs = self.model.get_outputs()
        self.input_layer_name = inputs[0].name
        self.output_layer_name = outputs[0].name
        self.img_height = img_height
        self.img_width = img_width

    def predict(self, image: Image.Image) -> list[str]:
        """Классификация изображения"""
        image = image.convert("L")
        image_resized = image.resize((self.img_width, self.img_height), resample=Image.Resampling.LANCZOS)
        resized = np.array(image_resized)
        resized = np.pad(resized, 5)  # TODO: сделать менее хардкодным. Нужно, потому что при обучении использовался паддинг 5 пикс.

        img_in = resized.astype(np.float32)
        img_in /= 255.0
        img_in = np.expand_dims(img_in, axis=-1)
        img_in = np.expand_dims(img_in, axis=0)
        predictions = self.model.run(
            output_names=[self.output_layer_name],
            input_feed={self.input_layer_name: img_in},
        )[0]
        return self.class_names[predictions.argmax()]
