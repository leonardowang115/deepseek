from src.models import Email, EmailAnalysis, EmailExport
from src.prioritizer import prioritize_emails


def test_prioritize_emails_sort_order():
    email = Email(
        subject="测试邮件",
        sender="测试发件人",
        received_time=None,
        body="邮件正文",
        entry_id="id123",
        folder="Inbox",
    )
    analyses = [
        EmailAnalysis(
            email=email,
            summary="摘要",
            category="一般",
            intent="阅读",
            priority_score=0.2,
            key_phrases=[],
        ),
        EmailAnalysis(
            email=email,
            summary="摘要",
            category="紧急",
            intent="立即处理",
            priority_score=0.95,
            key_phrases=["紧急"],
        ),
    ]

    results = prioritize_emails(analyses)
    assert results[0].priority == "高"
    assert results[1].priority == "低"
