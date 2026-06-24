from __future__ import annotations

from typing import List, Tuple

from .analyzer import AnalyzerConfig, analyze_emails
from .fetcher import fetch_emails
from .models import Email, EmailAnalysis, EmailExport, PriorityResult
from .prioritizer import prioritize_emails
from .storage import save_emails


def run_pipeline(
    folder_name: str = "Inbox",
    hours: int = 24,
    output_dir: str = "email_bodies",
    provider: str = "mock",
    analysis_limit: int | None = None,
) -> Tuple[List[Email], List[EmailExport], List[EmailAnalysis], List[PriorityResult]]:
    """执行 Outlook 邮件采集、存储、分析和优先级评估流水线。"""
    emails = fetch_emails(folder_name=folder_name, hours=hours)
    exports = save_emails(emails, output_dir=output_dir)
    analyses = analyze_emails(
        exports,
        AnalyzerConfig(provider=provider, max_emails=analysis_limit),
    )
    priorities = prioritize_emails(analyses)

    return emails, exports, analyses, priorities
