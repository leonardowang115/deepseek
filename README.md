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
python main.py --folder "Inbox" --output-dir "email_bodies" --hours 24
```

- `--folder`：指定 Outlook 文件夹名称，默认 `Inbox`。
- `--output-dir`：指定邮件正文保存目录，默认 `email_bodies`。
- `--hours`：指定检索时间范围（小时），默认 `24`。

## 输出结构

程序会将每封邮件保存到如下结构：

```
email_bodies/
  Inbox/
    2026-06-22/
      20260622_091234_sender_subject/
        body.txt
        metadata.json
```

每封邮件目录包含：

- `body.txt`：邮件正文
- `metadata.json`：邮件主题、发件人、接收时间、EntryID、来源文件夹等元数据

脚本执行完后会打印保存目录、邮件总数，以及前 5 个保存的邮件目录，方便快速检查。 

## 仓库说明

本仓库还包含 agent skill 配置：

- `.agents/skills/`：已安装的 Matt Pocock 中文 skill
- `skills-lock.json`：skill 版本锁定文件
- `docs/agents/`：agent 文档说明
- `CONTEXT.md`：项目上下文说明
- `docs/adr/`：架构决策记录目录

## 跨设备同步

该项目已将 `.agents/skills` 和 `skills-lock.json` 一并提交到仓库，因此在另一台设备上克隆后，支持 skill 的 agent 环境可以直接使用这些 skill 定义。

推荐流程：

```powershell
git clone https://github.com/leonardowang115/deepseek.git
cd deepseek
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

如果你的 agent 环境没有自动加载 `.agents`，请检查你的 Copilot/agent 工具是否将仓库根目录作为 skill 根目录。

## 生成目录

`email_bodies/` 为脚本运行时生成的目录，已添加到 `.gitignore`，不会被同步到 GitHub。
