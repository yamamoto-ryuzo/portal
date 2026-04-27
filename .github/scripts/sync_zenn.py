#!/usr/bin/env python3
import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def parse_simple_yaml(path):
	data = {}
	topics = []
	with open(path, encoding='utf-8') as f:
		lines = f.readlines()
	i = 0
	while i < len(lines):
		line = lines[i].rstrip('\n')
		if not line.strip() or line.lstrip().startswith('#'):
			i += 1
			continue
		if ':' in line:
			key, val = line.split(':', 1)
			key = key.strip()
			val = val.strip().strip('"').strip("'")
			if val == '':
				# handle list (topics)
				if key == 'topics':
					i += 1
					while i < len(lines):
						l = lines[i]
						if l.strip().startswith('-'):
							topics.append(l.strip().lstrip('-').strip().strip('"').strip("'"))
							i += 1
						else:
							break
					data['topics'] = topics
					continue
				else:
					data[key] = val
			else:
				lv = val.lower()
				if lv in ('true', 'false'):
					data[key] = (lv == 'true')
				else:
					try:
						data[key] = int(val)
					except Exception:
						data[key] = val
		i += 1
	return data


def strip_frontmatter(text):
	if text.startswith('---'):
		parts = text.split('---', 2)
		if len(parts) >= 3:
			return parts[2].lstrip('\n')
	return text


def build_frontmatter(cfg):
	parts = []
	parts.append('---')
	if 'title' in cfg:
		parts.append(f'title: "{cfg.get("title")}"')
	if 'emoji' in cfg:
		parts.append(f'emoji: "{cfg.get("emoji")}"')
	if 'type' in cfg:
		parts.append(f'type: "{cfg.get("type")}"')
	if 'topics' in cfg:
		parts.append('topics: ' + json.dumps(cfg.get('topics'), ensure_ascii=False))
	if 'published' in cfg:
		parts.append('published: ' + ("true" if cfg.get('published') else "false"))
	if 'canonical_url' in cfg:
		parts.append(f'canonical_url: "{cfg.get("canonical_url")}"')
	if 'publication_name' in cfg:
		parts.append(f'publication_name: "{cfg.get("publication_name")}"')
	if 'toc_depth' in cfg:
		parts.append('toc_depth: ' + str(cfg.get('toc_depth')))
	parts.append('---\n')
	return '\n'.join(parts)


def main():
	cfg_path = os.path.join(os.path.dirname(__file__), 'zenn_config.yaml')
	if not os.path.exists(cfg_path):
		print('zenn_config.yaml not found', file=sys.stderr)
		sys.exit(1)
	cfg = parse_simple_yaml(cfg_path)

	src = cfg.get('src')
	dst = cfg.get('dst')
	if not src or not dst:
		print('src or dst not set in config', file=sys.stderr)
		sys.exit(1)

	src_path = os.path.join(ROOT, src)
	dst_path = os.path.join(ROOT, dst)

	if not os.path.exists(src_path):
		print(f'src not found: {src_path}', file=sys.stderr)
		sys.exit(1)

	with open(src_path, encoding='utf-8') as f:
		src_text = f.read()

	body = strip_frontmatter(src_text)

	front = build_frontmatter(cfg)
	out_text = front + body

	# ensure destination dir exists
	os.makedirs(os.path.dirname(dst_path), exist_ok=True)

	prev = None
	if os.path.exists(dst_path):
		with open(dst_path, encoding='utf-8') as f:
			prev = f.read()

	if prev == out_text:
		print('No changes to write.')
		return

	with open(dst_path, 'w', encoding='utf-8') as f:
		f.write(out_text)

	print(f'Wrote {dst_path}')


if __name__ == '__main__':
	main()
