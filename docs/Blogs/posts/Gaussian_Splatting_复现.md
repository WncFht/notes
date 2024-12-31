---
title: Gaussian_Splatting_复现
tags:
  - 科研 - 复现
categories: 
date: 2024-12-31T21:11:43+08:00
modify: 2024-12-31T21:11:43+08:00
dir: 
share: false
cdate: 2024-12-31
mdate: 2024-12-31
---

# Gaussian_Splatting_复现

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
scp -r -P 26000 fanghaotian@RHOS:/home/fanghaotian/3DGS/gaussian-splatting/output C:\Users\fanghaotian\Desktop\

./SIBR_gaussianViewer_app -m C:\Users\fanghaotian\Desktop\data\82ea91ef-6\
```

## 自己的数据集

TODO

### ffmpeg 的问题

[ffmpeg: error while loading shared libraries: libopenh264.so.5:-CSDN博客](https://blog.csdn.net/weixin_43546619/article/details/124219304)

## Reference

- [Site Unreachable](https://zhuanlan.zhihu.com/p/685698909)
- [用3D高斯泼溅(3DGS)重建自己的数据\_3d高斯泼溅文物数字化重建-CSDN博客](https://blog.csdn.net/leviopku/article/details/136480697)
- [3D Gaussian Spaltting代码复现全流程与代码结构解读\_3d gaussian splatting复现-CSDN博客](https://blog.csdn.net/weixin_71780622/article/details/135484407)
- [3D Gaussian Splatting复现-CSDN博客](https://blog.csdn.net/Sakuya__/article/details/135376331)
- [Windows下3D Gaussian Splatting从0开始安装配置环境及训练教程\_3d gaussian splatting安装教程-CSDN博客](https://blog.csdn.net/weixin_64588173/article/details/138140240)
- [3D Gaussian Splatting主程序代码解读\_3d gaussian splatting核心代码-CSDN博客](https://blog.csdn.net/xiner0114/article/details/143283944)
