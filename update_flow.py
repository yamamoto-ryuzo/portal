import re

with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'r', encoding='utf-8') as f:
    content = f.read()

new_flow = '''
閉鎖環境における継続的学習は、単なる手作業の学習ではなく、以下のような自動化されたパイプライン（システム）として構築される。このループは、**「日常業務からの自動RAG構築とSSOTルール」→「既存システムによるSSOT抽出」→「4つの高度なRAG技術による推論」→「教師データへの自動変換」→「LoRAによる継続学習」という高度な循環システム**として機能する。

**【高度な循環システム（データフライホイール）の全体フロー】**
`mermaid
flowchart LR
    A[⓪ 日常業務と<br>SSOTファイリング] -->|自動同期| B[① 既存検索API<br>SSOT抽出]
    B -->|SSOT提供| C[② 4つのRAG推論<br>マルチエージェント]
    C -->|高品質ログ| D[③ 教師データ<br>自動変換]
    D -->|JSONL| E[④ LoRAによる<br>継続学習]
    E -.背景知識をアップデート.-> C
`
'''

content = content.replace(
    '   閉鎖環境における継続的学習は、単なる手作業の学習ではなく、以下のような自動化 されたパイプライン（システム）として構築される。このループは、**「日常業務からの自動RAG構築とSSOTルール」→「既存システムによるSSOT抽出」→「4つの高度なRAG技術に よる推論」→「教師データへの自動変換」→「LoRAによる継続学習」という高度な循環システム**として機能する。',
    new_flow.strip()
)

with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'w', encoding='utf-8') as f:
    f.write(content)
