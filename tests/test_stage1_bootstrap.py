from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from lifeops.boot import build_boot_context, render_boot_context_markdown
from lifeops.db import connect, init_db, table_names


class Stage1BootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.old_root = os.environ.get("LIFEOPS_REPO_ROOT")
        self.tmp = Path(tempfile.mkdtemp(prefix="lifeops-stage1-"))
        os.environ["LIFEOPS_REPO_ROOT"] = str(self.tmp)
        weekly = self.tmp / "data" / "weekly"
        weekly.mkdir(parents=True, exist_ok=True)
        (weekly / "current_input.md").write_text(
            "\n".join(
                [
                    "# 이번 주 입력",
                    "- 이번 주 근무:",
                    "- 특수 일정:",
                    "- 우선순위:",
                    "- 피로 예상:",
                    "- 완전 휴식일 후보:",
                    "- 이번 주 차단 강화 시간대:",
                ]
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        if self.old_root is None:
            os.environ.pop("LIFEOPS_REPO_ROOT", None)
        else:
            os.environ["LIFEOPS_REPO_ROOT"] = self.old_root
        shutil.rmtree(self.tmp)

    def test_init_db_creates_required_tables(self) -> None:
        db_file = init_db()
        with connect(db_file) as conn:
            tables = set(table_names(conn))
        expected = {
            "schedule_blocks",
            "tasks",
            "activity_events",
            "intervention_events",
            "intervention_decisions",
            "exceptions",
            "recovery_sessions",
            "pattern_findings",
            "rule_proposals",
        }
        self.assertTrue(expected.issubset(tables))

    def test_boot_context_renders_expected_sections(self) -> None:
        context = build_boot_context()
        text = render_boot_context_markdown(context)
        self.assertIn("오늘의 고정 일정", text)
        self.assertIn("현재 계획 블록", text)
        self.assertIn("다음 3개 행동", text)
        self.assertIn("알려진 고위험 시간대", text)
        self.assertIn("확인 필요", text)

    def test_event_logs_are_created(self) -> None:
        init_db()
        for name in ["activity.jsonl", "interventions.jsonl", "exceptions.jsonl"]:
            self.assertTrue((self.tmp / "data" / "events" / name).exists())


class RepositorySafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = Path(__file__).resolve().parents[1]

    def test_startup_scripts_exist(self) -> None:
        for rel in [
            "scripts/Start-LifeOps.ps1",
            "scripts/Open-CodexOperator.ps1",
            "scripts/Install-StartupTask.ps1",
            "scripts/Remove-StartupTask.ps1",
        ]:
            self.assertTrue((self.repo / rel).exists(), rel)

    def test_code_does_not_call_openai_api_directly(self) -> None:
        forbidden = ["import openai", "from openai", "api.openai.com"]
        for path in list((self.repo / "src").rglob("*.py")) + list((self.repo / "scripts").rglob("*.ps1")):
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for token in forbidden:
                self.assertNotIn(token, lowered, str(path))

    def test_code_does_not_collect_keystrokes_or_screenshots(self) -> None:
        forbidden = [
            "getasynckeystate",
            "setwindowshookex",
            "printwindow",
            "imagegrab",
            "screenshot",
        ]
        for path in (self.repo / "src").rglob("*.py"):
            lowered = path.read_text(encoding="utf-8").lower()
            for token in forbidden:
                self.assertNotIn(token, lowered, str(path))


if __name__ == "__main__":
    unittest.main()
