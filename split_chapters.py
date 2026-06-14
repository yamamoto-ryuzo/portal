import re
import os

with open('books/rag-multiagent-build/1_overview.md', 'r', encoding='utf-8') as f:
    overview_content = f.read()

def extract_section(text, start_marker, end_marker=None):
    if end_marker:
        pattern = f"({start_marker}.*?)(?={end_marker})"
    else:
        pattern = f"({start_marker}.*)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else ""

# Extract sections
sec_learning = extract_section(overview_content, r"## 学習データ・ファインチューニング・RAGの違い\n", r"# 対象読者\n")
sec_tech = extract_section(overview_content, r"# 技術要素（RAGコアレイヤー）\n", r"# システム構成（公開・認証アーキテクチャ）\n")
sec_infra = extract_section(overview_content, r"# システム構成（公開・認証アーキテクチャ）\n", r"## 1.7 RAGパイプライン機能を持つシステム一覧\n")

sec_pipeline_all = extract_section(overview_content, r"## 1.7 RAGパイプライン機能を持つシステム一覧\n", None)
sec_pipeline_systems = extract_section(sec_pipeline_all, r"## 1.7 RAGパイプライン機能を持つシステム一覧\n", r"### 1.7.2 RAG拡張による回答品質の向上\n")
sec_rag_quality = extract_section(sec_pipeline_all, r"### 1.7.2 RAG拡張による回答品質の向上\n", None)

# Update Chapter 1
new_ch1 = extract_section(overview_content, r"# 本書が解決すること\n", r"## 学習データ・ファインチューニング・RAGの違い\n")
ch1_part2 = extract_section(overview_content, r"# 対象読者\n", r"# 技術要素（RAGコアレイヤー）\n")

roadmap = """
# 本書の構成（ロードマップ）

本書は以下のステップでRAGマルチエージェントシステムの構築・運用手法を解説します。

*   **第1章：本書が解決すること・実装トラック（本章）**
    *   目的と対象読者、フレームワーク選定の結論
*   **第2章：RAGの基本理論とSSOT戦略**
    *   RAGとファインチューニングの役割分担、回答品質の向上、コンテキストの制約とSSOT（唯一の正しい情報源）設計
*   **第3章：既存APIを活用したSSOT抽出フローの設計**
    *   RAGコア技術要素、検索システム一覧、既存APIを利用した検索フロー設計
*   **第4章：マルチエージェント構成のアーキテクチャ設計**
    *   複数エージェントによる分業・相互監視の構成パターン
*   **第5章：LoRAによる「背景知識」実装のシステムアーキテクチャ**
    *   マルチエージェントを強化するためのファインチューニング（LoRA）基盤
*   **第6章：システム構成と公開・運用アーキテクチャ**
    *   Azure Container Apps等を活用したセキュアなシステム公開・認証の仕組み
"""

with open('books/rag-multiagent-build/1_overview.md', 'w', encoding='utf-8') as f:
    f.write(new_ch1 + ch1_part2 + roadmap)

# Update Chapter 2
with open('books/rag-multiagent-build/2_ssot_strategy.md', 'r', encoding='utf-8') as f:
    ch2_content = f.read()

ch2_content = ch2_content.replace("# 第2章 ソースをSSOT（Single Source of Truth）とする設計", "# 第2章 RAGの基本理論とSSOT（Single Source of Truth）戦略")
parts = ch2_content.split("## 要旨（先に結論）\n")
new_ch2 = parts[0] + sec_learning + "\n\n" + sec_rag_quality.replace("### 1.7.2", "## 2.1") + "\n\n## 要旨（先に結論）\n" + parts[1]

with open('books/rag-multiagent-build/2_ssot_strategy.md', 'w', encoding='utf-8') as f:
    f.write(new_ch2)

# Update Chapter 3
with open('books/rag-multiagent-build/3_search_technology.md', 'r', encoding='utf-8') as f:
    ch3_content = f.read()

parts3 = ch3_content.split("## なぜ今、高度な検索フローが必要なのか\n")
new_ch3 = parts3[0] + sec_tech.replace("# 技術要素", "## 3.1 技術要素") + "\n" + sec_pipeline_systems.replace("## 1.7", "## 3.2") + "\n\n## なぜ今、高度な検索フローが必要なのか\n" + parts3[1]

with open('books/rag-multiagent-build/3_search_technology.md', 'w', encoding='utf-8') as f:
    f.write(new_ch3)

# Create Chapter 6
ch6_content = sec_infra.replace("# システム構成（公開・認証アーキテクチャ）", "# 第6章 システム構成と公開・運用アーキテクチャ\n\n## 6.1 概要").replace("## 1.6", "## 6")
with open('books/rag-multiagent-build/6_deployment_architecture.md', 'w', encoding='utf-8') as f:
    f.write(ch6_content)

print("Split complete!")
