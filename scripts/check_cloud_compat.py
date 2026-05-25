#!/usr/bin/env python3
"""Static check for Cloud / Kubernetes compatibility.

This plugin must run unmodified on NetBox Enterprise and NetBox Cloud,
both of which run as immutable, horizontally-scalable Kubernetes pods.
This means a number of patterns that would work fine on a classic
single-VM NetBox install will silently misbehave in a multi-pod
environment:

* Anything that writes to the local filesystem outside django-storages
  (the file ends up on one pod, then disappears the next request).
* Django management commands (Enterprise/Cloud cannot run them on
  demand).
* In-process schedulers / background threads (the pod can be killed
  mid-flight; long-running work belongs in a JobRunner).
* Per-pod caches (locmem / filebased) — Redis is the cache backend on
  Enterprise/Cloud.

This script scans the source tree for those patterns and exits non-zero
on a hit. The full contract is documented in AGENTS.md under
"Cloud / Kubernetes compatibility (HARD CONTRACT)".

Run as: python scripts/check_cloud_compat.py

The check intentionally lives outside ruff because (a) it spans tokens
ruff doesn't model well (string contents like ``/tmp``) and (b) the
diagnostic message is much friendlier when we own the rendering.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Where to scan. Tests are excluded — they routinely use tempfile,
# threading, etc. for legitimate reasons.
ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "netbox_cisco_aci"
EXCLUDE_DIRS = {"tests", "migrations", "__pycache__"}

# Each rule is (regex, human-friendly explanation).
# Regexes are matched with re.MULTILINE on the file text; keep them
# tight enough that they don't false-positive on docstrings about *not*
# doing the thing. (The whole-word \b anchors and ``\.`` attribute
# patterns help.)
RULES: list[tuple[re.Pattern[str], str]] = [
    # --- local filesystem ---
    (
        # Catches `import tempfile`, `from tempfile import X`, and any
        # `tempfile.foo(...)` attribute access.
        re.compile(r"(?m)^\s*import\s+tempfile\b|^\s*from\s+tempfile\b|\btempfile\."),
        "tempfile is per-pod and not safe across requests. "
        "Use django-storages via default_storage.",
    ),
    (
        re.compile(r"\bos\.makedirs\("),
        "os.makedirs writes to the container's ephemeral filesystem. Use django-storages.",
    ),
    (
        re.compile(r"\bos\.mkdir\("),
        "os.mkdir writes to the container's ephemeral filesystem. Use django-storages.",
    ),
    (
        re.compile(r"\bshutil\.(copy|move|rmtree|copytree|copyfile)\b"),
        "shutil file ops touch local disk. Use django-storages.",
    ),
    (
        # Match Path(...).write_text/.write_bytes/.mkdir/.unlink/.touch/.rename
        # rather than the bare import; reading via importlib.resources is fine.
        re.compile(r"\.(write_text|write_bytes|mkdir|unlink|touch|rename)\s*\("),
        "pathlib write/mutation methods touch the container's ephemeral "
        "filesystem. Use django-storages via default_storage.",
    ),
    (
        # Literal `open(<arg>, '<w|a|x>...')` — catches the obvious writes
        # while ignoring read-only opens of in-package data files.
        re.compile(r"\bopen\s*\([^)]*['\"][wax][btr+]*['\"]"),
        "Writing through open() lands on the container's ephemeral disk. "
        "Route writes through default_storage (django-storages).",
    ),
    (
        re.compile(r"\b(FileField|ImageField|FilePathField)\("),
        "Django file fields need an explicit storage= routed through "
        "default_storage so Enterprise/Cloud sees them.",
    ),
    (
        re.compile(r"['\"](/tmp/|/var/|/opt/netbox|/home/)"),
        "Hard-coded host paths don't exist (or aren't writeable) inside "
        "the NetBox Enterprise/Cloud container.",
    ),
    (
        re.compile(r"\bMEDIA_ROOT\b|\bSTATIC_ROOT\b"),
        "MEDIA_ROOT / STATIC_ROOT are per-pod. Route file I/O through default_storage instead.",
    ),
    # --- processes / threads ---
    (
        re.compile(r"\bthreading\.Thread\("),
        "Background threads die with the pod and can leak DB connections. "
        "Use NetBox's JobRunner framework.",
    ),
    (
        re.compile(r"\bmultiprocessing\."),
        "multiprocessing inside a Kubernetes pod is almost always wrong. "
        "Use NetBox's JobRunner framework.",
    ),
    (
        re.compile(r"\bsubprocess\."),
        "subprocess assumes shell tooling exists in the container image. "
        "Reimplement in pure Python or move to a JobRunner that the "
        "platform has packaged for you.",
    ),
    (
        re.compile(r"\bsocket\.(bind|listen)\("),
        "Direct socket binding clashes with the Kubernetes ingress layer.",
    ),
    # --- schedulers / cron-in-process ---
    (
        re.compile(r"\b(apscheduler|schedule\.every|sched\.scheduler)\b", re.I),
        "In-process schedulers double-fire under horizontal scaling. "
        "Use NetBox jobs + the Enterprise scheduler.",
    ),
    # --- caches ---
    (
        re.compile(r"backends\.(locmem|filebased)"),
        "locmem/filebased caches don't share across pods. "
        "Rely on the platform-provided Redis cache.",
    ),
    # --- logging ---
    (
        re.compile(r"\b(FileHandler|RotatingFileHandler|TimedRotatingFileHandler)\b"),
        "Logs must go to stdout so the platform can collect them. Don't attach file handlers.",
    ),
    # --- one-shot bootstrap done wrong ---
    (
        re.compile(r"^\s*class\s+Command\s*\(BaseCommand\)"),
        "Django management commands cannot be invoked on NetBox Cloud / "
        "Enterprise on demand. Move the logic into a data migration or "
        "a NetBox JobRunner job.",
    ),
]

ALLOW_MARKER = "cloud-compat: ok"


def iter_python_files(root: Path):
    for path in root.rglob("*.py"):
        # Skip test / migration / cache dirs.
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        yield path


def scan() -> int:
    findings: list[tuple[Path, int, str, str]] = []
    for path in iter_python_files(PACKAGE):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        lines = text.splitlines()
        for pattern, explanation in RULES:
            for match in pattern.finditer(text):
                lineno = text.count("\n", 0, match.start()) + 1
                line = lines[lineno - 1] if lineno <= len(lines) else ""
                if ALLOW_MARKER in line:
                    continue
                findings.append((path.relative_to(ROOT), lineno, line.strip(), explanation))

    if not findings:
        print("cloud-compat: OK — no forbidden patterns found.")
        return 0

    print("cloud-compat: FAIL — found patterns incompatible with")
    print("NetBox Enterprise / NetBox Cloud (Kubernetes / multi-pod).")
    print("See AGENTS.md, section 'Cloud / Kubernetes compatibility'.\n")
    for path, lineno, line, explanation in findings:
        print(f"  {path}:{lineno}")
        print(f"    code: {line}")
        print(f"    why : {explanation}")
        print()
    print(f"{len(findings)} finding(s).")
    return 1


if __name__ == "__main__":
    sys.exit(scan())
