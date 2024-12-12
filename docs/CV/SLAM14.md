# 视觉SLAM十四讲

## 1 预备知识

### 1.1 本书讲什么

simultaneous localization and mapping

- 定位
- 地图构建
- 背景知识:
	- 射影几何
	- 计算机视觉
	- 状态估计理论
	- 李群与李代数

### 1.2 如何使用本书

#### 1.2.1 组织方式

- 数学基础篇
	- ![QQ_1725118522621.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408312335787.png)
- 实践应用篇
	- ![QQ_1725118558994.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202408312336762.png)

#### 1.2.2 代码

[GitHub - gaoxiang12/slambook2: edition 2 of the slambook](https://github.com/gaoxiang12/slambook2)

#### 1.2.3 面向的读者

- 基础知识:
	- 高数线代概率论
	- C++语言基础（C++标准库，模板类，一部分 C++11 ）
	- Linux 基础

### 1.3 风格约定

### 1.4 致谢和声明

### 1.5 习题

- **题目**：有线性方程 \(A x=b\)，若已知 \(A, b\)，需要求解 x，该如何求解？这对 A 和 b 有哪些要求？提示：从 A 的维度和秩角度来分析。
   - **答案**：线性方程组 $Ax = b$ 可以通过多种方法求解，如高斯消元法、矩阵逆法等。要求 \(A\) 是一个方阵且可逆（即 \(A\) 的行列式不为零），这样方程才有唯一解。如果 \(A\) 不是方阵，需要 \(A\) 的秩等于列数且等于增广矩阵 $\displaystyle [A|b]$ 的秩，这样方程组才有解。
- **题目**：高斯分布是什么？它的一维形式是什么样子？它的高维形式是什么样子？
   - **答案**：高斯分布，也称为正态分布，是一种连续概率分布。一维高斯分布的数学表达式为 $\displaystyle f (x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$，其中 $\displaystyle \mu$ 是均值，$\displaystyle \sigma$ 是标准差。高维高斯分布是一维高斯分布在多维空间的推广，其概率密度函数为 $\displaystyle N (\mathbf{x}; \mathbf{\mu}, \Sigma)$，其中 $\displaystyle \mathbf{\mu}$ 是均值向量，$\displaystyle \Sigma$ 是协方差矩阵。
- **题目**：你知道 C++11 标准吗？你听说过或用过其中哪些新特性？有没有其他的标准？
   - **答案**：是的，C++11 是 C++ 语言的一个重要标准，它引入了许多新特性，如自动类型推导（auto）、基于范围的 for 循环、lambda 表达式、智能指针等。除了 C++11，还有 C++14、C++17 和 C++20 等后续标准，它们也引入了新的特性和改进。
- **题目**：如何在 Ubuntu 系统中安装软件（不打开软件中心的情况下）？这些软件被安装在什么地方？如果只知道模糊的软件名称（比如想要装一个名称中含有 Eigen 的库），应该如何安装它？
   - **答案**：
   - 软件安装：在 Ubuntu 中，可以使用命令行工具 `apt` 来安装软件。基本命令为 `sudo apt install [package-name]`。
   - 安装位置：软件通常被安装在 `/usr/` 目录下，但具体的文件可能分布在多个子目录中。
   - 模糊名称安装：如果只知道软件名称的一部分，可以使用 `apt search` 命令来搜索。例如，`sudo apt search eigen` 可以帮助找到所有包含 "eigen" 的软件包。
- **题目**：*花一个小时学习 Vim，因为你迟早会用它。你可以在终端中输入 vimtutor 阅读一遍所有内容。我们不需要你非常熟练地操作它，只要能够在学习本书的过程中使用它输入代码即可。不要在它的插件上浪费时间，不要想着把 Vim 用成 IDE，我们只用它做文本编辑的工作。
   - **答案**:
	- vim 根本不熟练捏

## 2 初识 SLAM

### 2.1 引子: 小萝卜的例子

- 自主运动能力
- 感知周边环境
	- 状态
	- 环境
- 安装于环境中（不太好反正）
- 机器人本体上
	- 激光 SLAM
	- 视觉 SLAM（本书重点）
		- 单目（Monocular）
			- 只能用一个摄像头
			- 距离感
				- motion
				- Structure
				- Disparity
				- Scale
					- Scale Ambiguity
				- 但是无法确定深度
		- 双目（Sterco）
			- 两个相机的距离（基线 Baseline）已知
			- 配置与标定比较复杂
		- 深度（RGB-D）
			- 红外结构关 Time-of-Flight（ToF）
			- 主要用在室内，室外会有很多影响
		- 还有一些非主流的: 全景，Event

### 2.2 经典视觉 SLAM 框架

- ![QQ_1725120955824.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409010016267.png)![QQ_1725121088279.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409010018113.png)
- 在外界换几个比较稳定的情况下，SLAM 技术已经比较成熟

#### 2.2.1 视觉里程计

- 只通过视觉里程计来估计轨迹会出现累积漂移（Accumulating Drift）。
- 所以需要回环检测与后端优化

#### 2.2.2 后端优化

 - 最大后验概率估计（Maximum-a-Posteriori MAP）
 - 前端
	 - 图像的特征提取与匹配
 - 后端
	 - 滤波与非线性算法
 - 对运动主体自身和周围环境空间不确定性的估计

#### 2.2.3 回环检测

- 闭环检测
- 识别到过的场景
- 利用图像的相似性

#### 2.2.4 建图

- 度量地图
	- Sparse
		- Landmark
		- 定位用
	- Dense
		- Grid / Vocel
		- 导航用
- 拓扑地图  
	Graph

### 2.3 SLAM 问题的数学表述

- 运动方程
	- $\displaystyle \quad\boldsymbol{x}_k=f\left(\boldsymbol{x}_{k-1},\boldsymbol{u}_k,\boldsymbol{w}_k\right).$
		- $\displaystyle \boldsymbol{u}_{k}$ 是运动传感器的输入
		- $\displaystyle \boldsymbol{w}_{k}$ 是过程中加入的噪声
- 观测方程
	- $\displaystyle \boldsymbol{z}_{k,j} = h (\boldsymbol{y}_{j},\boldsymbol{x}_{k},\boldsymbol{v}_{k,j})$
		- $\displaystyle \boldsymbol{v}_{k,j}$ 是观测里的噪声
- 又很多参数化的方式
- 可以总结为如下两个方程

$$
\begin{cases}\boldsymbol{x}_k=f\left(\boldsymbol{x}_{k-1},\boldsymbol{u}_k,\boldsymbol{w}_k\right),&k=1,\cdots,K\\\boldsymbol{z}_{k,j}=h\left(\boldsymbol{y}_j,\boldsymbol{x}_k,\boldsymbol{v}_{k,j}\right),&(k,j)\in\mathcal{O}\end{cases}.
$$

- 知道运动测量的读数 $\displaystyle \boldsymbol{u}$ 和传感器的读数 $\displaystyle \boldsymbol{z}$，如何求解定位问题和建图问题。
	- 状态估计问题: 如何通过带有噪声的测量数据，估计内部的、隐藏着的状态变量
- Linear Gaussian -> Kalman Filter
- Non-Linear Non-Gaussian -> Extended Kalman Filter 和非线性优化
- EKF -> Particle Filter -> Graph Optimization

### 2.4 实践: 编程基础

#### 2.4.1 安装 Linux 操作系统

#### 2.4.2 Hello SLAM

#### 2.4.3 使用 cmake

```
cmake_minimum_required( VERSION 2.8)

project(HelloSLAM)

add_executable(helloSLAM helloSLAM.cpp)
```

对中间文件的处理:

```
mkdir build
cd build
cmake ..
make
```

#### 2.4.4 使用库

```
add_library(hello libHelloSLAM.cpp)
```

- 静态库
	- .a 作为后缀名，每次调用都有一个副本
- 共享库
	- .so，只有一个副本

```
add_library(hello_shared SHARED libHelloSLAM.cpp)
```

- 还要一个头文件来说明库里都有什么

```
#ifndef LIBHELLOSLAM_H_
#define LIBHELLOSLAM_H_

void printHello()

#endif
```

- 最后写一个可执行程序:

```c++
#include "libHelloSLAM.h"

int main(int argc, char **argv) {
	printHello();
	return 0;	
}
```

- 在 CMakeLists. txt 中添加可执行命令的生成命令，链接到库上:

```
add_executable(useHello useHello.cpp)
target_link_libraries(useHello hello_shared)
```

#### 2.4.5 使用 IDE

- KDevelop
- Clion
- 还没写

## 3 三维空间刚体运动

### 3.1 旋转矩阵

#### 3.1.1 点、向量和坐标系

- Skew-symmetric Matrix

$$
a\times b = 
\begin{Vmatrix}e_1&e_2&e_3\\ \\
a_1&a_2&a_3\\ \\
b_1&b_2&b_3 \\
\end{Vmatrix}
=
\begin{bmatrix}
a_2b_3-a_3b_2\\ \\
a_3b_1-a_1b_3\\ \\
a_1b_2-a_2b_1 
\end{bmatrix}
=
\begin{bmatrix} 
0&-a_3&a_2\\ \\
a_3&0&-a_1\\ \\
-a_2&a_1&0 
\end{bmatrix}
\boldsymbol{b}\overset{\mathrm{def}}{\operatorname*{=}}\boldsymbol{a}^{\wedge}\boldsymbol{b}.
$$

- 于是就把外积变成了线性运算
- 即

$$
\displaystyle \boldsymbol{a}^{\wedge}=\begin{bmatrix}
0  & -a_{3}  & a_{2} \\
a_{3} & 0 & -a_{1} \\
-a_{2} & a_{1} & 0
\end{bmatrix}
$$

#### 3.1.2 坐标系间的欧式变换

- Euclidean Transform

$$
\begin{bmatrix}a_1\\ \\
a_2\\\\a_3\end{bmatrix}=\begin{bmatrix}e_1^\mathrm{T}e_1^{\prime}&e_1^\mathrm{T}e_2^{\prime}&e_1^\mathrm{T}e_3^{\prime}\\e_2^\mathrm{T}e_1^{\prime}&e_2^\mathrm{T}e_2^{\prime}&e_2^\mathrm{T}e_3^{\prime}\\e_3^\mathrm{T}e_1^{\prime}&e_3^\mathrm{T}e_2^{\prime}&e_3^\mathrm{T}e_3^{\prime}\end{bmatrix}\begin{bmatrix}a_1^{\prime}\\\\a_2^{\prime}\\\\a_3^{\prime}\end{bmatrix}\stackrel{\mathrm{def}}{=}Ra^{\prime}
$$

- $\displaystyle \boldsymbol{R}$ 是旋转矩阵、方向余弦矩阵
- Special Orthogonal Group $\displaystyle \mathrm{SO}(n)=\{\boldsymbol{R}\in \mathbb{R}^{n \times n}|\boldsymbol{R}\boldsymbol{R}^{\mathrm{T}}=\boldsymbol{I},\det(\boldsymbol{R})=1\}$
- $\displaystyle a^{\prime}=R^{-1}a=R^{\intercal}a.$
- 旋转+平移: $\displaystyle a^{\prime}=Ra+t.$

#### 3.1.3 变换矩阵与齐次坐标

- 但是这里的变换关系不是一个线性关系
- $\displaystyle c=R_2\left(R_1a+t_1\right)+t_2$
- 我们改写一下形式:
	- $\displaystyle \begin{bmatrix}a'\\\\1\end{bmatrix}=\begin{bmatrix}R&t\\\\\mathbf{0}^\mathrm{T}&1\end{bmatrix}\begin{bmatrix}a\\\\1\end{bmatrix}\overset{\mathrm{def}}{=}T\begin{bmatrix}a\\\\1\end{bmatrix}$
	- 这就是齐次坐标，$\displaystyle \boldsymbol{T}$ 称为变换矩阵（Transform matrix）
- $\displaystyle \tilde{b}=T_1\tilde{\boldsymbol{a}}, \tilde{\boldsymbol{c}}=T_2\tilde{\boldsymbol{b}}\quad\Rightarrow\tilde{\boldsymbol{c}}=T_2T_1\tilde{\boldsymbol{a}}.$
- 并且 $\displaystyle \boldsymbol{T}$ 称为特殊欧式群（Special Euclidean Group）
	- $\displaystyle \mathrm{SE}(3)=\left\{T=\begin{bmatrix}R&t\\\mathbf{0}^\mathrm{T}&1\end{bmatrix}\in\mathbb{R}^{4\times4}|\boldsymbol{R}\in\mathrm{SO}(3),\boldsymbol{t}\in\mathbb{R}^3\right\}$
- $\displaystyle T^{-1}=\begin{bmatrix}R^\mathrm{T}&-R^\mathrm{T}t\\0^\mathrm{T}&1\end{bmatrix}$
- 在 C++程序中可以使用运算符重载来处理齐次和非齐次的情况

### 3.2 实践:Eigen

```C++
#include <iostream>
using namespace std;

#include <ctime>

#include <eigen3>
using namespace Eigen;

#define MATRIX_SIZE 50

int main(int argc, char **argv) {
    Matrix<float, 2, 3> matrix_23;
// 如下都是三维向量
    Vector3d v_3d;
    Matrix<float, 3, 1> vd_3d;
// 如下是3*3矩阵
    Matrix3d matrix_33 = Matrix3d::Zero();
// 两个动态分配
    Matrix<double, Dynamic, Dynamic> matrix_dynamic;
    MatrixXd matrix_x;

    matrix_23 << 1, 2, 3, 4, 5, 6;
    cout<< "matrix 2*3 from 1 to 6: \n" << matrix_23 << endl;

    cout << "print matrix 2*3:" << endl;
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 3; j+) cout << matrix_23(i, j) << "\t";
        cout << endl;
    }

    v_3d << 3, 2, 1;
    vd_3d << 4, 5, 6;
    
    Matrix<double, 2, 1> result = matrix_23.cast<double>() * v_3d;
    cout << "[1, 2, 3; 4, 5, 6] * [3, 2, 1] =" << result.transpose() << endl;

    matrix_22 = Matrix3d::Random();

    // 一些矩阵的操作:
    // transpose()
    // sum()
    // trace()
    // inverse()
    // determinant()
    
    SelfAdjointEigenSolver<Matrix3d> eigen_solver(matrix_33.transpose() * matrix_33);
    cout << eigen_solver.eigenvalues() << endl;
    cout << eigen_solver.eigenvectors() << endl;

    // solve the equation
    Matrix<double, MATRIX_SIZE, MATRIX_SIZE> matrix_NN = MatrixXd::Random(MATRIX_SIZE, MATRIX_SIZE);
    matrix_NN = matrix_NN * matrix_NN.transpose()
    Matrix<double, MATRIX_SIZE, 1> v_Nd = MatrixXd::random(MATRIX_SIZE, 1);

    // 第一种:直接求逆
    Matrix<double, MATRIX_SIZE, 1> x = matrix_NN.inverse() * v_Nd;

    // 第二种:矩阵分解
    x = matrix_NN.colPivHouseholderQr().solve(v_Nd);
    
}
```

- Eigen 不支持自动类型提升，即不会隐式转换

### 3.3 旋转向量和欧拉角

#### 3.3.1 旋转向量

- Axis-Angle
- Rodrigues's Formula
	- $\displaystyle \boldsymbol{R}=\cos\theta\boldsymbol{I}+\left(1-\cos\theta\right)\boldsymbol{n}\boldsymbol{n}^\mathrm{T}+\sin\theta\boldsymbol{n}^\mathrm{\wedge}.$

$$
\begin{aligned}
\mathrm{tr}\left(R\right)& =\cos\theta\operatorname{tr}\left(\boldsymbol{I}\right)+\left(1-\cos\theta\right)\operatorname{tr}\left(\boldsymbol{n}\boldsymbol{n}^\mathrm{T}\right)+\sin\theta\operatorname{tr}(\boldsymbol{n}^\mathrm{\Lambda}) \\
&=3\cos\theta+(1-\cos\theta) \\
&=1+2\cos\theta 
\end{aligned}
$$

thus:

$$
\theta=\arccos\frac{\mathrm{tr}(R)-1}{2}.
$$

$$
Rn=n.
$$

- 即 $\displaystyle \boldsymbol{n}$ 是矩阵 $\displaystyle \boldsymbol{R}$ 特征值 1 对应的特诊向量

#### 3.3.2 欧拉角

- 比较常用的一种 yaw-pitch-roll
	- ZYX
- 但会有 Gimbal Lock 问题
	- 所以欧拉角比较适合用于快速检验结果是否有错

### 3.4 四元数

#### 3.4.1 四元数的定义

- 我们找不到不带奇异性的三位向量描述方式
	- 找不到一个流形？
- Quaternion
	- 紧凑又没有奇异性
	- 只是不够直观+运算复杂
- $\displaystyle q=q_0+q_1\mathrm{i}+\mathrm{q}_2\mathrm{j}+\mathrm{q}_3\mathrm{k}$

$$
\begin{cases}\mathbf{i}^2=\mathbf{j}^2=\mathbf{k}^2=-1\\\mathbf{ij}=\mathbf{k},\mathbf{ji}=-\mathbf{k}\\\mathbf{jk}=\mathbf{i},\mathbf{kj}=-\mathbf{i}\\\mathbf{ki}=\mathbf{j},\mathbf{ik}=-\mathbf{j}\end{cases}
$$

- (也许可以用度规来表示？)
- $\displaystyle \boldsymbol{q}=\left[s,\boldsymbol{v}\right]^\mathrm{T},\quad s=q_0\in\mathbb{R},\quad\boldsymbol{v}=\left[q_1,q_2,q_3\right]^\mathrm{T}\in\mathbb{R}^3.$
- 书上没写直观的几何对应

#### 3.4.2 四元数的运算

- 乘法: $\displaystyle \boldsymbol{q}_a\boldsymbol{q}_b=\begin{bmatrix}s_as_b-\boldsymbol{v}_a^\mathrm{T}\boldsymbol{v}_b,s_a\boldsymbol{v}_b+s_b\boldsymbol{v}_a+\boldsymbol{v}_a\times\boldsymbol{v}_b\end{bmatrix}^\mathrm{T}.$
	- 由于最后一项的存在，乘法不具有交换律
- 共轭: $\displaystyle q_a^*=s_a-x_a\mathrm{i}-\mathrm{y_aj}-\mathrm{z_ak}=[\mathrm{s_a},-\mathrm{v_a}]^\mathrm{T}.$
	- $\displaystyle q^*q=qq^*=[s_a^2+\boldsymbol{v}^\mathrm{T}\boldsymbol{v},\boldsymbol{0}]^\mathrm{T}.$
- 逆: $\displaystyle q^{-1}=q^*/\|q\|^2.$
	- $\displaystyle (\boldsymbol{q}_a\boldsymbol{q}_b)^{-1}=\boldsymbol{q}_b^{-1}\boldsymbol{q}_a^{-1}.$

#### 3.4.3 用四元数表示旋转

- 先表示三维空间点:
	- $\displaystyle p=[0,x,y,z]^{\mathrm{T}}=[0,\boldsymbol{v}]^{\mathrm{T}}.$
- 再旋转:
	- $\displaystyle p'=qpq^{-1}.$

#### 3.4.4 四元数到其他旋转表示的转换

- 设 $\displaystyle \boldsymbol{q} = [s,\boldsymbol{v}]^\mathrm{T}$
	- $\displaystyle \boldsymbol{q}^+=\begin{bmatrix}s&-\boldsymbol{v}^\mathrm{T}\\\\\boldsymbol{v}&s\boldsymbol{I}+\boldsymbol{v}^\wedge\end{bmatrix},\quad\boldsymbol{q}^\oplus=\begin{bmatrix}s&-\boldsymbol{v}^\mathrm{T}\\\\\boldsymbol{v}&s\boldsymbol{I}-\boldsymbol{v}^\wedge\end{bmatrix}.$
	- $\displaystyle q_1^+q_2=\begin{bmatrix}s_1&-\boldsymbol{v}_1^\mathrm{T}\\\\\boldsymbol{v}_1&s_1\boldsymbol{I}+\boldsymbol{v}_1^\wedge\end{bmatrix}\begin{bmatrix}s_2\\\\\boldsymbol{v}_2\end{bmatrix}=\begin{bmatrix}-\boldsymbol{v}_1^\mathrm{T}\boldsymbol{v}_2+s_1s_2\\\\s_1\boldsymbol{v}_2+s_2\boldsymbol{v}_1+\boldsymbol{v}_1^\wedge\boldsymbol{v}_2\end{bmatrix}=\boldsymbol{q}_1\boldsymbol{q}_2.$
	- 同理可证:
		- $\displaystyle q_1q_2=q_1^+q_2=q_2^\oplus q_1.$
- 再来考虑旋转:
	- $\displaystyle \begin{aligned}p^{\prime}&=qpq^{-1}=q^{+}p^{+}q^{-1}\\&=q^{+}q^{-1^{\oplus}}p.\end{aligned}$
	- 于是可以得到:
		- $\displaystyle \boldsymbol{q}^{+}\big(\boldsymbol{q}^{-1}\big)^{\oplus}=\begin{bmatrix}s&-\boldsymbol{v}^{\mathrm{T}}\\\boldsymbol{v}&s\boldsymbol{I}+\boldsymbol{v}^{\wedge}\end{bmatrix}\begin{bmatrix}s&\boldsymbol{v}^{\mathrm{T}}\\-\boldsymbol{v}&s\boldsymbol{I}+\boldsymbol{v}^{\wedge}\end{bmatrix}=\begin{bmatrix}1&\boldsymbol{0}\\\boldsymbol{0}^{\mathrm{T}}&\boldsymbol{v}\boldsymbol{v}^{\mathrm{T}}+s^{2}\boldsymbol{I}+2s\boldsymbol{v}^{\wedge}+\left(\boldsymbol{v}^{\wedge}\right)^{2}\end{bmatrix}.$
		- 即: $\displaystyle R=\boldsymbol{v}\boldsymbol{v}^\mathrm{T}+s^2\boldsymbol{I}+2s\boldsymbol{v}^\wedge+\left(\boldsymbol{v}^\wedge\right)^2.$

$$
\begin{aligned}
\operatorname{tr}(R)& =\mathbf{tr}(\boldsymbol{vv}^\mathrm{T}+3s^2+2s\cdot0+\mathbf{tr}((\boldsymbol{v}^\wedge)^2) \\
&=v_{1}^{2}+v_{2}^{2}+v_{3}^{2}+3s^{2}-2(v_{1}^{2}+v_{2}^{2}+v_{3}^{2}) \\
&=(1-s^2)+3s^2-2(1-s^2) \\
&=4s^2-1.
\end{aligned}
$$

- 即 $\displaystyle \theta=2\arccos s.$
- 再加上旋转轴:

$$
\begin{cases}\theta=2\arccos q_0\\
[n_x,n_y,n_z]^\mathrm{T}=[q_1,q_2,q_3]^\mathrm{T}/\sin\frac{\theta}{2}\end{cases}.
$$

### 3.5 相似、仿射、射影变换

1. 相似变换:

$$
\boldsymbol{T}_S=\begin{bmatrix}s\boldsymbol{R}&t\\\mathbf{0}^\mathrm{T}&1\end{bmatrix}.
$$

允许缩放，相似变换群: Sim (3)  
2. 仿射变换:

$$
T_A=\begin{bmatrix}A&t\\\mathbf{0}^\mathrm{T}&1\end{bmatrix}.
$$

只保证平行关系  
3. 射影变换

$$
T_P=\begin{bmatrix}A&t\\\\a^\mathrm{T}&v\end{bmatrix}.
$$

总结一下:

$$
\begin{array}{c|c|c|c}\hline\text{变换名称}&\text{矩阵形式}&\text{自由度}&\text{不变性质}\\\hline\text{欧氏变换}&\begin{bmatrix}R&t\\0^\mathrm{T}&1\end{bmatrix}&6&\text{长度、夹角、体积}\\\text{相似变换}&\begin{bmatrix}sR&t\\0^\mathrm{T}&1\end{bmatrix}&7&\text{体积比}\\\text{仿射变换}&\begin{bmatrix}A&t\\0^\mathrm{T}&1\end{bmatrix}&12&\text{平行性、体积比}\\\text{射影变换}&\begin{bmatrix}A&t\\a^\mathrm{T}&v\end{bmatrix}&15&\text{接触平面的相交和相切}\\\hline\end{array}
$$

### 3.6 实践: Eigen 几何模块

#### 3.6.1 Eigen 几何模块的数据演示

再说吧。

#### 3.6.2 实际的坐标变换例子

TODO

### 3.7 可视化演示

#### 3.7.1 显示运动轨迹

- 用 Pangolin 库
- TODO

#### 3.7.2 显示相机的位姿

### 3.8 习题

TODO

## 4 李群和李代数

- 由于旋转矩阵本身带有约束（正交且行列式为 1），让优化变得困难。
- 所以我们引入李群-李代数间的转换关系，把位姿估计变成无约束的优化问题

### 4.1 李群和李代数基础

- 三维旋转矩阵构成了特殊正交群 $\displaystyle \boldsymbol{SO}(3)$
- 变换矩阵构成了特殊欧氏群 $\displaystyle \boldsymbol{SE}(3)$
	- 但是他们都对加法不封闭
	- 对乘法封闭

#### 4.1.1 群

- $\displaystyle G = (A,\cdot)$ 满足:
	- 封闭性
	- 结合律
	- 幺元
	- 逆
- 李群是具有连续（光滑）性质的群

#### 4.1.2 李代数的引出

- $\displaystyle \boldsymbol{R}\boldsymbol{R}^\mathrm{T} = \boldsymbol{I}$
- 我们易得: $\displaystyle \dot{\boldsymbol{R}}(t)\boldsymbol{R}(t)^\mathrm{T}=-\left(\dot{\boldsymbol{R}}(t)\boldsymbol{R}(t)^\mathrm{T}\right)^\mathrm{T}.$
	- 即 $\displaystyle \dot{\boldsymbol{R}}(t)\boldsymbol{R}(t)^\mathrm{T}$ 是反对称
- 而对于任意反对称矩阵，我们都可以找到唯一与之对应的向量
	- $\displaystyle \dot{\boldsymbol{R}}(t)\boldsymbol{R}(t)^\mathrm{T}=\boldsymbol{\phi}(t)^{\wedge}.$
	- $\displaystyle \dot{\boldsymbol{R}}(t)=\phi(t)^{\wedge}\boldsymbol{R}(t)=\begin{bmatrix}0&-\phi_3&\phi_2\\\phi_3&0&-\phi_1\\-\phi_2&\phi_1&0\end{bmatrix}\boldsymbol{R}(t).$  
考虑 $\displaystyle t_{0} = 0$ 和 $\displaystyle \boldsymbol{R}(0) = \boldsymbol{I}$ 时:

$$
\begin{aligned}
R(t)& \approx\boldsymbol{R}\left(t_{0}\right)+\dot{\boldsymbol{R}}\left(t_{0}\right)\left(t-t_{0}\right) \\
&=I+\phi(t_0)^{\wedge}(t).
\end{aligned}
$$

于是求导->一个算符 $\displaystyle \phi$ ，被称为 $\displaystyle \boldsymbol{SO}(3)$ 原点附近的正切空间（Tangent Space）  
设在 $\displaystyle t_{0}$ 附近，$\displaystyle \phi$ 保持常数 $\displaystyle \phi(t_{0})=\phi_{0}$，

$$
\dot{\boldsymbol{R}}(t)=\boldsymbol{\phi}(t_0)^\wedge\boldsymbol{R}(t)=\boldsymbol{\phi}_0^\wedge\boldsymbol{R}(t).
$$

再有 $\displaystyle \boldsymbol{R}(0) = \boldsymbol{I}$，解的:

$$
\boldsymbol{R}(t)=\exp\left(\boldsymbol{\phi}_{0}^{\wedge}t\right).
$$

- $\displaystyle \phi$ 正是对应到 $\displaystyle SO(3)$ 上的李代数 $\displaystyle \mathfrak{so}(3)$
- $\displaystyle \begin{aligned}&\text{其次,给定某个向量 }\phi\text{ 时,矩阵指数}\exp(\phi^{\wedge})\text{ 如何计算? 反之,给定 }R\text{ 时,能否有相反}\\&\text{的运算来计算 }\phi?\text{ 事实上,这正是李群与李代数间的指数}/\text{对数映射。}\end{aligned}$

#### 4.1.3 李代数的定义

李代数由一个集合 $\displaystyle \mathbb{V}$、一个数域 $\displaystyle \mathbb{F}$ 和一个二元运算 $\displaystyle [,]$ 组成。如果满足以下几条性质，则称 ( $\displaystyle \mathbb{V},\mathbb{F},[,]$) 为一个李代数，记作 $\displaystyle \mathfrak{g}$。

1. 封闭性
2. 双线性
3. 自反性 $\displaystyle \quad\forall \boldsymbol{X}\in\mathbb{V},[\boldsymbol{X},\boldsymbol{X}]=0$
4. 雅可比等价 $\displaystyle \forall X,Y,Z\in\mathbb{V},[X,[Y,Z]]+[Z,[X,Y]]+[Y,[Z,X]]=0.$  
其中二元运算被称为李括号。  
eg: 叉积是一种李括号

#### 4.1.4 李代数 $\displaystyle \mathfrak{so}(3)$

$\displaystyle \boldsymbol{\Phi}=\boldsymbol{\phi}^{\wedge}=\begin{bmatrix}0&-\phi_3&\phi_2\\\\\phi_3&0&-\phi_1\\\\-\phi_2&\phi_1&0\end{bmatrix}\in\mathbb{R}^{3\times3}.$  
所以两个向量 $\displaystyle \phi_{1},\phi_{2}$ 的李括号为:

$$
[\phi_1,\phi_2]=(\boldsymbol{\Phi}_1\boldsymbol{\Phi}_2-\boldsymbol{\Phi}_2\boldsymbol{\Phi}_1)^\vee.
$$

$$
\mathfrak{so}(3)=\left\{\phi\in\mathbb{R}^3,\boldsymbol{\Phi}=\phi^\wedge\in\mathbb{R}^{3\times3}\right\}.
$$

$$
R=\exp(\phi^{\wedge}).
$$

#### 4.1.5 李代数 $\displaystyle \mathfrak{se}(3)$

$$
\mathfrak{se}(3)=\left\{\boldsymbol{\xi}=\begin{bmatrix}\boldsymbol{\rho}\\\boldsymbol{\phi}\end{bmatrix}\in\mathbb{R}^6,\boldsymbol{\rho}\in\mathbb{R}^3,\boldsymbol{\phi}\in\mathfrak{so}(3),\boldsymbol{\xi}^\wedge=\begin{bmatrix}\boldsymbol{\phi}^\wedge&\boldsymbol{\rho}\\\boldsymbol{0}^\mathrm{T}&0\end{bmatrix}\in\mathbb{R}^{4\times4}\right\}.
$$

前三维为平移，后三维为旋转（实质上是 $\displaystyle \mathfrak{so}(3)$ 元素）

$$
\xi^\wedge=\begin{bmatrix}\phi^\wedge&\rho\\0^\mathrm{T}&0\end{bmatrix}\in\mathbb{R}^{4\times4}.
$$

同样李代数 $\displaystyle \mathfrak{se}(3)$ 也有类似于 $\displaystyle \mathfrak{so}(3)$ 的李括号:

$$
[\xi_1,\xi_2]=\left(\xi_1^\wedge\xi_2^\wedge-\xi_2^\wedge\xi_1^\wedge\right)^\vee.
$$

### 4.2 指数与对数映射

#### 4.2.1 SO(3)上的指数映射

- Exponential Map
- 首先任意矩阵的指数映射可以写成一个泰勒展开（收敛的时候）

$$
\exp(A)=\sum_{n=0}^\infty\frac1{n!}A^n.
$$

- 应用到 $\displaystyle \mathfrak{so}(3)$ 中:

$$
\exp(\phi^\wedge)=\sum_{n=0}^\infty\frac{1}{n!}(\phi^\wedge)^n.
$$

- 我们可以把 $\displaystyle \phi$ 表示成 $\displaystyle \theta \boldsymbol{a}$，对于 $\displaystyle \boldsymbol{a}^\wedge$:

$$
\boldsymbol{a}^{\wedge}\boldsymbol{a}^{\wedge}=\begin{bmatrix}-a_2^2-a_3^2&a_1a_2&a_1a_3\\\\a_1a_2&-a_1^2-a_3^2&a_2a_3\\\\a_1a_3&a_2a_3&-a_1^2-a_2^2\end{bmatrix}=\boldsymbol{a}\boldsymbol{a}^\mathrm{T}-\boldsymbol{I},
$$

和

$$
a^{\wedge}a^{\wedge}a^{\wedge}=a^{\wedge}(aa^{\mathrm{T}}-I)=-a^{\wedge}.
$$

于是我们可以化简:

$$
\begin{aligned}
\exp\left(\phi^\wedge\right)& =\exp\left(\theta\boldsymbol{a}^\wedge\right)=\sum_{n=0}^\infty\frac1{n!}\left(\theta\boldsymbol{a}^\wedge\right)^n \\
&=I+\theta\boldsymbol{a}^{\wedge}+\frac{1}{2!}\theta^{2}\boldsymbol{a}^{\wedge}\boldsymbol{a}^{\wedge}+\frac{1}{3!}\theta^{3}\boldsymbol{a}^{\wedge}\boldsymbol{a}^{\wedge}\boldsymbol{a}^{\wedge}+\frac{1}{4!}\theta^{4}(\boldsymbol{a}^{\wedge})^{4}+\cdots \\
&=\boldsymbol{a}\boldsymbol{a}^{\mathrm{T}}-\boldsymbol{a}^{\wedge}\boldsymbol{a}^{\wedge}+\theta\boldsymbol{a}^{\wedge}+\frac{1}{2!}\theta^{2}\boldsymbol{a}^{\wedge}\boldsymbol{a}^{\wedge}-\frac{1}{3!}\theta^{3}\boldsymbol{a}^{\wedge}-\frac{1}{4!}\theta^{4}(\boldsymbol{a}^{\wedge})^{2}+\cdots \\
&=\boldsymbol{a}\boldsymbol{a}^{\mathsf{T}}+\underbrace{\left(\theta-\frac{1}{3!}\theta^{3}+\frac{1}{5!}\theta^{5}-\cdots\right)}_{\sin\theta}\boldsymbol{a}^{\wedge}-\underbrace{\left(1-\frac{1}{2!}\theta^{2}+\frac{1}{4!}\theta^{4}-\cdots\right)}_{\cos\theta}\boldsymbol{a}^{\wedge}\boldsymbol{a}^{\wedge} \\
&=a^\wedge a^\wedge+I+\sin\theta a^\wedge-\cos\theta a^\wedge a^\wedge \\
&=(1-\cos\theta)\boldsymbol{a}^\wedge\boldsymbol{a}^\wedge+\boldsymbol{I}+\sin\theta\boldsymbol{a}^\wedge \\
&=\cos\theta\boldsymbol{I}+(1-\cos\theta)\boldsymbol{aa}^\mathrm{T}+\sin\theta\boldsymbol{a}^\mathrm{\wedge}.
\end{aligned}
$$

最后得到:

$$
\exp(\theta\boldsymbol{a}^\wedge)=\cos\theta\boldsymbol{I}+(1-\cos\theta)\boldsymbol{a}\boldsymbol{a}^\mathrm{T}+\sin\theta\boldsymbol{a}^\wedge.
$$

所以 $\displaystyle \mathfrak{so}(3)$ 就是旋量向量组成的空间，而指数映射即罗德里格斯公式。

- 通过上面的公式，我们可以把 $\displaystyle \mathfrak{so}(3)$ 中任意向量对应到 SO (3) 中的旋转矩阵
- 反过来也是可以的

$$
\phi=\ln\left(\boldsymbol{R}\right)^\vee=\left(\sum_{n=0}^\infty\frac{\left(-1\right)^n}{n+1}\left(\boldsymbol{R}-\boldsymbol{I}\right)^{n+1}\right)^\vee.
$$

#### 4.2.2 SE (3) 上的指数映射

同样的推导方式:

$$
\begin{aligned}
\exp\left(\xi^{\wedge}\right)& =\begin{bmatrix}\sum_{n=0}^{\infty}\frac{1}{n!}(\phi^{\wedge})^{n}&\sum_{n=0}^{\infty}\frac{1}{(n+1)!}(\phi^{\wedge})^{n}\rho\\\\\mathbf{0}^{\mathrm{T}}&1\end{bmatrix} \\
&\stackrel{\Delta}{=}\begin{bmatrix}R&J\rho\\\\0^\mathrm{T}&1\end{bmatrix}=T.
\end{aligned}
$$

$$
\begin{aligned}
\sum_{n=0}^{\infty}\frac{1}{(n+1)!}(\phi^{\wedge})^{n}& =\boldsymbol{I}+\frac{1}{2!}\theta\boldsymbol{a}^{\wedge}+\frac{1}{3!}\theta^{2}{(\boldsymbol{a}^{\wedge})}^{2}+\frac{1}{4!}\theta^{3}{(\boldsymbol{a}^{\wedge})}^{3}+\frac{1}{5!}\theta^{4}{(\boldsymbol{a}^{\wedge})}^{4}\cdots  \\
&=\frac{1}{\theta}\left(\frac{1}{2!}\theta^{2}-\frac{1}{4!}\theta^{4}+\cdots\right)(\boldsymbol{a}^{\wedge})+\frac{1}{\theta}\left(\frac{1}{3!}\theta^{3}-\frac{1}{5}\theta^{5}+\cdots\right)(\boldsymbol{a}^{\wedge})^{2}+\boldsymbol{I} \\
&=\frac1\theta\left(1-\cos\theta\right)\left(\boldsymbol{a}^{\wedge}\right)+\frac{\theta-\sin\theta}\theta\left(\boldsymbol{a}\boldsymbol{a}^{\mathrm{T}}-\boldsymbol{I}\right)+\boldsymbol{I} \\
&=\frac{\sin\theta}\theta\boldsymbol{I}+\left(1-\frac{\sin\theta}\theta\right)\boldsymbol{aa}^\mathrm{T}+\frac{1-\cos\theta}\theta\boldsymbol{a}^\mathrm{\wedge}\overset{\mathrm{def}}{\operatorname*{=}}\boldsymbol{J}.
\end{aligned}
$$

$$
\boldsymbol{J}=\frac{\sin\theta}{\theta}\boldsymbol{I}+\left(1-\frac{\sin\theta}{\theta}\right)\boldsymbol{a}\boldsymbol{a}^\mathrm{T}+\frac{1-\cos\theta}{\theta}\boldsymbol{a}^\mathrm{\wedge}.
$$

4.28 没看懂  
![image.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409012205650.png)

### 4.3 李代数求导与扰动模型

#### 4.3.1 BCH 公式与近似形式

探究如下式子是否成立:

$$
\ln\left(\exp\left(A\right)\exp\left(B\right)\right)=A+B ?
$$

但它并不成立。两个李代数指数映射乘积的完整形式，由 Baker-Campbell-Hausdorff 给出:

$$
\ln\left(\exp\left(A\right)\exp\left(B\right)\right)=A+B+\frac{1}{2}\left[A,B\right]+\frac{1}{12}\left[A,\left[A,B\right]\right]-\frac{1}{12}\left[B,\left[A,B\right]\right]+\cdots
$$

特别的，当 $\displaystyle \phi_{1}$ 或 $\displaystyle \phi_{2}$ 为小量时，小量二次以上的项都可以被忽略，此时的线性近似表达:

$$
\ln\left(\exp\left(\phi_1^\wedge\right)\exp\left(\phi_2^\wedge\right)\right)^\vee\approx\begin{cases}J_l(\phi_2)^{-1}\phi_1+\phi_2&\text{当}\phi_1\text{为小量},\\J_r(\phi_1)^{-1}\phi_2+\phi_1&\text{当}\phi_2\text{为小量}.\end{cases}
$$

$$
\boldsymbol{J}_{l}=\frac{\sin\theta}{\theta}\boldsymbol{I}+\left(1-\frac{\sin\theta}{\theta}\right)\boldsymbol{a}\boldsymbol{a}^\mathrm{T}+\frac{1-\cos\theta}{\theta}\boldsymbol{a}^\mathrm{\wedge}.
$$

$$
\boldsymbol{J}_{\ell}^{-1}=\frac{\theta}{2}\cot\frac{\theta}{2}\boldsymbol{I}+\left(1-\frac{\theta}{2}\cot\frac{\theta}{2}\right)\boldsymbol{a}\boldsymbol{a}^{\mathrm{T}}-\frac{\theta}{2}\boldsymbol{a}^{\wedge}.
$$

$$
J_{r}(\phi)=J_{l}(-\phi).
$$

于是我们就可以谈论李群乘法与李代数加法的关系了。  
$\displaystyle \boldsymbol{R}$ 对应 $\displaystyle \phi$，我们给它左乘一个微小旋转，记作 $\displaystyle \Delta \boldsymbol{R}$

$$
\exp\left(\Delta\phi^{\wedge}\right)\exp\left(\phi^{\wedge}\right)=\exp\left(\left(\phi+J_{l}^{-1}\left(\phi\right)\Delta\phi\right)^{\wedge}\right).
$$

$$
\exp\left(\left(\phi+\Delta\phi\right)^{\wedge}\right)=\exp\left(\left(J_{l}\Delta\phi\right)^{\wedge}\right)\exp\left(\phi^{\wedge}\right)=\exp\left(\phi^{\wedge}\right)\exp\left(\left(J_{r}\Delta\phi\right)^{\wedge}\right).
$$

对于 SE (3) 我们也有:

$$
\exp\left(\Delta\xi^{\wedge}\right)\exp\left(\xi^{\wedge}\right)\approx\exp\left(\left(\mathcal{J}_{l}^{-1}\Delta\xi+\xi\right)^{\wedge}\right)
$$

$$
exp\left(\xi^{\wedge}\right)\exp\left(\Delta\xi^{\wedge}\right)\approx\exp\left(\left(\mathcal{J}_{r}^{-1}\Delta\xi+\xi\right)^{\wedge}\right).
$$

唯一不同的是这里的 $\displaystyle J_{l}$ 比较复杂。

#### 4.3.2 SO (3) 上的李代数求导

$$
z=T\boldsymbol{p}+\boldsymbol{w}.
$$

其中 $\displaystyle \boldsymbol{w}$ 是随机噪声。

$$
e=z-Tp.
$$

假设一共有 N 个这样的路标点和观测:

$$
\min_{\boldsymbol{T}}J(\boldsymbol{T})=\sum_{i=1}^N\left\|\boldsymbol{z}_i-\boldsymbol{T}\boldsymbol{p}_i\right\|_2^2.
$$

most importantly，我们会构建与位姿有关的函数，并讨论该函数关于位姿的导数，以调整当前的估计值。  
使用李代数解决求导问题的思路分为两种:

1. 用李代数表示姿态，然后根据李代数加法对李代数求导。
2. 对李群左乘或右乘微小扰动，然后对该扰动求导，称为左扰动和右扰动模型。

### 4.4 李代数求导

要计算 $\displaystyle \frac{\partial\left(Rp\right)}{\partial R}$, 由于SO（3）没有加法，我们转而计算: $\displaystyle \frac{\partial\left(\exp\left(\phi^{\wedge}\right)\boldsymbol{p}\right)}{\partial\boldsymbol{\phi}}.$

$$
\begin{aligned}
\frac{\partial\left(\exp\left(\phi^{\wedge}\right)\boldsymbol{p}\right)}{\partial\phi}& =\lim_{\delta\boldsymbol{\phi}\to0}\frac{\exp\left(\left(\boldsymbol{\phi}+\delta\boldsymbol{\phi}\right)^{\wedge}\right)\boldsymbol{p}-\exp\left(\boldsymbol{\phi}^{\wedge}\right)\boldsymbol{p}}{\delta\boldsymbol{\phi}} \\
&=\lim_{\delta\phi\to0}\frac{\exp\left(\left(\boldsymbol{J}_i\delta\boldsymbol{\phi}\right)^\wedge\right)\exp\left(\boldsymbol{\phi}^\wedge\right)\boldsymbol{p}-\exp\left(\boldsymbol{\phi}^\wedge\right)\boldsymbol{p}}{\delta\boldsymbol{\phi}} \\
&=\lim_{\delta\phi\to0}\frac{\left(\boldsymbol{I}+\left(\boldsymbol{J}_{l}\delta\boldsymbol{\phi}\right)^{\wedge}\right)\exp\left(\boldsymbol{\phi}^{\wedge}\right)\boldsymbol{p}-\exp\left(\boldsymbol{\phi}^{\wedge}\right)\boldsymbol{p}}{\delta\phi} \\
&=\lim_{\delta\phi\to0}\frac{\left(\boldsymbol{J}_{l}\delta\phi\right)^{\wedge}\exp\left(\boldsymbol{\phi}^{\wedge}\right)\boldsymbol{p}}{\delta\phi} \\
&=\lim_{\delta\boldsymbol{\phi}\to0}\frac{-(\exp\left(\boldsymbol{\phi}^{\wedge}\right)\boldsymbol{p})^{\wedge}\boldsymbol{J}_{l}\delta\boldsymbol{\phi}}{\delta\boldsymbol{\phi}}=-(\boldsymbol{R}\boldsymbol{p})^{\wedge}\boldsymbol{J}_{l}.
\end{aligned}
$$

BCH 线性近似+泰勒展开取线性项:

$$
\frac{\partial\left(\boldsymbol{Rp}\right)}{\partial\boldsymbol{\phi}}=\left(-\boldsymbol{Rp}\right)^{\wedge}\boldsymbol{J}_{l}.
$$

但是这里仍然有 $\displaystyle \boldsymbol{J}_{l}$

#### 4.4.1 扰动模型（左乘）

$\displaystyle \varphi$ 对应左扰动 $\displaystyle \Delta \boldsymbol{R}$

$$
\begin{aligned}
\frac{\partial\left(Rp\right)}{\partial\varphi}& =\lim_{\varphi\to0}\frac{\exp\left(\varphi^{\wedge}\right)\exp\left(\phi^{\wedge}\right)p-\exp\left(\phi^{\wedge}\right)p}{\varphi} \\
&=\lim_{\varphi\to0}\frac{(\boldsymbol{I}+\boldsymbol{\varphi}^{\wedge})\exp\left(\boldsymbol{\phi}^{\wedge}\right)\boldsymbol{p}-\exp\left(\boldsymbol{\phi}^{\wedge}\right)\boldsymbol{p}}{\varphi} \\
&=\lim_{\varphi\to0}\frac{\varphi^\wedge Rp}\varphi=\lim_{\varphi\to0}\frac{-\left(Rp\right)^\wedge\varphi}\varphi=-\left(Rp\right)^\wedge.
\end{aligned}
$$

#### 4.4.2 SE (3) 上的李代数求导

$$
\begin{aligned}
\frac{\partial\left(\boldsymbol{T}\boldsymbol{p}\right)}{\partial\delta\boldsymbol{\xi}}&=\lim_{\delta\boldsymbol{\xi}\to\boldsymbol{0}}\frac{\exp\left(\delta\boldsymbol{\xi}^{\wedge}\right)\exp\left(\boldsymbol{\xi}^{\wedge}\right)\boldsymbol{p}-\exp\left(\boldsymbol{\xi}^{\wedge}\right)\boldsymbol{p}}{\delta\xi} \\
&=\lim_{\delta\boldsymbol{\xi}\to\mathbf{0}}\frac{\left(\boldsymbol{I}+\delta\boldsymbol{\xi}^{\wedge}\right)\exp\left(\boldsymbol{\xi}^{\wedge}\right)\boldsymbol{p}-\exp\left(\boldsymbol{\xi}^{\wedge}\right)\boldsymbol{p}}{\delta\boldsymbol{\xi}} \\
&=\lim_{\delta\boldsymbol{\xi}\to0}\frac{\delta\boldsymbol{\xi}^{\wedge}\exp\left(\boldsymbol{\xi}^{\wedge}\right)\boldsymbol{p}}{\delta\boldsymbol{\xi}} \\
&=\lim_{\delta\boldsymbol{\xi}\to\mathbf{0}}\frac{\begin{bmatrix}\delta\boldsymbol{\phi}^\wedge&\delta\boldsymbol{\rho}\\\\\mathbf{0}^\mathrm{T}&0\end{bmatrix}\begin{bmatrix}\boldsymbol{R}\boldsymbol{p}+\boldsymbol{t}\\\\1\end{bmatrix}}{\delta\boldsymbol{\xi}} \\
&=\lim_{\delta\boldsymbol{\xi}\to\boldsymbol{0}}\frac{\begin{bmatrix}\delta\boldsymbol{\phi}^{\wedge}\left(\boldsymbol{R}\boldsymbol{p}+\boldsymbol{t}\right)+\delta\boldsymbol{\rho}\\\boldsymbol{0}^{\mathrm{T}}\end{bmatrix}}{[\delta\boldsymbol{\rho},\delta\boldsymbol{\phi}]^{\mathrm{T}}}=\begin{bmatrix}\boldsymbol{I}&-(\boldsymbol{R}\boldsymbol{p}+\boldsymbol{t})^{\wedge}\\\boldsymbol{0}^{\mathrm{T}}&\boldsymbol{0}^{\mathrm{T}}\end{bmatrix}\stackrel{\mathrm{def}}{=}(\boldsymbol{T}\boldsymbol{p})^{\odot}.
\end{aligned}
$$

$$
\frac{\mathrm{d}\begin{bmatrix}a\\b\end{bmatrix}}{\mathrm{d}\begin{bmatrix}x\\y\end{bmatrix}}=\left(\frac{\mathrm{d}[a,b]^\mathrm{T}}{\mathrm{d}\begin{bmatrix}x\\y\end{bmatrix}}\right)^\mathrm{T}=\begin{bmatrix}\frac{\mathrm{d}a}{\mathrm{d}x}&\frac{\mathrm{d}b}{\mathrm{d}x}\\\frac{\mathrm{d}a}{\mathrm{d}y}&\frac{\mathrm{d}b}{\mathrm{d}y}\end{bmatrix}^\mathrm{T}=\begin{bmatrix}\frac{\mathrm{d}a}{\mathrm{d}x}&\frac{\mathrm{d}a}{\mathrm{d}y}\\\frac{\mathrm{d}b}{\mathrm{d}x}&\frac{\mathrm{d}b}{\mathrm{d}y}\end{bmatrix}
$$

### 4.5 实践:Sophus

#### 4.5.1 Sophus 的基本使用方法 

#### 4.5.2 例子: 评估轨迹的误差

- 绝对轨迹误差（Absolute Trajectory Error, ATE）

$$
\mathrm{ATE}_{\mathrm{all}}=\sqrt{\frac{1}{N}\sum_{i=1}^{N}\|\log(T_{\mathrm{gt},i}^{-1}T_{\mathrm{esti},i})^{\vee}\|_{2}^{2}},
$$

即均方根误差（Root-Mean-Squared Error, RMSE）

- 绝对平移误差（Average Translational Error）

$$
\mathrm{ATE}_{\mathrm{all}}=\sqrt{\frac{1}{N}\sum_{i=1}^{N}\|\log(T_{\mathrm{gt},i}^{-1}T_{\mathrm{esti},i})^{\vee}\|_{2}^{2}},
$$

- 相对位姿误差（Relative Pose Error, RPE）

$$
\mathrm{RPE}_{\mathrm{all}}=\sqrt{\frac{1}{N-\Delta t}\sum_{i=1}^{N-\Delta t}\|\log\left(\left(\boldsymbol{T}_{\mathrm{gt},i}^{-1}\boldsymbol{T}_{\mathrm{gt},i+\Delta t}\right)\right)^{-1}\left(\boldsymbol{T}_{\mathrm{est},i}^{-1}\boldsymbol{T}_{\mathrm{est},i+\Delta t}\right))^{\vee}\|_{2}^{2}},
$$

$$
\mathrm{RPE}_{\mathrm{trans}}=\sqrt{\frac{1}{N-\Delta t}\sum_{i=1}^{N-\Delta t}\|\mathrm{trans}\left(\left(T_{gt,i}^{-1}T_{gt,i+\Delta t}\right)\right)^{-1}\left(T_{\mathrm{esti},i}^{-1}T_{\mathrm{esti},i+\Delta t}\right))\|_{2}^{2}}.
$$

代码计算:

```
TODO
```

### 4.6 相似变换与李代数

在这里我们讨论 Sim (3) 和对应的李代数 $\displaystyle \mathfrak{sim}(3)$。  
对于位于空间的点 $\displaystyle \boldsymbol{p}$，在相机坐标系下要经过一个相似变换，而非欧氏变换:

$$
\boldsymbol{p}'=\begin{bmatrix}s\boldsymbol{R}&\boldsymbol{t}\\\boldsymbol{0}^\mathrm{T}&1\end{bmatrix}\boldsymbol{p}=s\boldsymbol{R}\boldsymbol{p}+\boldsymbol{t}.
$$

$$
\mathrm{Sim}(3)=\left\{S=\begin{bmatrix}sR&t\\\\\mathbf{0}^\mathrm{T}&1\end{bmatrix}\in\mathbb{R}^{4\times4}\right\}.
$$

$$
\sin(3)=\left\{\zeta|\zeta=\begin{bmatrix}\rho\\\\\phi\\\\\sigma\end{bmatrix}\in\mathbb{R}^7,\zeta^\wedge=\begin{bmatrix}\sigma\boldsymbol{I}+\phi^\wedge&\rho\\\\\mathbf{0}^\mathrm{T}&0\end{bmatrix}\in\mathbb{R}^{4\times4}\right\}.
$$

$$
\exp\left(\zeta^{\wedge}\right)=\begin{bmatrix}\mathrm{e}^{\sigma}\exp\left(\phi^{\wedge}\right)&J_{s}\rho\\0^{\mathrm{T}}&1\end{bmatrix}.
$$

其中，$\displaystyle \boldsymbol{J}_{S}$ 的形式是:

$$
\begin{aligned}
\text{J}& =\frac{\mathrm{e}^{\sigma}-1}{\sigma}I+\frac{\sigma\mathrm{e}^{\sigma}\sin\theta+\left(1-\mathrm{e}^{\sigma}\cos\theta\right)\theta}{\sigma^{2}+\theta^{2}}\boldsymbol{a}^{\wedge} \\
&+\left(\frac{\mathrm{e}^\sigma-1}{\sigma}-\frac{\left(\mathrm{e}^\sigma\cos\theta-1\right)\sigma+\left(\mathrm{e}^\sigma\sin\theta\right)\theta}{\sigma^2+\theta^2}\right)\boldsymbol{a}^\wedge\boldsymbol{a}^\wedge.
\end{aligned}
$$

于是，李代数与李群的关系:

$$
s=\mathrm{e}^\sigma, R=\exp(\phi^\wedge), t=J_s\rho.
$$

$$
\frac{\partial\boldsymbol{Sp}}{\partial\boldsymbol{\zeta}}=\begin{bmatrix}\boldsymbol{I}&-\boldsymbol{q}^\wedge&\boldsymbol{q}\\\boldsymbol{0}^\mathrm{T}&\boldsymbol{0}^\mathrm{T}&0\end{bmatrix}.
$$

### 4.7 习题

TODO

## 5 相机与图像

- 观测主要是指相机成像的过程。

### 5.1 相机模型

- 针孔模型
- 透镜会产生畸变
- 内参数（Intrinsics）

#### 5.1.1 针孔相机模型

![QQ_1725253336267.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409021302607.png)

$$
\frac{Z}{f}=-\frac{X}{X'}=-\frac{Y}{Y'}.
$$

去掉负号:

$$
\frac Zf=\frac X{X^{\prime}}=\frac Y{Y^{\prime}}.
$$

$$
\begin{aligned}X'&=f\frac{X}{Z}\\Y'&=f\frac{Y}{Z}\end{aligned}.
$$

还有一个像素坐标系，u 轴与 x 轴平行，v 轴与 y 轴平行:

$$
\begin{cases}u=\alpha X'+c_x\\[2ex]v=\beta Y'+c_y\end{cases}.
$$

$$
\begin{cases}u=f_x\frac{X}{Z}+c_x\\\\v=f_y\frac{Y}{Z}+c_y\end{cases}.
$$

$$
Z\begin{pmatrix}u\\\\v\\\\1\end{pmatrix}=\begin{pmatrix}f_x&0&c_x\\0&f_y&c_y\\\\0&0&1\end{pmatrix}\begin{pmatrix}X\\\\Y\\\\Z\end{pmatrix}\overset{\text{def}}{=}\boldsymbol{KP}.
$$

最中间的矩阵称为相机的内参数（Camera Inrinsics）矩阵 $\displaystyle \boldsymbol{K}$。  
标定: 确定相机的内参

$$
Z\boldsymbol{P}_{uv}=Z\begin{bmatrix}u\\\\v\\\\1\end{bmatrix}=\boldsymbol{K}\left(\boldsymbol{R}\boldsymbol{P}_\mathrm{w}+\boldsymbol{t}\right)=\boldsymbol{K}\boldsymbol{T}\boldsymbol{P}_\mathrm{w}.
$$

其中 $\displaystyle \boldsymbol{R},\boldsymbol{t}$ 又称为相机的外参数（Camera Extrinsics）

$$
(\boldsymbol{RP_\mathrm{w}}+\boldsymbol{t})=\underbrace{[X,Y,Z]^\mathrm{T}}_{\text{相机坐标}}\to\underbrace{[X/Z,Y/Z,1]^\mathrm{T}}_{\text{归一化坐标}} .
$$

- 归一化平面
- 点的深度在投影过程中被丢失了

#### 5.1.2 畸变模型

- 畸变 (Distortion 失真) 径向畸变
	- 筒形畸变
	- 枕形畸变  
![QQ_1725256803201.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409021400509.png)  
![QQ_1725289917431.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409022312526.png)
- 径向畸变即 $\displaystyle r$ 变化
- 切向畸变即 $\displaystyle \theta$ 变化  
我们可以假设:

$$
\begin{align}
x_{\mathrm{distorted}}&=x(1+k_1r^2+k_2r^4+k_3r^6) \\
y_{\mathrm{distorted}}&=y(1+k_1r^2+k_2r^4+k_3r^6).
\end{align}
$$

$$
\begin{align}
x_{\mathrm{distorted}}&=x+2p_1xy+p_2(r^2+2x^2) \\
y_{\mathrm{distorted}}&=y+p_1(r^2+2y^2)+2p_2xy
\end{align}
$$

所以我们可以找到一个点在像素平面上的正确位置:

1. 将三维空间点投影到归一化图像平面。设它的归一化坐标为 $\displaystyle [x, y]^\mathrm{T}$。
2. 对归一化平面上的点计算径向畸变和切向畸变

$$
\begin{cases}x_\text{distorted}=x(1+k_1r^2+k_2r^4+k_3r^6)+2p_1xy+p_2(r^2+2x^2)\\y_\text{distorted}=y(1+k_1r^2+k_2r^4+k_3r^6)+p_1(r^2+2y^2)+2p_2xy\end{cases}
$$

1. 将畸变后的点通过内参数矩阵投影到像素平面，得到该点在图像上的正确位置。

$$
\begin{cases}u=f_xx_\text{distorted}+c_x\\\\v=f_yy_\text{distorted}+c_y\end{cases}.
$$

还有很多的相机模型比如: 仿射模型，透视模型。

总结一下单目相机的成像过程:

1. 世界坐标系下有一个固定的点 $\displaystyle P$，世界坐标为 $\displaystyle \boldsymbol{P}_{w}$。
2. 由于相机在运动，它的运动由 $\displaystyle \boldsymbol{R},\boldsymbol{t}$ 或变换矩阵 $\displaystyle \boldsymbol{T}\in SE(3)$ 描述。$\displaystyle P$ 的相机坐标为 $\displaystyle \tilde{P_{c}} = \boldsymbol{R}\boldsymbol{P}_{w}+\boldsymbol{t}$。
3. 这时的 $\displaystyle \tilde{\boldsymbol{P}_{c}}$ 的分量是 $\displaystyle X,Y,Z$ ，把它们投影到归一化平面 $\displaystyle Z = 1$ 上，得到 $\displaystyle P$ 的归一化坐标: $\displaystyle \boldsymbol{P}_{c} = \left[ \frac{X}{Z},   \frac{Y}{Z}, 1 \right]^\mathrm{T}$。
4. 有畸变时，根据畸变参数计算 $\displaystyle \boldsymbol{P}_{c}$ 发生畸变后的坐标。
5. $\displaystyle P$ 的归一化坐标经过内参后，对应到它的像素坐标: $\displaystyle \boldsymbol{P}_{uv} = \boldsymbol{K} \boldsymbol{P}_{c}$。

#### 5.1.3 双目相机模型

![QQ_1725291418446.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409022337946.png)  
两者之间的距离称为双目相机的基线

$$
z=\frac{fb}{d},\quad d\stackrel{\mathrm{def}}{=}u_{\mathrm{L}}-u_{\mathrm{R}}.
$$

- d 定义为左右图的横坐标之差，称为视差。
	- 由于视差最小为一个像素，所以双目的深度存在一个理论上的最大值。

#### 5.1.4 RGB-D 相机模型

- 红外结构光（Structured lightning）
- 飞行时间（Time-of-Flight, ToF）  
![QQ_1725291798269.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409022343328.png)
- ToF 相机可以获得整个图像的像素深度
- 输出彩色图和深度图，生成点云（Point Cloud）

### 5.2 图像

$$
I(x,y):\mathbb{R}^2\mapsto\mathbb{R}.
$$

- channel

### 5.3 实践: 计算机中的图像

#### 5.3.1 OpenCV 的基本使用方法

TODO

#### 5.3.2 图像去畸变

TODO

### 5.4 实践: 3 D 视觉

#### 5.4.1 双目视觉

TODO

#### 5.4.2 RGB-D 视觉

### 5.5 习题

## 6 非线性优化

前面我们已经搞清楚了运动方程和观测方程的来源，现在我们开始讨论噪声。

### 6.1 状态估计问题

#### 6.1.1 批量状态估计与最大后验估计

$$
\begin{cases}\boldsymbol{x}_k=f\left(\boldsymbol{x}_{k-1},\boldsymbol{u}_k\right)+\boldsymbol{w}_k\\\boldsymbol{z}_{k,j}=h\left(\boldsymbol{y}_j,\boldsymbol{x}_k\right)+\boldsymbol{v}_{k,j}\end{cases}.
$$

$$
s\boldsymbol{z}_{k,j}=\boldsymbol{K}(R_k\boldsymbol{y}_j+\boldsymbol{t}_k).
$$

其中 $\displaystyle s$ 为像素点的距离。  
我们通常假设噪声项满足零均值的高斯分布:

$$
\boldsymbol{w}_k\sim\mathcal{N}\left(\boldsymbol{0},\boldsymbol{R}_k\right),\boldsymbol{v}_k\sim\mathcal{N}\left(\boldsymbol{0},\boldsymbol{Q}_{k,j}\right).
$$

有两种方法来解决状态估计问题:

- 用新的数据来更新当前时刻的估计状态，增量/渐进 (incremental) 的方法，或者教滤波器
- 也可以把数据都攒起来，称为批量 (batch) 的方法  
SfM (Structure from Motion)  
综合一下就有了滑动窗口估计法

$$
\boldsymbol{x}=\{\boldsymbol{x}_1,\ldots,\boldsymbol{x}_N\},\quad\boldsymbol{y}=\{\boldsymbol{y}_1,\ldots,\boldsymbol{y}_M\}.
$$

$$
P(\boldsymbol{x},\boldsymbol{y}|z,\boldsymbol{u}).
$$

$$
P\left(\boldsymbol{x},\boldsymbol{y}|\boldsymbol{z},\boldsymbol{u}\right)=\frac{P\left(\boldsymbol{z},\boldsymbol{u}|\boldsymbol{x},\boldsymbol{y}\right)P\left(\boldsymbol{x},\boldsymbol{y}\right)}{P\left(\boldsymbol{z},\boldsymbol{u}\right)}\propto\underbrace{P\left(\boldsymbol{z},\boldsymbol{u}|\boldsymbol{x},\boldsymbol{y}\right)}_{\text{似然}}\underbrace{P\left(\boldsymbol{x},\boldsymbol{y}\right)}_{\text{先验}}.
$$

可以先求一个状态最优估计:

$$
(\boldsymbol{x},\boldsymbol{y})^*_{\mathrm{MAP}}=\arg\max P(\boldsymbol{x},\boldsymbol{y}|\boldsymbol{z},\boldsymbol{u})=\arg\max P(\boldsymbol{z},\boldsymbol{u}|\boldsymbol{x},\boldsymbol{y})P(\boldsymbol{x},\boldsymbol{y}).
$$

求解最大后验概率等价于最大化似然和先验的乘积。  
但如果没有的先验，那么可以求解最大似然估计 (Maximize Likelihood Estimation， MLE):

$$
(\boldsymbol{x},\boldsymbol{y})^*{}_{\mathrm{MLE}}=\arg\max P(\boldsymbol{z},\boldsymbol{u}|\boldsymbol{x},\boldsymbol{y}).
$$

最大似然估计: 在什么样的状态下，最可能产生现在观测到的数据。

#### 6.1.2 最小二乘的引出

对于某一次观测:

$$
z_{k,j}=h\left(y_{j},x_{k}\right)+v_{k,j},
$$

$$
P(\boldsymbol{z}_{j,k}|\boldsymbol{x}_k,\boldsymbol{y}_j)=N\left(h(\boldsymbol{y}_j,\boldsymbol{x}_k),\boldsymbol{Q}_{k,j}\right).
$$

可以使用最小化负对数来求一个高斯分布的最大似然。

$$
P\left(\boldsymbol{x}\right)=\frac{1}{\sqrt{\left(2\pi\right)^{N}\det\left(\boldsymbol{\Sigma}\right)}}\exp\left(-\frac{1}{2}(\boldsymbol{x}-\boldsymbol{\mu})^{\mathrm{T}}\boldsymbol{\Sigma}^{-1}\left(\boldsymbol{x}-\boldsymbol{\mu}\right)\right).
$$

$$
-\ln\left(P\left(\boldsymbol{x}\right)\right)=\frac12\ln\left(\left(2\pi\right)^N\det\left(\boldsymbol{\Sigma}\right)\right)+\frac12\left(\boldsymbol{x}-\boldsymbol{\mu}\right)^\mathrm{T}\boldsymbol{\Sigma}^{-1}\left(\boldsymbol{x}-\boldsymbol{\mu}\right).
$$

$$
\begin{aligned}
(x_{k},y_{j})^{*}& =\arg\max\mathcal{N}(h(\boldsymbol{y}_{j},\boldsymbol{x}_{k}),\boldsymbol{Q}_{k,j}) \\
&=\arg\min\left(\left(\boldsymbol{z}_{k,j}-h\left(\boldsymbol{x}_k,\boldsymbol{y}_j\right)\right)^\mathrm{T}\boldsymbol{Q}_{k,j}^{-1}\left(\boldsymbol{z}_{k,j}-h\left(\boldsymbol{x}_k,\boldsymbol{y}_j\right)\right)\right).
\end{aligned}
$$

该式等价于最小化噪声项的一个二次型，马哈拉诺比斯距离 (Mahalanobis distance)。其中 $\displaystyle \boldsymbol{Q}_{k,j}^{-1}$ 叫信息矩阵，即高斯分布协方差矩阵之逆。  
假设各个时刻的输入和观测都是独立的，那么:

$$
P\left(\boldsymbol{z},\boldsymbol{u}|\boldsymbol{x},\boldsymbol{y}\right)=\prod_kP\left(\boldsymbol{u}_k|\boldsymbol{x}_{k-1},\boldsymbol{x}_k\right)\prod_{k,j}P\left(\boldsymbol{z}_{k,j}|\boldsymbol{x}_k,\boldsymbol{y}_j\right),
$$

$$
\begin{align}
e_{u,k} &=\boldsymbol{x}_k-f\left(\boldsymbol{x}_{k-1},\boldsymbol{u}_k\right) \\
e_{z,j,k} &=\boldsymbol{z}_{k,j}-h\left(\boldsymbol{x}_k,\boldsymbol{y}_j\right), 
\end{align}
$$

$$
\min J(\boldsymbol{x},\boldsymbol{y})=\sum_{k}\boldsymbol{e}_{\boldsymbol{u},k}^{\mathrm{T}}\boldsymbol{R}_{k}^{-1}\boldsymbol{e}_{\boldsymbol{u},k}+\sum_{k}\sum_{j}\boldsymbol{e}_{\boldsymbol{z},k,j}^{\mathrm{T}}\boldsymbol{Q}_{k,j}^{-1}\boldsymbol{e}_{\boldsymbol{z},k,j}.
$$

这样就得到了一个最小二乘问题 (Least Square Problem) 

- 整个问题有一种稀疏的形式。
- 用李代数表示增量会有无约束的优势。
- 用二次型度量误差，那么误差的分布会影响此项在整个问题中的权重。  
接下俩讲一些非线性优化的基本知识，来帮助我们求解这个最小二乘问题。

#### 6.1.3 例子: 批量状态估计

考虑一个非常简单的离散时间系统:

$$
\begin{aligned}&x_{k}=x_{k-1}+u_{k}+w_{k},&&\boldsymbol{w}_{k}\sim\mathcal{N}\left(0,\boldsymbol{Q}_{k}\right)\\&\boldsymbol{z}_{k}=\boldsymbol{x}_{k}+\boldsymbol{n}_{k},&&\boldsymbol{n}_{k}\sim\mathcal{N}\left(0,\boldsymbol{R}_{k}\right)\end{aligned}
$$

$$
\begin{gathered}
x_{map}^{*} =\arg\max P(\boldsymbol{x}|\boldsymbol{u},\boldsymbol{z})=\arg\max P(\boldsymbol{u},\boldsymbol{z}|\boldsymbol{x}) \\
=\prod_{k=1}^3P(\boldsymbol{u}_k|\boldsymbol{x}_{k-1},\boldsymbol{x}_k)\prod_{k=1}^3P(\boldsymbol{z}_k|\boldsymbol{x}_k), 
\end{gathered}
$$

而对于具体的每一项，我们有:

$$
P(\boldsymbol{u}_k|\boldsymbol{x}_{k-1},\boldsymbol{x}_k)=\mathcal{N}(\boldsymbol{x}_k-\boldsymbol{x}_{k-1},\boldsymbol{Q}_k),
$$

$$
P\left(\boldsymbol{z}_{k}|\boldsymbol{x}_{k}\right)=\mathcal{N}\left(\boldsymbol{x}_{k},\boldsymbol{R}_{k}\right).
$$

于是，我们可以构建误差变量:

$$
e_{\boldsymbol{u},k}=\boldsymbol{x}_k-\boldsymbol{x}_{k-1}-\boldsymbol{u}_k,\quad\boldsymbol{e}_{z,k}=\boldsymbol{z}_k-\boldsymbol{x}_k,
$$

于是最小二乘的目标函数为:

$$
\min\sum_{k=1}^{3}e_{u,k}^{\mathrm{T}}Q_{k}^{-1}e_{u,k}+\sum_{k=1}^{3}e_{z,k}^{\mathrm{T}}R_{k}^{-1}e_{z,k}.
$$

定义向量 $\displaystyle \boldsymbol{y} = [\boldsymbol{u},\boldsymbol{z}]^\mathrm{T}$

$$
y-Hx=e\sim\mathcal{N}(\mathbf{0},\boldsymbol{\Sigma}).
$$

$$
H=\begin{bmatrix}1&-1&0&0\\0&1&-1&0\\0&0&1&-1\\\hline0&1&0&0\\0&0&1&0\\0&0&0&1\end{bmatrix},
$$

且 $\displaystyle \Sigma = diag(\boldsymbol{Q_{1}},\boldsymbol{Q_{2}},\boldsymbol{Q_{3}},\boldsymbol{R_{1}},\boldsymbol{R_{2}},\boldsymbol{R_{3}})$。  
问题就转化成:

$$
x_{\mathrm{map}}^*=\arg\min e^{\mathrm{T}}\Sigma^{-1}e,
$$

它的唯一解是:

$$
x_{\mathrm{map}}^{*}=(H^{\mathrm{T}}\Sigma^{-1}H)^{-1}H^{\mathrm{T}}\Sigma^{-1}y.
$$

### 6.2 非线性最小二乘

先考虑一个简单的最小二乘问题:

$$
\min_{x}F(x)=\frac12\|f\left(x\right)\|_{2}^{2}.`
$$

对于不方便直接求解的最小二乘问题，我们可以用迭代的方式，从一个初始值出发，不断地更新当前的优化变量，使目标函数下降:

1. 给定某个初始值 $\displaystyle \boldsymbol{x_{0}}$。
2. 对于第 $\displaystyle k$ 次迭代，寻找一个增量 $\displaystyle \Delta x_{k}$，使得 $\displaystyle \left\|f\left(\boldsymbol{x}_{k}+\Delta\boldsymbol{x}_{k}\right)\right\|_{2}^{2}$ 达到最小值。
3. 若 $\displaystyle \Delta x_k$ 足够小，则停止。
4. 否则，令 $\displaystyle x_{k+1} = x_{k} + \Delta x_{k}$，返回第二步  
于是求解导函数为零 -> 寻找下降增量 $\displaystyle \Delta x_{k}$ 

下面是一些广泛使用的结果。

#### 6.2.1 一阶和二阶梯度法

使用泰勒展开:

$$
F(\boldsymbol{x}_k+\Delta\boldsymbol{x}_k)\approx F(\boldsymbol{x}_k)+\boldsymbol{J}\left(\boldsymbol{x}_k\right)^\mathrm{T}\Delta\boldsymbol{x}_k+\frac{1}{2}\Delta\boldsymbol{x}_k^\mathrm{T}\boldsymbol{H}(\boldsymbol{x}_k)\Delta\boldsymbol{x}_k.
$$

其中 $\displaystyle \boldsymbol{J}(x_{k})$ 是 $\displaystyle F(x)$ 关于 $\displaystyle x$ 的一阶导数（梯度、雅可比矩阵），$\displaystyle \boldsymbol{H}$ 是二阶导数（海塞矩阵）。

$$
\Delta\boldsymbol{x}^*=-\boldsymbol{J}(\boldsymbol{x}_k).
$$

$$
\Delta\boldsymbol{x}^*=\arg\min\left(F\left(\boldsymbol{x}\right)+\boldsymbol{J}\left(\boldsymbol{x}\right)^\mathrm{T}\Delta\boldsymbol{x}+\frac{1}{2}\Delta\boldsymbol{x}^\mathrm{T}\boldsymbol{H}\Delta\boldsymbol{x}\right).
$$

对 $\displaystyle \Delta x$ 求导，并令它等于零，得到:

$$
J+H\Delta x=\mathbf{0}\Rightarrow H\Delta x=-J.
$$

这个方法又叫牛顿法。

#### 6.2.2 高斯牛顿法

换一个函数展开:

$$
f\left(x+\Delta x\right)\approx f\left(x\right)+\boldsymbol{J}\left(\boldsymbol{x}\right)^{\mathrm{T}}\Delta\boldsymbol{x}.
$$

$$
\Delta x^{*}=\arg\min_{\Delta x}\frac{1}{2}\Big\|f\left(\boldsymbol{x}\right)+\boldsymbol{J}\left(\boldsymbol{x}\right)^{\mathrm{T}}\Delta\boldsymbol{x}\Big\|^{2}.
$$

$$
\begin{aligned}
\frac12\left\|f\left(\boldsymbol{x}\right)+\boldsymbol{J}\left(\boldsymbol{x}\right)^\mathrm{T}\Delta\boldsymbol{x}\right\|^2& =\frac12\Big(f\left(\boldsymbol{x}\right)+\boldsymbol{J}\left(\boldsymbol{x}\right)^\mathrm{T}\Delta\boldsymbol{x}\Big)^\mathrm{T}\Big(f\left(\boldsymbol{x}\right)+\boldsymbol{J}\left(\boldsymbol{x}\right)^\mathrm{T}\Delta\boldsymbol{x}\Big) \\
&=\frac12\left(\|f(\boldsymbol{x})\|_2^2+2f\left(\boldsymbol{x}\right)\boldsymbol{J}(\boldsymbol{x})^\intercal\Delta\boldsymbol{x}+\Delta\boldsymbol{x}^\intercal\boldsymbol{J}(\boldsymbol{x})\boldsymbol{J}(\boldsymbol{x})^\intercal\Delta\boldsymbol{x}\right).
\end{aligned}
$$

$$
\boldsymbol{J}(\boldsymbol{x})f\left(\boldsymbol{x}\right)+\boldsymbol{J}(\boldsymbol{x})\boldsymbol{J}^\mathrm{T}\left(\boldsymbol{x}\right)\Delta\boldsymbol{x}=\boldsymbol{0}.
$$

$$
\underbrace{\boldsymbol{J}(\boldsymbol{x})\boldsymbol{J}^{\intercal}}_{\boldsymbol{H}(\boldsymbol{x})}\left(\boldsymbol{x}\right)\Delta\boldsymbol{x}=\underbrace{-\boldsymbol{J}(\boldsymbol{x})f\left(\boldsymbol{x}\right)}_{\boldsymbol{g}(\boldsymbol{x})}.
$$

增量方程 or Gauss-Newton equation or Normal equation

$$
H\Delta x=g.
$$

求解增量方程是整个优化问题的核心所在  
总结一下:

1. 给定初始值 $\displaystyle \boldsymbol{x}_{0}$。
2. 对于第 $\displaystyle k$ 次迭代，求解当前的雅可比矩阵 $\displaystyle \boldsymbol{J}(x)$ 和误差 $\displaystyle f(\boldsymbol{x}_{k})$。
3. 求解增量方程: $\displaystyle \boldsymbol{H} \Delta x_{k} = \boldsymbol{g}$。
4. 若 $\displaystyle \Delta x_{k}$ 足够小，则停止。否则，令 $\displaystyle x_{k+1} = x_{k}+ \Delta x_{k}$，返回第 2 步。

#### 6.2.3 列文伯格——马夸尔特方法

Damped Newton Method  
Trust Region  
Trust Region Method

$$
\rho=\frac{f\left(\boldsymbol{x}+\Delta\boldsymbol{x}\right)-f\left(\boldsymbol{x}\right)}{\boldsymbol{J}\left(\boldsymbol{x}\right)^{\intercal}\Delta\boldsymbol{x}}.
$$

框架:

1. 给定初始值 $\displaystyle \boldsymbol{x}_{0}$，以及初始优化半径 $\displaystyle \mu$。
2. 对于第 $\displaystyle k$ 次迭代，在高斯牛顿法的基础上加上信赖区域，求解: $\displaystyle \min_{\Delta\boldsymbol{x}_{k}}\frac{1}{2}\Big\|f\left(\boldsymbol{x}_{k}\right)+\boldsymbol{J}\left(\boldsymbol{x}_{k}\right)^{\mathrm{T}}\Delta\boldsymbol{x}_{k}\Big\|^{2},\quad\mathrm{s.t.}\quad\left\|\boldsymbol{D}\Delta\boldsymbol{x}_{k}\right\|^{2}\leqslant\mu,$ 
3. 计算 $\displaystyle \rho$
4. 对于 $\displaystyle \frac{1}{4}  \frac{3}{4}$ 进行分类讨论
5. 判断阈值，循环

这是带不等式约束的优化问题:

$$
\mathcal{L}(\Delta\boldsymbol{x}_{k},\lambda)=\frac{1}{2}\left\|f\left(\boldsymbol{x}_{k}\right)+\boldsymbol{J}\left(\boldsymbol{x}_{k}\right)^{\mathrm{T}}\Delta\boldsymbol{x}_{k}\right\|^{2}+\frac{\lambda}{2}\left(\left\|\boldsymbol{D}\Delta\boldsymbol{x}_{k}\right\|^{2}-\mu\right).
$$

$$
(H+\lambda D^\mathrm{T}D) \Delta x_k=g.
$$

### 6.3 实践: 曲线拟合问题

#### 6.3.1 手写高斯牛顿法

TODO

#### 6.3.2 使用 Ceres 进行曲线拟合

TODO

#### 6.3.3 使用 g2o进行曲线拟合

TODO

## 7 视觉里程计 1

### 7.1 特征点法

- 特征点法
	- 两视图几何（Two-view geometry）
- 直接法

#### 7.1.1 特征点

- 如何根据图像估计相机运动
- 路标: 图像特征
- 特征点在相机运动之后保持稳定
	- 角点
- 人工设计的特征点:
	- Repeatability
	- Distinctiveness
	- Efficiency
	- Locality
- 由两部分组成:
	- 关键点（Key-point）
	- 描述子（Descriptor）
- SIFT (尺度不变特征变换，Scale-Invariant Feature Transform)
	- 考虑充分，但是计算量比较大
- ORB (Oriented FAST and Rotated BRIEF)

#### 7.1.2 ORB 特征

1. FAST 角点提取: ORB 中计算了特征点的主方向，为后续的 BRIEF 描述子增加了旋转不变特性
2. BRIEF 描述子: 对前一步提取出特征点的周围图像区域进行描述。使用先前计算的方向信息。
- FAST 关键点  
![QQ_1725463627449.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409042327348.png)  
Non-maximal suppression  
尺度不变性由构建图像金字塔  
特征的旋转: Intensity Centroid  
旋转方面，我们计算特征点附近的图像灰度质心。
1. 定义图像的矩: $\displaystyle m_{pq} = \Sigma _{x,y \in B} x^p x^q I(x, y),p,q \in \{0, 1\}$.
2. 找到图像块的质心: $\displaystyle C=\left(\frac{m_{10}}{m_{00}},\frac{m_{01}}{m_{00}}\right).$
3. 得到一个几何中心到质心的方向向量: $\displaystyle \theta=\arctan(m_{01}/m_{10}).$
- BRIEF 描述子  
二进制表达+随机选点比较

#### 7.1.3 特征匹配

data association  
Brute-Force Matcher

- 通过测量描述子的距离来去最近的一个作为匹配点。描述子距离表示了两个特征之间的相似程度。
	- 欧氏距离
	- 汉明距离
		- 两个二进制串的不同位数的个数
- 快速近似最近邻（FLANN）

### 7.2 实践: 特征提取和匹配

#### 7.2.1 OpenCV 的 ORB 特征

TODO

#### 7.2.2 手写 ORB 特征

#### 7.2.3 计算相机运动

1. 当相机为单目时，我们通过对极几何来解决两组 2 D 点估计运动的问题
2. 当相机为双目、RGB-D 时，通过 ICP 来解决两组 3 D 点估计运动的问题
3. 一个是 2 D 一个是 3 D 时，通过 PnP 来求解

### 7.3 D-2 D: 对极几何

#### 7.3.1 对极约束

- Epipolar plane
- Epipoles
- Epipolar line  
![QQ_1725464590361.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409042343436.png)

$$
P=[X,Y,Z]^{\mathrm{T}}.
$$

$$
s_{1}p_{1}=KP,\quad s_{2}p_{2}=K\left(RP+t\right).
$$

成投影关系:尺度意义下相等 (equal up to scale)

$$
sp\simeq p.
$$

$$
p_1\simeq KP,\quad p_2\simeq K\left(RP+t\right).
$$

$$
x_1=K^{-1}p_1,\quad x_2=K^{-1}p_2.
$$

$$
x_2\simeq Rx_1+t.
$$

$$
t^{\wedge}x_{2}\simeq t^{\wedge}Rx_{1}.
$$

$$
x_2^\mathrm{T}t^\wedge x_2\simeq x_2^\mathrm{T}t^\wedge Rx_1.
$$

$$
x_2^\mathrm{T}t^\wedge Rx_1=0.
$$

$$
p_2^\mathrm{T}K^{-\mathrm{T}}t^\wedge RK^{-1}p_1=0.
$$

对极约束

$$
E=t^{\wedge}R,\quad F=K^{-\mathrm{T}}EK^{-1},\quad x_{2}^{\mathrm{T}}Ex_{1}=p_{2}^{\mathrm{T}}Fp_{1}=0.
$$

1. 根据配对点的像素位置求出 $\displaystyle \boldsymbol{E}$ 或者 $\displaystyle \boldsymbol{F}$。
2. 根据 $\displaystyle \boldsymbol{E}$ 或者 $\displaystyle \boldsymbol{F}$ 求出 $\displaystyle \boldsymbol{R},\boldsymbol{t}$。  
$\displaystyle \boldsymbol{E}$ 和 $\displaystyle \boldsymbol{F}$ 只相差了相机内参，所以实践中往往使用形式更简单的 $\displaystyle \boldsymbol{E}$。

#### 7.3.2 本质矩阵

本质矩阵: $\displaystyle E=t^{\wedge}R$

- $\displaystyle \boldsymbol{E}$ 不同尺度下是等价的。
- 可以证明，本质矩阵 $\displaystyle \boldsymbol{E}$ 的奇异值必定是 $\displaystyle [\sigma,\sigma,0]^\mathrm{T}$ 的形式，这称为本质矩阵的内在性质。
- $\displaystyle \boldsymbol{E}$ 实际上有 5 个自由度。  
八点法 (Eight-point-algorithm)  
考虑一堆配对点，它们的归一化坐标为 $\displaystyle x_{1}=[u_{1},v_{1},1]^{\mathrm{T}},x_{2}=[u_{2},v_{2},1]^{\mathrm{T}}$。根据对极约束，有

$$
\begin{pmatrix}u_2,v_2,1\end{pmatrix}\begin{pmatrix}e_1&e_2&e_3\\\\e_4&e_5&e_6\\\\e_7&e_8&e_9\end{pmatrix}\begin{pmatrix}u_1\\\\v_1\\\\1\end{pmatrix}=0.
$$

$$
\boldsymbol{e}=[e_1,e_2,e_3,e_4,e_5,e_6,e_7,e_8,e_9]^\mathrm{T},
$$

$$
[u_2u_1,u_2v_1,u_2,v_2u_1,v_2v_1,v_2,u_1,v_1,1]\cdot e=0.
$$

我们把所有点都放到一个方程中，变成线性方程组:

$$
\begin{pmatrix}u_2^1u_1^1&u_2^1v_1^1&u_2^1&v_2^1u_1^1&v_2^1v_1^1&v_2^1&u_1^1&v_1^1&1\\u_2^2u_1^2&u_2^2v_1^2&u_2^2&v_2^2u_1^2&v_2^2v_1^2&v_2^2&u_1^2&v_1^2&1\\\vdots&\vdots&\vdots&\vdots&\vdots&\vdots&\vdots&\vdots\\u_2^8u_1^8&u_2^8v_1^8&u_2^8&v_2^8u_1^8&v_2^8u_1^8&u_1^8&v_1^8&1\end{pmatrix}\begin{pmatrix}e_1\\e_2\\e_3\\e_4\\e_5\\e_6\\e_7\\e_8\\e_9\end{pmatrix}=0.
$$

$$
E=U\Sigma V^{\mathrm{T}},
$$

$$
\begin{aligned}&t_{1}^{\wedge}=UR_{Z}(\frac{\pi}{2})\Sigma U^{\mathrm{T}},\quad R_{1}=UR_{Z}^{\mathrm{T}}(\frac{\pi}{2})V^{\mathrm{T}}\\&t_{2}^{\wedge}=UR_{Z}(-\frac{\pi}{2})\Sigma U^{\mathrm{T}},\quad R_{2}=UR_{Z}^{\mathrm{T}}(-\frac{\pi}{2})V^{\mathrm{T}}.\end{aligned}
$$

![QQ_1725466210372.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409050010777.png)

$$
\boldsymbol{E}=\boldsymbol{U}\mathrm{diag}(\frac{\sigma_1+\sigma_2}2,\frac{\sigma_1+\sigma_2}2,0)\boldsymbol{V}^\mathrm{T}.
$$

#### 7.3.3 单应矩阵

Homography

## 8 视觉里程计 2

### 8.1 直接法的引出

- 特征点法的缺点
	- 关键点的提取与描述子的计算非常耗时
	- 使用特征点时，会忽略除特征点以外的所有信息
	- 相机有时会运动到特征缺失的地方
- 那么如何克服这些缺点
	- 保留特征点，但只计算关键点，不计算描述子。使用光流法（Optical Flow）跟踪特征点的运动
	- 只计算关键点，不计算描述子。使用直接法（Direct Method）
- 第一种方法仍然使用特征点，只是把匹配描述字替换成了光流跟踪，估计相机运动时仍然是哦那个对极几何、PnP 或 ICP 算法（即，我们需要提到角点）
- 特征点法:通过最小化重投影误差（Reprojection error）优化相机运动
- 直接法: 通过最小化光度误差（Photometric error）
- 只要场景中存在明暗变化就可以工作
	- 稠密
	- 半稠密
	- 稀疏

### 8.2 D 光流

- 计算部分像素运动: 稀疏光流
	- Lucas-Kanasde
- 计算所有像素运动: 稠密光流
	- Horn-Schunck  
![QQ_1725858685580.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409091311387.png)  
**Lucas-Kanade 光流**
- 灰度不变假设: 同一个空间点的像素灰度值，在各个图像中时固定不变的

$$
I(x+\mathrm{d}x,y+\mathrm{d}y,t+\mathrm{d}t)=I(x,y,t).
$$

$$
\boldsymbol{I}\left(x+\mathrm{d}x,y+\mathrm{d}y,t+\mathrm{d}t\right)\approx\boldsymbol{I}\left(x,y,t\right)+\frac{\partial\boldsymbol{I}}{\partial x}\mathrm{d}x+\frac{\partial\boldsymbol{I}}{\partial y}\mathrm{d}y+\frac{\partial\boldsymbol{I}}{\partial t}\mathrm{d}t.
$$

$$
\frac{\partial\boldsymbol{I}}{\partial x}\frac{\mathrm{d}x}{\mathrm{d}t}+\frac{\partial\boldsymbol{I}}{\partial y}\frac{\mathrm{d}y}{\mathrm{d}t}=-\frac{\partial\boldsymbol{I}}{\partial t}.
$$

$$
\begin{bmatrix}I_x&I_y\end{bmatrix}\begin{bmatrix}u\\\\v\end{bmatrix}=-I_t.
$$

$$
\begin{bmatrix}I_x&I_y\end{bmatrix}_k\begin{bmatrix}u\\\\v\end{bmatrix}=-I_{tk},\quad k=1,\ldots,w^2.
$$

$$
A\begin{bmatrix}u\\\\v\end{bmatrix}=-b.
$$

$$
\begin{bmatrix}u\\\\v\end{bmatrix}^*=-\begin{pmatrix}\boldsymbol{A}^\mathrm{T}\boldsymbol{A}\end{pmatrix}^{-1}\boldsymbol{A}^\mathrm{T}\boldsymbol{b}.
$$

### 8.3 实践: LK 光流

#### 8.3.1 使用 LK 光流

```C++
vector<Point2f> pt1, pt2;
for (auto &kp: kp1) pt1.push_back(kp.pt);
vector<uchar> status;
vector<float> error;
cv::calcOpticalFlowPyrLK(img1, img2, pt1, pt2, status, error);
```

#### 8.3.2 用高斯牛顿法实现光流

**单层光流**  
TODO

$$
\min_{\Delta x,\Delta y}\left\|\boldsymbol{I}_1\left(x,y\right)-\boldsymbol{I}_2\left(x+\Delta x,y+\Delta y\right)\right\|_2^2.
$$

**多层光流**
- 由粗至精（Coarse-to-fine）

#### 8.3.3 光流实践小结

### 8.4 直接法

#### 8.4.1 直接法的推导

![QQ_1725859950007.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409091332369.png)

$$
\boldsymbol{p}_1=\begin{bmatrix}u\\\\v\\\\1\end{bmatrix}_1=\frac{1}{Z_1}\boldsymbol{K}\boldsymbol{P},
$$

$$
\boldsymbol{p}_{2}=\begin{bmatrix}u\\\\v\\\\1\end{bmatrix}_{2}=\frac{1}{Z_{2}}\boldsymbol{K}\left(\boldsymbol{R}\boldsymbol{P}+\boldsymbol{t}\right)=\frac{1}{Z_{2}}\boldsymbol{K}\left(\boldsymbol{T}\boldsymbol{P}\right)_{1:3}.
$$

$$
e=\boldsymbol{I}_1\left(\boldsymbol{p}_1\right)-\boldsymbol{I}_2\left(\boldsymbol{p}_2\right).
$$

$$
\min_{T}J\left(T\right)=\left\|e\right\|^{2}.
$$

$$
\min_{\boldsymbol{T}}J\left(\boldsymbol{T}\right)=\sum_{i=1}^{N}e_{i}^{\mathrm{T}}e_{i},\quad e_{i}=\boldsymbol{I}_{1}\left(\boldsymbol{p}_{1,i}\right)-\boldsymbol{I}_{2}\left(\boldsymbol{p}_{2,i}\right).
$$

$$
\begin{aligned}&q=TP,\\&\boldsymbol{u}=\frac{1}{Z_{2}}Kq.\end{aligned}
$$

$$
e(T)=I_1(p_1)-I_2(u),
$$

$$
\frac{\partial e}{\partial\boldsymbol{T}}=\frac{\partial\boldsymbol{I}_{2}}{\partial\boldsymbol{u}}\frac{\partial\boldsymbol{u}}{\partial\boldsymbol{q}}\frac{\partial\boldsymbol{q}}{\partial\delta\boldsymbol{\xi}}\delta\boldsymbol{\xi},
$$

$$
\frac{\partial\boldsymbol{u}}{\partial\boldsymbol{q}}=\begin{bmatrix}\frac{\partial u}{\partial X}&\frac{\partial u}{\partial Y}&\frac{\partial u}{\partial Z}\\\frac{\partial v}{\partial X}&\frac{\partial v}{\partial Y}&\frac{\partial v}{\partial Z}\end{bmatrix}=\begin{bmatrix}\frac{f_x}{Z}&0&-\frac{f_xX}{Z^2}\\0&\frac{f_y}{Z}&-\frac{f_yY}{Z^2}\end{bmatrix}.
$$

$$
\frac{\partial\boldsymbol{q}}{\partial\delta\boldsymbol{\xi}}=\left[I,-\boldsymbol{q}^{\wedge}\right].
$$

$$
\frac{\partial\boldsymbol{u}}{\partial\delta\boldsymbol{\xi}}=\begin{bmatrix}\frac{f_x}{Z}&0&-\frac{f_xX}{Z^2}&-\frac{f_xXY}{Z^2}&f_x+\frac{f_xX^2}{Z^2}&-\frac{f_xY}{Z}\\0&\frac{f_y}{Z}&-\frac{f_yY}{Z^2}&-f_y-\frac{f_yY^2}{Z^2}&\frac{f_yXY}{Z^2}&\frac{f_yX}{Z}\end{bmatrix}.
$$

$$
J=-\frac{\partial I_2}{\partial u}\frac{\partial u}{\partial\delta\xi}.
$$

#### 8.4.2 直接法的讨论

### 8.5 实践: 直接法

#### 8.5.1 单层直接法

#### 8.5.2 多层直接法

#### 8.5.3 结果讨论

- Normalized Cross

#### 8.5.4 直接法优缺点总结

## 9 后端 1

### 9.1 概述

#### 9.1.1 状态估计的概率解释

- 只使用过去的信息: 渐进的（Incremental）
- 使用未来的信息更新: 批量的（Batch）

$$
\begin{cases}\boldsymbol{x}_k=f\left(\boldsymbol{x}_{k-1},\boldsymbol{u}_k\right)+\boldsymbol{w}_k\\\boldsymbol{z}_{k,j}=h\left(\boldsymbol{y}_j,\boldsymbol{x}_k\right)+\boldsymbol{v}_{k,j}\end{cases}\quad k=1,\ldots,N, j=1,\ldots,M.
$$

- 观测方程的数量会远远大于运动方程
- 当没有运动方程的时候，我们可以假设相机不动，或假设相机匀速运动
- 问题：当存在一些运动数据和观测数据时，我们如何估计状态量的高斯分布
- 误差时逐渐累积的
- 最大似然估计: 批量状态估计问题可以转化为最大似然估计问题，并使用最小二乘法进行求解

$$
x_k\stackrel{\mathrm{def}}{=}\{x_k,y_1,\ldots,y_m\}.
$$

$$
\begin{cases}\boldsymbol{x}_k=f\left(\boldsymbol{x}_{k-1},\boldsymbol{u}_k\right)+\boldsymbol{w}_k\\\boldsymbol{z}_k=h\left(\boldsymbol{x}_k\right)+\boldsymbol{v}_k\end{cases}\quad k=1,\ldots,N.
$$

$$
P\left(\boldsymbol{x}_k|\boldsymbol{x}_0,\boldsymbol{u}_{1:k},\boldsymbol{z}_{1:k}\right)\propto P\left(\boldsymbol{z}_k|\boldsymbol{x}_k\right)P\left(\boldsymbol{x}_k|\boldsymbol{x}_0,\boldsymbol{u}_{1:k},\boldsymbol{z}_{1:k-1}\right).
$$

- 第一项称为似然，第二项称为先验

$$
P\left(\boldsymbol{x}_{k}|\boldsymbol{x}_{0},\boldsymbol{u}_{1:k},\boldsymbol{z}_{1:k-1}\right)=\int P\left(\boldsymbol{x}_{k}|\boldsymbol{x}_{k-1},\boldsymbol{x}_{0},\boldsymbol{u}_{1:k},\boldsymbol{z}_{1:k-1}\right)P\left(\boldsymbol{x}_{k-1}|\boldsymbol{x}_{0},\boldsymbol{u}_{1:k},\boldsymbol{z}_{1:k-1}\right)\mathrm{d}\boldsymbol{x}_{k-1}.
$$

- 虽然可以继续对此式进行展开，但我们只关心 $\displaystyle k$ 时刻和 $\displaystyle k - 1$ 时刻的情况
	- 第一种方法是假设马尔可夫性: 即认为 $\displaystyle k$ 时刻状态只与 $\displaystyle k - 1$ 时刻状态有关
		- 那么我们就可以得到以扩展卡尔曼滤波（EKF）为代表的滤波器方式
	- 第二种方法是依然考虑和之前所有状态的关系，姿势会得到非线性优化为主体的优化框架。
	- 主流是非线性优化

#### 9.1.2 线性系统和 KF

$$
P\left(\boldsymbol{x}_k|\boldsymbol{x}_{k-1},\boldsymbol{x}_0,\boldsymbol{u}_{1:k},\boldsymbol{z}_{1:k-1}\right)=P\left(\boldsymbol{x}_k|\boldsymbol{x}_{k-1},\boldsymbol{u}_k\right).
$$

$$
P\left(\boldsymbol{x}_{k-1}|\boldsymbol{x}_0,\boldsymbol{u}_{1:k},\boldsymbol{z}_{1:k-1}\right)=P\left(\boldsymbol{x}_{k-1}|\boldsymbol{x}_0,\boldsymbol{u}_{1:k-1},\boldsymbol{z}_{1:k-1}\right).
$$

- 所以我们实际在做的事如何把 $\displaystyle k - 1$ 时刻的状态分布推导至 $\displaystyle k$ 时刻
	- 即我们只要维护一个状态，并不断地迭代更新
		- 只要维护状态量的均值和协方差（状态量服从高斯分布）

$$
\begin{cases}x_k=A_kx_{k-1}+u_k+w_k\\z_k=C_kx_k+v_k\end{cases}\quad k=1,\ldots,N.
$$

$$
w_k\sim N(0,\boldsymbol{R}).\quad\boldsymbol{v}_k\sim N(\boldsymbol{0},\boldsymbol{Q}).
$$

- 上帽子表示后验，下帽子表示先验

$$
P\left(\boldsymbol{x}_k|\boldsymbol{x}_0,\boldsymbol{u}_{1:k},\boldsymbol{z}_{1:k-1}\right)=N\left(\boldsymbol{A}_k\hat{x}_{k-1}+\boldsymbol{u}_k,\boldsymbol{A}_k\hat{\boldsymbol{P}}_{k-1}\boldsymbol{A}_k^\mathrm{T}+\boldsymbol{R}\right).
$$

- 这一步称为预测（Predict）

$$
\check{\boldsymbol{x}}_k=\boldsymbol{A}_k\hat{\boldsymbol{x}}_{k-1}+\boldsymbol{u}_k,\quad\check{\boldsymbol{P}}_k=A_k\hat{\boldsymbol{P}}_{k-1}\boldsymbol{A}_k^\mathrm{T}+\boldsymbol{R}.
$$

$$
P\left(\boldsymbol{z}_k|\boldsymbol{x}_k\right)=N\left(\boldsymbol{C}_k\boldsymbol{x}_k,\boldsymbol{Q}\right).
$$

- 如果结果设为 $\displaystyle x_k\sim N(\hat{\boldsymbol{x}}_k,\hat{\boldsymbol{P}}_k)$，那么

$$
N(\hat{\boldsymbol{x}}_k,\hat{\boldsymbol{P}}_k)=\eta N\left(\boldsymbol{C}_k\boldsymbol{x}_k,\boldsymbol{Q}\right)\cdot N(\check{\boldsymbol{x}}_k,\check{\boldsymbol{P}}_k).
$$

$$
(\boldsymbol{x}_{k}-\hat{\boldsymbol{x}}_{k})^{\mathrm{T}}\hat{\boldsymbol{P}}_{k}^{-1}\left(\boldsymbol{x}_{k}-\hat{\boldsymbol{x}}_{k}\right)=\left(\boldsymbol{z}_{k}-\boldsymbol{C}_{k}\boldsymbol{x}_{k}\right)^{\mathrm{T}}\boldsymbol{Q}^{-1}\left(\boldsymbol{z}_{k}-\boldsymbol{C}_{k}\boldsymbol{x}_{k}\right)+\left(\boldsymbol{x}_{k}-\check{\boldsymbol{x}}_{k}\right)^{\mathrm{T}}\boldsymbol{P}_{k}^{-1}\left(\boldsymbol{x}_{k}-\check{\boldsymbol{x}}_{k}\right).
$$

- 二次系数

$$
\hat{P}_k^{-1}=C_k^{\mathrm{T}}Q^{-1}C_k+\check{P}_k^{-1}.
$$

- 定义一个中间变量

$$
K=\hat{P}_kC_k^{\mathrm{T}}Q^{-1}.
$$

$$
I=\hat{P}_{k}C_{k}^{\mathrm{T}}Q^{-1}C_{k}+\hat{P}_{k}\check{P}_{k}^{-1}=KC_{k}+\hat{P}_{k}\check{P}_{k}^{-1}.
$$

$$
\hat{P}_{k}=(I-KC_{k})\check{P}_{k}.
$$

- 一次项系数

$$
-2\hat{\boldsymbol{x}}_k^\mathrm{T}\hat{\boldsymbol{P}}_k^{-1}\boldsymbol{x}_k=-2\boldsymbol{z}_k^\mathrm{T}\boldsymbol{Q}^{-1}\boldsymbol{C}_k\boldsymbol{x}_k-2\boldsymbol{\dot{x}}_k^\mathrm{T}\check{\boldsymbol{P}}_k^{-1}\boldsymbol{x}_k.
$$

$$
\hat{\boldsymbol{P}}_k^{-1}\hat{\boldsymbol{x}}_k=\boldsymbol{C}_k^\mathrm{T}\boldsymbol{Q}^{-1}\boldsymbol{z}_k+\check{\boldsymbol{P}}_k^{-1}\check{\boldsymbol{x}}_k.
$$

$$
\begin{aligned}
\hat{x}_{k}& =\hat{\boldsymbol{P}}_k\boldsymbol{C}_k^\mathrm{T}\boldsymbol{Q}^{-1}\boldsymbol{z}_k+\hat{\boldsymbol{P}}_k\check{\boldsymbol{P}}_k^{-1}\check{\boldsymbol{x}}_k \\
&=K\boldsymbol{z}_k+\left(\boldsymbol{I}-\boldsymbol{K}\boldsymbol{C}_k\right)\check{\boldsymbol{x}}_k=\check{\boldsymbol{x}}_k+\boldsymbol{K}\left(\boldsymbol{z}_k-\boldsymbol{C}_k\check{\boldsymbol{x}}_k\right).
\end{aligned}
$$

![QQ_1725871447753.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409091644803.png)

#### 9.1.3 非线性系统和 EKF

- 扩展卡尔曼滤波器
	- 即把非高斯分布近似成高斯分布

$$
\boldsymbol{x}_k\approx f\left(\hat{\boldsymbol{x}}_{k-1},\boldsymbol{u}_k\right)+\left.\frac{\partial f}{\partial\boldsymbol{x}_{k-1}}\right|_{\tilde{\boldsymbol{x}}_{k-1}}\left(\boldsymbol{x}_{k-1}-\hat{\boldsymbol{x}}_{k-1}\right)+\boldsymbol{w}_k.
$$

$$
\boldsymbol{F}=\left.\frac{\partial f}{\partial\boldsymbol{x}_{k-1}}\right|_{\hat{\boldsymbol{x}}_{k-1}}.
$$

$$
z_k\approx h\left(\check{\boldsymbol{x}}_k\right)+\left.\frac{\partial h}{\partial\boldsymbol{x}_k}\right|_{\dot{\boldsymbol{x}}_k}\left(\boldsymbol{x}_k-\check{\boldsymbol{x}}_k\right)+\boldsymbol{n}_k.
$$

$$
H=\left.\frac{\partial h}{\partial\boldsymbol{x}_k}\right|_{\check{\boldsymbol{x}}_k}.
$$

$$
P\left(\boldsymbol{x}_k|\boldsymbol{x}_0,\boldsymbol{u}_{1:k},\boldsymbol{z}_{0:k-1}\right)=N(f\left(\hat{\boldsymbol{x}}_{k-1},\boldsymbol{u}_k\right),\boldsymbol{F}\hat{\boldsymbol{P}}_{k-1}\boldsymbol{F}^\mathrm{T}+\boldsymbol{R}_k).
$$

$$
\check{\boldsymbol{x}}_k=f\left(\hat{\boldsymbol{x}}_{k-1},\boldsymbol{u}_k\right),\quad\check{\boldsymbol{P}}_k=\boldsymbol{F}\hat{\boldsymbol{P}}_{k-1}\boldsymbol{F}^\mathrm{T}+\boldsymbol{R}_k.
$$

$$
P\left(\boldsymbol{z}_k|\boldsymbol{x}_k\right)=N(h\left(\check{\boldsymbol{x}}_k\right)+\boldsymbol{H}\left(\boldsymbol{x}_k-\check{\boldsymbol{x}}_k\right),Q_k).
$$

- 定义一个卡尔曼增益 $\displaystyle \boldsymbol{K}_{k}$

$$
K_{k}=\check{P}_{k}H^{\mathrm{T}}(H\check{P}_{k}H^{\mathrm{T}}+Q_{k})^{-1}.
$$

$$
\hat{\boldsymbol{x}}_k=\check{\boldsymbol{x}}_k+\boldsymbol{K}_k\left(\boldsymbol{z}_k-h\left(\check{\boldsymbol{x}}_k\right)\right),\hat{\boldsymbol{P}}_k=\left(\boldsymbol{I}-\boldsymbol{K}_k\boldsymbol{H}\right)\check{\boldsymbol{P}}_k.
$$

#### 9.1.4 EKF 的讨论

- 局限
	- 假设了马尔可夫性，但是非线性优化是全体时间上的 SLAM (Full-SLAM)
	- 有非线性误差（主要问题所在）
	- 如果把路标也放进状态，存不下
	- 没有异常检测机制

### 9.2 BA 与图优化

- Bundle Adjustment
	- 从视觉图像中提炼出最有的 3 D 模型和相机参数，让光线最终收束到相机的光心

#### 9.2.1 投影模型和 BA 代价函数

$$
P^{\prime}=Rp+t=[X^{\prime},Y^{\prime},Z^{\prime}]^\mathrm{T}.
$$

$$
\boldsymbol{P}_{\mathrm{c}}=[u_{\mathrm{c}},v_{\mathrm{c}},1]^{\mathrm{T}}=[X^{\prime}/Z^{\prime},Y^{\prime}/Z^{\prime},1]^{\mathrm{T}}.
$$

$$
\begin{cases}u_\mathrm{c}'=u_\mathrm{c}\left(1+k_1r_\mathrm{c}^2+k_2r_\mathrm{c}^4\right)\\v_\mathrm{c}'=v_\mathrm{c}\left(1+k_1r_\mathrm{c}^2+k_2r_\mathrm{c}^4\right)\end{cases}.
$$

$$
\begin{cases}u_s=f_xu_\mathrm{c}'+c_x\\[2ex]v_s=f_yv_\mathrm{c}'+c_y\end{cases}.
$$

$$
z=h(\boldsymbol{x},\boldsymbol{y}).
$$

![QQ_1725872841730.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409091707361.png)

$$
e=z-h(\boldsymbol{T},\boldsymbol{p}).
$$

$$
z\overset{\mathrm{def}}{\operatorname*{=}}[u_s,v_s]^\mathrm{T}
$$

$$
\frac12\sum_{i=1}^m\sum_{j=1}^n\|e_{ij}\|^2=\frac12\sum_{i=1}^m\sum_{j=1}^n\|z_{ij}-h(\boldsymbol{T}_i,\boldsymbol{p}_j)\|^2.
$$

#### 9.2.2 BA 的求解

$$
x=[T_1,\ldots,T_m,p_1,\ldots,p_n]^\mathrm{T}.
$$

$$
\frac12\left\|f(\boldsymbol{x}+\Delta\boldsymbol{x})\right\|^2\approx\frac12\sum_{i=1}^m\sum_{j=1}^n\left\|\boldsymbol{e}_{ij}+\boldsymbol{F}_{ij}\Delta\boldsymbol{\xi}_i+\boldsymbol{E}_{ij}\Delta\boldsymbol{p}_j\right\|^2.
$$

$$
x_{\mathfrak{c}}=[\boldsymbol{\xi}_1,\boldsymbol{\xi}_2,\ldots,\boldsymbol{\xi}_m]^{\mathrm{T}}\in\mathbb{R}^{6m}
$$

$$
\boldsymbol{x}_p=[\boldsymbol{p}_1,\boldsymbol{p}_2,\ldots,\boldsymbol{p}_n]^\mathrm{T}\in\mathbb{R}^{3n}
$$

$$
\frac12\left\|f(\boldsymbol{x}+\Delta\boldsymbol{x})\right\|^2=\frac12\left\|\boldsymbol{e}+\boldsymbol{F}\Delta\boldsymbol{x}_c+\boldsymbol{E}\Delta\boldsymbol{x}_p\right\|^2.
$$

$$
\boldsymbol{J}=[\boldsymbol{F}\boldsymbol{E}].
$$

$$
H=J^\mathrm{T}J=\begin{bmatrix}F^\mathrm{T}F&F^\mathrm{T}E\\E^\mathrm{T}F&E^\mathrm{T}E\end{bmatrix}.
$$

#### 9.2.3 稀疏性和边缘化

$$
J_{ij}(x)=\left(\mathbf{0}_{2\times6},\ldots\mathbf{0}_{2\times6},\frac{\partial\boldsymbol{e}_{ij}}{\partial\boldsymbol{T}_{i}},\mathbf{0}_{2\times6},\ldots\mathbf{0}_{2\times3},\ldots\mathbf{0}_{2\times3},\frac{\partial\boldsymbol{e}_{ij}}{\partial\boldsymbol{p}_{j}},\mathbf{0}_{2\times3},\ldots\mathbf{0}_{2\times3}\right).
$$

$$
H=\sum_{i,j}J_{ij}^{\top}J_{ij},
$$

$$
H=\begin{bmatrix}H_{11}&H_{12}\\\\H_{21}&H_{22}\end{bmatrix}.
$$

![QQ_1725873562244.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409091719496.png)  
![QQ_1725874123833.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409091728991.png)

- 对于稀疏矩阵，我们用 Schur 消元（Marginalization）

$$
\begin{bmatrix}B&E\\E^\mathrm{T}&C\end{bmatrix}\begin{bmatrix}\Delta x_\mathrm{c}\\\Delta x_p\end{bmatrix}=\begin{bmatrix}v\\w\end{bmatrix}.
$$

$$
\begin{bmatrix}I&-EC^{-1}\\0&I\end{bmatrix}\begin{bmatrix}B&E\\E^{\intercal}&C\end{bmatrix}\begin{bmatrix}\Delta x_\mathrm{c}\\\Delta x_p\end{bmatrix}=\begin{bmatrix}I&-EC^{-1}\\0&I\end{bmatrix}\begin{bmatrix}v\\w\end{bmatrix}.
$$

$$
\begin{bmatrix}B-EC^{-1}E^\mathrm{T}&0\\E^\mathrm{T}&C\end{bmatrix}\begin{bmatrix}\Delta x_\mathrm{c}\\\Delta x_p\end{bmatrix}=\begin{bmatrix}v-EC^{-1}w\\\\w\end{bmatrix}.
$$

$$
\begin{bmatrix}B-EC^{-1}E^\mathrm{T}\end{bmatrix}\Delta x_\mathrm{c}=v-EC^{-1}w.
$$

- 优势
	- $\displaystyle \boldsymbol{C}$ 为对角块，逆比较容易解出
- 非对角线上的非零矩阵块表示对应的两个相机变量之间存在共同观测的路标点，即共视（Co-visibility）

#### 9.2.4 鲁棒核函数

- Robust Kernel

$$
H(e)=\begin{cases}\frac{1}{2}e^2&\text{当}|e|\leqslant\delta,\\\\\delta\left(|e|-\frac{1}{2}\delta\right)&\text{其他}\end{cases}
$$

![QQ_1725898890681.png](https://cdn.jsdelivr.net/gh/WncFht/picture/202409100021134.png)

### 9.3 实践: Ceres BA

#### 9.3.1 BAL 数据集

#### 9.3.2 Ceres BA 的书写

### 9.4 实践: g 2 o 求解 BA

### 9.5 小结

## 10 后端 2

## 11 回环检测

## 12 建图

## 13 实践: 设计 SLAM 系统

## 14 SLAM: 现在与未来
