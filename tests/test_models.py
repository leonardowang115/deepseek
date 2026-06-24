from datetime import datetime

from src.models import AnalysisRequest, Email, EmailExport, EmailAnalysis, PriorityResult


def test_email_dataclass_fields():
    email = Email(
        subject="主题",
        sender="发件人",
        received_time=datetime(2026, 6, 22, 10, 0),
        body="邮件正文",
        entry_id="id123",
        folder="Inbox",
    )

    assert email.subject == "主题"
    assert email.sender == "发件人"
    assert email.entry_id == "id123"


def test_email_export_dataclass():
    email = Email(
        subject="主题",
        sender="发件人",
        received_time=datetime(2026, 6, 22, 10, 0),
        body="邮件正文",
        entry_id="id123",
        folder="Inbox",
    )
    export = EmailExport(email=email, export_path="email_bodies/Inbox/2026-06-22")

    assert export.email is email
    assert export.export_path.endswith("2026-06-22")


def test_analysis_request_dataclass_fields():
    received_time = datetime(2026, 6, 22, 10, 0)
    request = AnalysisRequest(
        subject="主题",
        sender="发件人",
        received_time=received_time,
        body="邮件正文",
        entry_id="id123",
        folder="Inbox",
        export_path="email_bodies/Inbox/2026-06-22/mail",
    )

    assert request.subject == "主题"
    assert request.sender == "发件人"
    assert request.received_time == received_time
    assert request.body == "邮件正文"
    assert request.entry_id == "id123"
    assert request.folder == "Inbox"
    assert request.export_path.endswith("mail")


def test_priority_result_fields():
    email = Email(
        subject="主题",
        sender="发件人",
        received_time=datetime(2026, 6, 22, 10, 0),
        body="邮件正文",
        entry_id="id123",
        folder="Inbox",
    )
    analysis = EmailAnalysis(
        email=email,
        summary="摘要",
        category="一般",
        intent="阅读",
        priority_score=0.5,
        key_phrases=[],
    )
    result = PriorityResult(analysis=analysis, priority="低", reason="理由")

    assert result.priority == "低"
    assert result.reason == "理由"
