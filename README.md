# deepseek

`deepseek` 是一个本地 Outlook 邮件检索工具，支持读取过去 24 小时内的邮件并将邮件正文保存到本地目录。

## 先决条件

- Windows 10/11
- 已安装 Microsoft Outlook 桌面客户端
- Python 3.10+
- 安装 pywin32：

```powershell
pip install pywin32
```

## 使用方法

```powershell
python main.py
```

默认会读取 Outlook 默认收件箱（Inbox）最近 24 小时的邮件，并将正文保存到 `email_bodies/`。

### 可选参数

```powershell
python main.py --folder "Inbox" --output-dir "email_bodies"
```

- `--folder`：指定 Outlook 文件夹名称，默认 `Inbox`。
- `--output-dir`：指定邮件正文保存目录，默认 `email_bodies`。
- `--hours`：指定检索时间范围（小时），默认 `24`。

## 输出

脚本会打印邮件数量、目录路径和每封邮件的主题、发件人、接收时间以及正文预览。

## 仓库说明

本仓库还包含 agent skill 配置：

- `.agents/skills/`：已安装的 Matt Pocock 中文 skill
- `docs/agents/`：agent 文档说明
- `CONTEXT.md`：项目上下文说明
- `docs/adr/`：架构决策记录目录
