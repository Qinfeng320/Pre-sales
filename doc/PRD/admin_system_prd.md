# 智能体系统后台管理 PRD（极简版）

| 版本 | 日期 | 作者 | 说明 |
|------|------|------|------|
| v1.0 | 2026-05-08 | - | 极简版 - 仅数据管理 |

---

## 1. 概述

### 1.1 产品定位

轻量级后台管理系统，用于管理 4 类业务数据：
- 客户数据
- 政策数据
- 方案数据
- 大模型配置

### 1.2 使用场景

无登录认证，直接访问后台页面进行数据管理。

---

## 2. 功能需求

### 2.1 客户管理

| 功能 | 描述 |
|------|------|
| 客户列表 | 分页展示客户信息，支持搜索 |
| 查看详情 | 查看客户完整信息 |
| 编辑客户 | 修改客户信息 |
| 删除客户 | 软删除客户数据 |

### 2.2 政策管理

| 功能 | 描述 |
|------|------|
| 政策列表 | 分页展示政策信息，支持搜索、筛选 |
| 查看详情 | 查看政策完整信息 |
| 编辑政策 | 修改政策信息 |
| 删除政策 | 软删除政策数据 |

### 2.3 方案管理

| 功能 | 描述 |
|------|------|
| 方案列表 | 分页展示方案信息 |
| 查看详情 | 查看方案完整内容 |
| 编辑方案 | 修改方案信息 |
| 删除方案 | 软删除方案数据 |

### 2.4 模型配置

| 功能 | 描述 |
|------|------|
| 模型列表 | 展示所有已配置模型 |
| 添加模型 | 新增 DeepSeek/Qwen/MiniMax 模型 |
| 编辑模型 | 修改模型参数（API Key、URL等） |
| 删除模型 | 删除模型配置 |
| 测试连接 | 测试模型 API 连通性 |
| Agent映射 | 配置 Agent 与模型的绑定关系 |

---

## 3. 数据模型

### 3.1 模型配置表

```sql
CREATE TABLE admin_model_configs (
    id UUID PRIMARY KEY,
    model_id VARCHAR(50) UNIQUE NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    provider VARCHAR(50),
    base_url VARCHAR(255),
    api_key VARCHAR(255),
    capabilities JSONB,
    max_tokens INTEGER DEFAULT 32000,
    temperature DECIMAL(3,2) DEFAULT 0.7,
    status VARCHAR(20) DEFAULT 'online',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 3.2 Agent模型映射表

```sql
CREATE TABLE admin_agent_model_mappings (
    id UUID PRIMARY KEY,
    system VARCHAR(50) NOT NULL,
    agent_id VARCHAR(50) NOT NULL,
    model_id VARCHAR(50) REFERENCES admin_model_configs(model_id),
    is_active BOOLEAN DEFAULT true,
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(system, agent_id)
);
```

---

## 4. API 规格

### 4.1 客户管理

```
GET    /api/admin/customers
GET    /api/admin/customers/{customer_code}
PUT    /api/admin/customers/{customer_code}
DELETE /api/admin/customers/{customer_code}
```

### 4.2 政策管理

```
GET    /api/admin/policies
GET    /api/admin/policies/{citation_id}
PUT    /api/admin/policies/{citation_id}
DELETE /api/admin/policies/{citation_id}
```

### 4.3 方案管理

```
GET    /api/admin/solutions
GET    /api/admin/solutions/{solution_id}
PUT    /api/admin/solutions/{solution_id}
DELETE /api/admin/solutions/{solution_id}
```

### 4.4 模型配置

```
GET    /api/admin/models
POST   /api/admin/models
PUT    /api/admin/models/{model_id}
DELETE /api/admin/models/{model_id}
POST   /api/admin/models/{model_id}/test

GET    /api/admin/agent-mappings
PUT    /api/admin/agent-mappings
```

---

## 5. 页面布局

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  智能体系统后台                                                              │
├────────────┬────────────────────────────────────────────────────────────────┤
│            │                                                                │
│  📋 客户   │                                                                │
│  📋 政策   │                      主内容区域                                │
│  📋 方案   │                                                                │
│  ⚙ 模型   │                                                                │
│            │                                                                │
└────────────┴────────────────────────────────────────────────────────────────┘
```

---

## 6. 实施计划

| 阶段 | 内容 |
|------|------|
| 阶段一 | 导航框架 |
| 阶段二 | 客户管理 CRUD |
| 阶段三 | 政策管理 CRUD |
| 阶段四 | 方案管理 CRUD |
| 阶段五 | 模型配置 + Agent映射 |

预计工期：3-5 天

---

## 7. 验收标准

- [ ] 4个模块均可正常增删改查
- [ ] 模型可测试连接
- [ ] Agent映射可切换模型
