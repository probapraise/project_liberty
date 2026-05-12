from __future__ import annotations

import argparse
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .db import init_db
from .paths import repo_root

DEFAULT_TZ = timezone(timedelta(hours=9), "Asia/Seoul")


def write_heartbeat(message: str) -> None:
    root = repo_root()
    log_path = root / "data" / "runtime" / "activity_watcher.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(DEFAULT_TZ).isoformat(timespec="seconds")
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{timestamp} {message}\n")


def run(interval_seconds: int, once: bool) -> None:
    init_db()
    write_heartbeat("Stage 1 watcher placeholder started. Stage 2 scope is Chrome/Steam only; no window contents, keystrokes, screenshots, or page bodies are collected.")
    if once:
        return
    while True:
        write_heartbeat("Stage 1 watcher heartbeat. Real Chrome/Steam-only activity polling starts in Stage 2.")
        time.sleep(interval_seconds)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage 1 LifeOps watcher placeholder")
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args(argv)
    run(args.interval, args.once)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
