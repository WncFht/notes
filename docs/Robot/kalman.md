# 卡尔曼滤波

## 1 Why

- 差分
	- 受噪声干扰大
	- 有延迟
	- 速度不连续（不能得到瞬时速度）

## 2 How

### 2.1 卡尔曼滤波

- 合理地根据误差来推导，而不是直接忽视影响最终量
	- [无人驾驶技术入门（十三）| 手把手教你写卡尔曼滤波器 - 知乎](https://zhuanlan.zhihu.com/p/45238681)  

$$
\begin{array}{|c|}\hline\textbf{Prediction}\\\hline x^{'}=Ax+u\\P^{'}=APA^{T}+R\\\hline\textbf{Measurement update}\\\hline y=z-Cx^{'}\\S=CPC^{T}+Q\\K=PC^{T}S^{-1}\\x=x^{'}+Ky\\P=(I-KC)P\\\hline\end{array}
$$

```C++
#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <ctime>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <Eigen/Dense>
#include <opencv2/core/eigen.hpp>
using namespace std;
using namespace cv;
using namespace Eigen;

int main() {
srand((unsigned int) time(NULL));
// generate data with noise
const int N = 20;
const double k = 2.5;
Matrix<double, 1, N> noise = Matrix<double, 1, N>::Random();
Matrix<double, 1, N> data = Matrix<double, 1, N>::LinSpaced(0, k * (N - 1));
data += noise;
std::cout << data << std::endl;
// calculate speed
const int Z_N = 1, X_N = 2;
Matrix<double, X_N, 1> X;
Matrix<double, X_N, X_N> A;
Matrix<double, X_N, X_N> P;
Matrix<double, X_N, X_N> R;
Matrix<double, X_N, Z_N> K;
Matrix<double, Z_N, X_N> C;
Matrix<double, Z_N, Z_N> Q;

X << data[0], 0;
A << 1, 1, 0, 1;
C << 1, 0;
R << 2, 0, 0, 2;
Q << 10;
for (int i = 1; i < N; i++) {
	// 更新预测
	Matrix<double, X_N, 1> X_k = A * X;
	P = A * P * A.transpose() + R;
	// 更新观测
	K = P * C.transpose() * (C * P * C.transpose() + Q).inverse();
	Matrix<double, Z_N, 1> Z{data[i]};
	X = X_k + K * (Z - C * X_k);
	P = (Matrix<double, X_N, X_N>::Identity() - K * C) * P;
	std::cout << "step " << i << ": " << X[1] << std::endl;
}
std:cout << "final speed: " << X[1] << std::endl;
return 0;
}
```

### 2.2 EKF 算法的实现

```C++
#include <ceres/jet.h>
#include <Eigen/Dense>

template<int N_X, int N_Y>
class AdaptiveEKF {
    using MatrixXX = Eigen::Matrix<double, N_X, N_X>;
    using MatrixYX = Eigen::Matrix<double, N_Y, N_X>;
    using MatrixXY = Eigen::Matrix<double, N_X, N_Y>;
    using MatrixYY = Eigen::Matrix<double, N_Y, N_Y>;
    using VectorX = Eigen::Matrix<double, N_X, 1>;
    using VectorY = Eigen::Matrix<double, N_Y, 1>;

public:
    explicit AdaptiveEKF(const VectorX &X0 = VectorX::Zero())
            : Xe(X0), P(MatrixXX::Identity()), Q(MatrixXX::Identity()), R(MatrixYY::Identity()) {}

    // 预测函数
    template<class Func>
    VectorX predict(Func &&func) {
        calculateJacobian(Xe, func, Xp, F);
        P = F * P * F.transpose() + Q;
        return Xp;
    }

    // 更新函数
    template<class Func>
    VectorX update(Func &&func, const VectorY &Y) {
        calculateJacobian(Xp, func, Yp, H);
        MatrixYY S = H * P * H.transpose() + R;  // 创新协方差
        K = P * H.transpose() * S.inverse();     // 卡尔曼增益
        Xe = Xp + K * (Y - Yp);                  // 更新状态估计
        P = (MatrixXX::Identity() - K * H) * P;  // 更新状态协方差
        return Xe;
    }

private:
    // 计算雅克比矩阵的辅助函数
    template<class Func, int N_IN, int N_OUT>
    void calculateJacobian(const Eigen::Matrix<double, N_IN, 1> &input, Func &&func, Eigen::Matrix<double, N_OUT, 1> &output, Eigen::Matrix<double, N_OUT, N_IN> &jacobian) {
        ceres::Jet<double, N_IN> input_auto_jet[N_IN];
        for (int i = 0; i < N_IN; i++) {
            input_auto_jet[i].a = input[i];
            input_auto_jet[i].v[i] = 1;
        }
        ceres::Jet<double, N_OUT> output_auto_jet[N_OUT];
        func(input_auto_jet, output_auto_jet);
        for (int i = 0; i < N_OUT; i++) {
            output[i] = output_auto_jet[i].a;
            jacobian.block(i, 0, 1, N_IN) = output_auto_jet[i].v.transpose();
        }
    }

public:
    VectorX Xe;     // 估计状态变量
    VectorX Xp;     // 预测状态变量
    MatrixXX F;     // 预测雅克比矩阵
    MatrixYX H;     // 观测雅克比矩阵
    MatrixXX P;     // 状态协方差
    MatrixXX Q;     // 预测过程协方差
    MatrixYY R;     // 观测过程协方差
    MatrixXY K;     // 卡尔曼增益
    VectorY Yp;     // 预测观测量
};
```

### 2.3 非线性优化

TODO

## 一些资料

- [zhuanlan.zhihu.com/p/45238681](https://zhuanlan.zhihu.com/p/45238681)
- [卡尔曼滤波(Kalman Filter)概念介绍及详细公式推导-CSDN博客](https://blog.csdn.net/qq_37214693/article/details/130927283)
- 调节误差矩阵的实际意义
- 非线性拓展
- 自适应优化
- 作业中有一个天体运动的例子
