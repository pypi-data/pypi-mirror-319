# For normal user to use this model.
import os

os.environ["KERAS_BACKEND"] = "torch"

import pathlib
from typing import Any, Dict

import cv2
import keras
import numpy as np

from meter_detection.data_process import get_test_aug
from meter_detection.k.schema import ModelParams

params = ModelParams(root_dir="useless", NUM_KEYPOINTS=4)


class Detector:
  def __init__(self, model_path: str):
    self.model_path = model_path
    self.loaded_model = keras.saving.load_model(self.model_path)
    self.aug = get_test_aug(params)

  def detect_np(self, np_img: np.ndarray) -> Dict[str, Any]:
    # apply augmentation
    im = self.aug(image=np_img)
    assert im.shape == (224, 224, 3)

    # get 4 points
    results = self.loaded_model.predict(im[None])

    # 将 numpy 数组转换为嵌套列表
    # get labels.
    results_arr = results.reshape(-1, params.NUM_KEYPOINTS, 2) * params.IMG_SIZE
    points = results_arr.tolist()
    return {"points": points}

  def detect(self, img_path: pathlib.Path) -> Dict[str, Any]:
    """
    detect the meter reading area.

    return type is {"points": []}
    keypoints:
      point_1 = [self.data.data[i].xmin, self.data.data[i].ymin]
      point_2 = [self.data.data[i].xmax, self.data.data[i].ymin]
      point_3 = [self.data.data[i].xmax, self.data.data[i].ymax]
      point_4 = [self.data.data[i].xmin, self.data.data[i].ymax]
    """
    im = cv2.imread(img_path)
    return self.detect_np(np_img=im)
