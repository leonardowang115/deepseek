from __future__ import annotations

import datetime
import re
from typing import List

try:
    import win32com.client
except ImportError:  # pragma: no cover
    win32com = None

from .models import Email


def fetch_emails(folder_name: str = "Inbox", hours: int = 24) -> List[Email]:
    """从本地 Outlook 中获取最近 hours 小时内的邮件。"""
    if win32com is None:
        raise ImportError("需要安装 pywin32: pip install pywin32")

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox

    if folder_name != "Inbox":
        folder = None
        for sub_folder in inbox.Folders:
            if sub_folder.Name == folder_name:
                folder = sub_folder
                break
        if folder is None:
            raise ValueError(f"未找到 Outlook 文件夹: {folder_name}")
    else:
        folder = inbox

    now = datetime.datetime.now()
    since = now - datetime.timedelta(hours=hours)
    restriction = "[ReceivedTime] >= '{0}'".format(
        since.strftime("%m/%d/%Y %H:%M")
    )

    messages = folder.Items
    messages.Sort("ReceivedTime", True)
    recent_messages = messages.Restrict(restriction)

    results: List[Email] = []
    for message in recent_messages:
        try:
            body = getattr(message, "Body", "") or ""
            results.append(
                Email(
                    subject=message.Subject or "",
                    sender=getattr(message, "SenderName", "") or "",
                    received_time=getattr(message, "ReceivedTime", None),
                    body=body,
                    entry_id=getattr(message, "EntryID", "") or "",
                    folder=folder_name,
                )
            )
        except Exception:
            continue

    return results
