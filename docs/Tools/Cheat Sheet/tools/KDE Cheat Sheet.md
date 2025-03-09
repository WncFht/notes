---
title: KDE
tags:
  - CheatSheet
categories: 
date: 2025-01-28T22:58:21+08:00
modify: 2025-01-28T22:58:21+08:00
dir: 
share: false
cdate: 2025-01-28
mdate: 2025-01-28
---

# KDE

## Reference

- [KDE终极美化指南 \| Jiekang Hu's Blog](https://hujiekang.top/posts/kde-customization/)
- [KDE桌面美化指南 Part 1 \| Yaojie's Site](https://acherstyx.github.io/post/KDE%E6%A1%8C%E9%9D%A2%E7%BE%8E%E5%8C%96%E6%8C%87%E5%8D%97/)
- [欢迎 - Linux 银河漫游指南](https://libhitchhiker.eu.org/)

```zsh
sudo apt purge gnome gnome-shell
```

记录一下配置了一些什么：
- KDE 美化：主要是用了 McMojave 这个主题，然后用了 Kvantum manager
	- 没有使用 `Latte Dock` 和过多的插件
- 终端：
	- 用 KDE 自带的 konsole 和自己配置的 zsh。经典配置： `oh-my-zsh ` + ` powerlevel10k ` 和一些其他的插件。
- 浏览器用 edge + 登陆同步
- vscode + 登陆同步
- 下载字体主要是 `JetBrains Mono` 和 `LXGW Mono`
- 笔记软件是 Obsidian + GitHub 同步
	- 顺便配置了 Ubuntu 下的图床，仍旧是 PicGo + GitHub。有一些问题要看 issues。
	- 安装了一下 notion，好像官方没有提供 Linux 版本。
- 安装 OCS
- 输入法加强
	- [GitHub - Reverier-Xu/Ori-fcitx5](https://github.com/Reverier-Xu/Ori-Fcitx5)
	- [kancloud.cn/xhyx/xhyx/1917919](https://www.kancloud.cn/xhyx/xhyx/1917919)
	- [GitHub - cubercsl/rime-flypy: 小鹤音形 Rime 挂接 / Fcitx5 码表 For Linux & Android](https://github.com/cubercsl/rime-flypy)
	- [双拼练习 - 打字练习 - 在线打字练习（dazi.91xjr.com）](https://dazi.91xjr.com/typing/train/shuang.html)
	- 后来还是用了双拼而不是音形，感觉音形太复杂了。
		- 双拼直接在 fcitx5 中就有内置的，记得要去设置一下使用哪个方案，以及要开启云拼音

```zsh
sudo apt install bat
sudo apt install fd-find
```
