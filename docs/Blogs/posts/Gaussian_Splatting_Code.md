---
title: Gaussian Splatting 数据集
tags: 
categories: 
date: 2025-01-01T12:11:48+08:00
modify: 2025-01-01T12:11:48+08:00
dir: 
share: false
cdate: 2025-01-01
mdate: 2025-01-01
---

# Gaussian Splatting 数据集

主要有 colmap 和 blender 两种数据类型。

---

## **1. Colmap 数据集加载过程**

### **1.1 加载函数**

- 主函数为 `readColmapSceneInfo`，调用了一系列子函数以加载相机参数、点云和相关文件。
- 数据来源路径为 `sparse/` 文件夹，包含相机参数文件、点云文件等。

---

### **1.2 加载的主要步骤**

#### **步骤 1：加载相机外参**

代码如下：

```python
cameras_extrinsic_file = os.path.join(path, "sparse/0", "images.bin")
cam_extrinsics = read_extrinsics_binary(cameras_extrinsic_file)
````

- 如果 `images.bin` 文件不存在，则加载 `images.txt`：

    ```python
    cameras_extrinsic_file = os.path.join(path, "sparse/0", "images.txt")
    cam_extrinsics = read_extrinsics_text(cameras_extrinsic_file)
    ```

- 外参包括：
    - 相机旋转矩阵 (`R`)。
    - 平移向量 (`T`)。
    - 图像名称，用于匹配图像文件。

#### **步骤 2：加载相机内参**

代码如下：

```python
cameras_intrinsic_file = os.path.join(path, "sparse/0", "cameras.bin")
cam_intrinsics = read_intrinsics_binary(cameras_intrinsic_file)
```

- 如果 `cameras.bin` 文件不存在，则加载 `cameras.txt`：

    ```python
    cameras_intrinsic_file = os.path.join(path, "sparse/0", "cameras.txt")
    cam_intrinsics = read_intrinsics_text(cameras_intrinsic_file)
    ```

- 内参包括：
    - 焦距（`focal length`）。
    - 主点坐标（`principal point`）。
    - 图像分辨率（`width` 和 `height`）。

#### **步骤 3：加载点云**

代码如下：

```python
ply_path = os.path.join(path, "sparse/0/points3D.ply")
bin_path = os.path.join(path, "sparse/0/points3D.bin")
txt_path = os.path.join(path, "sparse/0/points3D.txt")

if not os.path.exists(ply_path):
    print("Converting point3d.bin to .ply, will happen only the first time you open the scene.")
    xyz, rgb, _ = read_points3D_binary(bin_path)
    storePly(ply_path, xyz, rgb)
pcd = fetchPly(ply_path)
```

- 点云文件的来源可以是：
    - `points3D.bin`
    - `points3D.txt`
    - `points3D.ply`（如果存在则直接加载，否则从 `bin` 或 `txt` 转换为 `.ply`）

#### **步骤 4：训练/测试集划分**

代码如下：

```python
if eval:
    cam_names = [cam_extrinsics[cam_id].name for cam_id in cam_extrinsics]
    cam_names = sorted(cam_names)
    test_cam_names_list = [name for idx, name in enumerate(cam_names) if idx % llffhold == 0]
else:
    test_cam_names_list = []
```

- 测试集可以通过 `eval` 参数启用。
- 默认每 8 个视角（`llffhold=8`）选取一个作为测试集。

#### **步骤 5：场景归一化**

代码如下：

```python
nerf_normalization = getNerfppNorm(train_cam_infos)
```

- 通过计算训练相机的中心和对角线长度，确定场景中心 (`translate`) 和半径 (`radius`)。

---

### **1.3 返回数据结构**

函数返回一个 `SceneInfo` 数据结构：

- `point_cloud`：点云数据。
- `train_cameras`：训练相机列表。
- `test_cameras`：测试相机列表。
- `nerf_normalization`：场景归一化参数。
- `ply_path`：点云文件路径。

---

## **2. Blender 数据集加载过程**

### **2.1 加载函数**

- 主函数为 `readNerfSyntheticInfo`，从 Blender 导出的 JSON 文件加载相机和图像信息。

---

### **2.2 加载的主要步骤**

#### **步骤 1：加载训练和测试相机**

代码如下：

```python
train_cam_infos = readCamerasFromTransforms(path, "transforms_train.json", depths_folder, white_background, False, extension)
test_cam_infos = readCamerasFromTransforms(path, "transforms_test.json", depths_folder, white_background, True, extension)
```

- 每个相机的数据来源于 `transforms_train.json` 和 `transforms_test.json`。
	- **`transforms_train.json`**:
		- 用于描述训练集中相机的位置信息（外参）、相机的内参（水平视角）以及对应的图像路径。
			- 每个相机视角都会有一条记录。
- 相机参数包含：
    - `transform_matrix`（相机到世界的变换矩阵）。
    - 水平视角 (`camera_angle_x`) 用于计算焦距。

#### **步骤 2：生成点云**

代码如下：

```python
if not os.path.exists(ply_path):
    num_pts = 100_000
    print(f"Generating random point cloud ({num_pts})...")
    xyz = np.random.random((num_pts, 3)) * 2.6 - 1.3
    shs = np.random.random((num_pts, 3)) / 255.0
    storePly(ply_path, xyz, SH2RGB(shs) * 255)
pcd = fetchPly(ply_path)
```

- Blender 数据集没有点云文件，因此随机生成 10 万个点：
    - 点的位置范围为 `[-1.3, 1.3]`。
    - 点的颜色通过球谐函数 (SH) 随机生成。

#### **步骤 3：场景归一化**

代码如下：

```python
nerf_normalization = getNerfppNorm(train_cam_infos)
```

- 与 Colmap 类似，计算场景的中心 (`translate`) 和半径 (`radius`)。

---

### **2.3 返回数据结构**

函数返回一个 `SceneInfo` 数据结构：

- `point_cloud`：生成的点云。
- `train_cameras`：训练相机列表。
- `test_cameras`：测试相机列表。
- `nerf_normalization`：场景归一化参数。
- `ply_path`：点云文件路径。

---

## **3. 总结对比**

|**特性**|**Colmap 数据集**|**Blender 数据集**|
|---|---|---|
|**相机参数**|从 `images.bin` 和 `cameras.bin` 中加载外参和内参|从 `transforms_train.json` 中加载变换矩阵|
|**点云**|从 `points3D.bin` 或 `points3D.txt` 加载|随机生成 10 万个点|
|**图像数据**|存储在 `images/` 文件夹|路径由 JSON 文件指定|
|**深度图**|可选，需 `depth_params.json` 定义|可选，需提供深度图文件夹|
|**归一化**|基于相机位置计算场景中心和半径|同上|
|**测试集划分**|每 8 个视角划分一个到测试集，或读取 `test.txt`|测试集通过 `transforms_test.json` 指定|
|**背景颜色**|无|可选白色或黑色背景|

---

## **4. 所需准备的文件**

### **Colmap 数据集**

1. 相机外参：`sparse/0/images.bin` 或 `images.txt`。
2. 相机内参：`sparse/0/cameras.bin` 或 `cameras.txt`。
3. 点云文件：`sparse/0/points3D.bin` 或 `points3D.txt`。
4. 图像文件夹：通常为 `images/`。
5. 可选文件：
    - `sparse/0/depth_params.json`（深度参数）。
    - `sparse/0/test.txt`（测试集划分文件）。

---

### **Blender 数据集**

1. 训练相机文件：`transforms_train.json`。
2. 测试相机文件：`transforms_test.json`。
3. 图像文件路径：由 JSON 文件指定。
4. 可选文件：
    - 深度图文件夹。
    - 背景颜色参数（`white_background`）。
