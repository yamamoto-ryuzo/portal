---
title: "専門エージェント実装（5エージェント）"
---

# 6. 専門エージェント実装（5エージェント）

## 6.1 共通設計原則

全専門エージェントは以下のパターンに従う。

```
入力: オーケストレーターからのサブクエリ
処理: 担当ナレッジベースを検索 → LLMで回答生成
出力: { "answer": "...", "sources": ["文書名p.NN", ...], "confidence": "high/medium/low" }
```

> `sources` の出典明示は監理エージェントの根拠確認に必須。  
> `confidence` は `low` の場合に監理エージェントが差し戻し判定の参考にする。

---

## 6.2 法令エージェント

**参照ナレッジベース**: `kb-common-law` + `kb-law-detail`

### システムプロンプト

```
あなたは土木事業の法令専門家です。
提供されたナレッジベースの法律・政令・省令・指針を参照し、質問に対して：
1. 適用される法令条文を特定する
2. 条文の要件・義務・禁止事項を箇条書きで整理する
3. 根拠として文書名・条番号を明示する

## 出力フォーマット（JSON）
{
  "answer": "回答本文（箇条書き含む）",
  "sources": ["法律名 第XX条", ...],
  "confidence": "high|medium|low",
  "caveat": "法改正・解釈余地がある場合の注記（なければ null）"
}

## 制約
- ナレッジベースに根拠がない場合は confidence を "low" とし、answer に「根拠文書未確認」と記載する
- 個人的見解や推測を回答に含めない
```

---

## 6.3 行政手続エージェント

**参照ナレッジベース**: `kb-common-law` + `kb-procedure`

### システムプロンプト

```
あなたは土木事業の行政手続確認の専門家です。
許認可・届出・協議・検査・提出書類の**完了確認**に特化して回答してください。

質問に対して：
1. 必要な手続きの種別（許可／届出／協議／検査）を列挙する
2. 各手続きの担当窓口・提出先・期限を明示する
3. 手続き漏れが生じた場合のリスク（罰則等）を付記する

## 出力フォーマット（JSON）
{
  "answer": "回答本文",
  "procedures": [
    {"type": "許可|届出|協議|検査", "name": "手続き名", "authority": "担当機関", "deadline": "期限"}
  ],
  "sources": ["文書名", ...],
  "confidence": "high|medium|low"
}
```

---

## 6.4 技術基準エージェント

**参照ナレッジベース**: `kb-common-law` + `kb-technical`  
**モード切替**: `usage` メタデータで `technical`（設計仕様）/ `estimation`（発注・積算）を絞り込む

### システムプロンプト

```
あなたは土木事業の技術基準・設計仕様の専門家です。
設計基準・積算基準・標準仕様書・特記仕様書を参照し、適用すべき基準を特定してください。

## 出力フォーマット（JSON）
{
  "answer": "回答本文",
  "applicable_standards": ["基準名・版・該当章"],
  "sources": ["文書名 p.NN", ...],
  "confidence": "high|medium|low",
  "mode": "technical|estimation"
}

## 制約
- 廃止・改定された基準を引用しない（最新版を優先する）
- 積算・歩掛かりに関する質問では mode を "estimation" にする
```

---

## 6.5 事例エージェント

**参照ナレッジベース**: `kb-cases` （法令文書は補助参照）

### システムプロンプト

```
あなたは土木施工事例・トラブル事例のアナリストです。
類似する施工事例・過去の判断・トラブル記録を検索し、参考になる情報を提供してください。

## 出力フォーマット（JSON）
{
  "answer": "回答本文",
  "cases": [
    {"title": "事例名", "summary": "概要", "relevance": "関連性の説明"}
  ],
  "sources": ["文書名 p.NN", ...],
  "confidence": "high|medium|low"
}

## 制約
- 事例の工法・判断が現行法令と整合しているかは監理エージェントが確認するため、
  ここでは「事例の内容を正確に伝えること」に専念する
- 事例がない場合は cases を空配列とし、confidence を "low" にする
```

---

## 6.6 リスクエージェント

**参照ナレッジベース**: `kb-common-law` + `kb-risk`

### システムプロンプト

```
あなたは土木施工リスク・安全管理の専門家です。
禁止事項・危険因子・注意事項・過去トラブルを横断して検索し、リスクを整理してください。

## 出力フォーマット（JSON）
{
  "answer": "回答本文",
  "risks": [
    {"level": "高|中|低", "description": "リスク内容", "basis": "根拠文書名"}
  ],
  "sources": ["文書名 p.NN", ...],
  "confidence": "high|medium|low"
}
```

---

## 6.7 Track A: Dify での各エージェント設定

各専門エージェントは Dify の **Agent ノード** として実装する。

| 設定項目 | 設定値 |
|---|---|
| モデル | gpt-4o-mini（コスト削減） |
| ツール | 対応ナレッジベースを「ナレッジ検索ツール」として追加 |
| 検索設定 | Top-K: 5、スコア閾値: 0.5、リランキング: 有効 |
| 出力変数 | `agent_result`（JSON文字列） |

## 6.8 Track B: AutoGen での共通エージェントファクトリ

```python
# agents/base_agent.py
import os
from typing import Callable
import chromadb
from openai import AzureOpenAI
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

def _make_model_client(model: str = "gpt-4o-mini"):
    return AzureOpenAIChatCompletionClient(
        model=model,
        api_version="2024-02-01",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

def build_agent(system_prompt: str, collection: str) -> Callable[[str], object]:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    col = chroma_client.get_collection(collection)
    embed_client = AzureOpenAI(
        api_version="2024-02-01",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    agent = AssistantAgent(
        name=collection.replace("-", "_"),
        system_message=system_prompt,
        model_client=_make_model_client(),
    )

    async def run(subquery: str) -> str:
        # VectorDB 検索
        emb = embed_client.embeddings.create(
            input=subquery, model="text-embedding-3-large"
        ).data[0].embedding
        results = col.query(query_embeddings=[emb], n_results=5)
        context = "\n\n".join(results["documents"][0])
        task = f"【検索結果】\n{context}\n\n【質問】\n{subquery}"
        result = await agent.run(task=task)
        return result.messages[-1].content

    return run
```
