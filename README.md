<div align="center">
<!-- Title: -->
  <img src="https://raw.githubusercontent.com/maksyuki/TaichiGAME-res/main/logo.png" />
  <br />
  <br />
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
> NOTE: due to the final exam approaching, 

## Motivation
postgraduate project. Provide a python based, easy-to-use framework. 
## Why TaichiGAME

## Feature

- collision detection
  - broad phase
  - narrow phase

## What is missing

> Text that is a quote

## Requirements
1. python>=3.7, <=3.9, because:
   > - use `from __future__ import annotations` to postpone evaluation of annotations `(python3.7+ intro)`
   > - taichi now support the highest version of `python` is `python3.9`

2. taichi>=0.8.0
    > - for support taichi's new features
    > - now `TaichiGAME` don't use the new GGUI `(taichi0.8+ intro)`, so you maybe can use lower version taichi(such as `taichi0.7+`).
    > - **NOTE**: In views of the rapid development of `taichi`, we don't have much enery and time to maintain `TaichiGAME` to multiply different main version. So we decide to only maintain one current main verion plus one latest previous main verion. For now, that mean we develop and test all features of `taichiGAME` in `taichi0.8+` , and **only** maintain a latest previous `taichi0.7.32`.

## Install

installation is simple, you can just type the following command in `shell` or `cmd` terminal.
```shell
$ python3 -m pip install TaichiGAME
```

## Development
<details><summary>example code</summary>
<p>

#### We can hide anything, even code!

    ```ruby
      puts "Hello World"
    ```

</p>
</details>

### Structure
insert a class diagram/chart
### Algorithm
### Implement
## Contribution
If you want to contribute to TaichiGAME, be sure to review the [guidelines](CONTRIBUTING.md). This project adheres to TaichiGAME's [code_of_conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

We use GitHub issues for tracking requests and bugs, so please direct specific questions to [issues panel](https://github.com/maksyuki/TaichiGAME/issues).

The TaichiGAME project strives to abide by generally accepted best practices in open-source software development, so feel free to raise a issues :smile:

## License
All of the TaichiGAME codes are release under the [MIT License](LICENSE).

## Acknowledgement
1. Thank [yuanming-hu](https://github.com/yuanming-hu) and [taichi-team](https://github.com/taichi-dev) for creating and maintaining [taichi](https://github.com/taichi-dev/taichi), such an excellent programming language.
2. Thanks to [ACRL](https://github.com/AngryAccelerated) and his engine project [Physics2D](https://github.com/AngryAccelerated/Physics2D) which is with detailed introduction and relevant contents in [zhihu post](https://www.zhihu.com/people/acrl/posts). Due to him, I learned a tons of konwledges about graphics and physics engine from sratch.
3. Use [Inkscape 1.1.1 (3bf5ae0d25, 2021-09-20, window x64 version, GPL-3.0)](https://inkscape.org/) to draw the logo, flow and architecture diagrams. You can get all of resources in [TaichiGAME-res repo](https://github.com/maksyuki/TaichiGAME-res)

4. Use [GeoGebra (online, GPL-3.0)](https://www.geogebra.org/) to draw shapes to help debug computer geometry algorithm in TaichiGAME.

use it to draw this project logo


[^1]: _Foundations of Physically Based Modeling and Animation_ By Donald H. House, John C. Keyser
[^2]:


