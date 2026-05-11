from __future__ import annotations

import argparse
import time
from datetime import datetime, timedelta, timezone

from .db import connect, init_db
from .paths import repo_root

DEFAULT_TZ = timezone(timedelta(hours=9), "Asia/Seoul")


def write_heartbeat(message: str) -> None:
    root = repo_root()
    log_path = root / "data" / "runtime" / "event_dispatcher.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(DEFAULT_TZ).isoformat(timespec="seconds")
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{timestamp} {message}\n")


def pending_count() -> int:
    with connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS count FROM intervention_events WHERE status = 'pending'"
        ).fetchone()
        return int(row["count"])


def run(interval_seconds: int, once: bool) -> None:
    init_db()
    count = pending_count()
    write_heartbeat(f"Stage 1 dispatcher placeholder started. pending_events={count}. Real Codex intervention dispatch starts in Stage 2.")
    if once:
        return
    while True:
        write_heartbeat(f"Stage 1 dispatcher heartbeat. pending_events={pending_count()}.")
        time.sleep(interval_seconds)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage 1 LifeOps event dispatcher placeholder")
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args(argv)
    run(args.interval, args.once)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

