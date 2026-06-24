# 1. Outlook 邮件 Agent Pipeline

状态: Accepted

## 背景

当前项目已实现从本地 Outlook 读取最近 N 小时邮件并保存正文的初步功能。下一步目标是将这套流程扩展为一个 agent pipeline，能够让大模型分析邮件并给出优先级建议。

用户希望的整体流程为：

1. 读取指定时间范围内的 Outlook 邮件
2. 将邮件正文和元数据保存为可重用的本地结构化数据
3. 使用大模型对邮件内容进行分析和摘要
4. 生成邮件优先级、处理建议或后续 agent 任务

## 决策

我们决定采用模块化架构，将邮件获取、存储、分析、优先级评估四个职责分离：

- `fetcher`：负责从 Outlook 中按时间范围检索邮件
- `storage`：负责将邮件正文、元数据以及索引保存到本地目录
- `analyzer`：负责将已保存邮件转换为大模型输入，并调用模型进行分析
- `prioritizer`：负责将分析结果映射为结构化优先级、分类和行动建议

模块边界尽量清晰，避免让 Outlook 特定逻辑与大模型调用混在一起。

## 执行方案

接口建议如下：

- `fetch_emails(folder_name: str, hours: int) -> list[Email]`
- `save_emails(emails: list[Email], output_dir: str) -> list[EmailExport]`
- `analyze_emails(emails: list[EmailExport], config: AnalysisConfig) -> list[EmailAnalysis]`
- `prioritize_emails(analysis: list[EmailAnalysis], strategy: str) -> list[PriorityResult]`

数据模型建议：

- `Email`：原始邮件字段（subject、sender、received_time、body、entry_id、folder）
- `EmailExport`：本地保存路径 + `Email` 数据
- `EmailAnalysis`：模型输出（摘要、主题、意图、风险、优先级得分）
- `PriorityResult`：最终排序结果、建议动作、理由说明

## 预期成果

- 支持时间范围查询（例如最近 24 小时、48 小时、7 天等）
- 支持通过本地保存结果重用同一批邮件进行多次分析
- 支持多种大模型提供者（如 OpenAI、Azure、local LLM）
- 支持不同优先级策略：紧急/重要、快速处理、长期跟进等
- 支持 agent 级别的后续执行提示，例如 "请立即回复"、"标记为待办"、"忽略此邮件"

## 影响

- 好处：架构清晰、模块可复用、后续扩展到 agent 系统更容易
- 风险：需要明确数据格式与模型输入输出协议，初期实现会多一层抽象
- 兼容性：保留当前 `main.py` 作为初始采集入口，逐步拆分到独立模块
