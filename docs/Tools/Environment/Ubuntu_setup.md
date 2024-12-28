# Ubuntu 配置
- [在 Ubuntu 安装配置 Fcitx 5 中文输入法 - muzing的杂货铺](https://muzing.top/posts/3fc249cf/#:~:text=Fcitx%205%20%E6%8F%90%E4%BE%9B)
- [fcitx5-rime 挂接小鹤音形 | rovo98's Blog](https://rovo98.github.io/posts/2f1de6fa/#:~:text=%E4%BD%BF%E7%94%A8%20fcitx5-)
- [zhuanlan.zhihu.com/p/660191327#:\~:text=Tabby（以前称为](https://zhuanlan.zhihu.com/p/660191327#:~:text=Tabby%EF%BC%88%E4%BB%A5%E5%89%8D%E7%A7%B0%E4%B8%BA)
- [Zsh 安装与配置，使用 Oh-My-Zsh 美化终端 | Leehow的小站](https://www.haoyep.com/posts/zsh-config-oh-my-zsh/)
- [zhuanlan.zhihu.com/p/658811059](https://zhuanlan.zhihu.com/p/658811059)
- [PKMer\_TiddyWiki 简易指南](https://pkmer.cn/Pkmer-Docs/12-tiddywiki/tiddywiki/)
- [Site Unreachable](https://docusaurus.nodejs.cn/docs)
- [Jedsek | Blog](https://jedsek.xyz/posts/desktop-beautify/gnome/)

```shell
visudo /etc/sudoers	
%sudo   ALL=(ALL:ALL) NOPASSWD: ALL
```

```shell
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

git clone git://github.com/joelthelion/autojump.git
cd autojump
./install.py

[[ -s ~/.autojump/etc/profile.d/autojump.sh ]] && . ~/.autojump/etc/profile.d/autojump.sh
```

- 截图软件

```shell
sudo apt-get install flameshot
flameshot gui

```

- [在 Ubuntu 22.04|20.04|18.04 上安装 Node.js 20](https://cn.linux-console.net/?p=20486)
