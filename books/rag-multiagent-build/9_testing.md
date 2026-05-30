---
title: "E2Eテスト・品質評価"
---

# 9. E2Eテスト・品質評価

## 9.1 評価の3層構造

```mermaid
flowchart LR
    L1["層1: 単体テスト\n各エージェント単独"] --> L2["層2: 統合テスト\nエージェント間連携"]
    L2 --> L3["層3: E2E評価\n想定問答セットで品質計測"]
```

## 9.2 剆1: 単体テスト（エージェント別）

各エージェントに対して、以下の3パターンを最低1問ずつ実施する。

| テストパターン | 期待結果 |
|---|---|
| 正常系（根拠あり） | `confidence="high"`, `sources` に1件以上 |
| 根拠なし | `confidence="low"`, `answer` に「根拠文書未確認」 |
| 軸外の問い（null 入力） | エラーにならず空回答 or スキップ |

### 法令エージェント 正常系テスト例

```python
# tests/test_law_agent.py
import json, pytest
from agents.base_agent import build_agent
from prompts import LAW_PROMPT

law_agent = build_agent(LAW_PROMPT, "kb-law-detail")

@pytest.mark.asyncio
async def test_law_agent_normal():
    result_str = await law_agent("河川占用許可の根拠法令と許可要件は？")
    parsed = json.loads(result_str)
    assert parsed["confidence"] in ("high", "medium")
    assert len(parsed["sources"]) >= 1
    assert "河川法" in parsed["answer"]
```

## 9.3 剆2: 統合テスト（監理サイクル）

監理エージェントの差し戻し・再試行フローを意図的に発生させるテスト。

### テスト手順

1. 法令エージェントの回答に意図的に `sources: []`（根拠なし）を入れる
2. 監理エージェントを実行し `verdict == "FAIL"` かつ `failed_checks` に `[2]` が含まれることを確認
3. `retry_count = 2` でも `FAIL` の場合に `integrate_with_caveat` ルートに進むことを確認

```python
# tests/test_supervisor.py
import json, pytest
from agents.supervisor_agent import supervise

@pytest.mark.asyncio
async def test_supervisor_fail_on_missing_sources():
    agent_results = {
        "kb-law-detail": json.dumps({"answer": "...", "sources": [], "confidence": "low"}),
        # 他エージェントの結果を省略...
    }
    verdict = await supervise(agent_results, retry_count=0)
    assert verdict["verdict"] == "FAIL"
    assert 2 in verdict["failed_checks"]
```

## 9.4 剆3: E2E評価（想定問答セット）

### 評価問答セット（最低10問推奨）

| # | 問い | 想定有効軸 | 評価ポイント |
|---|---|---|---|
| 1 | 河川占用許可の手順を教えてください | law / procedure | 法令条文と手続きリストの整合 |
| 2 | コンクリート橋梁の設計基準は？ | technical | 最新基準版の引用 |
| 3 | 急傾斜地での施工リスクは？ | risk / case | リスクレベルの付与 |
| 4 | 道路占用と河川占用が重複する場合の手続きは？ | law / procedure | 複数法令の統合回答 |
| 5 | 過去の護岸崩壊事例と原因は？ | case | 事例の出典明示 |
| 6 | 土砂崩れが想定される工区での法的義務は？ | law / procedure / risk | 3軸統合の整合性 |
| 7 | （根拠文書にない問い）量子コンピュータの活用方法は？ | なし（全null） | 全エージェントが "low" を返す |
| 8 | 工事着手前の届出書類一覧 | procedure | 手続きリストの網羅性 |
| 9 | 特記仕様書の作成ルールは？ | technical | 最新仕様書バージョン |
| 10 | 施工中に法改正があった場合の対応は？ | law / procedure / technical | 監理エージェントの矛盾検出 |

### 評価指標

| 指標 | 計測方法 | 合格基準 |
|---|---|---|
| **根拠付き回答率** | sources が1件以上の回答割合 | ≥ 80% |
| **差し戻し発生率** | FAIL 判定 / 全問 | ≤ 20%（精度上限） |
| **ハルシネーション率** | 人手確認でのソース不一致数 / 全出典 | ≤ 5% |
| **無効軸除去率** | null 軸がセクション省略されている割合 | 100% |
| **平均レイテンシ** | 問いから最終回答まで | ≤ 30秒（Track A）/ ≤ 15秒（Track B） |

## 9.5 評価ツール（Track B）

```python
# tests/e2e_eval.py
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# RAGAS による自動評価（要 OpenAI API）
results = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
)
print(results.to_pandas())
```

> RAGAS は英語ベースのため、日本語テキストでは faithfulness スコアが低めに出る傾向がある。  
> 8.4節の人手評価と組み合わせて判断する。
