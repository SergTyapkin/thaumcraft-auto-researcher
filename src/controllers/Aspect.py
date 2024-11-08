import logging

from PIL import Image
from PyQt5.QtGui import QPixmap

from src.utils.constants import getAspectImagePath, UNKNOWN_ASPECT_IMAGE_PATH, EMPTY_ASPECT_SLOT_IMAGE_PATH
from src.utils.utils import loadImage


emptyAspectInventorySlotImage = loadImage(EMPTY_ASPECT_SLOT_IMAGE_PATH)


class Aspect:
    idx: int
    name: str
    image: Image.Image
    pixMapImage: QPixmap
    mask: Image.Image
    count: int = None

    def __init__(self, name: str, idx: int):
        self.name = name
        self.idx = idx

        imagePath = getAspectImagePath(self.name)
        try:
            self.image = loadImage(imagePath, emptyAspectInventorySlotImage)
            self.pixMapImage = QPixmap(imagePath)
        except Exception as e:
            logging.critical(f"Couldn't load image from path {imagePath}. Error: {e}")
            self.image = loadImage(UNKNOWN_ASPECT_IMAGE_PATH, emptyAspectInventorySlotImage)
            self.pixMapImage = QPixmap(UNKNOWN_ASPECT_IMAGE_PATH)
        imagePath = getAspectImagePath(self.name, colored=False)
        try:
            self.mask = Image.open(imagePath).convert("L")
        except Exception as e:
            logging.critical(f"Couldn't load image from path {imagePath} Error: {e}")
            self.mask = Image.open(UNKNOWN_ASPECT_IMAGE_PATH).convert("L")

    def __repr__(self):
        return f"{self.name}({self.count})"
