---
title: Gaussian Splatting 复现
tags:
  - 科研
  - 复现
  - 三维重建
categories: 
date: 2024-12-31T21:11:43+08:00
modify: 2024-12-31T21:11:43+08:00
dir: 
share: false
cdate: 2024-12-31
mdate: 2024-12-31
---

# Gaussian Splatting 复现

## 官方数据集复现

### prepare

```
git clone https://github.com/graphdeco-inria/gaussian-splatting --recursive
conda env create --file environment.yml
conda activate gaussian_splatting
```

- 去下载个数据集

### train

```
python train.py  -s ./data/tandt/train/ -m ./output/train/ --eval

Optimizing ./output/train/
Output folder: ./output/train/ [31/12 20:58:06]
Tensorboard not available: not logging progress [31/12 20:58:06]
------------LLFF HOLD------------- [31/12 20:58:08]
Reading camera 301/301 [31/12 20:58:08]
Converting point3d.bin to .ply, will happen only the first time you open the scene. [31/12 20:58:08]
Loading Training Cameras [31/12 20:58:09]
Loading Test Cameras [31/12 20:58:19]
Number of points at initialisation :  182686 [31/12 20:58:20]
Training progress:  23%|███████▉                          | 7000/30000 [02:04<07:36, 50.34it/s, Loss=0.0985708, Depth Loss=0.0000000]
[ITER 7000] Evaluating test: L1 0.07567951896865116 PSNR 19.8115311672813 [31/12 21:00:25]

[ITER 7000] Evaluating train: L1 0.05251172706484795 PSNR 21.924707794189455 [31/12 21:00:25]

[ITER 7000] Saving Gaussians [31/12 21:00:25]
Training progress: 100%|█████████████████████████████████| 30000/30000 [10:58<00:00, 45.54it/s, Loss=0.0425664, Depth Loss=0.0000000]

[ITER 30000] Evaluating test: L1 0.05784237639684426 PSNR 22.03640069459614 [31/12 21:09:19]

[ITER 30000] Evaluating train: L1 0.025540136173367502 PSNR 27.51155662536621 [31/12 21:09:19]

[ITER 30000] Saving Gaussians [31/12 21:09:19]

Training complete. [31/12 21:09:28]
```

### render

```
python render.py -m ./output/train/

Looking for config file in ./output/train/cfg_args
Config file found: ./output/train/cfg_args
Rendering ./output/train/
Loading trained model at iteration 30000 [31/12 21:14:40]
------------LLFF HOLD------------- [31/12 21:14:41]
Reading camera 301/301 [31/12 21:14:41]
Loading Training Cameras [31/12 21:14:41]
Loading Test Cameras [31/12 21:14:53]
Rendering progress: 100%|██████████████████████████████████████████████████████████████████████████| 263/263 [01:41<00:00,  2.58it/s]
Rendering progress: 100%|████████████████████████████████████████████████████████████████████████████| 38/38 [00:15<00:00,  2.42it/s]
```

### evaluate

```
python metrics.py -m ./output/train/

Scene: ./output/train/
Method: ours_30000
Metric evaluation progress:   0%|                                                                             | 0/38 [00:00<?, ?it/s]Downloading: "https://download.pytorch.org/models/vgg16-397923af.pth" to /home/fanghaotian/.cache/torch/hub/checkpoints/vgg16-397923af.pth
100%|█████████████████████████████████████████████████████████████████████████████████████████████| 528M/528M [00:28<00:00, 19.4MB/s]
Downloading: "https://raw.githubusercontent.com/richzhang/PerceptualSimilarity/master/lpips/weights/v0.1/vgg.pth" to /home/fanghaotian/.cache/torch/hub/checkpoints/vgg.pth
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7.12k/7.12k [00:03<00:00, 2.29kB/s]
Metric evaluation progress: 100%|████████████████████████████████████████████████████████████████████| 38/38 [07:57<00:00, 12.58s/it] 7.12k/7.12k [00:03<00:00, 2.29kB/s]
  SSIM :    0.8192384
  PSNR :   22.0094910
  LPIPS:    0.1966141
```

> 看起来比论文里的数据低。

- `.\SIBR_remoteGaussian_app.exe` 远程不能用， issue 中也未解决

### Interactive Viewers

```
scp -r -P 26000 fanghaotian@RHOS:/home/fanghaotian/3DGS/gaussian-splatting/output/ C:\Users\fanghaotian\Desktop\

./SIBR_gaussianViewer_app -m C:\Users\fanghaotian\Desktop\data\82ea91ef-6\
```

![image.png](https://raw.githubusercontent.com/WncFht/picture/main/20241231225623884.png)

## 用 blender 数据集

### prepare

- 数据集
	- [GitHub - bmild/nerf: Code release for NeRF (Neural Radiance Fields)](https://github.com/bmild/nerf)
	- `nerf_synthetic/lego ` 那个是 blender 的格式

```
tree -I "*.png"
.
└── lego
    ├── test
    ├── train
    ├── transforms_test.json
    ├── transforms_train.json
    ├── transforms_val.json
    └── val
```

### Iterations=30000 no evaluation

#### train

```
python train.py  -s ./data/nerf_synthetic/lego/ -m ./output/lego/

Optimizing ./output/lego/
Output folder: ./output/lego/ [01/01 13:31:23]
Tensorboard not available: not logging progress [01/01 13:31:23]
Found transforms_train.json file, assuming Blender data set! [01/01 13:31:23]
Reading Training Transforms [01/01 13:31:23]
Reading Test Transforms [01/01 13:31:31]
Generating random point cloud (100000)... [01/01 13:31:38]
Loading Training Cameras [01/01 13:31:39]
Loading Test Cameras [01/01 13:31:53]
Number of points at initialisation :  100000 [01/01 13:31:53]
Training progress:  23%|████████████████████                                                                  | 7000/30000 [01:15<04:12, 91.02it/s, Loss=0.0152277, Depth Loss=0.0000000]
[ITER 7000] Evaluating train: L1 0.3646775007247925 PSNR 5.983335494995117 [01/01 13:33:09]

[ITER 7000] Saving Gaussians [01/01 13:33:09]
Training progress: 100%|█████████████████████████████████████████████████████████████████████████████████████| 30000/30000 [05:26<00:00, 91.97it/s, Loss=0.0105094, Depth Loss=0.0000000]

[ITER 30000] Evaluating train: L1 0.6417351365089417 PSNR 2.185275435447693 [01/01 13:37:19]

[ITER 30000] Saving Gaussians [01/01 13:37:19]

Training complete. [01/01 13:37:21]
```

#### render

```
python render.py -m ./output/lego/

Looking for config file in ./output/lego/cfg_args
Config file found: ./output/lego/cfg_args
Rendering ./output/lego/
Loading trained model at iteration 30000 [01/01 13:41:14]
Found transforms_train.json file, assuming Blender data set! [01/01 13:41:14]
Reading Training Transforms [01/01 13:41:14]
Reading Test Transforms [01/01 13:41:20]
Loading Training Cameras [01/01 13:41:28]
Loading Test Cameras [01/01 13:41:44]
Rendering progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 300/300 [01:06<00:00,  4.48it/s]
Rendering progress: 0it [00:00, ?it/s]
```

#### metric

```
python metrics.py -m ./output/lego/

Scene: ./output/lego/
Method: ours_30000
Metric evaluation progress: 0it [00:00, ?it/s]
  SSIM :          nan
  PSNR :          nan
  LPIPS:          nan
```

#### Interactive Viewers

```
scp -r -P 26000 fanghaotian@RHOS:/home/fanghaotian/3DGS/gaussian-splatting/output/lego C:\Users\fanghaotian\Desktop\

./SIBR_gaussianViewer_app -m C:\Users\fanghaotian\Desktop\lego
```

![image.png](https://raw.githubusercontent.com/WncFht/picture/main/20250101142557441.png)

🤔，好像一定要 --eval。

### Iteratations=30000 + evaluation

那么加上以后用 iterations=300000（default）再跑一次。

```
python train.py  -s ./data/nerf_synthetic/lego/ -m ./output/lego_eval/ --eval

Optimizing ./output/lego_eval/
Output folder: ./output/lego_eval/ [01/01 13:43:45]
Tensorboard not available: not logging progress [01/01 13:43:45]
Found transforms_train.json file, assuming Blender data set! [01/01 13:43:45]
Reading Training Transforms [01/01 13:43:45]
Reading Test Transforms [01/01 13:43:51]
Loading Training Cameras [01/01 13:43:58]
Loading Test Cameras [01/01 13:44:06]
Number of points at initialisation :  100000 [01/01 13:44:12]
Training progress:  23%|████████████████████                                                                  | 7000/30000 [01:24<04:48, 79.82it/s, Loss=0.0153927, Depth Loss=0.0000000]
[ITER 7000] Evaluating test: L1 0.34677238538861277 PSNR 6.254974584579468 [01/01 13:45:38]

[ITER 7000] Evaluating train: L1 0.3650033831596375 PSNR 5.939675426483155 [01/01 13:45:38]

[ITER 7000] Saving Gaussians [01/01 13:45:38]
Training progress: 100%|█████████████████████████████████████████████████████████████████████████████████████| 30000/30000 [05:47<00:00, 86.33it/s, Loss=0.0095609, Depth Loss=0.0000000]

[ITER 30000] Evaluating test: L1 0.557637879550457 PSNR 3.0822176444530487 [01/01 13:50:00]

[ITER 30000] Evaluating train: L1 0.5475435316562652 PSNR 3.064222288131714 [01/01 13:50:00]

[ITER 30000] Saving Gaussians [01/01 13:50:00]

Training complete. [01/01 13:50:04]


python render.py -m ./output/lego_eval/

Looking for config file in ./output/lego_eval/cfg_args
Config file found: ./output/lego_eval/cfg_args
Rendering ./output/lego_eval/
Loading trained model at iteration 30000 [01/01 13:51:20]
Found transforms_train.json file, assuming Blender data set! [01/01 13:51:20]
Reading Training Transforms [01/01 13:51:20]
Reading Test Transforms [01/01 13:51:26]
Loading Training Cameras [01/01 13:51:33]
Loading Test Cameras [01/01 13:51:40]
Rendering progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:25<00:00,  3.94it/s]
Rendering progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [00:48<00:00,  4.13it/s]


python metrics.py -m ./output/lego_eval/

Scene: ./output/lego_eval/
Method: ours_30000
Metric evaluation progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [04:00<00:00,  1.20s/it]
  SSIM :    0.2604475
  PSNR :    3.0649595
  LPIPS:    0.5116847
```

看起来效果不太好。
应该是初始化的问题，L1 甚至还是上次的 10 倍, `Evaluating train: L1 0.5475435316562652 PSNR 3.064222288131714 ` 。

把 iterations 调到 100000 再来一次，看看收敛情况。

### Iterations=100000 + evaluation

```
 python train.py  -s ./data/nerf_synthetic/lego/ -m ./output/lego_eval_100000/ --iterations 100000 --eval
 
Optimizing ./output/lego_eval_100000/
Output folder: ./output/lego_eval_100000/ [01/01 14:00:46]
Tensorboard not available: not logging progress [01/01 14:00:46]
Found transforms_train.json file, assuming Blender data set! [01/01 14:00:46]
Reading Training Transforms [01/01 14:00:46]
Reading Test Transforms [01/01 14:00:53]
Loading Training Cameras [01/01 14:01:00]
Loading Test Cameras [01/01 14:01:08]
Number of points at initialisation :  100000 [01/01 14:01:15]
Training progress:   7%|█████▉                                                                               | 7000/100000 [01:23<17:42, 87.50it/s, Loss=0.0159089, Depth Loss=0.0000000]
[ITER 7000] Evaluating test: L1 0.34856061153113843 PSNR 6.298382818698883 [01/01 14:02:40]

[ITER 7000] Evaluating train: L1 0.36839944720268253 PSNR 5.857858657836914 [01/01 14:02:40]

[ITER 7000] Saving Gaussians [01/01 14:02:40]
Training progress:  30%|████████████████████████▉                                                          | 29990/100000 [05:45<10:51, 107.52it/s, Loss=0.0095307, Depth Loss=0.0000000]
[ITER 30000] Evaluating test: L1 0.6024469056725502 PSNR 2.6481225460767748 [01/01 14:07:02]

[ITER 30000] Evaluating train: L1 0.5561836898326874 PSNR 2.9405082702636722 [01/01 14:07:02]

[ITER 30000] Saving Gaussians [01/01 14:07:02]
Training progress: 100%|██████████████████████████████████████████████████████████████████████████████████| 100000/100000 [16:33<00:00, 100.62it/s, Loss=0.0109117, Depth Loss=0.0000000]

[ITER 100000] Saving Gaussians [01/01 14:17:49]

Training complete. [01/01 14:17:51]
```

```
python render.py -m ./output/lego_eval_100000/
Looking for config file in ./output/lego_eval_100000/cfg_args
Config file found: ./output/lego_eval_100000/cfg_args
Rendering ./output/lego_eval_100000/
Loading trained model at iteration 100000 [01/01 14:21:43]
Found transforms_train.json file, assuming Blender data set! [01/01 14:21:43]
Reading Training Transforms [01/01 14:21:43]
Reading Test Transforms [01/01 14:21:50]
Loading Training Cameras [01/01 14:21:57]
Loading Test Cameras [01/01 14:22:06]
Rendering progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:22<00:00,  4.39it/s]
Rendering progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [00:42<00:00,  4.65it/s]
```

```
python metrics.py -m ./output/lego_eval_100000/

Scene: ./output/lego_eval_100000/
Method: ours_100000
Metric evaluation progress: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 200/200 [04:03<00:00,  1.22s/it]
  SSIM :    0.2404845
  PSNR :    2.4990394
  LPIPS:    0.5251624
```

好像评估仍然不太行，还越训练越差了。

```
scp -r -P 26000 fanghaotian@RHOS:/home/fanghaotian/3DGS/gaussian-splatting/output/lego_eval_100000/ C:\Users\fanghaotian\Desktop\
```

![image.png](https://raw.githubusercontent.com/WncFht/picture/main/20250101142324995.png)

### Blender 转 Colmap

- [Frequently Asked Questions — COLMAP 3.12.0.dev0 documentation](https://colmap.github.io/faq.html#reconstruct-sparse-dense-model-from-known-camera-poses)

```
colmap automatic_reconstructor --workspace_path . --image_path ./images --sparse 1 --camera_model SIMPLE_PINHOLE --dense 0
# colmap automatic_reconstructor: 这是调用COLMAP程序中的自动重建模块，它会自动完成特征提取、匹配、重投影误差优化和三角化等步骤，以生成场景的稀疏3D点云模型。
# --workspace_path .: 指定了工作空间路径为当前目录(.)，在这个路径下，COLMAP将存储中间结果以及最终的重建输出文件。
# --image_path ./images: 定义了图像数据集所在的路径，即所有参与重建的图片都位于./images目录下。
# --sparse 1: 这个参数表示进行稀疏重建（与密集重建相对），即只构建出场景中的关键点及其对应关系，并通过这些信息生成一个由稀疏点云组成的三维模型。
# --camera_model SIMPLE_PINHOLE: 指定使用的相机模型为“简单针孔模型”（Simple Pinhole Model）。这意味着COLMAP在进行重建时将假设相机遵循的是最基础的几何投影模型，其中不包括像径向畸变这样的复杂因素。
# --dense 0，减少不需要的计算操作。
```

![image.png](https://raw.githubusercontent.com/WncFht/picture/main/20250101153810194.png)
然后 train render metric

```
(gaussian_splatting) fanghaotian@rhos-Super-Server:~/3DGS/gaussian-splatting$ python metrics.py -m ./output/lego_colmap/

Scene: ./output/lego_colmap/
Method: ours_30000
Metric evaluation progress: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:23<00:00,  1.83s/it]
  SSIM :    0.2915006
  PSNR :    4.3199711
  LPIPS:    0.4333871
```

感觉是转换的时候图片太少了，然后就变差了。render 的时候很快。

### ffmpeg 的问题

[ffmpeg: error while loading shared libraries: libopenh264.so.5:-CSDN博客](https://blog.csdn.net/weixin_43546619/article/details/124219304)

## 代码解读

[[Gaussian_Splatting_Code]]

## Reference

- [Site Unreachable](https://zhuanlan.zhihu.com/p/685698909)
- [用3D高斯泼溅(3DGS)重建自己的数据\_3d高斯泼溅文物数字化重建-CSDN博客](https://blog.csdn.net/leviopku/article/details/136480697)
- [3D Gaussian Spaltting代码复现全流程与代码结构解读\_3d gaussian splatting复现-CSDN博客](https://blog.csdn.net/weixin_71780622/article/details/135484407)
- [3D Gaussian Splatting复现-CSDN博客](https://blog.csdn.net/Sakuya__/article/details/135376331)
- [Windows下3D Gaussian Splatting从0开始安装配置环境及训练教程\_3d gaussian splatting安装教程-CSDN博客](https://blog.csdn.net/weixin_64588173/article/details/138140240)
- [3D Gaussian Splatting主程序代码解读\_3d gaussian splatting核心代码-CSDN博客](https://blog.csdn.net/xiner0114/article/details/143283944)
