# Market Research — AI 智能体（Agent）市场调研技能

> 调研不是填空题。调研是**用公开证据支持决策判断**。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-blue)](https://hermes-agent.nousresearch.com)

**中文** | [English](#english)

---

## 这是什么？

这是一个为 AI 智能体（Agent）设计的**市场调研技能包**。它不是一套提示词模板，而是一个完整的调研方法论，指导 AI 如何像专业咨询分析师一样工作：

- 先校准问题，而不是直接套模板
- 先侦察证据，而不是先写目录
- 区分事实、推断、判断，而不是混为一谈
- 诚实标注"查不到"，而不是假装知道

给 AI Agent 装上这套技能后，它能把"帮我调研一下 XX 行业有没有机会"这种模糊需求，变成一份有证据来源、有置信度标注、有盲区说明的专业调研报告。

## 核心理念：证据驱动，不是模板驱动

传统 AI 调研的问题是：**给个标题就开始编**。看上去章节齐全，实际上每一章都是泛泛而谈。

这个技能的做法是：

```
模糊需求 → 校准决策问题 → 证据侦察 → 选研究路径 → 深挖高价值渠道 → 写报告 → 事实核查 → 交付
```

每一步都卡一个质量门，证据不够就不硬写。

### 5 个关键原则

1. **不校准不调研**：先跟用户确认"你到底要做什么决策"，把模糊需求变成可调研的问题
2. **先画证据地图**：每个方向标注证据密度和信息质量，低密度方向直接砍掉
3. **区分事实和推断**：Fact / Inference / Judgment / Recommendation 四档标注
4. **盲区比假数据好**：公开源查不到的内容写成"关键盲区 + 验证路径"，不编
5. **报告按证据自适应**：证据支持 4 章就写 4 章，不强塞成 11 章的模板报告

## 能做什么？

### 支持的调研场景

| 场景 | 说明 |
|---|---|
| 入局判断 | 这个赛道有没有真预算？有没有可复制的交付路径？头部是否已垄断？ |
| 产品 / 方向选型 | 我们该做哪个细分场景？产品切谁的蛋糕？ |
| 竞品调研 | 拆竞品能力边界、定价逻辑、用户替代方案 |
| 招投标情报 | 看采购品类、中标格局、供应商生态 |
| 企业尽调 | 股权、经营、法律、行业地位的公开信息整理 |

### 产出的交付物

每次调研跑完，你会得到：

- ✅ 一份**确认过的调研问题**（不是原封不动的初始需求）
- ✅ 一份**证据地图**（哪些方向有料、哪些方向空白）
- ✅ 一份 **Markdown 报告**（正式咨询/投研报告风格，不做公众号腔）
- ✅ 一份 **HTML 报告**（深色科技风 + 毛玻璃 + 左侧冻结目录 + 可点击引用）
- ✅ 一份**来源索引**（每条关键判断有出处）
- ✅ 一份**盲区清单**（公开源查不到但对决策关键的东西）

### HTML 报告长什么样

深色渐变背景 + 毛玻璃卡片 + 左侧冻结目录 + 渐变标题 + 入场动画。

→ 示例效果见 `references/report-template-dark.html`

## 文件结构

```
market-research/
├── README.md              # 你正在看的这个
├── SKILL.md               # 技能主文件（AI Agent 的系统指令）
├── LICENSE                # MIT
├── references/
│   ├── evidence-workflow.md    # 问题校准 + 证据侦察 + 各渠道打法
│   ├── methods.md              # 分析方法库（DBS、Superpowers、Lenny、CAICT）
│   ├── reporting.md            # 报告写作规范 + HTML 生成规则
│   ├── structure-patterns.md   # 报告结构模式（Cir.cn、Chinabgao、CAICT）
│   ├── quality.md              # 质量控制 + 置信度标注 + 事实核查
│   └── report-template-dark.html # HTML 报告模板
├── scripts/
│   ├── render_html.py      # Markdown → HTML 渲染脚本
│   ├── validate_skill.py   # 技能结构完整性检查
│   └── run_evals.py        # 评估用例运行器
└── evals/
    └── evals.json          # 7 个评估用例（含断言）
```

## 快速开始

### 前置条件

1. 安装 [Hermes Agent](https://hermes-agent.nousresearch.com)
2. 将本仓库克隆到 Hermes 的 skills 目录：

```bash
# 克隆到 Hermes 技能目录
git clone https://github.com/yzmw123/market-research.git \
  ~/.hermes/skills/research/market-research
```

3. 在 Hermes 对话中，当你提出调研需求时，Hermes 会自动加载这个技能。你也可以手动触发：

```
调研一下工业AI质检这个方向有没有机会
帮我做一份竞品对比分析
看看XX行业的招投标格局
```

### 验证安装

```bash
cd ~/.hermes/skills/research/market-research
python3 scripts/validate_skill.py
# 输出: PASS: market-research skill structure looks good
```

### 运行评估

```bash
# 列出所有评估用例
python3 scripts/run_evals.py

# 运行单个用例
python3 scripts/run_evals.py --run 1

# 运行全部（需 hermes CLI）
python3 scripts/run_evals.py --run all
```

## 评估用例（Evals）

这个技能配了 7 个评估用例，覆盖最容易出错的场景：

| # | 用例 | 测什么 |
|---|---|---|
| 1 | 模糊机会判断 | 不直接写报告，先校准问题 |
| 2 | ToG 内部信息陷阱 | 不假装知道评标细则和关系网络 |
| 3 | AI IDE 竞品调研 | 包含替代方案，不只列竞品功能表 |
| 4 | C 端指标陷阱 | 不编造 CAC/LTV/留存曲线 |
| 5 | 公开信息薄弱市场 | 识别后转验证计划，不做假报告 |
| 6 | 付费报告目录参考 | 把付费目录当结构参考，不当事实证据 |
| 7 | 信通院权威报告引用 | 复用权威框架，保留原始来源校验 |

## 为什么做这个？

我是一个 PM，日常需要调研各种行业、竞品、市场机会。用 ChatGPT/Claude 直接聊的问题是：

- 输出像 AI 总结，不像专业报告
- 数字没出处，真假难辨
- 每个调研都要重新教一遍 AI 怎么干活
- 写出来的报告语气像公众号文章

于是我花了几个月，把调研方法论固化成了一套可复用的 AI 技能。现在每次调研，AI 都按同一套标准流程走。

这套技能已经帮我产出了几十份调研报告。如果你也经常需要 AI 帮你做市场调研，拿去用。

---

<a name="english"></a>

## English

### What is this?

A **market research skill for AI agents** that turns vague research requests into evidence-backed, professional reports. It's not a prompt template — it's a complete methodology that teaches AI agents to work like professional analysts:

1. **Calibrate** the research question before searching
2. **Scout evidence** before drafting an outline
3. **Separate facts, inferences, and judgments** with confidence labels
4. **Honestly report blind spots** instead of fabricating data
5. **Adapt the report structure** to evidence density, not a fixed template

Built for [Hermes Agent](https://hermes-agent.nousresearch.com). Written in Chinese (primary) with English reference documentation.

### Quick Start

```bash
git clone https://github.com/yzmw123/market-research.git \
  ~/.hermes/skills/research/market-research
```

### License

MIT — see [LICENSE](LICENSE).
