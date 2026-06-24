import argparse
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from src.pipeline import run_pipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="从本地 Outlook 读取最近邮件并保存正文，然后进行模型分析和优先级推荐。"
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
    parser.add_argument(
        "--provider",
        default="mock",
        help="分析器提供者，默认 mock（后续可扩展 OpenAI/Azure/Local）。",
    )
    parser.add_argument(
        "--analysis-limit",
        type=int,
        default=5,
        help="最多送入分析器的邮件数，默认 5；设置为 0 表示不限制。",
    )
    return parser.parse_args()


def print_summary(priorities):
    print(f"邮件总数: {len(priorities)}")
    print("按优先级排序的结果：")
    for idx, item in enumerate(priorities, start=1):
        print(f"{idx}. [{item.priority}] {item.analysis.email.subject} - {item.reason}")


if __name__ == "__main__":
    args = parse_args()
    emails, exports, analyses, priorities = run_pipeline(
        folder_name=args.folder,
        hours=args.hours,
        output_dir=args.output_dir,
        provider=args.provider,
        analysis_limit=args.analysis_limit or None,
    )
    print(f"最近 {args.hours} 小时邮件数量: {len(emails)}")
    print(f"已保存邮件正文到目录: {args.output_dir}")
    print_summary(priorities)
