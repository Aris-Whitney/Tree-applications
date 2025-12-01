from __future__ import annotations

import os
import sys
import time
import textwrap

from src.trie import Trie


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DEFAULT_WORDS_FILE = os.path.join(DATA_DIR, "words.txt")


def load_words(trie: Trie, path: str) -> int:
    """Load words from a text file (one word per line) into the Trie."""
    if not os.path.exists(path):
        # fallback set if no file is present
        fallback = [
            "app", "apple", "apples", "application", "applied", "apply",
            "applet", "apt",
            "banana", "band", "bandit", "bandwidth",
            "bat", "batch", "bath",
            "cat", "catch", "cater",
            "dog", "dove", "doom",
        ]
        for w in fallback:
            trie.insert(w)
        return len(fallback)

    count = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip().lower()
            if word:
                trie.insert(word)
                count += 1
    return count


def collect_all_words(trie: Trie) -> list[str]:
    """Collect all words in the Trie (used for linear search comparison)."""
    results: list[str] = []

    def dfs(node, path: list[str]) -> None:
        if node.is_end:
            results.append("".join(path))
        for ch, child in node.children.items():
            path.append(ch)
            dfs(child, path)
            path.pop()

    dfs(trie._root, [])  # type: ignore[attr-defined]
    return results


def print_help() -> None:
    help_text = textwrap.dedent(
        """
        Commands:
          help
          stats
          search <word>
          prefix <prefix> [limit]
          add <word>
          delete <word>
          compare <prefix> [limit]
          quit
        """
    ).strip()
    print(help_text)


def main() -> None:
    trie = Trie()

    # Optional: allow a custom word list file via CLI arg
    words_file = DEFAULT_WORDS_FILE
    if len(sys.argv) > 1:
        words_file = sys.argv[1]

    loaded = load_words(trie, words_file)
    source_label = os.path.basename(words_file) if os.path.exists(words_file) else "built-in list"
    print(f"Loaded {loaded} words (source: {source_label})")
    print("Trie Autocomplete Demo")
    print_help()

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ("quit", "exit", "q"):
            print("Bye.")
            break

        elif cmd == "help":
            print_help()

        elif cmd == "stats":
            print(f"Words stored in trie: {trie.size()}")

        elif cmd == "search":
            if not args:
                print("Usage: search <word>")
                continue
            word = args[0].lower()
            print("YES" if trie.search(word) else "NO")

        elif cmd == "prefix":
            if not args:
                print("Usage: prefix <prefix> [limit]")
                continue
            prefix = args[0].lower()
            limit = 10
            if len(args) > 1:
                try:
                    limit = int(args[1])
                except ValueError:
                    print("Limit must be an integer; using default = 10.")
            matches = trie.get_words_with_prefix(prefix, limit=limit)
            if not matches:
                print("(no matches)")
            else:
                for w in matches:
                    print(" ", w)

        elif cmd == "add":
            if not args:
                print("Usage: add <word>")
                continue
            word = args[0].lower()
            existed = trie.search(word)
            trie.insert(word)
            if existed:
                print(f"'{word}' was already present.")
            else:
                print(f"Added '{word}'.")

        elif cmd == "delete":
            if not args:
                print("Usage: delete <word>")
                continue
            word = args[0].lower()
            if trie.delete(word):
                print(f"Deleted '{word}'.")
            else:
                print(f"'{word}' not found.")

        elif cmd == "compare":
            if not args:
                print("Usage: compare <prefix> [limit]")
                continue
            prefix = args[0].lower()
            limit = 10
            if len(args) > 1:
                try:
                    limit = int(args[1])
                except ValueError:
                    print("Limit must be an integer; using default = 10.")

            # linear search over all words
            all_words = collect_all_words(trie)

            start = time.perf_counter()
            linear_matches = [w for w in all_words if w.startswith(prefix)]
            t_linear = time.perf_counter() - start

            # trie-based search
            start = time.perf_counter()
            trie_matches = trie.get_words_with_prefix(prefix, limit=None)
            t_trie = time.perf_counter() - start

            print(f"Linear search found {len(linear_matches)} matches in {t_linear * 1e6:.1f} µs")
            print(f"Trie search found   {len(trie_matches)} matches in {t_trie * 1e6:.1f} µs")
            print(f"First {limit} trie matches:")
            for w in trie_matches[:limit]:
                print(" ", w)

        else:
            print("Unknown command. Type 'help'.")


if __name__ == "__main__":
    main()
