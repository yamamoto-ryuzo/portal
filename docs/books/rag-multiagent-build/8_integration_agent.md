---
title: "回答統合エージェント実装"
---

# 8. 回答統合エージェント実装

> 回答統合エージェントは**直接 RAG を参照しない**。  
> 監理エージェントが検証済みの情報を受け取り、**根拠付き構造化回答**に仕上げる。

## 8.1 出力フォーマット設計

ユーザーに返す最終回答は以下の構造を原則とする。

```
## 回答サマリー
（1〜3文の結論）

## 法令・根拠
- 適用法令・条文番号
- 参照基準

## 必要な手続き
- 手続き名 / 担当機関 / 期限

## 技術基準・仕様
- 適用すべき基準・版

## 参考事例
- 事例名と概要

## リスク・注意事項
- 高：...
- 中：...

## 出典一覧
- [文書名 p.NN]
```

## 8.2 回答統合エージェント・システムプロンプト

```
あなたは土木事業管理の回答統合エージェントです。
監理エージェントが検証済みの5専門エージェントの回答を受け取り、
ユーザー向けの「根拠付き構造化回答」を作成してください。

## 入力
{supervisor_approved_results}
{caveat}  // "検証保留" の注記がある場合のみ

## 出力規則
1. 回答サマリーは結論を先に述べる（ピラミッド原則）
2. 各セクションには必ず出典（文書名・ページ）を付ける
3. エージェントが confidence="low" を返した箇所には ⚠️ を付記する
4. caveat がある場合は冒頭に「※ 一部情報は検証保留です。専門家確認を推奨します。」を追加する
5. 回答に含まれない軸（null だったエージェント）のセクションは省略する

## 出力フォーマット
Markdown 形式で出力する。JSON 不要。
```

## 8.3 Track A: Dify 実装

| 設定 | 値 |
|---|---|
| ノード種別 | LLM ノード |
| モデル | gpt-4o（最終品質重視） |
| 入力変数 | 監理エージェントの承認済み結果 + caveat フラグ |
| 出力 | `final_answer`（Markdown テキスト） |

### コードノード: caveat 付与

```python
def main(supervisor_verdict: str, combined_results: str) -> dict:
    import json
    verdict = json.loads(supervisor_verdict)
    caveat = ""
    if verdict.get("retry_count", 0) >= 2:
        caveat = "※ 一部情報は検証保留です。専門家確認を推奨します。"
    return {"approved_results": combined_results, "caveat": caveat}
```

## 8.4 Track B: AutoGen 実装

```python
# agents/integration_agent.py
import json, os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

INTEGRATION_PROMPT = """...(8.2節のプロンプト)..."""

_model_client = AzureOpenAIChatCompletionClient(
    model="gpt-4o",
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

integration_agent = AssistantAgent(
    name="integration",
    system_message=INTEGRATION_PROMPT,
    model_client=_model_client,
)

async def integrate(agent_results: dict, retry_count: int = 0) -> str:
    caveat = "検証保留" if retry_count >= 2 else ""
    task = (
        f"【検証済み回答】\n{json.dumps(agent_results, ensure_ascii=False)}"
        f"\n\n【注記】\n{caveat}"
    )
    result = await integration_agent.run(task=task)
    return result.messages[-1].content
```

## 8.5 出力品質の確認項目

- [ ] 結論が冒頭の「回答サマリー」に明示されている
- [ ] 全セクションに出典（文書名）が付いている
- [ ] `confidence="low"` だった箇所に ⚠️ が付いている
- [ ] 検証保留の場合に注記が冒頭に表示されている
- [ ] null だった軸のセクションが省略されている（余計な「情報なし」記載がない）
