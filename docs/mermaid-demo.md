---
title: Mermaid デモ
layout: default
---

以下は Mermaid のサンプルです。ページにレンダリングされると図になります。

```mermaid
graph LR
  A[Start] --> B{Is it OK?}
  B -->|Yes| C[Proceed]
  B -->|No| D[Fix]
  C --> E[Done]
  D --> B
```

（このファイルを編集して別の Mermaid 図を試してください。）
