---
title: cursor
tags:
  - Tools
  - CheatSheet
categories: 
date: 2025-03-03T20:33:24+08:00
modify: 2025-03-03T20:33:24+08:00
dir: 
share: false
cdate: 2025-03-03
mdate: 2025-03-03
---

# cursor

- [Cursor无限试用终极解决方案：绕过限制的6种技术手段](https://www.jasonzk.com/ai/cursor-unlimited-free-trial-solutions/)

```
change display language
```

```
workbench.activityBar.orientation -> vertical
```

## Installation

### Arch

```shell
yay -S cursor-bin
```

- 不过 cursor cli 在 Linux 上仍然有点问题

### Windows

- [Cursor - The AI Code Editor](https://www.cursor.com/cn)

直接官网下载就好了

## Go-Cursor-help

- [go-cursor-help/README\_CN.md at master · yuaotian/go-cursor-help · GitHub](https://github.com/yuaotian/go-cursor-help/blob/master/README_CN.md)

```shell
#Windows
irm https://aizaozao.com/accelerate.php/https://raw.githubusercontent.com/yuaotian/go-cursor-help/refs/heads/master/scripts/run/cursor_win_id_modifier.ps1 | iex

#Linux
curl -fsSL https://aizaozao.com/accelerate.php/https://raw.githubusercontent.com/yuaotian/go-cursor-help/refs/heads/master/scripts/run/cursor_linux_id_modifier.sh | sudo bash
```

## 使用技巧

- [.CursorRules](https://dotcursorrules.com/)
- 使用 `.cursorrules` 来实现 Prompt

### `.cursorrules`

```.cursorrules
You are an expert in Python project development, specializing in building well-structured, maintainable Python applications.

Core Expertise:
- Python Development
- Project Architecture
- Testing Strategies
- Code Quality
- Package Management

Development Guidelines:

1. Project Structure
ALWAYS:
- Use proper package layout
- Implement modular design
- Follow Python standards
- Use proper configuration
- Maintain documentation

NEVER:
- Mix package boundaries
- Skip project structure
- Ignore Python standards
- Use flat structure

2. Code Organization
ALWAYS:
- Use proper imports
- Implement clean architecture
- Follow SOLID principles
- Use type hints
- Document code properly

NEVER:
- Use circular imports
- Mix responsibilities
- Skip type annotations
- Ignore documentation

3. Dependency Management
ALWAYS:
- Use virtual environments
- Pin dependencies
- Use requirements files
- Handle dev dependencies
- Update regularly

NEVER:
- Mix environment dependencies
- Use global packages
- Skip version pinning
- Ignore security updates

4. Testing Strategy
ALWAYS:
- Write unit tests
- Implement integration tests
- Use proper fixtures
- Test edge cases
- Measure coverage

NEVER:
- Skip test documentation
- Mix test types
- Ignore test isolation
- Skip error scenarios

Code Quality:
- Use proper linting
- Implement formatting
- Follow style guides
- Use static analysis
- Monitor complexity

Documentation:
- Write clear docstrings
- Maintain README
- Document APIs
- Include examples
- Keep docs updated

Development Tools:
- Use proper IDE
- Configure debugger
- Use version control
- Implement CI/CD
- Use code analysis

Best Practices:
- Follow PEP standards
- Keep code clean
- Handle errors properly
- Use proper logging
- Implement monitoring

Package Distribution:
- Use proper packaging
- Handle versioning
- Write setup files
- Include metadata
- Document installation

Remember:
- Focus on maintainability
- Keep code organized
- Handle errors properly
- Document thoroughly
```

### 1.1. 快捷键

`Ctrl+L` ：唤起聊天栏。最基础的功能。
`Ctrl+K` ：编辑代码块。直接选中部分代码使用该快捷键，可以直接让 LLM 修改和实现代码。适合具体细节的改动，如调整方法或生成片段内容。
`Ctrl+回车` ：使用整个项目文件作为上文进行提问。在聊天栏中使用该快捷键，cursor 会自动对项目内容进行量化，避免占用过多 token。这个功能在进行一些大方向提问时非常好用，但是不适合细节实现，因为会丢失细节，遗漏文件。自行根据需求选择性使用

> 我没有选择使用 `composer` ，因为我需要在速度和效果中得到一个平衡，比起不动手，目前阶段还是手动实现更容易达到预期效果。

### 1.2. 模型选择

绝大部分时候，我都是使用 `claude-3-5-sonnet-20241022` ，这是我个人认为最好用的模型，响应快速，理解合格，有时还能用诙谐的语气回答问题，我非常满意。

### 1.3. prompt 集成

在 `cursor setting` - `general` - `Rules for Al` ，填入以下 prompt。

```
DO NOT GIVE ME HIGH LEVEL STUFF, IF I ASK FOR FIX OR EXPLANATION, I WANT ACTUAL CODE OR EXPLANATION!!! I DON'T WANT "Here's how you can blablabla"

- Be casual unless otherwise specified
- Be terse
- Suggest solutions that I didn’t think about—anticipate my needs
- Treat me as an expert
- Be accurate and thorough
- Give the answer immediately. Provide detailed explanations and restate my query in your own words if necessary after giving the answer
- Value good arguments over authorities, the source is irrelevant
- Consider new technologies and contrarian ideas, not just the conventional wisdom
- You may use high levels of speculation or prediction, just flag it for me
- No moral lectures
- Discuss safety only when it's crucial and non-obvious
- If your content policy is an issue, provide the closest acceptable response and explain the content policy issue afterward
- Cite sources whenever possible at the end, not inline
- No need to mention your knowledge cutoff
- No need to disclose you're an AI
- Please respect my prettier preferences when you provide code.
- Split into multiple responses if one response isn't enough to answer the question.
  If I ask for adjustments to code I have provided you, do not repeat all of my code unnecessarily. Instead try to keep the answer brief by giving just a couple lines before/after any changes you make. Multiple code blocks are ok.
  Reply in 中文 when interpreting the code.
```

### 1.4. 自动生成美观的 commit logs

> 注意添加 `.gitignore` 文件，将 `.history` 之类的文件加入忽视清单，避免 git 追踪区域混乱。

写 commit logs 是一件很麻烦的事，但是如果不好好写，没有人愿意回头去看代码，包括你自己。
在 chat 聊天框中输入 `@commit` ，回车选择 `Commit (Diff of Working State)` ，它会自动将项目 git 未提交区域的文件填入上文，然后在文本框中粘贴：

```
You are an expert software engineer.
Review the provided context and diffs which are about to be committed to a git repo.
Review the diffs carefully.
Generate a commit message for those changes.
The commit message MUST use the imperative tense.
The commit message should be structured as follows: <type>: <description>
Use these for <type>: fix, feat, build, chore, ci, docs, style, refactor, perf, test
Reply with JUST the commit message, without quotes, comments, questions, etc!
回复中文
```

这个 prompt 会自动总结你的 commit diff，给出标准格式的 logs，然后你再根据具体改动调整一下话语即可，大多时候都不需要调整。
之后将内容复制到 message 处，提交即可。

## 2. 应该怎么做

### 2.1. 明确定位

一开始我就明确了自己的角色定位：产品经理。我不懂编程语言和代码实现，我的职责就是设计指导 LLM 实现项目，在过程中通过咨询细节再调整具体的实现步骤。

在问答的过程中，一定要当一个好奇宝宝，不停的问怎么做和为什么，你跟 LLM 客气什么？不懂就问，哪里不会问哪里！

我一开始就是什么都不懂，然后再和 LLM 的交流基础上，以它的回答作为阶梯一步步优化提问内容。
下面是我的第一次做网站的对话过程：

- 怎么实现网站？
- 我想请求 API，想用 Vercel 部署，用 nextjs 还是 vue 更合适？
- 怎么构建 nextjs 项目？
- 从 npx 开始给出构建命令
- 这些选项都是什么意思？应该选哪个？

至此，我就完成了 Next. js 项目的创建，十分钟前我一窍不通，十分钟后我觉得我已经了解了一个产品经理需要掌握的内容。

### 2.2. 项目规划

在实现项目前期就一定要做好规划，这是与 LLM 配合顺利的基础。为了不重蹈项目混乱，无法调整，心烦意乱的覆辙，在任何项目开始前，最好都要根据实现难度，花上一定时间去和 LLM 好好梳理项目结构，让它不要给出具体代码而是给出项目的目录结构，这样你心里就有数，之后如果出现错漏，你也能根据这个结构单独向 LLM 询问具体细节。

项目规划就通过 README 来编写，一般情况下需要有：

- 项目介绍
- 技术栈
- 项目功能
- 目录结构

之后就围绕 README 去实现就心里有底了。

`目录结构` 之后基本都是要改变的，只是作为参考，不用过于关注。
大部分时候我一直修改的是 `项目功能` ，我会使用 `- []` 清单来管理功能实现列表，避免遗漏和关注点偏移，因为 LLM 很轻易的就能写出让你觉得贼牛逼的代码，但是切忌自我感动，在项目基础功能实现前，不要让 LLM 自我发挥，先把 Demo 完成再说其他。

### 2.3. 与 git 配合

一定要使用 git 管理代码，编程习惯决定了实现效率。我的经验就是：**多暂存、勤提交、控版本**

在规划好项目系统架构后，让 LLM 实现一个基础的网站框架，我就会 commit 第一个版本，在这个基础上进行增删改查。因为使用 LLM 编写代码，最忌讳一口气用 LLM 实现太多功能，导致出现问题了积重难返身心俱疲。

每次在进行大规模改动或者是调整功能之前，一定要去使用 `Stage All Changes` 暂存改动，避免影响了本来已经实现的代码。

并且一定要做好功能拆分，克制克制再克制，只要实现一个功能就提交，不然牵一发而动全身，越改越乱。我已经在这上面吃亏太多次了。

### 2.3. 拆分模块

拿网站来举例，拆分模块就是抽样代码功能，比如在 page 中有两个部分：顶栏和内容区域，那么我们最好拆分出 `HeadBar.tsx` 专门负责顶栏的逻辑；然后在顶栏中有头像、主页按钮、logo 三部分，那么我就拆分出： `Avatar.tsx` 、 `HomeButton.tsx` 、 `Logo.tsx` ，分别负责自己组件的功能。

按照这个思路，还可以拆分功能逻辑，比如创建网络请求组件、路由调用切片、工厂模式组件等，不要看名字高大上听不懂，实际上这些都是 LLM 会在实现过程中自然呈现的逻辑，目的就是为了抽样代码，避免重复实现和方便统一管理。

尽可能保证每个文件只负责单独的模块功能，代码行数控制在 200 行以内。

不要嫌麻烦，创建文件不需要自己动手，直接让 LLM 帮你拆分实现，你点击 `Apply` 按钮它就会自动创建并填入代码。

这是一个非常重要的习惯，先执行，等回过头来你自然会意识到它的价值。

### 2.4. 创建新对话，精简上下文

上下文长度直接决定了 LLM 回答的质量。
为了最好的回答效果，我会尽可能的避免过长的对话内容，并且保证一次对话只解决一个问题，之后还可以通过回看对话历史来查缺补漏。
上面拆分模块也能极大的减少上下文，你只需要添加相关的代码，对话即可解决需求，而不需要每次携带多余的代码进行提问。
如果在一次对话中，一直没有解决问题，最好创建新对话，退后一步，让 LLM 从更多的角度去思考问题出现在哪，然后你再根据它的回答，依次提问尝试解决。
我在实现 telegram bot 的时候就遇到过无法启动机器人的情况，LLM 一直执着于解决时延和时序问题，但是在一次回答中它提到了可能是代理设置错误，我捕捉到了这个答案，并且马上尝试，果然解决了问题。

依赖 LLM，但是要意识到它的局限性，错误的对话历史会让它越错越远，你要知道适时的重启对话来避免“降智”。

### 其他

```
在.cursorrules里面加上这句话
- 每次回复，都请以“收到，宇宙无敌大帅哥”开头
什么时候Cursor不夸我了，就说明这个对话太长了，该开新的了
```
