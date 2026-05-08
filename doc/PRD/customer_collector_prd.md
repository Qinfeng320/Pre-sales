# 客户信息收集智能体系统 PRD

| 版本 | 日期 | 作者 | 说明 |
|------|------|------|------|
| v1.0 | 2026-05-08 | - | 初始版本 |

---

## 1. 概述

### 1.1 产品背景

需要一个客户信息收集智能体系统，解决售前工程师**三大核心痛点**：

1. **历史项目不清晰** - 不清楚客户过往做过哪些项目、用了谁的产品、花了多少钱
2. **政策匹配困难** - 不知道哪些政策适合哪些客户，很难找到政策依据
3. **信息分散难整合** - 客户信息分散在微信、邮件、笔记本里，很难统一管理

**核心场景**：输入客户（学校/教育局），系统自动展示：
- 客户基本信息 + 联系人
- 历史信息化项目（供应商、金额、建设内容）
- 现有系统情况
- 相关政策（为售前方案提供政策依据）

**与政策搜集系统联动**：
- 客户类型（高校/中小学/教育局）→ 匹配相关教育政策
- 历史项目 → 关联当时的相关政策
- 售前方案 → 可直接引用政策原文作为依据

**核心约束**：
- **准确性100%**：客户信息少，1%错误率都不可接受
- **引用原文**：需求/痛点必须原文记录，不接受摘要
- **人工校验**：客户信息由人工核对保证准确性

### 1.2 产品目标

1. **解决历史项目不清晰** - 详细记录客户过往信息化项目，包括供应商、金额、建设内容
2. **解决政策匹配困难** - 通过客户类型自动匹配相关政策，为售前方案提供政策依据
3. **解决信息分散难整合** - 集中管理所有客户信息在一个系统
4. 通过**人工校验**保证客户信息100%准确
5. 为售前方案提供**政策依据引用**

### 1.3 范围

**包含**：
- 客户发现与登记（用户发现客户后登记）
- 需求与痛点记录（售前关键信息）
- 历史项目记录（过往信息化项目）
- 人工校验（运营人员核对原文保证准确性）
- 政策联动检索（客户类型 → 相关政策）
- 向量检索（RAG）
- REST API + SDK输出

**不包含**：
- 自动爬虫采集（客户信息由用户手动补充）
- 文档生成（作为下游系统）

---

## 2. 功能需求

### 2.1 客户发现与登记

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 基本信息登记 | 客户名称、类型、地区、层级、地址 | P0 |
| 联系人登记 | 联系人姓名、职务、电话、邮箱 | P0 |
| **多角色分析入口** | 触发六大角色智能体分析客户 | P0 |
| 来源验证 | 验证信息来源可靠性，仅记录一手来源 | P1 |
| 去重引用 | 相同客户从不同来源入库时，建立引用关系 | P1 |

**客户类型**：
- 高等教育（大学、高职院校）
- 基础教育（中小学、幼儿园）
- 教育局（省/市/区县）
- 教育培训机构
- 其他教育相关机构

**客户层级**：
- 省级
- 市级
- 区县级
- 校级

**来源类型**：
- 官方渠道（官网、官方文件）
- 公开数据（企查查、天眼查）
- 实地拜访
- 客户主动联系
- 展会/会议

### 2.2 需求与痛点记录

**需求痛点记录**：

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 需求类型分类 | 基础设施/教学应用/数据治理/安全/运维等 | P0 |
| 痛点描述 | 原文记录客户反馈，不摘要不改写 | P0 |
| 需求来源 | 客户访谈/问卷/历史资料/公开信息 | P0 |
| 优先级标记 | 高/中/低 | P1 |
| 关联政策 | 可引用相关政策作为需求支撑 | P1 |

**需求类型分类**：
| 类型 | 说明 |
|------|------|
| 基础设施 | 网络、服务器、存储、机房等 |
| 教学应用 | 教学平台、实训系统、智慧教室等 |
| 数据治理 | 数据中台、数据标准、数据安全等 |
| 安全管理 | 等保、分级保护、安全运营等 |
| 运维服务 | 运维平台、服务水平、巡检等 |
| 移动办公 | 移动端、应用集成、即时通讯等 |
| 其他 | 其他需求 |

### 2.3 历史项目记录

**核心痛点解决**：记录客户过往信息化项目，解决"不清楚客户做过什么、用过谁的产品、花了多少钱"的问题。

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 项目基本信息 | 项目名称、时间、金额、供应商 | P0 |
| 项目内容描述 | 项目具体建设内容原文 | P0 |
| **现有系统情况** | 客户目前部署了哪些系统、供应商是谁 | P0 |
| 相关政策引用 | 项目当时依据的相关政策 | P1 |
| 竞争对手分析 | 同类项目的竞争对手/供应商 | P1 |
| 客户评价 | 客户对项目的反馈 | P2 |
| 后续跟进 | 是否有续期/扩展机会 | P2 |

**项目状态**：
| 状态 | 说明 |
|------|------|
| 在建 | 项目正在实施中 |
| 已完成 | 项目已验收 |
| 运维中 | 在运维服务期内 |
| 已到期 | 运维服务已到期 |
| 待续期 | 有续期意向 |

**现有系统情况记录**（重点）：
| 字段 | 说明 |
|------|------|
| 系统名称 | 如"智慧校园平台"、"数据中心"等 |
| 供应商 | 系统供应商/集成商 |
| 建设年份 | 建设时间 |
| 合同金额 | 项目金额 |
| 合同期限 | 运维到期时间 |
| 客户满意度 | 客户对该系统的评价 |
| 待改进点 | 客户反馈的问题或不足 |

### 2.4 多角色智能体分析

**核心价值**：同一客户信息，不同角色看到不同的分析重点。

#### 六大角色视角

| 角色 | 分析重点 | 关注信息 |
|------|----------|----------|
| **销售** | 商机识别 | 预算规模、决策链完整性、竞争态势、成交可能性 |
| **售前** | 方案支撑 | 需求痛点、技术可行性、政策依据、差异化优势 |
| **实施** | 技术落地 | 现有系统兼容性、集成难度、工时评估、技术风险 |
| **售后** | 运维风险 | 系统复杂度、客户满意度、续费机会、问题预警 |
| **客户-决策者** | 投资回报 | 投入产出比、战略价值、风险控制、政策合规 |
| **客户-使用者** | 使用体验 | 操作便捷性、功能实用性、培训需求、协作效率 |

#### 智能体分析流程
```
[客户信息] → [并行触发多角色分析] → [综合分析报告]
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
┌───────┐     ┌───────┐     ┌───────┐
│  销售  │     │  售前  │     │  实施  │
│ Agent │     │ Agent │     │ Agent │
└───────┘     └───────┘     └───────┘
    ↓               ↓               ↓
┌───────┐     ┌───────┐     ┌───────┐
│  售后  │     │决策者  │     │  使用者 │
│ Agent │     │ Agent │     │ Agent │
└───────┘     └───────┘     └───────┘
```

#### 各角色分析维度

**销售智能体分析**：
| 分析维度 | 说明 | 输出 |
|----------|------|------|
| 预算评估 | 根据客户类型/地区/历史项目估算预算 | 预算区间(高/中/低) |
| 决策链 | 识别关键决策人、评估决策周期 | 决策链图谱 |
| 竞争态势 | 分析竞争对手占据的市场、客户的满意度 | 竞争分析报告 |
| 成交概率 | 综合评估商机成熟度 | 商机评分(0-100) |
| 推荐策略 | 根据分析结果给出跟进策略 | 行动建议 |

**售前智能体分析**：
| 分析维度 | 说明 | 输出 |
|----------|------|------|
| 需求匹配 | 分析客户需求与产品/方案的匹配度 | 匹配度报告 |
| 政策依据 | 找出支持方案的政策引用 | 政策引用列表 |
| 差异化 | 对比竞争对手方案的优劣势 | 差异化分析 |
| 风险点 | 识别技术/商务风险 | 风险预警 |
| 方案建议 | 给出解决方案建议 | 方案框架 |

**实施智能体分析**：
| 分析维度 | 说明 | 输出 |
|----------|------|------|
| 兼容性 | 评估与现有系统的集成难度 | 兼容性报告 |
| 工时评估 | 估算实施周期和人力需求 | 工时估算 |
| 技术风险 | 识别技术难点和风险点 | 风险清单 |
| 资源需求 | 评估所需技术资源和设备 | 资源清单 |
| 实施建议 | 给出实施策略建议 | 实施路径 |

**售后智能体分析**：
| 分析维度 | 说明 | 输出 |
|----------|------|------|
| **续费机会** | 评估合同到期时间、续费意向、预估金额 | 续费概率(0-100)、到期时间、续费金额预估 |
| **续费历史** | 过往续费记录和金额 | 历史续费次数、总金额 |
| **客服工作量** | 评估历史客服请求量和问题类型 | 问题分类统计、平均响应时间 |
| **排障记录** | 分析历史故障记录，评估系统稳定性 | 故障频率、平均解决时间 |
| **扩展机会** | 识别现有系统扩展/升级需求 | 扩展机会清单 |
| **服务建议** | 给出续费策略和主动服务计划 | 服务策略 |

**售后分析数据来源**：
| 数据 | 说明 |
|------|------|
| 售后记录表 | 工单、故障、续费历史记录 |
| 合同状态 | 当前合同类型、到期时间 |
| 客户反馈 | 历史满意度调查、服务评价 |
| 客服工单 | 历史问题数量、类型、解决时效 |

**客户-决策者视角分析**：
| 分析维度 | 说明 | 输出 |
|----------|------|------|
| 战略价值 | 分析项目对客户业务的价值 | 价值分析报告 |
| 投入产出 | 估算投资回报周期和效益 | ROI分析 |
| 风险控制 | 评估项目风险和缓解措施 | 风险管理建议 |
| 政策合规 | 识别必须满足的政策要求 | 合规清单 |
| 投资建议 | 从决策者角度给出建议 | 决策参考 |

**客户-使用者视角分析**：
| 分析维度 | 说明 | 输出 |
|----------|------|------|
| 操作体验 | 评估系统的易用性 | 体验评分 |
| 功能实用性 | 分析功能对实际工作的帮助 | 功能价值分析 |
| 培训需求 | 评估用户需要哪些培训 | 培训计划建议 |
| 协作效率 | 分析对部门协作的影响 | 效率提升预测 |
| 改进建议 | 从使用者角度提出改进点 | 改进建议 |

#### 分析触发机制

| 触发方式 | 说明 |
|----------|------|
| 手动触发 | 用户选择客户后，点击"多角色分析"按钮 |
| 自动触发 | 客户信息更新时自动分析（可选） |
| 定时触发 | 定期重新分析（如每周） |

#### 分析结果展示

```json
{
  "success": true,
  "customer_code": "CUS-2024-089",
  "analysis_time": "2024-06-20T10:00:00Z",
  "role_analyses": {
    "sales": {
      "budget_assessment": "高",
      "decision_chain": ["信息化主任", "副校长", "校长"],
      "competition": {
        "current_vendors": ["竞品A", "竞品B"],
        "satisfaction": "中",
        "opportunity": "有替换意愿"
      },
      "win_probability": 75,
      "recommended_actions": ["重点跟进信息化主任", "准备差异化方案"]
    },
    "presales": {
      "need_match_score": 85,
      "policy_references": ["POL-2024-089", "POL-2023-045"],
      "differentiators": ["国产化适配", "本地化服务"],
      "risks": ["工期紧张", "集成复杂"],
      "proposal_suggestion": "建议分阶段实施"
    },
    "implementation": {
      "compatibility_score": 70,
      "estimated_man_days": 120,
      "technical_risks": ["旧系统接口不稳定"],
      "resource_requirements": ["2名高级工程师", "1名DBA"]
    },
    "after_sales": {
      "renewal_opportunity": {
        "probability": 85,
        "current_contract_expire": "2025-06-30",
        "renewal_intent": "高",
        "estimated_renewal_amount": 500000,
        "renewal_history": [
          {"year": 2024, "amount": 480000, "result": "成功"},
          {"year": 2023, "amount": 450000, "result": "成功"}
        ]
      },
      "service_workload": {
        "total_tickets_6m": 12,
        "avg_response_hours": 2.5,
        "avg_resolution_hours": 8,
        "ticket_types": {"咨询": 5, "故障申报": 4, "投诉": 3}
      },
      "fault_records": {
        "total_faults_6m": 3,
        "avg_downtime_minutes": 45,
        "fault_types": {"网络": 1, "系统": 1, "数据": 1}
      },
      "expansion_opportunities": [
        {"system": "智慧校园平台", "opportunity": "移动端扩展", "estimated_amount": 200000}
      ],
      "service_suggestions": [
        "合同到期前3个月启动续费洽谈",
        "针对历史故障提供主动巡检服务"
      ]
    },
    "client_decision_maker": {
      "strategic_value": "高",
      "roi_period": "3年",
      "risk_control": ["制定详细实施计划", "设置里程碑验收"],
      "policy_compliance": ["等保2.0三级", "教育信息化2.0行动计划"]
    },
    "client_user": {
      "ease_of_use_score": 80,
      "functional_value": ["提高协作效率", "减少重复工作"],
      "training_needs": ["系统操作培训", "数据分析培训"],
      "improvement_suggestions": ["希望增加移动端"]
    }
  },
  "summary": {
    "overall_score": 78,
    "key_insights": [
      "客户有明确需求，但竞争对手已占据市场",
      "需要突出差异化优势（国产化+本地服务）",
      "运维合同即将到期，是切入的良好时机"
    ],
    "priority_actions": [
      "尽快安排与信息化主任的深度沟通",
      "准备针对竞品缺点的差异化方案"
    ]
  }
}
```

---

### 2.5 政策联动检索

**核心痛点解决**：解决"不知道哪些政策适合哪些客户"的问题。

**核心场景**：
```
输入: 客户类型（高校/中小学/教育局）
↓ 匹配相关政策
返回: 相关政策列表（提供政策依据）
```

**联动方式**：

| 联动方向 | 说明 | 售前价值 |
|----------|------|----------|
| 客户 → 政策 | 输入客户类型，返回适用政策 | 了解客户适用哪些政策 |
| 政策 → 客户 | 输入政策，找到相关客户类型 | 反向发现潜在客户 |
| 项目 → 政策 | 历史项目关联当时的政策 | 了解项目背景 |
| 需求 → 政策 | 客户需求可引用政策作为依据 | 为方案提供政策支撑 |

**政策匹配维度**：
| 维度 | 说明 |
|------|------|
| 客户类型 | 高等教育/基础教育/教育局 匹配不同政策 |
| 地区 | 省级/市级/区县级 政策可能有差异 |
| 需求类型 | 基础设施/数据治理/安全 有对应政策 |
| 时间 | 仅返回5年内政策 |

**检索方式**：
- 向量检索（语义相似度）
- 关键词过滤（客户类型/地区/需求类型）
- 混合检索（向量 + BM25 + RRF融合 + Rerank）

**输出政策引用格式**：
```json
{
  "citation_id": "POL-2024-089",
  "title": "关于加快推进教育信息化建设的指导意见",
  "source": "教育部",
  "publish_date": "2024-06-15",
  "match_reason": "高等教育类型适用",
  "relevant_excerpt": "（一）加快教育数字化转型..."
}
```

### 2.6 人工校验

**客户信息准确性由人工校验保证**：

| 阶段 | 说明 |
|------|------|
| 登记时 | 仅记录元信息（名称/类型/地区），无需校验 |
| 补充详情后 | 进入人工校验队列 |
| 人工确认 | 运营人员核对信息与原始来源是否一致 |
| 校验通过 | 客户标记为"已校验"，允许检索 |

**校验状态**：
| 状态 | 说明 |
|------|------|
| unverified | 未校验（信息刚登记或校验未通过） |
| verified | 已校验通过，允许检索 |

### 2.7 时效性与排序

**搜索范围**：
- 客户信息默认展示全部（客户不像政策有时效性）
- 政策检索仅返回5年内政策（联动政策系统）

**排序规则**：
- 检索结果默认按 **最近更新时间倒序**
- 支持按客户名称/类型/地区/创建时间切换排序

---

## 3. 非功能需求

### 3.1 准确性

| 指标 | 要求 |
|------|------|
| 内容准确率 | 100%（不生成、不摘要、不改写） |
| 引用溯源 | 每个客户信息可追溯到原始来源 |
| 人工校验 | 客户信息必须经过人工校验才能被检索 |

### 3.2 性能

| 指标 | 要求 |
|------|------|
| 搜索延迟 | < 500ms |
| 并发支持 | 支持50+并发检索 |

### 3.3 安全

| 措施 | 说明 |
|------|------|
| 访问控制 | 按组织/角色细分客户信息访问权限 |
| 认证 | API Key + JWT |
| 数据隔离 | 多租户数据隔离 |

### 3.4 可用性

| 指标 | 要求 |
|------|------|
| SLA | 99.9% |
| 故障恢复 | < 1小时 |
| 数据备份 | 每日增量，每周全量 |

---

## 4. 系统架构

### 4.1 整体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CustomerCollector System                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      人工校验队列                                       │   │
│  │   运营人员核对客户信息与原始来源是否一致                             │   │
│  │   校验通过 → 客户标记为"已校验"，允许检索                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Policy Collector 联动                              │   │
│  │   客户类型 → 匹配相关政策                                            │   │
│  │   历史项目 → 关联当时政策                                            │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Storage Layer                                     │   │
│  │  File Storage (原文) │ Vector DB (Qdrant) │ PostgreSQL (元数据)  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Egress Layer                                     │   │
│  │  REST API │ Python SDK │ Webhook                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**与Policy Collector联动**：
```
[客户登记] → [客户类型] → [Policy Collector检索] → [返回相关政策]
                                              ↓
[历史项目] → [项目类型] → [Policy Collector检索] → [返回当时政策]
```

### 4.2 数据流

```
[用户发现客户] → [客户登记] → [待校验状态]
                                      ↓
[补充详情] → [人工校验队列] → [校验通过]
                                      ↓
[客户查询] → [政策联动检索] → [返回客户+政策]
```

---

## 5. 技术方案

### 5.1 技术栈（全开源免费）

| 层级 | 组件 | 开源协议 |
|------|------|----------|
| 向量存储 | Qdrant | Apache 2.0 |
| 关系型 | PostgreSQL / SQLite | PostgreSQL License |
| Embedding | BGE-M3 | MIT |
| Reranker | BGE-Reranker-v2-m3 | MIT |
| LLM | DeepSeek-V4 / Qwen2.5 | MIT / Apache 2.0 |
| 容器 | Docker | Apache 2.0 |

**与Policy Collector共用技术栈，便于联动**

### 5.2 数据模型

#### customers（客户主表）
```sql
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    customer_code VARCHAR(50) UNIQUE NOT NULL,  -- CUS-2024-001

    name TEXT NOT NULL,
    customer_type VARCHAR(50) NOT NULL,  -- '高等教育'/'基础教育'/'教育局'/'培训机构'
    level VARCHAR(20),  -- '省级'/'市级'/'区县级'/'校级'
    region VARCHAR(100),  -- 省/市/区
    address TEXT,

    contact_name VARCHAR(100),
    contact_phone VARCHAR(50),
    contact_email VARCHAR(100),
    contact_position VARCHAR(100),

    source_type VARCHAR(30),  -- '官方渠道'/'公开数据'/'实地拜访'/'客户联系'/'展会会议'
    source_url TEXT,  -- 信息来源URL

    -- 人工校验状态
    verification_status VARCHAR(20) DEFAULT 'unverified',
    verified_at TIMESTAMP,
    verified_by UUID,

    notes TEXT,  -- 备注

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### customer_needs（需求痛点表）
```sql
CREATE TABLE customer_needs (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers(id),

    need_type VARCHAR(50) NOT NULL,  -- '基础设施'/'教学应用'/'数据治理'/'安全管理'/'运维服务'/'移动办公'/'其他'
    description TEXT NOT NULL,  -- 原文记录，不摘要
    source VARCHAR(50),  -- '客户访谈'/'问卷'/'历史资料'/'公开信息'

    priority VARCHAR(10) DEFAULT '中',  -- '高'/'中'/'低'

    related_policy_id UUID,  -- 关联的政策（引用Policy Collector）

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### customer_projects（历史项目表）
```sql
CREATE TABLE customer_projects (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers(id),

    project_name VARCHAR(200) NOT NULL,
    project_type VARCHAR(50),  -- '基础设施'/'教学应用'/'数据治理'/'安全'/'运维'
    project_year INTEGER,  -- 实施年份
    project_amount DECIMAL(15,2),  -- 项目金额（元）
    vendor VARCHAR(200),  -- 供应商
    vendor_is_competitor BOOLEAN DEFAULT false,  -- 是否为竞争对手

    description TEXT,  -- 项目内容描述

    status VARCHAR(20) DEFAULT '已完成',  -- '在建'/'已完成'/'运维中'/'已到期'/'待续期'
    acceptance_date DATE,  -- 验收日期
    expire_date DATE,  -- 运维到期日期

    related_policy_id UUID,  -- 项目当时依据的政策

    customer_feedback TEXT,  -- 客户评价

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### customer_systems（现有系统表）
```sql
CREATE TABLE customer_systems (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers(id),

    system_name VARCHAR(200) NOT NULL,  -- 系统名称
    system_type VARCHAR(50),  -- '基础设施'/'教学应用'/'数据治理'/'安全'/'运维'
    vendor VARCHAR(200),  -- 供应商
    vendor_is_competitor BOOLEAN DEFAULT false,  -- 是否为竞争对手

    build_year INTEGER,  -- 建设年份
    contract_amount DECIMAL(15,2),  -- 合同金额

    maintenance_expire_date DATE,  -- 运维到期时间

    customer_satisfaction VARCHAR(10),  -- '高'/'中'/'低'
    improvement_points TEXT,  -- 待改进点（客户反馈）

    notes TEXT,  -- 备注

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### customer_policy_links（客户政策关联表）
```sql
CREATE TABLE customer_policy_links (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers(id),
    policy_id UUID,  -- 关联Policy Collector的政策ID

    link_type VARCHAR(30) NOT NULL,  -- '适用政策'/'历史项目关联'/'需求支撑'

    confidence FLOAT DEFAULT 1.0,
    evidence TEXT,  -- 关联依据

    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(customer_id, policy_id, link_type)
);
```

#### customer_analyses（多角色分析结果表）
```sql
CREATE TABLE customer_analyses (
    id UUID PRIMARY KEY,
    analysis_id VARCHAR(50) UNIQUE NOT NULL,  -- ANA-2024-089-001

    customer_id UUID REFERENCES customers(id),

    trigger VARCHAR(20) DEFAULT 'manual',  -- 'manual'/'auto'/'scheduled'

    -- 各角色分析结果（JSON存储）
    sales_analysis JSONB,
    presales_analysis JSONB,
    implementation_analysis JSONB,
    after_sales_analysis JSONB,
    client_decision_maker_analysis JSONB,
    client_user_analysis JSONB,

    -- 综合摘要
    overall_score FLOAT,
    key_insights TEXT[],
    priority_actions TEXT[],

    created_at TIMESTAMP DEFAULT NOW()
);
```

#### after_sales_records（售后记录表）
```sql
CREATE TABLE after_sales_records (
    id UUID PRIMARY KEY,
    customer_id UUID REFERENCES customers(id),

    record_type VARCHAR(30) NOT NULL,  -- '工单'/'故障'/'续费'
    record_date DATE NOT NULL,

    -- 工单相关
    ticket_id VARCHAR(50),
    ticket_type VARCHAR(50),  -- '咨询'/'投诉'/'故障申报'
    ticket_status VARCHAR(20),  -- '待处理'/'处理中'/'已解决'
    response_time INTEGER,  -- 响应时间（小时）
    resolution_time INTEGER,  -- 解决时间（小时）
    satisfaction_score INTEGER,  -- 客户满意度评分(1-5)

    -- 故障相关
    fault_type VARCHAR(50),  -- '系统故障'/'网络故障'/'数据异常'
    fault_duration INTEGER,  -- 故障持续时间（分钟）
    fault_cause TEXT,  -- 故障原因

    -- 续费相关
    renewal_id VARCHAR(50),
    renewal_type VARCHAR(30),  -- '系统续费'/'运维续费'/'升级续费'
    renewal_amount DECIMAL(15,2),  -- 续费金额
    renewal_result VARCHAR(20),  -- '成功'/'失败'/'洽谈中'

    description TEXT,  -- 详情描述
    handler VARCHAR(100),  -- 处理人

    created_at TIMESTAMP DEFAULT NOW()
);
```

### 5.3 API规格

#### 检索客户
```
GET /api/v1/customers/search?q={query}&customer_type={type}&region={region}&sort={sort}
```

**参数说明**：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| q | string | - | 检索关键词 |
| customer_type | string | - | 客户类型 |
| region | string | - | 地区 |
| need_type | string | - | 需求类型 |
| sort | string | `updated_at` | 排序方式 |
| limit | int | 10 | 返回数量 |
| offset | int | 0 | 分页偏移 |

**响应**：
```json
{
  "success": true,
  "query": "高校 数据治理",
  "total": 156,
  "results": [
    {
      "customer_code": "CUS-2024-089",
      "name": "某某大学",
      "customer_type": "高等教育",
      "region": "北京市",
      "verification_status": "verified",
      "relevance_score": 0.95,
      "recent_needs": ["数据治理平台建设", "数据安全体系建设"],
      "recent_projects": ["智慧校园一期", "数据中心建设"]
    }
  ]
}
```

**说明**：仅返回 `verification_status = 'verified'` 的已校验客户

#### 获取客户详情（含政策联动）
```
GET /api/v1/customers/{customer_code}?include_needs=true&include_projects=true&include_policies=true
```

**响应**：
```json
{
  "success": true,
  "customer": {
    "customer_code": "CUS-2024-089",
    "name": "某某大学",
    "customer_type": "高等教育",
    "level": "省级",
    "region": "北京市",
    "contact_name": "张老师",
    "contact_phone": "010-xxxx",
    "verification_status": "verified",
    "verified_at": "2024-06-20T10:00:00Z"
  },
  "needs": [
    {
      "need_type": "数据治理",
      "description": "需要建设统一的数据中台，实现全校数据的统一管理...",
      "priority": "高",
      "related_policies": ["POL-2024-089", "POL-2023-045"]
    }
  ],
  "projects": [...],
  "related_policies": [...],
  "customer_actions": [...]
}
```

#### 登记客户
```
POST /api/v1/customers/discover
```

**请求**：
```json
{
  "name": "某某大学",
  "customer_type": "高等教育",
  "level": "省级",
  "region": "北京市",
  "address": "北京市海淀区...",
  "source_type": "实地拜访",
  "source_url": "https://www.xxx.edu.cn/..."
}
```

**响应**：
```json
{
  "success": true,
  "customer": {
    "customer_code": "CUS-2024-089",
    "verification_status": "unverified"
  }
}
```

#### 补充客户详情
```
PUT /api/v1/customers/{customer_code}/details
```

**请求**：
```json
{
  "contact_name": "张老师",
  "contact_phone": "010-xxxx",
  "contact_email": "zhang@example.edu.cn",
  "contact_position": "信息化主任"
}
```

#### 校验客户
```
POST /api/v1/customers/{customer_code}/verify
```

**请求**：
```json
{
  "status": "verified",
  "comment": "信息核对无误"
}
```

#### 添加需求痛点
```
POST /api/v1/customers/{customer_code}/needs
```

**请求**：
```json
{
  "need_type": "数据治理",
  "description": "需要建设统一的数据中台，实现全校数据的统一管理，解决数据孤岛问题...",
  "source": "客户访谈",
  "priority": "高"
}
```

#### 添加历史项目
```
POST /api/v1/customers/{customer_code}/projects
```

**请求**：
```json
{
  "project_name": "智慧校园一期",
  "project_type": "智慧校园",
  "project_year": 2023,
  "project_amount": 15000000,
  "vendor": "某某科技",
  "vendor_is_competitor": false,
  "description": "建设内容包括智慧教学、智慧管理、智慧服务...",
  "status": "已完成",
  "acceptance_date": "2023-12-01"
}
```

#### 添加现有系统
```
POST /api/v1/customers/{customer_code}/systems
```

**请求**：
```json
{
  "system_name": "智慧校园平台",
  "system_type": "教学应用",
  "vendor": "竞品公司",
  "vendor_is_competitor": true,
  "build_year": 2021,
  "contract_amount": 8000000,
  "maintenance_expire_date": "2024-12-31",
  "customer_satisfaction": "中",
  "improvement_points": "系统响应慢，部分功能不满足当前需求",
  "notes": "客户表示有替换意愿"
}
```

#### 获取客户完整画像
```
GET /api/v1/customers/{customer_code}/profile
```

**响应**：
```json
{
  "success": true,
  "customer": {
    "customer_code": "CUS-2024-089",
    "name": "某某大学",
    "customer_type": "高等教育",
    "level": "省级",
    "region": "北京市"
  },
  "contact": {
    "name": "张老师",
    "position": "信息化主任",
    "phone": "010-xxxx"
  },
  "existing_systems": [
    {
      "system_name": "智慧校园平台",
      "vendor": "竞品公司",
      "vendor_is_competitor": true,
      "customer_satisfaction": "中",
      "improvement_points": "系统响应慢"
    }
  ],
  "historical_projects": [...],
  "needs": [...],
  "related_policies": [
    {
      "citation_id": "POL-2024-089",
      "title": "关于加快推进教育信息化建设的指导意见",
      "match_reason": "高等教育类型适用"
    }
  ]
}
```

#### 政策联动检索
```
GET /api/v1/customers/{customer_code}/related-policies?policy_type={type}
```

**响应**：
```json
{
  "success": true,
  "customer": {
    "customer_code": "CUS-2024-089",
    "name": "某某大学",
    "customer_type": "高等教育"
  },
  "related_policies": [
    {
      "citation_id": "POL-2024-089",
      "title": "关于加快推进教育信息化建设的指导意见",
      "match_reason": "高等教育类型适用",
      "relevance_score": 0.95
    }
  ]
}
```

#### 多角色智能体分析
```
POST /api/v1/customers/{customer_code}/analyze
```

**请求**：
```json
{
  "roles": ["sales", "presales", "implementation", "after_sales", "client_decision_maker", "client_user"],
  "trigger": "manual"
}
```

**响应**：
```json
{
  "success": true,
  "customer_code": "CUS-2024-089",
  "analysis_id": "ANA-2024-089-001",
  "analysis_time": "2024-06-20T10:00:00Z",
  "role_analyses": {
    "sales": {
      "budget_assessment": "高",
      "win_probability": 75,
      "recommended_actions": ["重点跟进信息化主任"]
    },
    "presales": {...},
    "implementation": {...},
    "after_sales": {...},
    "client_decision_maker": {...},
    "client_user": {...}
  },
  "summary": {
    "overall_score": 78,
    "key_insights": ["客户有明确替换意愿"],
    "priority_actions": ["准备差异化方案"]
  }
}
```

**说明**：
- `roles` 参数可指定只分析特定角色，默认为全部角色
- `trigger` 为 `manual` 表示手动触发
- 分析结果会被存储，支持历史对比

#### 添加售后记录
```
POST /api/v1/customers/{customer_code}/after-sales
```

**请求**：
```json
{
  "record_type": "工单",
  "record_date": "2024-06-15",
  "ticket_id": "TKT-2024-001",
  "ticket_type": "故障申报",
  "ticket_status": "已解决",
  "response_time": 2,
  "resolution_time": 8,
  "satisfaction_score": 4,
  "description": "用户反映系统登录缓慢，经排查为数据库索引问题",
  "handler": "张三"
}
```

#### 获取售后记录
```
GET /api/v1/customers/{customer_code}/after-sales?record_type={type}
```

**响应**：
```json
{
  "success": true,
  "customer_code": "CUS-2024-089",
  "records": [
    {
      "record_type": "工单",
      "record_date": "2024-06-15",
      "ticket_type": "故障申报",
      "ticket_status": "已解决",
      "resolution_time": 8,
      "satisfaction_score": 4
    },
    {
      "record_type": "续费",
      "record_date": "2024-01-01",
      "renewal_type": "运维续费",
      "renewal_amount": 500000,
      "renewal_result": "成功"
    }
  ],
  "summary": {
    "total_tickets": 15,
    "avg_resolution_time": 6.5,
    "avg_satisfaction": 4.2,
    "total_renewals": 3,
    "renewal_amount_total": 1500000
  }
}
```

---

## 6. 与Policy Collector联动方案

### 6.1 联动架构

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   CustomerCollector              PolicyCollector                 │
│   ┌─────────────────┐           ┌─────────────────┐            │
│   │  customers      │◄─────────►│  documents      │            │
│   │  customer_needs │           │  policy_relations│           │
│   │  customer_projects│         │                 │            │
│   └─────────────────┘           └─────────────────┘            │
│            │                              │                      │
│            │    customer_policy_links    │                      │
│            └──────────────────────────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 联动场景

| 场景 | 说明 | 实现方式 |
|------|------|----------|
| 客户查询时展示相关政策 | 查看客户时自动展示适用政策 | 客户类型 → Policy检索 |
| 政策查询时反向展示客户 | 查看政策时展示相关客户 | 政策类型 → 客户检索 |
| 需求引用政策 | 客户需求可关联政策作为支撑 | need.related_policy_id |
| 项目引用政策 | 历史项目可关联当时的政策 | project.related_policy_id |

### 6.3 联动实现

通过 `customer_policy_links` 表建立关联：
- 客户类型匹配政策类型时自动建立关联
- 用户可手动建立/删除关联
- 关联时记录关联依据（evidence）

---

## 7. 实施计划

### 7.1 阶段划分

| 阶段 | 周期 | 内容 | 交付物 |
|------|------|------|--------|
| 阶段一 | 1周 | 核心存储 + 客户登记 + 基础检索 | 可登记客户、可检索的原型 |
| 阶段二 | 1周 | 需求/项目记录 + 政策联动 + SDK | 完整的客户画像体系 |
| 阶段三 | 1.5周 | 多角色智能体 + 人工校验 + 部署 | 生产可用系统 |

### 7.2 Week 1：核心能力

**Day 1-2**：项目初始化
- 项目结构搭建
- Docker Compose 配置
- 数据库表结构创建

**Day 3-4**：客户登记
- 客户发现API
- 基本信息管理
- 去重逻辑

**Day 5-7**：基础检索
- Qdrant 部署
- BGE-M3 Embedding 集成
- 客户检索API

### 7.3 Week 2：高级功能

**Day 8-9**：需求/项目记录
- 需求痛点API
- 历史项目API + 现有系统API
- 向量索引

**Day 10-11**：政策联动
- Policy Collector接口对接
- 联动检索逻辑
- 关联管理

**Day 12-14**：SDK封装
- Python SDK
- 文档

### 7.4 Week 3-3.5：多角色智能体

**Day 15-17**：多角色智能体框架
- 智能体架构设计
- 销售/售前/实施 Agent实现
- 向量检索 + LLM分析

**Day 18-20**：售后 + 客户视角 Agent
- 售后 Agent实现
- 客户决策者/使用者 Agent实现
- 分析结果存储

**Day 21**：部署
- 本地测试
- 阿里云部署

**Day 22**：上线
- 监控配置
- 交接文档

---

## 8. 验收标准

### 8.1 功能验收（对应三大痛点）

| 痛点 | 功能 | 验收条件 |
|------|------|----------|
| **历史项目不清晰** | 现有系统记录 | 能记录客户现有系统，包括供应商、满意度 |
| **历史项目不清晰** | 历史项目记录 | 能记录客户过往项目，包括供应商、金额、建设内容 |
| **政策匹配困难** | 政策联动检索 | 输入客户类型，能返回相关政策列表及引用 |
| **信息分散难整合** | 客户检索 | 输入关键词，能检索到分散在多个渠道的客户信息 |
| **多角色分析** | 六大角色分析 | 销售/售前/实施/售后/决策者/使用者视角均能输出分析 |
| 需求记录 | 需求痛点记录 | 能记录客户需求痛点，原文保存 |
| 人工校验 | 校验状态管理 | 运营人员能校验客户信息，状态正确流转 |
| SDK调用 | Python SDK | SDK能完成检索和详情查询 |

### 8.2 准确性验收

| 指标 | 验收条件 |
|------|----------|
| 人工校验 | 客户信息必须经过人工校验才能被检索 |
| 校验状态 | verified/unverified 状态正确记录 |
| 原文记录 | 需求/痛点原文保存，不摘要不改写 |

### 8.3 性能验收

| 指标 | 验收条件 |
|------|----------|
| 搜索延迟 | P95 < 500ms |
| 并发 | 支持50并发检索 |

---

## 9. 成本估算

### 阿里云部署（与Policy Collector共用）

| 组件 | 配置 | 月费用(元) |
|------|------|-----------|
| ECS | 2核4G | 200-300 |
| RDS PostgreSQL | 2核4G | 300-500 |
| 系统盘+数据盘 | 140GB SSD | 70 |
| 带宽 | 5Mbps | 50 |
| **合计** | | **570-920** |

### 多角色智能体额外成本

| 组件 | 配置 | 月费用(元) |
|------|------|-----------|
| LLM API调用 | 视分析频率 | 约200-500 |
| **合计增加** | | **200-500** |

### 节省方案
- 本地测试：全部Docker，0成本
- 初期：可用抢占式实例，降低60-80%
- 与Policy Collector共用ECS和RDS
- LLM调用：使用DeepSeek-V4（低成本）

---

## 10. 风险与对策

| 核心痛点 | 风险 | 对策 |
|------|------|------|
| 历史项目不清晰 | 项目信息收集困难 | 提供批量导入模板、历史资料复用 |
| 政策匹配困难 | 返回不相关政策 | 多维度匹配（类型+地区+需求）+ Rerank优化 |
| 信息分散难整合 | 客户数据不足 | 提供多渠道接入（手动/导入）、定期回访更新 |
| 多角色智能体 | LLM分析结果不准确 | 设置分析质量阈值、人工抽检 |
| 多角色智能体 | 分析耗时过长 | 并行分析、优化prompt、支持异步 |

---

## 11. 附录

### A. 客户类型说明

| 类型 | 说明 | 适用政策类型 |
|------|------|--------------|
| 高等教育 | 大学、高职院校 | 高等教育政策 |
| 基础教育 | 中小学、幼儿园 |基础教育政策 |
| 教育局 | 省/市/区县教育局 | 教育管理政策 |
| 培训机构 | 校外培训机构 | 培训监管政策 |
| 其他 | 其他教育相关 | 通用教育政策 |

### B. 需求类型说明

| 类型 | 说明 | 关键词 |
|------|------|--------|
| 基础设施 | 网络、服务器、存储、机房 | 网络升级、服务器扩容、机房建设 |
| 教学应用 | 教学平台、实训系统、智慧教室 | 智慧教学、在线实训、虚拟仿真 |
| 数据治理 | 数据中台、数据标准、数据安全 | 数据中台、主数据、数据安全、等保 |
| 安全管理 | 等保、分级保护、安全运营 | 等保2.0、分级保护、安全运营中心 |
| 运维服务 | 运维平台、服务水平、巡检 | 运维外包、SLA、巡检报告 |
| 移动办公 | 移动端、应用集成、即时通讯 | 移动校园、企业微信、钉钉集成 |

### C. 项目状态说明

| 状态 | 说明 | 后续动作 |
|------|------|----------|
| 在建 | 项目正在实施中 | 关注进度 |
| 已完成 | 项目已验收 | 客户评价 |
| 运维中 | 在运维服务期内 | 定期巡检 |
| 已到期 | 运维服务已到期 | 续期洽谈 |
| 待续期 | 有续期意向 | 主动跟进 |

### D. 竞争对手分析说明

| 字段 | 说明 |
|------|------|
| vendor_is_competitor | 标记供应商是否为竞争对手 |
| customer_satisfaction | 客户对现有系统的满意度 |
| improvement_points | 客户反馈的不足之处（销售突破口） |

**分析价值**：
- 满意度低的系统 → 替换机会
- 竞争对手的系统 → 了解竞争态势
- 待改进点 → 制定差异化方案

### E. 多角色智能体Prompt设计指导

**设计原则**：
1. 每个角色有明确的身份定义和分析目标
2. 分析输出结构化，便于后续聚合
3. 结合客户画像 + 政策引用 + 历史案例

**示例Prompt结构**：

```
# 角色定义
你是一名资深[角色]，负责分析[分析目标]。

# 输入信息
客户信息：
- 名称：[name]
- 类型：[type]
- 地区：[region]
...

现有系统：
- [system_list]

历史项目：
- [project_list]

需求痛点：
- [needs_list]

相关政策：
- [policies]

# 分析任务
请从[角色]视角分析以上信息，输出：
1. [分析维度1]
2. [分析维度2]
3. [综合建议]

# 输出格式
{
  "analysis": {...},
  "confidence": 0.85
}
```

