Zenn publishing helper
=====================

This folder contains helper instructions to publish the book to Zenn.

Prerequisites
 - Node.js / npm (for `zenn-cli`) or use `npx`
 - Python 3.8+ and `pip install pyyaml`

Prepare Zenn content

```bash
# create virtualenv (optional)
python -m venv .venv
.venv\Scripts\activate
pip install pyyaml

# generate Zenn-compatible content (adjust paths as needed)
python ..\scripts\prepare_zenn_book.py ..\docs\books\rag-multiagent-build content\books\rag-multiagent-build
```

Preview & Publish with Zenn CLI

```bash
# preview (from this folder)
npx zenn preview

# login if not already
npx zenn login

# publish (follow CLI prompts)
npx zenn publish
```

Notes
- The script will copy markdown chapter files and create `index.md` with front matter. Verify front matter and images before publishing.
- Zenn publish requires you to be logged in and to have the content formatted per Zenn rules. Adjust manually if needed.
