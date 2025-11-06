"""Utility helpers for loading constrained YAML-like configuration files.

The Spec-Kit AnkerSPA integration needs human-readable configuration while
sticking to the Python standard library (the project forbids extra
dependencies).  To keep YAML authoring ergonomics without pulling in PyYAML,
this module implements a deliberately small parser that understands the subset
of YAML we emit in the PAT templates:

* Key/value mappings using the ``key: value`` syntax.
* Inline lists written as ``[item1, item2]``.
* Scalar values for strings, integers, floats, booleans, and ``null``.
* Nested mappings by indentation (two-space multiples recommended).

Anything beyond this surface area (multiline strings, anchors, tags, nested
lists expressed with ``-`` markers, etc.) is intentionally unsupported.  The
initializer only writes configurations within this constraint, so the runtime
parser remains small and dependency-free.

The goal is to provide robust error messages rather than full YAML
compatibility.  If the parser encounters constructs outside of its dialect, it
raises ``ValueError`` with a descriptive message so maintainers can adjust the
templates accordingly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class ParsedDocument:
    """Container for parsed YAML content and diagnostics."""

    data: Any


def _strip_quotes(value: str) -> str:
    if (value.startswith("'") and value.endswith("'")) or (
        value.startswith('"') and value.endswith('"')
    ):
        inner = value[1:-1]
        return inner.replace("\\'", "'").replace('\\"', '"')
    return value


def _parse_inline_list(value: str, *, line_no: int) -> list[Any]:
    inner = value[1:-1].strip()
    if not inner:
        return []

    items: list[str] = []
    buffer: list[str] = []
    quote: str | None = None
    escaped = False

    for char in inner:
        if quote:
            buffer.append(char)
            if escaped:
                escaped = False
                continue

            if char == "\\":
                escaped = True
                continue

            if char == quote:
                quote = None
        else:
            if char in {'"', "'"}:
                quote = char
                buffer.append(char)
            elif char == ',':
                items.append(''.join(buffer).strip())
                buffer = []
            else:
                buffer.append(char)

    if quote:
        raise ValueError(f"Unterminated quoted string in list at line {line_no}")

    if buffer:
        items.append(''.join(buffer).strip())

    return [
        _parse_scalar(item.strip(), line_no=line_no)
        for item in items
        if item.strip() or item == ""  # allow empty string items
    ]


def _parse_scalar(value: str, *, line_no: int) -> Any:
    raw = value.strip()
    if raw == "" or raw.lower() in {"null", "none", "~"}:
        return None
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    if raw.startswith("[") and raw.endswith("]"):
        return _parse_inline_list(raw, line_no=line_no)

    try:
        if raw.startswith("0") and len(raw) > 1 and raw[1].isdigit():
            raise ValueError  # avoid octal interpretation
        return int(raw)
    except ValueError:
        pass

    try:
        return float(raw)
    except ValueError:
        pass

    return _strip_quotes(raw)


def _ensure_container(container: Any, line_no: int) -> dict[str, Any]:
    if not isinstance(container, dict):
        raise ValueError(
            f"Configuration structure violation near line {line_no}: expected a mapping"
        )
    return container


def load_simple_yaml(source: Path | str | Iterable[str]) -> Any:
    """Parse a constrained YAML subset and return native Python objects.

    Args:
        source: ``Path`` to a YAML file, raw string content, or an iterable of
            lines.

    Returns:
        Parsed Python data structures (dict, list, scalars).

    Raises:
        ValueError: When encountering constructs outside the supported subset or
            malformed content.
    """

    if isinstance(source, Path):
        lines = source.read_text(encoding="utf-8").splitlines()
    elif isinstance(source, str):
        lines = source.splitlines()
    else:
        lines = list(source)

    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for idx, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))

        while stack and indent <= stack[-1][0] and len(stack) > 1:
            stack.pop()

        current_container = stack[-1][1]

        if stripped.startswith("- "):
            if not isinstance(current_container, list):
                raise ValueError(
                    f"List item found outside list context at line {idx}: {stripped}"
                )
            current_container.append(_parse_scalar(stripped[2:], line_no=idx))
            continue

        if ":" not in stripped:
            raise ValueError(
                f"Invalid line {idx}: '{stripped}'. Expected key: value pattern."
            )

        key, value_part = stripped.split(":", 1)
        key = key.strip()
        value_part = value_part.strip()

        parent = _ensure_container(current_container, line_no=idx)

        if value_part == "":
            new_dict: dict[str, Any] = {}
            parent[key] = new_dict
            stack.append((indent, new_dict))
            continue

        parsed_value = _parse_scalar(value_part, line_no=idx)
        parent[key] = parsed_value

        if isinstance(parsed_value, (dict, list)):
            stack.append((indent, parsed_value))

    return root


__all__ = ["ParsedDocument", "load_simple_yaml"]


