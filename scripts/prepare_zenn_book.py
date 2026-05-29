#!/usr/bin/env python3
"""
Prepare a Zenn-compatible book folder by copying a docs/books/<slug> folder.

Usage:
  python scripts/prepare_zenn_book.py docs/books/rag-multiagent-build zenn/content/books/rag-multiagent-build

This script requires PyYAML: `pip install pyyaml`
"""
import sys
import shutil
from pathlib import Path

try:
    import yaml
except Exception:
    print("PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


def load_config(config_path: Path):
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return data


def prepare(src: Path, dst: Path):
    config_path = src / "config.yaml"
    if not config_path.exists():
        print(f"config.yaml not found in {src}")
        return 1
    cfg = load_config(config_path)
    title = cfg.get("title", "")
    summary = cfg.get("summary", "")
    chapters = cfg.get("chapters", [])

    dst.mkdir(parents=True, exist_ok=True)

    # Copy chapter files
    for ch in chapters:
        src_md = src / f"{ch}.md"
        if not src_md.exists():
            print(f"Warning: chapter file not found: {src_md}")
            continue
        shutil.copy(src_md, dst / src_md.name)

    # Create index.md for Zenn book
    index_path = dst / "index.md"
    with index_path.open("w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f'title: "{title}"\n')
        f.write('type: "book"\n')
        f.write(f'short_description: "{summary}"\n')
        f.write('published: true\n')
        f.write("---\n\n")
        f.write(f"# {title}\n\n")
        f.write(f"{summary}\n\n")
        f.write("## 章一覧\n\n")
        for ch in chapters:
            md = f"{ch}.md"
            if (dst / md).exists():
                # Use relative link
                f.write(f"- [{md}]({md})\n")

    print(f"Prepared Zenn book at: {dst}")
    return 0


def main():
    if len(sys.argv) < 3:
        print("Usage: prepare_zenn_book.py <src_folder> <dst_folder>")
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    sys.exit(prepare(src, dst))


if __name__ == "__main__":
    main()
