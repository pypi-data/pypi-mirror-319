import json
import os
from typing import Tuple, List

import click
import cv2
from .config import SUPPORT_IMG_EXT
from .utils.statistics_helper import statistics_helper


def yolo_segment_to_labelme(txt_folder: str, img_folder: str, save_folder: str, labels_mapping: str, relative_path: str,
                            labelme_version: str, is_dir: bool) -> Tuple[int, List[str]]:
  """

  :param txt_folder: yolo label path
  :param img_folder: image path
  :param save_folder: output dir
  :param labels_mapping: label mapping file ,must endwith .txt
  :param relative_path: this path  of image relative the output
  :param labelme_version: the  labelme version
  :param is_dir: txt_folder and image_folder whether is dir
  :return: int, List[str] , successful_count and the list of failed_file
  """
  successful_count = 0
  fail_files = []
  txt_files = [txt_folder] if not is_dir else [os.path.join(txt_folder, txt_file)
                                               for txt_file in os.listdir(txt_folder)]
  img_files = [img_folder] if not is_dir else [os.path.join(img_folder, img_file)
                                               for img_file in os.listdir(img_folder)]

  # statistics all extension of the image
  temp_img_ext = set([os.path.splitext(img_file)[1] for img_file in img_files])
  img_ext = []
  for ext in temp_img_ext:
    # if it is a dir ,it will be empty string.
    if ext == "":
      continue
    else:
      if ext not in SUPPORT_IMG_EXT:
        raise Exception(f"{ext} image file not support,please commit a issue in github.")
      else:
        img_ext.append(ext)

    # TODO: 考虑多级目录
  img_folder = img_folder if is_dir else os.path.dirname(img_folder)
  for txt_file in txt_files:
    if txt_file.endswith(".txt"):
      possible_img_file = [os.path.join(img_folder, os.path.basename(txt_file.replace(".txt", ext)))
                           for ext in img_ext]
      for img_path in possible_img_file:
        # check image file exist
        if os.path.exists(img_path):
          img = cv2.imread(img_path)
          height, width, _ = img.shape

          # create labelme json data
          labelme_data = {
            "version": labelme_version,
            "flags": {},
            "shapes": [],
            # 需要图片的相对路径，需要根据实际修改
            "imagePath": os.path.join(relative_path, os.path.basename(img_path)),
            "imageHeight": height,
            "imageWidth": width,
            "imageData": None  # 可以选择将图像数据转为base64后嵌入JSON
          }

          # read yolo label file ,and write as labelme json
          with open(txt_file, "r") as file:
            for line in file.readlines():
              data = line.strip().split()
              class_id = int(data[0])  # 类别ID
              points = list(map(float, data[1:]))  # 获取多边形坐标

              # 将归一化坐标转换为实际像素坐标
              polygon = []
              for i in range(0, len(points), 2):
                x = points[i] * width
                y = points[i + 1] * height
                polygon.append([x, y])

              # 定义多边形区域
              shape = {
                "label": labels_mapping[class_id],  # 使用直接定义的类别名称
                "points": polygon,
                "group_id": None,
                "shape_type": "polygon",  # 分割使用多边形
                "flags": {}
              }
              labelme_data["shapes"].append(shape)
          save_path = os.path.join(save_folder, os.path.basename(txt_file).replace(".txt", ".json"))

          with open(save_path, "w", encoding="utf-8") as f:
            json.dump(labelme_data, f, indent=2, ensure_ascii=False)
            successful_count += 1
            # FIXME： 太长了会截断
            click.secho(f"successful convert: {os.path.basename(txt_folder)} ->{save_path}", fg="green")

          break
        # TODO： 添加-q 隐藏输出
      else:
        # all image file not exist
        fail_files.append(txt_file)
        click.secho(f"The image corresponding to '{txt_file}' does not exist ", fg="red", bold=True)

    else:
      # not endswith .txt
      click.secho(f"{txt_file} is not endWith .txt")
      fail_files.append(txt_file)

  return successful_count, fail_files
