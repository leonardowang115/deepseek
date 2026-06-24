import os
from datetime import datetime

import pytest

from src.models import Email, EmailAnalysis, EmailExport


@pytest.fixture
def sample_email() -> Email:
    return Email(
        subject="测试邮件",
        sender="测试发件人",
        received_time=datetime(2026, 6, 22, 10, 0),
        body="请你立即处理这件紧急事项。",
        entry_id="id123",
        folder="Inbox",
    )


@pytest.fixture
def sample_export(sample_email) -> EmailExport:
    return EmailExport(email=sample_email, export_path="email_bodies/Inbox/2026-06-22")


@pytest.fixture
def sample_analysis(sample_email) -> EmailAnalysis:
    return EmailAnalysis(
        email=sample_email,
        summary="请你立即处理这件紧急事项。",
        category="紧急",
        intent="立即处理",
        priority_score=0.95,
        key_phrases=["紧急", "立即"],
    )
