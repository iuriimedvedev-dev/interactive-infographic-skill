#!/usr/bin/env python3
"""Comprehensive test suite for lint.py and Nord Design System templates."""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
LINT_CLI = ROOT / "lint.py"
ASSETS = ROOT / "assets"
TEMPLATE_INFOGRAPHIC = ASSETS / "template-infographic.html"
TEMPLATE_JUDGE = ASSETS / "template-judge-report.html"
NORD_CSS = ASSETS / "nord-design-system.css"


class LintTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(LINT_CLI), *map(str, args)],
            capture_output=True,
            text=True,
        )

    def test_canonical_templates_pass_linter(self):
        """Canonical boilerplates must pass all 4 invariants and safety checks cleanly."""
        result = self.run_cli(TEMPLATE_INFOGRAPHIC, TEMPLATE_JUDGE)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("PASS: " + str(TEMPLATE_INFOGRAPHIC), result.stdout)
        self.assertIn("PASS: " + str(TEMPLATE_JUDGE), result.stdout)

    def test_invariant_1_rejects_unordered_lists(self):
        """Zero <ul> bullet lists invariant: any <ul> tag must be rejected."""
        valid_css = "<style>.compare-table { color: red; } .nord-mini-card { color: blue; }</style>"
        html_with_ul = f"<!doctype html><html><head>{valid_css}</head><body><ul><li>Point 1</li></ul></body></html>"

        test_file = self.path / "test_ul.html"
        test_file.write_text(html_with_ul, encoding="utf-8")

        result = self.run_cli(test_file)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unordered list (<ul>) detected", result.stderr.lower())

    def test_invariant_2_rejects_emojis(self):
        """Zero emojis invariant: emojis in text must be rejected."""
        valid_css = "<style>.compare-table { color: red; } .nord-mini-card { color: blue; }</style>"
        html_with_emoji = f"<!doctype html><html><head>{valid_css}</head><body><p>Launch rocket {chr(0x1F680)}</p></body></html>"

        test_file = self.path / "test_emoji.html"
        test_file.write_text(html_with_emoji, encoding="utf-8")

        result = self.run_cli(test_file)
        self.assertEqual(result.returncode, 1)
        self.assertIn("emoji detected", result.stderr.lower())

    def test_invariant_3_rejects_ascii_box_drawing_in_code_block(self):
        """Zero ASCII box-drawing invariant: box-drawing chars inside .code-block must be rejected."""
        valid_css = "<style>.compare-table { color: red; } .nord-mini-card { color: blue; }</style>"
        html_with_box = (
            f"<!doctype html><html><head>{valid_css}</head><body>"
            f"<pre class='code-block'>{chr(0x250C)}{chr(0x2500)}{chr(0x2510)}\n"
            f"{chr(0x2502)}  {chr(0x2502)}\n"
            f"{chr(0x2514)}{chr(0x2500)}{chr(0x2518)}</pre></body></html>"
        )

        test_file = self.path / "test_box.html"
        test_file.write_text(html_with_box, encoding="utf-8")

        result = self.run_cli(test_file)
        self.assertEqual(result.returncode, 1)
        self.assertIn("ascii box-drawing diagram in code-block", result.stderr.lower())

    def test_invariant_4_requires_compare_table_and_nord_mini_card_css(self):
        """Valid CSS invariant: .compare-table and .nord-mini-card styles must be present or linked."""
        no_css_file = self.path / "test_no_css.html"
        no_css_file.write_text("<!doctype html><html><head></head><body><p>Plain</p></body></html>", encoding="utf-8")
        res1 = self.run_cli(no_css_file)
        self.assertEqual(res1.returncode, 1)
        self.assertIn("missing compare-table css rules", res1.stderr.lower())
        self.assertIn("missing nord-mini-card css rules", res1.stderr.lower())

        only_table = self.path / "test_only_table.html"
        only_table.write_text("<!doctype html><html><head><style>.compare-table { border: 0; }</style></head><body></body></html>", encoding="utf-8")
        res2 = self.run_cli(only_table)
        self.assertEqual(res2.returncode, 1)
        self.assertIn("missing nord-mini-card css rules", res2.stderr.lower())

        both_present = self.path / "test_both.html"
        both_present.write_text(
            "<!doctype html><html><head><style>.compare-table { border: 0; } .nord-mini-card { border: 0; }</style></head><body></body></html>",
            encoding="utf-8"
        )
        res3 = self.run_cli(both_present)
        self.assertEqual(res3.returncode, 0, res3.stderr)

        linked_css = self.path / "test_linked.html"
        linked_css.write_text(
            '<!doctype html><html><head><link rel="stylesheet" href="./assets/nord-design-system.css"></head><body></body></html>',
            encoding="utf-8"
        )
        res4 = self.run_cli(linked_css)
        self.assertEqual(res4.returncode, 0, res4.stderr)

    def test_safety_heuristics_reject_secrets_and_private_hosts(self):
        """Security checks: secrets and private hosts must be flagged."""
        valid_css = "<style>.compare-table { color: red; } .nord-mini-card { color: blue; }</style>"

        secret_file = self.path / "test_secret.html"
        secret_file.write_text(f"<!doctype html><html><head>{valid_css}</head><body>api_key=abcdefghijk1234567890</body></html>", encoding="utf-8")
        res_sec = self.run_cli(secret_file)
        self.assertEqual(res_sec.returncode, 1)
        self.assertIn("secret", res_sec.stderr.lower())

        host_file = self.path / "test_host.html"
        host_file.write_text(f"<!doctype html><html><head>{valid_css}</head><body>server.corp.local</body></html>", encoding="utf-8")
        res_host = self.run_cli(host_file)
        self.assertEqual(res_host.returncode, 1)
        self.assertIn("internal hostname", res_host.stderr.lower())


class PracticalAuthoringAndChromeTests(unittest.TestCase):
    """End-to-end tests authoring sample reports and validating via headless Chrome."""

    @classmethod
    def setUpClass(cls):
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            shutil.which("google-chrome"),
            shutil.which("chromium"),
        ]
        cls.chrome_bin = next((p for p in chrome_paths if p and Path(p).exists()), None)
        if not cls.chrome_bin:
            raise unittest.SkipTest("Headless Chrome not found in environment")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)

    def run_chrome(self, html_path: Path) -> str:
        cmd = [
            self.chrome_bin,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--dump-dom",
            f"file://{html_path.resolve()}",
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.stdout

    def test_author_and_verify_bespoke_interactive_infographic(self):
        """Author a bespoke multi-section interactive report following SKILL.md and verify in Chrome."""
        # 1. Read base infographic template and customize for a bespoke Distributed Cache Atlas
        base = TEMPLATE_INFOGRAPHIC.read_text(encoding="utf-8")
        customized = base.replace("System atlas — interactive infographic", "Distributed Cache Atlas — Interactive Report")
        customized = customized.replace("Make the complex<br>feel simple.", "High-Throughput<br>Cache Architecture.")

        sample_file = self.path / "sample_cache_atlas.html"
        sample_file.write_text(customized, encoding="utf-8")

        # 2. Verify with lint.py
        lint_res = subprocess.run([sys.executable, str(LINT_CLI), str(sample_file)], capture_output=True, text=True)
        self.assertEqual(lint_res.returncode, 0, lint_res.stderr + lint_res.stdout)

        # 3. Add an automated Chrome verification test runner script into the page
        verification_script = """
        <script id="__e2e_verifier__">
          window.addEventListener('DOMContentLoaded', () => {
            const results = {
              ulCount: document.querySelectorAll('ul').length,
              tocLinksCount: document.querySelectorAll('#tocSidebar .toc-link').length,
              hasMetricGrid: !!document.querySelector('.metric-grid'),
              hasFlowPulse: !!document.querySelector('.flow-pulse'),
              hasCompareTable: !!document.querySelector('.compare-table'),
              hasMiniCards: document.querySelectorAll('.nord-mini-card').length,
            };

            // Test Theme toggle
            const themeBtn = document.getElementById('themeToggle');
            themeBtn.click();
            results.themeAfterToggle = document.documentElement.dataset.theme;

            // Test Lifecycle step click
            const stepBtn = document.querySelector('.lc-step[data-phase="Build"]');
            if (stepBtn) {
              stepBtn.click();
              results.activePhaseTitle = document.getElementById('phaseTitle').textContent;
              results.activePhaseNum = document.getElementById('phaseNumber').textContent;
            }

            // Test Modal open and close
            const openModalBtn = document.getElementById('openModal');
            const modalLayer = document.getElementById('infoModal');
            const closeModalBtn = document.getElementById('closeModal');
            openModalBtn.click();
            results.modalOpen = !modalLayer.hidden;
            closeModalBtn.click();
            results.modalClosedAfterClick = modalLayer.hidden;

            const out = document.createElement('div');
            out.id = '__e2e_results__';
            out.textContent = JSON.stringify(results);
            document.body.appendChild(out);
          });
        </script>
        """
        tested_html = customized.replace("</body>", f"{verification_script}</body>")
        sample_file.write_text(tested_html, encoding="utf-8")

        dom = self.run_chrome(sample_file)

        # 4. Check results from rendered DOM
        self.assertIn('id="__e2e_results__"', dom)
        match = re.search(r'<div id="__e2e_results__">(\{.*?\})</div>', dom)
        self.assertTrue(match, "Test results not found in dumped DOM")

        data = json.loads(match.group(1))
        self.assertEqual(data["ulCount"], 0, "Strict invariant violated: <ul> tags found!")
        self.assertGreaterEqual(data["tocLinksCount"], 6)
        self.assertTrue(data["hasMetricGrid"])
        self.assertTrue(data["hasFlowPulse"])
        self.assertTrue(data["hasCompareTable"])
        self.assertGreaterEqual(data["hasMiniCards"], 3)
        self.assertEqual(data["themeAfterToggle"], "light")
        self.assertEqual(data["activePhaseTitle"], "Build")
        self.assertEqual(data["activePhaseNum"], "06")
        self.assertTrue(data["modalOpen"])
        self.assertTrue(data["modalClosedAfterClick"])

    def test_author_and_verify_bespoke_agentic_judge_report(self):
        """Author a bespoke Agentic Judge report following SKILL.md and verify in Chrome."""
        base = TEMPLATE_JUDGE.read_text(encoding="utf-8")
        customized = base.replace(
            "Agentic Judge Evaluation Report",
            "Autonomous Coding Agent Evaluation Verdict"
        )

        sample_file = self.path / "sample_judge_verdict.html"
        sample_file.write_text(customized, encoding="utf-8")

        # 1. Verify with lint.py
        lint_res = subprocess.run([sys.executable, str(LINT_CLI), str(sample_file)], capture_output=True, text=True)
        self.assertEqual(lint_res.returncode, 0, lint_res.stderr + lint_res.stdout)

        # 2. Render in headless Chrome and verify DOM structure
        dom = self.run_chrome(sample_file)
        self.assertIn("Content-Security-Policy", dom)
        self.assertIn("Autonomous Coding Agent Evaluation Verdict", dom)
        self.assertIn("status-pill pill-good", dom)
        self.assertIn("compare-table", dom)
        self.assertIn("nord-mini-card", dom)
        self.assertNotRegex(dom, r"<\s*ul\b")


if __name__ == "__main__":
    unittest.main()
