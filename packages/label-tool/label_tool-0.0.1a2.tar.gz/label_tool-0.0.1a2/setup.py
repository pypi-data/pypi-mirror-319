from setuptools import setup, find_packages


# 读取 README 文件内容作为长描述
def get_long_description():
  """Read long description from README"""
  with open("README.md", encoding="utf-8") as f:
    long_description = f.read()
  return long_description


setup(
  name='label-tool',  # 包名
  version='0.0.1a2',  # 版本号
  author='leftover',  # 作者
  author_email='hi.leftover@qq.com',  # 作者邮箱
  description='A simple command-line interface tool',
  long_description=get_long_description(),  # 长描述，通常从 README.md 读取
  long_description_content_type='text/markdown',  # 长描述格式，通常为 Markdown
  url='https://github.com/left0ver/label-tool',
  license="MIT",
  keywords="label convert, labelme convert yolo, yolo convert labelme, labelme,yolo",
  packages=find_packages(),  # 自动查找包（所有目录下有 `__init__.py` 的目录会被认为是包）
  classifiers=[  # 分类，便于 Python 包索引 (PyPI) 查找
    "Intended Audience :: Developers",
    "Natural Language :: English",
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
  python_requires='>=3.10',
  install_requires=[
    'click>=8.0',
  ],
  entry_points={
    'console_scripts': [
      'lt=cli.cli:cli',
    ],
  },
  include_package_data=True,  # 包含额外的文件（如静态文件、配置文件等）
  zip_safe=False,  # 是否支持压缩包
)
