from __future__ import annotations

import json
from typing import List

from .models import AnalysisRequest, EmailAnalysis, EmailExport


REQUIRED_RESULT_FIELDS = (
    "summary",
    "category",
    "intent",
    "priority_score",
    "key_phrases",
)


class AnalysisProviderError(RuntimeError):
    pass


class AnalyzerConfig:
    def __init__(self, provider="mock", max_emails: int | None = None):
        self.provider = provider
        self.max_emails = max_emails


class MockAnalysisProvider:
    def analyze(self, request):
        body = request.body or ""
        text_for_analysis = f"{request.subject} {body}".strip()
        summary = text_for_analysis[:200].replace("\n", " ").strip()
        priority_score = 0.5 if len(body) < 500 else 0.8
        category = "一般"
        intent = "阅读"

        if any(phrase in text_for_analysis for phrase in ["紧急", "马上", "立即"]):
            priority_score = 0.95
            category = "紧急"
            intent = "立即处理"

        key_phrases = [
            phrase
            for phrase in ["紧急", "马上", "立即"]
            if phrase in text_for_analysis
        ]

        return {
            "summary": summary,
            "category": category,
            "intent": intent,
            "priority_score": priority_score,
            "key_phrases": key_phrases,
        }


class OpenAIAnalysisProvider:
    def __init__(
        self,
        client=None,
        model: str = "gpt-5.4-nano",
        max_body_chars: int = 2000,
    ):
        self.client = client
        self.model = model
        self.max_body_chars = max_body_chars

    def analyze(self, request: AnalysisRequest):
        client = self.client or self._default_client()
        response = client.responses.create(
            model=self.model,
            input=self._build_prompt(request),
        )
        return json.loads(response.output_text)

    def _default_client(self):
        try:
            from openai import OpenAI
        except ImportError as error:
            raise RuntimeError("需要安装 OpenAI SDK: pip install openai") from error
        return OpenAI()

    def _build_prompt(self, request: AnalysisRequest):
        body = (request.body or "")[: self.max_body_chars]
        return (
            "你是邮件分析助手。请分析下面的邮件，并只返回 JSON，不要返回 Markdown。\n"
            "JSON 字段必须包含: summary, category, intent, priority_score, key_phrases。\n"
            "priority_score 必须是 0 到 1 之间的小数；key_phrases 必须是字符串数组。\n\n"
            f"Subject: {request.subject}\n"
            f"Sender: {request.sender}\n"
            f"Received time: {request.received_time}\n"
            f"Entry ID: {request.entry_id}\n"
            f"Folder: {request.folder}\n"
            f"Export path: {request.export_path}\n\n"
            f"Body:\n{body}"
        )


def _resolve_provider(config: AnalyzerConfig):
    if config.provider == "mock":
        return MockAnalysisProvider()
    if config.provider == "openai":
        return OpenAIAnalysisProvider()
    if hasattr(config.provider, "analyze"):
        return config.provider
    raise NotImplementedError("当前仅支持 mock 分析器，后续可接入 OpenAI/Azure/Local LLM")


def _build_analysis_request(export: EmailExport):
    email = export.email
    return AnalysisRequest(
        subject=email.subject,
        sender=email.sender,
        received_time=email.received_time,
        body=email.body,
        entry_id=email.entry_id,
        folder=email.folder,
        export_path=export.export_path,
    )


def _validate_provider_result(result, email):
    missing_fields = [field for field in REQUIRED_RESULT_FIELDS if field not in result]
    if missing_fields:
        fields = ", ".join(missing_fields)
        raise AnalysisProviderError(
            f"分析结果缺少字段: {fields}; subject={email.subject!r}, entry_id={email.entry_id!r}"
        )


def _to_email_analysis(email, result):
    return EmailAnalysis(
        email=email,
        summary=result["summary"],
        category=result["category"],
        intent=result["intent"],
        priority_score=result["priority_score"],
        key_phrases=result["key_phrases"],
    )


def _limited_exports(exports: List[EmailExport], max_emails: int | None):
    if max_emails is None:
        return exports
    return exports[:max_emails]


def analyze_emails(
    exports: List[EmailExport], config: AnalyzerConfig | None = None
) -> List[EmailAnalysis]:
    """将已保存邮件发送给分析提供者，并转换为结构化分析结果。"""
    config = config or AnalyzerConfig()
    provider = _resolve_provider(config)

    analyses: List[EmailAnalysis] = []
    for export in _limited_exports(exports, config.max_emails):
        email = export.email
        try:
            result = provider.analyze(_build_analysis_request(export))
        except Exception as error:
            raise AnalysisProviderError(
                f"分析邮件失败: subject={email.subject!r}, entry_id={email.entry_id!r}"
            ) from error
        _validate_provider_result(result, email)

        analyses.append(_to_email_analysis(email, result))

    return analyses
