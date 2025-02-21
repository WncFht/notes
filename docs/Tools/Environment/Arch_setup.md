---
title: arch 配置
tags:
  - arch
  - Environment
categories: 
date: 2025-02-09T22:08:30+08:00
modify: 2025-02-09T22:08:30+08:00
dir: 
share: false
cdate: 2025-02-09
mdate: 2025-02-09
---

# Arch 配置

## preprocess

- 删除卷
- 高级启动 `F12`

## install

```shell
systemctl stop reflector.service
systemctl status reflector.service

ls /sys/firmware/efi/efivars

iwctl # 进入交互式命令行
device list # 列出无线网卡设备名，比如无线网卡看到叫 wlan0
station wlan0 scan # 扫描网络
station wlan0 get-networks # 列出所有 wifi 网络
station wlan0 connect wifi-name # 进行连接，注意这里无法输入中文。回车后输入密码即可
exit # 连接成功后退出

ping www.bilibili.com

timedatectl set-ntp true # 将系统时间与网络时间进行同步
timedatectl status # 检查服务状态
```

```shell
vim /etc/pacman.d/mirrorlist

Server = https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch # 中国科学技术大学开源镜像站
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch # 清华大学开源软件镜像站
Server = https://repo.huaweicloud.com/archlinux/$repo/os/$arch # 华为开源镜像站
Server = http://mirror.lzu.edu.cn/archlinux/$repo/os/$arch # 兰州大学开源镜像站
```

```shell
lsblk # 显示当前分区情况

# 分区+挂载 ext4 or btrfs
```

```shell
pacstrap /mnt base base-devel linux linux-firmware btrfs-progs
# 如果使用btrfs文件系统，额外安装一个btrfs-progs包
pacstrap /mnt networkmanager vim sudo zsh zsh-completions
```

```shell
genfstab -U /mnt > /mnt/etc/fstab
cat /mnt/etc/fstab
```

```shell
arch-chroot /mnt
```

```shell
vim /etc/hostname

vim /etc/hosts

127.0.0.1   localhost
::1         localhost
127.0.1.1   myarch.localdomain myarch

ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

vim /etc/locale.gen #编辑 `/etc/locale.gen`，去掉 `en_US.UTF-8 UTF-8` 以及 `zh_CN.UTF-8 UTF-8` 行前的注释符号

echo 'LANG=en_US.UTF-8'  > /etc/locale.conf

useradd -m -g users -G wheel lingxi

# %wheel ALL=(ALL:ALL) ALL

passwd root

cat /proc/cpuinfo | grep "model name"

pacman -S intel-ucode # Intel
pacman -S amd-ucode # AMD	

pacman -S networkmanager
systemctl enable NetworkManager.service

pacman -S grub efibootmgr os-prober

grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB --removable
# 说明：
# --target 指定目标平台为x86_64-efi
# --efi-directory 指定EFI分区的路径
# --bootloader-id 指定引导程序的ID
# --removable 选项表示安装到可移动设备上，可不选
```

编辑`/etc/default/grub`文件，将`"GRUB_TIMEOUT=5"`修改为`"GRUB_TIMEOUT=30"`；

将 `"GRUB_CMDLINE_LINUX_DEFAULT="` 后面的参数修改为 `"loglevel=5 nowatchdog"` 。当然你也可以修改为”loglevel=7”使用最高日志等级来装逼，这将会输出全部内核日志

```shell
grub-mkconfig -o /boot/grub/grub.cfg

```

```shell
vim /etc/pacman.conf

[multilib]

[archlinuxcn]
Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch # 中国科学技术大学开源镜像站
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch # 清华大学开源软件镜像站
Server = https://mirrors.hit.edu.cn/archlinuxcn/$arch # 哈尔滨工业大学开源镜像站
Server = https://repo.huaweicloud.com/archlinuxcn/$arch # 华为开源镜像站

pacman -Syyu

pacman -S plasma-meta konsole dolphin # plasma-meta 元软件包、konsole 终端模拟器和 dolphin 文件管理器

systemctl enable sddm
systemctl start sddm  # 直接启动显示管理器，与以下reboot命令二选一即可

sudo pacman -S sof-firmware alsa-firmware alsa-ucm-conf # 声音固件
sudo pacman -S ntfs-3g # 使系统可以识别 NTFS 格式的硬盘
sudo pacman -S adobe-source-han-serif-cn-fonts wqy-zenhei # 安装几个开源中文字体。一般装上文泉驿就能解决大多 wine 应用中文方块的问题
sudo pacman -S noto-fonts noto-fonts-cjk noto-fonts-emoji noto-fonts-extra # 安装谷歌开源字体及表情
sudo pacman -S firefox chromium # 安装常用的火狐、chromium 浏览器
sudo pacman -S ark # 压缩软件。在 dolphin 中可用右键解压压缩包
sudo pacman -S packagekit-qt6 packagekit appstream-qt appstream # 确保 Discover（软件中心）可用，需重启
sudo pacman -S gwenview # 图片查看器
sudo pacman -S steam # 游戏商店。稍后看完显卡驱动章节再使用
sudo pacman -S archlinuxcn-keyring # cn 源中的签名（archlinuxcn-keyring 在 archlinuxcn）
sudo pacman -S yay # yay 命令可以让用户安装 AUR 中的软件（yay 在 archlinuxcn）

sudo pacman -S fcitx5-im # 输入法基础包组
sudo pacman -S fcitx5-chinese-addons # 官方中文输入引擎
sudo pacman -S fcitx5-anthy # 日文输入引擎
sudo pacman -S fcitx5-pinyin-moegirl # 萌娘百科词库。二刺猿必备（archlinuxcn）
sudo pacman -S fcitx5-material-color # 输入法主题

vim ~/.config/environment.d/im.conf

# fix fcitx problem
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
SDL_IM_MODULE=fcitx
GLFW_IM_MODULE=ibus

sudo systemctl enable --now bluetooth

sudo pacman -S timeshift
sudo systemctl enable --now cronie.service
```
## zsh

```shell
sudo pacman -S zsh
sh -c "$(curl -fsSL https://gitee.com/shmhlsy/oh-my-zsh-install.sh/raw/master/install.sh)" # 会覆盖 ~/.zshrc
sudo chsh -s /usr/bin/zsh


git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting

git clone https://github.com/zsh-users/zsh-autosuggestions.git ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions

git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
```

```shell
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

sudo pacman -S zsh-completions docker man-db exa bat tealdeer proxychains htop

sudo pacman -S man-pages-zh_cn man-pages-zh_tw
```

```shell
sudo pacman -S thefuck git-delta fd ripgrep bottom dust zoxide procs sd gitui
curl
sudo pacman -S thefuck
sudo pacman -S git-delta
slides/slidev
sudo pacman -S fd
sudo pacman -S ripgrep
bat
exa
sudo pacman -S bottom
sudo pacman -S fud
sudo pacman -S dust
sudo pacman -S zoxide # do not use with z and autojump
sudo pacman -S procs
sudo pacman -S sd
yay -S joshuto
sudo pacman -S gitui
yay -S lazydocker
yay -S downgrade
```

```shell
email: mutt/neomutt
translator: pot
yay -S pot-translation
```

## 软件

```shell
yay -S linuxqq
yay -S wechat
yay -S telegram-desktop
yay -S visual-studio-code-bin
yay -S Okular
yay -S Gwenview
yay -S OBS
yay -S KDEConnect
yay -S Clash-verge-rev-bin
yay -S Kate
yay -S Filelight

yay -S plasma-applet-window-buttons
yay -S plasma6-applets-window-title
yay -S plasma6-applets-panel-colorizer
yay -S kwin-effect-rounded-corners-git
```

## GRUB 美化

```shell
git clone https://github.com/vinceliuice/grub2-themes.git

[bigSur](https://www.pling.com/p/1443844)
```

## 主题

- WhiteSur
- Kvantum -> KvMojave
