from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from lifeops.db import connect
from lifeops.intervention_self_check import run_self_check


class Stage2InterventionLoopSelfCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.old_root = os.environ.get("LIFEOPS_REPO_ROOT")
        self.tmp = Path(tempfile.mkdtemp(prefix="lifeops-loop-"))
        os.environ["LIFEOPS_REPO_ROOT"] = str(self.tmp)
        prompts = self.tmp / "prompts"
        prompts.mkdir(parents=True, exist_ok=True)
        (prompts / "intervention_prompt.md").write_text(
            "event `{event_id}`\nblock `{current_block}`\nactivity `{detected_activity}`\nreason `{reason}`\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        if self.old_root is None:
            os.environ.pop("LIFEOPS_REPO_ROOT", None)
        else:
            os.environ["LIFEOPS_REPO_ROOT"] = self.old_root
        shutil.rmtree(self.tmp)

    def test_self_check_creates_prompt_and_records_decision(self) -> None:
        result = run_self_check(choice="return_now")
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["decision"], "return_now")
        self.assertEqual(result["final_event_status"], "decided")
        self.assertTrue(Path(str(result["prompt_path"])).exists())
        with connect() as conn:
            decisions = conn.execute("SELECT COUNT(*) AS count FROM intervention_decisions").fetchone()
            exceptions = conn.execute("SELECT COUNT(*) AS count FROM exceptions").fetchone()
        self.assertEqual(decisions["count"], 1)
        self.assertEqual(exceptions["count"], 0)

    def test_self_check_can_exercise_exception_path(self) -> None:
        result = run_self_check(choice="intentional_rest", duration_minutes=1)
        self.assertEqual(result["decision"], "intentional_rest")
        self.assertIsNotNone(result["exception_id"])
        with connect() as conn:
            exception = conn.execute("SELECT category FROM exceptions WHERE id = ?", (result["exception_id"],)).fetchone()
        self.assertEqual(exception["category"], "intentional_rest")


if __name__ == "__main__":
    unittest.main()
