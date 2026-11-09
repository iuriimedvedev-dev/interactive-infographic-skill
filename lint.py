#!/usr/bin/env python3
"""Linter for agent-authored interactive infographics and Agentic Judge HTML reports.

Checks HTML files for the 4 core design system invariants:
1. Zero <ul> bullet lists (bullet lists are forbidden; use colored .nord-mini-card or .toc-list).
2. Zero emojis (emojis are forbidden; use monochrome SVG icons or text).
3. Zero ASCII box-drawing in .code-block (use graphical .diagram-flow, .diagram-panels, or SVG).
4. Valid .compare-table and .nord-mini-card CSS classes present or linked.

Also checks heuristic safety invariants (secrets, private addresses, restricted names).
"""

import argparse
import hashlib
import html
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

# One-way SHA-256 fingerprints for detecting restricted internal names without leaking them.
RESTRICTED_FINGERPRINTS = frozenset({
    "9b2796ccfc66744190360d56e45c0e3f6bc79fa0b995296e1a523472b5e3709e",
    "2d807432caec5f3e571cc555c32fe0154cc1d0e64c9345dab04c20bf915c9a61",
    "6c2949a5b9698d223e285bc41038564e8626724885349976073ced55302fa3df",
    "c2d0d78cc9bdca1cf4936a2e177a7a29c4847018dcf3ec25f57cad27d4c2a0e2",
    "21f58e3dd651be0236e1cefbc898dcc6219e0b30ba0f539bb3fbbe51ecc53bb4",
    "c9ad94c6532dbca162161e0be7d9ae8b19fe717cf1fab6d59bdbeb8625a2efd4",
    "10a74cf5b6f16e8ae6f3f0394e03608170738b702ce4fa331fe906a969f2cfed",
    "073fdfdd9b05f82028dabd9e63cd6f61bb6563ec84143ed9f6f036d7af0a7cbc",
})
RESTRICTED_LENGTHS = (4, 5, 8, 9, 11, 12, 16)

EMOJI_PATTERN = re.compile("[\U0001f000-\U0001faff\u2600-\u27bf\ufe0f\u200d\u20e3]")
PRIVATE_HOST_PATTERN = re.compile(
    r"(?i)\b(?:[a-z0-9-]+\.)+(?:internal|corp|local|lan)\b|"
    r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
)
SECRET_PATTERN = re.compile(
    r"(?i)(?:api[_-]?key|access[_-]?token|password|secret|authorization)\s*[:=]\s*[\"']?"
    r"(?!none\b|null\b|false\b|true\b|placeholder\b|example\b)[A-Za-z0-9_./+\-=]{12,}|"
    r"\b(?:sk|ghp|github_pat)_[A-Za-z0-9_]{16,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
)


class HTMLStructureParser(HTMLParser):
    """Parses HTML to extract style blocks, code blocks, links, and tags."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.code_contents = []
        self.style_contents = []
        self.linked_stylesheets = []
        self.has_ul_tag = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get("class", "").split()
        in_code_block = bool(self.stack and self.stack[-1][1]) or ("code-block" in classes)

        if tag.lower() == "ul":
            self.has_ul_tag = True

        if tag.lower() == "link" and attr_dict.get("rel") == "stylesheet":
            href = attr_dict.get("href", "")
            if href:
                self.linked_stylesheets.append(href)

        void_tags = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
        if tag.lower() not in void_tags:
            self.stack.append((tag.lower(), in_code_block))

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag_lower:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.stack:
            if self.stack[-1][1]:
                self.code_contents.append(data)
            if any(t == "style" for t, _ in self.stack):
                self.style_contents.append(data)


def check_sensitive_content(text: str) -> list[str]:
    """Checks for emojis, private hostnames, exposed secrets, and restricted names."""
    findings = []
    unescaped = html.unescape(text)

    if EMOJI_PATTERN.search(unescaped):
        findings.append("emoji detected; emojis are forbidden, use monochrome SVG icons or text")

    if PRIVATE_HOST_PATTERN.search(unescaped):
        findings.append("internal hostname or private address detected")

    if SECRET_PATTERN.search(unescaped):
        findings.append("possible secret or access token detected")

    lowered = unescaped.lower()
    for match in re.finditer(r"[a-z0-9][a-z0-9.-]*", lowered):
        word = match.group()
        for length in RESTRICTED_LENGTHS:
            if len(word) >= length:
                for start in range(len(word) - length + 1):
                    sub = word[start:start + length]
                    if hashlib.sha256(sub.encode("utf-8")).hexdigest() in RESTRICTED_FINGERPRINTS:
                        findings.append("restricted internal name detected")
                        return findings
    return findings


def lint_html(html_content: str) -> list[str]:
    """Lints an HTML report against the 4 core invariants and safety checks."""
    findings = []

    # 1. Check for forbidden <ul> bullet lists
    if re.search(r"<\s*ul\b", html_content, re.IGNORECASE):
        findings.append(
            "unordered list (<ul>) detected; bullet lists are forbidden, "
            "use colored Nord mini-cards (.nord-mini-card) or <div class='toc-list'> instead"
        )

    # 2. Check for emojis and safety findings
    findings.extend(check_sensitive_content(html_content))

    parser = HTMLStructureParser()
    parser.feed(html_content)

    # 3. Check for ASCII box-drawing in .code-block
    code_text = "".join(parser.code_contents)
    if re.search(r"[\u2500-\u257f]", code_text):
        findings.append(
            "ASCII box-drawing diagram in code-block; "
            "use graphical .diagram-flow, .diagram-panels, or SVG instead"
        )

    # 4. Check for valid .compare-table and .nord-mini-card CSS rules
    combined_css = "\n".join(parser.style_contents)
    has_linked_nord_css = any("nord-design-system.css" in href for href in parser.linked_stylesheets)

    has_compare_table_css = bool(re.search(r"\.compare-table\b[^{}]*\{", combined_css)) or has_linked_nord_css
    has_mini_card_css = bool(re.search(r"\.nord-mini-card\b[^{}]*\{", combined_css)) or has_linked_nord_css

    if not has_compare_table_css:
        findings.append("missing compare-table CSS rules (embed .compare-table styles or link nord-design-system.css)")
    if not has_mini_card_css:
        findings.append("missing nord-mini-card CSS rules (embed .nord-mini-card styles or link nord-design-system.css)")

    # Deduplicate findings while preserving order
    return list(dict.fromkeys(findings))


def lint_file(path: Path) -> list[str]:
    """Reads and lints a single file."""
    try:
        content = path.read_text(encoding="utf-8")
        return lint_html(content)
    except Exception as exc:
        return [f"Failed to read {path}: {exc}"]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint HTML reports for the 4 Nord Design System invariants and safety heuristics."
    )
    parser.add_argument("files", nargs="+", type=Path, help="HTML file(s) to check")
    parser.add_argument("-q", "--quiet", action="store_true", help="Only output errors")

    args = parser.parse_args(argv)

    total_failures = 0
    for file_path in args.files:
        if not file_path.exists():
            print(f"Error: {file_path} does not exist", file=sys.stderr)
            total_failures += 1
            continue

        findings = lint_file(file_path)
        if findings:
            total_failures += 1
            print(f"FAIL: {file_path}", file=sys.stderr)
            for finding in findings:
                print(f"  - {finding}", file=sys.stderr)
        elif not args.quiet:
            print(f"PASS: {file_path} (all 4 invariants satisfied)")

    return 1 if total_failures > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
