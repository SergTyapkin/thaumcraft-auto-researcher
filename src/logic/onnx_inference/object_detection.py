from dataclasses import dataclass

import numpy as np
import onnxruntime
from PIL import Image


@dataclass
class ObjectPrediction:
    x: float  # Координаты центра рамки
    y: float  #
    width: float
    height: float
    predictionName: str
    confidence: float


class OnnxObjectDetection:
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

    def _predict_raw(self, img_in: np.ndarray) -> np.ndarray:
        """Performs object detection on the given image using the ONNX session.

        Args:
            img_in (np.ndarray): Input image as a NumPy array.

        Returns:
            Tuple[np.ndarray]: NumPy array representing the predictions, including boxes, confidence scores, and class confidence scores.
        """
        predictions = self.model.run(
            output_names=[self.output_layer_name],
            input_feed={self.input_layer_name: img_in},
        )[0]

        predictions = predictions.transpose(0, 2, 1)
        boxes = predictions[:, :, :4]
        class_confs = predictions[:, :, 4:]
        confs = np.expand_dims(np.max(class_confs, axis=2), axis=2)
        predictions = np.concatenate([boxes, confs, class_confs], axis=2)
        return predictions


    def predict(self, image: Image.Image) -> list[ObjectPrediction]:
        """Поиск аспектов на изображении image"""
        image = image.convert("RGB")
        preproc_image, returned_metadata = preprocess(image, self.img_height, self.img_width)
        predicted_arrays = self._predict_raw(preproc_image)
        postprocessed = postprocess(predicted_arrays, returned_metadata, self.img_height, self.img_width)[0]

        result = list(map(lambda prediction: ObjectPrediction(
            x=prediction[0] + abs(prediction[0] - prediction[2]) / 2,
            y=prediction[1] + abs(prediction[1] - prediction[3]) / 2,
            width=abs(prediction[0] - prediction[2]),
            height=abs(prediction[1] - prediction[3]),
            predictionName=self.class_names[int(prediction[6])],
            confidence=prediction[4],
        ), postprocessed))

        return result


def preprocess(
        image: Image.Image,
        height: int,
        width: int,
) -> tuple[np.ndarray, tuple[int, int]]:
    image_resized = image.resize((width, height))
    np_image = np.array(image)
    resized = np.array(image_resized)
    img_dims = tuple(np_image.shape[:2])
    img_in = np.transpose(resized, (2, 0, 1))
    img_in = img_in.astype(np.float32)
    img_in = np.expand_dims(img_in, axis=0)
    img_in /= 255.0
    return img_in, img_dims


def postprocess(
        predictions,
        img_dims,
        height: int,
        width: int,
        confidence: float = 0.4,
        iou_threshold: float = 0.3,
        max_detections: int = 300,
) -> list:
    """Postprocesses the object detection predictions.

    Args:
        predictions (np.ndarray): Raw predictions from the model.
        img_dims (List[Tuple[int, int]]): Dimensions of the images.
        confidence (float): Confidence threshold for filtering detections. Default is 0.5.
        iou_threshold (float): IoU threshold for non-max suppression. Default is 0.5.
        max_detections (int): Maximum number of final detections. Default is 300.
    """
    predictions = w_np_non_max_suppression(
        predictions,
        conf_thresh=confidence,
        iou_thresh=iou_threshold,
        max_detections=max_detections,
    )

    infer_shape = (height, width)
    predictions = post_process_bboxes(
        predictions,
        infer_shape,
        img_dims,
    )
    return predictions


def w_np_non_max_suppression(
        prediction,
        conf_thresh: float = 0.25,
        iou_thresh: float = 0.45,
        class_agnostic: bool = False,
        max_detections: int = 300,
        num_masks: int = 0,
        box_format: str = "xywh",
):
    """Applies non-maximum suppression to predictions.

    Args:
        prediction (np.ndarray): Array of predictions. Format for single prediction is
            [bbox x 4, max_class_confidence, (confidence) x num_of_classes, additional_element x num_masks]
        conf_thresh (float, optional): Confidence threshold. Defaults to 0.25.
        iou_thresh (float, optional): IOU threshold. Defaults to 0.45.
        class_agnostic (bool, optional): Whether to ignore class labels. Defaults to False.
        max_detections (int, optional): Maximum number of detections. Defaults to 300.
        num_masks (int, optional): Number of masks. Defaults to 0.
        box_format (str, optional): Format of bounding boxes. Either 'xywh' or 'xyxy'. Defaults to 'xywh'.

    Returns:
        list: List of filtered predictions after non-maximum suppression. Format of a single result is:
            [bbox x 4, max_class_confidence, max_class_confidence, id_of_class_with_max_confidence,
            additional_element x num_masks]
    """
    num_classes = prediction.shape[2] - 5 - num_masks

    np_box_corner = np.zeros(prediction.shape)
    if box_format == "xywh":
        np_box_corner[:, :, 0] = prediction[:, :, 0] - prediction[:, :, 2] / 2
        np_box_corner[:, :, 1] = prediction[:, :, 1] - prediction[:, :, 3] / 2
        np_box_corner[:, :, 2] = prediction[:, :, 0] + prediction[:, :, 2] / 2
        np_box_corner[:, :, 3] = prediction[:, :, 1] + prediction[:, :, 3] / 2
        prediction[:, :, :4] = np_box_corner[:, :, :4]
    elif box_format == "xyxy":
        pass
    else:
        raise ValueError(
            "box_format must be either 'xywh' or 'xyxy', got {}".format(box_format)
        )

    batch_predictions = []
    for np_image_i, np_image_pred in enumerate(prediction):
        filtered_predictions = []
        np_conf_mask = np_image_pred[:, 4] >= conf_thresh

        np_image_pred = np_image_pred[np_conf_mask]
        cls_confs = np_image_pred[:, 5: num_classes + 5]
        if (
                np_image_pred.shape[0] == 0
                or np_image_pred.shape[1] == 0
                or cls_confs.shape[1] == 0
        ):
            batch_predictions.append(filtered_predictions)
            continue

        np_class_conf = np.max(cls_confs, 1)
        np_class_pred = np.argmax(np_image_pred[:, 5: num_classes + 5], 1)
        np_class_conf = np.expand_dims(np_class_conf, axis=1)
        np_class_pred = np.expand_dims(np_class_pred, axis=1)
        np_mask_pred = np_image_pred[:, 5 + num_classes:]
        np_detections = np.append(
            np.append(
                np.append(np_image_pred[:, :5], np_class_conf, axis=1),
                np_class_pred,
                axis=1,
            ),
            np_mask_pred,
            axis=1,
        )

        np_unique_labels = np.unique(np_detections[:, 6])

        if class_agnostic:
            np_detections_class = sorted(
                np_detections, key=lambda row: row[4], reverse=True
            )
            filtered_predictions.extend(
                non_max_suppression_fast(np.array(np_detections_class), iou_thresh)
            )
        else:
            for c in np_unique_labels:
                np_detections_class = np_detections[np_detections[:, 6] == c]
                np_detections_class = sorted(
                    np_detections_class, key=lambda row: row[4], reverse=True
                )
                filtered_predictions.extend(
                    non_max_suppression_fast(np.array(np_detections_class), iou_thresh)
                )
        filtered_predictions = sorted(
            filtered_predictions, key=lambda row: row[4], reverse=True
        )
        batch_predictions.append(filtered_predictions[:max_detections])
    return batch_predictions


def non_max_suppression_fast(boxes, overlapThresh):
    """Applies non-maximum suppression to bounding boxes.

    Args:
        boxes (np.ndarray): Array of bounding boxes with confidence scores.
        overlapThresh (float): Overlap threshold for suppression.

    Returns:
        list: List of bounding boxes after non-maximum suppression.
    """
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []
    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
    # initialize the list of picked indexes
    pick = []
    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    conf = boxes[:, 4]
    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(conf)
    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]
        # delete all indexes from the index list that have
        idxs = np.delete(
            idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0]))
        )
    # return only the bounding boxes that were picked using the
    # integer data type
    return boxes[pick].astype("float")


def post_process_bboxes(
        predictions: list[list[float]],
        infer_shape: tuple[int, int],
        img_dim: tuple[int, int],
        resize_method: str = "Stretch to",
) -> list[list[list[float]]]:
    scaled_predictions = []
    for i, batch_predictions in enumerate(predictions):
        if len(batch_predictions) == 0:
            scaled_predictions.append([])
            continue
        np_batch_predictions = np.array(batch_predictions)
        predicted_bboxes = np_batch_predictions[:, :4]
        origin_shape = img_dim
        if resize_method == "Stretch to":
            predicted_bboxes = stretch_bboxes(
                predicted_bboxes=predicted_bboxes,
                infer_shape=infer_shape,
                origin_shape=origin_shape,
            )
        predicted_bboxes = clip_boxes_coordinates(
            predicted_bboxes=predicted_bboxes,
            origin_shape=origin_shape,
        )
        np_batch_predictions[:, :4] = predicted_bboxes
        scaled_predictions.append(np_batch_predictions.tolist())
    return scaled_predictions


def stretch_bboxes(
        predicted_bboxes: np.ndarray,
        infer_shape: tuple[int, int],
        origin_shape: tuple[int, int],
) -> np.ndarray:
    scale_height = origin_shape[0] / infer_shape[0]
    scale_width = origin_shape[1] / infer_shape[1]
    return scale_bboxes(
        bboxes=predicted_bboxes,
        scale_x=scale_width,
        scale_y=scale_height,
    )


def scale_bboxes(bboxes: np.ndarray, scale_x: float, scale_y: float) -> np.ndarray:
    bboxes[:, 0] *= scale_x
    bboxes[:, 2] *= scale_x
    bboxes[:, 1] *= scale_y
    bboxes[:, 3] *= scale_y
    return bboxes


def clip_boxes_coordinates(
        predicted_bboxes: np.ndarray,
        origin_shape: tuple[int, int],
) -> np.ndarray:
    predicted_bboxes[:, 0] = np.round(
        np.clip(predicted_bboxes[:, 0], a_min=0, a_max=origin_shape[1])
    )
    predicted_bboxes[:, 2] = np.round(
        np.clip(predicted_bboxes[:, 2], a_min=0, a_max=origin_shape[1])
    )
    predicted_bboxes[:, 1] = np.round(
        np.clip(predicted_bboxes[:, 1], a_min=0, a_max=origin_shape[0])
    )
    predicted_bboxes[:, 3] = np.round(
        np.clip(predicted_bboxes[:, 3], a_min=0, a_max=origin_shape[0])
    )
    return predicted_bboxes
