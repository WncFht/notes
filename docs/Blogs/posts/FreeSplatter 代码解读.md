---
title: FreeSplatter 代码解读
tags:
  - 科研
  - 三维重建
  - 复现
categories: 
date: 2025-01-02T13:22:16+08:00
modify: 2025-01-02T13:22:16+08:00
dir: 
share: false
cdate: 2025-01-02
mdate: 2025-01-02
---

# FreeSplatter 代码解读

## 稀疏重建对象 views_to_3d

```python
def run_views_to_3d(
    self, 
    image_files,  # 输入的图像文件列表
    do_rembg=False,  # 是否移除图像背景
    gs_type='2DGS',  # 高斯渲染类型：2DGS 或 3DGS
    mesh_reduction=0.5,  # 网格简化比例
    cache_dir=None,  # 缓存目录
):
    torch.cuda.empty_cache()  # 清理显存，避免碎片化

    # 创建输出目录
    self.output_dir = os.path.join(cache_dir, f'output_{uuid.uuid4()}')
    os.makedirs(self.output_dir, exist_ok=True)

    # 图像预处理：加载和处理输入图像
    images, alphas = [], []  # 图像和 alpha 通道存储
    for image_file in image_files:
        if isinstance(image_file, tuple):  # 兼容传入元组的情况
            image_file = image_file[0]
        image = Image.open(image_file)  # 打开图像
        w, h = image.size  # 获取图像尺寸

        # 可选：移除背景
        image_rgba = self.run_segmentation(image)  # 背景移除
        if image.mode == 'RGBA':  # 如果已有 alpha 通道
            image, alpha = rgba_to_white_background(image_rgba)  # 转换为白背景
            image = v2.functional.center_crop(image, min(h, w))  # 居中裁剪
            alpha = v2.functional.center_crop(alpha, min(h, w))  # 裁剪 alpha 通道
        else:  # 如果没有 alpha 通道
            image_rgba = resize_foreground(image_rgba, 0.9)  # 缩放前景
            image, alpha = rgba_to_white_background(image_rgba)  # 转换为白背景
        
        # 调整分辨率至 512x512
        image = v2.functional.resize(image, 512, interpolation=3, antialias=True).clamp(0, 1)
        alpha = v2.functional.resize(alpha, 512, interpolation=0, antialias=True).clamp(0, 1)

        # 保存处理后的图像和 alpha 通道
        images.append(image)
        alphas.append(alpha)

    # 将图像和 alpha 通道堆叠为张量
    images = torch.stack(images, dim=0)
    alphas = torch.stack(alphas, dim=0)

    # 生成可视化拼接图像
    images_vis = v2.functional.to_pil_image(rearrange(images, 'n c h w -> c h (n w)'))

    # 调用核心重建函数
    legends = [f'V{i}' for i in range(1, 1 + len(images))]  # 为每个视角生成图例
    gs_vis_path, video_path, mesh_fine_path, fig = self.run_freesplatter_object(
        images, alphas, legends=legends, gs_type=gs_type, mesh_reduction=mesh_reduction
    )

    return images_vis, gs_vis_path, video_path, mesh_fine_path, fig


def run_freesplatter_object(
    self, 
    images,  # 输入图像张量
    alphas,  # 图像的 alpha 通道张量
    legends=None,  # 图像视角的图例
    gs_type='2DGS',  # 高斯渲染类型
    mesh_reduction=0.5,  # 网格简化比例
):
    torch.cuda.empty_cache()  # 再次清理显存
    device = self.device

    # 根据渲染类型选择模型
    freesplatter = self.freesplatter_2dgs if gs_type == '2DGS' else self.freesplatter

    # 将图像和 alpha 通道移动到 GPU
    images, alphas = images.to(device), alphas.to(device)
    
    # **步骤 1：生成高斯点云**
    t0 = time.time()
    with torch.inference_mode():
        gaussians = freesplatter.forward_gaussians(images.unsqueeze(0))  # 生成高斯点云
    t1 = time.time()

    # **步骤 2：估计相机参数并可视化**
    c2ws_pred, focals_pred = freesplatter.estimate_poses(
        images, gaussians, masks=alphas, use_first_focal=True, pnp_iter=10
    )  # 估计相机外参和焦距
    fig = self.visualize_cameras_object(images, c2ws_pred, focals_pred, legends=legends)  # 可视化相机位姿
    t2 = time.time()
    
    # **步骤 3：保存高斯点云**
    gs_vis_path = os.path.join(self.output_dir, 'gs_vis.ply')
    save_gaussian(gaussians, gs_vis_path, freesplatter, opacity_threshold=5e-3, pad_2dgs_scale=True)
    print(f'Save gaussian at {gs_vis_path}')

    torch.cuda.empty_cache()  # 再次清理显存

    # **步骤 4：生成环绕视角视频**
    with torch.inference_mode():
        c2ws_video = get_circular_cameras(N=120, elevation=0, radius=2.0, normalize=True).to(device)  # 环绕相机轨迹
        fx = fy = focals_pred.mean() / 512.0  # 计算归一化焦距
        cx = cy = torch.ones_like(fx) * 0.5  # 中心点归一化
        fxfycxcy_video = torch.tensor([fx, fy, cx, cy]).unsqueeze(0).repeat(c2ws_video.shape[0], 1).to(device)

        video_frames = freesplatter.forward_renderer(
            gaussians, c2ws_video.unsqueeze(0), fxfycxcy_video.unsqueeze(0)
        )['image'][0].clamp(0, 1)  # 渲染视频帧

    video_path = os.path.join(self.output_dir, 'gs.mp4')
    save_video(video_frames, video_path, fps=30)  # 保存视频
    print(f'Save video at {video_path}')
    t3 = time.time()

    torch.cuda.empty_cache()  # 再次清理显存

    # **步骤 5：TSDF 融合生成网格**
    with torch.inference_mode():
        c2ws_fusion = get_fibonacci_cameras(N=120, radius=2.0)  # TSDF 融合相机轨迹
        c2ws_fusion, _ = normalize_cameras(
            c2ws_fusion, camera_position=torch.tensor([0., -2., 0.]), camera_system='opencv'
        )  # 相机归一化
        c2ws_fusion = c2ws_fusion.to(device)
        c2ws_fusion_reference = torch.linalg.inv(c2ws_fusion[0:1]) @ c2ws_fusion
        fx = fy = focals_pred.mean() / 512.0
        cx = cy = torch.ones_like(fx) * 0.5
        fov = np.rad2deg(np.arctan(0.5 / fx.item())) * 2
        fxfycxcy_fusion = torch.tensor([fx, fy, cx, cy]).unsqueeze(0).repeat(c2ws_fusion.shape[0], 1).to(device)

        fusion_render_results = freesplatter.forward_renderer(
            gaussians, c2ws_fusion_reference.unsqueeze(0), fxfycxcy_fusion.unsqueeze(0)
        )
        images_fusion = fusion_render_results['image'][0].clamp(0, 1).permute(0, 2, 3, 1)
        alphas_fusion = fusion_render_results['alpha'][0].permute(0, 2, 3, 1)
        depths_fusion = fusion_render_results['depth'][0].permute(0, 2, 3, 1)

        # TSDF 融合处理
        fusion_images = (images_fusion.detach().cpu().numpy() * 255).clip(0, 255).astype(np.uint8)
        fusion_depths = depths_fusion.detach().cpu().numpy()
        fusion_alphas = alphas_fusion.detach().cpu().numpy()
        fusion_masks = (fusion_alphas > 1e-2).astype(np.uint8)
        fusion_depths = fusion_depths * fusion_masks - np.ones_like(fusion_depths) * (1 - fusion_masks)

        fusion_c2ws = c2ws_fusion.detach().cpu().numpy()

        # 生成网格文件
        mesh_path = os.path.join(self.output_dir, 'mesh.obj')
        rgbd_to_mesh(
            fusion_images, fusion_depths, fusion_c2ws, fov, mesh_path, cam_elev_thr=-90
        )  # TSDF 融合生成网格
        print(f'Save mesh at {mesh_path}')
        t4 = time.time()

    torch.cuda.empty_cache()  # 清理显存

    # **步骤 6：优化纹理**
    cam_pos = c2ws_fusion[:, :3, 3].cpu().numpy()  # 获取相机位置
    cam_inds = torch.from_numpy(fpsample.fps_sampling(cam_pos, 16).astype(int)).to(device=device)  # 采样关键帧相机

    # 优化网格纹理
    alphas_bake = alphas_fusion[cam_inds]
    images_bake = (images_fusion[cam_inds] - (1 - alphas_bake)) / alphas_bake.clamp(min=1e-6)

    fxfycxcy = fxfycxcy_fusion[cam_inds].clone()
    intrinsics = torch.eye(3).unsqueeze(0).repeat(len(cam_inds), 1, 1).to(fxfycxcy)
    intrinsics[:, 0, 0] = fxfycxcy[:, 0]
    intrinsics[:, 0, 2] = fxfycxcy[:, 2]
    intrinsics[:, 1, 1] = fxfycxcy[:, 1]
    intrinsics[:, 1, 2] = fxfycxcy[:, 3]

    out_mesh = trimesh.load(str(mesh_path), process=False)  # 加载网格
    out_mesh = optimize_mesh(
        out_mesh, 
        images_bake, 
        alphas_bake.squeeze(-1), 
        c2ws_fusion[cam_inds].inverse(), 
        intrinsics,
        simplify=mesh_reduction,
        verbose=False
    )  # 优化纹理
    mesh_fine_path = os.path.join(self.output_dir, 'mesh.glb')
    out_mesh.export(mesh_fine_path)  # 保存优化后的网格
    print(f"Save optimized mesh at {mesh_fine_path}")
    t5 = time.time()

    # 打印时间统计
    print(f'Generate Gaussians: {t1-t0:.2f} seconds.')
    print(f'Estimate poses: {t2-t1:.2f} seconds.')
    print(f'Generate video: {t3-t2:.2f} seconds.')
    print(f'Generate mesh: {t4-t3:.2f} seconds.')
    print(f'Optimize mesh: {t5-t4:.2f} seconds.')

    return gs_vis_path, video_path, mesh_fine_path, fig
```

- **图像加载与预处理**：
    - 移除背景、裁剪、缩放为统一尺寸。
    - 将输入图像转换为 PyTorch 张量。
- **生成高斯点云**：
    - 使用高斯分布描述输入的 3D 点。
- **估计相机参数**：
    - 通过高斯点云估计相机的位姿（外参）和焦距（内参）。
- **视频渲染**：
    - 在环绕相机轨迹中渲染视频。
- **TSDF 融合生成网格**：
    - 通过深度图和 RGB 图像生成 3D 网格。
- **优化纹理**：
    - 使用深度和 RGB 图像优化网格的纹理和细节。

## 剩下的一些

```python
def visualize_cameras_object(
    self, 
    images,  # 输入的图像
    c2ws,  # 相机位姿（世界坐标系到相机坐标系的变换矩阵）
    focal_length,  # 焦距
    legends=None,  # 每个视角的图例，默认无
):
    # **1. 处理图像**：调整图像大小，限制像素值在 [0, 1] 范围，然后转换为 NumPy 格式
    images = v2.functional.resize(images, 128, interpolation=3, antialias=True).clamp(0, 1)
    images = (images.permute(0, 2, 3, 1).detach().cpu().numpy() * 255).astype(np.uint8)

    # **2. 相机位姿转换**：将 c2ws（相机位姿）转换到世界坐标系下
    cam2world = create_camera_to_world(torch.tensor([0, -2, 0]), camera_system='opencv').to(c2ws)  # 创建从相机到世界的变换
    transform = cam2world @ torch.linalg.inv(c2ws[0:1])  # 计算第一个相机的参考变换
    c2ws = transform @ c2ws  # 更新所有相机的位姿
    c2ws = c2ws.detach().cpu().numpy()
    c2ws[:, :, 1:3] *= -1  # 从 OpenCV 到 OpenGL 坐标系的转换

    # **3. 计算相机视场角（FOV）**
    focal_length = focal_length.mean().detach().cpu().numpy()
    fov = np.rad2deg(np.arctan(256.0 / focal_length)) * 2

    # **4. 为每个视角指定颜色**
    colors = [cmap(i / len(images))[:3] for i in range(len(images))]

    # **5. 设置图例**：如果未提供，默认为空
    legends = [None] * len(images) if legends is None else legends

    # **6. 调用可视化工具 CameraVisualizer**
    viz = CameraVisualizer(c2ws, legends, colors, images=images)
    fig = viz.update_figure(
        3,  # 维度
        height=320,  # 图形高度
        line_width=5,  # 相机线宽
        base_radius=1,  # 基准相机位置半径
        zoom_scale=1,  # 缩放比例
        fov_deg=fov,  # 视场角
        show_grid=True,  # 是否显示网格
        show_ticklabels=True,  # 是否显示坐标轴刻度
        show_background=True,  # 是否显示背景
        y_up=False,  # Y 轴方向向下
    )
    return fig


def run_views_to_scene(
    self, 
    image1,  # 输入的第一个图像
    image2,  # 输入的第二个图像
    cache_dir=None,  # 输出缓存目录
):
    torch.cuda.empty_cache()  # 清理显存

    # **1. 创建输出目录**
    self.output_dir = os.path.join(cache_dir, f'output_{uuid.uuid4()}')
    os.makedirs(self.output_dir, exist_ok=True)

    # **2. 图像预处理**
    images = []
    for image in [image1, image2]:
        w, h = image.size  # 获取图像宽高
        image = torch.from_numpy(np.asarray(image) / 255.0).float()  # 转为 NumPy，再转为张量
        image = rearrange(image, 'h w c -> c h w')  # 调整维度为 (C, H, W)
        image = v2.functional.center_crop(image, min(h, w))  # 中心裁剪
        image = v2.functional.resize(image, 512, interpolation=3, antialias=True).clamp(0, 1)  # 调整大小并归一化
        images.append(image)  # 添加到列表

    # **3. 将图像堆叠成一个张量**
    images = torch.stack(images, dim=0)

    # **4. 生成拼接可视化图像**
    images_vis = v2.functional.to_pil_image(rearrange(images, 'n c h w -> c h (n w)'))

    # **5. 调用场景重建方法**
    legends = [f'V{i}' for i in range(1, 1+len(images))]  # 为视角生成图例
    gs_vis_path, video_path, fig = self.run_freesplatter_scene(images, legends=legends)

    return images_vis, gs_vis_path, video_path, fig


def run_freesplatter_scene(
    self, 
    images,  # 输入图像
    legends=None,  # 每个视角的图例
):
    torch.cuda.empty_cache()  # 清理显存

    freesplatter = self.freesplatter_scene  # 使用 FreeSplatter 场景模型

    device = self.device
    images = images.to(device)  # 将图像移动到 GPU

    # **1. 生成高斯点云**
    t0 = time.time()
    with torch.inference_mode():
        gaussians = freesplatter.forward_gaussians(images.unsqueeze(0))  # 调用高斯生成器
    t1 = time.time()

    # **2. 估计相机位姿**
    c2ws_pred, focals_pred = freesplatter.estimate_poses(images, gaussians, use_first_focal=True, pnp_iter=10)
    # **2.1 归一化相机基线**
    baseline_pred = (c2ws_pred[:, :3, 3] - c2ws_pred[:1, :3, 3]).norm() + 1e-2  # 计算相机基线
    scale_factor = 1.0 / baseline_pred  # 归一化比例
    c2ws_pred = c2ws_pred.clone()
    c2ws_pred[:, :3, 3] *= scale_factor  # 缩放相机位置

    # **3. 可视化相机**
    fig = self.visualize_cameras_scene(images, c2ws_pred, focals_pred, legends=legends)
    t2 = time.time()

    # **4. 保存高斯点云**
    gs_vis_path = os.path.join(self.output_dir, 'gs_vis.ply')
    save_gaussian(gaussians, gs_vis_path, freesplatter, opacity_threshold=5e-3)  # 保存点云
    print(f'Save gaussian at {gs_vis_path}')

    # **5. 渲染视频**
    with torch.inference_mode():
        c2ws_video = generate_interpolated_path(c2ws_pred.detach().cpu().numpy()[:, :3, :], n_interp=120)  # 生成插值路径
        c2ws_video = torch.cat([
            torch.from_numpy(c2ws_video), 
            torch.tensor([0, 0, 0, 1]).reshape(1, 1, 4).repeat(c2ws_video.shape[0], 1, 1)
        ], dim=1).to(gaussians)  # 将路径转换为齐次坐标
        fx = fy = focals_pred.mean() / 512.0  # 计算归一化焦距
        cx = cy = torch.ones_like(fx) * 0.5  # 归一化中心点
        fxfycxcy_video = torch.tensor([fx, fy, cx, cy]).unsqueeze(0).repeat(c2ws_video.shape[0], 1).to(device)

        video_frames = freesplatter.forward_renderer(
            gaussians,  # 高斯点云
            c2ws_video.unsqueeze(0),  # 相机轨迹
            fxfycxcy_video.unsqueeze(0),  # 相机参数
            rescale=scale_factor.reshape(1).to(gaussians)  # 缩放比例
        )['image'][0].clamp(0, 1)  # 渲染图像帧

    video_path = os.path.join(self.output_dir, 'gs.mp4')
    save_video(video_frames, video_path, fps=30)  # 保存视频
    print(f'Save video at {video_path}')
    t3 = time.time()

    # **6. 打印时间统计**
    print(f'Generate Gaussians: {t1-t0:.2f} seconds.')
    print(f'Estimate poses: {t2-t1:.2f} seconds.')
    print(f'Generate video: {t3-t2:.2f} seconds.')

    return gs_vis_path, video_path, fig


def visualize_cameras_scene(
    self, 
    images,  # 输入的图像
    c2ws,  # 相机位姿
    focal_length,  # 焦距
    legends=None,  # 每个视角的图例
):
    # **1. 处理图像**：调整分辨率，归一化，转换为 NumPy 格式
    images = v2.functional.resize(images, 128, interpolation=3, antialias=True).clamp(0, 1)
    images = (images.permute(0, 2, 3, 1).detach().cpu().numpy() * 255).astype(np.uint8)

    # **2. 转换相机位姿坐标系**
    c2ws = c2ws.detach().cpu().numpy()
    c2ws[:, :, 1:3] *= -1  # OpenCV 到 OpenGL 转换

    # **3. 计算视场角（FOV）**
    focal_length = focal_length.mean().detach().cpu().numpy()
    fov = np.rad2deg(np.arctan(256.0 / focal_length)) * 2

    # **4. 为每个视角分配颜色**
    colors = [cmap(i / len(images))[:3] for i in range(len(images))]

    # **5. 设置图例**
    legends = [None] * len(images) if legends is None else legends

    # **6. 可视化相机**
    viz = CameraVisualizer(c2ws, legends, colors, images=images)
    fig = viz.update_figure(
        2, 
        height=320,
        line_width=5,
        base_radius=1, 
        zoom_scale=1, 
        fov_deg=fov, 
        show_grid=True, 
        show_ticklabels=True, 
        show_background=True, 
        y_up=False,
    )
    return fig

```
