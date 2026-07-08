# Quality Gates

Use this reference before final delivery and when reviewing the skill's behavior.

## Confidence Scoring

| Confidence | Standard |
|---|---|
| High | Multiple independent sources, at least one original source, recent enough, directly supports the claim |
| Medium | Clear source exists, but source is single, secondary, old, small-sample, or interpretation-heavy |
| Low | Weak signal, marketing source, user anecdote, long inference chain, or insufficient corroboration |

High confidence does not mean “certain”. It means the claim is well supported by available evidence.

## Fact-check Targets

Always verify:

- Numbers.
- Dates.
- Company and product names.
- Policy and standard titles.
- Funding amounts and rounds.
- Tender amounts and award entities.
- Comparative claims: first, only, largest, leading, most advanced.
- Causal claims: because, caused by, led to, proves.

## Claim Handling

If a claim cannot be verified:

1. Search for the original source.
2. Search with alternate language / synonyms.
3. If still unsupported, downgrade it to inference or remove it.
4. If it is decision-critical, move it to blind spots.

Never hide uncertainty in vague phrases like “据说”, “业内认为”, “有观点称” unless the source is explicitly named.

## Marketing-source Rules

Marketing pages can prove what a vendor claims, not what the market is.

Allowed:

- Vendor positioning.
- Feature claims.
- Customer logos shown by the vendor.
- Packaging and pricing.

Not allowed without corroboration:

- Market leadership.
- ROI impact.
- Customer satisfaction.
- Adoption scale.
- Technical superiority.

## Structure-source Rules

Paid report目录 and short secondary articles can improve report architecture, but they are not primary factual evidence.

Allowed:

- Identifying likely report modules.
- Learning table/caption/口径 patterns.
- Discovering candidate variables to verify elsewhere.

Not allowed without original-source verification:

- Market size, growth rate, market share, CR3/CR5, CAGR.
- Company financials or segment revenue.
- Policy interpretation or regulatory status.
- Comparative claims such as “最大/领先/唯一”.

## Authoritative Institutional-source Rules

Reports from authoritative institutions such as CAICT / 中国信通院 are high-quality domain evidence for ICT, digital economy, AI, data governance, telecom, industrial internet, cloud, and government digitalization.

Allowed with citation:

- Concept definitions and research boundaries.
- Technical / governance / standard-system frameworks.
- Policy and industry trend synthesis.
- Typical practice catalogs and maturity judgments.

Still verify when decision-critical:

- Market-size and growth numbers.
- Company-specific performance or market share.
- Policy effective dates and legal status.
- Claims of causality or superiority.

## Conversation Output Rules

不要在对话中直接输出完整报告原文。报告全文保存到本地 Markdown + HTML 文件即可，对话内只输出**简要概述 + 核心判断 + 后续如何打开文件**。

```markdown
REPORT 已保存到本地:
- MD: ~/Downloads/<主题>-调研报告.md
- HTML: ~/Downloads/<主题>-调研报告.html

核心判断（1 段即可）:
- 赛道性质、是否有真预算、最好的进入方向、不适合的路径。

关键数据来源（简短列出 3-5 个核心证据编号即可）。

一句话说明下一步: [例如：建议先做这 3 个验证再决定是否产品化]
```

## Public-source Boundaries

Do not present structurally private data as knowable from public sources:

- ToG: internal scoring, expert relationships, dark prices, unwritten access rules.
- ToB: specific internal procurement process, true ROI model, churn, renewal rate, private architecture.
- ToC: true CAC/LTV, retention curve, silent churn, algorithm weights, internal A/B tests.

## Review Checklist

Before final delivery, check:

- Did the work start from a confirmed research question?
- Is there an evidence map?
- If the report needs a formal structure, is there a structure scout or explicit structure rationale?
- Are sections generated from findings rather than a fixed template?
- Are paid TOCs / short secondary articles used only as structure references unless facts were independently verified?
- Does each main finding have sources?
- Are facts, inferences, judgments, and recommendations separated?
- Are blind spots explicit?
- Are unsupported claims removed or downgraded?
- Are Markdown and HTML files saved if requested/defaulted?

## Eval Prompts

Eval prompts are in `evals/evals.json`. Use those as pressure tests before and after modifying the skill.
