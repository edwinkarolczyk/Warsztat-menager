# version: 1.0
"""Scan repository for path usages that ignore the <root> data directory."""

from __future__ import annotations

import ast
import os
import pathlib
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Iterator, Sequence


REPO_ROOT = pathlib.Path(os.getcwd()).resolve()
REPORT_PATH = REPO_ROOT / "missing_root_report.txt"

EXCLUDED_DIR_PARTS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
}

SUSPECT_PREFIXES = (
    "data/",
    "data\\",
    "./data/",
    "../data/",
)

SUSPECT_SEGMENTS = {
    "magazyn",
    "narzedzia",
    "produkty",
    "polprodukty",
    "maszyny",
    "zlecenia",
    "profiles",
    "zadania_narzedzia",
    "zamowienia",
}


def iter_python_files(root: pathlib.Path) -> Iterator[pathlib.Path]:
    for path in root.rglob("*.py"):
        if any(part in EXCLUDED_DIR_PARTS for part in path.parts):
            continue
        yield path


def normalize_str(value: str) -> str:
    return value.replace("\\", "/").strip()


def _prefix_match(value: str, prefixes: Sequence[str]) -> bool:
    lower = value.lower()
    return any(lower.startswith(prefix) for prefix in prefixes)


def looks_like_repo_data(value: str) -> bool:
    normalized = normalize_str(value)
    if not normalized:
        return False
    if "<root>" in normalized.lower():
        return False
    lower = normalized.lower()
    if lower in {"data", "./data", "../data"}:
        return True
    if _prefix_match(lower, SUSPECT_PREFIXES):
        return True
    if "/" in normalized or "\\" in normalized:
        parts = normalized.replace("\\", "/").split("/")
        return bool(parts and parts[0] in ({"data"} | SUSPECT_SEGMENTS))
    return False


def dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        left = dotted_name(node.value)
        if left:
            return f"{left}.{node.attr}"
        return node.attr
    return ""


@dataclass
class Finding:
    path: pathlib.Path
    line: int
    reason: str
    source: str


class RootUsageAnalyzer(ast.NodeVisitor):
    def __init__(self, file_path: pathlib.Path, source: str) -> None:
        self.file_path = file_path
        self.source_lines = source.splitlines()
        self.findings: list[Finding] = []
        self._skip_constants: set[int] = set()
        self._node_stack: list[ast.AST] = []

    def visit(self, node: ast.AST) -> None:  # type: ignore[override]
        self._node_stack.append(node)
        super().visit(node)
        self._node_stack.pop()

    # --- helpers -----------------------------------------------------

    def _line_source(self, node: ast.AST) -> str:
        try:
            return self.source_lines[node.lineno - 1].strip()
        except Exception:
            return ""

    def _add_finding(
        self, node: ast.AST, reason: str, detail: str | None = None
    ) -> None:
        snippet = detail if detail is not None else self._line_source(node)
        self.findings.append(
            Finding(
                path=self.file_path,
                line=getattr(node, "lineno", 0),
                reason=reason,
                source=snippet,
            )
        )

    def _mark_constant(self, node: ast.AST) -> None:
        self._skip_constants.add(id(node))

    def _is_docstring(self, node: ast.Constant) -> bool:
        if not isinstance(node.value, str):
            return False
        if len(self._node_stack) < 2:
            return False
        parent = self._node_stack[-2]
        if not isinstance(parent, ast.Expr):
            return False
        if len(self._node_stack) < 3:
            return False
        grand = self._node_stack[-3]
        if not isinstance(
            grand,
            (
                ast.Module,
                ast.ClassDef,
                ast.AsyncFunctionDef,
                ast.FunctionDef,
            ),
        ):
            return False
        body: Sequence[ast.stmt] = getattr(grand, "body", ())
        return bool(body and body[0] is parent)

    def _classify_cfg_path(self, node: ast.Call) -> None:
        if not node.args:
            return
        arg = node.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            if looks_like_repo_data(arg.value):
                self._mark_constant(arg)
                self._add_finding(node, "cfg_path repo data")
        elif isinstance(arg, ast.Call):
            name = dotted_name(arg.func)
            if name.endswith("os.path.join") and arg.args:
                first = arg.args[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    if looks_like_repo_data(first.value):
                        self._mark_constant(first)
                        self._add_finding(node, "cfg_path os.path.join('data', …)")

    def _classify_os_join(self, node: ast.Call) -> None:
        if not node.args:
            return
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            if looks_like_repo_data(first.value):
                self._mark_constant(first)
                self._add_finding(node, "os.path.join repo data")

    def _classify_path_call(self, node: ast.Call) -> None:
        args = list(node.args)
        if not args:
            return
        for arg in args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                if looks_like_repo_data(arg.value) or arg.value.lower() in SUSPECT_SEGMENTS:
                    self._mark_constant(arg)
                    self._add_finding(node, "pathlib.Path repo data")
                    break

    def _classify_path_div(self, node: ast.BinOp) -> None:
        def _suspicious(operand: ast.AST) -> bool:
            if isinstance(operand, ast.Constant) and isinstance(operand.value, str):
                if operand.value.lower() in {"data", "./data", "../data"}:
                    self._mark_constant(operand)
                    return True
            return False

        if isinstance(node.op, ast.Div) and (_suspicious(node.left) or _suspicious(node.right)):
            self._add_finding(node, "pathlib division with 'data'")

    # --- visitors ----------------------------------------------------

    def visit_Call(self, node: ast.Call) -> None:  # noqa: D401 - inherited docs
        name = dotted_name(node.func)
        if name.endswith("cfg_path"):
            self._classify_cfg_path(node)
        elif name.endswith("os.path.join"):
            self._classify_os_join(node)
        elif name.split(".")[-1] == "Path":
            self._classify_path_call(node)
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:  # noqa: D401 - inherited docs
        self._classify_path_div(node)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:  # noqa: D401 - inherited docs
        if id(node) in self._skip_constants:
            return
        if isinstance(node.value, str) and not self._is_docstring(node):
            value = node.value
            if looks_like_repo_data(value):
                normalized = normalize_str(value)
                if normalized.lower() == "data":
                    return
                if "/" not in normalized and "\\" not in normalized:
                    return
                self._add_finding(node, "string literal repo data", value)
        # no call to generic_visit because Constant has no children

    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:  # noqa: D401 - inherited docs
        literal_parts = "".join(
            part.value
            for part in node.values
            if isinstance(part, ast.Constant) and isinstance(part.value, str)
        )
        if literal_parts and looks_like_repo_data(literal_parts):
            normalized = normalize_str(literal_parts)
            if normalized.lower() != "data" and ("/" in normalized or "\\" in normalized):
                self._add_finding(node, "f-string repo data", literal_parts)
        self.generic_visit(node)


def analyze_file(path: pathlib.Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    analyzer = RootUsageAnalyzer(path, text)
    analyzer.visit(tree)
    return analyzer.findings


def collect_findings(files: Iterable[pathlib.Path]) -> list[Finding]:
    findings: list[Finding] = []
    for file in files:
        findings.extend(analyze_file(file))
    return findings


def write_report(findings: list[Finding]) -> None:
    REPORT_PATH.write_text("", encoding="utf-8")
    with REPORT_PATH.open("w", encoding="utf-8") as handle:
        handle.write(
            f"=== MISSING <root> SCAN === {datetime.now():%Y-%m-%d %H:%M:%S}\n"
        )
        handle.write(f"Repository: {REPO_ROOT}\n")
        handle.write("Focus: references to repo-relative 'data/' paths (expected <root>)\n\n")

        handle.write("--- FINDINGS (file:line: reason: snippet) ---\n\n")
        if findings:
            for finding in sorted(findings, key=lambda f: (str(f.path).lower(), f.line, f.reason)):
                handle.write(
                    f"{finding.path}:{finding.line}: [{finding.reason}] {finding.source}\n"
                )
        else:
            handle.write("(none)\n")

        handle.write("\n--- SUMMARY BY REASON ---\n")
        if findings:
            by_reason: dict[str, int] = {}
            for finding in findings:
                by_reason[finding.reason] = by_reason.get(finding.reason, 0) + 1
            for reason, count in sorted(by_reason.items(), key=lambda item: (-item[1], item[0])):
                handle.write(f"{count:4d} × {reason}\n")
        else:
            handle.write("(empty)\n")

        handle.write("\n--- SUMMARY BY FILE ---\n")
        if findings:
            by_file: dict[str, int] = {}
            for finding in findings:
                key = str(finding.path)
                by_file[key] = by_file.get(key, 0) + 1
            for key, count in sorted(by_file.items(), key=lambda item: (-item[1], item[0])):
                handle.write(f"{count:4d} × {key}\n")
        else:
            handle.write("(empty)\n")


def main() -> int:
    print(f"[ROOT-SCAN] Working directory: {REPO_ROOT}")
    files = list(iter_python_files(REPO_ROOT))
    findings = collect_findings(files)
    write_report(findings)

    if findings:
        print(
            f"[ROOT-SCAN] ⚠️  Detected {len(findings)} repo-relative paths. Report: {REPORT_PATH}"
        )
        return 1
    print(f"[ROOT-SCAN] ✅  No repo-relative paths detected. Report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
