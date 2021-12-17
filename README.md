<div align="center">
<!-- Title: -->
  <img src="https://raw.githubusercontent.com/maksyuki/TaichiGAME-res/main/logo.png">

<!-- Labels: -->
  <!-- First row: -->

  <a href="https://github.com/maksyuki/TaichiGAME/actions">
    <img src="https://img.shields.io/github/workflow/status/maksyuki/TaichiGAME/unit-test/main?label=unit-test&logo=github&style=flat-square">
  </a>
  <a href="https://app.codecov.io/gh/maksyuki/TaichiGAME/">
    <img src="https://img.shields.io/codecov/c/github/maksyuki/TaichiGAME/main?logo=codecov&style=flat-square">
  </a>
  <a href="https://github.com/maksyuki/TaichiGAME">
    <img src="https://img.shields.io/pypi/v/numpy?logo=pypi&style=flat-square">
  </a>
  <a href="https://github.com/maksyuki/TaichiGAME">
    <img src="https://img.shields.io/pypi/pyversions/numpy?logo=python&style=flat-square">
  </a>
  <!-- Second row: -->
  <br>

  <a href="https://github.com/maksyuki/TaichiGAME">
    <img src="https://img.shields.io/github/license/maksyuki/TaichiGAME?color=brightgreen&logo=github&style=flat-square">
  </a>
  <a href="https://github.com/maksyuki/TaichiGAME">
    <img src="https://img.shields.io/tokei/lines/github/maksyuki/TaichiGAME?style=flat-square">
  </a>
  <a href="https://github.com/google/yapf">
    <img src="https://img.shields.io/badge/code%20style-yapf-red?style=flat-square">
  </a>
  <a href="https://github.com/PyCQA">
    <img src="https://img.shields.io/badge/static%20checker-pylint%20pycodestyle-red?style=flat-square">
  </a>
  <a href="https://github.com/maksyuki/TaichiGAME/blob/main/CONTRIBUTING.md">
    <img src="https://img.shields.io/badge/contribution-welcome-brightgreen?style=flat-square">
  </a>
<!-- Short description: -->

  <h1></h1>
</div>


## Overview
TaichiGAME is aim to become a light simulation engine specific for **robot motion planning and control**. I hope to design powered by [taichi lang](https://github.com/taichi-dev/taichi).

## Motivation
postgraduate project. Provide a python based, easy-to-use framework
## Why TaichiGAME

## Feature

1. Minkowski[^1]
2. collision detection
  2.1

## What is missing

## Requirements
1. python>=3.7, <=3.9
    1. use the 'from __future__ import annotations' to make type hints in class **(python3.7+ intro)**
    2. support type hints

2. taichi>=0.8.0
    1. now TaichiGAME don't use the new GGUI **(taichi0.8+ intro)**, so maybe low version taichi can work well

## Install

```shell
$ python3 -m pip install TaichiGAME
```

## Development
### Structure
### Algorithm
### Implement
## Contribution
If you want to contribute to TaichiGAME, be sure to review the [guidelines](CONTRIBUTING.md). This project adheres to TaichiGAME's [code_of_conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

We use GitHub issues for tracking requests and bugs, so please direct specific questions to [issues panel](https://github.com/maksyuki/TaichiGAME/issues).

The TaichiGAME project strives to abide by generally accepted best practices in open-source software development, so feel free to raise a issues :smile:

## Reference

## License
All of the TaichiGAME codes are release under the [MIT License](LICENSE).

## Acknowledgement
1. Thanks to [yuanming-hu](https://github.com/yuanming-hu) and [taichi-team](https://github.com/taichi-dev) to create and maintain [taichi](https://github.com/taichi-dev/taichi)
2. Thanks to [ACRL](https://github.com/AngryAccelerated) and his engine project [Physics2D](https://github.com/AngryAccelerated/Physics2D), which I learn a tons of konwledges from his [zhihu post](https://www.zhihu.com/people/acrl/posts).
3. Use [Inkscape 1.1.1 (3bf5ae0d25, 2021-09-20, window x64 version, GPL-3.0)](https://inkscape.org/) to draw the logo, flow and architecture diagrams. You can find all resources in [TaichiGAME-res repo](https://github.com/maksyuki/TaichiGAME-res)

use it to draw this project logo



## Reference

[1] _Real-time High-Quality Rendering of Non-Rotating Black Holes_ Eric Bruneton arXiv:2010.08735

