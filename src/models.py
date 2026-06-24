from __future__ import annotations

import dataclasses
import datetime
from typing import Optional


@dataclasses.dataclass
class Email:
    subject: str
    sender: str
    received_time: Optional[datetime.datetime]
    body: str
    entry_id: str
    folder: str


@dataclasses.dataclass
class EmailExport:
    email: Email
    export_path: str


@dataclasses.dataclass
class AnalysisRequest:
    subject: str
    sender: str
    received_time: Optional[datetime.datetime]
    body: str
    entry_id: str
    folder: str
    export_path: str


@dataclasses.dataclass
class EmailAnalysis:
    email: Email
    summary: str
    category: str
    intent: str
    priority_score: float
    key_phrases: list[str]


@dataclasses.dataclass
class PriorityResult:
    analysis: EmailAnalysis
    priority: str
    reason: str
