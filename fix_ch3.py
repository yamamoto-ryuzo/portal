import re

with open('books/rag-multiagent-build/3_search_technology.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's fix the numbering.
# What I want is:
# ## 3.1 技術要素（RAGコアレイヤー）
# ### 3.1.1 MDファイル・システムプロンプトによる簡易代替
# ## 3.2 RAGパイプライン機能を持つシステム一覧
# ### 3.2.1 選定の考え方
# ## 3.3 なぜ今、高度な検索フローが必要なのか
# ## 3.4 実装の現実解：既存APIを「最高の資産」とする
# ## 3.5 最高の資産からSSOTを抽出する高度な技術要素
# ## 3.6 SSOT抽出の高度化フロー（API連携の4ステップ）
# ### 3.6.1 意図分解と用語の正規化（CogGRAG × ドメインオントロジー）
# ### 3.6.2 広域検索と類似事例の取得（検索API × VectorRAG）
# ### 3.6.3 関係性の探索と文脈の補完（GraphRAG）
# ### 3.6.4 最終選定（リランキング）とLLMへの注入
# ## 3.7 まとめ：検索設計がRAGの品質を決める
# ## 3.8 RAGの限界と次なる展開：その場限りの知識から「背景知識」への転換
# ### 3.8.1 LoRA (Low-Rank Adaptation) / PEFTによる知識の焼き付け
# ### 3.8.2 RAFT (Retrieval Augmented Fine Tuning)
# ### 3.8.3 Continuous Pre-training (継続的事前学習)
# ### 3.8.4 擬似的な背景化：Prompt Caching (コンテキストキャッシュ)
# ## 3.9 RAG資産を活用した「背景知識」学習への移行戦略
# ### 3.9.1 GraphRAGの「関係性」を推論データに変換（関係性の背景化）
# ### 3.9.2 ドメインオントロジーを「基礎語彙」として学習（用語の背景化）
# ### 3.9.3 CogGRAGの「思考プロセス」をChain-of-Thoughtデータへ転用（推論の背景化）
# ### 3.9.4 VectorRAGの「検索・選択ログ」を用いた嗜好学習（価値観の背景化）
# ### 3.9.5 次のステップへ：LoRAによる「個の強化」から「マルチエージェント」の組織化へ

text = text.replace('### 3.3.1 技術要素', '## 3.1 技術要素')
text = text.replace('#### 3.3.1.1', '### 3.1.1')
text = text.replace('### 3.4.1 RAGパイプライン機能', '## 3.2 RAGパイプライン機能')
text = text.replace('#### 3.4.1.1', '### 3.2.1')
text = text.replace('## 3.1 なぜ今', '## 3.3 なぜ今')
text = text.replace('## 3.2 実装の現実解', '## 3.4 実装の現実解')
text = text.replace('## 3.3 最高の資産', '## 3.5 最高の資産')
text = text.replace('## 3.4 SSOT抽出', '## 3.6 SSOT抽出')

text = text.replace('### 1. 意図分解と', '### 3.6.1 意図分解と')
text = text.replace('### 2. 広域検索と', '### 3.6.2 広域検索と')
text = text.replace('### 3. 関係性の探索と', '### 3.6.3 関係性の探索と')
text = text.replace('### 4. 最終選定（', '### 3.6.4 最終選定（')

text = text.replace('## 3.5 まとめ：', '## 3.7 まとめ：')
text = text.replace('## 3.6 RAGの限界と', '## 3.8 RAGの限界と')

text = text.replace('### 1. LoRA (Low-Rank', '### 3.8.1 LoRA (Low-Rank')
text = text.replace('### 2. RAFT (Retrieval', '### 3.8.2 RAFT (Retrieval')
text = text.replace('### 3. Continuous Pre-training', '### 3.8.3 Continuous Pre-training')
text = text.replace('### 4. 擬似的な背景化：', '### 3.8.4 擬似的な背景化：')

text = text.replace('## 3.7 RAG資産を', '## 3.9 RAG資産を')

text = text.replace('### 1. GraphRAGの「', '### 3.9.1 GraphRAGの「')
text = text.replace('### 2. ドメインオントロジーを', '### 3.9.2 ドメインオントロジーを')
text = text.replace('### 3. CogGRAGの「', '### 3.9.3 CogGRAGの「')
text = text.replace('### 4. VectorRAGの「', '### 3.9.4 VectorRAGの「')
text = text.replace('### 次のステップへ：', '### 3.9.5 次のステップへ：')

with open('books/rag-multiagent-build/3_search_technology.md', 'w', encoding='utf-8') as f:
    f.write(text)
