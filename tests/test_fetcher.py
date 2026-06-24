from datetime import datetime

from src.models import Email


def test_import_fetcher():
    # 仅测试模块导入，不依赖 Outlook 环境
    assert Email(subject="", sender="", received_time=datetime.now(), body="", entry_id="", folder="Inbox")
