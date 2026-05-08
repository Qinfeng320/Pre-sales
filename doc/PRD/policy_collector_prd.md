# 政策搜集智能体系统 PRD

| 版本 | 日期 | 作者 | 说明 |
|------|------|------|------|
| v1.0 | 2026-05-08 | - | 初始版本 |

---

## 1. 概述

### 1.1 产品背景

需要一个政策搜集智能体系统，作为文档生成的预处理入口。核心场景是：输入客户 + 产品，自动匹配相关政策并提供原文引用。

**核心约束**：
- **准确性100%**：政策信息少，1%错误率都不可接受
- **引用全文**：必须返回完整原文，不接受摘要
- **人工校验**：政策内容由人工核对保证准确性

### 1.2 产品目标

1. 建立政策RAG知识库，支持客户+产品检索匹配
2. **确认政策与政策之间的关联**（上位法/下位法、系列政策、同源机构等）
3. 通过**人工校验**保证政策内容100%准确
4. 记录B端客户在政策下的实践行为，作为政策落地的参考案例

### 1.3 范围

**包含**：
- 政策发现与登记（用户发现政策URL后登记）
- 人工校验（运营人员核对原文保证准确性）
- 政策关联（Relation Agent自动发现关联）
- 向量检索（RAG）
- B端客户行为记录
- REST API + SDK输出

**不包含**：
- 自动爬虫采集（政策正文由用户手动补充）
- 文档生成（作为下游系统）

---

## 2. 功能需求

### 2.1 政策发现与登记

| 功能 | 描述 | 优先级 |
|------|------|--------|
| URL发现 | 用户搜索发现政策，记录政策URL | P0 |
| 来源验证 | 验证URL是第一手来源（非转载），仅允许政府官方域名 | P0 |
| 手动补充 | 政策正文内容由用户后续手动添加 | P0 |
| 去重引用 | 相同政策从不同来源入库时，建立引用关系 | P1 |

**来源验证规则**：
- 仅允许政府官方域名（gov.cn等）
- 必须是一手来源，不接受转载/聚合网站
- 验证方式：域名白名单 + 来源类型判断（政府/官方机构）

**数据校验规则**：
- 发现时仅记录：标题、原始URL、发布时间、发布机构（来源页面上有即可）
- 正文内容由用户在发现后手动补充

### 2.2 政策关联

**Relation Agent**：自动发现政策间的关联关系

| 关联类型 | 说明 | 示例 |
|----------|------|------|
| 上位法/下位法 | 法律层级关系 | 宪法→法律→行政法规→部门规章 |
| 系列政策 | 同一主题延续 | "稳就业"系列政策 |
| 继承/修订 | 时间线更新 | 旧政策废止→新政策替代 |
| 同源机构 | 同一发布机构 | 财政部发布的多个政策 |
| 主题相关 | 关键词/行业相似 | 同属"科技创新"领域 |
| 引用关系 | 正文引用其他政策 | A政策引用B政策 |

**识别方式**：
- 自动识别：标题相似度、关键词重叠、发布机构+时间线聚类
- 手动标记：用户可手动建立关联

### 2.3 人工校验

**政策内容准确性由人工校验保证**：

| 阶段 | 说明 |
|------|------|
| 登记时 | 仅记录元信息（标题/URL/发布时间），无需校验 |
| 补充正文后 | 进入人工校验队列 |
| 人工确认 | 运营人员核对原文与系统记录是否一致 |
| 校验通过 | 政策标记为"已校验"，允许检索 |

**校验状态**：
| 状态 | 说明 |
|------|------|
| unverified | 未校验（正文刚补充或校验未通过） |
| verified | 已校验通过，允许检索 |

### 2.4 时效性与排序

**搜索范围**：
- 仅搜索 **5年以内** 发布的政策
- 超过5年的政策归档但默认不展示

**排序规则**：
- 检索结果默认按 **发布时间倒序**（最新在前）
- 支持按相关性/发布时间切换排序

### 2.5 B端客户行为

| 功能 | 描述 |
|------|------|
| 记录行为 | 记录客户在某个政策下做的具体事项（申报/领补贴/享受优惠/合规整改） |
| 行为引用 | 行为描述必须引用政策原文条款 |
| 同行参考 | 展示同行业其他客户在这个政策下的实践 |

### 2.6 检索匹配

**核心场景**：
```
输入: 客户行业 + 产品信息
↓检索匹配政策
返回: 主政策 + 关联政策 + 客户实践案例（均提供原文引用）
```

**检索方式**：
- 向量检索（语义相似度）
- 关键词过滤（行业/产品）
- 混合检索（向量 + BM25 + RRF融合 + Rerank）

**检索范围**：
- 仅返回 **5年内** 发布的政策
- 按 **发布时间倒序**（最新在前）

---

## 3. 非功能需求

### 3.1 准确性

| 指标 | 要求 |
|------|------|
| 内容准确率 | 100%（不生成、不摘要、不改写） |
| 引用溯源 | 每个政策可追溯到原始URL |
| 人工校验 | 政策必须经过人工校验才能被检索 |

### 3.2 性能

| 指标 | 要求 |
|------|------|
| 搜索延迟 | < 500ms |
| 并发支持 | 支持50+并发检索 |

### 3.3 安全

| 措施 | 说明 |
|------|------|
| 来源验证 | 仅允许政府官方域名（gov.cn等一手来源） |
| 认证 | API Key + JWT |

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
│                        PolicyCollector System                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      人工校验队列                                       │   │
│  │   运营人员核对原文与系统记录是否一致                                    │   │
│  │   校验通过 → 政策标记为"已校验"，允许检索                          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      Relation Agent                                     │   │
│  │   自动发现政策间的关联关系                                            │   │
│  │   上位法/下位法、系列政策、同源机构、主题相关、引用关系             │   │
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

**流程说明**：
1. 用户发现政策 → 登记元信息（标题/URL/发布时间）
2. 用户手动补充正文 → 进入人工校验队列
3. 运营人员校验通过 → 政策允许检索
4. Relation Agent 自动发现政策关联

### 4.2 数据流

```
[用户发现政策URL] → [政策登记] → [待校验状态]
                                        ↓
[用户补充正文] → [人工校验队列] → [校验通过]
                                        ↓
                    [Relation Agent] → [关联入库] ←→ [Qdrant向量索引]
                                              ↓
[客户+产品查询] → [混合检索] → [Rerank] → [返回结果+引用]
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

### 5.2 数据模型

#### documents（政策主表）
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    citation_id VARCHAR(50) UNIQUE NOT NULL,  -- POL-2024-001

    title TEXT NOT NULL,
    source_url TEXT NOT NULL, -- 必须是政府官方一手来源
    publish_date DATE NOT NULL,
    issuing_authority VARCHAR(200),
    policy_type VARCHAR(50),

    source_domain VARCHAR(100), -- 来源域名

    content TEXT, -- 正文内容（手动补充）
    content_pending BOOLEAN DEFAULT true, -- 正文是否待补充

    -- 人工校验状态
    verification_status VARCHAR(20) DEFAULT 'unverified', -- 'unverified' | 'verified'
    verified_at TIMESTAMP,
    verified_by UUID,

    effective_date DATE, -- 政策生效日期

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### document_sections（段落表）
```sql
CREATE TABLE document_sections (
    id UUID PRIMARY KEY,
    document_id UUID REFERENCES documents(id),

    section_index INTEGER NOT NULL,
    section_title VARCHAR(200),
    start_char_offset INTEGER NOT NULL,
    end_char_offset INTEGER NOT NULL,
    content_text TEXT NOT NULL
);
```

#### policy_relations（政策关联表）
```sql
CREATE TABLE policy_relations (
    id UUID PRIMARY KEY,
    doc_id_1 UUID REFERENCES documents(id),
    doc_id_2 UUID REFERENCES documents(id),
    relation_type VARCHAR(30) NOT NULL, -- '上位法/下位法','系列政策','继承/修订','同源机构','主题相关','引用'

    confidence FLOAT DEFAULT 1.0, -- 0.0-1.0，仅自动识别时 < 1.0
    source VARCHAR(20) DEFAULT 'auto', -- 'auto' | 'manual'
    evidence TEXT, -- 关联依据，如"标题相似度0.92"

    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE(doc_id_1, doc_id_2, relation_type)
);
```

#### customer_policy_actions（客户行为表）
```sql
CREATE TABLE customer_policy_actions (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    customer_name VARCHAR(200),
    customer_industry VARCHAR(100),
    policy_id UUID REFERENCES documents(id),

    action_type VARCHAR(50),
    action_detail TEXT,
    action_date DATE,
    reference_quote TEXT,
    reference_section INTEGER,

    created_by UUID,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 5.3 API规格

#### 检索政策
```
GET /api/v1/policies/search?q={query}&policy_type={type}&sort={sort}
```

**参数说明**：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| q | string | - | 检索关键词 |
| policy_type | string | - | 政策类型 |
| sort | string | `publish_date` | 排序方式：`relevance` \| `publish_date` |
| limit | int | 10 | 返回数量 |
| offset | int | 0 | 分页偏移 |

**响应**：
```json
{
  "success": true,
  "query": "制造业 工业机器人",
  "total": 156,
  "results": [
    {
      "citation_id": "POL-2024-089",
      "title": "关于加快制造业绿色转型的指导意见",
      "source": "工业和信息化部",
      "publish_date": "2024-06-15",
      "verification_status": "verified",
      "relevance_score": 0.95,
      "excerpt": "（一）加快节能技术装备推广应用..."
    }
  ]
}
```

**说明**：仅返回 `verification_status = 'verified'` 的已校验政策

#### 获取政策详情（含关联）
```
GET /api/v1/policies/{citation_id}?include_relations=true&include_customer_actions=true
```

**响应**：
```json
{
  "success": true,
  "document": {
    "citation_id": "POL-2024-089",
    "title": "关于加快制造业绿色转型的指导意见",
    "content": "完整原文...",
    "sections": [...],
    "verification_status": "verified",
    "verified_at": "2024-06-20T10:00:00Z"
  },
  "related_policies": [...],
  "customer_actions": [...]
}
```

#### 获取段落（精准引用）
```
GET /api/v1/policies/{citation_id}/sections/{section_index}
```

#### 登记政策发现
```
POST /api/v1/policies/discover
```

**请求**：
```json
{
  "title": "关于加快制造业绿色转型的指导意见",
  "source_url": "https://www.miit.gov.cn/...",
  "publish_date": "2024-06-15",
  "issuing_authority": "工业和信息化部",
  "policy_type": "规范性文件",
  "effective_date": "2024-07-01"
}
```

**响应**：
```json
{
  "success": true,
  "document": {
    "citation_id": "POL-2024-089",
    "content_pending": true,
    "verification_status": "unverified"
  }
}
```

#### 补充政策正文
```
PUT /api/v1/policies/{citation_id}/content
```

**请求**：
```json
{
  "content": "完整正文内容..."
}
```

**说明**：补充正文后进入人工校验队列

#### 校验政策
```
POST /api/v1/policies/{citation_id}/verify
```

**请求**：
```json
{
  "status": "verified",
  "comment": "核对通过"
}
```

#### 记录客户行为
```
POST /api/v1/customer-actions
```

---

## 6. 实施计划

### 6.1 阶段划分

| 阶段 | 周期 | 内容 | 交付物 |
|------|------|------|--------|
| 阶段一 | 2周 | 核心存储 + 政策登记 + 向量检索 | 可登记政策、可检索的原型 |
| 阶段二 | 1周 | 人工校验 + 关联管理 + SDK | 准确性保障体系 |
| 阶段三 | 1周 | 本地测试 + 阿里云部署 | 生产可用系统 |

### 6.2 Week 1-2：核心能力

**Day 1-2**：项目初始化
- 项目结构搭建
- Docker Compose 配置
- 数据库表结构创建

**Day 3-4**：来源验证
- 政府域名白名单配置
- 来源类型验证逻辑
- URL一手来源判断

**Day 5-7**：政策登记
- 政策发现API
- 来源验证流程
- 待补充状态管理

**Day 8-10**：向量检索
- Qdrant 部署
- BGE-M3 Embedding 集成
- 混合检索实现

**Day 11-14**：API开发
- FastAPI 路由
- 搜索API
- 政策详情API

### 6.3 Week 3：校验 + 关联

**Day 15-17**：人工校验
- 校验队列API
- 运营界面
- 校验状态管理

**Day 18-19**：关联管理
- Relation Agent
- 关联入库逻辑
- 关联展示

**Day 20-21**：SDK封装
- Python SDK
- 文档

### 6.4 Week 4：部署

**Day 22-23**：本地测试
- 全流程测试
- 性能测试

**Day 24-26**：阿里云部署
- ECS + RDS
- Docker Compose 生产配置

**Day 27-28**：上线
- 监控配置
- 交接文档

---

## 7. 验收标准

### 7.1 功能验收

| 功能 | 验收条件 |
|------|----------|
| 政策发现 | 能登记政策元信息，验证来源为政府官方一手 |
| 手动补充 | API能接收正文补充，进入校验队列 |
| 人工校验 | 运营人员能校验政策，状态正确流转 |
| 向量检索 | 输入行业+产品关键词，能返回相关政策（仅已校验） |
| 关联查询 | 主政策返回关联政策列表，关联类型正确 |
| 客户行为 | 能记录并查询客户在政策下的行为 |
| SDK调用 | Python SDK能完成检索和详情查询 |

### 7.2 准确性验收

| 指标 | 验收条件 |
|------|----------|
| 人工校验 | 政策必须经过人工校验才能被检索 |
| 校验状态 | verified/unverified 状态正确记录 |
| 关联发现 | Relation Agent能正确发现政策间的关联 |

### 7.3 性能验收

| 指标 | 验收条件 |
|------|----------|
| 搜索延迟 | P95 < 500ms |
| 并发 | 支持50并发检索 |

---

## 8. 成本估算

### 阿里云部署

| 组件 | 配置 | 月费用(元) |
|------|------|-----------|
| ECS | 2核4G | 200-300 |
| RDS PostgreSQL | 2核4G | 300-500 |
| 系统盘+数据盘 | 140GB SSD | 70 |
| 带宽 | 5Mbps | 50 |
| **合计** | | **570-920** |

### 节省方案
- 本地测试：全部Docker，0成本
- 初期：可用抢占式实例，降低60-80%

---

## 9. 风险与对策

| 风险 | 影响 | 对策 |
|------|------|------|
| 用户发现政策困难 | 政策发现数量不足 | 提供政策线索提交功能、关键词推荐 |
| 人工校验效率低 | 政策积压无法检索 | 优化校验流程、提供批量校验 |
| 向量检索不准确 | 返回不相关政策 | Rerank、多路召回、人工标注优化 |

---

## 10. 附录

### A. 支持的政府网站白名单（初始）

```
gov.cn
nds.mof.gov.cn (财政部)
www.mohurd.gov.cn (住建部)
www.miit.gov.cn (工信部)
www.most.gov.cn (科技部)
www.moe.gov.cn (教育部)
www.nhc.gov.cn (卫健委)
http://www.moe.gov.cn/（教育部）

### B. 政策类型

- 法律
- 行政法规
- 部门规章
- 规范性文件
- 政策

### C. 客户行为类型

- 申报
- 领补贴
- 享受优惠
- 合规整改
- 购买了那些产品
