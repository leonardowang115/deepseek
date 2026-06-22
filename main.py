import datetime
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

try:
    import win32com.client
except ImportError:
    win32com = None


def get_outlook_emails_last_24h(folder_name="Inbox"):
    """获取本地 Outlook 中指定文件夹最近 24 小时的邮件。"""
    if win32com is None:
        raise ImportError(
            "需要安装 pywin32: pip install pywin32"
        )

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 = Inbox

    if folder_name != "Inbox":
        # 支持按名称查找子文件夹
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
    since = now - datetime.timedelta(hours=24)
    restriction = "[ReceivedTime] >= '{0}'".format(
        since.strftime("%m/%d/%Y %H:%M")
    )

    messages = folder.Items
    messages.Sort("ReceivedTime", True)
    recent_messages = messages.Restrict(restriction)

    result = []
    for message in recent_messages:
        try:
            body = getattr(message, "Body", "") or ""
            result.append({
                "subject": message.Subject,
                "sender": getattr(message, "SenderName", None),
                "received_time": message.ReceivedTime,
                "body": body,
                "entry_id": getattr(message, "EntryID", None),
            })
        except Exception:
            continue

    return result


def safe_filename(text):
    text = text or "email"
    text = re.sub(r"[\\/:*?\"<>|]+", "_", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:120] or "email"


def save_email_bodies(emails, dest_folder="email_bodies"):
    os.makedirs(dest_folder, exist_ok=True)
    for idx, mail in enumerate(emails, start=1):
        subject = safe_filename(mail.get("subject"))
        received_time = mail.get("received_time")
        timestamp = received_time.strftime("%Y%m%d_%H%M%S") if received_time else f"{idx:04d}"
        filename = f"{timestamp}_{subject}.txt"
        filepath = os.path.join(dest_folder, filename)
        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(dest_folder, f"{timestamp}_{subject}_{counter}.txt")
            counter += 1

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Subject: {mail.get('subject', '')}\n")
            f.write(f"Sender: {mail.get('sender', '')}\n")
            f.write(f"ReceivedTime: {mail.get('received_time', '')}\n")
            f.write("\n")
            f.write(mail.get("body", ""))

    return dest_folder


if __name__ == "__main__":
    emails = get_outlook_emails_last_24h()
    print(f"最近 24 小时邮件数量: {len(emails)}")
    saved_folder = save_email_bodies(emails)
    print(f"已保存邮件正文到目录: {os.path.abspath(saved_folder)}")
    for mail in emails:
        print("---")
        print(f"主题: {mail['subject']}")
        print(f"发件人: {mail['sender']}")
        print(f"接收时间: {mail['received_time']}")
        print(f"正文预览: {mail['body'][:200]}")
