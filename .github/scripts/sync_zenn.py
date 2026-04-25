#!/usr/bin/env python3
import re
from pathlib import Path

src = Path("プロジェクトCDE/index.md")
dst = Path("articles/project-cde-guide.md")

content = src.read_text(encoding="utf-8")

# Jekyllフロントマター除去
content = re.sub(r'^---\s*\n(.*?\n)?---\s*\n', '', content, flags=re.DOTALL).strip()

# Zennフロントマター
front = (
    '---\n'
    'title: "プロジェクトCDE — 構想・機能・運用ガイド"\n'
    'emoji: "🗺️"\n'
    'type: "idea"\n'
    'topics: ["GIS", "CDE", "BIM", "公共事業", "土木"]\n'
    'published: true\n'
    'canonical_url: "https://yamamoto-ryuzo.github.io/portal/%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88CDE/"\n'
    'publication_name: "dx_junkyard"\n'
    '---\n\n'
)

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(front + content + "\n", encoding="utf-8")
print(f"Synced: {src} -> {dst}")
