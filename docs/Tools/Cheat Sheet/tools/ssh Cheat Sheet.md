---
title: SSH配置指南
tags:
  - Tools
  - CheatSheet
categories: graph
date: 2024-10-12T13:01:56+0800
modify: 2024-12-06T00:13:54+0800
dir: Obsidian
share: false
---

# SSH配置指南

## 一、SSH基础概念

### 1. SSH工作原理

SSH(Secure Shell)是一种加密的网络协议，通过在不安全的网络上为网络服务提供安全的传输环境。SSH通过使用加密技术，能够有效防止中间人攻击，保护数据传输的安全。

SSH工作流程：

1. **TCP连接建立**：客户端和服务器建立TCP连接（默认端口22）
2. **版本协商**：双方交换版本信息，确定使用的SSH协议版本
3. **密钥交换**：使用Diffie-Hellman算法交换会话密钥
4. **认证**：使用公钥或密码进行身份验证
5. **会话**：建立加密通信通道

### 2. 认证方式详解

#### 2.1 密码认证

- 最简单但最不安全的认证方式
- 容易受到暴力破解攻击
- 不推荐在生产环境中使用

#### 2.2 公钥认证

认证流程

1. 客户端发送公钥信息给服务器
2. 服务器检查authorized_keys文件
3. 服务器生成随机字符串，用公钥加密后发送给客户端
4. 客户端用私钥解密，将结果返回服务器
5. 服务器验证结果，完成认证

### 3. 安全建议

#### 3.1 基本安全设置

```bash
# /etc/ssh/sshd_config 安全配置
PermitRootLogin no                 # 禁止root直接登录
PasswordAuthentication no          # 禁用密码认证
PubkeyAuthentication yes          # 启用公钥认证
PermitEmptyPasswords no           # 禁止空密码
Protocol 2                        # 只使用SSH2协议
MaxAuthTries 3                    # 最大认证尝试次数
LoginGraceTime 30                 # 登录超时时间
X11Forwarding no                  # 禁用X11转发（除非需要）
AllowUsers user1 user2            # 限制允许登录的用户
```

#### 3.2 密钥管理

```bash
# 生成强密钥
ssh-keygen -t ed25519 -C "your_email@example.com" -a 100

# 密钥权限设置
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/known_hosts
```

### 常用的 SSH 命令

 [SSH 教程 菜鸟教程](https://www.cainiaojc.com/ssh/ssh-index.html)

## 二、完整配置指南

### 1. Linux服务器配置

```bash
# 1. 安装SSH服务器
sudo apt update
sudo apt install openssh-server

# 2. 配置SSH服务
sudo nano /etc/ssh/sshd_config

# 3. 基本安全配置
Port 22                          # 可以修改为非标准端口
ListenAddress 0.0.0.0            # 监听地址
Protocol 2
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
UsePAM yes
X11Forwarding no
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server

# 4. 重启SSH服务
sudo systemctl restart sshd

# 5. 检查服务状态
sudo systemctl status sshd
```

### 2. Windows SSH配置

#### 2.1 安装OpenSSH

```powershell
# 使用PowerShell安装OpenSSH
# 检查OpenSSH状态
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'

# 安装客户端和服务器
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# 启动SSH服务
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

如果有网络问题可以**下载并安装 OpenSSH 的离线安装包**：

- 您可以尝试从 GitHub 上下载 OpenSSH 的离线安装包，并按照以下步骤进行安装：
	1. 访问 GitHub 上的 Win32-OpenSSH 发布页面：[Win32-OpenSSH Releases](https://github.com/PowerShell/Win32-OpenSSH/releases)
	2. 下载适用于您的系统的安装包（Win32 或 Win64）。
	3. 解压下载的文件到一个目录。
	4. 以管理员权限打开命令提示符（cmd），并导航到解压的目录。
	5. 运行 `powershell.exe -ExecutionPolicy Bypass -File install-sshd.ps1` 来安装 OpenSSH 服务。
![image.png](https://raw.githubusercontent.com/WncFht/picture/main/picture/20241118020842.png)

#### 2.2 配置Windows SSH服务

```powershell
# 编辑SSH配置文件
notepad "$env:ProgramData\ssh\sshd_config"

# 基本配置内容与Linux类似，但路径需要调整
PubkeyAuthentication yes
PasswordAuthentication no
Subsystem sftp sftp-server.exe
```

### 3. SSH客户端配置

#### 3.1 创建SSH配置文件

```bash
# ~/.ssh/config
# 全局设置
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    HashKnownHosts yes
    GSSAPIAuthentication no
    
# GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/github_ed25519
    AddKeysToAgent yes
    
# 开发服务器
Host dev
    HostName dev.example.com
    User developer
    Port 22
    IdentityFile ~/.ssh/dev_ed25519
    ForwardAgent yes
    
# 生产服务器
Host prod
    HostName prod.example.com
    User deployer
    Port 22
    IdentityFile ~/.ssh/prod_ed25519
    ForwardAgent no
```

## 三、具体实践，用笔记本连台式机

### 台式电脑（服务端）配置：

1. **安装并启动SSH服务**:

```bash
# Ubuntu/Debian系统
sudo apt install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh

# 检查SSH服务状态
sudo systemctl status ssh
```

2. **配置SSH服务**:

```bash
# 编辑SSH服务器配置
sudo nano /etc/ssh/sshd_config

# 添加或修改以下配置
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers your_username    # 替换为您的用户名
```

3. **设置固定IP或动态DNS**:

```bash
# 查看当前IP
ip addr show

# 如果是动态IP，建议设置静态IP或使用动态DNS服务
```

### 笔记本（客户端）配置：

1. **生成SSH密钥对**（如果还没有）:

```bash
ssh-keygen -t ed25519 -C "your_laptop"
```

2. **将公钥复制到台式机**:

```bash
# 方法1：使用ssh-copy-id
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@desktop_ip

# 方法2：手动复制
cat ~/.ssh/id_ed25519.pub | ssh username@desktop_ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

3. **配置SSH客户端**:

```bash
# 编辑 ~/.ssh/config
nano ~/.ssh/config

# 添加以下配置
Host desktop
    HostName 192.168.1.xxx  # 替换为台式机的IP
    User your_username      # 替换为您的用户名
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ForwardX11 yes         # 如果需要图形界面转发
    ForwardAgent yes
    Compression yes
    ServerAliveInterval 60
```

### 常用连接命令：

1. **基本连接**:

```bash
# 从笔记本连接到台式机
ssh desktop

# 使用图形界面转发
ssh -X desktop
```

2. **文件传输**:

```bash
# 从笔记本复制文件到台式机
scp /path/to/local/file desktop:/path/to/remote/

# 从台式机复制文件到笔记本
scp desktop:/path/to/remote/file /path/to/local/
```

3. **端口转发**:

```bash
# 本地端口转发
ssh -L 8080:localhost:80 desktop

# 远程端口转发
ssh -R 8080:localhost:80 desktop
```

## 四、高级操作

### 1. SSH端口转发

#### 1.1 本地端口转发

```bash
# 将本地8080端口转发到远程80端口
ssh -L 8080:localhost:80 user@remote

# 使用配置文件设置
Host tunnel
    HostName remote.example.com
    LocalForward 8080 localhost:80
```

#### 1.2 远程端口转发

```bash
# 将远程3000端口转发到本地3000端口
ssh -R 3000:localhost:3000 user@remote

# 配置文件设置
Host remote-tunnel
    HostName remote.example.com
    RemoteForward 3000 localhost:3000
```

### 2. SSH代理转发

```bash
# 启用代理转发
ssh -A user@remote

# 配置文件设置
Host *
    ForwardAgent yes
    AddKeysToAgent yes
```

### 3. 跳板机配置

```bash
# 通过跳板机连接
ssh -J jumphost user@target

# 配置文件设置
Host target
    HostName target.example.com
    ProxyJump jumphost
```

## 五、故障排查

### 1. 最佳实践

```bash
# 1. 使用SSH配置文件管理连接
# 2. 为不同用途使用不同的密钥
# 3. 定期轮换密钥
# 4. 使用ssh-agent管理密钥
# 5. 备份SSH配置和密钥
```

### 2. 常见问题解决

```bash
# 连接被拒绝
ssh -v user@host  # 查看详细连接信息

# 权限问题
ls -la ~/.ssh     # 检查权限
chmod 600 ~/.ssh/id_ed25519

# 密钥问题
ssh-add -l        # 查看已加载的密钥
ssh-add ~/.ssh/id_ed25519  # 添加密钥到agent
```

### 3. 日志查看

```bash
# 服务器端
sudo tail -f /var/log/auth.log    # Debian/Ubuntu
sudo tail -f /var/log/secure      # CentOS/RHEL

# 客户端调试
ssh -vvv user@host  # 最详细的调试信息
```
