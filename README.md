# 随机地图生成器

RMG（Random Map Generator），随机地图生成器。主要核心算法是随机地图的生成，该项目额外使用 PyQt6 和 Pygame 开发了应用程序，对地图进行了展示。

## 安装说明

1. 安装

    使用以下命令下载。

    ```bash
    $ git clone git@github.com:glzteam/RMG.git
    ```

    或者下载 zip 均可。

2. 使用

    依次使用以下命令安装 python 库

    ```bash
    $ pip install pygame
    $ pip install PyQt6
    $ pip install PyQt6-Fluent-Widgets -i https://pypi.org/simple/
    $ pip install mysql-connector
    ```

## 使用说明

1. 使用地图生成算法

    vs01 下即为 C++ 编写的地图生成算法。

2. 使用Pygame游戏

    python_game 下即为 pygame 编写的地图游戏。

3. 使用应用程序

    直接运行 main.py 即可打开应用程序。

> pages 文件夹下为使用 PyQt6 于 PyQt6-fluent-ui 编写的各个页面。
>
> minesql.py 是使用 mysq 数据库管理数据的文件。

## 技术栈

1. 地图生成算法

    编程语言：C++。

2. 游戏编写

    编程语言：python。

    使用库：pygame。

3. 应用程序编写

    编程语言：python。

    使用库：

    - PyQt6 完成框架设计。
    -  PyQt6-Fluent-Widgets -i https://pypi.org/simple/ 完成 UI 设计。
    - mysql-connector 完成数据库设计。

## 贡献指南

如果有任何问题于建议，请在 issue 中提出。

## 许可证

本项目使用 GPLv3 进行许可。