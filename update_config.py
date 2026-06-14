import yaml

with open('books/rag-multiagent-build/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

config['chapters'] = [
    "1_overview.md",
    "2_ssot_strategy.md",
    "3_search_technology.md",
    "4_multiagent_architecture.md",
    "5_lora_system_architecture.md",
    "6_deployment_architecture.md"
]

with open('books/rag-multiagent-build/config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
