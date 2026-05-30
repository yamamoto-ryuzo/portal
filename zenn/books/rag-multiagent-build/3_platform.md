---
title: "実装プラットフォーム選択"
---

# 3. 実装プラットフォーム選択

## 3.1 選択肢の比較

| 観点 | Dify（Track A） | AutoGen（Track B） | M365 Copilot Studio |
|---|---|---|---|
| **セットアップ時間** | 数時間（Docker 1コマンド） | 1〜3日 | 数時間（テナント設定次第） |
| **エージェント間接続** | GUI でフロー設計 | Python コードで定義 | Power Automate フロー |
| **RAGナレッジ管理** | 組み込み UI で文書登録 | 外部VectorDB（Chroma/pgvector） | SharePoint / Copilot データソース |
| **カスタムロジック** | DSL / HTTP ノードで拡張 | 完全自由（Python + A2A/MCP） | Power FX / Azure Function 連携 |
| **コスト** | セルフホスト無料 | インフラ費のみ | M365 ライセンス必須 |
| **本番可用性** | ★★★☆☆ | ★★★★★ | ★★★★☆ |
| **向いているフェーズ** | PoC・部署展開 | 本番・大規模 | M365 統合重視環境 |

## 3.2 Track A: Dify 環境構築

### 3.2.1 前提

- Docker Desktop 4.x 以上インストール済み
- OpenAI API キー または Azure OpenAI エンドポイント

### 3.2.2 起動手順

```bash
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env
# .env の OPENAI_API_KEY を設定
docker compose up -d
# http://localhost/install でセットアップ
```

### 3.2.3 モデル設定

Dify 管理画面 → **設定 > モデルプロバイダー** で以下を設定する。

| 用途 | 推奨モデル | 備考 |
|---|---|---|
| オーケストレーター | GPT-4o | 問い分解の品質が高い |
| 専門エージェント | GPT-4o-mini | コスト削減 |
| 埋め込み | text-embedding-3-large | 日本語精度優先 |
| リランキング | BGE-Reranker-v2-m3 | ローカルモデル可 |

### 3.2.4 Dify のマルチエージェント構成イメージ

```
Chatflow（オーケストレーター）
  └─ Agent ノード × 5（専門エージェント）
       └─ HTTP ノード or Agent ノード（監理エージェント）
            └─ LLM ノード（回答統合エージェント）
```

## 3.3 Track B: AutoGen 環境構築

### 3.3.1 前提