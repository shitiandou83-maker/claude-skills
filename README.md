# Claude Skills

个人收集整理的 Claude Code 自定义技能（Skills）。

## Skills 列表

### 1. product-design（产品设计）

一套完整的产品设计流程技能，包含竞品分析、需求分析、产品原型、PRD 文档四个步骤，支持新需求、版本迭代、修改已有版本三种模式。

- **版本**：v2.5.0
- **特性**：
  - 四步流程：竞品分析 → 需求分析 → 产品原型 → PRD 文档
  - 三种模式：新需求 / 版本迭代 / 修改已有版本
  - 内置 DongDesign 2.0 B 端设计规范知识库（页面/列表页/图标）
  - 需求讨论记录机制（记录方案对比、决策理由、否决方案、待确认项）
  - 原型生成遵循 B 端规范（1440×900、顶导航 48px、左导航 200px 等）
  - PRD 输出：Markdown 直接输出，docx 需询问确认后才截图+生成
  - 业务知识库自动沉淀
  - 模板与流程分离，SKILL.md 精简，模板按需读取

```
product-design/
├── SKILL.md                              # 技能定义（流程+规则）
└── knowledge/
    ├── b端页面设计规范.md                  # 容器/文本/按钮/导航
    ├── b端列表页规范.md                    # 组件构成/框架布局/表格分页
    ├── b端图标规范.md                      # Outlined/Filled 图标速查
    └── templates/
        ├── 竞品分析报告模板.md              # 竞品分析报告 Markdown 模板
        ├── 需求文档模板.md                  # 需求文档 Markdown 模板
        ├── 需求讨论记录模板.md              # 需求讨论记录 Markdown 模板
        ├── PRD文档模板.md                   # PRD文档 Markdown 模板
        └── 业务知识库模板.md                # 业务知识库 Markdown 模板
└── scripts/
    ├── screenshot.py                     # 原型截图脚本
    ├── screenshot_schema_example.json   # 截图配置模板
    ├── gen_prd_docx.py                 # PRD docx 生成脚本
    └── prd_docx_schema_example.json   # docx 配置模板
```

### 2. user-guide-creator（用户手册生成）

根据 PRD 文档自动生成面向终端用户的使用指引，输出三个文件（用户手册.docx / 用户手册.md / 功能简介.md）。

- **特性**：
  - 输出 3 个文件：用户手册.docx（含原型截图）、用户手册.md、功能简介.md
  - 自动截图原型 HTML 页面（Playwright 无头浏览器）
  - 参数化脚本，支持 JSON 配置驱动
  - 写作规范：去"测试用例"化、emoji 视觉元素、服务意识

```
user-guide-creator/
├── SKILL.md                      # 技能定义
└── scripts/                      # 参数化脚本
    ├── gen_docx.py               # docx 生成脚本
    ├── screenshot.py             # 原型截图脚本
    ├── doc_schema_example.json   # docx 配置模板
    └── screenshot_schema_example.json  # 截图配置模板
```

## 使用方法

将对应技能目录复制到 Claude Code 的 skills 目录：

```bash
# macOS / Linux
cp -r product-design/ ~/.claude/skills/
cp -r user-guide-creator/ ~/.claude/skills/

# Windows
# 复制到 %USERPROFILE%\.claude\skills\
```

重启 Claude Code 后即可使用。

## 环境依赖

### product-design
```bash
pip3 install playwright python-docx
playwright install chromium
```

### user-guide-creator
```bash
pip3 install playwright python-docx
playwright install chromium
```

## License

MIT

### 3. prd-review（PRD 评审自检）

在需求评审前，让 AI 扮演不同角色（研发/设计/运营/用户/老板）对 PRD 进行多角度挑战，提前暴露逻辑漏洞、技术风险、用户体验问题。

- **版本**：v1.0.0
- **特性**：
  - 5 种评审角色：研发/设计/运营/用户/老板，可多选
  - 逐角色按维度检查（研发：技术可行性/接口依赖/数据一致性/性能/安全/扩展性等）
  - 风险分级（高/中/低）+ 可操作建议
  - 评审报告带时间戳，不覆盖历史记录
  - 对比历史评审报告，检查遗留问题修复状态

```
prd-review/
└── SKILL.md                      # 技能定义
```
