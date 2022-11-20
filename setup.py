# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: setup.py
# @AUthor: Fei Wu
# @Time: 11月, 20, 2022
import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="FlowIncomePredict",
  version="0.0.1",
  author="Fei Wu",
  author_email="wufei.pku@163.com",
  description="package for match best sample to predict income or flow",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/wufeipku/FlowIncomePredict.git",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)