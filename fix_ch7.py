with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('### 7.1.1 なぜ'):
        line = line.replace('？**', '？\n')
    elif line.startswith('### 7.1.2 オーケストレーター'):
        line = line.replace('最適解**', '最適解\n')
    elif line.startswith('   ### 7.2.1 具体的な継続的学習'):
        line = line.replace('   ###', '###').replace('仕組み】**', '仕組み\n')
    elif line.startswith('### 7.2.2 継続的学習'):
        line = line.replace('学習循環エコシステム）**', '学習循環エコシステム）\n')
    new_lines.append(line)

with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
