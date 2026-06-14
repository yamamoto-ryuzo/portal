with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re

new_mermaid = '''`mermaid
flowchart TD
    A[⓪ 日常業務と<br>SSOTファイリング] -->|自動同期| B[① 既存検索API<br>SSOT抽出]
    
    subgraph 推論と生成
        B -->|SSOT提供| C[② 4つのRAG推論<br>マルチエージェント<br>※初期はゼロショット〜軽量LoRA]
    end
    
    subgraph 継続的学習ループ
        C -->|高品質ログ| D[③ 教師データ<br>自動変換]
        D -->|JSONL| E[④ LoRAによる<br>継続学習]
        E -.最新の背景知識を<br>アップデート.-> C
    end
`'''

text = re.sub(r'`mermaid\nflowchart TD\n    A\[.*?`', new_mermaid, text, flags=re.DOTALL)

with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'w', encoding='utf-8') as f:
    f.write(text)
