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
I am a postgraduate in school of astronautics and major in aerospace robot guidance, navigation and control. During my first year, I took a class on _advanced control theory_ and was taught many different control algorithms for estimating dynamic model, fitting state curves and so on.

When I carried out a research on asteroid rover's motion planning supported by NFSC(**National Natural Science Foundation of China**), I spent lots of time on learning c++ for writing parallel program to solve complex rigid body dynamics equations. To be honest, achieving all of the details, especially some c++ advanced features, made me thoroughly exhausted. I could not just focus on the algorithms and built rapid prototype to verify it. I searched online and found it have no open source, scientific-oriented, out-of-the-box tools or framework to execute such high performance rigid body motion computing. In that case, why not I built one?


When I ,

## Why TaichiGAME
postgraduate project. Provide a python based, easy-to-use framework. 

## Feature

- collision detection
  - broad phase
  - narrow phase

## What is missing

> Text that is a quote

## Requirements
1. python>=3.7, <=3.9, because:
   - use `from __future__ import annotations` to postpone evaluation of annotations `(python3.7+ intro)`
   - taichi now support the highest version of `python` is `python3.9`

2. taichi>=0.8.0, because:
    - for support taichi's new features
    - now `TaichiGAME` don't use the new GGUI `(taichi0.8+ intro)`, so you maybe can use lower version taichi(such as `taichi0.7+`).
    - **NOTE:** some `TaichiGAME`'s API is based on specific `taichi` features. In views of the rapid development of `taichi`, we don't have much enery and time to maintain `TaichiGAME` to adapt or be compatiable to multiple different major version of `taichi`. It can make `TaichiGAME` too verbose. So we decide to **only maintain TaichiGAME to adapt to current major verion plus one latest previous major verion of taichi**. For now, because a major version of `taichi` has not been released yet, we decide to **CHANGE** the '`major version`' of previous policy into '`minor version`'. Specifically, we develop and test all features of `TaichiGAME` in `taichi0.8+` , and **ONLY** maintain compatible version of `TaichiGAME` to `taichi0.7+`, the `TaichiGAME` based on `taichi<0.7+` will no longer be maintained.
      > **ATTENTION: This policy maybe be modified according to `taichi`'s development.**

## Install

installation is simple, you can just type the following command in `shell` or `cmd` terminal.
```shell
$ python3 -m pip install TaichiGAME
```

another method is `git clone` this repo and `pip install` dependencies.
```shell
$ git clone https://github.com/maksyuki/TaichiGAME.git
$ python3 -m pip install -r requirements.txt
```

> NOTE: Recommand use `venv` to isolate test environment from system directories, you can get more details from [Creation of virtual environments](https://docs.python.org/3/library/venv.html).

After installation, 
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
1. Thank [yuanming-hu](https://github.com/yuanming-hu) and [taichi-team](https://github.com/taichi-dev) for creating and maintaining [taichi](https://github.com/taichi-dev/taichi), such an excellent programming language. Meanwile, express thanks for [taichi-team](https://github.com/taichi-dev) to provide free and high-quality [taichi course](https://github.com/taichiCourse01).

2. Thanks to [ACRL](https://github.com/AngryAccelerated) and his engine project [Physics2D](https://github.com/AngryAccelerated/Physics2D). In addition, His [series posts](https://www.zhihu.com/people/acrl/posts) is full of detailed and understandable contents about graphcs and physics engine. Due to him, I learned a tons of konwledges from sratch.

3. Use [Inkscape 1.1.1 (3bf5ae0d25, 2021-09-20, window x64 version, GPL-3.0)](https://inkscape.org/) to draw the logo, flow and architecture diagrams. You can get all of resources in [TaichiGAME-res repo](https://github.com/maksyuki/TaichiGAME-res).

4. Use [GeoGebra (online, GPL-3.0)](https://www.geogebra.org/) to draw shapes to help debug computer geometry algorithm in TaichiGAME.


[^1]: _Foundations of Physically Based Modeling and Animation_ By Donald H. House, John C. Keyser
[^2]:


