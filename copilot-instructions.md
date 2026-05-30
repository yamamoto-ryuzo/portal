# Zenn公開ワークフロー・同期手順まとめ（最新版）

1. **原稿・章構成の管理**
    - `docs/books/<slug>/` や `docs/Project_CDE/` などでMarkdown原稿・画像・`config.yaml`（章リスト・タイトル・概要）を管理
    - 必要に応じてGitでバージョン管理
2. **Zenn用データへの同期（変換）**
    - `python scripts/prepare_zenn_book.py <src> <dst>` を実行
    - 例: `python scripts/prepare_zenn_book.py docs/books/rag-multiagent-build zenn/content/books/rag-multiagent-build`
    - スクリプトは `config.yaml` を読み、指定章のmdをコピーし、Zenn用 `index.md` を自動生成
    - `docs/RAG_System/INDEX.md` を編集した場合は `python scripts/sync_rag_summary.py` を実行し、`articles/rag-multiagent-guide-summary.md` を自動同期
3. **Zenn公式ディレクトリへの移動**
    - 記事: `articles/`
    - ブック: `books/`
    - 必要に応じて `xcopy` やエクスプローラーで移動
4. **Zenn CLIでプレビュー・公開**
    - `npx zenn preview` でローカルプレビュー
    - `npx zenn login` でZennにログイン
    - `npx zenn publish` で公開
5. **公開後の確認**
    - Zenn上で表示・リンク・画像・目次などを必ず確認