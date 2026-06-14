import sys
import re

content = open('books/rag-multiagent-build/6_deployment_architecture.md', 'r', encoding='utf-8').read()

new_mermaid = """```mermaid
flowchart TD
    User((ユーザー))
    
    %% 総指揮者のグループ
    Orch[マネージャーエージェント<br>タスク分解・意思決定]
    L_All[全LoRA: 法務+積算+施工]
    Base1[(中規模モデル)]
    Note_O[※重たいRAGは持たず全体俯瞰に専念]

    User -->|1. 指示/質問| Orch
    Base1 --> Orch
    L_All -.動的ロード.-> Orch
    Orch -.- Note_O

    %% ワーカーのグループ（法務）
    Agent_Legal[法務ワーカー]
    L_Legal[法務専用LoRA]
    Base2[(中規模モデル)]
    RAG_Legal[(法務SSOT DB)]

    Orch -->|2. 法務チェック依頼| Agent_Legal
    Base2 --> Agent_Legal
    L_Legal -.ロード.-> Agent_Legal
    RAG_Legal <-->|根拠検索| Agent_Legal
    Agent_Legal -->|3. 法務レポート| Orch

    %% ワーカーのグループ（技術）
    Agent_Tech[技術・積算ワーカー]
    L_Tech[積算専用LoRA]
    Base3[(中規模モデル)]
    RAG_Tech[(技術SSOT DB)]

    Orch -->|2. 技術チェック依頼| Agent_Tech
    Base3 --> Agent_Tech
    L_Tech -.ロード.-> Agent_Tech
    RAG_Tech <-->|根拠検索| Agent_Tech
    Agent_Tech -->|3. 技術レポート| Orch

    Orch -->|4. 最終回答生成| User

    style Orch fill:#f9f,stroke:#333,stroke-width:2px
    style Agent_Legal fill:#bbf,stroke:#333,stroke-width:2px
    style Agent_Tech fill:#bbf,stroke:#333,stroke-width:2px
```"""

# Replace the existing mermaid block
content = re.sub(r'```mermaid.*?```', new_mermaid, content, flags=re.DOTALL)
open('books/rag-multiagent-build/6_deployment_architecture.md', 'w', encoding='utf-8').write(content)
