from unittest.mock import Mock

import src.pipeline as pipeline


from src.pipeline import run_pipeline


def test_run_pipeline_calls_components(monkeypatch):
    mocked_emails = [Mock()]
    mocked_exports = [Mock()]
    mocked_analyses = [Mock()]
    mocked_priorities = [Mock()]

    monkeypatch.setattr("src.pipeline.fetch_emails", Mock(return_value=mocked_emails))
    monkeypatch.setattr("src.pipeline.save_emails", Mock(return_value=mocked_exports))
    monkeypatch.setattr("src.pipeline.analyze_emails", Mock(return_value=mocked_analyses))
    monkeypatch.setattr("src.pipeline.prioritize_emails", Mock(return_value=mocked_priorities))

    emails, exports, analyses, priorities = run_pipeline(
        folder_name="Inbox",
        hours=24,
        output_dir="email_bodies",
        provider="mock",
        analysis_limit=5,
    )

    assert emails == mocked_emails
    assert exports == mocked_exports
    assert analyses == mocked_analyses
    assert priorities == mocked_priorities
    pipeline.fetch_emails.assert_called_once_with(folder_name="Inbox", hours=24)
    pipeline.save_emails.assert_called_once_with(mocked_emails, output_dir="email_bodies")
    pipeline.analyze_emails.assert_called_once()
    analyzer_exports, analyzer_config = pipeline.analyze_emails.call_args.args
    assert analyzer_exports == mocked_exports
    assert analyzer_config.provider == "mock"
    assert analyzer_config.max_emails == 5
    pipeline.prioritize_emails.assert_called_once_with(mocked_analyses)
