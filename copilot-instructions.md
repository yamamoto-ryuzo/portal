# Zenn公開ワークフロー・同期手順まとめ（汎用版）

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