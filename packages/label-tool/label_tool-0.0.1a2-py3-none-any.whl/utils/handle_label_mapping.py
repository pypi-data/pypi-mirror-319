import os
from typing import List


def handle_label_mapping(label_mapping: str) -> List[str]:
  label_mapping_file = os.path.abspath(label_mapping)
  # check mapping file
  if not os.path.exists(label_mapping_file):
    raise Exception(f"the mapping file {label_mapping_file} not exist")

  _, ext = os.path.splitext(label_mapping_file)
  if ext != '.txt':
    raise Exception("the extension of label mapping file must be .txt")

  # label mapping
  label_to_class_id = []
  with open(label_mapping_file, "r", encoding="utf-8") as f:
    for line in [line.strip() for line in f.readlines()]:
      label_to_class_id.append(line)

  return label_to_class_id
