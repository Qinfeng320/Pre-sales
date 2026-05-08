# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Pre-sales 项目仓库（售前解决方案），包含四个智能体系统的 PRD 文档和 Demo HTML 原型。**无实际代码实现**。

## 目录结构

```
d:\Pre-sales\
├── doc\PRD\                    # 产品需求文档
│   ├── policy_collector_prd.md       # 政策搜集智能体系统
│   ├── customer_collector_prd.md     # 客户信息收集智能体系统
│   ├── solution_manager_prd.md       # 产品解决方案管理智能体系统
│   └── admin_system_prd.md           # 智能体系统后台管理
└── demo\                          # HTML 原型演示
    ├── policy_collector.html
    ├── customer_collector.html
    ├── solution-orchestrator.html
    └── agent-model-config.html
```

## 常用命令

本仓库为 PRD/Demo 文档仓库，无构建命令。

**Demo 预览**：
- 直接在浏览器中打开 `demo/*.html` 文件即可预览

**PRD 文档**：
- 各 PRD 文件包含完整的 API 规格、数据模型、Agent 设计
- 参考 `doc\PRD\` 下的 `.md` 文件

## 系统架构

### 三大核心系统关系

```
┌──────────────────────────────────────────────────────────────────────┐
│                      SolutionManager (方案生成)                        │
│   Multi-Agent 架构: PolicyAgent → NeedsAgent → GoalsAgent → SolutionAgent
│   支撑 Agents: AfterSalesAgent, OpsAgent, TeamAgent, CasesAgent      │
└──────────────────────────────────────────────────────────────────────┘
                              │
                    联动 CustomerCollector + PolicyCollector
                              │
         ┌────────────────────┴────────────────────┐
         ▼                                         ▼
┌─────────────────────────┐         ┌─────────────────────────┐
│  CustomerCollector      │         │   PolicyCollector        │
│  客户信息收集系统         │◄──────►│   政策搜集系统           │
│  - 客户登记/校验         │         │   - 政策登记/校验        │
│  - 需求/项目记录         │         │   - Relation Agent      │
│  - 多角色智能体分析       │         │   - 向量检索 RAG        │
└─────────────────────────┘         └─────────────────────────┘
```

### AdminSystem（后台管理）

轻量级后台管理系统，管理四类业务数据：
- 客户数据 (customers)
- 政策数据 (policies)
- 方案数据 (solutions)
- 大模型配置 (admin_model_configs + admin_agent_model_mappings)

AdminSystem 通过 `admin_agent_model_mappings` 表配置 Agent 与模型的绑定关系，供 SolutionManager 等系统查询使用。

### LLM 选型策略

SolutionManager 根据任务类型选择最适合的 LLM：

| Agent | 推荐 LLM | 原因 |
|-------|---------|------|
| PolicyAgent / NeedsAgent | **Qwen3.6-Plus** | 中文政策理解强 |
| GoalsAgent / SolutionAgent | **DeepSeek-V4** | 复杂推理、SMART 目标分解 |
| 支撑 Agents (AfterSales/Ops/Team/Cases) | **Qwen3.6-Plus** | 中文表述 |

**混合策略**: 中文理解/生成 → Qwen3.6-Plus；复杂推理/架构设计 → DeepSeek-V4

## 技术栈（参考）

| 组件 | 技术 |
|------|------|
| 向量存储 | Qdrant (Apache 2.0) |
| 关系型数据库 | PostgreSQL / SQLite |
| Embedding | BGE-M3 (MIT) |
| Reranker | BGE-Reranker-v2-m3 (MIT) |
| LLM | DeepSeek-V4 / Qwen2.5 |
| 容器 | Docker |

## 关键设计

### 人工校验机制
所有系统均采用"人工校验"保证数据准确性：
- 用户登记 → 待校验状态 → 人工确认 → 允许检索

### Multi-Agent 协作（SolutionManager）
编排器协调 8 个 Agent 串行/并行执行：
- **串行链**: PolicyAgent → NeedsAgent → GoalsAgent → SolutionAgent
- **必须确认**: NeedsAgent 和 SolutionAgent 输出后必须人工确认
- **并行支撑**: AfterSalesAgent, OpsAgent, TeamAgent 在 SolutionAgent 确认后并行执行
- **案例查询**: CasesAgent 在支撑 Agent 完成后执行，依赖 PolicyAgent 和 NeedsAgent 的结果

### 政策联动
- 客户类型 → 匹配相关政策
- 历史项目 → 关联当时政策
- 需求/方案 → 引用政策原文作为依据

## 注意事项

- Demo 文件可直接在浏览器中打开预览
- 各 PRD 文档包含完整的 API 规格和数据模型设计，可直接参考实现
