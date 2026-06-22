# 项目背景

仓库名：deepseek
用途：本项目为本地 Outlook 邮件检索与相关工具的小型实用程序，包含用于从本地 MAPI/pywin32 读取邮件并将邮件正文保存到 `email_bodies/` 的脚本。

## 关键点

- `Outlook`：通过本地 MAPI（pywin32）访问（详见 `main.py`）。
- `email_bodies/`：脚本将最近的邮件正文保存到此目录，以便后续处理或测试。

## 维护者

- 主要维护人：zhijian.wang@trinasolar.com

## 项目布局与约定

- 单一上下文仓库：在仓库根放置 `CONTEXT.md`，架构决策放在 `docs/adr/`。
