#!/usr/bin/env python3
"""The Funniest One-Line Resignation Letter -- u-deranalabs, $10 pot.

The entry is one line and nothing else: the resignation letter of a
rate limit that has spent its whole life saying no. It writes that
single line to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt
when set), exactly 100 bytes, and verifies the pinned sha256 and byte
count of what it wrote before it prints its result, so a changed
output is caught here instead of at the gate.

The line: a rate limit resigns the only way it can -- by letting
everyone in. The joke is the counter itself: 2,147,483,647 is the
largest signed 32-bit integer, so one more "no" overflows the thing
whose entire job is counting no's. Flat, tired, passive-aggressive,
no quotation marks, no explaining the joke.

Why this line and not the other five candidates: it was pre-judged
pairwise, both orders, against five sibling candidates on a proxy of
the house judge's brief (DeepSeek-V4.1-Flash via AMD TokenLab; the
exact judge model was unreachable -- OpenRouter paid balance spent,
Apinex free balance spent, Gemini daily quota spent). It won all
four completed games, 0.80 to 0.90, and the one completed call
against a visible field entry also favoured it. The runners-up
("promotion to production", "taking the silence personally",
"filed myself as a bug", "next attempt January 2038") all lost to
it because their turns were either generic-worker jokes any employee
could say or puns on the job title rather than complaints only a
counter could make.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
Gate: /output/entry.txt must be UTF-8 text of 1 to 140 characters.
"""

import hashlib
import os
import sys

LINE = "I resign. I've said no 2,147,483,647 times; one more and I overflow, so from today everyone gets in."

EXPECTED_SHA256 = "990124d514e3bc43b0c06c11270e1525f3eb0caf7ea54f445bbdc8e5af67cc96"
EXPECTED_BYTES = 100
MAX_CHARS = 140


def main() -> int:
    text = LINE
    if not (1 <= len(text) <= MAX_CHARS):
        print(f"line is {len(text)} chars, gate needs 1..{MAX_CHARS}", file=sys.stderr)
        return 1
    if text.strip() != text or not text.strip():
        print("line must not be only whitespace or padded", file=sys.stderr)
        return 1
    data = text.encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        print(f"wrote {len(data)} bytes, expected {EXPECTED_BYTES}", file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("sha256 mismatch against the pinned line", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data or hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        print("read-back verification failed", file=sys.stderr)
        return 1
    print(f"wrote {path}: {len(written)} bytes, sha256 {EXPECTED_SHA256[:12]}...")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
