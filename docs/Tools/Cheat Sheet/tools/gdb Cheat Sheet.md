---
title: gdb Cheat Sheet
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

# gdb Cheat Sheet

pwngdb

```
cd ~/
git clone https://github.com/scwuaptx/Pwngdb.git 
cp ~/Pwngdb/.gdbinit ~/
```

pwndbg

```
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh
```

联合使用

```
vim ~/.gdbinit
注释掉第一行 然后在第二行写入
source ~/pwndbg/gdbinit.py
```

```
git clone https://github.com/longld/peda.git ~/peda
sudo pacman -S python-six
```

## 启动 GDB

```
gdb object                # 正常启动，加载可执行
gdb object core           # 对可执行 + core 文件进行调试
gdb object pid            # 对正在执行的进程进行调试
gdb                       # 正常启动，启动后需要 file 命令手动加载
gdb -tui                  # 启用 gdb 的文本界面（或 ctrl-x ctrl-a 更换 CLI/TUI）
```

## 帮助信息

```
help                      # 列出命令分类
help running              # 查看某个类别的帮助信息
help run                  # 查看命令 run 的帮助
help info                 # 列出查看程序运行状态相关的命令
help info line            # 列出具体的一个运行状态命令的帮助
help show                 # 列出 GDB 状态相关的命令
help show commands        # 列出 show 命令的帮助
```

## 断点

```
break main                # 对函数 main 设置一个断点，可简写为 b main
break 101                 # 对源代码的行号设置断点，可简写为 b 101
break basic.c:101         # 对源代码和行号设置断点
break basic.c:foo         # 对源代码和函数名设置断点
break *0x00400448         # 对内存地址 0x00400448 设置断点
info breakpoints          # 列出当前的所有断点信息，可简写为 info break
delete 1                  # 按编号删除一个断点
delete                    # 删除所有断点
clear                     # 删除在当前行的断点
clear function            # 删除函数断点
clear line                # 删除行号断点
clear basic.c:101         # 删除文件名和行号的断点
clear basic.c:main        # 删除文件名和函数名的断点
clear *0x00400448         # 删除内存地址的断点
disable 2                 # 禁用某断点，但是不删除
enable 2                  # 允许某个之前被禁用的断点，让它生效
rbreak {regexpr}          # 匹配正则的函数前断点，如 ex_* 将断点 ex_ 开头的函数
tbreak function|line      # 临时断点
hbreak function|line      # 硬件断点
ignore {id} {count}       # 忽略某断点 N-1 次
condition {id} {expr}     # 条件断点，只有在条件生效时才发生
condition 2 i == 20       # 2号断点只有在 i == 20 条件为真时才生效
watch {expr}              # 对变量设置监视点
info watchpoints          # 显示所有观察点
catch exec                # 断点在exec事件，即子进程的入口地址
```

| 命令                           | 作用                       |
| ---------------------------- | ------------------------ |
| break [file]:function        | 在文件file的function函数入口设置断点 |
| break [file]:line            | 在文件file的第line行设置断点       |
| info breakpoints             | 查看断点列表                   |
| break [+-]offset             | 在当前位置偏移量为[+-]offset处设置断点 |
| break *addr                  | 在地址addr处设置断点             |
| break ... if expr            | 设置条件断点，仅仅在条件满足时          |
| ignore n count               | 接下来对于编号为n的断点忽略count次     |
| clear                        | 删除所有断点                   |
| clear function               | 删除所有位于function内的断点       |
| delete n                     | 删除指定编号的断点                |
| enable n                     | 启用指定编号的断点                |
| disable n                    | 禁用指定编号的断点                |
| save breakpoints file        | 保存断点信息到指定文件              |
| source file                  | 导入文件中保存的断点信息             |
| break                        | 在下一个指令处设置断点              |
| clear [file:]line            | 删除第line行的断点              |
| watch variable               | 设置变量数据断点                 |
| watch var1 + var2            | 设置表达式数据断点                |
| rwatch variable              | 设置读断点，仅支持硬件实现            |
| awatch variable              | 设置读写断点，仅支持硬件实现           |
| info watchpoints             | 查看数据断点列表                 |
| set can-use-hw-watchpoints 0 | 强制基于软件方式实现               |
| catch fork                   | 程序调用fork时中断              |
| tcatch fork                  | 设置的断点只触发一次，之后被自动删除       |
| catch syscall ptrace         | 为ptrace系统调用设置断点          |

### 为了解决局部变量断点失效

| 命令                      | 作用                   |
| ----------------------- | -------------------- |
| print &variable         | 查看变量的内存地址            |
| watch *(type *)address  | 通过内存地址间接设置断点         |
| watch -l variable       | 指定location参数         |
| watch variable thread 1 | 仅编号为1的线程修改变量var值时会中断 |

## 运行程序

```
run                       # 运行程序
run {args}                # 以某参数运行程序
run < file                # 以某文件为标准输入运行程序
run < <(cmd)              # 以某命令的输出作为标准输入运行程序
run <<< $(cmd)            # 以某命令的输出作为标准输入运行程序
set args {args} ...       # 设置运行的参数
show args                 # 显示当前的运行参数
continue                  # 继续运行，可简写为 c 或 cont
step                      # 单步进入，碰到函数会进去（Step in）
step {count}              # 单步多少次
next                      # 单步跳过，碰到函数不会进入（Step Over）
next {count}              # 单步多少次
finish                    # 运行到当前函数结束（Step Out）
until                     # 持续执行直到代码行号大于当前行号（跳出循环）
until {line}              # 持续执行直到执行到某行
CTRL+C                    # 发送 SIGINT 信号，中止当前运行的程序
attach {process-id}       # 链接上当前正在运行的进程，开始调试
detach                    # 断开进程链接
kill                      # 杀死当前运行的函数
```

## 栈帧

```
bt [n]                    # 打印 backtrace （命令 where 是 bt 的别名）
frame [n]                 # 显示当前运行的栈帧
up                        # 向上移动栈帧（向着 main 函数）
down                      # 向下移动栈帧（远离 main 函数）
info locals               # 打印帧内的相关变量
info args                 # 打印函数的参数
```

## 代码浏览

```
list 101                  # 显示第 101 行周围 10行代码
list 1,10                 # 显示 1 到 10 行代码
list main                 # 显示函数周围代码
list basic.c:main         # 显示另外一个源代码文件的函数周围代码
list -                    # 重复之前 10 行代码
list *0x22e4              # 显示特定地址的代码
cd dir                    # 切换当前目录
pwd                       # 显示当前目录
search {regexpr}          # 向前进行正则搜索
reverse-search {regexp}   # 向后进行正则搜索
dir {dirname}             # 增加源代码搜索路径
dir                       # 复位源代码搜索路径（清空）
show directories          # 显示源代码路径
```

## 浏览数据

```
print {expression}        # 打印表达式，并且增加到打印历史
print /x {expression}     # 十六进制输出，print 可以简写为 p
print array[i]@count      # 打印数组范围
print $                   # 打印之前的变量
print *$->next            # 打印 list
print $1                  # 输出打印历史里第一条
print ::gx                # 将变量可视范围（scope）设置为全局
print 'basic.c'::gx       # 打印某源代码里的全局变量，(gdb 4.6)
print /x &main            # 打印函数地址
x *0x11223344             # 显示给定地址的内存数据
x /nfu {address}          # 打印内存数据，n是多少个，f是格式，u是单位大小
x /10xb *0x11223344       # 按十六进制打印内存地址 0x11223344 处的十个字节
x/x &gx                   # 按十六进制打印变量 gx，x和斜杆后参数可以连写
x/4wx &main               # 按十六进制打印位于 main 函数开头的四个 long 
x/gf &gd1                 # 打印 double 类型
help x                    # 查看关于 x 命令的帮助
info locals               # 打印本地局部变量
info functions {regexp}   # 打印函数名称
info variables {regexp}   # 打印全局变量名称
ptype name                # 查看类型定义，比如 ptype FILE，查看 FILE 结构体定义
whatis {expression}       # 查看表达式的类型
set var = {expression}    # 变量赋值
display {expression}      # 在单步指令后查看某表达式的值
undisplay                 # 删除单步后对某些值的监控
info display              # 显示监视的表达式
show values               # 查看记录到打印历史中的变量的值 (gdb 4.0)
info history              # 查看打印历史的帮助 (gdb 3.5)
```

## 目标文件操作

```
file {object}             # 加载新的可执行文件供调试
file                      # 放弃可执行和符号表信息
symbol-file {object}      # 仅加载符号表
exec-file {object}        # 指定用于调试的可执行文件（非符号表）
core-file {core}          # 加载 core 用于分析
```

## 信号控制

```
info signals              # 打印信号设置
handle {signo} {actions}  # 设置信号的调试行为
handle INT print          # 信号发生时打印信息
handle INT noprint        # 信号发生时不打印信息
handle INT stop           # 信号发生时中止被调试程序
handle INT nostop         # 信号发生时不中止被调试程序
handle INT pass           # 调试器接获信号，不让程序知道
handle INT nopass         # 调试器不接获信号
signal signo              # 继续并将信号转移给程序
signal 0                  # 继续但不把信号给程序
```

## 线程调试

```
info threads              # 查看当前线程和 id
thread {id}               # 切换当前调试线程为指定 id 的线程
break {line} thread all   # 所有线程在指定行号处设置断点
thread apply {id..} cmd   # 指定多个线程共同执行 gdb 命令
thread apply all cmd      # 所有线程共同执行 gdb 命令
set schedule-locking ?    # 调试一个线程时，其他线程是否执行，off|on|step
set non-stop on/off       # 调试一个线程时，其他线程是否运行
set pagination on/off     # 调试一个线程时，分页是否停止
set target-async on/off   # 同步或者异步调试，是否等待线程中止的信息
```

| 命令                         | 作用                                  |
| -------------------------- | ----------------------------------- |
| info threads               | 查看线程列表                              |
| print $_thread             | 显示当前正在调试的线程编号                       |
| set scheduler-locking on   | 调试一个线程时，其他线程暂停执行                    |
| set scheduler-locking off  | 调试一个线程时，其他线程同步执行                    |
| set scheduler-locking step | 仅用step调试线程时其他线程不执行，用其他命令如next调试时仍执行 |

## 进程调试

```
info inferiors                       # 查看当前进程和 id
inferior {id}                        # 切换某个进程
kill inferior {id...}                # 杀死某个进程
set detach-on-fork on/off            # 设置当进程调用fork时gdb是否同时调试父子进程
set follow-fork-mode parent/child    # 设置当进程调用fork时是否进入子进程
```

| 命令                          | 作用               |
| --------------------------- | ---------------- |
| info inferiors              | 查看进程列表           |
| attach pid                  | 绑定进程id           |
| inferior num                | 切换到指定进程上进行调试     |
| print $_exitcode            | 显示程序退出时的返回值      |
| set follow-fork-mode child  | 追踪子进程            |
| set follow-fork-mode parent | 追踪父进程            |
| set detach-on-fork on       | fork调用时只追踪其中一个进程 |
| set detach-on-fork off      | fork调用时会同时追踪父子进程 |

## 汇编调试

```
info registers            # 打印普通寄存器
info all-registers        # 打印所有寄存器
print/x $pc               # 打印单个寄存器
stepi                     # 指令级别单步进入，可以简写为 si
nexti                     # 指令级别单步跳过，可以简写为 ni
display/i $pc             # 监控寄存器（每条单步完以后会自动打印值）
x/x &gx                   # 十六进制打印变量
info line 22              # 打印行号为 22 的内存地址信息
info line *0x2c4e         # 打印给定内存地址对应的源代码和行号信息
disassemble {addr}        # 对地址进行反汇编，比如 disassemble 0x2c4e
```

## 历史信息

```
show commands             # 显示历史命令 (gdb 4.0)
info editing              # 显示历史命令 (gdb 3.5)
ESC-CTRL-J                # 切换到 Vi 命令行编辑模式
set history expansion on  # 允许类 c-shell 的历史
break class::member       # 在类成员处设置断点
list class:member         # 显示类成员代码
ptype class               # 查看类包含的成员
print *this               # 查看 this 指针
```

## 其他命令

```
define command ... end    # 定义用户命令
<return>                  # 直接按回车执行上一条指令
shell {command} [args]    # 执行 shell 命令
source {file}             # 从文件加载 gdb 命令
quit                      # 退出 gdb
```

##### 打印字符串

使用`x/s`命令打印`ASCII`字符串，如果是宽字符字符串，需要先看宽字符的长度 `print sizeof(str)`。

如果长度为`2`，则使用`x/hs`打印；如果长度为`4`，则使用`x/ws`打印。

|命令|作用|
|---|---|
|x/s str|打印字符串|
|set print elements 0|打印不限制字符串长度/或不限制数组长度|
|call printf("%s\n",xxx)|这时打印出的字符串不会含有多余的转义符|
|printf "%s\n",xxx|同上|

##### 打印数组

|命令|作用|
|---|---|
|print *array@10|打印从数组开头连续10个元素的值|
|print array[60]@10|打印array数组下标从60开始的10个元素，即第60~69个元素|
|set print array-indexes on|打印数组元素时，同时打印数组的下标|

##### 打印指针

|命令|作用|
|---|---|
|print ptr|查看该指针指向的类型及指针地址|
|print *(struct xxx *)ptr|查看指向的结构体的内容|

##### 打印指定内存地址的值

使用`x`命令来打印内存的值，格式为`x/nfu addr`，以`f`格式打印从`addr`开始的`n`个长度单元为`u`的内存值。

- `n`：输出单元的个数
- `f`：输出格式，如`x`表示以`16`进制输出，`o`表示以`8`进制输出，默认为`x`
- `u`：一个单元的长度，`b`表示`1`个`byte`，`h`表示`2`个`byte`（`half word`），`w`表示`4`个`byte`，`g`表示`8`个`byte`（`giant word`）

|命令|作用|
|---|---|
|x/8xb array|以16进制打印数组array的前8个byte的值|
|x/8xw array|以16进制打印数组array的前16个word的值|

##### 打印局部变量

|命令|作用|
|---|---|
|info locals|打印当前函数局部变量的值|
|backtrace full|打印当前栈帧各个函数的局部变量值，命令可缩写为bt|
|bt full n|从内到外显示n个栈帧及其局部变量|
|bt full -n|从外向内显示n个栈帧及其局部变量|

##### 打印结构体

|命令|作用|
|---|---|
|set print pretty on|每行只显示结构体的一名成员|
|set print null-stop|不显示'\000'这种|

### 函数跳转

|命令|作用|
|---|---|
|set step-mode on|不跳过不含调试信息的函数，可以显示和调试汇编代码|
|finish|执行完当前函数并打印返回值，然后触发中断|
|return 0|不再执行后面的指令，直接返回，可以指定返回值|
|call printf("%s\n", str)|调用printf函数，打印字符串(可以使用call或者print调用函数)|
|print func()|调用func函数(可以使用call或者print调用函数)|
|set var variable=xxx|设置变量variable的值为xxx|
|set {type}address = xxx|给存储地址为address，类型为type的变量赋值|
|info frame|显示函数堆栈的信息（堆栈帧地址、指令寄存器的值等）|

### 其它

#### 图形化

tui为`terminal user interface`的缩写，在启动时候指定`-tui`参数，或者调试时使用`ctrl+x+a`组合键，可进入或退出图形化界面。

|命令|含义|
|---|---|
|layout src|显示源码窗口|
|layout asm|显示汇编窗口|
|layout split|显示源码 + 汇编窗口|
|layout regs|显示寄存器 + 源码或汇编窗口|
|winheight src +5|源码窗口高度增加5行|
|winheight asm -5|汇编窗口高度减小5行|
|winheight cmd +5|控制台窗口高度增加5行|
|winheight regs -5|寄存器窗口高度减小5行|

#### 汇编

|命令|含义|
|---|---|
|disassemble function|查看函数的汇编代码|
|disassemble /mr function|同时比较函数源代码和汇编代码|

#### 调试和保存core文件

| 命令                  | 含义                      |
| ------------------- | ----------------------- |
| file exec_file  *#* | 加载可执行文件的符号表信息           |
| core core_file      | 加载core-dump文件           |
| gcore core_file     | 生成core-dump文件，记录当前进程的状态 |

## GDB 前端

```
gdb-tui                   使用 gdb -tui 启动（或 ctrl-x ctrl-a 更换 CLI/TUI）
cgdb                      http://cgdb.github.io/
emacs                     http://gnu.org/software/emacs
gdbgui                    https://github.com/cs01/gdbgui
vimspector                https://github.com/puremourning/vimspector
termdebug                 https://github.com/vim/vim

GDB 图形化前端评测        http://www.skywind.me/blog/archives/2036
```

## References

- https://sourceware.org/gdb/current/onlinedocs/gdb/
- https://kapeli.com/cheat_sheets/GDB.docset/Contents/Resources/Documents/index
- http://www.yolinux.com/TUTORIALS/GDB-Commands.html
- https://gist.github.com/rkubik/b96c23bd8ed58333de37f2b8cd052c30
- http://security.cs.pub.ro/hexcellents/wiki/kb/toolset/gdb
- [ ] [GDB调试-从入门实践到原理](https://mp.weixin.qq.com/s/XxPIfrQ3E0GR88UsmQNggg)

---

## gdb 命令

### 运行

- `(gdb) run` 直接运行 (r)
- `(gdb) continue` 继续运行 (c)
- `(gdb) step` 运行到下一条源码 (s)
- `(gdb) stepi` 运行到下一条指令 (si)
- `(gdb) next` 单步运行，跳过函数 (n)
- `(gdb) finish` 运行完当前函数 (fin)
- `(gdb) attach <pid>` 连接程序
- `(gdb) detach` 从当前程序断连
- `(gdb) target remote localhost:1234` 连接 qemu

### 断点

- `(gdb) break main` 断在符号处 (b)
- `(gdb) break *0x....` 断在地址
- `(gdb) info breakpoints` 查看断点及状态 (i b)
- `(gdb) delete / clear` 清除所有断点 (d/cl)
- `(gdb) delete <breakpoint#>` 删除某一断点（从 i b 得来断点号）
- `(gdb) clear ...` 清除某一符号、地址处的断点
- `(gdb) disable <breakpoint#>` 禁用某一断点
- `(gdb) enable <breakpoint#>` 启用某一断点
- `(gdb) watch ...` 在某处增加观察点，delete、enable、disable 与断点共用
- `(gdb) break/watch <where> if <condition>` 如果条件满足则断
- `(gdb) condition <breakpoint#> <condition>` 更改条件

### 调用栈

- `(gdb) backtrace` 查看调用栈 (bt)
- `(gdb) frame` 查看当前帧栈
- `(gdb) up/down` 移动当前帧栈（向 main / 远离 main）
- `(gdb) info locals` 查看当前帧栈变量
- `(gdb) info args` 查看函数参数

### 查看寄存器 / 变量 / 内存

- `(gdb) print/format <what>`
  - `format`
    - a: pointer
    - c: int -> char
    - d: signed decimal
    - f: floating point number
    - o: int -> octal
    - s: treat as string
    - t: int -> bin
    - u: unsigned decimal
    - x: int -> hex
  - `<what>`
    - 可以是类 C 表达式
    - 可以是 file\_name:: variable\_name
    - 可以是 function:: variable\_name
    - 可以是 {type}address
    - 可以是 $register
- `(gdb) display/format <what>`
- `(gdb) undisplay <display#>`
- `(gdb) enable display <display#>`
- `(gdb) disable display <display#>`
- `(gdb) x/nfu <address>` 显示内存
  - n 表示查找、打印几个单位
  - f 表示 format，在前面写了
  - u 表示单位：b 一字节、h 两字节、w 四字节、g 八字节
- `(gdb) info register` 查看所有寄存器 (i r)
- `(gdb) info register <register>` 查看某一寄存器

## gdb 插件

### gdb-peda

每条指令带寄存器、汇编、内存数据回显

```plain&#x20;text
$ git clone https://github.com/longld/peda.git ~/peda
$ echo "source ~/peda/peda.py" >> ~/.gdbinit
```
