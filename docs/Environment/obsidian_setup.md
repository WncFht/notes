# obsidian 配置

???+note
    如果懒得搞，可以直接 clone 我的配置，放到 .obsidian 文件里。
    这是[配置文件](https://github.com/WncFht/.obsidian)。

## 1 使用语言

- 主要是 Markdown
- 配置插件也会涉及一些 javascript

## 2 插件

### 2.1 $\displaystyle \LaTeX$ 

- Latex Suite
- LaTex-like Theorem & Equation Referencer
- MathLinks  

搭配 simpleTex 使用

### 2.2 编辑增强

- Easy Typing
- Linter
- Remember cursor position
- PDF++
- Code Styler
- Number Headings
- Outliner
- Completr
- Mind map
- Excalidraw

### 2.3 图片

- Paste image rename
- Auto Link Title
- Image auto upload Plugin

搭配 Picgo + GitHub 使用

### 2.4 同步备份

- Git
- Remotely Save

### 2.5 日程

- Calendar
- Periodic Notes
- Tasks Progress Bar
- Tasks
- Tasks Calendar Wrapper

### 2.6 仍在探索

- Local REST API + 简约
- RSS Reader

## 我的模板
需要安装 dataview + periodic notes 插件。
!!! note
    由于 markdown 代码块嵌套不太行，所以要手动修复。注意修复 '' 带来的代码块问题

=== "daily"
    ??? note
        ```
        # {{date:YYYY}}-{{date:WW}}-{{date:DD}}-{{date:HH}}-{{date:d}}

        ## 1. 计划

        ### 🌅 早晨

        #### 计划 

        #### 复盘 

        ---

        ### ☀️ 中午

        #### 计划 

        #### 复盘 

        ---

        ### 🌇 晚上

        #### 计划

        #### 复盘 

        ---

        ## 2. 笔记索引

        ``dataview
        LIST FROM ""
        WHERE file.cday = date("{{date:YYYY}}-{{date:MM}}-{{date:DD}}")
        ``

        ---

        ## 3. 资源与链接

        ---

        ## 4. 未完成的任务

        ``dataview
        TASK FROM "dairy"
        WHERE !completed
        AND file.cday >= (this.file.cday - dur(7 days))
        AND file.cday <= this.file.cday
        SORT file.cday DESC
        ``

        ---

        ## 5. 反思

        ```
=== "weekly"
    ??? note
        ```
        # {{date:YYYY}}-W{{date:WW}}-{{date:DD}}

        ## 1. 本周复盘

        ---

        ## 2. 下周计划

        ```
## 3 相关链接

- [PKMer\_PKMer](https://pkmer.cn/)
- [Obsidian 中文论坛 - Obsidian 知识管理 笔记](https://forum-zh.obsidian.md/)
- [Obsidian文档咖啡豆版 | Obsidian Docs by CoffeeBean](https://coffeetea.top/)
- [zhuanlan.zhihu.com/p/619960525](https://zhuanlan.zhihu.com/p/619960525)
