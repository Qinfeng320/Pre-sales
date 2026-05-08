# 政策搜集智能体系统 (PolicyCollector)

精准政策匹配与溯源系统 - 基于 RAG 知识库检索，返回完整原文引用，100% 人工校验保证准确性。

## 核心功能

- **政策发现与登记** - 用户发现政策 URL 后登记，仅记录元信息
- **来源验证** - 仅允许政府官方域名（gov.cn 等一手来源）
- **人工校验** - 运营人员核对原文，通过后允许检索
- **向量检索** - 混合检索：向量 + BM25 + RRF + Rerank
- **政策关联** - 自动发现政策间的关联关系

## 技术栈

| 组件 | 技术 |
|------|------|
| 向量存储 | Qdrant (Apache 2.0) |
| 关系型 | SQLite / PostgreSQL |
| Embedding | BGE-M3 (MIT) |
| Reranker | BGE-Reranker-v2-m3 (MIT) |
| LLM | DeepSeek-V4 / Qwen2.5 |
| 框架 | FastAPI |
| 容器 | Docker |

## 快速开始

### 1. 克隆项目

```bash
cd policy_collector
```

### 2. 使用 Docker Compose 启动

```bash
docker-compose up -d
```

### 3. 本地开发

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .

# 初始化数据库
python scripts/init_db.py

# 插入测试数据（可选）
python scripts/seed_data.py

# 启动服务
uvicorn policy_collector.main:app --reload --port 8000
```

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口

### 政策登记
```bash
POST /api/v1/policies/discover
```

### 政策搜索
```bash
GET /api/v1/policies/search?q={query}&policy_type={type}&sort={sort}
```

### 政策详情
```bash
GET /api/v1/policies/{citation_id}?include_relations=true&include_customer_actions=true
```

### 补充正文
```bash
PUT /api/v1/policies/{citation_id}/content
```

### 校验政策
```bash
POST /api/v1/policies/{citation_id}/verify
```

### 获取段落
```bash
GET /api/v1/policies/{citation_id}/sections/{section_index}
```

### 客户行为
```bash
POST /api/v1/customer-actions
```

## 环境变量

参考 `.env.example`：

```bash
DATABASE_URL=sqlite+aiosqlite:///./data/policy_collector.db
QDRANT_HOST=localhost
QDRANT_PORT=6333
LOG_LEVEL=INFO
GOV_DOMAINS=gov.cn,mof.gov.cn,mohurd.gov.cn,miit.gov.cn,most.gov.cn,moe.gov.cn,nhc.gov.cn
```

## 项目结构

```
policy_collector/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
├── src/
│   └── policy_collector/
│       ├── __init__.py
│       ├── main.py           # FastAPI 入口
│       ├── config.py         # 配置管理
│       ├── database.py       # 数据库连接
│       ├── models/           # 数据模型
│       ├── api/              # API 路由
│       ├── services/         # 业务逻辑
│       ├── core/             # 核心功能（向量/Embedding）
│       └── utils/            # 工具函数
├── scripts/
│   ├── init_db.py           # 数据库初始化
│   └── seed_data.py         # 测试数据
└── tests/                   # 测试
```

## 数据模型

### documents (政策主表)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| citation_id | VARCHAR | 引用ID (POL-2024-001) |
| title | TEXT | 政策标题 |
| source_url | TEXT | 来源URL |
| publish_date | DATE | 发布日期 |
| issuing_authority | VARCHAR | 发布机构 |
| policy_type | VARCHAR | 政策类型 |
| content | TEXT | 正文内容 |
| content_pending | BOOLEAN | 正文是否待补充 |
| verification_status | VARCHAR | 校验状态 |
| verified_at | TIMESTAMP | 校验时间 |

### document_sections (段落表)
段落表存储政策的分段内容，支持精准条款引用。

### policy_relations (政策关联表)
| 关联类型 | 说明 |
|----------|------|
| 上位法/下位法 | 法律层级关系 |
| 系列政策 | 同一主题延续 |
| 继承/修订 | 旧政策废止→新政策替代 |
| 同源机构 | 同一发布机构 |
| 主题相关 | 关键词/行业相似 |
| 引用关系 | 正文引用其他政策 |

### customer_policy_actions (客户行为表)
记录 B 端客户在政策下的实践行为（申报/领补贴/享受优惠/合规整改）。

## 实施阶段

| 阶段 | 内容 | 交付物 |
|------|------|--------|
| 阶段一 (2周) | 核心存储 + 政策登记 + 向量检索 | 可登记政策、可检索原型 |
| 阶段二 (1周) | 人工校验 + 关联管理 + SDK | 准确性保障体系 |
| 阶段三 (1周) | 本地测试 + 阿里云部署 | 生产可用系统 |

## License

MIT
