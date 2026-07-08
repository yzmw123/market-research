# Evidence Workflow

Use this reference when the research request is vague, broad, or likely to produce a generic report.

## 1. Calibrate the Decision (Interactive)

A research request must become a decision-support question before research starts. **Use the `clarify` tool with choices** to let the user pick their decision scenario — do not ask them to type it free-form.

### Step 1: Offer decision scenarios as choices

Use the `clarify` tool (not free-text questions) to present these options:

```python
clarify(
    question="这份调研将用于什么决策？请选择最贴切的一项：",
    choices=[
        "投资/入局判断 —— 判断某细分赛道未来1-2年是否有真预算、可复制交付路径、头部未完全垄断的切入机会",
        "产品/方向选型 —— 判断我们该做哪个细分场景、产品形态或竞品切口",
        "销售/标书/提案素材 —— 判断招投标热点、甲方关注指标、准入门槛和销售话术",
        "其他/组合场景 —— 我会在下一步补充具体决策描述"
    ]
)
```

**关键原则**：`clarify` choices 最多 4 个。把最可能的 3 个做成硬选项 + 1 个"其他/组合场景"兜底。具体内容根据用户原问题动态调整，不照搬模板。

### Step 2: "其他/组合场景"兜底

If user picks "其他/组合场景", use open-ended clarify:

```python
clarify(
    question="请简述你的具体决策场景（1-2句话）：",
    choices=[]  # open-ended
)
```

### Step 3: Rewrite and confirm

After knowing the decision type, rewrite the original vague question into a researchable form. Present the rewrite and ask for explicit confirmation (not implied) via clarify or direct reply:

```markdown
基于你的选择，我建议把原问题：
"{用户原话}"

重写为：
"{可调研问题}"

这份调研主要回答：
1. ...
2. ...
3. ...

不回答：
- ...

**确认无误请回复"确认"，或提出修改意见。**
```

### Translate vague terms into decision criteria

Use this table when crafting the rewrite:

| Vague term | Possible concrete meaning |
|---|---|
| 有机会 | budget exists, user pain exists, competition has gaps, acquisition channel exists |
| 有前景 | growth, policy push, capital interest, technology maturity, customer willingness to pay |
| 空间大 | TAM/SAM, underserved segment, pricing power, low competition, workflow frequency |
| 适合做 | reachable customers, deliverable product, sales channel, feasible differentiation |

Do not proceed to evidence scout without explicit user confirmation of the rewritten research question.

## 2. DBS-style Problem Dissolution

Check whether the user's question is answerable as written.

1. **Language trap** — key words are undefined.
2. **Hidden assumption** — the question assumes something false or unproven.
3. **Logic error** — correlation is treated as causation.
4. **Fact premise** — a stated fact may be false.
5. **Information gap** — the question is real but current information is insufficient.

Do not over-interrogate. One sharp question is better than a long questionnaire.

## 3. Evidence Scout

The first research pass is not a report. It is a map of what evidence exists.

For each candidate channel, record:

- Search queries used.
- Number and quality of useful results.
- Whether sources are original, authoritative institutional, secondary, marketing, or commentary.
- Whether sources provide **facts** or only **structure inspiration**.
- Whether the channel should be deepened.

### Structure Scout（报告目录侦察）

When the topic is broad, commercial, or expected to become a formal report, do a short structure scout before locking the outline.

Useful sources:

- `Cir.cn` paid report pages: open 2-5 relevant report pages and extract H1/H2/H3 table-of-contents headings. These reveal professional report modules such as industry overview, development environment, technology, supply-demand, segments, region, import/export, price, key companies, competition, strategy, investment risk.
- `Cir.cn` service pages: enterprise due diligence (`/QiyeDiaoyan/`), feasibility (`/Kexingxingyanjiu/`), market专项 (`/ZhuanxiangDiaoyan/`) provide mode-specific structures.
- `chinabgao.com/info` short articles: open 3-5 related articles and inspect H2/H3/caption structure. These show how to build a compact analysis around numbers, tables,口径 explanation, interpretation, and core insights.
- CAICT / 中国信通院 reports: for AI, digital economy, data governance, industrial internet, cloud, telecom, government digitalization, low-altitude economy and similar topics, prioritize 1-3 official CAICT reports. Use them both as structure patterns and as high-authority domain evidence, but verify critical numbers against original statistical / policy / company sources when possible.

Rules:

- Treat TOCs and short articles as **structure evidence**, not factual proof.
- If a chinabgao article contains a useful number, verify it from the original source before citing.
- Record structure scout output separately from factual evidence.
- Use recurring modules as chapter candidates; skip modules that are unsupported or irrelevant.

Detailed pattern bank: read `references/structure-patterns.md`.

## 4. Evidence Channels

### ToG

Start with public, document-based signals:

- `gov.cn`, ministries, local government sites.
- Policy documents and pilot programs.
- Standards and industry specifications.
- Procurement intentions and budgets.
- Tender and award announcements.
- Supplier names, consortium patterns, regions, project amounts.

Expected outputs: funding direction, procurement categories, supplier patterns, technical requirements, regional differences.

Unavailable from public sources: internal scoring, expert relationships, dark prices, unwritten entry rules.

### ToB

Start with market-facing and organization-facing signals:

- Product websites, pricing pages, docs, help centers.
- Case studies and customer logos.
- G2/Capterra/review sites when relevant.
- Hiring JD, technical blogs, conference talks.
- Annual reports, IPO prospectuses, investor decks.
- Funding, layoffs, partnerships, product launches.

Expected outputs: positioning, feature boundaries, pricing/package logic, target customers, technical investment signals, customer pain language, growth/retreat signals.

Unavailable from public sources: a specific company's internal procurement flow, true ROI model, churn, renewal rate, private architecture, decision-chain details.

### ToC

Start with public behavior and language signals:

- App Store / Google Play / local app stores.
- Version history and ratings.
- Xiaohongshu, Zhihu, Weibo, Reddit, X, Bilibili, Douyin where accessible.
- Public ranking tools and app-intelligence summaries.
- Public ads, landing pages, pricing pages.
- User comments, complaints, tutorials, comparison posts.

Expected outputs: user language, recurring pains/delights, scenario segmentation, pricing sensitivity signals, content传播素材, UX complaints.

Unavailable from public sources: true CAC/LTV, retention curve, silent churn, algorithm weights, internal A/B results.

### Product / Competitor

Start with product-owned and user-owned evidence:

- Official site, docs, release notes, changelog.
- Demo videos, onboarding flows, pricing.
- GitHub, community forum, Discord/Slack/public discussions if accessible.
- Review sites, comparison pages, Reddit/HN/Linux.do discussions.
- Public roadmap only if official.

Expected outputs: positioning, capability boundary, evolution direction, complaints, alternatives, differentiation opportunities.

## 5. Evidence Map Template

```markdown
## Evidence Map

| Direction | Queries / sources | Density | Quality | Continue? | Reason |
|---|---|---:|---:|---|---|
| ... | ... | high/medium/low | high/medium/low | yes/no/cautious | ... |

### Structure references（not factual evidence）
| Source | Useful modules / analysis pattern | How it affects outline |
|---|---|---|
| Cir.cn paid TOCs | e.g. supply-demand, technology, competition, investment risk | candidate modules only |
| Chinabgao short articles | e.g. table-driven 2-block analysis | style and table logic only |
| CAICT / 中国信通院 reports | e.g. background → concept/framework → status → practice → challenges/trends/suggestions | structure + authoritative domain evidence; verify critical numbers |

### Early blind spots
- {dimension}: public sources likely cannot answer because ...
```

## 6. Pivot Rules

- If a direction has low density and low decision impact, drop it.
- If a direction has low density but high decision impact, convert it to a blind spot.
- If a surprising evidence channel is strong, pivot the report around it.
- If all public channels are weak, stop trying to write a full report and produce a validation plan.
