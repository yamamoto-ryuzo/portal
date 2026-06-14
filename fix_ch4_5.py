import re

# Format Chapter 4
with open('books/rag-multiagent-build/4_multiagent_architecture.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('### シングルエージェントの限界', '### 4.1.1 シングルエージェントの限界')
text = text.replace('### マルチエージェントの価値：分業と相互監視', '### 4.1.2 マルチエージェントの価値：分業と相互監視')

text = text.replace('### パターンA：シーケンシャル型（ウォーターフォール）', '### 4.2.1 パターンA：シーケンシャル型（ウォーターフォール）')
text = text.replace('### パターンB：階層型（マネージャー・ワーカー）', '### 4.2.2 パターンB：階層型（マネージャー・ワーカー）')
text = text.replace('### パターンC：ネットワーク型（自律的議論）', '### 4.2.3 パターンC：ネットワーク型（自律的議論）')

text = text.replace('### 全体フロー：SSOTベースの意思決定システム', '### 4.3.1 全体フロー：SSOTベースの意思決定システム')

with open('books/rag-multiagent-build/4_multiagent_architecture.md', 'w', encoding='utf-8') as f:
    f.write(text)

# Format Chapter 5
with open('books/rag-multiagent-build/5_lora_system_architecture.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('### 全体構成図（概念）', '### 5.1.1 全体構成図（概念）')
text = text.replace('### ① データ生成パイプライン', '### 5.2.1 データ生成パイプライン')
text = text.replace('### ② 学習環境 (Training)', '### 5.2.2 学習環境 (Training)')
text = text.replace('### ③ 推論環境 (Serving / Inference)', '### 5.2.3 推論環境 (Serving / Inference)')

with open('books/rag-multiagent-build/5_lora_system_architecture.md', 'w', encoding='utf-8') as f:
    f.write(text)

