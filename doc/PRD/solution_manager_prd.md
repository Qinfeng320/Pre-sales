# 产品解决方案管理智能体系统 PRD

| 版本 | 日期 | 作者 | 说明 |
|------|------|------|------|
| v2.1 | 2026-05-08 | - | 新增Multi-Agent协作架构设计 |
| v2.0 | 2026-05-08 | - | 升级为Multi-Agent架构 |

---

## 1. 概述

### 1.1 产品背景

需要一个产品解决方案管理智能体系统，解决售前工程师**核心痛点**：

1. **方案编写耗时** - 每次都要从零开始写方案，花费大量时间在重复性工作上
2. **方案内容不统一** - 不同人写的方案差异大，质量参差不齐
3. **政策依据难引用** - 方案中的政策背景和政策引用难以准确获取
4. **客户需求脱节** - 方案内容与客户实际需求匹配度不高

**核心场景**：输入客户信息 + 需求，系统通过**Multi-Agent协作**自动生成定制化解决方案。每个解决方案模块都是一个独立的子智能体，通过智能体协作流程完成方案生成。

### 1.2 Multi-Agent架构总览

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           SolutionManager Orchestrator                               │
│                              (主智能体编排器)                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────┐   │
│  │                          Agent Collaboration Flow                              │   │
│  │                                                                              │   │
│  │    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐            │   │
│  │    │ PolicyAgent │ ───▶ │ NeedsAgent   │ ───▶ │ GoalsAgent   │            │   │
│  │    │ 政策背景     │      │ 需求分析     │      │ 建设目标     │            │   │
│  │    └──────────────┘      └──────────────┘      └──────────────┘            │   │
│  │          │                    │                     │                       │   │
│  │          │                    │                     ▼                       │   │
│  │          │                    │            ┌──────────────┐                 │   │
│  │          │                    │            │SolutionAgent│                 │   │
│  │          │                    │            │ 具体方案内容 │                 │   │
│  │          │                    │            └──────────────┘                 │   │
│  │          │                    │                     │                       │   │
│  │          ▼                    ▼                     ▼                       │   │
│  │    ┌──────────────────────────────────────────────────────────────┐        │   │
│  │    │           Supporting Agents (并行执行)                         │        │   │
│  │    │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │        │   │
│  │    │  │AfterSales   │  │  OpsAgent  │  │  TeamAgent  │          │        │   │
│  │    │  │ 售后服务   │  │  运维服务   │  │  交付团队   │          │        │   │
│  │    │  └─────────────┘  └─────────────┘  └─────────────┘          │        │   │
│  │    │                          ┌─────────────┐                    │        │   │
│  │    │                          │CasesAgent   │                    │        │   │
│  │    │                          │ 成功案例   │                    │        │   │
│  │    │                          └─────────────┘                    │        │   │
│  │    └──────────────────────────────────────────────────────────────┘        │   │
│  └────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

**Agent依赖关系**：

| Agent | 输入 | 输出 | 依赖Agent |
|-------|------|------|-----------|
| **PolicyAgent** | 客户类型、需求类型 | 政策背景、引用列表 | 无 |
| **NeedsAgent** | 政策背景、客户原始需求 | 需求分析报告 | PolicyAgent |
| **GoalsAgent** | 需求分析报告 | 建设目标列表 | NeedsAgent |
| **SolutionAgent** | 建设目标、客户约束 | 具体方案内容 | GoalsAgent |
| **AfterSalesAgent** | 项目规模、合同类型 | 售后服务方案 | SolutionAgent |
| **OpsAgent** | 项目复杂度、客户规模 | 运维服务方案 | SolutionAgent |
| **TeamAgent** | 项目类型、所需技能 | 交付团队方案 | SolutionAgent |
| **CasesAgent** | 客户画像、项目类型 | 成功案例列表 | PolicyAgent、NeedsAgent |

### 1.3 产品目标

1. **Multi-Agent协作** - 每个模块是独立智能体，通过编排器协调生成完整方案
2. **政策驱动需求分析** - 需求分析基于政策背景 + 客户实际需求
3. **目标导向方案设计** - 具体方案内容根据建设目标定制化生成
4. **所见即所得编辑** - 支持人工干预和调整，智能体实时响应修改
5. **积累成功案例** - 沉淀优质方案作为参考，提升整体方案水平

### 1.4 与前两个系统联动

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│   CustomerCollector              PolicyCollector              SolutionManager          │
│   ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐     │
│   │  customers      │         │  documents      │         │ Orchestrator    │     │
│   │  customer_needs │         │  policy_relations│         │    Agent        │     │
│   │  customer_projects│       │                 │         └────────┬────────┘     │
│   └────────┬────────┘         └────────┬────────┘                  │              │
│            │                           │                           │              │
│            │    customer profile       │    policy citations       │              │
│            └───────────────────────────┼───────────────────────────┘              │
│                                        │                                          │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.5 LLM选型策略

根据任务类型选择最适合的LLM：

| Agent | 推荐LLM | 原因 |
|-------|---------|------|
| PolicyAgent | **Qwen3.6-Plus** | 中文政策理解强，擅长政策解读和条款提取 |
| NeedsAgent | **Qwen3.6-Plus** | 中文需求理解强，能准确理解客户表达 |
| GoalsAgent | **DeepSeek-V4** | 推理能力强，擅长SMART目标分解 |
| SolutionAgent | **DeepSeek-V4** | 复杂方案设计和架构推理 |
| AfterSalesAgent | **Qwen3.6-Plus** | 服务方案中文表述 |
| OpsAgent | **Qwen3.6-Plus** | 运维服务中文表述 |
| TeamAgent | **Qwen3.6-Plus** | 团队描述中文表述 |
| CasesAgent | **Qwen3.6-Plus** | 案例分析中文理解 |

**LLM混合使用策略**：
- 中文理解/生成任务 → Qwen3.6-Plus
- 复杂推理/架构设计任务 → DeepSeek-V4

---

## 2. Agent详细设计

### 2.1 PolicyAgent（政策背景Agent）

**角色定义**：
```
你是一名政策分析专家，负责从政策角度为解决方案提供背景支撑。
你的职责是根据客户类型和需求，精准匹配相关政策，并提供原文引用。
```

**输入**：
```json
{
  "customer_type": "高等教育",
  "customer_region": "华东-上海市",
  "need_types": ["数据治理", "智慧校园"],
  "project_budget_range": "1000-2000万",
  "project_duration": "12个月"
}
```

**处理逻辑**：
1. 分析客户类型对应的政策适用性
2. 根据需求类型匹配相关政策领域
3. 调用PolicyCollector检索相关政策
4. 筛选5年内有效政策
5. 提取关键条款作为引用

**输出**：
```json
{
  "agent": "PolicyAgent",
  "status": "completed",
  "policy_background": [
    {
      "policy_id": "POL-2024-089",
      "title": "关于加快推进教育信息化建设的指导意见",
      "issuing_authority": "教育部",
      "publish_date": "2024-06-15",
      "relevance_score": 0.95,
      "key_statements": [
        "（一）加快教育数字化转型，推动数字技术与教育深度融合",
        "（三）推进教育数据共享开放，构建教育数据治理体系"
      ],
      "quoted_sections": [
        {
          "section_index": 3,
          "content": "（一）加快教育数字化转型，推动数字技术与教育深度融合...",
          "char_offset_start": 1024,
          "char_offset_end": 1156
        }
      ]
    }
  ],
  "executive_summary": "本方案符合《教育信息化2.0行动计划》和《数字中国建设整体布局规划》相关要求..."
}
```

**Prompt模板**：
```
# 角色
你是一名政策分析专家，负责为教育信息化解决方案提供政策背景支撑。

# 输入信息
客户类型：{customer_type}
客户地区：{customer_region}
需求类型：{need_types}
项目预算：{project_budget_range}
建设周期：{project_duration}

# 任务
1. 根据客户类型识别适用的政策框架
2. 提取与需求类型相关的政策条款
3. 分析政策对方案设计的指导意义
4. 生成政策背景综述

# 输出格式
{
  "policy_background": [...],
  "executive_summary": "..."
}

# 政策引用规范
- 必须引用原文，不得摘要
- 标注政策来源和文号
- 说明政策与方案的关联性
```

---

### 2.2 NeedsAgent（需求分析Agent）

**角色定义**：
```
你是一名需求分析专家，负责结合政策背景和客户实际情况，
深度分析客户的核心需求和痛点，形成结构化的需求分析报告。
```

**输入**：
```json
{
  "customer_profile": {
    "customer_id": "CUS-2024-089",
    "name": "某某大学",
    "customer_type": "高等教育",
    "region": "华东-上海市",
    "student_count": 30000,
    "existing_systems": [
      {"name": "教务管理系统", "vendor": "供应商A", "satisfaction": "中"},
      {"name": "数据中心", "vendor": "供应商B", "satisfaction": "低"}
    ],
    "historical_projects": [...]
  },
  "original_needs": [
    {"need_type": "数据治理", "description": "数据孤岛严重", "source": "客户访谈"}
  ],
  "policy_background": "<来自PolicyAgent输出>"
}
```

**处理逻辑**：
1. 整合客户原始需求和政策驱动需求
2. 分析现有系统的问题和不足
3. 识别客户的隐性需求（从政策要求推导）
4. 区分刚性需求和弹性需求
5. 评估需求优先级和实现复杂度

**输出**：
```json
{
  "agent": "NeedsAgent",
  "status": "completed",
  "parent_agents": ["PolicyAgent"],
  "needs_analysis": {
    "executive_summary": "某某大学数据治理需求分析报告",
    "policy_driven_needs": [
      {
        "need_id": "N-POL-001",
        "policy_source": "《教育信息化2.0》",
        "policy_requirement": "构建教育数据治理体系",
        "derived_need": "建立全校统一的数据标准和管理规范",
        "priority": "高"
      }
    ],
    "customer_stated_needs": [
      {
        "need_id": "N-CUS-001",
        "need_type": "数据治理",
        "description": "数据孤岛严重，各业务系统数据无法互通",
        "source": "客户访谈-2024-05-10",
        "evidence_quotes": ["业务系统间数据交换依靠手工，效率低下"],
        "priority": "高",
        "underlying_causes": ["缺乏统一数据标准", "系统接口不统一"]
      }
    ],
    "existing_system_gaps": [
      {
        "system": "数据中心",
        "current_state": "存储分散，无统一管理",
        "gaps": ["缺乏数据治理能力", "数据质量差"],
        "improvement_needed": "是"
      }
    ],
    "synthesized_needs": [
      {
        "synthesized_id": "SN-001",
        "category": "数据治理-基础能力",
        "description": "建立统一数据标准体系",
        "driven_by": ["N-POL-001", "N-CUS-001"],
        "acceptance_criteria": "制定并发布全校数据标准",
        "priority": "高",
        "estimated_effort": "中"
      }
    ],
    "needs_hierarchy": {
      "strategic": ["支撑教育数字化转型战略"],
      "tactical": ["解决数据孤岛问题", "提升数据质量"],
      "operational": ["统一数据口径", "自动化数据交换"]
    }
  }
}
```

**Prompt模板**：
```
# 角色
你是一名资深需求分析专家，负责深度分析客户的实际需求。

# 输入信息
## 客户画像
{customer_profile_json}

## 客户原始需求
{original_needs_json}

## 政策背景（来自PolicyAgent）
{policy_background}

# 任务
1. **政策驱动需求分析**：从政策要求推导出客户的刚性需求
   - 哪些政策条款直接转化为客户必须满足的需求？
   - 政策的时间节点要求是否影响需求优先级？

2. **客户实际需求分析**：深度挖掘客户反馈背后的真实问题
   - 表面需求背后的根本原因是什么？
   - 客户未明确提出但实际需要的隐性需求？

3. **现有系统差距分析**：对比客户期望与现状
   - 现有系统有哪些不足？
   - 竞争对手的方案解决了哪些问题？

4. **需求综合与优先级**：
   - 将政策驱动需求和客户实际需求融合
   - 按战略重要性/实施复杂度评估优先级

# 输出要求
- 每个需求必须有来源追溯（政策引用或客户原话）
- 识别需求间的依赖关系
- 给出明确的验收标准
```

---

### 2.3 GoalsAgent（建设目标Agent）

**角色定义**：
```
你是一名方案规划专家，负责基于需求分析结果，
设计清晰、可衡量、可达成、相关性强、有时限的建设目标。
```

**输入**：
```json
{
  "needs_analysis": "<来自NeedsAgent输出>",
  "project_constraints": {
    "budget_range": "1500-2000万",
    "duration": "12-18个月",
    "phases": 3
  }
}
```

**处理逻辑**：
1. 将需求转化为建设目标（SMART原则）
2. 按优先级和时间维度组织目标
3. 设定可量化的验收指标
4. 划分建设阶段里程碑

**输出**：
```json
{
  "agent": "GoalsAgent",
  "status": "completed",
  "parent_agents": ["NeedsAgent"],
  "construction_goals": {
    "overall_objective": "建成国内一流的高校数据治理标杆平台",
    "strategic_goals": [
      {
        "goal_id": "G-S-001",
        "goal": "支撑学校'十四五'数字化转型战略",
        "description": "通过数据治理体系建设，为学校教学、科研、管理服务提供坚实的数据基础",
        "aligns_to": ["SN-001", "SN-002"],
        "metrics": {
          "indicator": "数据赋能业务场景数",
          "baseline": "5个",
          "target": "30个",
          "measurement": "每年统计"
        }
      }
    ],
    "specific_goals": [
      {
        "goal_id": "G-SP-001",
        "goal": "打通12个核心业务系统数据壁垒",
        "description": "实现教务、学工、人事、财务等核心系统数据互联互通",
        "aligns_to": ["SN-001"],
        "metrics": {
          "indicator": "已接入系统数",
          "baseline": "2个",
          "target": "12个",
          "measurement": "系统对接完成验收"
        },
        "phase": 1,
        "duration": "6个月"
      },
      {
        "goal_id": "G-SP-002",
        "goal": "建立全校统一数据标准体系",
        "description": "制定并发布数据标准字典，覆盖80%以上核心数据",
        "aligns_to": ["SN-002"],
        "metrics": {
          "indicator": "数据标准覆盖率",
          "baseline": "20%",
          "target": "80%",
          "measurement": "标准发布后审计"
        },
        "phase": 1,
        "duration": "4个月"
      },
      {
        "goal_id": "G-SP-003",
        "goal": "建成数据资产可视化平台",
        "description": "实现数据资产全生命周期管理，提供数据资产全景视图",
        "aligns_to": ["SN-003"],
        "metrics": {
          "indicator": "数据资产数量",
          "baseline": "500",
          "target": "3000+",
          "measurement": "平台上线后统计"
        },
        "phase": 2,
        "duration": "8个月"
      }
    ],
    "milestones": [
      {"phase": 1, "month": 6, "description": "数据标准体系建立，核心系统接入完成"},
      {"phase": 2, "month": 12, "description": "数据资产平台上线，数据质量达标"},
      {"phase": 3, "month": 18, "description": "全面运营，数据赋能场景落地"}
    ],
    "success_criteria": [
      "完成12个系统数据接入",
      "数据标准覆盖率达到80%",
      "数据资产平台注册用户1000+",
      "数据质量问题响应时间<4小时"
    ]
  }
}
```

**Prompt模板**：
```
# 角色
你是一名方案规划专家，负责将需求转化为清晰、可衡量的建设目标。

# 输入信息
## 需求分析结果（来自NeedsAgent）
{needs_analysis_json}

## 项目约束
预算范围：{budget_range}
建设周期：{duration}
建设阶段：{phases}

# 任务
1. **总体目标设定**：根据需求分析，设定项目的战略总体目标
   - 体现客户的核心诉求
   - 呼应政策要求
   - 具有一定高度但可达成

2. **具体目标分解**：将总体目标分解为可执行的具体目标
   - 每个目标必须可衡量（SMART原则）
   - 设定基线值和目标值
   - 明确验收指标

3. **目标-需求映射**：确保每个目标都能追溯到需求
   - 目标必须能解决某个或某几个需求
   - 避免目标与需求脱节

4. **阶段规划**：根据项目约束，规划建设阶段
   - 划分合理的里程碑
   - 平衡各阶段的工作量
   - 考虑依赖关系

5. **成功标准**：明确项目成功的衡量标准
   - 量化指标优先
   - 质量指标辅助

# 输出要求
- 目标必须有明确的验收指标
- 每个具体目标必须映射到需求
- 阶段规划必须可行
```

---

### 2.4 SolutionAgent（具体方案内容Agent）

**角色定义**：
```
你是一名解决方案架构师，负责基于建设目标，设计具体、可落地的技术方案。
你必须深入理解客户业务，提供定制化的解决方案，而非泛泛而谈。
```

**输入**：
```json
{
  "construction_goals": "<来自GoalsAgent输出>",
  "customer_profile": "<客户画像>",
  "existing_systems": "<现有系统情况>",
  "constraints": {
    "budget": "1500-2000万",
    "timeline": "18个月",
    "technical_constraints": ["必须支持国产化", "必须兼容现有系统"]
  },
  "product_modules": ["<可用产品模块库>"]
}
```

**处理逻辑**：
1. 分析每个建设目标的技术实现路径
2. 从产品模块库选择合适的模块组合
3. 根据客户约束定制化调整
4. 设计系统架构和技术路线
5. 输出详细的方案内容

**输出**：
```json
{
  "agent": "SolutionAgent",
  "status": "completed",
  "parent_agents": ["GoalsAgent"],
  "solution_content": {
    "executive_summary": "某某大学数据治理平台建设方案",
    "design_principles": [
      "以数据标准为纲，统一数据口径",
      "以业务场景为驱动，解决实际问题",
      "以平台化思维构建，便于扩展"
    ],
    "system_architecture": {
      "overall_architecture": "...",
      "architecture_diagram": "见附件",
      "technology_stack": {
        "data_integration": ["Apache SeaTunnel", "Apache Flink"],
        "data_storage": ["Apache Iceberg", "PostgreSQL"],
        "data_governance": ["自研数据治理平台"],
        "visualization": ["自研数据资产平台"]
      }
    },
    "module_designs": [
      {
        "module_id": "MOD-DC-001",
        "module_name": "数据汇聚模块",
        "goal_alignment": ["G-SP-001"],
        "description": "实现多源异构数据的统一采集和交换",
        "technical_details": {
          "approach": "基于CDC+消息队列的实时数据采集",
          "data_sources": [
            {"system": "教务系统", "type": "关系型", "method": "CDC", "schedule": "实时"}
          ],
          "key_components": ["数据接入网关", "消息中间件", "数据同步引擎"]
        },
        "implementation": {
          "phase": 1,
          "duration": "3个月",
          "deliverables": ["数据接入规范", "接入适配器×12"]
        },
        "cost_estimation": {
          "effort_man_months": 6,
          "software_cost": 200000,
          "hardware_cost": 300000
        }
      }
    ],
    "implementation_plan": {
      "phase_1": {
        "name": "基础能力建设",
        "duration": "6个月",
        "goals": ["G-SP-001", "G-SP-002"],
        "modules": ["MOD-DC-001", "MOD-DC-002"],
        "milestones": [
          {"month": 3, "deliverable": "数据接入规范发布"},
          {"month": 6, "deliverable": "核心系统数据接入完成"}
        ]
      },
      "phase_2": {
        "name": "平台能力提升",
        "duration": "8个月",
        "goals": ["G-SP-003"],
        "modules": ["MOD-DC-003", "MOD-DC-004"],
        "milestones": [
          {"month": 10, "deliverable": "数据资产平台上线"},
          {"month": 14, "deliverable": "数据质量管理达标"}
        ]
      },
      "phase_3": {
        "name": "深化应用",
        "duration": "4个月",
        "modules": ["MOD-DC-005"],
        "milestones": [
          {"month": 18, "deliverable": "数据赋能场景落地"}
        ]
      }
    },
    "risk_mitigation": [
      {
        "risk": "现有系统接口不稳定",
        "likelihood": "高",
        "impact": "高",
        "mitigation": "实施前进行接口评估，制定兜底方案"
      }
    ]
  }
}
```

**Prompt模板**：
```
# 角色
你是一名资深解决方案架构师，负责设计具体、可落地、定制化的技术方案。

# 输入信息
## 建设目标（来自GoalsAgent）
{construction_goals_json}

## 客户画像
{customer_profile_json}

## 现有系统情况
{existing_systems_json}

## 项目约束
{constraints_json}

## 可用产品模块
{available_modules_json}

# 任务
1. **架构设计**：设计整体系统架构
   - 选择合适的技术路线
   - 确定技术栈组合
   - 绘制架构拓扑

2. **模块设计**：为每个建设目标设计对应的解决方案模块
   - 选择合适的产品模块组合
   - 根据客户情况进行定制化调整
   - 给出详细的实现方案

3. **方案定制化**：深入理解客户业务，提供针对性方案
   - 避免泛泛而谈的方案描述
   - 具体说明如何解决客户的实际问题
   - 结合客户现有的技术栈和团队能力

4. **实施规划**：设计可执行的实施计划
   - 划分合理的建设阶段
   - 设定可检验的里程碑
   - 评估资源和成本

5. **风险识别**：识别方案实施风险并提出应对措施

# 输出要求
- 方案必须高度定制化，不可通用
- 每个模块必须有明确的实施内容和交付物
- 成本估算必须有依据
```

---

### 2.5 AfterSalesAgent（售后服务Agent）

**角色定义**：
```
你是一名售后服务规划专家，负责设计贴合项目规模和合同类型的售后服务方案。
```

**输入**：
```json
{
  "project_info": {
    "project_type": "数据治理平台建设",
    "project_scale": "大型",
    "contract_amount": 18000000,
    "contract_type": "总包合同"
  },
  "solution_modules": "<来自SolutionAgent的模块列表>"
}
```

**输出**：
```json
{
  "agent": "AfterSalesAgent",
  "status": "completed",
  "after_sales_plan": {
    "service_overview": "某某大学数据治理平台售后服务方案",
    "service_period": "12个月（自项目验收之日起）",
    "service_scope": [
      "平台系统维护",
      "bug修复",
      "安全更新",
      "性能优化",
      "电话支持",
      "远程支持"
    ],
    "service_content": {
      "level_1": {
        "name": "远程支持服务",
        "description": "通过电话/远程方式提供技术支持",
        "response_time": "2小时",
        "availability": "5×8小时",
        "included": true
      },
      "level_2": {
        "name": "现场支持服务",
        "description": "紧急问题现场支持",
        "response_time": "24小时到达现场",
        "availability": "5×8小时",
        "included": true,
        "limitations": "每月最多2次现场支持"
      },
      "level_3": {
        "name": "主动巡检服务",
        "description": "定期系统健康检查",
        "frequency": "季度",
        "included": true
      }
    },
    "excluded_services": [
      "功能定制开发",
      "第三方系统问题",
      "因客户操作失误导致的系统问题"
    ],
    "service_process": {
      "issue_report": "客户提交工单",
      "issue_classification": "服务台分类（紧急/重大/一般）",
      "response": "按SLA响应",
      "resolution": "问题解决或升级",
      "closure": "客户确认关闭"
    },
    "sla": {
      "critical_issue": {
        "definition": "系统不可用",
        "response_time": "30分钟",
        "resolution_time": "4小时",
        "compensation": "顺延服务期"
      },
      "major_issue": {
        "definition": "核心功能受损",
        "response_time": "2小时",
        "resolution_time": "24小时"
      },
      "general_issue": {
        "definition": "非核心功能问题",
        "response_time": "8小时",
        "resolution_time": "72小时"
      }
    }
  }
}
```

---

### 2.6 OpsAgent（运维服务Agent）

**角色定义**：
```
你是一名运维服务规划专家，负责设计贴合项目复杂度和客户规模的运维服务方案。
```

**输出**：
```json
{
  "agent": "OpsAgent",
  "status": "completed",
  "ops_plan": {
    "ops_overview": "某某大学数据治理平台运维服务方案",
    "ops_period": "12个月（质保期满后）",
    "ops_model": "驻场 + 远程支持",
    "ops_team": {
      "site_engineer": {
        "count": 1,
        "level": "中级工程师",
        "on_site_hours": "5×8小时",
        "responsibilities": ["日常运维", "监控巡检", "问题处理"]
      },
      "remote_expert": {
        "count": 1,
        "level": "高级工程师",
        "availability": "5×8小时远程",
        "responsibilities": ["技术专家支持", "问题升级处理", "优化建议"]
      }
    },
    "ops_content": {
      "daily_operations": [
        "系统健康状态检查",
        "日志审查",
        "性能监控",
        "备份验证"
      ],
      "periodic_operations": [
        {"name": "周巡检", "description": "系统全面检查、性能报告"},
        {"name": "月巡检", "description": "深度维护、安全检查"},
        {"name": "季巡检", "description": "系统评估、优化建议"}
      ],
      "ops_reports": [
        "周报：运维周报（系统状态、问题汇总）",
        "月报：运维月报（性能分析、容量评估）",
        "年报：运维年报（服务总结、下年度建议）"
      ]
    },
    "ops_tools": [
      "Zabbix（监控）",
      "ELK（日志分析）",
      "自研运维平台"
    ],
    "ops_kpis": [
      {"kpi": "系统可用率", "target": "≥99.5%"},
      {"kpi": "平均故障恢复时间", "target": "≤30分钟"},
      {"kpi": "工单解决率", "target": "≥95%"}
    ]
  }
}
```

---

### 2.7 TeamAgent（交付团队Agent）

**角色定义**：
```
你是一名项目管理专家，负责设计贴合项目类型和所需技能的交付团队方案。
```

**输出**：
```json
{
  "agent": "TeamAgent",
  "status": "completed",
  "team_plan": {
    "project_name": "某某大学数据治理平台建设项目",
    "project_duration": "18个月",
    "team_structure": {
      "management": [
        {
          "role": "项目总监",
          "name": "[客户指定或公司指派]",
          "responsibilities": ["项目整体把控", "关键决策", "客户高层沟通"],
          "dedication": "20%间歇"
        },
        {
          "role": "项目经理",
          "name": "[待定]",
          "responsibilities": ["项目计划", "进度管理", "风险管理", "客户日常沟通"],
          "dedication": "100%驻场"
        }
      ],
      "technical": [
        {
          "role": "技术架构师",
          "responsibilities": ["技术方案设计", "关键技术决策", "代码评审"],
          "dedication": "40%现场",
          "on_site_months": "1-6月"
        },
        {
          "role": "高级开发工程师",
          "count": 2,
          "responsibilities": ["核心模块开发", "技术难题攻关"],
          "dedication": "80%现场",
          "on_site_months": "3-12月"
        },
        {
          "role": "开发工程师",
          "count": 3,
          "responsibilities": ["功能开发", "单元测试"],
          "dedication": "100%现场",
          "on_site_months": "4-14月"
        },
        {
          "role": "数据工程师",
          "count": 2,
          "responsibilities": ["数据接入", "数据治理规则开发"],
          "dedication": "100%现场",
          "on_site_months": "2-10月"
        },
        {
          "role": "测试工程师",
          "count": 2,
          "responsibilities": ["功能测试", "性能测试"],
          "dedication": "60%现场",
          "on_site_months": "8-16月"
        }
      ],
      "quality": [
        {
          "role": "QA负责人",
          "responsibilities": ["质量把控", "测试管理"],
          "dedication": "30%现场"
        }
      ]
    },
    "man_power_summary": {
      "total_man_months": 180,
      "peak_headcount": 10,
      "cost_breakdown": "项目成本中的40%用于人力成本"
    },
    "key_personnel_intro": [
      {
        "role": "项目经理",
        "requirement": "5年以上项目管理经验，3个以上数据治理项目经验，PMP优先"
      },
      {
        "role": "技术架构师",
        "requirement": "8年以上开发经验，精通大数据架构，有教育行业经验优先"
      }
    ]
  }
}
```

---

### 2.8 CasesAgent（成功案例Agent）

**角色定义**：
```
你是一名案例分析专家，负责从历史项目中匹配与当前客户相似度最高的成功案例，
并提取可复用的经验和方法论。
```

**输入**：
```json
{
  "customer_profile": "<客户画像>",
  "project_type": ["数据治理", "智慧校园"],
  "solution_summary": "<方案概要>"
}
```

**处理逻辑**：
1. 根据客户类型、规模、需求匹配相似案例
2. 按相似度排序
3. 提取案例的关键成功因素

**输出**：
```json
{
  "agent": "CasesAgent",
  "status": "completed",
  "parent_agents": ["PolicyAgent", "NeedsAgent"],
  "matched_cases": [
    {
      "case_id": "CASE-2023-045",
      "case_name": "华东理工大学数据治理平台建设项目",
      "relevance_score": 0.92,
      "similarity_factors": [
        {"factor": "客户类型", "match": "高等教育", "similarity": "完全匹配"},
        {"factor": "学生规模", "match": "28000", "similarity": "高"},
        {"factor": "地区", "match": "华东-上海市", "similarity": "完全匹配"},
        {"factor": "需求类型", "match": "数据治理+智慧校园", "similarity": "高"}
      ],
      "project_overview": {
        "project_name": "华东理工大学数据治理平台一期",
        "contract_amount": 16000000,
        "duration": "14个月",
        "completion_date": "2023-06-01"
      },
      "key_success_factors": [
        {
          "factor": "高层支持",
          "description": "信息化建设处一把手亲自挂帅，协调各部门配合",
          "transferable": true
        },
        {
          "factor": "标准先行",
          "description": "先建立数据标准再推进接入，避免返工",
          "transferable": true
        }
      ],
      "achievements": [
        "完成10个核心业务系统数据接入",
        "建立全校统一数据标准字典",
        "数据质量问题响应时间从3天缩短至4小时"
      ],
      "lessons_learned": [
        {
          "lesson": "提前识别数据质量差的系统",
          "mitigation": "在项目启动阶段进行数据质量评估"
        }
      ],
      "client_testimonial": "...",
      "reference_contacts": [
        {"name": "王老师", "position": "信息化主任", "willing_to_share": true}
      ]
    }
  ],
  "methodology_summary": "基于多个同类项目经验，总结以下方法论：1）数据标准先行；2）小步快跑迭代；3）价值驱动推进..."
}
```

---

## 3. Orchestrator（主编排器）

### 3.1 编排流程

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           Agent Orchestration Flow                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  Step 1: 初始化                                                                       │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │  输入：customer_id, need_types, template_id                                   │  │
│  │  1. 从CustomerCollector获取客户画像                                           │  │
│  │  2. 加载方案模板                                                               │  │
│  │  3. 初始化上下文（context）                                                   │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                              │
│                                      ▼                                              │
│  Step 2: PolicyAgent执行                                                             │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │                               PolicyAgent                                    │  │
│  │  输出：policy_background → 存入context                                       │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                              │
│                                      ▼                                              │
│  Step 3: 串行执行核心Agent链                                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │                               NeedsAgent                                     │  │
│  │  输入：customer_profile + original_needs + policy_background                  │  │
│  │  输出：needs_analysis → 存入context                                          │  │
│  │  ⚠️ 必须人工确认后才能继续                                                    │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                              │
│                                      ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │                               GoalsAgent                                     │  │
│  │  输入：needs_analysis + constraints                                          │  │
│  │  输出：construction_goals → 存入context                                     │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                              │
│                                      ▼                                              │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │                             SolutionAgent                                    │  │
│  │  输入：construction_goals + all_context                                     │  │
│  │  输出：solution_content → 存入context                                        │  │
│  │  ⚠️ 必须人工确认后才能继续                                                    │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                              │
│                                      ▼                                              │
│  Step 4: 并行执行支撑Agent                                                          │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │    AfterSalesAgent    │    OpsAgent    │    TeamAgent    │   CasesAgent    │  │
│  │  并行执行，结果存入context                                                   │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                              │
│                                      ▼                                              │
│  Step 5: 汇总输出                                                                   │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │  组装完整解决方案 → 返回给用户                                                │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 上下文管理

```json
{
  "orchestration_context": {
    "solution_id": "SOL-2024-001",
    "customer_id": "CUS-2024-089",
    "template_id": "TPL-2024-001",
    "created_at": "2024-06-01T10:00:00Z",
    "agents_results": {
      "PolicyAgent": {
        "status": "completed",
        "output": {...},
        "execution_time_ms": 1200
      },
      "NeedsAgent": {
        "status": "pending",
        "depends_on": ["PolicyAgent"],
        "input_ready": false
      },
      "GoalsAgent": {
        "status": "pending",
        "depends_on": ["NeedsAgent"]
      },
      "SolutionAgent": {
        "status": "pending",
        "depends_on": ["GoalsAgent"]
      },
      "SupportingAgents": {
        "status": "pending",
        "parallel_execution": true,
        "depends_on": ["SolutionAgent"]
      }
    },
    "shared_context": {
      "customer_profile": {...},
      "original_needs": [...],
      "policy_background": {...},
      "needs_analysis": {...},
      "construction_goals": {...},
      "solution_content": {...}
    }
  }
}
```

### 3.3 人工干预机制（必须确认）

**干预策略**：
- NeedsAgent 和 SolutionAgent 的输出**必须人工确认**后才能继续后续Agent
- 其他Agent为可选确认，可直接继续

**干预操作类型**：

| 操作 | 说明 | 后续动作 |
|------|------|----------|
| **APPROVE** | 批准当前结果 | 继续执行下一Agent |
| **REJECT** | 拒绝，要求重新生成 | 重新触发该Agent |
| **MODIFY** | 直接修改输出 | 保存修改，继续下一Agent |
| **RERUN** | 修改输入后重新执行 | 用新输入重新执行 |
| **SKIP** | 跳过该Agent | 使用默认值，继续下一Agent |

**干预流程**：
```
Agent执行完成 → 输出待确认状态 → 用户操作(APPROVE/MODIFY/REJECT)
                                              ↓
                              APPROVE → 继续下一Agent
                              REJECT → 重新生成
                              MODIFY → 保存修改后继续
```

---

## 4. 外部系统联动设计

### 4.1 联动架构

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              SolutionManager                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                            Orchestrator                                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │  Message   │  │   State    │  │   Cache    │  │   Error    │      │   │
│  │  │  Queue     │  │  Machine   │  │  Manager   │  │  Handler   │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                              │
│  ┌───────────────────────────────────┼───────────────────────────────────────┐   │
│  │                    External System Gateway                                   │   │
│  │  ┌─────────────────────┐    ┌─────────────────────┐                       │   │
│  │  │  CustomerCollector   │    │   PolicyCollector    │                       │   │
│  │  │      Client         │    │       Client         │                       │   │
│  │  └──────────┬──────────┘    └──────────┬──────────┘                       │   │
│  └─────────────┼───────────────────────────┼───────────────────────────────────┘   │
│                │                               │                                   │
└────────────────┼───────────────────────────────┼───────────────────────────────────┘
                 │                               │
                 ▼                               ▼
        ┌─────────────────┐            ┌─────────────────┐
        │CustomerCollector│            │ PolicyCollector  │
        │  (客户信息)     │            │   (政策信息)     │
        └─────────────────┘            └─────────────────┘
```

### 4.2 调用时序

**阶段1: 初始化（从CustomerCollector获取）**

```
SolutionManager                          CustomerCollector
      │                                       │
      │──── getCustomerProfile(customer_id) ──▶│
      │◀──── customer_profile ─────────────────│
      │                                       │
      │──── getCustomerNeeds(customer_id) ────▶│
      │◀──── customer_needs ──────────────────│
      │                                       │
      │──── getCustomerProjects(customer_id) ─▶│
      │◀──── historical_projects ─────────────│
```

**阶段2: PolicyAgent执行（调用PolicyCollector）**

```
SolutionManager                          PolicyCollector
      │                                       │
      │──── searchPolicies(customer_type,     │
      │       need_types) ───────────────────▶│
      │◀──── policy_list ─────────────────────│
      │                                       │
      │ 对每条政策:                           │
      │──── getPolicyDetail(citation_id) ────▶│
      │◀──── policy_full_text ────────────────│
```

**阶段3: 后续Agent执行**

```
后续Agent执行: 直接使用上下文中的数据，无需再次调用外部系统
```

### 4.3 数据映射

**CustomerCollector → SolutionManager**

```json
// 数据映射规则
{
  "customer_profile": {
    "source": "CustomerCollector.getCustomerProfile()",
    "mapping": {
      "customer_code": "→ customer_id",
      "name": "→ customer.name",
      "customer_type": "→ customer.type",
      "level": "→ customer.level",
      "region": "→ customer.region",
      "contact": "→ customer.contact",
      "existing_systems": "→ customer.existing_systems",
      "historical_projects": "→ customer.historical_projects"
    }
  },
  "customer_needs": {
    "source": "CustomerCollector.getCustomerNeeds()",
    "mapping": {
      "need_id": "→ original_needs[].need_id",
      "need_type": "→ original_needs[].need_type",
      "description": "→ original_needs[].description",
      "source": "→ original_needs[].source",
      "priority": "→ original_needs[].priority"
    }
  }
}
```

**PolicyCollector → SolutionManager**

```json
// 数据映射规则
{
  "policies": {
    "source": "PolicyCollector.searchPolicies() + getPolicyDetail()",
    "mapping": {
      "citation_id": "→ policy_id",
      "title": "→ policy.title",
      "issuing_authority": "→ policy.authority",
      "publish_date": "→ policy.date",
      "content": "→ policy.full_text",
      "sections": "→ policy.sections (精准引用)"
    }
  }
}
```

### 4.4 缓存策略

| 缓存项 | TTL | 说明 |
|--------|-----|------|
| `policy:search:{hash}` | 1小时 | 政策搜索结果（按查询hash） |
| `policy:detail:{citation_id}` | 24小时 | 政策详情（相对稳定） |
| `customer:profile:{customer_id}` | 30分钟 | 客户画像 |
| `customer:needs:{customer_id}` | 15分钟 | 客户需求（可能频繁更新） |

### 4.5 错误处理与降级策略

**错误分类**：

| 错误类别 | 原因 | 处理策略 |
|----------|------|----------|
| TRANSIENT | 网络超时、暂时不可用 | 重试3次，指数退避 |
| RATE_LIMIT | API限流 | 等待后重试，最多5次 |
| TIMEOUT | 请求超时 | 重试2次 |
| PERMANENT | 资源不存在 | 直接失败，不重试 |

**降级策略**：

| 故障场景 | 降级级别 | 处理方式 |
|----------|----------|----------|
| PolicyCollector不可用 | DEGRADED | 使用缓存 + 生成通用政策背景 |
| CustomerCollector不可用 | DEGRADED | 使用缓存 + 允许手动输入客户信息 |
| 两者都不可用 | MINIMAL | 仅能编辑已有方案，无法生成 |
| LLM不可用 | EMERGENCY | 暂停所有生成，仅支持手动 |

### 4.6 外部系统接口定义

**CustomerCollector接口**：

```typescript
// 获取客户画像
GET /api/v1/customers/{customer_code}/profile

// 获取客户需求
GET /api/v1/customers/{customer_code}/needs

// 获取历史项目
GET /api/v1/customers/{customer_code}/projects

// 响应格式
{
  "success": true,
  "customer": {
    "customer_code": "CUS-2024-089",
    "name": "某某大学",
    "customer_type": "高等教育",
    "level": "省级",
    "region": "华东-上海市",
    "contact": {...},
    "existing_systems": [...],
    "historical_projects": [...]
  }
}
```

**PolicyCollector接口**：

```typescript
// 搜索政策
GET /api/v1/policies/search?q={query}&customer_type={type}&sort={sort}

// 获取政策详情
GET /api/v1/policies/{citation_id}

// 获取段落（精准引用）
GET /api/v1/policies/{citation_id}/sections/{section_index}

// 响应格式
{
  "success": true,
  "results": [{
    "citation_id": "POL-2024-089",
    "title": "...",
    "issuing_authority": "教育部",
    "publish_date": "2024-06-15",
    "relevance_score": 0.95
  }]
}
```

---

## 5. 消息通信协议

### 5.1 消息格式

```typescript
interface AgentMessage {
  message_id: string;           // UUID
  message_type: MessageType;    // 消息类型
  timestamp: string;            // ISO 8601
  sender: AgentName;            // 发送方
  receiver?: AgentName;          // 接收方（广播时为空）
  correlation_id?: string;       // 关联ID
  payload: unknown;             // 消息负载
  metadata?: {
    retry_count?: number;
    timeout_ms?: number;
  };
}

type MessageType =
  | 'TASK_ASSIGNMENT'      // 任务下发
  | 'TASK_RESULT'           // 任务结果
  | 'STATUS_REPORT'         // 状态上报
  | 'ERROR_REPORT'          // 错误报告
  | 'HUMAN_INTERVENTION'    // 人工干预
  | 'CONTEXT_UPDATE';       // 上下文更新
```

### 5.2 任务下发消息

```typescript
interface TaskAssignmentMessage extends AgentMessage {
  message_type: 'TASK_ASSIGNMENT';
  payload: {
    task_id: string;
    agent_name: AgentName;
    task_type: TaskType;
    input_data: Record<string, unknown>;
    execution_config?: {
      timeout_ms?: number;
      max_retries?: number;
      llm_model?: 'qwen' | 'deepseek';
    };
    callback_url?: string;
  };
}
```

### 5.3 任务结果消息

```typescript
interface TaskResultMessage extends AgentMessage {
  message_type: 'TASK_RESULT';
  payload: {
    task_id: string;
    status: 'completed' | 'failed' | 'partial';
    output_data: Record<string, unknown>;
    execution_time_ms: number;
    artifacts?: {
      name: string;
      url: string;
      type: string;
    }[];
    error?: {
      code: string;
      message: string;
      details?: unknown;
    };
  };
}
```

---

## 6. 执行状态机

### 6.1 状态定义

```
                                      ┌─────────────┐
                                      │    INIT     │
                                      └──────┬──────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    ▼                        ▼                        ▼
            ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
            │   POLICY    │          │   WAITING   │          │   FAILED    │
            │ (执行中)    │          │  (等待确认)  │          │  (失败)     │
            └──────┬──────┘          └──────┬──────┘          └─────────────┘
                   │                        │
                   │ 完成                   │ 确认
                   ▼                        ▼
            ┌─────────────┐          ┌─────────────┐
            │   NEEDS     │─────────▶│  NEEDS     │
            │ (执行中)    │ 确认     │  CONFIRMED  │
            └──────┬──────┘          └──────┬──────┘
                   │                        │
                   │ 完成                   │ 确认
                   ▼                        ▼
            ┌─────────────┐          ┌─────────────┐
            │   GOALS     │          │  GOALS     │
            │ (执行中)    │          │  CONFIRMED │
            └──────┬──────┘          └──────┬──────┘
                   │                        │
                   │ 完成                   │ 确认
                   ▼                        ▼
            ┌─────────────┐          ┌─────────────┐
            │  SOLUTION   │─────────▶│ SOLUTION   │
            │ (执行中)    │ 确认     │  CONFIRMED │
            └──────┬──────┘          └──────┬──────┘
                   │                        │
                   │ 完成                   │ 确认
                   ▼                        ▼
            ┌─────────────┐          ┌─────────────┐
            │ SUPPORTING  │          │ COMPLETED  │
            │ (并行执行)  │          │  (完成)     │
            └──────┬──────┘          └─────────────┘
                   │
                   │ 所有支撑Agent完成
                   ▼
            ┌─────────────┐
            │   CASES    │
            │ (执行中)    │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │ COMPLETED  │
            │  (完成)    │
            └─────────────┘
```

### 6.2 状态转换规则

| 当前状态 | 事件 | 下一状态 | 说明 |
|----------|------|----------|------|
| INIT | 初始化完成 | POLICY | 开始PolicyAgent |
| POLICY | PolicyAgent完成 | NEEDS | 开始NeedsAgent |
| NEEDS | NeedsAgent完成 | WAITING_NEEDS | 等待人工确认 |
| WAITING_NEEDS | 用户确认 | NEEDS_CONFIRMED | 确认通过 |
| WAITING_NEEDS | 用户拒绝 | NEEDS | 重新生成 |
| WAITING_NEEDS | 用户修改 | NEEDS_CONFIRMED | 修改后继续 |
| NEEDS_CONFIRMED | 自动 | GOALS | 开始GoalsAgent |
| GOALS | GoalsAgent完成 | GOALS_CONFIRMED | 自动确认（可选干预） |
| GOALS_CONFIRMED | 自动 | SOLUTION | 开始SolutionAgent |
| SOLUTION | SolutionAgent完成 | WAITING_SOLUTION | 等待人工确认 |
| WAITING_SOLUTION | 用户确认 | SOLUTION_CONFIRMED | 确认通过 |
| WAITING_SOLUTION | 用户拒绝 | SOLUTION | 重新生成 |
| WAITING_SOLUTION | 用户修改 | SOLUTION_CONFIRMED | 修改后继续 |
| SOLUTION_CONFIRMED | 自动 | SUPPORTING | 开始并行支撑Agent |
| SUPPORTING | 支撑Agent全部完成 | CASES | 开始CasesAgent |
| CASES | CasesAgent完成 | COMPLETED | 方案生成完成 |

---

## 7. 交互设计

### 7.1 用户交互流程

```
[选择客户] → [确认需求] → [选择模板] → [触发生成] → [方案生成] → [人工确认] → [定稿]
                    │                    │                          │               │
                    ▼                    ▼                          ▼               ▼
               输入原始需求           配置参数              查看/修改各模块      导出/发布
```

### 7.2 交互模式

| 阶段 | 交互方式 | 说明 |
|------|----------|------|
| 初始化 | 表单选择 | 选择客户、需求类型、模板 |
| 生成中 | 实时进度 | 显示各Agent执行状态和进度 |
| 生成后（必须） | 人工确认 | NeedsAgent、SolutionAgent必须确认 |
| 生成后（可选） | 分模块查看 | 其他Agent可跳过确认 |
| 调整时 | 直接编辑 | 修改任意模块内容 |
| 重新生成 | 单模块刷新 | 重新触发特定Agent |

### 7.3 人工干预点

| Agent | 干预必要性 | 干预时机 | 干预方式 |
|-------|------------|----------|----------|
| PolicyAgent | **可选** | 生成后 | 添加/删除/修改政策引用 |
| NeedsAgent | **必须确认** | 生成后 | 确认/修改/补充需求分析 |
| GoalsAgent | **可选** | 生成后 | 调整目标优先级/指标 |
| SolutionAgent | **必须确认** | 生成后 | 修改具体方案内容 |
| AfterSalesAgent | **可选** | 生成后 | 调整服务内容和SLA |
| OpsAgent | **可选** | 生成后 | 调整运维配置 |
| TeamAgent | **可选** | 生成后 | 调整团队配置 |

### 4.4 所见即所得编辑

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  解决方案编辑器                                        [保存] [导出] [版本] [发布]      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌───────────────────────────────────────────────────────────────────────────────┐ │
│  │  Agent协作状态                                                                │ │
│  │  ✓ PolicyAgent   ✓ NeedsAgent   ✓ GoalsAgent   ⟳ SolutionAgent   ...       │ │
│  └───────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    │                          │                              │   │
│  │   模块导航          │      编辑区域              │      实时预览                │   │
│  │   (左侧)           │      (中间)              │      (右侧)                  │   │
│  │                    │                          │                              │   │
│  │  ▼ 1.政策背景      │  ┌──────────────────┐   │  ┌──────────────────────┐   │   │
│  │    · 相关政策      │  │ 编辑: 需求分析    │   │  │ 需求分析报告         │   │   │
│  │                    │  │                  │   │  │                      │   │   │
│  │  ▼ 2.需求分析      │  │ [AI生成内容]     │   │  │ 1.政策驱动需求       │   │   │
│  │    · 政策驱动需求  │  │                  │   │  │   - 数据治理要求...  │   │   │
│  │    · 客户实际需求  │  │ ░░░░░░░░░░░░░░  │   │  │                      │   │   │
│  │    · 现有系统差距  │  │ ░░░░░░░░░░░░░░  │   │  │ 2.客户实际需求       │   │   │
│  │                    │  │                  │   │  │   - 数据孤岛...      │   │   │
│  │  ▼ 3.建设目标      │  │ 人工编辑区域     │   │  │                      │   │   │
│  │    · 总体目标      │  │                  │   │  │ 3.差距分析           │   │   │
│  │    · 具体目标      │  └──────────────────┘   │  │   - 现有系统不足...  │   │   │
│  │    · 里程碑        │                          │  └──────────────────────┘   │   │
│  │                    │  ┌──────────────────┐   │                              │   │
│  │  ▼ 4.具体方案内容  │  │ Agent操作         │   │  ┌──────────────────────┐   │   │
│  │    · 架构设计      │  │                  │   │  │ AI辅助                │   │   │
│  │    · 数据汇聚      │  │ [重新生成] [展开] │   │  │ [优化表述] [精简内容] │   │   │
│  │    · 数据治理      │  │ [添加政策引用]    │   │  └──────────────────────┘   │   │
│  │    · 数据服务      │  └──────────────────┘   │                              │   │
│  │                    │                          │                              │   │
│  │  ▼ 5.售后服务      │                          │                              │   │
│  │  ▼ 6.运维服务      │                          │                              │   │
│  │  ▼ 7.交付团队      │                          │                              │   │
│  │  ▼ 8.成功案例      │                          │                              │   │
│  │                    │                          │                              │   │
│  └────────────────────┴──────────────────────────┴──────────────────────────────┘   │
│                                                                                      │
│  [+ 添加模块]  [拖拽排序]                                           [全部重新生成]    │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. 数据模型

### 5.1 解决方案主表
```sql
CREATE TABLE solutions (
    id UUID PRIMARY KEY,
    solution_code VARCHAR(50) UNIQUE NOT NULL,

    title VARCHAR(200) NOT NULL,
    customer_id UUID,
    template_id UUID,

    -- 各Agent输出（JSON存储）
    agent_outputs JSONB NOT NULL DEFAULT '{}',

    status VARCHAR(20) DEFAULT 'draft',
    version INTEGER DEFAULT 1,
    is_latest BOOLEAN DEFAULT true,

    created_by UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP
);
```

### 5.2 Agent执行记录表
```sql
CREATE TABLE agent_executions (
    id UUID PRIMARY KEY,
    solution_id UUID REFERENCES solutions(id),

    agent_name VARCHAR(50) NOT NULL,
    agent_version VARCHAR(20),

    input_data JSONB,
    output_data JSONB,
    execution_time_ms INTEGER,

    status VARCHAR(20) DEFAULT 'pending',  -- pending/running/completed/failed
    error_message TEXT,

    triggered_by UUID,  -- user or system
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 5.3 Agent配置表
```sql
CREATE TABLE agent_configs (
    id UUID PRIMARY KEY,
    agent_name VARCHAR(50) UNIQUE NOT NULL,

    prompt_template TEXT NOT NULL,
    model_config JSONB,  -- model selection, temperature, etc.
    input_schema JSONB,
    output_schema JSONB,

    is_active BOOLEAN DEFAULT true,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## 9. API规格

### 9.1 创建解决方案
```
POST /api/v1/solutions
```

### 9.2 触发Agent生成
```
POST /api/v1/solutions/{solution_code}/agents/{agent_name}/execute
```

### 9.3 获取Agent执行状态
```
GET /api/v1/solutions/{solution_code}/agents/status
```

### 9.4 更新Agent输出（人工干预）
```
PUT /api/v1/solutions/{solution_code}/agents/{agent_name}/output
```

### 9.5 重新执行Agent
```
POST /api/v1/solutions/{solution_code}/agents/{agent_name}/rerun
```

### 9.6 确认Agent输出（必须确认流程）
```
POST /api/v1/solutions/{solution_code}/agents/{agent_name}/approve
Request: { action: 'approve' | 'reject' | 'modify', modifications?: [...] }
```

---

## 10. 实施计划

| 阶段 | 周期 | 内容 | 交付物 |
|------|------|------|--------|
| 阶段一 | 1周 | Agent框架 + PolicyAgent + NeedsAgent | Agent执行框架，2个Agent可用 |
| 阶段二 | 1周 | GoalsAgent + SolutionAgent | 核心Agent链完成 |
| 阶段三 | 1周 | 支撑Agent + Orchestrator | 全部Agent完成，编排器完成 |
| 阶段四 | 1周 | 编辑界面 + API | 交互界面和API |
| 阶段五 | 0.5周 | 联调 + 部署 | 生产可用系统 |

---

## 11. 验收标准

### 11.1 Agent验收

| Agent | LLM选择 | 验收条件 |
|-------|---------|----------|
| PolicyAgent | Qwen3.6-Plus | 能根据客户类型和需求准确匹配政策，提供原文引用 |
| NeedsAgent | Qwen3.6-Plus | 能结合政策驱动和客户实际需求生成需求分析报告 |
| GoalsAgent | DeepSeek-V4 | 能将需求转化为SMART建设目标 |
| SolutionAgent | DeepSeek-V4 | 能基于建设目标生成定制化方案内容 |
| AfterSalesAgent | Qwen3.6-Plus | 能生成符合项目规模的售后服务方案 |
| OpsAgent | Qwen3.6-Plus | 能生成符合项目复杂度的运维服务方案 |
| TeamAgent | Qwen3.6-Plus | 能生成合理的交付团队方案 |
| CasesAgent | Qwen3.6-Plus | 能匹配相似成功案例 |

### 11.2 编排验收

| 功能 | 验收条件 |
|------|----------|
| 串行执行 | 依赖链正确执行 |
| 并行执行 | 支撑Agent并行执行 |
| 上下文传递 | Agent间数据正确传递 |
| 错误处理 | Agent失败时正确处理 |
| 人工干预 | **必须确认机制**：NeedsAgent和SolutionAgent输出后必须人工确认 |

### 11.3 外部联动验收

| 系统 | 验收条件 |
|------|----------|
| CustomerCollector | 能正确获取客户画像、需求、历史项目 |
| PolicyCollector | 能正确搜索政策、获取原文引用 |
| 降级机制 | 外部系统不可用时能正确降级 |

### 11.4 交互验收

| 功能 | 验收条件 |
|------|----------|
| 进度展示 | 各Agent执行状态可见 |
| 必须确认 | NeedsAgent和SolutionAgent执行后阻塞，等待用户确认 |
| 分模块编辑 | 可单独编辑/重新生成各模块 |
| 实时预览 | 编辑内容实时反映 |
| 版本管理 | 支持版本保存和回滚 |

---

## 12. 术语表

| 术语 | 说明 |
|------|------|
| Agent | 智能体，能够自主完成特定任务的AI系统 |
| Orchestrator | 编排器，负责协调多个Agent执行顺序和上下文传递 |
| Multi-Agent | 多智能体系统，由多个协作的Agent组成 |
| 上下文 | Context，贯穿整个方案的共享数据载体 |
| 依赖链 | Agent间的执行依赖关系 |
| 必须确认 | 某些关键Agent的输出必须人工确认后才能继续 |
| 降级策略 | 外部系统不可用时的备用处理方案 |
