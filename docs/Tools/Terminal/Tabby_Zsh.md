# Tabby + Zsh 配置指南



## 前置准备

系统要求

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y \
    git \
    curl \
    wget \
    build-essential \
    cmake \
    python3-pip \
    pkg-config \
    libssl-dev
```


## ZSH 基础配置

ZSH 安装

```bash
# 安装zsh
sudo apt install zsh

# 设置为默认shell
chsh -s $(which zsh)

# 确认设置
echo $SHELL
# 应该输出: /usr/bin/zsh
```


### 1. Oh My Zsh 安装

```bash
# 安装Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 备份默认配置
cp ~/.zshrc ~/.zshrc.backup
```

### 2. 插件管理器安装

```bash
# 安装zinit
bash -c "$(curl --fail --show-error --silent --location https://raw.githubusercontent.com/zdharma-continuum/zinit/HEAD/scripts/install.sh)"

# 等待安装完成后重启终端
exec zsh
```

### 3. 基础配置文件

```bash
# 创建新的配置文件
cat << 'EOF' > ~/.zshrc
# 基础设置
export ZSH="$HOME/.oh-my-zsh"
export LANG=en_US.UTF-8
export EDITOR='nvim'
export VISUAL='nvim'

# zinit配置
source "$HOME/.local/share/zinit/zinit.git/zinit.zsh"
autoload -Uz _zinit
(( ${+_comps} )) && _comps[zinit]=_zinit

# 加载核心插件
zinit ice depth=1; zinit light romkatv/powerlevel10k  # 主题
zinit light zsh-users/zsh-autosuggestions           # 命令建议
zinit light zsh-users/zsh-syntax-highlighting       # 语法高亮
zinit light zsh-users/zsh-completions              # 补全增强
zinit light agkozak/zsh-z                          # 目录跳转

# 历史记录设置
HISTFILE="$HOME/.zsh_history"
HISTSIZE=50000
SAVEHIST=50000
setopt EXTENDED_HISTORY          # 记录命令时间戳
setopt HIST_EXPIRE_DUPS_FIRST   # 优先删除重复命令
setopt HIST_IGNORE_DUPS         # 忽略连续重复命令
setopt HIST_IGNORE_SPACE        # 忽略以空格开头的命令
setopt HIST_VERIFY              # 执行历史命令前展示
setopt INC_APPEND_HISTORY       # 实时添加历史记录
setopt SHARE_HISTORY           # 共享历史记录

# 目录设置
setopt AUTO_CD              
setopt AUTO_PUSHD          
setopt PUSHD_IGNORE_DUPS   
setopt PUSHD_MINUS         
DIRSTACKSIZE=20

EOF
```

### 4. 实用别名设置

```bash
# 添加到~/.zshrc
cat << 'EOF' >> ~/.zshrc
# 基础命令增强
alias ls='ls --color=auto'
alias ll='ls -lah'
alias la='ls -A'
alias l='ls -CF'
alias grep='grep --color=auto'
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias mkdir='mkdir -p'
alias df='df -h'
alias free='free -m'
alias duf='du -sh *'
alias ps='ps auxf'
alias ping='ping -c 5'
alias root='sudo -i'
alias reboot='sudo reboot'
alias poweroff='sudo poweroff'

# Git快捷命令
alias gs='git status'
alias ga='git add'
alias gaa='git add --all'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'
alias gco='git checkout'
alias gb='git branch'
alias gm='git merge'
alias glog='git log --oneline --decorate --graph'

# Docker快捷命令
alias dk='docker'
alias dkc='docker-compose'
alias dkps='docker ps'
alias dkst='docker stats'
alias dktop='docker top'
alias dkimg='docker images'
alias dkpull='docker pull'
alias dkex='docker exec -it'

# 快速编辑
alias zshconfig="$EDITOR ~/.zshrc"
alias zshreload="source ~/.zshrc"
alias vimconfig="$EDITOR ~/.vimrc"
alias tmuxconfig="$EDITOR ~/.tmux.conf"
EOF
```

### 5. 实用函数

```bash
# 添加到~/.zshrc
cat << 'EOF' >> ~/.zshrc
# 创建并进入目录
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# 提取压缩文件
extract() {
    if [ -f $1 ]; then
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
            *)          echo "'$1' cannot be extracted" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# 快速查找文件
ff() { find . -type f -iname "*$1*" ; }
fd() { find . -type d -iname "*$1*" ; }

# 快速查看进程
psg() { ps aux | grep -v grep | grep -i -e VSZ -e "$1"; }

# 网络工具
myip() {
    curl -s http://ipecho.net/plain
    echo
}

# 快速HTTP服务器
serve() {
    local port="${1:-8000}"
    python3 -m http.server "$port"
}

# Git日志美化
gll() {
    git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
}
EOF
```

## 主题美化与插件增强

### 一、Powerlevel10k 主题配置

#### 1. 安装必要字体

```bash
# 创建字体目录
mkdir -p ~/.local/share/fonts

# 下载推荐字体
wget -P /tmp https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf
wget -P /tmp https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf
wget -P /tmp https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf
wget -P /tmp https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf

# 移动字体文件
mv /tmp/MesloLGS*.ttf ~/.local/share/fonts/

# 更新字体缓存
fc-cache -f -v
```

#### 2. 主题配置

```bash
# 添加到 ~/.zshrc
cat << 'EOF' >> ~/.zshrc
# Powerlevel10k 配置
# 启用 Powerlevel10k 即时提示
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# 加载主题
source ~/.oh-my-zsh/custom/themes/powerlevel10k/powerlevel10k.zsh-theme

# 主题个性化设置
POWERLEVEL9K_MODE='nerdfont-complete'
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  os_icon                 # 操作系统图标
  dir                     # 当前目录
  vcs                     # git状态
  newline                 # 换行
  prompt_char            # 提示符
)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(
  status                  # 上一个命令的状态
  background_jobs        # 后台任务
  load                   # 系统负载
  ram                    # 内存使用
  time                   # 时间
)

# 目录显示设置
POWERLEVEL9K_DIR_BACKGROUND='blue'
POWERLEVEL9K_DIR_FOREGROUND='black'
POWERLEVEL9K_SHORTEN_DIR_LENGTH=2
POWERLEVEL9K_SHORTEN_STRATEGY="truncate_middle"

# Git状态设置
POWERLEVEL9K_VCS_CLEAN_BACKGROUND='green'
POWERLEVEL9K_VCS_UNTRACKED_BACKGROUND='yellow'
POWERLEVEL9K_VCS_MODIFIED_BACKGROUND='red'
EOF

# 运行配置向导（首次使用）
p10k configure
```

### 二、高级插件配置

#### 1. 高级补全系统

```bash
# 添加到 ~/.zshrc
cat << 'EOF' >> ~/.zshrc
# 补全系统配置
autoload -Uz compinit
compinit

# 补全菜单设置
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'   # 忽略大小写
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}       # 补全菜单着色
zstyle ':completion:*' verbose yes                         # 详细补全菜单
zstyle ':completion:*:descriptions' format '%U%B%d%b%u'     # 补全菜单格式
zstyle ':completion:*:warnings' format '%BSorry, no matches for: %d%b'
zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'
zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'

# 使用缓存加速补全
zstyle ':completion:*' use-cache on
zstyle ':completion:*' cache-path ~/.zsh/cache
EOF
```

#### 2. FZF 集成配置

```bash
# 安装FZF
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# 添加到 ~/.zshrc
cat << 'EOF' >> ~/.zshrc
# FZF 配置
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --preview "bat --style=numbers --color=always --line-range :500 {}"'

# FZF 快捷键
bindkey '^T' fzf-file-widget
bindkey '^R' fzf-history-widget
bindkey '^[c' fzf-cd-widget

# FZF 函数
# 快速打开文件
fe() {
  local file
  file=$(fzf --query="$1" --select-1 --exit-0)
  [ -n "$file" ] && ${EDITOR:-vim} "$file"
}

# 快速切换目录
fd() {
  local dir
  dir=$(find ${1:-.} -path '*/\.*' -prune -o -type d -print 2> /dev/null | fzf +m)
  [ -n "$dir" ] && cd "$dir"
}

# 搜索历史命令
fh() {
  print -z $( ([ -n "$ZSH_NAME" ] && fc -l 1 || history) | fzf +s --tac | sed -E 's/ *[0-9]*\*? *//' | sed -E 's/\\/\\\\/g')
}
EOF
```

#### 3. 增强目录导航

```bash
# 添加到 ~/.zshrc
cat << 'EOF' >> ~/.zshrc
# 目录书签
hash -d proj=~/projects
hash -d docs=~/Documents
hash -d dl=~/Downloads
hash -d pics=~/Pictures

# z 插件配置
ZSHZ_DATA=~/.local/share/z/data
ZSHZ_MAX_SCORE=5000
ZSHZ_CASE=smart

# 目录堆栈导航
setopt AUTO_PUSHD           # 自动将目录加入堆栈
setopt PUSHD_IGNORE_DUPS    # 忽略重复目录
setopt PUSHD_SILENT        # 静默模式
setopt PUSHD_TO_HOME       # pushd 不带参数时等同于 pushd $HOME

# 目录别名
alias -g ...='../..'
alias -g ....='../../..'
alias -g .....='../../../..'
alias d='dirs -v'
for index ({1..9}) alias "$index"="cd +${index}"; unset index
EOF
```

#### 4. 增强历史记录搜索

```bash
# 添加到 ~/.zshrc
cat << 'EOF' >> ~/.zshrc
# 历史记录搜索配置
bindkey '^[[A' history-substring-search-up
bindkey '^[[B' history-substring-search-down
bindkey '^P' history-substring-search-up
bindkey '^N' history-substring-search-down

# 历史记录格式化
HIST_STAMPS="yyyy-mm-dd"
HISTORY_IGNORE="(ls|ls *|cd|cd *|pwd|exit|date|* --help)"

# 命令执行时间显示
REPORTTIME=10
EOF
```

## Tabby 终端配置

### 一、安装和初始化

#### 1. 安装 Tabby

```bash
# Ubuntu/Debian
wget https://github.com/Eugeny/tabby/releases/latest/download/tabby-1.0.0-linux-x64.deb
sudo dpkg -i tabby-*.deb
sudo apt-get install -f

# 确保字体支持
fc-cache -fv
```

#### 2. 初始配置

```yaml
# ~/.config/tabby/config.yaml
config:
  version: 3

terminal:
  shell: zsh  # 使用前面配置的zsh
  fontSize: 14
  lineHeight: 1.2
  bell: 'off'
  copyOnSelect: true
  rightClick: menu

  # 基础环境变量
  environment:
    TERM: xterm-256color
    COLORTERM: truecolor

  # 性能设置
  performanceMode: true
  gpuAcceleration: true
  webGL: true
```

### 二、外观配置

#### 1. 字体设置

```yaml
terminal:
  font: JetBrainsMono Nerd Font  # 确保已安装
  fontSize: 14
  lineHeight: 1.2
  ligatures: true  # 连字支持
  
  # 字体回退
  fallbackFont: 'Sarasa Mono SC'  # 中文支持
```

#### 2. Dracula 主题配置

```yaml
profiles:
  - name: Default
    theme:
      name: 'Dracula'
    
    colors:
      background: '#282a36'
      foreground: '#f8f8f2'
      cursor: '#f8f8f2'
      
      selection:
        background: '#44475a'
        foreground: '#f8f8f2'
      
      # ANSI Colors
      black: '#21222c'
      red: '#ff5555'
      green: '#50fa7b'
      yellow: '#f1fa8c'
      blue: '#bd93f9'
      magenta: '#ff79c6'
      cyan: '#8be9fd'
      white: '#f8f8f2'
      
      # Bright Colors
      brightBlack: '#6272a4'
      brightRed: '#ff6e6e'
      brightGreen: '#69ff94'
      brightYellow: '#ffffa5'
      brightBlue: '#d6acff'
      brightMagenta: '#ff92df'
      brightCyan: '#a4ffff'
      brightWhite: '#ffffff'
```

#### 3. 透明背景配置

```yaml
terminal:
  background:
    type: 'image'  # 或 'color'
    image: '~/.config/tabby/backgrounds/bg.jpg'  # 自定义背景图片
    opacity: 0.85  # 透明度
    
  # 亚克力效果（Windows）
  experimental:
    vibrancy: true
```

### 三、快捷键配置

```yaml
hotkeys:
  # 标签管理
  new-tab: ['Ctrl+T']
  close-tab: ['Ctrl+W']
  previous-tab: ['Ctrl+Shift+Tab']
  next-tab: ['Ctrl+Tab']
  
  # 分屏操作
  split-right: ['Ctrl+Shift+E']
  split-bottom: ['Ctrl+Shift+O']
  split-nav-left: ['Alt+Left']
  split-nav-right: ['Alt+Right']
  split-nav-up: ['Alt+Up']
  split-nav-down: ['Alt+Down']
  
  # 终端操作
  clear: ['Ctrl+L']
  copy: ['Ctrl+C']
  paste: ['Ctrl+V']
  search: ['Ctrl+Shift+F']
  
  # 视图控制
  zoom-in: ['Ctrl+Plus']
  zoom-out: ['Ctrl+Minus']
  reset-zoom: ['Ctrl+0']
  toggle-fullscreen: ['F11']
  
  # 快速命令
  command-palette: ['Ctrl+Shift+P']
```

### 四、SSH 配置

#### 1. 基础 SSH 配置

```yaml
ssh:
  auth:
    agent: true
    privateKeys:
      - ~/.ssh/id_ed25519
      - ~/.ssh/id_rsa
  
  # 连接保持
  keepaliveInterval: 30
  keepaliveCountMax: 3
  
  # 转发设置
  forwardAgent: true
  x11: false
```

#### 2. SSH 连接配置

```yaml
ssh:
  profiles:
    - name: "开发服务器"
      group: "开发环境"
      host: dev.example.com
      port: 22
      user: username
      auth: publicKey
      privateKey: ~/.ssh/id_ed25519
      
    - name: "生产服务器"
      group: "生产环境"
      host: prod.example.com
      port: 22
      user: username
      auth: agent
      
    - name: "跳板机"
      host: jump.example.com
      forwardAgent: true
      jumpHost: true  # 标记为跳板机
```

### 五、插件配置

#### 1. 核心插件

```yaml
plugins:
  # SSH管理
  ssh:
    enabled: true
    
  # 终端录制
  record:
    enabled: true
    directory: ~/terminal-records
    
  # 命令面板
  commander:
    enabled: true
    
  # 主题插件
  community-color-schemes:
    enabled: true
```

#### 2. 扩展功能

```yaml
# 搜索增强
search:
  enabled: true
  searchOptions:
    regex: true
    wholeWord: false
    caseSensitive: false

# 终端分割
split:
  autoRemove: true  # 自动关闭空终端
  copyOnSelect: true
  pasteOnMiddleClick: true
```

### 六、性能优化

```yaml
# 性能相关配置
terminal:
  # 基础优化
  performanceMode: true
  gpuAcceleration: true
  webGL: true
  
  # 历史记录
  scrollback: 5000
  
  # 进程管理
  autoClose: true
  closeOnExit: true
  
  # 渲染优化
  smoothScroll: false
  experimentalFontRendering: false
  
  # 资源限制
  environment:
    LIMIT_MEMORY: 512  # MB
```

## 开发工具与终端工具配置

### 一、现代命令行工具

#### 1. 基础工具安装

```bash
# 安装基础工具
sudo apt install -y \
    exa `# 现代ls替代品` \
    bat `# 现代cat替代品` \
    ripgrep `# 现代grep替代品` \
    fd-find `# 现代find替代品` \
    duf `# 现代df替代品` \
    ncdu `# 磁盘使用分析` \
    tldr `# 命令简化说明` \
    jq `# JSON处理` \
    fzf `# 模糊搜索`

# 创建别名
cat << 'EOF' >> ~/.zshrc
# 现代命令行工具别名
alias ls='exa --icons'
alias ll='exa -l --icons --git'
alias la='exa -la --icons --git'
alias lt='exa -T --icons --git-ignore'
alias cat='batcat'
alias find='fd'
alias du='ncdu'
alias df='duf'
alias help='tldr'

# fzf 配置
export FZF_DEFAULT_OPTS="--height 40% --layout=reverse --border \
    --preview 'batcat --style=numbers --color=always --line-range :500 {}'"
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
EOF
```

#### 2. 文件管理器 - Ranger

```bash
# 安装ranger和依赖
sudo apt install ranger python3-pillow ueberzug

# 生成配置文件
ranger --copy-config=all

# 配置Ranger
cat << 'EOF' > ~/.config/ranger/rc.conf
# 基础设置
set preview_images true
set preview_images_method ueberzug
set show_hidden true
set hostname_in_titlebar false
set tilde_in_titlebar true
set line_numbers relative
set mouse_enabled true

# 配色方案
set colorscheme solarized

# 文件预览
set use_preview_script true
set preview_files true
set preview_directories true
set collapse_preview true

# 快捷键
map <C-f> fzf_select
map <C-p> shell -w echo %d/%f | xsel -b
map <C-g> shell lazygit
EOF

# 添加FZF集成
cat << 'EOF' > ~/.config/ranger/commands.py
from ranger.api.commands import Command
class fzf_select(Command):
    def execute(self):
        import subprocess
        import os.path
        command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        fzf = self.fm.execute_command(command, universal_newlines=True, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)
EOF
```

#### 3. 系统监控 - htop/glances

```bash
# 安装工具
sudo apt install htop glances

# htop配置
mkdir -p ~/.config/htop
cat << 'EOF' > ~/.config/htop/htoprc
# 基础显示设置
show_cpu_frequency=1
show_cpu_temperature=1
show_program_path=0
highlight_base_name=1
highlight_megabytes=1
highlight_threads=1

# 显示设置
fields=0 48 17 18 38 39 40 2 46 47 49 1
sort_key=46
sort_direction=-1
tree_view=1
tree_view_always_by_pid=0

# 颜色设置
color_scheme=0
EOF

# glances配置
mkdir -p ~/.config/glances
cat << 'EOF' > ~/.config/glances/glances.conf
[global]
# 刷新间隔
refresh=2
# 历史大小
history_size=1200

[cpu]
# CPU 警告阈值
careful=50
warning=70
critical=90

[memory]
# 内存警告阈值
careful=50
warning=70
critical=90

[network]
# 网络带宽显示单位 (bit/sec)
unit=bit
EOF
```

#### 4. Git 工具 - Lazygit

```bash
# 安装Lazygit
LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[^"]*')
curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz"
sudo tar xf lazygit.tar.gz -C /usr/local/bin lazygit

# 配置Lazygit
mkdir -p ~/.config/lazygit
cat << 'EOF' > ~/.config/lazygit/config.yml
gui:
  # UI主题
  theme:
    lightTheme: false
    activeBorderColor:
      - green
      - bold
    inactiveBorderColor:
      - white
    selectedLineBgColor:
      - reverse
  # 常用设置  
  showFileTree: true
  showRandomTip: false
  showCommandLog: false
  
git:
  # git设置
  paging:
    colorArg: always
    useConfig: true
  # commit设置
  commits:
    showGraph: always
    showWholeGraph: true
  # 自动获取
  autoFetch: true
  # 分支显示
  branchLogCmd: "git log --graph --color=always --abbrev-commit --decorate --date=relative --pretty=medium {{branchName}} --"

keybinding:
  # 自定义快捷键
  universal:
    return: '<c-c>'
    quit: 'q'
    quit-alt1: '<esc>'
EOF
```

#### 5. 代码搜索工具

```bash
# ripgrep配置
cat << 'EOF' >> ~/.zshrc
# ripgrep 配置
export RIPGREP_CONFIG_PATH="$HOME/.ripgreprc"

# ripgrep 别名
alias rg='rg --smart-case'
alias rgf='rg --files | rg'
alias rgh='rg --hidden'
alias rgc='rg --count'

# fzf + ripgrep 集成
fif() {
    if [ ! "$#" -gt 0 ]; then echo "Need a string to search for!"; return 1; fi
    rg --files-with-matches --no-messages "$1" | fzf --preview "highlight -O ansi -l {} 2> /dev/null | rg --colors 'match:bg:yellow' --ignore-case --pretty --context 10 '$1' || rg --ignore-case --pretty --context 10 '$1' {}"
}
EOF

# 创建ripgrep配置文件
cat << 'EOF' > ~/.ripgreprc
# 默认配置
--smart-case
--hidden
--follow
--glob=!.git/*

# 搜索配置
--max-columns=150
--max-columns-preview

# 颜色配置
--colors=line:fg:yellow
--colors=line:style:bold
--colors=path:fg:green
--colors=path:style:bold
--colors=match:fg:black
--colors=match:bg:yellow
--colors=match:style:nobold
EOF
```

#### 6. 实用开发工具

```bash
# 安装开发辅助工具
sudo apt install -y \
    shellcheck `# shell脚本检查` \
    python3-pip `# Python包管理` \
    nodejs npm `# Node.js环境` \
    golang `# Go语言环境` \
    docker.io `# Docker支持` \
    postgresql-client `# 数据库客户端` \
    redis-tools `# Redis客户端` \
    mycli `# MySQL客户端` \
    httpie `# HTTP客户端`

# 添加实用别名和函数
cat << 'EOF' >> ~/.zshrc
# Docker别名
alias dk='docker'
alias dkc='docker-compose'
alias dkps='docker ps'
alias dkst='docker stats'
alias dkimg='docker images'
alias dkpull='docker pull'
alias dkexec='docker exec -it'

# 开发辅助函数
# 快速HTTP服务器
serve() {
    local port="${1:-8000}"
    python3 -m http.server "$port"
}

# JSON格式化
json() {
    if [ -t 0 ]; then  # 参数输入
        python -m json.tool <<< "$*" | pygmentize -l json
    else  # 管道输入
        python -m json.tool | pygmentize -l json
    fi
}

# Git分支清理
git-clean() {
    git branch --merged | egrep -v "(^\*|master|main|dev)" | xargs git branch -d
}

# 环境变量管理
envfile() {
    if [[ -f "$1" ]]; then
        set -a
        source "$1"
        set +a
    else
        echo "Error: File $1 not found"
        return 1
    fi
}
EOF
```
