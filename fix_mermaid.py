import sys
import re

content = open('books/rag-multiagent-build/6_deployment_architecture.md', 'r', encoding='utf-8').read()

new_mermaid = """```mermaid
flowchart TD
    %% ユーザー
    User((ユーザー)) -->|1. 指示/質問| Orchestrator

    %% オーケストレーター層
    Orchestrator[マネージャーエージェント<br>タスク分解・調停・意思決定]
    L_All[全LoRA: 法務+積算+施工] -.動的ロード.-> Orchestrator
    Base1[(中規模ベースモデル)] --> Orchestrator
    Note_O[※重たいRAGは持たず全体俯瞰に専念] -.- Orchestrator

    %% 依頼
    Orchestrator -->|2. 法務チェック依頼| Agent_Legal
    Orchestrator -->|2. 技術チェック依頼| Agent_Tech

    %% 法務ワーカー層
    Agent_Legal[法務ワーカー]
    L_Legal[法務専用LoRA] -.ロード.-> Agent_Legal
    Base2[(中規模ベースモデル<br>※メモリ共有)] --> Agent_Legal
    Search_API_Legal[[既存検索API / SSOT抽出]] <-->|検索・絞り込み| RAG_Legal[(法務SSOT DB)]
    Search_API_Legal <-->|4つのRAG推論| Agent_Legal

    %% 技術ワーカー層
    Agent_Tech[技術・積算ワーカー]
    L_Tech[積算専用LoRA] -.ロード.-> Agent_Tech
    Base3[(中規模ベースモデル<br>※メモリ共有)] --> Agent_Tech
    Search_API_Tech[[既存検索API / SSOT抽出]] <-->|検索・絞り込み| RAG_Tech[(技術SSOT DB)]
    Search_API_Tech <-->|4つのRAG推論| Agent_Tech

    %% 回収と出力
    Agent_Legal -->|3. 法務レポート| Orchestrator
    Agent_Tech -->|3. 技術レポート| Orchestrator
    Orchestrator -->|4. 最終回答生成| User

    %% スタイル設定
    style Orchestrator fill:#f9f,stroke:#333,stroke-width:2px
    style Agent_Legal fill:#bbf,stroke:#333,stroke-width:2px
    style Agent_Tech fill:#bbf,stroke:#333,stroke-width:2px
```"""

# Replace the existing mermaid block
content = re.sub(r'```mermaid.*?```', new_mermaid, content, flags=re.DOTALL)
open('books/rag-multiagent-build/6_deployment_architecture.md', 'w', encoding='utf-8').write(content)
