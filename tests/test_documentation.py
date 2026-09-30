"""Execute the Python examples readers copy from the README and user documentation."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PYTHON_BLOCK = re.compile(r"^```python[ \t]*\n(.*?)^```[ \t]*$", re.MULTILINE | re.DOTALL)
EXPECTED_OUTPUT = re.compile(r"\s*```text[ \t]*\n(.*?)^```[ \t]*$", re.MULTILINE | re.DOTALL)
EXAMPLE_PAGES = [
    path
    for path in [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
    if PYTHON_BLOCK.search(path.read_text(encoding="utf-8"))
]


@pytest.mark.parametrize(
    "path", EXAMPLE_PAGES, ids=[path.relative_to(ROOT).as_posix() for path in EXAMPLE_PAGES]
)
def test_documented_python_examples(path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Run blocks in page order and check any immediately following text output."""
    markdown = path.read_text(encoding="utf-8")
    namespace: dict[str, object] = {"__name__": "__documentation__", "__file__": str(path)}

    for block in PYTHON_BLOCK.finditer(markdown):
        line_offset = markdown.count("\n", 0, block.start(1))
        # Preserve Markdown line numbers in tracebacks, including for continuation blocks.
        source = "\n" * line_offset + block.group(1)
        capsys.readouterr()
        exec(compile(source, str(path), "exec"), namespace)
        output = capsys.readouterr().out
        expected = EXPECTED_OUTPUT.match(markdown[block.end():])
        if expected is not None:
            assert output.rstrip() == expected.group(1).rstrip(), (
                f"Output differs from {path.relative_to(ROOT)}:{line_offset + 1}"
            )
