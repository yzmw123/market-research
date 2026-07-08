# Reporting

Use this reference when turning research material into a formal industry / market / product research report.

## 核心原则

**报告是递进式分析，不是模板填空，也不是卡片合集。**

- 每个章节有明确的研究问题、分析过程、证据说明和阶段性结论。
- 以连续正文分析为主，表格只做辅助；每张表前后必须有解释。
- 所有大判断必须解释"为什么"，不能只写结论。
- 对拿不到的数据，写成"研究限制 / 关键盲区 / 验证路径"，不要假装已充分验证。
- 报告语气像正式咨询 / 投研 / 产业调研报告，而非公众号文章、AI 总结、项目建议书或销售方案。
- 结论必须从前文推导，而非先验给出。
- **空章节不出现。** 章节来自证据密度和决策目标，不来自固定目录。

## Finding Cards（内部组织工具，不出现在最终报告中）

Finding Cards 用于写报告前整理证据，不作为最终输出结构。

```markdown
### Finding 01: {one-sentence finding}

- Type: fact / inference / judgment / recommendation
- Evidence:
  1. {source + key content}
  2. {source + key content}
- Confidence: high / medium / low
- Limits:
  - {sample/source/verification limits}
- Decision impact:
  - {how this affects the user's decision}
```

### Type Rules

- **Fact**: directly supported by a source.
- **Inference**: reasoned from sources but not directly stated.
- **Judgment**: conclusion after weighing evidence.
- **Recommendation**: action suggestion based on findings.

Never label inference or judgment as fact.

## Adaptive Formal Report Structure

Do **not** always use an 11-chapter report. Build the final outline after evidence scouting and Finding Card clustering.

Recommended shape:

1. **执行摘要** — 2-4 段，给出核心判断、置信度、关键限制。
2. **研究问题与边界** — 原问题、重写后的决策问题、回答什么 / 不回答什么、证据来源。
3. **4-7 个主体章节** — 从下方模块库选择；每章必须有证据和阶段性结论。
4. **风险、盲区与验证路径** — 决策关键但公开源不可得的变量。
5. **结论与建议** — 区分"可继续研究 / 可试点验证 / 暂不建议进入"。
6. **来源索引** — 可溯源表。

If the report is intentionally short, use the chinabgao-style analysis note pattern in `structure-patterns.md`: conclusion-first title → opening context → 2 analytical blocks → tables with口径 → 核心洞察。

## Module Bank（按证据选择，不是固定目录）

Use a module only when evidence supports it or when it is a decision-critical blind spot.

| Module | Use when | Typical evidence |
|---|---|---|
| 行业定义与研究边界 | 概念容易混、范围容易漂 | 政策定义、标准、报告目录、产品分类 |
| 市场规模与增长 | 用户要判断"空间/前景" | 统计局、协会、财报、招股书、可信报告 |
| 需求侧：客户/用户/采购 | 要判断谁买、为何买、如何买 | 招投标、评论、访谈、案例、采购文件 |
| 政策、监管与标准 | ToG/强监管/合规驱动行业 | 政策文件、标准、监管案例、预算文件 |
| 产业链与价值链 | 需要看利润、上中下游、卡点 | 产业链图、企业业务结构、成本/毛利数据 |
| 供给侧与竞争格局 | 要看玩家、集中度、生态位 | 公司官网、年报、融资、投标、中标、份额数据 |
| 技术/产品演进 | 技术迭代影响机会窗口 | 专利、论文、文档、路线图、招聘JD、产品发布 |
| 细分市场/产品结构 | 大行业太泛，需要找切口 | 品类数据、客户场景、价格带、用例差异 |
| 区域/进出口/价格 | 地域、外贸、成本或价格是关键 | 海关、区域统计、价格指数、区域项目 |
| 重点企业/样本企业 | 需要用公司经营验证行业判断 | 年报、财务指标、业务拆分、研发投入 |
| 渠道/商业模式/交付 | 需要判断怎么卖、怎么交付、能否复制 | 渠道资料、定价、案例、合同、访谈 |
| 进入机会/风险/验证 | 用户要做决策 | 前文证据综合、盲区、试点方案 |

## Chapter Progression Patterns

Choose one progression based on the decision:

### Market opportunity / 是否值得做

研究问题与边界 → 市场与政策信号 → 需求/采购触发 → 供给与竞争 → 可进入切口 → 风险盲区 → 结论建议。

### Product / competitor teardown

研究问题与边界 → 用户任务与替代方案 → 竞品定位与能力边界 → 体验/定价/渠道 → 差异化空白 → 验证方案 → 结论建议。

### ToG / procurement intelligence

研究问题与边界 → 政策与资金 → 招投标项目类型 → 供应商/生态角色 → 技术与准入要求 → 关键盲区（评标、关系、暗价）→ 机会与验证路径。

### Company diligence / 企业调研

研究问题与边界 → 公司概况与历史沿革 → 股权/管理层 → 经营与财务 → 法律纠纷与公共信息 → 所在行业与竞争地位 → 信用/合作风险结论。

### Feasibility / 立项可研

项目背景与必要性 → 市场与需求 → 建设/技术方案 → 运营/管理/营销方案 → 投资估算与融资 → 财务/社会效益 → 风险与可行性结论。

### Authoritative institutional / CAICT-style report

Strategic background → concept and boundary → development status → framework / technology / governance architecture → typical practices → challenges and opportunities → trends and recommendations.

## Section Title Rules

- Main headings should be formal and decision-relevant, not generic filler.
- Subheadings can be finding-style, e.g. "存量运维而非新增建设，是工业清洗增长的主动力"。
- Avoid empty "宏观环境分析" sections unless macro evidence directly changes the decision.
- Avoid "发展趋势" as a standalone list; tie趋势 to evidence and decision impact.

## Evidence Use Rules

- Every major judgment needs source marks such as `[1]`.
- Inference must say "基于公开资料推断" and state confidence.
- If sources conflict, state the conflict and judgment reason.
- Marketing pages can prove what a vendor claims, not market truth.
- Paid report目录 (e.g. Cir.cn) can inspire structure, but cannot prove facts.
- Short industry articles (e.g. chinabgao) can inspire analysis style and point to candidate data; verify numbers from original sources before citing.

## Table Rules

Good tables usually come from actual data and answer one analytical question:

- regional distribution, market share, cost structure, user decision factors;
- sample company financial indicators, R&D intensity, business segment mix;
- tender project type / amount / supplier / buyer patterns.

Before the table: explain data source,口径, period, and why this table matters.
After the table: interpret the pattern and its decision implication.

## HTML 报告输出

不使用 Python 脚本渲染。Agent 直接根据以下规范生成完整 HTML 文件。

### 视觉风格（用户确认偏好 · 智敏 2026-07-01）

**深色科技渐变 + 毛玻璃**。这是用户确认过的偏好，写入 skill 作为所有调研报告的基准样式：

#### 核心色板

- 主背景：`#0a0a0f`（近黑）+ 径向渐变光晕（蓝/紫低透明）
- 文本主色：`#e8e8f0`，次级：`#a8a8b8`，辅助：`#686878`
- 强调色（accent-blue）：`#4f8fff` — 用于标题渐变、高亮、按钮、链接
- 强调色（accent-cyan）：`#00d4ff` — 用于数据高亮、二级标题
- 强调色（accent-purple）：`#8b5cf6` — 用于卡片渐变、特殊标记
- 玻璃态背景：`rgba(255,255,255,0.04~0.06)` + `backdrop-filter: blur(12~20px)`
- 边框：`rgba(255,255,255,0.08~0.12)`

#### 结构

1. **Hero 区域**：渐变背景 + 细线分隔底部 + badge + 渐变标题
2. **目录侧栏**：`position: sticky; height: 100vh; overflow-y: auto`，固定左侧
3. **数据卡片**：玻璃态 + hover 上移 + accent 色边框高亮
4. **表格**：可见边框 + 表头背景 + hover 行高亮 + 圆角
5. **进度条/可视化**：accent 渐变填充，动画过渡
6. **Hero h1**：`background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-blue) 100%)` + `background-clip: text` 渐变文字

#### 响应式
- 桌面：左侧 sticky 目录 + 右侧正文两栏
- 移动（< 800px）：目录折叠到正文上方

#### 关键细节
- **来源引用 `[S1]`**：accent-blue 色，hover 变色，可锚点跳转
- **strong**：白色文字 + 渐变背景 pill 风格
- **`<em>`**：斜体 + accent 色
- **卡片 hover**：`translateY(-2px)` + 边框变 accent 色
- **入场动画**：IntersectionObserver 触发 fade + translateY

#### HTML 代码模板

完整模板见 `references/report-template-dark.html`，Agent 复制后修改内容即可。

### 输出

- MD + HTML 保存到 `~/Downloads/<topic>-调研报告.{md,html}`
- 对话中只回复文件路径 + 一句话核心判断，不贴全文

### 布局：左侧冻结目录 + 右侧正文

目录必须冻结在左侧（类似 Excel 冻结窗口），不随正文滚动：

```
┌────────────┬────────────────────────────────┐
│  目录      │  正文区域                      │
│  (固定)    │  (可滚动)                      │
│            │                                │
│  1.1 xxx   │  # 标题                        │
│  1.2 xxx   │  正文内容...                   │
│  2.1 xxx   │                                │
│  ...       │  表格 / 列表 / 引用              │
│            │                                │
└────────────┴────────────────────────────────┘
```

实现方式（CSS Grid 或 flex）：
- 左侧目录栏 `position: sticky; top: 0; height: 100vh; overflow-y: auto`
- 正文区域 `margin-left` 或 grid 第二列自适应
- 移动端（< 800px）：目录折叠到正文上方

### 可读性增强（所有报告必须）

| 元素 | 处理方式 |
|---|---|
| `<strong>` | 暖色背景（如 `#f5e6c8`）+ 深色文字 + 圆角 padding 2-6px |
| `<em>` | 斜体 + 强调色文字，或左下边框 |
| `table` | 可见边框（1px solid #d4c8a8 或更深）+ 表头背景 + hover 行高亮 + 圆角 |
| `[S1]` 来源 | 珊瑚色/琥珀色编号，悬停可跳转 |
| 标题 h1/h2 | 纯黑 `#000`，不要任何渐变/环境色继承 |

### 主题色（按行业自动选）

不同行业用不同的强调色，但**底纹始终为浅色暖底**：

- `tech` — 强调：`#5b9bff` 蓝
- `cict` — 强调：`#3da9ff` 蓝
- `industry` — 强调：`#d4a017` 琥珀
- `consumer` — 强调：`#5db8a6` 青绿
- `finance` — 强调：`#5b9bff` 蓝

### 格式

```html
<!doctype html>
<html><head>
  <style>
    /* Agent 根据以上原则自行编写，不使用外部 css */
  </style>
</head>
<body>
  <!-- 左侧目录 -->
  <aside class="toc">...</aside>
  <!-- 右侧正文 -->
  <main>
    <h1>...</h1>
    <section>...</section>
  </main>
</body>
</html>
```

### 输出

- MD + HTML 保存到 `~/Downloads/<topic>-调研报告.{md,html}`
- 对话中只回复路径 + 一句话核心判断，不贴全文

## 本地文件输出

- Markdown：`~/Downloads/{topic}-调研报告.md`
- HTML：`~/Downloads/{topic>-调研报告.html`

## Blind Spots

A blind spot is not a failure. It is a decision-critical variable that public sources cannot answer.

For each blind spot, state:

- Why it matters.
- Why public sources cannot answer it.
- What proxy signals were checked.
- How the user can validate it: interview, expert call, POC, survey, internal data export, paid data tool, field visit.

## 来源索引格式

| 编号 | 来源 | 类型 | 核心引用 | 获取时间 | 置信度 | 备注 |
