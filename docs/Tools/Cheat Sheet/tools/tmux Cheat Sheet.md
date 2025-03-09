---
title: tmux Cheat Sheet
tags:
  - CheatSheet
categories: 
date: 2025-02-01T14:22:36+08:00
modify: 2025-02-01T14:22:36+08:00
dir: 
share: false
cdate: 2025-02-01
mdate: 2025-02-01
---

# tmux Cheat Sheet

## session

```
tmux                      # 创建新的 session
tmux new -S name          # 创建新的 session 并指定一个name
tmux ls                   # 查看多少个后台工作的 session
tmux a/at/attach          # 重新连接 session 
tmux a/at/attach -t num   # 如果有多个 session, 指定 session num 连接
tmux kill-ses -t myses    # kill 某个 session
tmux kill-ses -a          # kill 所有 session, 除了当前的 session
tmux kill-ses -a -t myses # kill 所有 session, 除了 myses
```

## 操作方式

```
<prefix> + key            # <prefix> 默认为 ctrl + b
<prefix> + c              # 表示先按 ctrl + b 再按 c 键
```

## 帮助信息

```
<prefix> + ?              # 查看所有的 key map
```

## window 操作

```
<prefix> + c              # 新建一个 window
<prefix> + n              # 下一个 window
<prefix> + p              # 上一个 window
<prefix> + w              # 列出 window
<prefix> + &              # 关闭当前 window
<prefix> + num[1-9]       # 选定特定 num 的 window
<prefix> + f              # 查找 window 
<prefix> + ,              # 重命名 window 
<prefix> + .              # 移动 window 
```

## pane 操作

```
<prefix> + %              # 横向分裂 
<prefix> + "              # 纵向分裂 
<prefix> + 方向键         # 在一个 window 中切换 pane 
<prefix> + ctrl-方向键    # 调整 pane 大小
<prefix> + z              # 全屏化当前 pane, 再次执行退出全屏 
<prefix> + x              # 关闭当前 pane
<prefix> + q              # 显示 pane 编号
<prefix> + o              # 跳到下一个 pane 
<prefix> + {              # 跟前一个编号的 pane 交换
<prefix> + }              # 跟后一个编号的 pane 交换
<prefix> + ;              # 跳转到上一个活跃的 pane 
<prefix> + !              # 将 pane 转化为 window 
<prefix> + <Space>        # 改变 pane 的布局 
```

## session

```
<prefix> + d              # detach 整个session, 后续可以重新连接
<prefix> + s              # 列出 session
<prefix> + $              # 重命名 session
<prefix> + (              # 跳到上一个 seesion 
<prefix> + )              # 跳到下一个 seesion 
```

## Misc

```
<prefix> + t              # 显示时钟 
<prefix> + :              # 命令行 
```

## pane 同步

```
:setw synchronize-panes  # 打开(关闭) pane 同步模式, 发送命令到所有的 pane 中
                         # 只影响当前 window 的 pane
```

## 复制模式 (copy-mode)

添加下面一行到 $HOME/.tmux.conf, 通过 vim 的快捷键实现浏览, 复制等操作;

`setw -g mode-keys vi`

更多 vim 快捷键可参考 ../editors/vim.txt, 以下列出一些常用快捷键.

```
<prefix> + [              # 进入 copy mode 

vi             emacs      功能
^              M-m        # 跳转到一行开头
Escape         C-g        # 放弃选择
k              Up         # 上移
j              Down       # 下移 
h              Left       # 左移
l              Right      # 右移
L                         # 最后一行
M              M-r        # 中间一行
H              M-R        # 第一行    
$              C-e        # 跳转到行尾
:              g          # 跳转至某一行
C-d            M-Down     # 下翻半页
C-u            M-Up       # 上翻半页
C-f            Page down  # 下翻一页
C-b            Page up    # 上翻一页
w              M-f        # 下一个字符     
b              M-b        # 前一个字符
q              Escape     # 退出        
?              C-r        # 往上查找
/              C-s        # 往下查找
n              n          # 查找下一个

Space          C-Space    # 进入选择模式
Enter          M-w        # 确认选择内容, 并退出 

<prefix> + ]              # 粘贴选择内容(粘贴 buffer_0 的内容) 

:show-buffer              # 显示 buffer_0 的内容
:capture-buffer           # 复制整个能见的内容到当前的 buffer
:list-buffers             # 列出所有的 buffer 
:choose-buffer            # 列出所有的 buffer, 并选择用于粘贴的 buffer
:save-buffer buf.txt      # 将 buffer 的内容复制到 buf.txt
:delete-buffer -b 1       # 删除 buffer_1
```

## mouse-mode

```
:set -g mouse on           # 打开鼠标模式
```

## References

- https://gist.github.com/MohamedAlaa/2961058
- https://tmuxcheatsheet.com/
- 所有的快捷键都有对应的 command, 参考:
	- http://man.openbsd.org/OpenBSD-current/man1/tmux.1
- 可以通过 $HOME/.tmux.conf 更改配置, 参考一些比较好的 tmux 配置:
	- https://github.com/gpakosz/.tmux
- [Tmux 配置：打造最适合自己的终端复用工具 - zuorn - 博客园](https://www.cnblogs.com/zuoruining/p/11074367.html)

## 配置文件

```.tmux.conf
# 设置前缀键为 Ctrl+a
set-option -g set-titles-string '#h - tmux (#S)'

# 状态栏内容
set-option -g status-left '[#S]'
set-option -g status-right '[#I:#P] | %a %Y-%m-%d %H:%M'

# 设置默认命令为 zsh
set-option -g default-command "zsh"

# 更换左右窗口快捷键
bind-key -r h select-pane -L
bind-key -r j select-pane -D
bind-key -r k select-pane -U
bind-key -r l select-pane -R

# 快速切换窗口
bind -r C-h select-window -p
bind -r C-l select-window -n

# 分离 / 重新连接会话
bind d detach
bind C-r source-file ~/.tmux.conf \; display "配置已重新加载！"

# 连接已有会话
bind C-c new-window -c '#{pane_current_path}'

# 切换分屏
bind \\ split-window -v
bind-key v split-window -h
bind-key s split-window -v

# 复制模式
bind-key [ copy-mode
bind-key ] paste-buffer

# 设置默认分屏的方向
bind-key '"' split-window -h
bind-key % split-window -v

# 设置默认的窗口标题
set-option -g set-titles on

# 窗口永久关闭
bind-key & confirm-before -p "是否杀死窗口 #W? (y/n)" kill-window

# 复制模式下方便的选词选段
bind-key -T copy-mode-vi 'y' send -X copy-pipe-and-cancel "xclip -i -f -selection primary | xclip -i -selection clipboard"
unbind -T copy-mode-vi Enter
bind-key -T copy-mode-vi MouseDragEnd1Pane send -X copy-pipe-and-cancel "xclip -i -f -selection primary | xclip -i -selection clipboard"

# 设置其他快捷键
bind-key M-1 select-window -t :1
bind-key M-2 select-window -t :2
bind-key M-3 select-window -t :3
bind-key M-4 select-window -t :4
bind-key M-5 select-window -t :5
bind-key M-6 select-window -t :6
bind-key M-7 select-window -t :7
bind-key M-8 select-window -t :8
bind-key M-9 select-window -t :9
bind-key M-0 select-window -t :10

# 禁用警告音
set -g bell-action none
```
