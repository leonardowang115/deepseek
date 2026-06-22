import argparse
import datetime
import json
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


def get_outlook_emails_last_24h(folder_name="Inbox", hours=24):
    """获取本地 Outlook 中指定文件夹过去 `hours` 小时的邮件。"""
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
    since = now - datetime.timedelta(hours=hours)
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


def save_email_bodies(emails, dest_folder="email_bodies", folder_name="Inbox"):
    root_folder = os.path.join(dest_folder, safe_filename(folder_name))
    os.makedirs(root_folder, exist_ok=True)
    saved_folders = []

    for idx, mail in enumerate(emails, start=1):
        subject = safe_filename(mail.get("subject"))
        sender = safe_filename(mail.get("sender"))
        received_time = mail.get("received_time")
        date_folder = (
            received_time.strftime("%Y-%m-%d") if received_time else "unknown_date"
        )
        timestamp = (
            received_time.strftime("%Y%m%d_%H%M%S") if received_time else f"{idx:04d}"
        )

        email_folder_name = f"{timestamp}_{sender}_{subject}"
        email_folder_name = email_folder_name[:120] or f"email_{idx:04d}"
        email_folder = os.path.join(root_folder, date_folder, email_folder_name)
        os.makedirs(email_folder, exist_ok=True)

        body_path = os.path.join(email_folder, "body.txt")
        metadata_path = os.path.join(email_folder, "metadata.json")

        with open(body_path, "w", encoding="utf-8") as f:
            f.write(mail.get("body", ""))

        metadata = {
            "subject": mail.get("subject", ""),
            "sender": mail.get("sender", ""),
            "received_time": str(mail.get("received_time", "")),
            "entry_id": mail.get("entry_id", ""),
            "folder": folder_name,
        }
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        saved_folders.append(email_folder)

    return root_folder, saved_folders


def parse_args():
    parser = argparse.ArgumentParser(
        description="从本地 Outlook 读取最近邮件并保存正文。"
    )
    parser.add_argument(
        "--folder",
        default="Inbox",
        help="Outlook 文件夹名称，默认 Inbox",
    )
    parser.add_argument(
        "--output-dir",
        default="email_bodies",
        help="保存邮件正文的目录，默认 email_bodies",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="检索过去的小时范围，默认 24",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    emails = get_outlook_emails_last_24h(folder_name=args.folder, hours=args.hours)
    print(f"最近 {args.hours} 小时邮件数量: {len(emails)}")
    saved_folder, saved_folders = save_email_bodies(
        emails, dest_folder=args.output_dir, folder_name=args.folder
    )
    print(f"已保存邮件正文到目录: {os.path.abspath(saved_folder)}")
    print(f"邮件总数: {len(saved_folders)}，按日期和邮件文件夹组织")
    print("前 5 个邮件目录：")
    for folder in saved_folders[:5]:
        print(f"- {folder}")
