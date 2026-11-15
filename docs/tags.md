---
title: タグ索引
date: 2026-11-15
permalink: /tags/
---

# タグ索引

記事のフロントマター（`tags:`）から自動生成される索引ページです。

{% assign all_tags = site.pages | map: "tags" | compact | join: "," | split: "," | uniq | sort -%}
{% if all_tags.size == 0 %}
タグ付きのページはまだありません。
{% else %}
{%- for tag in all_tags %}
{%- if tag == "" %}{% continue %}{% endif %}

## {{ tag }}

{% for p in site.pages -%}
{% if p.tags contains tag -%}
- [{{ p.title | default: p.name }}]({{ p.url | relative_url }}){% if p.date %}（{{ p.date | date: "%Y-%m-%d" }}）{% endif %}
{% endif -%}
{% endfor %}
{%- endfor %}
{% endif %}
