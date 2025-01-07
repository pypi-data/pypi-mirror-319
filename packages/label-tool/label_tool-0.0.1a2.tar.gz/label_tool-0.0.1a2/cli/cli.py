import os
import typing as t

import click
from click._compat import term_len
from click.formatting import measure_table, iter_rows, wrap_text

from .yolo_segment_to_labelme import yolo_segment_to_labelme
from .config import SUPPORT_TYPE, DEFAULT_LABELME_VERSION
from .utils import handle_label_mapping, statistics_helper

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# TODO： 添加一个交互式的选项 -i 可以交互式地运行
class CustomHelpFormatter(click.HelpFormatter):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def write_heading(self, heading):
    """自定义帮助文本标题的格式"""
    self.write(f"{'':>{self.current_indent}}{click.style(heading, fg='green')}:\n")

  def write_dl(
          self,
          rows: t.Sequence[t.Tuple[str, str]],
          col_max: int = 30,
          col_spacing: int = 2,
  ) -> None:
    # copy from click
    rows = list(rows)
    widths = measure_table(rows)
    if len(widths) != 2:
      raise TypeError("Expected two columns for definition list")

    first_col = min(widths[0], col_max) + col_spacing

    for first, second in iter_rows(rows, len(widths)):
      self.write(f"{'':>{self.current_indent}}{click.style(first, fg=(111, 201, 189), bold=True)}")
      if not second:
        self.write("\n")
        continue
      if term_len(first) <= first_col - col_spacing:
        self.write(" " * (first_col - term_len(first)))
      else:
        self.write("\n")
        self.write(" " * (first_col + self.current_indent))

      text_width = max(self.width - first_col - 2, 10)
      wrapped_text = wrap_text(second, text_width, preserve_paragraphs=True)
      lines = wrapped_text.splitlines()

      if lines:
        self.write(f"{lines[0]}\n")

        for line in lines[1:]:
          self.write(f"{'':>{first_col + self.current_indent}}{line}\n")
      else:
        self.write("\n")


click.Context.formatter_class = CustomHelpFormatter


# TODO: 添加进度条

@click.group("lt", options_metavar='<options>', subcommand_metavar="command", context_settings=CONTEXT_SETTINGS)
def cli():
  """a tool to convert label between yolo and labelme"""
  pass


# TODO: 修改epilog
@click.command("yolo2json", context_settings=CONTEXT_SETTINGS,
               options_metavar='<options>',
               short_help="convert yolo label to labelme label",
               epilog="see https://github.com/left0ver/label-tool for more information")
# TODO：自定义path的异常处理
@click.argument("input", metavar='input', type=click.Path(exists=True, resolve_path=True, readable=True),
                required=True, )
@click.option("-i", "--image", type=click.Path(exists=True, resolve_path=True, readable=True), required=True,
              metavar="<file_path>",
              help="image file or image dir")
@click.option("-m", "--mapping", "label_mapping", type=click.Path(exists=True, resolve_path=True, readable=True),
              required=True, metavar="<file_path>",
              help="labelme mapping between labelme and yolo")
@click.option("-o", "--output", type=click.Path(resolve_path=True, dir_okay=True), default="output", required=True,
              show_default=True, metavar="<file_path>", help="image file or image dir")
@click.option("-t", "--type", type=click.Choice(SUPPORT_TYPE, case_sensitive=False), default=SUPPORT_TYPE[0],
              help=f"label type，可选值{SUPPORT_TYPE}")
@click.option("-v", "--version", "labelme_version", default=DEFAULT_LABELME_VERSION, metavar='',
              help=f"labelme version,default={DEFAULT_LABELME_VERSION}")
def yolo2json(input, image, label_mapping, output, type, labelme_version):
  input_label_isdir = os.path.isdir(input)
  input_image_isdir = os.path.isdir(image)
  if input_label_isdir != input_image_isdir:
    raise Exception(
      f"{'input label file is dir' if input_label_isdir else 'input label file is not dir'} and {'input_image is dir' if input_image_isdir else 'input_image is not dir'}")
  is_dir = input_label_isdir
  relative_path = os.path.relpath(image if is_dir else os.path.dirname(image), os.path.basename(output))

  label_mapping = handle_label_mapping(label_mapping)
  # create it if not exist
  if not os.path.exists(output):
    os.mkdir(output)
  match type:
    case "segment":
      successful_count, fail_files = yolo_segment_to_labelme(input, image, output, label_mapping, relative_path,
                                                             labelme_version, is_dir)
    case 'detect':
      # TODO:
      pass
    case _:
      raise Exception(f"only support label type include {SUPPORT_TYPE}")

  statistics_helper(successful_count, fail_files)

cli.add_command(yolo2json)
if __name__ == '__main__':
  cli()
