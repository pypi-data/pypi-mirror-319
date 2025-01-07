import os


def check_file_exist(file_path: str, throw: bool = True) -> bool:
  """

  :param file_path: abs path
  :param throw: decide if or not throw Exception
  :return:
  """
  if not os.path.exists(file_path):
    if throw:
      raise Exception(f"{file_path} is not exist")
    else:
      return False
  return True
