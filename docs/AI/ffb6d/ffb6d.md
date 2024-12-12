# FFB6D环境配置指南：原生系统安装

## 1. 系统要求

- Ubuntu 20.04/22.04/24.04
- NVIDIA GPU（支持CUDA）
- 至少8GB内存
- 至少30GB磁盘空间

## 2. 基础环境配置

### 2.1 安装NVIDIA驱动

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

### 2.2 安装CUDA和cuDNN

```bash
# 下载并安装CUDA 11.0
wget https://developer.download.nvidia.com/compute/cuda/11.0.3/local_installers/cuda_11.0.3_450.51.06_linux.run
sudo sh cuda_11.0.3_450.51.06_linux.run

# 配置环境变量
echo 'export PATH=/usr/local/cuda-11.0/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.0/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 下载并安装cuDNN 8.0
# 注：需要从NVIDIA开发者网站下载cuDNN v8.0，解压后：
sudo cp cuda/include/cudnn*.h /usr/local/cuda/include
sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
```

### 2.3 安装系统依赖

```bash
sudo apt-get update
sudo apt-get install -y \
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
    libeigen3-dev
```

### 2.4 配置Python环境

```bash
# 设置Python 3.6为默认版本
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --set python3 /usr/bin/python3.6

# 配置pip镜像源
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 升级pip
python3 -m pip install --upgrade pip
```

## 3. 安装PyTorch和依赖包

### 3.1 安装PyTorch

```bash
pip3 install torch==1.10.2+cu113 torchvision==0.11.3+cu113 -f https://download.pytorch.org/whl/torch_stable.html
```

### 3.2 安装项目依赖

创建requirements.txt并安装依赖：

```bash
pip3 install -r requirements.txt
```

requirements.txt内容：
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

## 4. 编译和安装特殊组件

### 4.1 编译apex

```bash
git clone https://github.com/NVIDIA/apex
cd apex
export TORCH_CUDA_ARCH_LIST="6.0;6.1;6.2;7.0;7.5"
python setup.py install -v
cd ..
```

### 4.2 安装和编译normalspeed

```bash
# 1. 准备OpenCV环境
pip uninstall opencv-python opencv-python-headless -y
pip install opencv-python==4.5.3.56

# 2. 克隆并安装normalspeed
git clone https://github.com/hfutcgncas/normalspeed.git
cd normalspeed/normalSpeed

# 安装编译依赖
sudo apt-get install python3-pybind11
pip3 install Cython==0.29.15

# 清理并重新安装
rm -rf build/ dist/ *.egg-info/
python3 setup.py install --user
cd ../..
```

## 5. 克隆和配置FFB6D

```bash
# 克隆代码
git clone https://github.com/ethnhe/FFB6D.git
cd FFB6D

# 创建必要的目录
mkdir -p datasets models train_log

# 配置环境变量
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## 6. 验证安装

```bash
# 验证CUDA支持
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# 验证apex安装
python3 -c "from apex import amp; print('APEX installed')"

# 验证normalspeed安装
python3 -c "import normalSpeed; print('normalspeed installed')"
```

## 7. 常见问题

### 7.1 网络问题

```bash
# 使用代理（如需要）
export http_proxy="http://proxy:port"
export https_proxy="http://proxy:port"

# 或使用国内镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 7.2 版本兼容性问题

- 确保NVIDIA驱动版本支持CUDA 11.0
- 确保Python包版本相互兼容
- 检查CUDA版本与PyTorch版本的匹配

### 7.3 编译错误

- 确保已安装所有必要的编译工具
- 检查CUDA路径配置是否正确
- 确认系统库版本是否满足要求

## 8. 训练

按照官方文档配置LineMOD数据集并开始训练。

## 参考资料

1. [FFB6D项目](https://github.com/ethnhe/FFB6D)
2. [CUDA安装指南](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html)
3. [PyTorch安装指南](https://pytorch.org/get-started/locally/)
4. [【论文笔记】FFB6D | 马浩飞丨博客](https://www.mahaofei.com/post/d027527.html)