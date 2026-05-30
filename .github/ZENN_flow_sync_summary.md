
# Zenn公開ワークフロー・同期手順まとめ（汎用版）

## 1. 全体フロー

1. **原稿・章構成の管理**
    - `docs/books/<slug>/` や `docs/プロジェクトCDE/` などでMarkdown原稿・画像・`config.yaml`（章リスト・タイトル・概要）を管理
    - 必要に応じてGitでバージョン管理
2. **Zenn用データへの同期（変換）**
    - `python scripts/prepare_zenn_book.py <src> <dst>` を実行
    - 例: `python scripts/prepare_zenn_book.py docs/books/rag-multiagent-build zenn/content/books/rag-multiagent-build`
    - スクリプトは `config.yaml` を読み、指定章のmdをコピーし、Zenn用 `index.md` を自動生成
3. **Zenn CLIでプレビュー・公開**
    - `npx zenn preview` でローカルプレビュー
    - `npx zenn login` でZennにログイン
    - `npx zenn publish` で公開
4. **公開後の確認**
    - Zenn上で表示・リンク・画像・目次などを必ず確認

---

## 2. 詳細手順

### 2.1. 必要な準備
- Node.js / npm（Zenn CLI用）
- Python 3.8+、`pip install pyyaml`

### 2.2. 仮想環境の作成（任意）
```bash
python -m venv .venv
.venv\Scripts\activate
pip install pyyaml
```

### 2.3. Zenn用コンテンツの同期
```bash
python scripts/prepare_zenn_book.py <src> <dst>
```
- `<src>`は原稿ディレクトリ、`<dst>`はZenn用ディレクトリ（例: `zenn/content/books/<slug>`）
- 変換後、`<dst>`配下にZenn形式のファイルが生成される

### 2.4. Zenn CLIでプレビュー・公開
```bash
npx zenn preview
npx zenn login
npx zenn publish
```

---

## 3. 注意点・補足
- 画像や外部リンクはZennの仕様に合わせてパスや形式を調整してください
- 変換スクリプトはfront matterや画像パスも自動調整しますが、公開前に内容・目次・リンク切れ等を必ず確認してください
- Zennのルール（front matter、画像サイズ、目次、リンク形式など）に従い、必要に応じて手動修正してください
- 公開にはZennアカウントが必要です
- 公開後はZenn上での表示・リンク・画像・目次などを再度確認してください

---

## 4. 参考
- [Zenn公式ドキュメント](https://zenn.dev/zenn/articles/zenn-cli-guide)
- [Zenn CLI GitHub](https://github.com/zenn-dev/zenn-cli)
