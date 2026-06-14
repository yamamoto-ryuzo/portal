---
title: "システム構成と公開・運用アーキテクチャ"
---

# 第6章 システム構成と公開・運用アーキテクチャ

## 6.1 概要

本書で構築する AutoGen アプリは **Azure Container Apps + Microsoft Entra ID（旧 Azure AD）** の組み合わせで、  
**インターネット経由・VPN不要・組織アカウント限定**での公開が可能である。

```
社外ネットワーク（自宅・出先・スマホ等）
  │
  │ HTTPS
  ▼
Azure Container Apps
  ├─ Easy Auth（組み込み認証）
  │    └─ Microsoftログイン画面にリダイレクト
  │         └─ Microsoft Entra ID で認証
  │              ├─ 認証成功 → AutoGen アプリへ到達 ✅
  │              └─ 認証失敗（未ログイン・別テナント） → 403 ❌
  │
  └─ AutoGen API（FastAPI / AutoGen Studio）
       └─ Azure OpenAI / OpenAI API（LLM推論）
```

## 6.2 構成コンポーネント

| コンポーネント | 役割 | 備考 |
|---|---|---|
| **Azure Container Apps** | AutoGen アプリのホスティング | スケールアウト対応・HTTPS自動付与 |
| **Azure Container Registry（ACR）** | Dockerイメージの保管 | Container Apps と同一RGに配置推奨 |
| **Microsoft Entra ID** | ユーザー認証・アクセス制御 | M365テナントをそのまま流用可 |
| **Easy Auth（組み込み認証）** | Entra ID との認証連携 | アプリコード変更不要 |
| **Azure OpenAI Service** | LLM推論エンドポイント | APIキー管理はKey Vault推奨 |

## 6.3 アクセス制御の粒度

| レベル | 設定箇所 | 効果 |
|---|---|---|
| **テナント全体（社員全員）** | Entra ID アプリ登録 → アカウント種別を「単一テナント」 | 組織メンバー全員がアクセス可 |
| **特定グループのみ** | エンタープライズアプリ → 「割り当て必須」ON → グループ追加 | 指定グループ外は弾く |
| **ロールベース（閲覧/管理）** | アプリロールを定義 → RBAC で割り当て | 権限レベルで機能を分岐 |

## 6.4 デプロイ手順（概要）

```bash
# 1. コンテナイメージをビルドして ACR へプッシュ
az acr build --registry <ACR名> --image myautogen:latest .

# 2. Container Apps を作成（外部公開・ポート8000）
az containerapp create \
  --name my-autogen-app \
  --resource-group <RG名> \
  --image <ACR名>.azurecr.io/myautogen:latest \
  --ingress external --target-port 8000

# 3. Entra ID 認証（Easy Auth）を有効化
az containerapp auth microsoft update \
  --name my-autogen-app \
  --resource-group <RG名> \
  --client-id <アプリ登録のクライアントID> \
  --client-secret <シークレット> \
  --tenant-id <テナントID>
```

> **前提条件**  
> - Azure サブスクリプションと M365（Entra ID）テナントが紐づいていること  
> - Azure CLI がインストール済みで `az login` 済みであること  
> - Entra ID でアプリ登録（App Registration）を事前に作成し、クライアントIDとシークレットを取得していること

## 6.5 開発・運用サイクル

本書の想定する開発から運用までのライフサイクルを以下に示す。

```
【開発】ローカル PC（デスクトップ）
  ├─ python main.py でエージェント動作確認
  ├─ プロンプト・ナレッジ・ツール設定を修正
  └─ git commit / git push → GitHub リポジトリ
          │
          │ CI/CD（GitHub Actions 等）
          ▼
【ビルド】Docker コンテナ化
  └─ az acr build → Azure Container Registry にイメージ登録
          │
          ▼
【公開】Azure Container Apps
  ├─ Entra ID 認証で組織内ユーザーに限定公開
  ├─ HTTPS エンドポイントを共有 → チームが利用開始
  └─ ログ・メトリクスを Azure Monitor で確認
          │
          │ 改善サイクル
          ▼
【改善】ローカルで修正 → push → 自動ビルド・再デプロイ
```

| フェーズ | 環境 | 主な作業 | 担当者 |
|---|---|---|---|
| **開発** | ローカル PC | エージェント実装・プロンプト調整・単体テスト | バックエンドエンジニア |
| **PoC公開** | Azure Container Apps | チームへの共有・受入テスト実施 | AI導入担当者 |
| **本番移行** | Azure Container Apps | アクセス制御・監視設定・SLA策定 | 運用担当者 |
| **継続改善** | ローカル → Azure | KPIモニタリング・精度改善・新機能追加 | 全担当者 |

> **ローカルと Azure の環境差異を最小化するポイント**  
> - 環境変数（APIキー・エンドポイント）は `.env` ファイルと Azure の「シークレット」で統一管理  
> - `requirements.txt` でライブラリバージョンを固定し、ローカルと Docker イメージを同一にする  
> - `docker run` でローカルからもコンテナ動作を検証できる構成にすることで、「ローカルでは動くがAzureで動かない」を防ぐ

## 6.6 Azure Container Apps で動かせるアプリの範囲

Azure Container Apps は **「Dockerコンテナが動く場所」** であり、AutoGen に限らずコンテナ化できるアプリであれば言語・フレームワークを問わず動作する。

| アプリ種別 | 動作 | 備考 |
|---|:---:|---|
| AutoGen（本書のメイン） | ✅ | ヘッドレス実行・FastAPI経由でWebUI公開 |
| FastAPI / Flask / Django | ✅ | WebサーバーとしてHTTPS公開 |
| LangGraph / CrewAI 等 | ✅ | 本書の他フレームワークも同様にデプロイ可 |
| Node.js / Go / Java 等 | ✅ | 言語不問・Dockerfile があれば動く |
| AutoGen Studio（Web UI） | ✅ | `autogenstudio ui` をコンテナ化して公開 |
| GUIアプリ（tkinter 等） | ❌ | サーバー側に画面がないため不可 |
| `C:\Users\...` 依存の処理 | ❌ | Windowsローカルパスはコンテナ内に存在しない |
| Windows専用DLL依存アプリ | ❌ | コンテナはLinuxベースが標準のため |

> **結論：「ヘッドレス（画面なし）で動くPythonアプリ」はそのままAzureへ持っていける。**  
> デスクトップで `python main.py` が動く構成であれば、`Dockerfile` を1枚追加するだけで Azure Container Apps にデプロイできる。

## 6.7 Docker を使わない場合の代替サービス

`Dockerfile` を書かずに Python アプリを Azure で公開したい場合は、**Azure App Service** が最も手軽な選択肢となる。

| サービス | Docker不要 | 向いているケース | Entra ID認証 |
|---|:---:|---|:---:|
| **Azure App Service** | ✅ | WebアプリをZIPまたはGitで直接デプロイ | ✅（Easy Auth） |
| **Azure Functions** | ✅ | イベント駆動・バッチ処理・API単体公開 | ✅ |
| **Azure Container Apps** | ❌（要Docker） | コンテナ化済みアプリの本番運用 | ✅（Easy Auth） |

**Azure App Service でのデプロイ（Docker不要）:**

```bash
# requirements.txt と main.py があればそのままデプロイできる
az webapp up \
  --name my-autogen-app \
  --resource-group <RG名> \
  --runtime "PYTHON:3.11" \
  --sku B1
```

> **App Service の制約**  
> - 常駐プロセス（長時間実行エージェント）は `B1` 以上のプランが必要  
> - AutoGen のような非同期・長時間タスクは **タイムアウト設定（230秒制限）** に注意  
> - 長時間実行が必要な場合は Azure Container Apps または Azure Functions（Durable Functions）を推奨

## 6.8 Windows EXE（コマンドライン）をAzureで動かす方法

デスクトップで動く `.exe` ファイルをAzure上で実行し、結果を取得したい場合の選択肢を示す。

| 方法 | 概要 | 向いているケース |
|---|---|---|
| **① App Service（Windowsプラン）+ subprocess** | Python から `subprocess.run("tool.exe")` で呼び出す。EXEをアプリと一緒にデプロイ | Webトリガーで単発実行・結果をAPIで返す |
| **② Azure VM（Windows）** | WindowsのVMをそのまま立ててEXEを常駐 | 既存の複雑なEXE・DLL依存・GUI補助ツール |
| **③ Azure Batch** | 大量ジョブをバッチ実行し結果をストレージに保存 | 定期バッチ・並列処理・大量ファイル変換 |
| **④ ローカル実行＋結果アップロード** | EXEはデスクトップで動かし、結果ファイルだけAzureに送る | EXEの移植が難しい場合の最小構成 |

**① App Service（Windowsプラン）でのEXE呼び出し例（Python）:**

```python
import subprocess
from fastapi import FastAPI

app = FastAPI()

@app.post("/run")
def run_tool(input: str):
    result = subprocess.run(
        ["mytool.exe", "--input", input],
        capture_output=True, text=True, timeout=60
    )
    return {"stdout": result.stdout, "returncode": result.returncode}
```

```bash
# Windows プランで App Service を作成（EXEが動くWindows環境）
az webapp up \
  --name my-tool-app \
  --resource-group <RG名> \
  --runtime "PYTHON:3.11" \
  --os-type Windows \
  --sku B1
```

**④ ローカル実行＋結果アップロード（最小構成）:**

```python
import subprocess, json
from azure.storage.blob import BlobServiceClient

# EXE をローカルで実行
result = subprocess.run(["mytool.exe", "--input", "data.csv"],
                        capture_output=True, text=True)

# 結果を Azure Blob Storage にアップロード
client = BlobServiceClient.from_connection_string("<接続文字列>")
client.get_blob_client("results", "output.json").upload_blob(
    json.dumps({"output": result.stdout}), overwrite=True
)
```

> **EXEをAzureで動かす際の注意点**  
> - Linux系（Container Apps / App Service Linux）では `.exe` は動かない → **Windows プランまたはVM必須**  
> - EXEが他のDLLや外部ツールに依存する場合は、依存ファイルも一緒にデプロイすること  
> - Entra ID 認証は方法①②③いずれでも Easy Auth または Azure AD で設定可能

## 6.9 Azure VM ベースの AutoGen 公開構成（推奨構成）

**Azure VM + Azure AD Application Proxy** の組み合わせは、  
Docker不要・EXEも動く・Entra ID認証付き という3条件を満たす構成として実用性が高い。

```
インターネット上のユーザー
  │ HTTPS
  ▼
Microsoft Entra ID（認証）
  │ 認証成功後
  ▼
Azure AD Application Proxy（中継・Entra ID認証ゲートウェイ）
  │ 内部転送（VMに公開IPなし）
  ▼
Azure VM（Windows / Linux）
  ├─ AutoGen API（FastAPI: python main.py）
  ├─ AutoGen Studio（autogenstudio ui）
  └─ Windows EXE ツール群（必要に応じて subprocess で呼び出し）
       └─ Azure OpenAI API（LLM推論）
```

**この構成の利点:**

| 項目 | 内容 |
|---|---|
| **Docker不要** | VMに直接 Python + AutoGen をインストール |
| **Windows EXE対応** | VM上でそのまま `.exe` が動く |
| **公開IPなし** | VMにパブリックIPを付けずに済む（セキュリティ高） |
| **Entra ID認証** | Application Proxy が認証ゲートウェイとして機能 |
| **VPN不要** | インターネットからEntra IDでアクセス可能 |

**セットアップ手順（概要）:**

```bash
# ① Azure VM を作成（Linux推奨・Windowsも可）
az vm create \
  --name autogen-vm \
  --resource-group <RG名> \
  --image Ubuntu2204 \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys

# ② VM上にAutoGenをインストール（SSHで接続後）
pip install autogen-agentchat autogen-ext fastapi uvicorn

# ③ AutoGen APIをサービスとして起動（systemd）
# /etc/systemd/system/autogen.service に登録して常駐化
uvicorn main:app --host 127.0.0.1 --port 8000

# ④ Azure AD Application Proxy コネクタをVM上にインストール
#    → Azure Portal: Entra ID > アプリケーション プロキシ > コネクタのダウンロード
#    → コネクタがVM内からAzureへのアウトバウンド接続を確立（インバウンド開放不要）

# ⑤ Application Proxy でアプリを公開
#    → Azure Portal: Entra ID > エンタープライズアプリケーション > 新しいアプリ
#    → 内部URL: http://127.0.0.1:8000
#    → 外部URL: https://autogen-app.msappproxy.net（自動発行）
#    → 事前認証: Microsoft Entra ID
```

> **Application Proxy の動作原理**  
> VMからAzureへのアウトバウンド接続（ポート80/443）のみで動作するため、  
> **VMのNSGでインバウンドを完全に閉じたまま**インターネット公開できる。  
> これはContainer Appsのインバウンド公開より安全な構成となる。

> **運用コスト目安（2026年時点）**  
> Standard_B2s（2vCPU/4GB）: 約 ¥6,000〜8,000／月  
> Application Proxy: Entra ID P1 ライセンスが必要（M365 Business Premium に含まれる場合あり）

## 6.10 閉鎖環境（オンプレミス・LAN内）でのOSSマルチエージェント構築

クラウド（Azure OpenAIなど）を利用せず、情報漏洩リスクを極限まで排除したい要件（行政、インフラ、防衛、機密R&Dなど）においては、外部インターネットと通信しない**完全閉鎖のLAN環境（オンプレミス）**での構築が求められる。

近年、Llama 3系やQwen、国内のELYZAなどのオープンソースLLM（OSS LLM）の性能が飛躍的に向上したこと、およびOllamaやvLLMなどの推論エンジンの進化により、閉鎖環境でも実用的なRAG・マルチエージェントシステムを構築することが十分に可能となっている。

### 6.10.1 閉鎖環境における技術スタック（クラウドとの対比）

クラウド依存のサービスを、ローカルで動作するOSSソフトウェアに置き換える。

| 役割 | クラウド構成（参考） | 閉鎖環境（オンプレミス）での推奨スタック | 備考 |
|---|---|---|---|
| **推論エンジン（API）** | Azure OpenAI | **Ollama** または **vLLM** | Ollamaは導入とモデル管理が容易。vLLMは複数同時リクエストの高速処理（本番運用向け）と、**後述するMulti-LoRA（複数LoRAの同時運用）**に優れる。どちらもOpenAI互換APIを提供するため、AutoGen等のコード変更を最小限に抑えられる。 |
| **LLMモデル（生成用）** | GPT-4o / Claude 3.5 | **Llama 3.1**, **Qwen 2.5**, **ELYZA** 等 | ハードウェア（VRAM容量）に合わせて、軽量な8Bクラスから高精度な70Bクラスまで選択する。 |
| **埋め込みモデル（検索用）** | text-embedding-3 | **multilingual-e5-large**, **BGE-M3** 等 | 日本語に強いOSSの埋め込みモデルをローカルで動かし、ベクトル化を行う。 |
| **ベクトルDB** | Azure AI Search | **Qdrant**, **Chroma**, **Milvus** | いずれもDockerコンテナとしてローカル環境にデプロイ可能。完全オフラインで動作する。 |
| **オーケストレーター** | Azure AI Foundry等 | **Dify (セルフホスト版)** または **AutoGen / LangGraph** | DifyはDocker Composeで社内サーバーに展開可。AutoGen/LangGraphはローカルのPython環境でそのまま動作する。 |
| **UI（フロントエンド）** | Copilot Studio等 | **Open WebUI** または **Dify標準UI** | Open WebUIはOllamaとの親和性が非常に高く、ChatGPTライクなUIを社内に提供できる。 |

### 6.10.2 代表的な2つの構築パターン

**パターンA：ローコード・早期展開（Difyセルフホスト）**
- **構成:** Dify (Docker) ＋ Ollama ＋ ローカルLLM
- **特徴:** DifyのGUIを用いて、RAGのナレッジ登録やエージェントフローを直感的に構築できる。すべてのコンポーネントがDockerコンテナ内で完結するため、必要なDockerイメージとモデルファイル（`.gguf`等）をLAN内に持ち込めば、完全にオフラインで動作する。

**パターンB：高度なマルチエージェント開発（Pythonコードベース）**
- **構成:** AutoGen / LangGraph ＋ vLLM (OpenAI互換API) ＋ Qdrant (ベクトルDB)
- **特徴:** エンジニアがコードで厳密なマルチエージェントを制御する。vLLMが「ローカルのOpenAI APIサーバー」として振る舞うため、AutoGen側のコードはクラウドを使う場合とほぼ同じ（エンドポイントURLを `http://localhost:8000/v1` のように変更するだけ）で機能する。

### 6.10.3 閉鎖環境構築におけるハードルと運用上の注意点

1. **ハードウェア（GPU）の調達とサイジング**
   高度な推論を実用的な速度で行うには、GPUを搭載したローカルサーバーが必須となる。
   - **8Bクラス（軽量・高速）:** VRAM 16GB〜24GB（RTX 4090等のコンシューマGPUでも可）
   - **70Bクラス（高精度・複雑な推論）:** VRAM 80GB以上（NVIDIA A100/H100や、複数GPUの連結が必要）
   マルチエージェント環境では複数モデルを同時に動かす、あるいは大量のコンテキスト（RAGソース）を入力するため、VRAMの余裕を持ったサイジングが重要である。

2. **オフライン環境への「データ移送」（エアギャップ対策）**
   外部と遮断されているため、構築やアップデートのたびに以下のデータをインターネット接続環境でダウンロードし、セキュアな手段（暗号化USBメモリ等）で閉鎖環境へ物理的に移送する作業が発生する。
   - ソフトウェアのインストールパッケージ（Dockerイメージ、Pythonの `pip` パッケージ一式 `*.whl`）
   - LLMモデルのファイル（`.gguf` や `.safetensors`）
   - ※依存関係のあるライブラリを全てオフラインでインストールするためのリポジトリミラーリング等、インフラ運用面の工夫が必要となる。