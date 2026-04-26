#!/usr/bin/env python3
import re
from pathlib import Path

# Load simple YAML config (no external dependency)
def load_simple_yaml(path: Path):
    cfg = {}
    if not path.exists():
        return cfg
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            k, v = line.split(':', 1)
            k = k.strip()
            v = v.strip()
            # simple list handling (only for topics)
            if v == '':
                cfg[k] = []
            elif v.startswith('[') and v.endswith(']'):
                items = [s.strip().strip('"').strip("'") for s in v[1:-1].split(',') if s.strip()]
                cfg[k] = items
            elif v.startswith('"') and v.endswith('"'):
                cfg[k] = v[1:-1]
            elif v in ('true', 'false'):
                cfg[k] = (v == 'true')
            else:
                # try number
                try:
                    cfg[k] = int(v)
                except Exception:
                    cfg[k] = v.strip('"').strip("'")
    return cfg

cfg_path = Path('.github/scripts/zenn_config.yaml')
cfg = load_simple_yaml(cfg_path)

src = Path(cfg.get('src', 'プロジェクトCDE/index.md'))
dst = Path(cfg.get('dst', 'articles/project-cde-guide.md'))
toc_depth = int(cfg.get('toc_depth', 3))

content = src.read_text(encoding='utf-8')

# Jekyllフロントマター除去
content = re.sub(r'^---\s*\n(.*?\n)?---\s*\n', '', content, flags=re.DOTALL).strip()

# Build Zenn front matter from config
front_lines = ['---']
front_lines.append(f'title: "{cfg.get("title", "")}"')
front_lines.append(f'emoji: "{cfg.get("emoji", "")}"')
front_lines.append(f'type: "{cfg.get("type", "")}"')
topics = cfg.get('topics', [])
if isinstance(topics, list):
    topics_str = '[' + ', '.join(f'"{t}"' for t in topics) + ']'
else:
    topics_str = '[]'
front_lines.append(f'topics: {topics_str}')
front_lines.append(f'published: {str(cfg.get("published", True)).lower()}')
front_lines.append(f'canonical_url: "{cfg.get("canonical_url", "")}"')
front_lines.append(f'publication_name: "{cfg.get("publication_name", "")}"')
front_lines.append('---\n')
front = '\n'.join(front_lines) + '\n'

# Generate manual TOC up to toc_depth (include headings H2..H{toc_depth})
toc_lines = []
for m in re.finditer(r'^(#{2,6})\s+(.*)$', content, flags=re.MULTILINE):
    level = len(m.group(1))
    text = m.group(2).strip()
    if level <= toc_depth:
        indent = '  ' * (level - 2)
        # create slug: replace spaces with -, keep unicode chars
        slug = re.sub(r'[\s]+', '-', re.sub(r'[\(\)\"\'']', '', text)).strip().lower()
        toc_lines.append(f'{indent}- [{text}](#{slug})')

toc_block = ''
if toc_lines:
    toc_block = '## 目次\n\n' + '\n'.join(toc_lines) + '\n\n'

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(front + toc_block + content + "\n", encoding='utf-8')
print(f"Synced: {src} -> {dst}")
