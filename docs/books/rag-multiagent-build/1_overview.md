---
title: "本書の目的・対象読者・前提知識"
---

# 1. 本書の目的・対象読者・前提知識

## 1.1 本書が解決すること

[土木事業管理 RAGシステム構築ガイド](../rag-civil-engineering/1_intro.md)（以下「設計書」）では、  
マルチエージェント構成の**理論と設計方針**を示した。  
本書はその続編として、**実際に動くシステムを手順通りに組み立てる**ための実装ガイドである。


| 設計書（rag-civil-engineering） | 本書（rag-multiagent-build） |
|---|---|
| なぜマルチエージェントが必要か | どう実装するか |
| エージェント構成の論理設計 | 各エージェントのプロンプト・接続設定 |
| RAGスコープの推奨設計 | ナレッジベースの実際の作り方 |
| KPI・ロードマップ | テスト手順・評価指標の測定方法 |

## 1.2 対象読者

| 読者 | 期待する成果 |
|---|---|
| AI導入担当者（ローコード） | DifyでPoC環境を1週間以内に動かす |
| バックエンドエンジニア | Microsoft AutoGenで本番グレードのパイプラインを構築する |
| 事業管理担当者 | 動作テストの評価基準を理解し、受入検査を実施できる |

## 1.3 前提知識

本書を進める前に以下を把握していること。

- [設計書 1章〜7章](../rag-civil-engineering/1_intro.md)の内容（特に7章のエージェント構成図）
- Markdown・YAMLの基本読み書き
- LLM API（OpenAI / Azure OpenAI）の基本操作
- Git の基本操作（clone / commit / push）

## 1.4 本書で扱う実装トラック

### 1.4.1 フレームワーク選定基準（評価軸）

本書での実装トラックを選定する際の評価軸は以下の8項目を用いる。

1. **A2A（Agent-to-Agent）** — 2025年4月にGoogleが正式公開した[A2A Protocol](https://github.com/google-a2a/A2A)への準拠・マルチエージェント間協調実装の成熟度
2. **MCP（Model Context Protocol）** — Anthropicが提唱し2025年に事実上の標準となったツール・データソース接続プロトコル([Model Context Protocol](https://modelcontextprotocol.io/))への対応状況。知識源・外部API・Box/M365等との接続手段として評価
3. **GitHub Copilot 連携** — Copilot を使った開発フローの対応状況（テンプレート・Copilot Studio 等）
4. **ドキュメント生成** — Pandoc 等によるきめ細かいドキュメント出力の容易さ
5. **Box AI 接続** — Box AI との接続・コンテンツ取得の容易性（MCP Server経由含む）
6. **M365 Copilot 接続** — Microsoft 365 / M365 Copilot との親和性。特に **M365 Copilot Studio（Agent Studio）で作成したエージェントを外部フレームワークからA2A呼び出しできるか**（Azure AI Agent Service経由・A2A Protocol・Power Platform Connector等）を重視して評価
7. **CLI 利用** — ワークフローをコマンドラインで起動・自動化できる容易さ
8. **MD知識活用AIの選択性** — [§1.5 技術要素（RAGコアレイヤー）](#15-技術要素ragコアレイヤー) の技術定義MDをAIエージェントが直接読み込み・参照・活用できるか（知識源として組み込める構成の柔軟性）

### 1.4.2 推奨フレームワーク（優先度順）

評価軸1〜8をもとに並べた優先候補一覧。各評価軸の詳細は [§1.4.1](#141-フレームワーク選定基準評価軸) 参照。

| 優先度 | フレームワーク | ①A2A | ②MCP | ③Copilot | ④Doc生成 | ⑤BoxAI | ⑥M365 | ⑦CLI | ⑧MD活用 | ライセンス |
|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 1 | Microsoft AutoGen | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | ◎ | OSS |
| 2 | LangGraph | ◎ | ◎ | ○ | ◎ | ◎ | △ | ◎ | ◎ | OSS |
| 3 | MetaGPT | ○ | △ | ○ | ◎ | △ | △ | ○ | ◎ | OSS |
| 4 | CrewAI | ○ | ◎ | ○ | ◎ | ◎ | △ | ○ | ◎ | OSS |
| 5 | LangChain | △ | ◎ | ○ | ◎ | ◎ | △ | ◎ | ◎ | OSS |
| 6 | LlamaIndex | △ | ◎ | ○ | ◎ | ◎ | △ | ○ | ◎ | OSS |
| 7 | Temporal | × | × | △ | × | × | × | ◎ | × | OSS（商用サポートあり） |
| 8 | Argo Workflows / Airflow | × | × | △ | × | × | × | ◎ | × | OSS |
| 参考 | M365 Copilot Studio | ○ | × | ◎ | △ | ○ | ◎ | × | ○ | 商用（M365ライセンス必須） |

> **凡例** ◎ネイティブ対応 ○公式/主要プラグインあり △外部ライブラリ補完 ×別途実装が必要  
> 各フレームワークの選定根拠・スコア理由は [§1.4.3](#143-評価軸ごとの根拠) 参照  
> 「参考」行の M365 Copilot Studio は単独実装トラックではなく、AutoGen から `AzureAIAgent` 経由で呼ばれる **M365統合フロントエンド**として機能する。②MCP クライアント機能・⑦CLI・カスタム VectorDB 接続は非対応のため優先度付け対象外とした。

> **【④Doc生成 ◎ の共通根拠】**  
> 全 Python ベースフレームワーク（1〜6位）は `import subprocess; subprocess.run(["pandoc", "in.md", "-o", "out.docx"])` の1行で Pandoc を呼び出せる。Python が実行前提である以上、全フレームワークで ◎ となる（MetaGPT のみビルトイン doc 生成として ◎、他は Python subprocess 経由として同等の ◎）。

### 1.4.3 評価軸ごとの根拠

- **Microsoft AutoGen（1位）** — A2A Protocol（Google標準）への対応が進んでおり、AutoGen Studio・AutoGen Core等でマルチエージェント協調設計が充実。MCP対応は `autogen-ext` のMCPToolAdapterで実現し、Box/M365等の外部サービスにMCP Server経由で接続できる。GitHub Copilot との親和性が高く、MDをエージェント知識源として直接組み込める構成も組みやすく、CLI化はSDKでヘッドレス実行が可能。**M365 Copilot Studio（Agent Studio）で作成したエージェントとのA2A連携は、`autogen-ext` の `AzureAIAgent` クラスで Azure AI Agent Service 上の Copilot Studio エージェントを直接呼び出す方法が最もシームレス。Microsoft Agents SDK（A2A Protocol対応）経由での連携も同一エコシステム内で最小実装で実現できる。**
- **LangGraph（2位）** — グラフでA2Aワークフローを厳密に設計可能。**LangGraph は LangChain を依存として内包するため、`pip install langgraph` 一発で LangChain の DocLoader・チェーン・ツール類がすべて利用可能**。MCP対応は `langchain-mcp-adapters` でネイティブに実現し、MCP ServerとのBridge機能も提供。MDファイルをRAG知識として取り込み・BoxとのAPI連携・CLIでのワークフロー起動まで、LangGraph 単体で7軸（①〜⑤・⑦⑧）に対応できる（⑥M365 は △）。
- **MetaGPT（3位）** — 開発工程の自動化（仕様→コード→ドキュメント生成）に優れる。MDファイルをインプットとした自動化パイプラインが構築しやすく、Copilot併用で開発効率が向上。MCP対応はコミュニティプラグイン段階（△）のため、Box AI・M365の接続は追加実装が必要。
- **CrewAI（4位）** — 役割モデルでA2Aを直感的に組め、ローコードでPoC立上げが速い。MCP対応は `crewai-tools` の **MCPServerAdapter が公式サポート**（◎）で、LangGraph の `langchain-mcp-adapters` と同等レベル。**MDファイルは `Knowledge` クラスの `MDXKnowledgeSource` でネイティブにナレッジ指定でき**（◎）、エージェントが直接参照できる構成を最小実装で組める。①A2A は CrewAI Flows でエージェント間連携は可能だが Google A2A Protocol への公式準拠は未対応（○）。M365 Copilot 専用統合は別途検討が必要（△）。
- **LangChain（5位）** — LLMアプリ基盤として汎用性が高く、MCPは `langchain-mcp-adapters` でネイティブ対応（◎）。DocLoaderによるMD取り込みが標準的に用意されている。A2A協調ワークフローはLangGraph併用を推奨。CLIやバッチ実行に適する。
- **LlamaIndex（6位）** — ドキュメント索引・RAGに特化し、MCP対応は `llama-index-tools-mcp` でMCP Server接続が可能（◎）。MDファイルを最短でインデックス化・検索可能にできる。Pandocとの組合せで文書生成パイプラインも構築しやすい。A2A協調は外部フレームワーク補完が前提。
- **Temporal（7位）／Argo Workflows・Airflow（8位）** — 信頼性・運用基盤の強みはあるが、A2A対話・MCPネイティブ対応・Copilot/M365の直接統合・MDの直接活用はすべて外部エージェント層での補完が前提。CLIやスケジューリングは得意分野。

### 1.4.4 推奨フレームワークの動作要件

| 項目 | Microsoft AutoGen | LangGraph |
|---|---|---|
| **Python バージョン** | 3.10 以上 | 3.9 以上（3.11 推奨） |
| **コアインストール** | `pip install autogen-agentchat autogen-ext` | `pip install langgraph`（LangChain を内包） |
| **MCP 対応** | `pip install autogen-ext[mcp]` | `pip install langchain-mcp-adapters` |
| **Azure AI 連携** | `pip install autogen-ext[azure]` | `pip install langchain-openai` |
| **Box SDK** | `pip install box-sdk-gen` | `pip install box-sdk-gen` |
| **ドキュメント生成** | Pandoc（別途インストール・PATH設定） | Pandoc（別途インストール・PATH設定） |
| **LLM API** | OpenAI / Azure OpenAI（APIキー必須） | OpenAI / Azure OpenAI 他（LangChain 経由） |
| **OS** | Windows / macOS / Linux | Windows / macOS / Linux |
| **メモリ目安** | 8 GB RAM 以上推奨 | 8 GB RAM 以上推奨 |

> Pandoc のインストール：Windows は `winget install JohnMacFarlane.Pandoc`、macOS は `brew install pandoc`。  
> Box SDK は Box Enterprise 契約の AI 機能有効化が別途必要。

> **【動作環境の前提】**  
> AutoGen・LangGraph はどちらも **Pure Python ライブラリ** であり、Python 実行環境があればどこでも動く。  
>
> | 実行場所 | 可否 | 備考 |
> |---|:---:|---|
> | **ローカル PC（Windows / macOS / Linux）** | ○ | 本書の主な想定環境。`python main.py` で即起動 |
> | **VPS**（WebARENA・Sakura VPS・AWS EC2 等） | ○ | root 権限あり・Python インストール可・常駐プロセス起動可 |
> | **共有レンタルサーバー**（Xserver・Sakura レンサバ等の PHP 共有環境） | × | Python 任意パッケージ導入不可・常駐プロセス禁止が一般的 |
>
> 本書の手順はローカル PC での実行を前提として記述する。VPS 上でも同様の手順で動作するが、ポート設定・プロセス管理（systemd 等）は各環境に応じて対応すること。  
> フレームワーク本体はローカル完結で動作し、LLM 推論（OpenAI / Azure OpenAI）のみ外部 API 呼び出しとなる（**LLM API キー必須・従量課金発生**）。

## 1.5 技術要素（RAGコアレイヤー）

実装パイプラインで使用する主要技術要素を示す。

| 技術要素 | 役割 | 主な効果 |
|---|---|---|
| **GraphRAG** | 法令・基準間の関係をグラフ構造で保持 | 多段推論（2ホップ以上）の実現 |
| **VectorRAG** | 非構造化テキストの意味検索 | 類似事例・実務知識の高速参照 |
| **ドメインオントロジー** | 概念・用語の公式スキーマ定義 | 用語の一意化・推論ルールの基盤 |
| **CogGRAG** | 人間の思考プロセスを模倣した問題分解 | 複雑な問いへの構造化した推論 |

パイプライン配置順: **入力整形 → VectorRAG → GraphRAG → CogGRAG（複雑な問いのみ） → 統合・生成**

### 1.5.1 MDファイル・システムプロンプトによる簡易代替

フル実装が困難な初期段階では、各技術をMDファイルとシステムプロンプトで代替できる。対応範囲と限界を下表に示す。

| 技術（§3） | 簡易実装での代替 | 実現できること | 主な限界 |
|---|---|---|---|
| **GraphRAG** | `knowledge_map.md`（Mermaid図）| 3ホップ程度の関係追跡・事実抽出 | 動的グラフ走査・大規模ノード管理不可 |
| **VectorRAG** | `source_docs/`（MD群を直接RAGへ登録） | 意味的類似検索・メタデータフィルタ | Cross-Encoder再ランキング・数万件超は非対応 |
| **CogGRAG** | `system_prompt.md`（回答手順として明示） | 固定パターンの多段推論・手順強制 | 動的分解・並列検索・自動矛盾検出は不可 |
| **ドメインオントロジー** | `entity_dictionary.md`＋制約ルール | 用語正規化・明示した制約の遵守 | SHACL網羅検証・OWL自動推論は不可 |

> 簡易代替は Track A（PoC段階）での早期検証に有効。精度・スケールの限界に達した時点でフル実装（4章）へ移行する。

