# Docker从入门到实践：以FFB6D环境配置为例

## 1. 简介

Docker是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的Linux或Windows操作系统上。本文将以配置FFB6D（一个3D目标检测模型）的运行环境为例，介绍Docker的基本使用。

## 2. 环境准备

### 2.1 系统要求

- Ubuntu 20.04/22.04/24.04 
- NVIDIA GPU（支持CUDA）
- 至少8GB内存
- 至少30GB磁盘空间

### 2.2 基础组件安装

**安装Docker**

```bash
# 更新apt包索引
sudo apt-get update

# 安装必要的系统工具
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 添加Docker的官方GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 设置稳定版仓库
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# 验证安装
sudo docker run hello-world
```

**安装NVIDIA驱动**

```bash
# 添加NVIDIA包仓库
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt-get update

# 安装NVIDIA驱动
sudo apt-get install -y nvidia-driver-535  # 根据需要选择版本

# 重启系统
sudo reboot

# 验证安装
nvidia-smi
```

**安装NVIDIA Container Toolkit**

```bash
# 设置稳定版仓库
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/ubuntu22.04/$(arch) /" | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# 更新软件包列表
sudo apt-get update

# 安装nvidia-docker2
sudo apt-get install -y nvidia-container-toolkit

# 重启Docker服务
sudo systemctl restart docker

# 测试GPU支持
sudo docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
```

### 2.3 Docker配置优化

**配置镜像加速**

```bash
sudo tee /etc/docker/daemon.json << EOF
{
  "registry-mirrors": [
    "https://docker.1panel.dev",
    "https://docker.zhai.cm",
    "https://hub.littlediary.cn",
    "https://docker.nastool.de"
  ],
  "dns": ["8.8.8.8", "8.8.4.4"],
  "max-concurrent-downloads": 10,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 3. FFB6D环境配置实例

### 3.1 项目结构

```bash
ffb6d_docker/
├── Dockerfile
├── docker-compose.yml
├── build_and_run.sh
├── downloads/
│   ├── apex/
│   └── normalspeed/
├── code/
├── datasets/
├── models/
└── train_log/
```

### 3.2 创建Dockerfile

```dockerfile
# 使用较新的 CUDA 镜像
FROM nvcr.io/nvidia/cuda:11.0.3-cudnn8-devel-ubuntu18.04

# 使用 NVIDIA CUDA 11.3 基础镜像
# FROM nvcr.io/nvidia/cuda:11.3.1-cudnn8-devel-ubuntu20.04

# 避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/workspace/code
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

WORKDIR /workspace

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3.6 \
    python3.6-dev \
    python3-pip \
    git \
    cmake \
    build-essential \
    libopencv-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libboost-all-dev \
    libeigen3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 设置 Python 3.6 为默认版本
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
RUN update-alternatives --set python3 /usr/bin/python3.6

# 升级 pip
RUN python3 -m pip install --upgrade pip

# 配置pip镜像源
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 先安装 PyTorch (使用较新但兼容的版本)
RUN pip3 install torch==1.10.2+cu113 torchvision==0.11.3+cu113 -f https://download.pytorch.org/whl/torch_stable.html

# 复制预下载的文件
COPY downloads/apex /workspace/apex
COPY downloads/normalspeed /workspace/normalspeed
COPY code /workspace/code

# 安装 apex
#RUN cd /workspace/apex && \
#    pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./ || \
#    (echo "Apex installation failed. Check the error messages above." && exit 1)

# 安装 normalspeed
#RUN cd /workspace/normalspeed && \
#    python3 setup.py build_ext --inplace && \
#    python3 setup.py install

WORKDIR /workspace/code
```

更改 `requirement.txt` 

```
h5py         
numpy              
pyyaml==5.4.1
enum34        
future           
scipy==1.4.1          
opencv_contrib_python==3.4.2.16               
transforms3d==0.3.1     
scikit_image==0.13.1     
lmdb==0.94              
setuptools==41.0.0    
cffi==1.11.5         
easydict==1.7      
plyfile==0.6      
pillow==8.2.0 
dataclasses
glumpy                                                      
tqdm
tensorboardX 
pandas
scikit-learn         
scipy 
termcolor
pybind11
```

### 3.3 创建docker-compose.yml

```yaml
version: '3'
services:
  ffb6d:
    build: .
    image: ffb6d:latest
    container_name: ffb6d_container
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    volumes:
      - ./datasets:/workspace/code/datasets
      - ./train_log:/workspace/code/train_log
      - ./models:/workspace/code/models
    shm_size: '8gb'
    tty: true
    stdin_open: true
```

### 3.4 构建和运行脚本

创建`build_and_run.sh`：

```bash
#!/bin/bash

# 创建必要目录
mkdir -p downloads datasets models train_log

# 下载依赖
cd downloads
if [ ! -d "apex" ]; then
  git clone https://github.com/NVIDIA/apex.git
fi
if [ ! -d "normalspeed" ]; then
  git clone https://github.com/hfutcgncas/normalspeed.git
fi
cd ..

# 克隆FFB6D代码
if [ ! -d "code" ]; then
  git clone https://github.com/ethnhe/FFB6D.git code
fi

# 构建镜像
docker-compose build

# 运行容器
docker-compose up -d
docker exec -it ffb6d_container bash
```

### 3.5 启动和验证

```bash
# 添加执行权限
chmod +x build_and_run.sh

# 运行
./build_and_run.sh

# 在容器内验证
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"
python3 -c "from apex import amp; print('APEX installed')"
python3 -c "import normalspeed; print('normalspeed installed')"
```

### 3.6 编译 apex

```
git clone https://github.com/NVIDIA/apex
cd apex
export TORCH_CUDA_ARCH_LIST="6.0;6.1;6.2;7.0;7.5"
python setup.py install -v
```

### 3.7 编译 normalspeed

```
# 1. 卸载当前cv2
pip uninstall opencv-python opencv-python-headless -y

# 2. 安装特定版本的OpenCV，选择与Python 3.6兼容的版本
pip install opencv-python==4.5.3.56

# 3. 验证安装
python3 -c "import cv2; print(cv2.__version__)"

```

```
# 进入normalSpeed目录
cd /workspace/code/normalspeed/normalSpeed

# 安装依赖
apt-get update
apt-get install python3-pybind11
pip3 install Cython==0.29.15

# 清理之前的构建
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# 重新安装
python3 setup.py install

# 验证安装
python3 -c "import normalSpeed"

# 返回ffb6d目录
cd /workspace/code/ffb6d/
```

```
python3 setup.py install --user
```

### 3.8 训练

把 LineMOD 复制到对应的路径下，然后按官网来就好了

## 4. 常见问题

### 4.1 网络问题

如果遇到下载慢或失败：

```bash
# 临时使用代理
export http_proxy="http://proxy:port"
export https_proxy="http://proxy:port"

# 或修改pip源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**注意**用了代理的话，docker hub 镜像就会被覆盖掉，导致速度很慢。所以到时候一定要取消代理 / 删除代理文件

docker hub 镜像设置上面写了，官网是这个 [GitHub - dongyubin/DockerHub: 2024年11月更新，目前国内可用Docker镜像源汇总，DockerHub国内镜像加速列表，🚀DockerHub镜像加速器](https://github.com/dongyubin/DockerHub)

### 4.2 CUDA兼容性

确保NVIDIA驱动版本支持所需的CUDA版本：

```bash
# 检查支持的最高CUDA版本
nvidia-smi
```

### 4.3 内存不足

调整Docker内存限制：

```yaml
# 在docker-compose.yml中添加
services:
  ffb6d:
    deploy:
      resources:
        limits:
          memory: 16G
```

## 5. 总结

本文介绍了使用Docker配置深度学习环境的完整流程，以FFB6D为例展示了如何处理复杂依赖关系。通过容器化技术，我们可以：

1. 确保环境一致性
2. 简化部署流程
3. 提高开发效率
4. 方便团队协作

希望本教程能帮助你更好地理解和使用Docker。

## 参考资料

1. [Docker官方文档](https://docs.docker.com/)
2. [NVIDIA Docker文档](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/overview.html)
3. [FFB6D项目](https://github.com/ethnhe/FFB6D)
4. [【论文笔记】FFB6D | 马浩飞丨博客](https://www.mahaofei.com/post/d027527.html)
