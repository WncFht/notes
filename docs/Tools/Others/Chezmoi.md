# 用 chezmoi 实现跨设备同步配置

本指南将帮助你使用 chezmoi 管理你的配置文件（dotfiles），并使用包管理器维护软件列表。

## 前期准备

### 1. 需要的工具

- Git
- GitHub 账号
- chezmoi
- 包管理器（Windows: Scoop, Ubuntu: apt/snap）

### 2. 重要的配置文件

**Windows 常用配置文件**:

```
%USERPROFILE%/
├── .gitconfig                        # Git配置
├── .ssh/                            # SSH配置
├── Documents/
│   └── PowerShell/
│       └── Microsoft.PowerShell_profile.ps1  # PowerShell配置
├── AppData/
│   ├── Roaming/
│   │   └── Code/
│   │       └── User/
│   │           └── settings.json    # VSCode配置
│   └── Local/
└── .config/
    └── scoop/
        └── config.json              # Scoop配置
```

**Ubuntu 常用配置文件**:

```
~/
├── .bashrc                          # Bash配置
├── .zshrc                           # Zsh配置
├── .gitconfig                       # Git配置
├── .ssh/                           # SSH配置
└── .config/
    ├── Code/
    │   └── User/
    │       └── settings.json       # VSCode配置
    └── tabby/
        └── config.yaml            # Tabby终端配置
```

## GitHub 设置

### 1. 创建 GitHub 仓库

1. 访问 GitHub 并登录
2. 点击 "New repository"
3. 仓库名称设置为 `dotfiles`
4. 设置为 Public（推荐）
5. 不要初始化 README（我们将从本地初始化）
6. 创建仓库

### 2. 配置 SSH 密钥（如果还没有）

```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥添加到GitHub
# 1. 复制公钥内容
cat ~/.ssh/id_ed25519.pub
# 2. 访问 GitHub → Settings → SSH and GPG keys → New SSH key
# 3. 粘贴公钥内容并保存
```

## Windows 配置

### 1. 安装必要工具

使用 PowerShell（以管理员身份运行）：

```powershell
# 安装Scoop
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# 安装Git（如果还没有）
scoop install git

# 安装chezmoi
scoop install chezmoi
```

### 2. 初始化 chezmoi

```powershell
# 初始化chezmoi并克隆你的仓库
chezmoi init --apply https://github.com/yourusername/dotfiles.git
# 用 ssh 也可以

# 查看chezmoi将进行的更改
chezmoi diff

# 将现有配置文件添加到chezmoi
chezmoi add $HOME/.gitconfig
chezmoi add $HOME/.ssh/config
chezmoi add $HOME/Documents/PowerShell/Microsoft.PowerShell_profile.ps1
chezmoi add $HOME/AppData/Roaming/Code/User/settings.json

# 提交并推送更改
chezmoi cd
git add .
git commit -m "Initial Windows config"
git push
```

### 3. 导出软件包列表

```powershell
# 导出Scoop包列表
scoop export > packages/scoop-packages.txt

# 提交包列表
chezmoi cd
git add packages/scoop-packages.txt
git commit -m "Add Windows package list"
git push
```

## Ubuntu 配置

### 1. 安装必要工具

```bash
# 安装Git（如果还没有）
sudo apt update
sudo apt install git

# 安装chezmoi
sh -c "$(curl -fsLS get.chezmoi.io)"
```

参考这个网站 [Install - chezmoi](https://www.chezmoi.io/install/) 进行下载，我命令行一直不成功，直接选择对应的包就行了。

```
sudo dpkg -i chezmoi_2.54.0_linux_amd64.deb
chezmoi --version
```

### 2. 初始化 chezmoi

```bash
# 初始化chezmoi并克隆你的仓库
chezmoi init --apply https://github.com/yourusername/dotfiles.git

# 查看chezmoi将进行的更改
chezmoi diff

# 将现有配置文件添加到chezmoi
chezmoi add ~/.bashrc
chezmoi add ~/.zshrc
chezmoi add ~/.gitconfig
chezmoi add ~/.ssh/config
chezmoi add ~/.config/Code/User/settings.json

# 提交并推送更改
chezmoi cd
git add .
git commit -m "Initial Ubuntu config"
git push
```

### 3. 导出软件包列表

```bash
chezmoi cd
mkdir packages
# 导出apt包列表
dpkg --get-selections | grep -v deinstall | awk '{print $1}' > packages/apt-packages.txt

# 导出snap包列表
snap list | awk '{if (NR>1) print $1}' > packages/snap-packages.txt

# 提交包列表
git add packages/apt-packages.txt packages/snap-packages.txt
git commit -m "Add Ubuntu package lists"
git push
```

## 日常使用

### 1. 更新配置

当你修改了配置文件后：

```bash
# 将更改添加到chezmoi
chezmoi add ~/.bashrc  # 或其他修改的配置文件

# 查看更改
chezmoi diff

# 提交并推送更改
chezmoi cd
git add .
git commit -m "Update bashrc"
git push
```

### 2. 在其他机器上同步

```bash
# 拉取并应用最新更改
chezmoi update
```

### 3. 更新软件包列表

Windows:

```powershell
# 更新Scoop包列表
scoop export > packages/scoop-packages.txt
```

Ubuntu:

```bash
# 更新apt包列表
dpkg --get-selections | grep -v deinstall | awk '{print $1}' > packages/apt-packages.txt

# 更新snap包列表
snap list | awk '{if (NR>1) print $1}' > packages/snap-packages.txt
```

### 4. 在新机器上设置

Windows:

```powershell
# 安装chezmoi
scoop install chezmoi

# 初始化并应用配置
chezmoi init https://github.com/yourusername/dotfiles.git
chezmoi apply
```

Ubuntu:

```bash
# 安装chezmoi
sh -c "$(curl -fsLS get.chezmoi.io)"

# 初始化并应用配置
chezmoi init https://github.com/yourusername/dotfiles.git
chezmoi apply
```

## 常见问题

### 1. 如何处理不同机器的特定配置？

使用模板和条件语句。在 `.chezmoi.toml.tmpl` 中：

```toml
{{- $osid := .chezmoi.os -}}
[data]
    name = "Your Name"
    email = "your@email.com"
    {{- if eq .chezmoi.os "windows" }}
    is_windows = true
    {{- else if eq .chezmoi.os "linux" }}
    is_linux = true
    {{- end }}
```

### 2. 如何处理敏感信息？

对于敏感信息，可以：

1. 使用模板和环境变量
2. 使用 chezmoi 的加密功能
3. 将敏感信息存储在单独的私有仓库中

### 3. 如何撤销更改？

```bash
# 查看将要进行的更改
chezmoi diff

# 如果不满意，可以撤销
chezmoi forget ~/.bashrc  # 移除文件的管理

# 或者重置为原始状态
chezmoi apply --force
```

### 4. 配置文件权限问题？

chezmoi 会自动处理文件权限。对于特殊权限需求，可以在源文件名中使用特殊前缀：

- `private_` : 创建私有文件 (chmod 600)
- `executable_` : 创建可执行文件 (chmod 700)
- `readonly_` : 创建只读文件 (chmod 400)

### 5. 如何查看管理的文件？

```bash
# 列出所有管理的文件
chezmoi managed

# 查看源文件
chezmoi cd
ls -la
```

### 6. 更新出错怎么办？

```bash
# 备份当前状态
chezmoi archive --output=backup.tar.gz

# 重置更改
chezmoi init --force

# 重新应用配置
chezmoi apply
```
