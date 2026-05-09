/**
 * 教育信息化政策测试用例
 *
 * 测试场景：收集近五年（2021-2026）国家及教育信息化相关政策
 *
 * 测试步骤：
 * 1. 打开浏览器控制台 (F12)
 * 2. 粘贴本脚本并执行
 * 3. 观察系统是否正确显示政策数据
 * 4. 执行搜索验证检索功能
 */

// 清空现有数据（可选，保留已有数据可以取消注释下一行）
// localStorage.removeItem('policy_collector_data');

// 测试数据：教育信息化相关政策（2021-2026）
const educationPolicies = [
    {
        citation_id: 'PC-EDU-2025-001',
        title: '教育部等九部门关于加快推进教育数字化的意见',
        source: '教育部等九部门',
        source_url: 'https://www.gov.cn/zhengce/zhengceku/202504/content_7019045.htm',
        publish_date: '2025-04-11',
        effective_date: '2025-05-01',
        policy_type: '规范性文件',
        verification_status: 'verified',
        content: `为贯彻落实《教育强国建设规划纲要(2024—2035年)》，以教育数字化为重要突破口，开辟教育发展新赛道和塑造发展新优势，全面支撑教育强国建设，提出如下意见。

一、总体要求
坚持以习近平新时代中国特色社会主义思想为指导，深入实施国家教育数字化战略，坚持应用导向、治理为基，聚焦集成化、智能化、国际化，扩大优质教育资源受益面，促进人工智能助力教育变革，加快形成泛在可及的终身教育体系。

二、深入推进集成化，建强用好国家智慧教育公共服务平台
（一）完善国家智慧教育"四横五纵"平台资源布局
（二）优化教育资源供给
（三）深化平台应用支撑

三、加快推进智能化，推动人工智能助力教育变革
（一）构建人工智能教育应用体系
（二）开发教育专用大模型
（三）推进人工智能赋能教、学、管、评、研

四、扩大国际化，服务全球教育治理
（一）深化数字教育国际合作
（二）输出中国数字教育方案
（三）参与全球数字教育治理

五、保障措施
（一）加强组织领导
（二）完善制度标准
（三）强化资金保障
（四）营造良好氛围`,
        excerpt: '以教育数字化为重要突破口，实施国家教育数字化战略，聚焦集成化、智能化、国际化...',
        relatedPolicies: [],
        customerActions: [],
        created_at: '2025-04-15T10:00:00Z',
        updated_at: '2025-04-15T10:00:00Z'
    },
    {
        citation_id: 'PC-EDU-2025-002',
        title: '教育信息化标准化工作管理办法',
        source: '教育部办公厅',
        source_url: 'https://www.moe.gov.cn/',
        publish_date: '2025-02-01',
        effective_date: '2025-03-01',
        policy_type: '部门规章',
        verification_status: 'verified',
        content: `为加强教育信息化标准化工作，规范教育信息化标准管理，发挥标准在教育数字化战略行动中的支撑引领作用，制定本办法。

第一章 总则
第一条 为了加强教育信息化标准化工作，规范教育信息化标准管理，根据《中华人民共和国标准化法》等法律法规，制定本办法。

第二条 本办法适用于教育信息化标准的制定、实施、监督和管理等活动。

第三条 教育信息化标准化工作坚持统筹规划、协同推进、创新引领、开放合作的原则。

第二章 组织机构与职责
第四条 教育部负责统筹协调全国教育信息化标准化工作。

第三章 标准制定
第五条 制定教育信息化标准应当遵循以下程序：
（一）标准立项
（二）标准起草
（三）技术审查
（四）标准公示
（五）批准发布

第四章 标准实施
第六条 教育信息化标准的实施由各级教育行政部门负责监督落实。

第五章 附则
第七条 本办法自发布之日起施行。`,
        excerpt: '规范教育信息化标准管理，发挥标准在教育数字化战略行动中的支撑引领作用...',
        relatedPolicies: [],
        customerActions: [],
        created_at: '2025-02-05T10:00:00Z',
        updated_at: '2025-02-05T10:00:00Z'
    },
    {
        citation_id: 'PC-EDU-2021-001',
        title: '关于加强新时代教育管理信息化工作的通知',
        source: '教育部',
        source_url: 'https://www.moe.gov.cn/',
        publish_date: '2021-03-26',
        effective_date: '2021-05-01',
        policy_type: '规范性文件',
        verification_status: 'verified',
        content: `为有效解决系统整合不足、数据共享不畅、服务体验不佳、设施重复建设等突出问题，就加强新时代教育管理信息化工作通知。

一、总体要求
（一）指导思想
以习近平新时代中国特色社会主义思想为指导，全面贯彻党的教育方针。

（二）工作目标
到2025年，基本形成新时代教育管理信息化制度体系，信息系统实现优化整合，一体化水平大幅提升，数据孤岛得以打通。

二、重点任务
（一）加强教育管理信息化统筹协调
（二）优化信息系统供给模式
（三）提高教育数据管理水平
（四）促进管理服务流程再造
（五）提高基础设施支撑能力

三、保障措施
（一）加强组织领导
（二）完善制度标准
（三）强化资金保障

四、以信息化支撑教育治理体系和治理能力现代化，推动教育决策由经验驱动向数据驱动转变。`,
        excerpt: '到2025年基本形成新时代教育管理信息化制度体系，解决系统整合不足、数据共享不畅等问题...',
        relatedPolicies: [],
        customerActions: [],
        created_at: '2021-03-28T10:00:00Z',
        updated_at: '2021-03-28T10:00:00Z'
    },
    {
        citation_id: 'PC-EDU-2024-001',
        title: '2024年提升全民数字素养与技能工作要点',
        source: '中央网信办、教育部、工业和信息化部、人力资源社会保障部',
        source_url: 'https://www.moe.gov.cn/',
        publish_date: '2024-02-01',
        effective_date: '2024-02-15',
        policy_type: '政策',
        verification_status: 'verified',
        content: `为加快弥合数字鸿沟，培育高水平复合型数字人才，支撑做强做优做大数字经济，制定本工作要点。

一、总体目标
到2024年底，数字素养与技能提升行动取得积极成效，全民数字素养与技能水平稳步提升。

二、重点任务
（一）培育高水平复合型数字人才
（二）加快弥合数字鸿沟
（三）支撑做强做优做大数字经济
（四）拓展智慧便捷的数字生活场景
（五）打造积极健康有序的网络空间

三、保障措施
（一）强化支撑保障和协调联动
（二）加强宣传引导
（三）做好监测评估`,
        excerpt: '培育高水平复合型数字人才，加快弥合数字鸿沟，支撑数字经济发展...',
        relatedPolicies: [],
        customerActions: [],
        created_at: '2024-02-05T10:00:00Z',
        updated_at: '2024-02-05T10:00:00Z'
    },
    {
        citation_id: 'PC-EDU-2025-003',
        title: '国家教育数字化战略行动2025年部署会精神',
        source: '教育部',
        source_url: 'https://www.moe.gov.cn/',
        publish_date: '2025-04-01',
        effective_date: '2025-04-01',
        policy_type: '政策',
        verification_status: 'verified',
        content: `2025年3月28日，教育部召开国家教育数字化战略行动2025年部署会，会议以"人工智能与教育变革"为主题。

一、会议背景
在国家智慧教育平台开通三周年之际，召开此次部署会，总结"十四五"时期教育数字化成效经验。

二、战略方向
（一）集成化：完善平台资源布局
（二）智能化：推动AI赋能教育
（三）国际化：服务全球教育治理

三、重点部署
（一）落实《教育强国建设规划纲要(2024—2035年)》
（二）高质量实施三年行动计划
（三）推动国家智慧教育平台建设再上新台阶

四、部长讲话要点
教育部党组书记、部长怀进鹏强调，要用好人工智能这一关键变量，以"人工智能+教育"为抓手，推动人工智能融入教育全要素、全过程、全场景。`,
        excerpt: '以"人工智能与教育变革"为主题，推动国家智慧教育平台建设，部署"十五五"时期重点工作...',
        relatedPolicies: [],
        customerActions: [],
        created_at: '2025-04-02T10:00:00Z',
        updated_at: '2025-04-02T10:00:00Z'
    },
    {
        citation_id: 'PC-EDU-2022-001',
        title: '国家教育数字化战略行动启动',
        source: '教育部',
        source_url: 'https://www.moe.gov.cn/',
        publish_date: '2022-03-01',
        effective_date: '2022-03-01',
        policy_type: '政策',
        verification_status: 'verified',
        content: `2022年，教育部启动实施国家教育数字化战略行动。

一、战略背景
为贯彻落实党中央、国务院关于推进教育数字化的决策部署。

二、平台建设
（一）建成国家智慧教育平台
（二）整合各类教育资源
（三）提供"三横五纵"服务体系

三、三年成效
（一）注册用户突破1.64亿
（二）覆盖220余个国家和地区
（三）成为世界第一大教育资源数字化中心和平台

四、战略方向2.0
2025年5月，在武汉举办的2025世界数字教育大会上，将正式启动"国家教育数字化战略行动2.0"。`,
        excerpt: '启动国家教育数字化战略行动，建成国家智慧教育平台，用户突破1.64亿...',
        relatedPolicies: [],
        customerActions: [],
        created_at: '2022-03-05T10:00:00Z',
        updated_at: '2022-03-05T10:00:00Z'
    }
];

// 获取现有政策
function getStoredPolicies() {
    const data = localStorage.getItem('policy_collector_data');
    return data ? JSON.parse(data) : [];
}

// 保存政策
function savePolicies(policies) {
    localStorage.setItem('policy_collector_data', JSON.stringify(policies));
}

// 添加测试数据
function addTestPolicies() {
    const existingPolicies = getStoredPolicies();
    const existingIds = existingPolicies.map(p => p.citation_id);

    let addedCount = 0;
    educationPolicies.forEach(policy => {
        if (!existingIds.includes(policy.citation_id)) {
            existingPolicies.unshift(policy);
            addedCount++;
        }
    });

    savePolicies(existingPolicies);
    return { total: existingPolicies.length, added: addedCount };
}

// 执行测试
function runTest() {
    console.log('=== 教育信息化政策测试用例 ===\n');

    // 1. 添加测试数据
    console.log('1. 添加教育信息化政策数据...');
    const result = addTestPolicies();
    console.log(`   已添加 ${result.added} 条政策，当前共 ${result.total} 条政策\n`);

    // 2. 验证数据
    console.log('2. 验证政策数据:');
    const policies = getStoredPolicies();
    const eduPolicies = policies.filter(p =>
        p.title.includes('教育') ||
        p.title.includes('数字化') ||
        p.title.includes('信息化') ||
        p.title.includes('智慧教育')
    );
    console.log(`   教育相关政策: ${eduPolicies.length} 条\n`);

    // 3. 显示五年内的政策
    console.log('3. 五年内政策列表 (2021-2026):');
    const fiveYearsAgo = new Date();
    fiveYearsAgo.setFullYear(fiveYearsAgo.getFullYear() - 5);

    eduPolicies
        .filter(p => new Date(p.publish_date) >= fiveYearsAgo)
        .sort((a, b) => new Date(b.publish_date) - new Date(a.publish_date))
        .forEach(p => {
            console.log(`   [${p.verification_status === 'verified' ? '✓' : '○'}] ${p.publish_date} - ${p.title}`);
        });

    console.log('\n4. 测试检索功能:');
    console.log('   搜索关键词: "教育信息化"');
    const searchResults = policies.filter(p =>
        p.verification_status === 'verified' && (
            p.title.toLowerCase().includes('教育') ||
            p.title.toLowerCase().includes('信息化') ||
            p.title.toLowerCase().includes('数字化')
        )
    );
    console.log(`   找到 ${searchResults.length} 条已校验的相关政策\n`);

    console.log('=== 测试完成 ===');
    console.log('请在浏览器中打开政策搜集系统，手动验证检索效果。');
    console.log('搜索关键词建议: "教育数字化"、"教育信息化"、"智慧教育"');

    return eduPolicies;
}

// 导出测试函数
window.runEducationPolicyTest = runTest;

// 自动执行
console.log('教育信息化政策测试用例已加载...');
console.log('输入 runEducationPolicyTest() 开始测试\n');
