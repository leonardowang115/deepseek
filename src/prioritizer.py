from __future__ import annotations

from typing import List

from .models import EmailAnalysis, PriorityResult


def prioritize_emails(analyses: List[EmailAnalysis]) -> List[PriorityResult]:
    """将分析结果映射为最终优先级和推荐理由。"""
    sorted_analyses = sorted(analyses, key=lambda item: item.priority_score, reverse=True)
    results: List[PriorityResult] = []

    for analysis in sorted_analyses:
        if analysis.priority_score >= 0.9:
            priority = "高"
            reason = "包含紧急词汇或正文较长，需要尽快处理。"
        elif analysis.priority_score >= 0.7:
            priority = "中"
            reason = "正文较长，可能需要回应或后续跟进。"
        else:
            priority = "低"
            reason = "正文较短，可稍后处理。"

        results.append(PriorityResult(analysis=analysis, priority=priority, reason=reason))

    return results
