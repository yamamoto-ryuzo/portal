---
title: "オーケストレーター実装"
---

# 5. オーケストレーター実装

> オーケストレーターは**直接 RAG を参照せず、問いを分解してルーティングする**ことに専念する。  
> 検索と問い分解を同一エージェントに担わせると精度が不安定になる（設計書 11.2節参照）。

## 5.1 役割の明確化

```
入力: ユーザーの自然言語の問い
処理: 問いを「法令／行政手続／技術基準／事例／リスク」の5軸に分解し、
      各専門エージェントへのサブクエリを生成する
出力: JSON 形式のサブクエリセット
```

## 5.2 オーケストレーター・システムプロンプト

```
あなたは土木事業管理の質問ルーターです。
ユーザーの問いを以下の5軸で分析し、各エージェントに渡すサブクエリをJSON形式で出力してください。

## 出力フォーマット
{
  "law":       "法令・条文の観点からのサブクエリ（不要な場合は null）",
  "procedure": "許認可・届出・行政手続の観点からのサブクエリ（不要な場合は null）",
  "technical": "技術基準・設計仕様の観点からのサブクエリ（不要な場合は null）",
  "case":      "類似施工事例・過去判断の観点からのサブクエリ（不要な場合は null）",
  "risk":      "リスク・禁止事項・注意事項の観点からのサブクエリ（不要な場合は null）"
}

## 制約
- サブクエリは元の問いの意図を保ちながら、各エージェントが検索しやすい表現に変換する
- 関係のない軸は必ず null にすること（全軸を埋めない）
- JSON のみ出力し、前後に説明文を付けない
```

## 5.3 Track A: Dify 実装

### 5.3.1 Chatflow 設計

```
[START] → [LLM ノード: オーケストレーター]
              ↓ JSON 出力
           [コード ノード: JSON パース & null 除去]
              ↓
           [並列分岐]
           ├─ law ノード（nullでない場合）
           ├─ procedure ノード（nullでない場合）
           ├─ technical ノード（nullでない場合）
           ├─ case ノード（nullでない場合）
           └─ risk ノード（nullでない場合）
```

### 5.3.2 JSON パース コードノード（Dify / Python）

```python
import json

def main(orchestrator_output: str) -> dict:
    data = json.loads(orchestrator_output)
    # null を除外して有効なサブクエリのみ返す
    return {k: v for k, v in data.items() if v is not None}
```

## 5.4 Track B: AutoGen 実装

```python
# agents/orchestrator.py
import json, os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

SYSTEM_PROMPT = """...(5.2節のプロンプト)..."""

_model_client = AzureOpenAIChatCompletionClient(
    model="gpt-4o",
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

orchestrator = AssistantAgent(
    name="orchestrator",
    system_message=SYSTEM_PROMPT,
    model_client=_model_client,
)

async def orchestrate(question: str) -> dict:
    result = await orchestrator.run(task=question)
    raw = result.messages[-1].content
    subqueries = json.loads(raw)
    # null を除外して有効なサブクエリのみ返す
    return {k: v for k, v in subqueries.items() if v}
```

## 5.5 ルーティング精度の確認

以下のテスト問いでサブクエリ分解を確認する。

| テスト問い | 期待する有効軸 |
|---|---|
| 「河川占用許可の手順を教えてください」 | law / procedure |
| 「コンクリート構造物の設計基準は？」 | technical |
| 「斜面崩壊のリスク対策事例は？」 | case / risk |
| 「工事施工中の河川流量制限と届出義務は？」 | law / procedure / technical / risk |

各テスト問いに対し、不要な軸が `null` になっていることを確認する。
