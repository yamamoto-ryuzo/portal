import sys, math
try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    has_tiktoken = True
except Exception:
    enc = None
    has_tiktoken = False
paths = [r"c:\github\portal\books\rag-multiagent-build\1_overview.md", r"c:\github\portal\books\rag-multiagent-build\2_ssot_strategy.md"]
for path in paths:
    with open(path, encoding='utf-8') as f:
        s = f.read()
    chars = len(s)
    if has_tiktoken:
        toks = len(enc.encode(s))
    else:
        toks = int(round(chars/4))
    print(path)
    print(f"CHARS:{chars}")
    print(f"TOKENS:{toks}")
    for sz in (500,800,1000):
        print(f"CHUNK_{sz}:{math.ceil(toks/sz)}")
    print('HAS_TIKTOKEN:' + str(has_tiktoken))
