# Structure Patterns from Chinese Report Sites

Use this reference when a research report needs a stronger chapter architecture. It captures structure lessons from two public sites the user pointed to:

- `https://www.cir.cn/Diaoyan/` and service pages such as `/QiyeDiaoyan/`, `/Kexingxingyanjiu/`, `/ZhuanxiangDiaoyan/`.
- `https://www.chinabgao.com/info/` short industry-analysis articles.

These sources are useful for **report architecture** and **analysis rhythm**. They are not primary evidence for facts unless their claims are verified from original sources.

## 1. How to Use Paid Report TOCs

Paid report pages often expose only the table of contents. That is still valuable:

1. Open 2-5 pages for the same or adjacent industry.
2. Extract H1/H2/H3 headings and table captions.
3. Mark recurring modules and unusual modules.
4. Convert recurring modules into candidate report chapters.
5. Do not copy the full TOC mechanically; keep only modules supported by evidence.
6. Never cite a paid TOC as evidence for market size, share, growth, or company performance.

Good search/query patterns:

```bash
autocli google search "site:cir.cn 行业名 前景 报告 目录" --limit 10 --format json
autocli read "https://www.cir.cn/...html" -f text
```

## 2. Cir.cn Full Report TOC Patterns

Observed pages:

- `全球与中国纳米铬粉行业市场分析及发展前景预测报告（2026-2032年）`
- `中国自调控电伴热带市场调查研究与前景趋势报告（2026-2032年）`

Recurring module order:

1. **行业/产业概述** — definition, classification, business model, industry chain, industry dynamics.
2. **发展环境** — political/legal, economic, social, policy, standards.
3. **技术发展** — current technology, domestic/foreign differences, direction, capability improvement.
4. **Global vs China supply-demand** — global manufacturers/countries/trends; China manufacturer distribution, output, demand, customer structure, regional demand, forecast.
5. **细分市场** — product/category submarkets.
6. **总体发展 / 财务能力** — scale, profitability, solvency, operating capability, growth.
7. **进出口 / 价格 / 区域** — if relevant to commodity or manufacturing industries.
8. **重点企业** — key company profiles and comparisons.
9. **竞争格局** — concentration, competitive pattern, strategy.
10. **企业发展策略** — market strategy, sales strategy, brand strategy, competitiveness improvement.
11. **投资 / 风险 / 进入壁垒** — investment opportunities, risks, barriers, risk controls.
12. **结论与建议** — market prospect, trend forecast, research conclusion, investment suggestion.

Useful lesson: Cir-style reports are strong at **coverage completeness**, but they easily become template-filled. In our reports, use this as a module checklist after evidence scouting, not as a mandatory sequence.

## 3. Cir.cn Enterprise Due Diligence Pattern

Observed `/QiyeDiaoyan/` basic directory:

1. 前言
2. 公司概况
3. 注册信息
4. 历史沿革
5. 股份结构
6. 主要管理人员信息
7. 财务状况 — balance sheet, income statement, key financial data, financial ratios
8. 银行信息
9. 经营状况 — main business, sales, procurement, premises, employees
10. 法律纠纷
11. 公共信息
12. 行业分析
13. 综述

Use when the user asks about a specific company, partner, competitor, acquisition target, supplier, or customer credit risk.

## 4. Cir.cn Market专项 Pattern

Observed `/ZhuanxiangDiaoyan/`:

- 市场规模和发展潜力研究 — market sizing, potential, trend estimation.
- 市场细分和客户行为研究 — target segments, customer positioning, potential customers, sales/marketing fit.
- 渠道研究 — channel structure, channel width/depth, distributor state, channel management.
- 消费者研究 — demand, behavior and attitude, satisfaction, loyalty, complaints, recommendation.
- 竞争对手研究 — finance, HR, marketing, product/pricing, competition, R&D, channel strategy.
- 市场进入研究 — market, competition, product, user, channel; opportunities and threats.

Use when the decision is **how to enter a market** or **which customer/channel/product segment to prioritize**.

## 5. Cir.cn Feasibility / 立项可研 Pattern

Observed `/Kexingxingyanjiu/` visible text:

Use cases include financing/招商合作, NDRC立项, bank loan, overseas investment approval, IPO fundraising projects, and government-fund applications.

Visible requirements emphasize:

- market analysis accuracy;
- reasonable investment plan;
- competitive analysis;
- marketing plan;
- management plan;
- technical R&D / technical plan;
- financing plan and risk assessment.

Use when the user asks for 立项、可研、申报、融资、贷款、募投 or “这个项目可不可行”. Do not turn ordinary market research into a formal可研 unless the decision is project approval / financing / investment.

## 6. Chinabgao Short Industry-Analysis Pattern

Observed `chinabgao.com/info` articles are shorter than paid reports but useful because they show a real analytical rhythm.

Common structure:

1. **Title contains a conclusion and a number** — e.g. “运营业务增速近50%”, “华东占比达42%”, “净利增幅超50%”.
2. **Lead paragraph** — defines the sector and states the core change.
3. **Two large analytical blocks** — often “industry situation / market structure” + “industry chain / competition / trend”.
4. **Nested 1.1 / 1.1.1 subsections** — each small section answers one data question.
5. **Tables with captions** — financial metrics, regional share, cost structure, user decision factors, market share, R&D indicators.
6. **口径 explanation around tables** — period, sample, source type, unit, whether data are comparable.
7. **Interpretation after table** — not just listing numbers; explains what the pattern means.
8. **核心洞察** — compact final judgment.

Observed article examples:

- 智慧停车：头部企业竞争格局 → 硬件集成 / 运营服务 → 产业链盈利特征 → 业务结构转型。
- 网络游戏：政策监管 / 版号 → 区域营收结构 → 样本上市企业经营 → 成本收益结构。
- 采矿：规模与盈利 → 合规监管案例 → 头部黄金矿企盈利 → 海外投资区域。
- 工业清洗：市场规模/区域分布 → 供给端企业分布 → 上游药剂/设备 → 中游服务竞争。
- 在线音频：用户付费意愿 → 消费决策因素 → 头部平台份额 → 播客用户与商业化。
- IDC：机架规模 → 区域结构 → 产品结构 → 绿色转型 → 头部运营商经营数据 → 中长期预测。

Useful lesson: a strong short report is not a mini encyclopedia. It picks **one angle**, proves it with 3-4 tables, and ends with a judgment.

## 7. CAICT / 中国信通院 Authoritative Report Pattern

Use CAICT reports as priority references for digital economy, AI, data governance, industrial internet, telecom, cloud, government digitalization, and adjacent emerging industries. Observed local examples include: low-altitude economy data governance, AI for SMEs, AI+ocean, industrial intelligence, government digital transformation, and enterprise agents.

### Source status

CAICT is an authoritative institutional source. It can support:

- definitions, concept boundaries, technical / governance frameworks;
- policy and industry trend synthesis;
- reference architectures, implementation paths, standard-system views;
- typical practice / case catalogs.

Still verify decision-critical numbers, market-size claims, company-specific performance, and causal claims against original sources when possible.

### Common CAICT report progression

1. **战略背景 / 发展态势** — why the topic matters now; policy, technology, industry demand.
2. **概念内涵 / 资源体系 / 研究边界** — definitions, layers, actors, data or capability systems.
3. **发展现状 / 总体进展** — domestic/foreign situation, maturity stage, existing platforms or mechanisms.
4. **技术能力 / 参考架构 / 产业链分层** — architecture, key technologies, upstream-midstream-downstream, governance components.
5. **典型实践 / 场景应用** — cases by industry or function; each case explains integration point and value.
6. **挑战与机遇 / 风险约束** — infrastructure, data, technology, talent, governance, commercialization.
7. **趋势展望与建议** — technical trend, application trend, industry/ecosystem trend, policy and implementation suggestions.

### Reusable structure archetypes from observed CAICT PDFs

- **治理类**: 发展态势 → 资源体系与治理内涵 → 总体进展 → 参考架构与实施路径 → 对策建议.
- **AI赋能产业类**: 背景/内涵 → 产业链现状（上游/中游/下游）→ 典型实践（按场景）→ 挑战与机遇 → 趋势与建议.
- **工业/技术演进类**: 愿景篇 → 技术篇 → 应用篇 → 展望篇.
- **政府数智化类**: 全球时代特征 → 国内发展格局 → 新范式/建设路径 → 发展展望 → 附录实践案例.
- **企业级技术应用类**: 发展概述 → 技术能力 → 运营管理 → 应用实践 → 趋势展望.

### Writing lessons

- Use a clear “前言/执行摘要” to state why the report exists and preview chapters.
- Prefer framework diagrams and layer models when the subject is complex.
- Name maturity stage explicitly: 起步期、规模化初始阶段、深度融合阶段等.
- Cases should not be decorative; each case should show integration point, mechanism, and value.
- Recommendations should map back to challenges and implementation path, not float as slogans.

## 8. Translation Rules for Our Reports

When using these patterns:

- Start with the user's decision question, not with the external site's category.
- Use Cir TOCs to avoid missing obvious modules.
- Use chinabgao-style tables and口径 notes to make analysis concrete.
- Prefer 4-7 meaningful main chapters over 10+ generic chapters.
- If a module appears in paid TOCs but public evidence is weak, mention it under blind spots or validation, not as an empty chapter.
- If a report needs a headline/summary, make it conclusion-bearing and evidence-based, e.g. “工业清洗的机会不在新增产线，而在存量运维外包渗透率提升”.

## 9. Structure Scout Output Template

```markdown
## Structure Scout

### Pages checked
- Cir.cn: <title/url> — recurring modules: ...
- Chinabgao: <title/url> — analysis pattern: ...

### Candidate modules for this report
| Module | Why relevant | Evidence available? | Action |
|---|---|---|---|
| 市场规模与增长 | 用户关心空间 | medium | include, verify with original data |
| 进出口 | TOC common but not decision-relevant | low | skip |
| 渠道结构 | 决定进入路径 | high | include |
| 真实采购决策链 | decision-critical but private | unavailable | blind spot + interview plan |
```
