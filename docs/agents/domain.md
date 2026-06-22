# 域文档（Domain Docs）

工程类技能在探索代码库时，需如何使用本仓库的域文档：

必读（优先顺序）：
- 根目录的 `CONTEXT.md`：项目概述与关键术语
- `docs/adr/`：架构决策记录（ADRs），说明重大设计/决策历史

仓库布局（单上下文示例）：
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-example.md
	└── 0002-another-decision.md
└── src/

说明：
- 本仓库采用 single-context 布局（即只有一个 `CONTEXT.md`）。
- 若未来改为多上下文（例如 monorepo），请改为使用 `CONTEXT-MAP.md` 指向各子上下文。