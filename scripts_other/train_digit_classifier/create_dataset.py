import json
import os
import pickle

import cv2
import numpy as np
import tqdm
from PIL import Image


def from_coco_dataset(json_path: str, imgs_dir_path: str) -> list[tuple[np.ndarray, int]]:
    """
    Забирает изображения цифр из coco датасета
    Args:
        json_path: Путь на coco json
        imgs_dir_path: Путь на папку с изображениями

    Returns:
        Список пар (изображение цифры, цифра)
    """
    with open(json_path) as file:
        config = json.load(file)

    # Загружаем изображения
    images = []
    for img_data in tqdm.tqdm(config["images"], desc="Loading images"):
        img_path = os.path.join(imgs_dir_path, img_data["file_name"])
        img = load_image(img_path)
        images.append(img)

    # Loading digit images
    X = []
    y = []
    for ann in tqdm.tqdm(config["annotations"], desc="Loading digit images"):
        category = ann["category_id"]
        if category in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:  # is digit category
            digit = category - 1
            bbox = ann["bbox"]
            digit_img = crop_bbox(
                images[ann["image_id"]],
                bbox
            )
            # digit_img = digit_img[:, 2: -5]
            X.append(digit_img)
            y.append(digit)
    return list(zip(X, y))


def load_image(path):
    image = Image.open(path)
    image = image.convert("L")  # grayscale
    image_np = np.array(image)
    return image_np


def draw_bbox(img, bbox):
    x, y, h, w = map(int, bbox)
    p1 = (x, y)
    p2 = (x + w, y + h)
    cv2.rectangle(img, p1, p2, (255, 0, 0), 1)


def crop_bbox(img, bbox):
    x, y, h, w = map(round, bbox)
    y = round(y + h * 0.05)
    h = round(h * 0.95)
    x = round(x + w * 0.1)
    w = round(w * 0.7)
    # h = round(h * 1.1)
    return img[y: y + h, x: x + w]


if __name__ == '__main__':
    paths = [
        ("inventory_aspects_quality_2-4/quality_2.coco.json", "inventory_aspects_quality_2-4/quality_2"),
        ("inventory_aspects_quality_2-4/quality_3.coco.json", "inventory_aspects_quality_2-4/quality_3"),
        ("inventory_aspects_quality_2-4/quality_4.coco.json", "inventory_aspects_quality_2-4/quality_4"),
        ("inventory_aspects_quality_5-6/quality_5.coco.json", "inventory_aspects_quality_5-6/quality_5"),
        ("inventory_aspects_quality_5-6/quality_6.coco.json", "inventory_aspects_quality_5-6/quality_6"),
    ]
    ds = []
    for p in paths:
        ds += from_coco_dataset(*paths[0])
    X = [d[0] for d in ds]
    y = [d[1] for d in ds]
    with open("dataset.pkl", "wb") as file:
        pickle.dump((X, y), file)
