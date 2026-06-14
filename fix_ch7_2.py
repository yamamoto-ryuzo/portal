with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('## 7.1 Multi-LoRA Serving（vLLMの活用）**', '## 7.1 Multi-LoRA Serving（vLLMの活用）')
text = text.replace('## 7.2 継続的学習ループのセキュアな運用**', '## 7.2 継続的学習ループのセキュアな運用')

with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'w', encoding='utf-8') as f:
    f.write(text)
