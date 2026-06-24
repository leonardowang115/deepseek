from __future__ import annotations

import json
import os
import re
from typing import List

from .models import Email, EmailExport


def safe_filename(text: str) -> str:
    text = text or "email"
    text = re.sub(r"[\\/:*?\"<>|]+", "_", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:120] or "email"


def save_emails(emails: List[Email], output_dir: str = "email_bodies") -> List[EmailExport]:
    root_folder = os.path.join(output_dir, safe_filename(emails[0].folder if emails else "Inbox"))
    os.makedirs(root_folder, exist_ok=True)
    exports: List[EmailExport] = []

    for idx, email in enumerate(emails, start=1):
        date_folder = (
            email.received_time.strftime("%Y-%m-%d") if email.received_time else "unknown_date"
        )
        timestamp = (
            email.received_time.strftime("%Y%m%d_%H%M%S") if email.received_time else f"{idx:04d}"
        )
        folder_name = f"{timestamp}_{safe_filename(email.sender)}_{safe_filename(email.subject)}"
        folder_name = folder_name[:120] or f"email_{idx:04d}"
        email_folder = os.path.join(root_folder, date_folder, folder_name)
        os.makedirs(email_folder, exist_ok=True)

        body_path = os.path.join(email_folder, "body.txt")
        metadata_path = os.path.join(email_folder, "metadata.json")

        with open(body_path, "w", encoding="utf-8") as f:
            f.write(email.body)

        metadata = {
            "subject": email.subject,
            "sender": email.sender,
            "received_time": str(email.received_time),
            "entry_id": email.entry_id,
            "folder": email.folder,
        }
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        exports.append(EmailExport(email=email, export_path=email_folder))

    return exports
