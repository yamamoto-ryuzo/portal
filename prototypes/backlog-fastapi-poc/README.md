バックログ起点 PoC: Backlog → FastAPI（Webhook）→ キュー → ワーカー

目的
- Backlog 等のタスク完了をトリガとして Webhook を受け、外部 API ワーカー（FastAPI）で実処理をキュー化する PoC。

構成
- `main.py`: FastAPI アプリ。`/webhook` で受信し、署名検証後 Redis に enqueue（無ければファイルに追記）。
- `requirements.txt`: 依存ライブラリ
- `flow.mmd`: 簡易フロー図（Mermaid）

クイックスタート（ローカル）
1. 仮想環境を作成・有効化

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS/Linux
```

2. 依存をインストール

```bash
pip install -r requirements.txt
```

3. 環境変数を設定（簡易）

```bash
set BACKLOG_SECRET=your-secret   # Windows
export BACKLOG_SECRET=your-secret
```

4. サーバ起動

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. Backlog の Webhook 宛先に `http://<host>:8000/webhook` を指定し、署名ヘッダ `X-Backlog-Signature`（HMAC-SHA256）を付与して送信する。署名の検算には `BACKLOG_SECRET` を使用。

注意点
- 実運用では `BACKLOG_SECRET` を Vault 等で安全に管理してください。
- Redis を使う場合は `REDIS_URL` 環境変数を設定してください。
- 署名検証、冪等性、監査ログの永続化、再試行ポリシーを実装してください。
