import sys
import re

content = open('books/rag-multiagent-build/6_deployment_architecture.md', 'r', encoding='utf-8').read()

new_mermaid = """```mermaid
flowchart TD
    %% ユーザー入力
    User((ユーザー)) -->|指示/質問| Orchestrator

    %% 総指揮者
    subgraph "総指揮者（オーケストレーター）"
        direction TB
        Orchestrator[マネージャーエージェント<br>タスク分解・調停・意思決定]
        L_All[法務LoRA + 積算LoRA + 施工LoRA] -.動的ロード.-> Orchestrator
        Base1[(中規模ベースモデル)] --> Orchestrator
        Note_O[※重たい外部検索RAGは行わず<br>全体俯瞰に専念] -.- Orchestrator
    end

    %% 分配
    Orchestrator -->|1. 法務チェック依頼| Agent_Legal
    Orchestrator -->|2. 技術/積算チェック依頼| Agent_Tech

    %% 法務エージェント
    subgraph "法務エージェント（ワーカー）"
        direction TB
        Agent_Legal[法務ワーカー]
        L_Legal[法務専用LoRA] -.ロード.-> Agent_Legal
        Base2[(中規模ベースモデル<br>※メモリ共有)] --> Agent_Legal
        RAG_Legal[(法務SSOT専用<br>ベクトルDB)] <-->|根拠検索| Agent_Legal
    end

    %% 技術エージェント
    subgraph "技術エージェント（ワーカー）"
        direction TB
        Agent_Tech[技術・積算ワーカー]
        L_Tech[積算専用LoRA] -.ロード.-> Agent_Tech
        Base3[(中規模ベースモデル<br>※メモリ共有)] --> Agent_Tech
        RAG_Tech[(技術SSOT専用<br>ベクトルDB)] <-->|根拠検索| Agent_Tech
    end

    %% 統合
    Agent_Legal -->|3. 法務レポート（根拠付）| Orchestrator
    Agent_Tech -->|4. 技術レポート（根拠付）| Orchestrator
    
    Orchestrator -->|5. 最終回答生成| User

    style Orchestrator fill:#f9f,stroke:#333,stroke-width:2px
    style Agent_Legal fill:#bbf,stroke:#333,stroke-width:2px
    style Agent_Tech fill:#bbf,stroke:#333,stroke-width:2px
```"""

# Replace the existing mermaid block
content = re.sub(r'```mermaid.*?```', new_mermaid, content, flags=re.DOTALL)
open('books/rag-multiagent-build/6_deployment_architecture.md', 'w', encoding='utf-8').write(content)
