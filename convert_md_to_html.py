# -*- coding: utf-8 -*-
"""docs/ 配下の .md を .html へ一括変換する（front matter・Liquid タグを保持）。"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "docs"

liquid = []


def stash(m):
    liquid.append(m.group(0))
    return "LIQMARK%dLIQMARK" % (len(liquid) - 1)


def convert(md: Path):
    text = md.read_text(encoding="utf-8")
    fm, body = "", text
    m = re.match(r"\A---\r?\n.*?\r?\n---\r?\n?", text, re.S)
    if m:
        fm, body = text[: m.end()], text[m.end():]

    del liquid[:]
    body2 = re.sub(r"\{%-?.*?-?%\}|\{\{.*?\}\}", stash, body, flags=re.S)

    # kramdown は空行なしでも ATX 見出しを認めるが pandoc は段落に吸収する。
    # コードフェンス外で、非空行の直後に来る見出しの前に空行を挿入する
    fixed, in_fence = [], False
    for line in body2.split("\n"):
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
        if (
            not in_fence
            and re.match(r"^#{1,6}\s", line)
            and fixed
            and fixed[-1].strip() != ""
            and not fixed[-1].lstrip().startswith(("<", "{%", "{{"))
        ):
            fixed.append("")
        fixed.append(line)
    body2 = "\n".join(fixed)

    r = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html", "--wrap=none"],
        input=body2, capture_output=True, text=True, encoding="utf-8",
    )
    if r.returncode != 0:
        sys.exit("pandoc failed on %s: %s" % (md, r.stderr))
    html = r.stdout

    # ブロック単位の Liquid: <p>LIQMARKn</p> ごと復元して <p> を残さない
    html = re.sub(
        r"<p>\s*LIQMARK(\d+)LIQMARK\s*</p>",
        lambda mm: liquid[int(mm.group(1))],
        html,
    )
    # インラインの Liquid 残りを復元
    html = re.sub(
        r"LIQMARK(\d+)LIQMARK", lambda mm: liquid[int(mm.group(1))], html
    )

    # サイト内 .md リンクを .html へ
    html = re.sub(r'(href="[^"]*?)\.md([#"])', r"\1.html\2", html)

    md.with_suffix(".html").write_text(fm + html, encoding="utf-8")
    print("converted:", md.name, "->", md.with_suffix(".html").name)


for f in sorted(ROOT.rglob("*.md")):
    convert(f)
