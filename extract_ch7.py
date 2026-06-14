with open('books/rag-multiagent-build/6_deployment_architecture.md', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('### 6.10.4 閉鎖環境とLoRA（背景知識）の完全統合')
if len(parts) == 2:
    with open('books/rag-multiagent-build/6_deployment_architecture.md', 'w', encoding='utf-8') as f:
        f.write(parts[0].strip())

    ch7_content = '# 第7章 閉鎖環境におけるLoRAとSSOTの完全統合（継続的学習システム）\n\n' + parts[1].strip()
    
    # Adjust headings in ch7
    ch7_content = ch7_content.replace('1. **Multi-LoRA Serving', '## 7.1 Multi-LoRA Serving')
    ch7_content = ch7_content.replace('**なぜ「巨大な単一モデル」', '### 7.1.1 なぜ「巨大な単一モデル」')
    ch7_content = ch7_content.replace('**オーケストレーターと専門エージェントの役割分担の最適解', '### 7.1.2 オーケストレーターと専門エージェントの役割分担の最適解')
    ch7_content = ch7_content.replace('2. **継続的学習ループのセキュアな運用', '## 7.2 継続的学習ループのセキュアな運用')
    ch7_content = ch7_content.replace('**【具体的な継続的学習', '### 7.2.1 具体的な継続的学習')
    ch7_content = ch7_content.replace('**継続的学習と4つの高度なRAG技術のシナジー', '### 7.2.2 継続的学習と4つの高度なRAG技術のシナジー')
    
    with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'w', encoding='utf-8') as f:
        f.write(ch7_content + '\n')

with open('books/rag-multiagent-build/config.yaml', 'r', encoding='utf-8') as f:
    config = f.read()

if '7_continuous_learning_and_integration.md' not in config:
    config = config.replace('  - 6_deployment_architecture.md', '  - 6_deployment_architecture.md\n  - 7_continuous_learning_and_integration.md')
    with open('books/rag-multiagent-build/config.yaml', 'w', encoding='utf-8') as f:
        f.write(config)
        
