---
title: obsidian 配置
tags: [Environment, Obsidian]
categories: 
date: 2024-12-22T18:41:30+08:00
modify: 2024-12-22T18:41:30+08:00
dir: 
share: false
cdate: 2024-12-22
mdate: 2024-12-22
---

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
	- 这个插件可以让你直接通过字母组合激活关键词，来加快 $\displaystyle \LaTeX$ 速度。
	- 比如：输入 `mk` 就可以自动替换为 ` $\displaystyle $ `
- LaTex-like Theorem & Equation Referencer
	- 提供公式环境和自动为公式编号，我感觉不是很有用
	- 需要 MathLinks 前置

??? notes
	如果你的 $\displaystyle \LaTeX$ 书写速度比较慢，可以尝试使用 ocr 软件，比如 simpleTex，但是这个只有 Windows 平台支持。对于 Linux，我暂时还没有比较好的软件。

### 2.2 编辑增强

- Easy Typing
	- 可以自动补全一些，比如括号，以及自动在中文和英文之间空格，很有用
- Linter
	- 可以自动格式化，很强的插件。可以自动生成 yaml，格式化空行空格，标题等
- Remember cursor position
	- 记住 cursor 的位置，可以在下一次打开这个文件的时候跳转。但我觉得其实不是很好用，在你有同步的时候。因为这样子，就会不停的冲突，除非你把它加入 .gitignore 或者其他。
- PDF++
	- 可以批注 PDF，很强。但是我不喜欢，不要尝试把 obsidian 变成 all in one。PDF 应该用别的软件来操作。
- Code Styler
	- 提供代码高亮和不同形式的代码块，我不喜欢，没必要搞个插件，用 CSS 就可以解决。
- Number Headings
	- 自动为标题编号，也可以自动生成目录。
	- 曾经我觉得编号很重要，但是后来感觉不如让平台自动支持悬浮目录更舒适。
- Outliner
	- 更好的列表支持，很好用。
- Completr
	- 自动补全，有一点用。
- Mind map
	- 绘制思维导图，感觉没必要，而且画出来的不是矢量图，不好用。
- Excalidraw
	- 好用，但是我不是很熟练。我还没有到需要大量画图的阶段。
- dataview
	- 可以用来统计等，其实感觉跟 excel 差不多。
	- 很强，但是学习成本比较高，建议 copy。

### 2.3 图片

- Paste image rename
	- 自动为复制的图片重命名，好用
- Auto Link Title
	- 自动获取链接的名字，好用
- Image auto upload Plugin
	- 自动上传图片，结合图床使用，好用
	- 搭配 Picgo + GitHub 使用
- Image toolkit
	- 可以放大图片，好用

对于图片，一般有两种方案：

1. 用图床，方便部署和管理
2. 用本地附件文件夹，隐私好，不用怕图床坏掉，部署的时候有点麻烦。

### 2.4 同步备份

- Git
	- 好用
- Remotely Save
	- 不太好用，同时，其实我并没有很多需要用移动设备，比如 iPads，手机写 obsidian 的需求，电脑段用 git 同步也不是不行。

### 2.5 日程

- Calendar
	- 好用
- Periodic Notes
	- 好用，相当于调用模板的插件
- Day Planner
	- 还行，可以可视化时间轴。但是我现在记录时间还是用时间日志，感觉还是把功能分开更好的发挥每个软件的优势。
- Wakatime
	- 记录使用 obsidian 的时间

### 2.6 部署

- Envelope
	- 好用，可以自动部署到 GitHub 仓库，同时它最大的功能是可以自动更改图片，双链变成一般格式，以及自动渲染 dataview。
	- 特别支持的框架有 Hugo，Mkdocs 等

### 2.7 标签

- TagFolder
	- 好用，支持可视化 tag 管理的文件，彻底替换用树形文件夹。
- Tag Wrangler
	- 好用，可以统一重命名管理 tag，唯一的缺点是不能删除 tag，不过其实可以用一个没用的 tag 来当回收站，然后重命名过去。

### 2.8 仍在探索

- kanban
- zotero 和 obsidian 结合使用

### 2.9 我现在在使用的插件


```
"obsidian-auto-link-title",
"obsidian-latex-suite",
"number-headings-obsidian",
"mathlinks",
"obsidian-outliner",
"obsidian-completr",
"calendar",
"periodic-notes",
"obsidian-wakatime",
"obsidian-image-auto-upload-plugin",
"obsidian-paste-image-rename",
"dataview",
"obsidian-export-image",
"obsidian-day-planner",
"templater-obsidian",
"obsidian-git",
"easy-typing-obsidian",
"obsidian-linter",
"obsidian-style-settings",
"obsidian-image-toolkit",
"tag-wrangler",
"obsidian-tagfolder"
```


## 我的模板

需要安装 dataview + periodic notes 插件。

- 日记主要是使用了 periodic notees 进行日记的初始化，自动填入一些 yaml 信息。同时对于 TODO 以及当天创建和修改的文件进行检索（其实我感觉这个功能不是很有用，不过在每天总结的时候还是有点用的）。
- 周结就没有什么了，一些初始化。不过这个 Links 可以自动收纳一个星期日记中的所有 Links，方便日后查找。

!!! note
    由于 markdown 代码块嵌套不太行，所以要手动修复。注意修复 '' 带来的代码块问题, 记得补全。

=== "daily"
    ??? note
        ```
		---
		title: "{{date}}"
		tags:
		  - " #日记 "
		categories: dairy
		date: " {{ date:YYYY-MM-DDTHH:mm:ss+08:00 }} "
		modify: " {{ date:YYYY-MM-DDTHH:mm:ss+08:00 }} "
		dir: dairy
		share: false
		cdate: " {{ date:YYYY-MM-DD }} "
		mdate: " {{ date:YYYY-MM-DD }} "
		---

		# {{date}}
		
		## Daily Plan
		
		### Morning
		
		#### Plan
		
		### Afternoon
		
		#### Plan
		
		### Night
		
		#### Plan
		
		## NOTES
		
		```dataview
		LIST FROM "" 
		WHERE cdate = this.cdate
		  Or mdate = this.mdate
		``
		
		## LINKS
		
		## TODOs
		
		```dataview
		TASK FROM "dairy"
		WHERE !completed
		  AND mdate >= (this.mdate - dur(7 days))
		  AND mdate <= this.mdate
		SORT file.cday DESC
		``
		
		## THOUGHTS

        ```
=== "weekly"
    ??? note
        ```
		 ---
		title: " {{date}} "
		tags:
		  - " #周记 "
		categories: dairy
		date: " {{ date:YYYY-MM-DDTHH:mm:ss+08:00 }} "
		modify: " {{ date:YYYY-MM-DDTHH:mm:ss+08:00 }} "
		dir: dairy
		share: false
		cdate: " {{ date:YYYY-MM-DD }} "
		mdate: " {{ date:YYYY-MM-DD }} "
		---

		# {{date:YYYY}} -W {{date:WW}} - {{date:MM}}
		
		## Review
		
		## Next Week Plan
		
		## Time Line
		
		## THOUGHTS
		
		## LINKS
		
		```dataviewjs
		// Configuration for collecting LINKS sections from daily notes
		const tars = {
		  'LINKS': 2,  // Collect second-level LINKS headings
		}
		
		await dv.view('zob_config/js/dv-检索', {
		  // Get only daily notes from dairy folder
		  files: dv.pages('"dairy"')
		    .where(p => {
		      // Extract the week number from the current file name (weekly note)
		      const weekMatch = dv.current().file.name.match(/(\d{4})-W(\d{1,2})/);
		      if (!weekMatch) return false;
		      
		      const [_, weekYear, weekNum] = weekMatch;
		      
		      // Extract date components from daily note name (2024-49-12-08-7 format)
		      const dateMatch = p.file.name.match(/(\d{4})-(\d{1,2})-(\d{2})-(\d{2})-(\d{1})/);
		      if (!dateMatch) return false;
		      
		      const [__, year, week, month, day] = dateMatch;
		      
		      // Check if the daily note belongs to the same week and year
		      return year === weekYear && week === weekNum;
		    })
		    .sort(p => {
		      // Create sortable date string from daily note format
		      const [_, year, week, month, day] = p.file.name.match(/^(\d{4})-(\d{1,2})-(\d{2})-(\d{2})-(\d{1})$/);
		      // Sort by YYYYMMDD format (descending)
		      return -1 * parseInt(`${year}${month.padStart(2, '0')}${day.padStart(2, '0')}`);
		    }),
		
		  kwd: false,      // Don't filter by keywords
		  showHead: false, // Don't include heading in output
		  tars,           // Target sections to collect (LINKS)
		  obsidian,       // Pass obsidian object
		  scale: 0.8,     // Scale of rendered content
		  
		  // List item configuration
		  li: ([p, li]) => {
		    const [_, year, week, month, day] = p.file.name.match(/^(\d{4})-(\d{1,2})-(\d{2})-(\d{2})-(\d{1})$/);
		    const formattedDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
		    // Create a header with date and file link, followed by the content
		    return dv.paragraph(`### ${formattedDate} [[${p.file.path}|${p.file.name}]]\n${li}`);
		  },
		});
		``
        ```

## 3 相关链接

- [PKMer\_PKMer](https://pkmer.cn/)
- [Obsidian 中文论坛 - Obsidian 知识管理 笔记](https://forum-zh.obsidian.md/)
- [Obsidian文档咖啡豆版 | Obsidian Docs by CoffeeBean](https://coffeetea.top/)
- [zhuanlan.zhihu.com/p/619960525](https://zhuanlan.zhihu.com/p/619960525)
