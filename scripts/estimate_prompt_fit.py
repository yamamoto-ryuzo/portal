#!/usr/bin/env python3
import argparse
import os
import sys

def try_import_tiktoken():
    try:
        import tiktoken
        try:
            enc = tiktoken.get_encoding("cl100k_base")
        except Exception:
            enc = None
        return tiktoken, enc
    except Exception:
        return None, None

def count_tokens(text, enc):
    if enc:
        return len(enc.encode(text))
    return round(len(text) / 4)

def human(n):
    return f"{n:,}"

def main():
    p = argparse.ArgumentParser(description='Estimate prompt fit for models (token/char basis)')
    p.add_argument('--model-tokens', type=int, default=8000)
    p.add_argument('--chunk-tokens', type=int, default=500)
    p.add_argument('--selected-chunks', type=int, default=5)
    p.add_argument('--summary-tokens', type=int, default=150)
    p.add_argument('--selected-summaries', type=int, default=5)
    p.add_argument('--system-chars', type=int, default=300)
    p.add_argument('--query-chars', type=int, default=200)
    p.add_argument('--output-reserved-chars', type=int, default=500)
    p.add_argument('--file', type=str, help='Optional file to measure chars/tokens')
    args = p.parse_args()

    tiktoken_mod, enc = try_import_tiktoken()
    has_tiktoken = tiktoken_mod is not None and enc is not None

    file_chars = None
    file_tokens = None
    if args.file:
        if not os.path.exists(args.file):
            print(f"File not found: {args.file}")
            sys.exit(2)
        with open(args.file, 'r', encoding='utf-8') as f:
            txt = f.read()
        file_chars = len(txt)
        file_tokens = count_tokens(txt, enc)

    chunk_chars = args.chunk_tokens * 4
    read_chars_raw = args.selected_chunks * chunk_chars
    read_chars_condensed = args.selected_summaries * args.summary_tokens * 4

    model_max_chars = args.model_tokens * 4
    usable_min = int(model_max_chars * 0.5)
    usable_max = int(model_max_chars * 0.7)

    total_ref_chars = read_chars_raw + read_chars_condensed
    total_prompt_chars = args.system_chars + args.query_chars + total_ref_chars + args.output_reserved_chars

    print("--- Estimate Prompt Fit ---")
    print(f"Has tiktoken (cl100k_base): {has_tiktoken}")
    if file_chars is not None:
        print(f"File: {args.file}")
        print(f"  chars: {human(file_chars)}")
        print(f"  tokens (est): {human(file_tokens)}")
    print(f"chunk_tokens: {args.chunk_tokens} -> chunk_chars: {human(chunk_chars)}")
    print(f"selected_chunks: {args.selected_chunks} -> read_chars_raw: {human(read_chars_raw)}")
    print(f"selected_summaries: {args.selected_summaries} x summary_tokens {args.summary_tokens} -> read_chars_condensed: {human(read_chars_condensed)}")
    print(f"total_ref_chars: {human(total_ref_chars)}")
    print(f"system_chars: {human(args.system_chars)}, query_chars: {human(args.query_chars)}, output_reserved_chars: {human(args.output_reserved_chars)}")
    print(f"total_prompt_chars (system+query+refs+output_reserved): {human(total_prompt_chars)}")
    print(f"model max chars (theoretical): {human(model_max_chars)}")
    print(f"usable_chars 50%: {human(usable_min)}  / 70%: {human(usable_max)}")

    def verdict(limit, name):
        ok = total_prompt_chars <= limit
        print(f"Fits {name}? {'YES' if ok else 'NO'} (limit={human(limit)})")

    verdict(model_max_chars, 'model_max_chars (strict)')
    verdict(usable_min, 'usable 50% (conservative)')
    verdict(usable_max, 'usable 70% (aggressive)')

    print('\nNotes:')
    print('- The token->char factor 4 is an approximation; use tiktoken for exact counts when available.')
    print('- If verdict is NO, reduce selected_chunks/summaries or increase model context.')

if __name__ == '__main__':
    main()
