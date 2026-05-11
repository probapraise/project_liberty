from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .boot import write_boot_context, write_boot_prompt
from .db import connect, init_db, table_names, utc_now
from .schedule_engine import format_block, get_current_block, get_fixed_obligations

DEFAULT_TZ = timezone(timedelta(hours=9), "Asia/Seoul")


def _print_lines(lines: list[str]) -> None:
    for line in lines:
        print(line)


def cmd_init_db(args: argparse.Namespace) -> int:
    db_file = init_db()
    with connect(db_file) as conn:
        tables = table_names(conn)
    print(f"DB initialized: {db_file}")
    print("Tables: " + ", ".join(tables))
    return 0


def cmd_export_boot_context(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else None
    path = write_boot_context(output)
    if args.print_text:
        print(path.read_text(encoding="utf-8"))
    else:
        print(f"Boot briefing context written: {path}")
    return 0


def cmd_write_boot_prompt(args: argparse.Namespace) -> int:
    output = Path(args.output) if args.output else None
    path = write_boot_prompt(output)
    if args.print_text:
        print(path.read_text(encoding="utf-8"))
    else:
        print(f"Boot prompt written: {path}")
    return 0


def cmd_get_today_plan(args: argparse.Namespace) -> int:
    init_db()
    now = datetime.now(DEFAULT_TZ)
    with connect() as conn:
        rows = get_fixed_obligations(conn, now.date().isoformat())
    if not rows:
        print("오늘 등록된 고정 일정이 없습니다.")
        return 0
    _print_lines([format_block(row) for row in rows])
    return 0


def cmd_get_current_block(args: argparse.Namespace) -> int:
    init_db()
    now = datetime.now(DEFAULT_TZ)
    with connect() as conn:
        row = get_current_block(conn, now)
    print(format_block(row))
    return 0


def cmd_get_pending_events(args: argparse.Namespace) -> int:
    init_db()
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT * FROM intervention_events
            WHERE status = 'pending'
            ORDER BY timestamp, id
            LIMIT ?
            """,
            (args.limit,),
        ).fetchall()
    print(json.dumps([dict(row) for row in rows], ensure_ascii=False, indent=2))
    return 0


def cmd_record_decision(args: argparse.Namespace) -> int:
    init_db()
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO intervention_decisions(
                event_id, timestamp, decision, category, duration_minutes,
                user_text_summary, followup_action
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                args.event_id,
                utc_now(),
                args.decision,
                args.category,
                args.duration_minutes,
                args.reason,
                args.followup_action,
            ),
        )
        conn.execute(
            "UPDATE intervention_events SET status = 'decided' WHERE id = ?",
            (args.event_id,),
        )
        conn.commit()
    print(f"Decision recorded for event #{args.event_id}: {args.decision}")
    return 0


def cmd_enter_recovery_mode(args: argparse.Namespace) -> int:
    init_db()
    now = datetime.now(DEFAULT_TZ)
    minimized = {
        "label": "남은 하루 최소안",
        "preserve": ["수면", "식사", "복약", "위생", "고정 일정"],
        "next_action": "물 한 잔 마시고 3분 동안 다음 필수 행동 하나만 정하기",
        "note": "밀린 일은 자동 재배치 대상입니다. 보충 벌칙은 없습니다.",
    }
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO recovery_sessions(start_time, end_time, reason, minimized_plan_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                now.isoformat(timespec="seconds"),
                (now + timedelta(hours=4)).isoformat(timespec="seconds"),
                args.reason,
                json.dumps(minimized, ensure_ascii=False),
            ),
        )
        conn.commit()
    print("오늘 계획을 현재 상태에 맞게 줄입니다.")
    print("다음 행동은 3분짜리입니다.")
    print(minimized["next_action"])
    return 0


def cmd_write_daily_summary(args: argparse.Namespace) -> int:
    init_db()
    now = datetime.now(DEFAULT_TZ)
    output = Path(args.output) if args.output else Path("data/daily") / f"{now.date().isoformat()}.md"
    with connect() as conn:
        intervention_count = conn.execute(
            "SELECT COUNT(*) AS count FROM intervention_events WHERE timestamp LIKE ?",
            (f"{now.date().isoformat()}%",),
        ).fetchone()["count"]
        false_positive_count = conn.execute(
            """
            SELECT COUNT(*) AS count FROM intervention_decisions
            WHERE timestamp LIKE ? AND category = 'false_positive'
            """,
            (f"{now.date().isoformat()}%",),
        ).fetchone()["count"]
    text = "\n".join(
        [
            f"# Daily Summary {now.date().isoformat()}",
            "",
            f"- total_interventions: {intervention_count}",
            f"- false_positives: {false_positive_count}",
            "- recovery_mode_usage: 확인 필요",
            "- sleep_boundary_incidents: 확인 필요",
            "",
            "점수 없음. 처벌 없음. 시스템 조정 참고용 요약입니다.",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"Daily summary written: {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lifeops", description="LifeOps Codex Operator local CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init-db")
    init.set_defaults(func=cmd_init_db)

    boot_context = sub.add_parser("export-boot-briefing-context")
    boot_context.add_argument("--output")
    boot_context.add_argument("--print", dest="print_text", action="store_true")
    boot_context.set_defaults(func=cmd_export_boot_context)

    boot_prompt = sub.add_parser("write-boot-prompt")
    boot_prompt.add_argument("--output")
    boot_prompt.add_argument("--print", dest="print_text", action="store_true")
    boot_prompt.set_defaults(func=cmd_write_boot_prompt)

    today = sub.add_parser("get-today-plan")
    today.set_defaults(func=cmd_get_today_plan)

    current = sub.add_parser("get-current-block")
    current.set_defaults(func=cmd_get_current_block)

    pending = sub.add_parser("get-pending-events")
    pending.add_argument("--limit", type=int, default=20)
    pending.set_defaults(func=cmd_get_pending_events)

    decision = sub.add_parser("record-decision")
    decision.add_argument("--event-id", type=int, required=True)
    decision.add_argument("--decision", required=True)
    decision.add_argument("--category")
    decision.add_argument("--reason", default="")
    decision.add_argument("--duration-minutes", type=int)
    decision.add_argument("--followup-action", default="")
    decision.set_defaults(func=cmd_record_decision)

    recovery = sub.add_parser("enter-recovery-mode")
    recovery.add_argument("--reason", required=True)
    recovery.set_defaults(func=cmd_enter_recovery_mode)

    daily = sub.add_parser("write-daily-summary")
    daily.add_argument("--output")
    daily.set_defaults(func=cmd_write_daily_summary)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())


