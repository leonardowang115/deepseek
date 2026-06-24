import os
import tempfile

from src.models import Email
from src.storage import save_emails


def test_save_emails_creates_files():
    emails = [
        Email(
            subject="测试邮件",
            sender="测试发件人",
            received_time=None,
            body="这是一封测试邮件。",
            entry_id="id123",
            folder="Inbox",
        )
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        exports = save_emails(emails, output_dir=tmpdir)
        assert len(exports) == 1
        assert os.path.isdir(exports[0].export_path)
        assert os.path.isfile(os.path.join(exports[0].export_path, "body.txt"))
        assert os.path.isfile(os.path.join(exports[0].export_path, "metadata.json"))
