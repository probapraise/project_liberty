from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScheduleBlock:
    id: int
    date: str
    start_time: str
    end_time: str
    type: str
    title: str
    enforcement_level: str
    source: str
    status: str


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    priority: str
    estimated_minutes: int | None
    energy_level: str | None
    due_date: str | None
    status: str
