---
title: Tabby 终端配置完全指南
tags:
  - Tools
  - CheatSheet
categories: graph
date: 2024-11-18T20:58:22+0800
modify: 2024-12-06T00:13:58+0800
dir: Obsidian
share: false
---

# Tabby 终端配置完全指南

## 目录

1. [安装](#安装)
2. [基础配置](#基础配置)
3. [美化](#美化)
4. [插件](#插件)
5. [Shell集成](#shell集成)
6. [SSH管理](#ssh管理)
7. [性能优化](#性能优化)
8. [配置示例](#配置示例)
9. [常见问题](#常见问题)

## 安装

### Linux (Ubuntu/Debian)

```bash
# 下载最新的.deb包
wget https://github.com/Eugeny/tabby/releases/latest/download/tabby-1.0.0-linux-x64.deb

# 安装
sudo dpkg -i tabby-*.deb
sudo apt-get install -f
```

### Windows

```powershell
# 使用 Scoop
scoop install tabby

# 或使用 winget
winget install Eugeny.Tabby
```

## 基础配置

### 1. 终端设置

在 `~/.config/tabby/config.yaml` 或通过 GUI 配置：

```yaml
terminal:
  shell: bash  # 或 powershell/zsh
  fontSize: 14
  lineHeight: 1.2
  bell: 'off'
  copyOnSelect: true
  rightClick: menu  # 或 paste
  
  environment:
    TERM: xterm-256color
```

### 2. 快捷键配置

推荐的快捷键设置：

```yaml
hotkeys:
  new-tab:
    - 'Ctrl+T'
  close-tab:
    - 'Ctrl+W'
  toggle-fullscreen:
    - 'F11'
  split-right:
    - 'Ctrl+Shift+E'
  split-bottom:
    - 'Ctrl+Shift+O'
  copy:
    - 'Ctrl+C'
  paste:
    - 'Ctrl+V'
  search:
    - 'Ctrl+Shift+F'
  zoom-in:
    - 'Ctrl+Plus'
  zoom-out:
    - 'Ctrl+Minus'
```

## 美化

### 1. 字体配置

1. 安装 Nerd Fonts：

```bash
# Linux
wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.0.2/JetBrainsMono.zip
unzip JetBrainsMono.zip -d ~/.local/share/fonts
fc-cache -fv

# Windows (使用 scoop)
scoop bucket add nerd-fonts
scoop install JetBrainsMono-NF
```

2. 配置字体：

```yaml
terminal:
  font: JetBrainsMono Nerd Font
  fontSize: 14
  ligatures: true
```

### 2. 主题配置

内置主题：

```yaml
profiles:
  - name: Default
    theme: 
      # 流行的主题选项：
      # - "Dracula"
      # - "Material"
      # - "One Dark"
      # - "Snazzy"
      # - "Nord"
      name: "Dracula"
    
    # 自定义配色
    colors:
      background: '#282a36'
      foreground: '#f8f8f2'
      cursor: '#f8f8f2'
      
      # ANSI Colors
      black: '#21222c'
      red: '#ff5555'
      green: '#50fa7b'
      yellow: '#f1fa8c'
      blue: '#bd93f9'
      magenta: '#ff79c6'
      cyan: '#8be9fd'
      white: '#f8f8f2'
```

### 3. 背景配置

```yaml
terminal:
  background:
    type: 'image'  # 或 'color'
    image: '/path/to/your/image.jpg'
    opacity: 0.8
    
  # 或使用纯色背景
  background:
    type: 'color'
    color: '#1a1b26'
```

## 插件

### 1. 推荐插件

- **tabby-ssh**: SSH 连接管理
- **tabby-serial**: 串口连接
- **tabby-community-color-schemes**: 更多配色方案
- **tabby-save-output**: 保存终端输出
- **tabby-commander**: 命令面板

### 2. 插件配置

```yaml
plugins:
  # SSH 插件配置
  ssh:
    auth:
      agent: true
      privateKeys:
        - ~/.ssh/id_rsa
        - ~/.ssh/id_ed25519
    
    # 保存的连接配置
    profiles:
      - name: "开发服务器"
        host: dev.example.com
        user: username
        port: 22
        
  # 社区主题插件
  communityThemes:
    enabled: true
```

## PowerShell 集成

1. 安装 Oh My Posh：

```powershell
Install-Module oh-my-posh -Scope CurrentUser
```

2. 配置 PowerShell 配置文件：

```powershell
# 在 $PROFILE 中添加
Import-Module oh-my-posh
Set-PoshPrompt -Theme paradox
```

## SSH 管理

### 1. SSH 配置

```yaml
ssh:
  connections:
    - name: "开发服务器"
      host: dev.example.com
      port: 22
      user: username
      auth: publicKey
      privateKey: ~/.ssh/id_rsa
      
    - name: "生产服务器"
      host: prod.example.com
      port: 22
      user: username
      auth: agent
      
  options:
    reconnectOnError: true
    keepaliveInterval: 30
    keepaliveCountMax: 3
    compression: true
```

### 2. SSH 代理转发

```yaml
ssh:
  forwardAgent: true
  
  # 特定主机的代理转发
  profiles:
    - name: "跳板机"
      forwardAgent: true
      host: jump.example.com
```

## 性能优化

### 1. 终端性能设置

```yaml
terminal:
  # 提升性能的设置
  performanceMode: true
  shellIntegration: false  # 如果不需要shell集成
  colorSchemeAdjustment: null  # 禁用颜色调整
  
  # 减少资源使用
  scrollback: 1000  # 减少历史记录
  enableAnalytics: false
  
  # GPU 加速
  gpuAcceleration: true
  webGL: true
```

### 2. 启动优化

```yaml
appearance:
  # 减少启动时间
  dock: 'off'  # 禁用dock
  theme: 'Native'  # 使用原生主题
  frame: 'thin'  # 使用细边框
```

## 配置示例

完整的配置示例：

```yaml
# ~/.config/tabby/config.yaml

config:
  version: 3

terminal:
  shell: zsh
  font: JetBrainsMono Nerd Font
  fontSize: 14
  ligatures: true
  lineHeight: 1.2
  
  background:
    type: 'image'
    image: '~/.config/tabby/background.jpg'
    opacity: 0.8
  
  cursor:
    style: 'beam'
    blink: true
    
  colorScheme:
    name: 'Dracula'
    
hotkeys:
  new-tab: ['Ctrl+T']
  close-tab: ['Ctrl+W']
  toggle-fullscreen: ['F11']
  split-right: ['Ctrl+Shift+E']
  split-bottom: ['Ctrl+Shift+O']
  
ssh:
  connections:
    - name: "开发服务器"
      host: dev.example.com
      user: username
      
profiles:
  - name: Default
    shell: zsh
    theme:
      name: 'Dracula'
      
  - name: PowerShell
    shell: powershell
    theme:
      name: 'One Dark'

plugins:
  ssh: true
  serial: true
  save-output: true
```

## 推荐终端工具

### 1. 文件管理器

#### Ranger

```bash
# 安装
sudo apt install ranger

# 生成配置文件
ranger --copy-config=all

# 配置预览
vim ~/.config/ranger/rc.conf

# 常用配置
set preview_images true
set preview_images_method ueberzug
set show_hidden true
```

#### nnn

```bash
# 安装
sudo apt install nnn

# 配置别名
echo 'alias n="nnn -de"' >> ~/.zshrc

# 环境变量
export NNN_PLUG='f:finder;o:fzopen;p:mocplay;d:diffs;t:nmount;v:imgview'
```

### 2. 系统监控

#### htop

```bash
# 安装
sudo apt install htop

# 配置
mkdir -p ~/.config/htop
cp /etc/htop/htoprc ~/.config/htop/
```

#### glances

```bash
# 安装
sudo apt install glances

# 配置
mkdir -p ~/.config/glances
glances -C > ~/.config/glances/glances.conf
```

### 3. 搜索工具

#### ripgrep (rg)

```bash
# 安装
sudo apt install ripgrep

# 配置
echo 'alias rg="rg --smart-case"' >> ~/.zshrc
```

#### fzf

```bash
# 安装
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# 配置
echo 'export FZF_DEFAULT_OPTS="--height 40% --layout=reverse --border"' >> ~/.zshrc
echo 'export FZF_DEFAULT_COMMAND="fd --type f"' >> ~/.zshrc
```

### 4. Git 工具

#### lazygit

```bash
# 安装
sudo add-apt-repository ppa:lazygit-team/release
sudo apt-get update
sudo apt-get install lazygit

# 配置
mkdir -p ~/.config/lazygit
echo "gui:
  theme:
    activeBorderColor:
      - green
      - bold
    inactiveBorderColor:
      - white
    optionsTextColor:
      - blue" > ~/.config/lazygit/config.yml
```

#### tig

```bash
# 安装
sudo apt install tig

# 配置
echo "
set main-view = id date author commit-title:graph=yes,refs=yes
set blame-view = date:default author:email-user id:yes,color line-number:yes,interval=5 text
" > ~/.tigrc
```

### 5. 开发工具

#### tmux

```bash
# 安装
sudo apt install tmux

# 配置
cat << 'EOF' > ~/.tmux.conf
# 使用Ctrl-a作为前缀键
set -g prefix C-a
unbind C-b
bind C-a send-prefix

# 开启鼠标支持
set -g mouse on

# 使用vim键位
setw -g mode-keys vi

# 状态栏设置
set -g status-style fg=white,bg=black
set -g status-left "#[fg=green]Session: #S #[fg=yellow]#I #[fg=cyan]#P"
set -g status-right "#[fg=cyan]%d %b %R"

# 窗口列表
set -g window-status-current-style fg=black,bg=white
EOF
```

#### neovim

```bash
# 安装
sudo apt install neovim

# 配置
mkdir -p ~/.config/nvim
cat << 'EOF' > ~/.config/nvim/init.vim
" 基础设置
set number
set relativenumber
set expandtab
set tabstop=4
set shiftwidth=4
set smartindent
set cursorline
set termguicolors

" 插件管理
call plug#begin()
Plug 'morhetz/gruvbox'
Plug 'vim-airline/vim-airline'
Plug 'neoclide/coc.nvim', {'branch': 'release'}
Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plug 'junegunn/fzf.vim'
call plug#end()

" 主题设置
colorscheme gruvbox
set background=dark
EOF
```

## Zsh 配置

安装 Oh My Zsh：

```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

配置 .zshrc：

```bash
# Oh My Zsh 配置
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(
  git
  zsh-syntax-highlighting
  zsh-autosuggestions
  docker
  docker-compose
)
```

### 1. Oh My Zsh 增强

```bash
# 安装zinit
sh -c "$(curl -fsSL https://raw.githubusercontent.com/zdharma-continuum/zinit/master/doc/install.sh)"

# 配置zinit和插件
cat << 'EOF' >> ~/.zshrc
### Added by Zinit's installer
source "$HOME/.local/share/zinit/zinit.git/zinit.zsh"
autoload -Uz _zinit
(( ${+_comps} )) && _comps[zinit]=_zinit

# 加载插件
zinit light zdharma-continuum/fast-syntax-highlighting
zinit light zsh-users/zsh-autosuggestions
zinit light zsh-users/zsh-completions
zinit ice depth=1; zinit light romkatv/powerlevel10k

# 补全设置
autoload -Uz compinit
compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

# 历史记录设置
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_FIND_NO_DUPS

# 目录跳转
setopt AUTO_CD
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS

# 别名设置
alias ll='ls -lah'
alias gz='git cz'
alias gst='git status'
alias gd='git diff'
alias gc='git checkout'
alias gp='git push'
alias gl='git pull'
alias vim='nvim'
alias vi='nvim'
alias :q='exit'

# FZF集成
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
export FZF_DEFAULT_COMMAND='rg --files --hidden --follow --glob "!.git/*"'

# 自定义函数
mkcd() {
    mkdir -p "$1" && cd "$1"
}

extract() {
    if [ -f $1 ] ; then
        case $1 in
            *.tar.bz2)   tar xjf $1     ;;
            *.tar.gz)    tar xzf $1     ;;
            *.bz2)       bunzip2 $1     ;;
            *.rar)       unrar e $1     ;;
            *.gz)        gunzip $1      ;;
            *.tar)       tar xf $1      ;;
            *.tbz2)      tar xjf $1     ;;
            *.tgz)       tar xzf $1     ;;
            *.zip)       unzip $1       ;;
            *.Z)         uncompress $1  ;;
            *.7z)        7z x $1        ;;
            *)          echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# 开发环境变量
export EDITOR=nvim
export VISUAL=nvim
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
EOF
```

### 2. Powerlevel10k 主题配置

```bash
# 安装字体
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf
wget https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf

# 移动到字体目录
sudo mv MesloLGS*.ttf /usr/local/share/fonts/

# 更新字体缓存
fc-cache -f -v

# 配置p10k
p10k configure
```

### 3. 常用插件配置

```bash
# 目录跳转插件
zinit light agkozak/zsh-z

# Git插件
zinit light paulirish/git-open

# 命令提示插件
zinit light zsh-users/zsh-history-substring-search

# 加载完成后的按键绑定
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down
```

### 4. 工作流优化

```bash
# 添加到 .zshrc

# 快速编辑配置文件
alias zshconfig="$EDITOR ~/.zshrc"
alias ohmyzsh="$EDITOR ~/.oh-my-zsh"

# 目录书签
hash -d projects=~/projects
hash -d downloads=~/Downloads
hash -d docs=~/Documents

# 命令行计算器
calc() {
    echo "$*" | bc -l
}

# HTTP服务器
serve() {
    python3 -m http.server ${1:-8000}
}

# Git快捷函数
gdiff() {
    git diff --color | diff-so-fancy | less -RFX
}

# 快速查找和编辑
fe() {
    local file
    file=$(fzf --query="$1" --select-1 --exit-0)
    [ -n "$file" ] && ${EDITOR:-vim} "$file"
}

# 进程查找
fps() {
    ps aux | head -1
    ps aux | grep -v grep | grep -i "$@"
}
```


## 常见问题

### 1. 字体显示问题

如果字体显示不正确：

1. 确保正确安装了 Nerd Fonts
2. 检查字体名称是否正确
3. 尝试禁用连字

### 2. 性能问题

如果遇到性能问题：

1. 启用性能模式
2. 减少历史记录大小
3. 禁用不必要的插件
4. 使用简单的主题

### 3. SSH 连接问题

常见 SSH 问题解决：

1. 检查 SSH 密钥权限
2. 确认代理是否正常运行
3. 检查防火墙设置
4. 查看详细日志

### 4. 配置备份

建议使用 chezmoi 管理配置：

```bash
# 添加配置到 chezmoi
chezmoi add ~/.config/tabby/config.yaml

# 应用配置
chezmoi apply
```
