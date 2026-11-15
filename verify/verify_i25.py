import os, re, json
from datetime import datetime

DOCS = r"C:\devin\portal\docs"
pages = []
fm_re = re.compile(r'\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n?', re.S)

def parse_fm(txt):
    fm, body = {}, txt
    m = fm_re.match(txt)
    if not m:
        return fm, body
    body = txt[m.end():]
    for line in m.group(1).splitlines():
        mm = re.match(r'^(\w[\w-]*)\s*:\s*(.*)$', line)
        if not mm:
            continue
        k, v = mm.group(1), mm.group(2).strip()
        if v.startswith('[') and v.endswith(']'):
            fm[k] = [x.strip().strip('"').strip("'") for x in v[1:-1].split(',') if x.strip()]
        elif v == '':
            fm[k] = None
        else:
            fm[k] = v.strip('"').strip("'")
    return fm, body

for root, dirs, files in os.walk(DOCS):
    dirs[:] = [d for d in dirs if not d.startswith(('_', '.'))]
    for f in files:
        if not f.endswith('.md'):
            continue
        path = os.path.join(root, f)
        raw = open(path, encoding='utf-8').read()
        fm, body = parse_fm(raw)
        rel = os.path.relpath(path, DOCS).replace(os.sep, '/')
        url = fm.get('permalink') or '/' + re.sub(r'(index)?\.md$', '', rel)
        d = fm.get('date')
        if isinstance(d, str):
            try:
                d = datetime.strptime(d[:10], '%Y-%m-%d').date()
            except Exception:
                print('BAD DATE:', rel, repr(d))
                d = None
        pages.append(dict(name=f, rel=rel, title=fm.get('title') or f,
                          tags=fm.get('tags') or [], date=d,
                          content=re.sub(r'<[^>]+>', '', body), url=url))

# --- search.json emulation ---
idx = [dict(title=p['title'], url=p['url'], content=p['content'],
            tags=p['tags'], date=str(p['date']) if p['date'] else None)
       for p in pages if p['name'] != 'search.json']
s = json.dumps(idx, ensure_ascii=False)
data = json.loads(s)
print(f"pages={len(pages)} index_entries={len(data)} JSON=OK")

# --- search.js filter emulation ---
def search(q):
    ql = q.lower()
    return [p for p in data if ql in (p['title'] or '').lower()
            or ql in (p['content'] or '').lower()
            or ql in ' '.join(p['tags'] or []).lower()][:20]

for q in ['RAG', 'QGIS', '犬', '検索', 'CDE']:
    h = search(q)
    print(f"query={q!r}: {len(h)} hits -> {[x['title'] for x in h[:5]]}")
    if h:
        c = h[0]['content']
        i = c.lower().find(q.lower())
        st = max(0, i - 40)
        snip = ('...' if st > 0 else '') + c[st:i + len(q) + 40].replace('\n', ' ') + '...'
        print("   snippet:", snip)

# --- tags.md emulation ---
all_tags = sorted({t for p in pages for t in (p['tags'] or [])})
print("\nTAG INDEX:")
for t in all_tags:
    arts = [p['title'] for p in pages if t in (p['tags'] or [])]
    print(f"  {t}: {len(arts)} pages {arts[:3]}")

# --- index.md recent list emulation ---
recent = sorted([p for p in pages if p['date']], key=lambda p: p['date'], reverse=True)[:10]
print("\nRECENT TOP:", [(str(p['date']), p['title']) for p in recent])
