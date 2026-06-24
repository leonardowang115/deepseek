import pytest

from src.analyzer import (
    AnalysisProviderError,
    AnalyzerConfig,
    OpenAIAnalysisProvider,
    analyze_emails,
)
from src.models import AnalysisRequest, Email, EmailExport


class FakeAnalysisProvider:
    def __init__(self):
        self.requests = []

    def analyze(self, request):
        self.requests.append(request)
        return {
            "summary": "供应商返回的摘要",
            "category": "客户请求",
            "intent": "需要回复",
            "priority_score": 0.72,
            "key_phrases": ["报价", "交期"],
        }


class FailingAnalysisProvider:
    def analyze(self, request):
        raise RuntimeError("provider unavailable")


class IncompleteAnalysisProvider:
    def analyze(self, request):
        return {
            "summary": "缺少分类字段",
            "intent": "需要回复",
            "priority_score": 0.7,
            "key_phrases": [],
        }


class FakeOpenAIResponse:
    output_text = (
        '{"summary":"需要处理客户投诉","category":"客户投诉",'
        '"intent":"判断风险并回复","priority_score":0.88,'
        '"key_phrases":["投诉","风险","处理建议"]}'
    )


class FakeOpenAIResponses:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return FakeOpenAIResponse()


class FakeOpenAIClient:
    def __init__(self):
        self.responses = FakeOpenAIResponses()


def test_analyze_emails_uses_provider_result():
    email = Email(
        subject="报价咨询",
        sender="客户A",
        received_time=None,
        body="请确认报价和交期。",
        entry_id="id456",
        folder="Inbox",
    )
    export = EmailExport(email=email, export_path="email_bodies/Inbox/mail-1")
    provider = FakeAnalysisProvider()

    analyses = analyze_emails([export], AnalyzerConfig(provider=provider))

    assert len(analyses) == 1
    assert provider.requests == [
        AnalysisRequest(
            subject="报价咨询",
            sender="客户A",
            received_time=None,
            body="请确认报价和交期。",
            entry_id="id456",
            folder="Inbox",
            export_path="email_bodies/Inbox/mail-1",
        )
    ]
    assert analyses[0].email is email
    assert analyses[0].summary == "供应商返回的摘要"
    assert analyses[0].category == "客户请求"
    assert analyses[0].intent == "需要回复"
    assert analyses[0].priority_score == 0.72
    assert analyses[0].key_phrases == ["报价", "交期"]


def test_openai_provider_uses_low_cost_model_and_returns_analysis_result():
    client = FakeOpenAIClient()
    provider = OpenAIAnalysisProvider(client=client)
    request = AnalysisRequest(
        subject="客户升级投诉",
        sender="客户B",
        received_time=None,
        body="请尽快判断风险和处理建议。",
        entry_id="entry-openai-1",
        folder="Inbox",
        export_path="email_bodies/Inbox/mail-4",
    )

    result = provider.analyze(request)

    assert result == {
        "summary": "需要处理客户投诉",
        "category": "客户投诉",
        "intent": "判断风险并回复",
        "priority_score": 0.88,
        "key_phrases": ["投诉", "风险", "处理建议"],
    }
    call = client.responses.calls[0]
    assert call["model"] == "gpt-5.4-nano"
    assert "客户升级投诉" in call["input"]
    assert "请尽快判断风险和处理建议。" in call["input"]


def test_openai_provider_truncates_email_body_to_2000_characters():
    client = FakeOpenAIClient()
    provider = OpenAIAnalysisProvider(client=client)
    request = AnalysisRequest(
        subject="长邮件",
        sender="客户C",
        received_time=None,
        body="A" * 2000 + "TAIL_AFTER_LIMIT",
        entry_id="entry-long-body",
        folder="Inbox",
        export_path="email_bodies/Inbox/mail-5",
    )

    provider.analyze(request)

    prompt = client.responses.calls[0]["input"]
    assert "A" * 2000 in prompt
    assert "TAIL_AFTER_LIMIT" not in prompt


def test_analyze_emails_limits_provider_requests():
    exports = [
        EmailExport(
            email=Email(
                subject=f"测试邮件 {idx}",
                sender="测试发件人",
                received_time=None,
                body="测试正文",
                entry_id=f"entry-{idx}",
                folder="Inbox",
            ),
            export_path=f"email_bodies/Inbox/mail-{idx}",
        )
        for idx in range(6)
    ]
    provider = FakeAnalysisProvider()

    analyses = analyze_emails(
        exports,
        AnalyzerConfig(provider=provider, max_emails=5),
    )

    assert len(analyses) == 5
    assert len(provider.requests) == 5
    assert [request.entry_id for request in provider.requests] == [
        "entry-0",
        "entry-1",
        "entry-2",
        "entry-3",
        "entry-4",
    ]


def test_analyze_emails_adds_email_context_when_provider_fails():
    email = Email(
        subject="合同审批",
        sender="法务",
        received_time=None,
        body="请审批合同。",
        entry_id="entry-789",
        folder="Inbox",
    )
    export = EmailExport(email=email, export_path="email_bodies/Inbox/mail-2")

    with pytest.raises(AnalysisProviderError) as error:
        analyze_emails([export], AnalyzerConfig(provider=FailingAnalysisProvider()))

    assert "合同审批" in str(error.value)
    assert "entry-789" in str(error.value)


def test_analyze_emails_adds_context_when_provider_result_is_incomplete():
    email = Email(
        subject="付款提醒",
        sender="财务",
        received_time=None,
        body="请确认付款状态。",
        entry_id="entry-999",
        folder="Inbox",
    )
    export = EmailExport(email=email, export_path="email_bodies/Inbox/mail-3")

    with pytest.raises(AnalysisProviderError) as error:
        analyze_emails([export], AnalyzerConfig(provider=IncompleteAnalysisProvider()))

    message = str(error.value)
    assert "category" in message
    assert "付款提醒" in message
    assert "entry-999" in message


def test_analyze_emails_mock():
    email = Email(
        subject="紧急请求",
        sender="测试发件人",
        received_time=None,
        body="请你立即处理这件事。",
        entry_id="id123",
        folder="Inbox",
    )
    exports = [EmailExport(email=email, export_path="path")]
    analyses = analyze_emails(exports, AnalyzerConfig(provider="mock"))

    assert len(analyses) == 1
    assert analyses[0].category == "紧急"
    assert analyses[0].intent == "立即处理"
    assert analyses[0].priority_score == 0.95
    assert "紧急" in analyses[0].key_phrases


def test_analyze_emails_resolves_openai_provider(monkeypatch):
    email = Email(
        subject="客户升级投诉",
        sender="客户B",
        received_time=None,
        body="请尽快判断风险和处理建议。",
        entry_id="entry-openai-1",
        folder="Inbox",
    )
    export = EmailExport(email=email, export_path="email_bodies/Inbox/mail-4")
    provider = FakeAnalysisProvider()

    monkeypatch.setattr("src.analyzer.OpenAIAnalysisProvider", lambda: provider)

    analyses = analyze_emails([export], AnalyzerConfig(provider="openai"))

    assert len(analyses) == 1
    assert provider.requests[0].entry_id == "entry-openai-1"
