# CMake 相关

## 1 构建最小项目

- CMake 支持大写、小写和混合大小写命令、

```
mkdir build
cd build
cmake -G"MinGW Makefiles" ..
cmake --build .
```

之后会生成可执行文件

```text
step1/
    build/
    CMakeLists.txt
    tutorial.cpp
```

## 2 优化 CMakeLists. txt 文件

```cmake
cmake_minimum_required(VERSION 3.15)

# set the project name
project(Tutorial)

SET(SRC_LIST tutorial.cpp)

# add the executable
add_executable(${PROJECT_NAME} ${SRC_LIST})
```

1.0.2 分别对应 MAJOR MINOR PATCH

- set 和 PROJECT_NAME
- 添加版本号和配置头文件
- 添加编译时间戳
- 指定 C++标准
- 添加库（添加库的位置，库文件名，头文件名）
- 将库设置为可选项（分经典和现代）
- 添加库的使用要求
	- INTERFACE
	- PRIVATE
	- PUBLIC
	- 静态链接库/动态链接库
- build 目录介绍

## links

- [Site Unreachable](https://www.runoob.com/cmake/cmake-tutorial.html)
- [IPADS新人培训第二讲：CMake\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV14h41187FZ/)
