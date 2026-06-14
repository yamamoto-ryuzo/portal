import re

# Format Chapter 1
ch1 = open('books/rag-multiagent-build/1_overview.md', 'r', encoding='utf-8').read()
ch1 = re.sub(r'^# 本書が解決すること', r'# 第1章 本書の目的と実装トラック\n\n## 1.1 本書が解決すること', ch1, flags=re.MULTILINE)
ch1 = re.sub(r'^# 対象読者', r'## 1.2 対象読者', ch1, flags=re.MULTILINE)
ch1 = re.sub(r'^# 前提知識', r'## 1.3 前提知識', ch1, flags=re.MULTILINE)
ch1 = re.sub(r'^# 本書で扱う実装トラック', r'## 1.4 本書で扱う実装トラック', ch1, flags=re.MULTILINE)
ch1 = re.sub(r'^## 1\.1 フレームワーク', r'### 1.4.1 フレームワーク', ch1, flags=re.MULTILINE)
ch1 = re.sub(r'^## 1\.2 推奨フレームワーク', r'### 1.4.2 推奨フレームワーク', ch1, flags=re.MULTILINE)
ch1 = re.sub(r'^## 1\.3 評価軸ごとの', r'### 1.4.3 評価軸ごとの', ch1, flags=re.MULTILINE)
ch1 = re.sub(r'^## 1\.4 推奨フレームワークの動作', r'### 1.4.4 推奨フレームワークの動作', ch1, flags=re.MULTILINE)
ch1 = re.sub(r'^# 本書の構成', r'## 1.5 本書の構成', ch1, flags=re.MULTILINE)
open('books/rag-multiagent-build/1_overview.md', 'w', encoding='utf-8').write(ch1)

# Format Chapter 2
ch2 = open('books/rag-multiagent-build/2_ssot_strategy.md', 'r', encoding='utf-8').read()
ch2 = re.sub(r'^# 第2章 RAGの基本理論とSSOT（Single Source of Truth）戦略', r'# 第2章 RAGの基本理論とSSOT戦略', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## 学習データ・ファインチューニング・RAGの違い', r'## 2.1 学習データ・ファインチューニング・RAGの違い', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## 2\.1 RAG拡張による回答品質の向上', r'## 2.2 RAG拡張による回答品質の向上', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## 要旨（先に結論）', r'## 2.3 要旨（先に結論）', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## 本章で使う基本用語', r'## 2.4 本章で使う基本用語', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## 関連モデルとのコンテキスト長比較', r'## 2.5 関連モデルとのコンテキスト長比較', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## 背景と目的', r'## 2.6 背景と目的', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## コンテキスト予算の判定式', r'## 2.7 コンテキスト予算の判定式', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## 影響と設計パターン', r'## 2.8 影響と設計パターン', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## ワークフロー', r'## 2.9 ワークフロー', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## チェックリスト', r'## 2.10 チェックリスト', ch2, flags=re.MULTILINE)
ch2 = re.sub(r'^## 付録:', r'## 2.11 付録:', ch2, flags=re.MULTILINE)
open('books/rag-multiagent-build/2_ssot_strategy.md', 'w', encoding='utf-8').write(ch2)

# Format Chapter 3
ch3 = open('books/rag-multiagent-build/3_search_technology.md', 'r', encoding='utf-8').read()
ch3 = re.sub(r'^## なぜ今、高度な検索フローが必要なのか', r'## 3.1 なぜ今、高度な検索フローが必要なのか', ch3, flags=re.MULTILINE)
ch3 = re.sub(r'^## 実装の現実解：既存APIを「最高の資産」とする', r'## 3.2 実装の現実解：既存APIを「最高の資産」とする', ch3, flags=re.MULTILINE)
ch3 = re.sub(r'^## 最高の資産からSSOTを抽出する高度な技術要素', r'## 3.3 最高の資産からSSOTを抽出する高度な技術要素', ch3, flags=re.MULTILINE)
ch3 = re.sub(r'^## SSOT抽出の高度化フロー（API連携の4ステップ）', r'## 3.4 SSOT抽出の高度化フロー（API連携の4ステップ）', ch3, flags=re.MULTILINE)
ch3 = re.sub(r'^## まとめ：検索設計がRAGの品質を決める', r'## 3.5 まとめ：検索設計がRAGの品質を決める', ch3, flags=re.MULTILINE)
ch3 = re.sub(r'^## RAGの限界と次なる展開：その場限りの知識から「背景知識」への転換', r'## 3.6 RAGの限界と次なる展開', ch3, flags=re.MULTILINE)
ch3 = re.sub(r'^## RAG資産を活用した「背景知識」学習への移行戦略', r'## 3.7 RAG資産を活用した「背景知識」学習への移行戦略', ch3, flags=re.MULTILINE)
# Fix the existing headers moved from ch1
ch3 = re.sub(r'^## 3\.1 技術要素', r'### 3.3.1 技術要素', ch3, flags=re.MULTILINE)
ch3 = re.sub(r'^## 3\.1\.1', r'#### 3.3.1.1', ch3, flags=re.MULTILINE)
ch3 = re.sub(r'^## 3\.2 RAGパイプライン機能', r'### 3.4.1 RAGパイプライン機能', ch3, flags=re.MULTILINE)
ch3 = re.sub(r'^## 3\.2\.1', r'#### 3.4.1.1', ch3, flags=re.MULTILINE)
open('books/rag-multiagent-build/3_search_technology.md', 'w', encoding='utf-8').write(ch3)

# Format Chapter 4
ch4 = open('books/rag-multiagent-build/4_multiagent_architecture.md', 'r', encoding='utf-8').read()
ch4 = re.sub(r'^## 1\. なぜ', r'## 4.1 なぜ', ch4, flags=re.MULTILINE)
ch4 = re.sub(r'^## 2\. マルチエージェント・アーキテクチャ', r'## 4.2 マルチエージェント・アーキテクチャ', ch4, flags=re.MULTILINE)
ch4 = re.sub(r'^## 3\. RAGとLoRAを組み込んだ', r'## 4.3 RAGとLoRAを組み込んだ', ch4, flags=re.MULTILINE)
ch4 = re.sub(r'^## 4\. マルチエージェント実装のための', r'## 4.4 マルチエージェント実装のための', ch4, flags=re.MULTILINE)
ch4 = re.sub(r'^## まとめ：個の専門性と', r'## 4.5 まとめ：個の専門性と', ch4, flags=re.MULTILINE)
open('books/rag-multiagent-build/4_multiagent_architecture.md', 'w', encoding='utf-8').write(ch4)

# Format Chapter 5
ch5 = open('books/rag-multiagent-build/5_lora_system_architecture.md', 'r', encoding='utf-8').read()
ch5 = re.sub(r'^## 1\. LoRA実装の全体', r'## 5.1 LoRA実装の全体', ch5, flags=re.MULTILINE)
ch5 = re.sub(r'^## 2\. 各構成要素の役割', r'## 5.2 各構成要素の役割', ch5, flags=re.MULTILINE)
ch5 = re.sub(r'^## 3\. RAGからLoRAへの継続的', r'## 5.3 RAGからLoRAへの継続的', ch5, flags=re.MULTILINE)
ch5 = re.sub(r'^## まとめ：LoRAインフラ', r'## 5.4 まとめ：LoRAインフラ', ch5, flags=re.MULTILINE)
open('books/rag-multiagent-build/5_lora_system_architecture.md', 'w', encoding='utf-8').write(ch5)

print("Formatting applied.")
