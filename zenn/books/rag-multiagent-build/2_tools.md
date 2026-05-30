---
title: "エージェントツール設計"
---

# 2. エージェントツール設計

> 本章では「各エージェントに持たせるツール」の全体構成を整理する。  
> RAG 検索だけでなく、**Pandoc 等による文書ファイル生成**も含めてツールセットを定義する。

## 2.1 ツールの種類と役割

```mermaid
flowchart TD
    subgraph Retrieve["検索・取得系ツール"]
        T1["VectorSearch\nナレッジベース意味検索"]
        T2["WebSearch\n最新法改正・通達を検索"]
        T3["FileRead\n指定文書の本文取得"]
    end
    subgraph Generate["生成・変換系ツール"]
        T4["DocumentWriter\n回答→Word/PDF生成\n(Pandoc / python-docx)"]
        T5["TemplateRenderer\n定型書類テンプレート差込"]
        T6["ExcelWriter\nチェックリスト・積算表生成"]
    end
    subgraph Validate["検証・計算系ツール"]
        T7["Calculator\n数量計算・積算"]
        T8["DateChecker\n法令施行日・有効期限確認"]
        T9["CrossReference\n複数文書の整合チェック"]
    end
    subgraph Notify["通知・連携系ツール"]
        T10["EmailNotify\n完了通知・承認依頼"]
        T11["SharePointUpload\n生成文書のアップロード"]
        T12["BacklogPost\nBacklogチケット起票"]
    end
```

## 2.2 エージェント別ツール割り当て

| エージェント | 必須ツール | 推奨追加ツール |
|---|---|---|
| **オーケストレーター** | なし（ルーティングのみ） | DateChecker（法改正時期確認） |
| **法令エージェント** | VectorSearch（kb-law系） | WebSearch（最新改正確認）/ CrossReference |
| **行政手続エージェント** | VectorSearch（kb-procedure） | TemplateRenderer（申請書雛形） |
| **技術基準エージェント** | VectorSearch（kb-technical） | Calculator（数量計算）/ FileRead |
| **事例エージェント** | VectorSearch（kb-cases） | FileRead（報告書全文取得） |
| **リスクエージェント** | VectorSearch（kb-risk系） | CrossReference |
| **監理エージェント** | CrossReference | なし（検索ツールは持たせない） |
| **回答統合エージェント** | DocumentWriter | TemplateRenderer / ExcelWriter |

---

## 2.3 DocumentWriter（Pandoc 連携）

### 2.3.1 Pandoc が解決すること

本システムの最終出力は **Markdown 形式の構造化回答**だが、実務では以下の形式が必要になる。

| 出力形式 | 用途 | Pandoc コマンド |
|---|---|---|
| Word (.docx) | 決裁文書・報告書 | `pandoc -o output.docx --reference-doc=template.docx` |
| PDF | 印刷・保管 | `pandoc -o output.pdf --pdf-engine=lualatex` |
