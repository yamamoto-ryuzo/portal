with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r'(+)mermaid', '`mermaid', text)
text = re.sub(r'E -\.背景知識をアップデート\.-> C\n *+', 'E -.背景知識をアップデート.-> C\n`', text)

with open('books/rag-multiagent-build/7_continuous_learning_and_integration.md', 'w', encoding='utf-8') as f:
    f.write(text)
