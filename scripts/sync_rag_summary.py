import pathlib
from datetime import datetime

SRC = pathlib.Path('docs/RAG_System/INDEX.md')
DST = pathlib.Path('articles/rag-multiagent-guide-summary.md')

FRONTMATTER = '''---
title: "RAGマルチエージェント実装ガイド（要約）"
type: "idea"
emoji: "🦾"
published: true
topics:
  - "ai"
  - "rag"
  - "知識管理"
  - "llm"
  - "土木"
publication_name: "dx_junkyard"
toc_depth: 4
---
'''

def main():
    if not SRC.exists():
        print(f"Source not found: {SRC}")
        return 1
    body = SRC.read_text(encoding='utf-8')
    # Remove any YAML frontmatter from source
    if body.startswith('---'):
        body = body.split('---', 2)[-1].lstrip('\r\n')
    out = FRONTMATTER + '\n' + body.strip() + '\n'
    DST.write_text(out, encoding='utf-8')
    print(f"Updated {DST} from {SRC}")
    return 0

if __name__ == '__main__':
    main()
