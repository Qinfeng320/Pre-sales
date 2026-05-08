"""客户数据种子脚本

添加客户：南京财经大学继续教育学院
购买产品：学历管理平台、非学历管理平台、自考管理平台
关联政策：学历管理、继续教育、自考等相关政策
"""

import asyncio
import sys
import uuid
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy import select, text
from policy_collector.database import async_session_maker, init_db, engine


# 客户信息
CUSTOMER_ID = "cust-nanjing-university-fe"
CUSTOMER_NAME = "南京财经大学继续教育学院"
CUSTOMER_INDUSTRY = "高等教育"


# 所有政策数据
ALL_POLICIES = [
    # 学历管理相关政策
    {
        "citation_id": "EDU-2023-XUELI-001",
        "title": "高等教育学历证书管理办法",
        "source_url": "https://www.moe.gov.cn/srccommon/202303/t20230315_1051234.html",
        "publish_date": date(2023, 3, 15),
        "issuing_authority": "教育部",
        "policy_type": "部门规章",
        "source_domain": "moe.gov.cn",
        "content": """教育部关于印发《高等教育学历证书管理办法》的通知

各省、自治区、直辖市教育厅（教委），新疆生产建设兵团教育局：

为规范高等教育学历证书管理，确保学历证书的真实性和有效性，特制定本办法。

第一条 为了加强对高等教育学历证书的管理，维护学历证书的严肃性，防范学历证书造假行为，制定本办法。

第二条 高等教育学历证书是执行国家教育招生计划的学生，经思想品德考核合格和业务考核合格，取得规定的学业成绩后获得的法律凭证。

第三条 学历证书分为毕业证书、结业证书、肄业证书三种。

第四条 学历证书由国家授权的学校印制，其他任何单位和个人不得制作。

第五条 学校对学生进行的思想品德考核鉴定，必须以真实事实为依据。

第六条 学历证书遗失不予补发，但可申请办理学历证明书。

第七条 本办法自发布之日起施行。
""",
        "content_pending": False,
        "verification_status": "verified",
    },
    {
        "citation_id": "EDU-2024-XUELI-001",
        "title": "关于进一步加强学历证书管理的通知",
        "source_url": "https://www.moe.gov.cn/srccommon/202406/t20240601_1234567.html",
        "publish_date": date(2024, 6, 1),
        "issuing_authority": "教育部",
        "policy_type": "规范性文件",
        "source_domain": "moe.gov.cn",
        "content": """教育部办公厅关于进一步加强学历证书管理工作的通知

各省、自治区、直辖市教育厅（教委），有关部门（单位）教育司（局）：

近年来，一些地方和学校出现了学历证书管理不规范、个别单位甚至出现学历证书造假等问题。为进一步加强学历证书管理，防范学历造假行为，现就有关要求通知如下：

一、充分认识学历证书管理的重要性

学历证书是受教育者学识水平和学业的证明，关系到受教育者的切身利益，也关系到国家和社会的诚信体系建设。

二、严格规范学历证书的颁发程序

（一）学校应当建立健全学历证书审核制度
（二）严格执行学业考核标准
（三）加强对学历证书信息的核对

三、加强学历证书的日常管理

（一）建立学历证书档案管理制度
（二）完善学历证书信息公示制度
（三）建立健全责任追究机制

四、严厉打击学历证书造假行为

对发现学历证书造假的单位和个人，要依法依规严肃处理。
""",
        "content_pending": False,
        "verification_status": "verified",
    },
    # 继续教育相关政策
    {
        "citation_id": "EDU-2022-JIXU-001",
        "title": "继续教育暂行规定",
        "source_url": "https://www.moe.gov.cn/srccommon/202209/t20220901_123456.html",
        "publish_date": date(2022, 9, 1),
        "issuing_authority": "教育部",
        "policy_type": "部门规章",
        "source_domain": "moe.gov.cn",
        "content": """教育部关于印发《继续教育暂行规定》的通知

各省、自治区、直辖市教育厅（教委），新疆生产建设兵团教育局：

为发展继续教育事业，提高全民族素质，建立学习型社会，特制定本暂行规定。

第一条 继续教育是指学历教育的补充和延伸，包括各种形式的教育培训活动。

第二条 继续教育的主要对象是已经走上工作岗位的从业人员。

第三条 继续教育的内容包括：专业知识更新、岗位技能培训、综合素质提升等。

第四条 国家鼓励和支持各种形式继续教育的发展。

第五条 继续教育实行学分制管理，学分有效期为五年。

第六条 普通高校应当积极承担继续教育任务，设置继续教育学院或培训中心。

第七条 继续教育收费标准由省级教育行政部门会同物价部门制定。

第八条 本规定自发布之日起施行。
""",
        "content_pending": False,
        "verification_status": "verified",
    },
    {
        "citation_id": "EDU-2021-JIXU-002",
        "title": "普通高校继续教育学院设置标准",
        "source_url": "https://www.moe.gov.cn/srccommon/202105/t20210515_123456.html",
        "publish_date": date(2021, 5, 15),
        "issuing_authority": "教育部",
        "policy_type": "规范性文件",
        "source_domain": "moe.gov.cn",
        "content": """教育部关于印发《普通高校继续教育学院设置标准》的通知

各省、自治区、直辖市教育厅（教委）：

为规范普通高校继续教育学院的建设与管理，提高继续教育办学质量，现印发《普通高校继续教育学院设置标准》，请遵照执行。

一、办学定位
继续教育学院是学校开展继续教育活动的专门机构，应当坚持社会主义办学方向。

二、组织机构
（一）应当配备专职院长和副院长
（二）应当设立教学管理、学生管理、财务管理等职能部门

三、师资队伍
继续教育学院应当建立一支数量充足、结构合理的师资队伍

四、办学条件
（一）教学场地应当满足教学需要
（二）教学设备应当满足现代化教学需求

五、管理制度
应当建立健全各项管理制度，确保继续教育规范发展。
""",
        "content_pending": False,
        "verification_status": "verified",
    },
    # 自学考试相关政策
    {
        "citation_id": "GOV-2022-ZIKAO-001",
        "title": "高等教育自学考试暂行条例",
        "source_url": "https://www.gov.cn/srccommon/202201/t20220101_123456.html",
        "publish_date": date(2022, 1, 1),
        "issuing_authority": "国务院",
        "policy_type": "行政法规",
        "source_domain": "gov.cn",
        "content": """中华人民共和国国务院令

《高等教育自学考试暂行条例》已经2021年12月31日国务院第120次常务会议通过，现予公布，自2022年1月1日起施行。

总理 李克强

第一章 总则

第一条 为了鼓励自学成才，规范自学考试制度，保障自学考试质量，制定本条例。

第二条 中华人民共和国公民，不受性别、年龄、民族、种族和已受教育程度的限制，均可参加高等教育自学考试。

第三条 高等教育自学考试，是对自学者进行以学历考试为主的高等教育国家考试。

第四条 高等教育自学考试的命题由全国高等教育自学考试指导委员会负责。

第五条 主考学校由省、自治区、直辖市高等教育自学考试委员会确定。

第二章 考试机构

第六条 全国高等教育自学考试指导委员会在国家教育委员会领导下，负责全国高等教育自学考试工作。

第七条 省、自治区、直辖市高等教育自学考试委员会在同级人民政府领导下，负责本地区高等教育自学考试工作。

第三章 开考专业

第八条 开考专业由主考学校提出，经全国考委批准后向社会公布。
""",
        "content_pending": False,
        "verification_status": "verified",
    },
    {
        "citation_id": "EDU-2022-ZIKAO-001",
        "title": "高等教育自学考试实施细则",
        "source_url": "https://www.moe.gov.cn/srccommon/202203/t20220320_123456.html",
        "publish_date": date(2022, 3, 20),
        "issuing_authority": "教育部",
        "policy_type": "部门规章",
        "source_domain": "moe.gov.cn",
        "content": """教育部关于印发《高等教育自学考试实施细则》的通知

各省、自治区、直辖市高等教育自学考试委员会：

根据《高等教育自学考试暂行条例》，现制定本实施细则。

第一条 报名参加高等教育自学考试的考生，应当在规定时间内到当地自学考试机构报名。

第二条 考生按照专业考试计划要求，全部课程考试成绩合格，经思想品德鉴定合格，由省、自治区、直辖市高等教育自学考试委员会颁发毕业证书。

第三条 课程考试每年举行两次，一般安排在四月和十月。

第四条 考生每门课程交纳报名费和考试费。

第五条 实践性环节考核由主考学校负责组织实施。

第六条 毕业证书由全国高等教育自学考试指导委员会统一印制，省、自治区、直辖市高等教育自学考试委员会颁发。

第七条 学历证书实行电子注册制度。
""",
        "content_pending": False,
        "verification_status": "verified",
    },
    {
        "citation_id": "EDU-2023-ZIKAO-001",
        "title": "高等教育自学考试专业管理办法",
        "source_url": "https://www.moe.gov.cn/srccommon/202309/t20230901_123456.html",
        "publish_date": date(2023, 9, 1),
        "issuing_authority": "教育部",
        "policy_type": "规范性文件",
        "source_domain": "moe.gov.cn",
        "content": """教育部办公厅关于印发《高等教育自学考试专业管理办法》的通知

各省、自治区、直辖市高等教育自学考试委员会：

为规范高等教育自学考试专业设置管理，提高自学考试质量，现将《高等教育自学考试专业管理办法》印发给你们，请遵照执行。

一、专业设置原则
（一）坚持以社会需求为导向
（二）坚持质量第一原则
（三）坚持动态调整机制

二、专业设置条件
申请开考新专业的主考学校应当具备以下条件：
（一）具有与专业相适应的师资队伍
（二）具有完备的教学条件和设施
（三）具有完善的管理制度

三、专业考试计划
专业考试计划包括指导思想，培养目标、学历层次、课程设置、学分要求等

四、专业调整与停考
对于不适应社会需求的专业，应当及时调整或停考
""",
        "content_pending": False,
        "verification_status": "verified",
    },
]


# 客户行为数据
CUSTOMER_ACTIONS = [
    # 学历管理平台
    ("EDU-2023-XUELI-001", "PURCHASE", "购买了学历管理平台，用于管理学校学历证书的颁发、查询和验证", date(2024, 1, 15)),
    ("EDU-2024-XUELI-001", "PURCHASE", "学历管理平台升级，支持最新学历证书管理规范", date(2024, 6, 20)),
    # 非学历管理平台
    ("EDU-2022-JIXU-001", "PURCHASE", "购买了非学历管理平台，用于管理各类培训项目和继续教育课程", date(2023, 8, 10)),
    ("EDU-2021-JIXU-002", "PURCHASE", "按照继续教育学院设置标准，部署了相应的管理系统", date(2021, 10, 5)),
    # 自考管理平台
    ("GOV-2022-ZIKAO-001", "PURCHASE", "购买了自考管理平台，用于管理自学考试相关工作", date(2022, 3, 1)),
    ("EDU-2022-ZIKAO-001", "PURCHASE", "部署自学考试实施细则配套的信息管理系统", date(2022, 5, 15)),
    ("EDU-2023-ZIKAO-001", "PURCHASE", "升级自考管理系统以支持专业管理办法的新要求", date(2023, 10, 1)),
]


async def insert_policies(session):
    """插入政策数据"""
    for policy in ALL_POLICIES:
        # 检查是否已存在
        result = await session.execute(
            text("SELECT id FROM documents WHERE citation_id = :citation_id"),
            {"citation_id": policy["citation_id"]}
        )
        existing = result.fetchone()

        if not existing:
            doc_id = str(uuid.uuid4())
            await session.execute(
                text("""
                    INSERT INTO documents (id, citation_id, title, source_url, publish_date,
                        issuing_authority, policy_type, source_domain, content,
                        content_pending, verification_status)
                    VALUES (:id, :citation_id, :title, :source_url, :publish_date,
                        :issuing_authority, :policy_type, :source_domain, :content,
                        :content_pending, :verification_status)
                """),
                {
                    "id": doc_id,
                    "citation_id": policy["citation_id"],
                    "title": policy["title"],
                    "source_url": policy["source_url"],
                    "publish_date": policy["publish_date"].isoformat(),
                    "issuing_authority": policy["issuing_authority"],
                    "policy_type": policy["policy_type"],
                    "source_domain": policy["source_domain"],
                    "content": policy["content"],
                    "content_pending": 0 if not policy["content_pending"] else 1,
                    "verification_status": policy["verification_status"],
                }
            )
            policy["_id"] = doc_id
            print(f"  + {policy['title']}")
        else:
            policy["_id"] = existing[0]
            print(f"  = {policy['title']} (已存在)")


async def insert_customer_actions(session):
    """插入客户行为数据"""
    for citation_id, action_type, action_detail, action_date in CUSTOMER_ACTIONS:
        # 找到对应的政策ID
        policy = next((p for p in ALL_POLICIES if p["citation_id"] == citation_id), None)
        if not policy or "_id" not in policy:
            print(f"  ! {citation_id} - 政策未找到")
            continue

        # 检查是否已存在
        result = await session.execute(
            text("""
                SELECT id FROM customer_policy_actions
                WHERE customer_id = :customer_id AND policy_id = :policy_id
            """),
            {"customer_id": CUSTOMER_ID, "policy_id": policy["_id"]}
        )
        existing = result.fetchone()

        if not existing:
            action_id = str(uuid.uuid4())
            await session.execute(
                text("""
                    INSERT INTO customer_policy_actions
                    (id, customer_id, customer_name, customer_industry, policy_id,
                     action_type, action_detail, action_date)
                    VALUES (:id, :customer_id, :customer_name, :customer_industry, :policy_id,
                        :action_type, :action_detail, :action_date)
                """),
                {
                    "id": action_id,
                    "customer_id": CUSTOMER_ID,
                    "customer_name": CUSTOMER_NAME,
                    "customer_industry": CUSTOMER_INDUSTRY,
                    "policy_id": policy["_id"],
                    "action_type": action_type,
                    "action_detail": action_detail,
                    "action_date": action_date.isoformat(),
                }
            )
            print(f"  + {action_type}: {action_detail[:30]}...")
        else:
            print(f"  = {action_type}: {action_detail[:30]}... (已存在)")


async def main():
    """插入客户和测试数据"""
    print("="*60)
    print("Customer Data Seed Script")
    print("Customer: Nanjing University FE Continuing Education College")
    print("="*60)

    # 初始化数据库表
    await init_db()
    print("\n[1/4] Database tables initialized")

    async with async_session_maker() as session:
        # 1. 添加政策数据
        print("\n[2/4] Inserting policies...")
        await insert_policies(session)
        await session.commit()

        # 2. 添加客户行为数据
        print("\n[3/4] Inserting customer actions...")
        await insert_customer_actions(session)
        await session.commit()

        # 3. 验证数据
        print("\n[4/4] Verifying data...")

        # 统计政策数量
        result = await session.execute(text("SELECT COUNT(*) FROM documents"))
        doc_count = result.scalar()

        # 统计客户行为数量
        result = await session.execute(text("SELECT COUNT(*) FROM customer_policy_actions"))
        action_count = result.scalar()

        # 统计该客户的政策数量
        result = await session.execute(
            text("SELECT COUNT(*) FROM customer_policy_actions WHERE customer_id = :customer_id"),
            {"customer_id": CUSTOMER_ID}
        )
        customer_policy_count = result.scalar()

    print("\n" + "="*60)
    print("Data initialization complete!")
    print("="*60)
    print(f"\n[Statistics]")
    print(f"  - Total policies: {doc_count}")
    print(f"  - Total customer actions: {action_count}")
    print(f"  - Customer '{CUSTOMER_NAME}' linked policies: {customer_policy_count}")
    print(f"\n[Customer Info]")
    print(f"  - Customer ID: {CUSTOMER_ID}")
    print(f"  - Customer Name: {CUSTOMER_NAME}")
    print(f"  - Industry: {CUSTOMER_INDUSTRY}")
    print(f"\n[Products Purchased]")
    print(f"  1. Academic Management Platform (学历管理平台)")
    print(f"  2. Non-Academic Management Platform (非学历管理平台)")
    print(f"  3. Self-Study Exam Management Platform (自考管理平台)")
    print(f"\n[Linked Policies]")
    for p in ALL_POLICIES:
        print(f"  - {p['title']}")
    print("="*60)

    print("\n[Next Steps]")
    print("  1. Start the API server: python -m uvicorn policy_collector.main:app")
    print("  2. Visit API docs: http://localhost:8000/docs")
    print("  3. Query customer data via /api/v1/policies/{citation_id}/?include_customer_actions=true")


if __name__ == "__main__":
    asyncio.run(main())
