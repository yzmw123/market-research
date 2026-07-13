# Evidence Standard

## 目录

1. 证据文件
2. 来源规则
3. 判断规则
4. 证据侦察
5. 采样与去重
6. 完成标准

## 1. 证据文件

每份正式报告维护一个 YAML 文件：

```yaml
research:
  question: 工业 AI 质检是否存在可进入的中端制造市场？
  scope: 中国，中小型制造企业，2024-2026
  cutoff_date: 2026-07-13
  generated_at: 2026-07-13

sources:
  - id: S1
    title: 来源标题
    url: https://example.com/source
    publisher: 发布机构
    published_at: 2026-06-01  # 无法确认时写 null
    retrieved_at: 2026-07-13
    source_type: primary
    independence_group: official-announcement-001
    notes: 原始公告

claims:
  - id: C1
    statement: 该市场存在明确采购信号
    type: inference
    confidence: medium
    source_ids: [S1]
    limitations:
      - 样本只覆盖公开采购
    decision_impact: 值得继续验证，但不足以直接决定产品化
```

合法类型：

- `source_type`: `primary`、`institutional`、`secondary`、`vendor`、`community`
- `type`: `fact`、`inference`、`judgment`、`recommendation`
- `confidence`: `high`、`medium`、`low`

## 2. 来源规则

优先级：

1. 原始政策、监管文件、采购公告、财报、招股书、产品文档、价格页。
2. 权威机构报告、行业协会和统计机构。
3. 可信媒体和专业研究机构。
4. 厂商营销材料。
5. 社区评论、社交媒体和个人文章。

厂商材料可以证明“厂商如何描述自己”，不能单独证明市场领导、ROI、客户满意度或技术优势。

记录发布时间和获取时间。无法确定发布日期时写 `null` 并降低置信度；对会快速变化的价格、产品能力、公司状态和政策执行情况重新核验。来源发布日期不得晚于证据截止日，获取日期不得晚于报告生成日。

## 3. 判断规则

- `fact`：来源直接陈述，可逐字定位。
- `inference`：由多个事实推导，必须写出限制。
- `judgment`：权衡证据后的决策结论。
- `recommendation`：由判断产生的行动建议。

高置信度通常需要两个独立来源，至少一个原始来源。来源数量不能替代独立性和相关性。

## 4. 证据侦察

第一轮只建立证据地图，不写报告。对每个通道记录：

- 查询式、语言、地域和时间窗。
- 有效结果数量和典型来源。
- 证据类型、质量、时效性和决策影响。
- 是否继续、转为盲区或放弃。

ToG 优先政策、预算、采购意向、招中标和标准；ToB 优先官网、定价、文档、案例、财报和招聘；ToC 优先商店评论、版本历史、公开排名、社媒和价格页。

## 5. 采样与去重

数量分析前明确：

- 时间范围、地域范围、关键词和排除条件。
- 项目去重键、联合体处理、废标处理、缺失金额处理。
- 金额单位、币种、含税口径和异常值规则。
- 样本覆盖偏差和不可见市场。

使用 `independence_group` 标记同一新闻稿、同一公告转载或同源数据。属于同一组的来源只算一个独立证据。

## 6. 完成标准

- 每个重大判断都有 `claim`。
- 每个 `claim.source_ids` 都能解析到来源。
- 每个正文 `[Sx]` 都存在于证据文件。
- 所有来源 URL 合法、可访问或注明访问限制。
- 高置信度判断满足独立来源要求。
- 所有推断、判断和建议都写明限制或决策影响。
