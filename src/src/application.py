from __future__ import annotations

import os
import sys
import time
import textwrap

from trie import Trie


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DEFAULT_WORDS_FILE = os.path.join(DATA_DIR, "words.txt")


def load_words(trie: Trie, path: str) -> int:
    """
    Load words from a text file (one word per line) into the Trie.
    Returns the number of words read (duplicates are allowed but
    do not change trie.size()).
    """
    if not os.path.exists(path):
        # Fallback: a small built-in list if no file is provided.
        seed_words = [
            "app",
            "apple",
            "apples",
            "application",
            "applied",
            "apply",
            "applet",
            "apt",
            "banana",
            "band",
            "bandit",
            "bandwidth",
            "bat",
            "batch",
            "bath",
            "cat",
            "catch",
            "cater",
            "dog",
            "dove",
            "doom",
        ]
        for w in seed_words:
            trie.insert(w.lower())
        return len(seed_words)

    inserted = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip().lower()
            if word:
                trie.insert(word)
                inserted += 1
    return inserted


def collect_all_words(trie: Trie) -> list[str]:
    """
    Collect all words in the Trie into a list via DFS.

    Used to compare Trie prefix search vs naive linear search.
    """
    results: list[str] = []

    # access internal root just for comparison and demo purposes
    root = trie._root  # type: ignore[attr-defined]

    def dfs(node, path: list[str]) -> None:
        if node.is_end:
            results.append("".join(path))
        for ch, child in node.children.items():
            path.append(ch)
            dfs(child, path)
            path.pop()

    dfs(root, [])
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

    # Allow optional custom word list via command-line argument
    words_file = DEFAULT_WORDS_FILE
    if len(sys.argv) > 1:
        words_file = sys.argv[1]

    loaded = load_words(trie, words_file)
    file_label = os.path.basename(words_file) if os.path.exists(words_file) else "built-in word list"
    print(f"Loaded {loaded} words (source: {file_label})")
    print("Trie Autocomplete Demo")
    print_help()

    while True:
        try:
            raw = input("> ").strip()
        except EOFError:
            print("\nBye.")
            break
        except KeyboardInterrupt:
            print("\nInterrupted. Bye.")
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ("quit", "exit", "q"):
            print("Bye.")
            break

        if cmd == "help":
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
            words = trie.get_words_with_prefix(prefix, limit=limit)
            if not words:
                print("(no matches)")
            else:
                for w in words:
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

            all_words = collect_all_words(trie)

            # Linear search
            start = time.perf_counter()
            linear_matches = [w for w in all_words if w.startswith(prefix)]
            linear_time = time.perf_counter() - start

            # Trie search
            start = time.perf_counter()
            trie_matches = trie.get_words_with_prefix(prefix, limit=None)
            trie_time = time.perf_counter() - start

            print(
                f"Linear search found {len(linear_matches)} matches in {linear_time * 1e6:.1f} µs"
            )
            print(
                f"Trie search found   {len(trie_matches)} matches in {trie_time * 1e6:.1f} µs"
            )
            print(f"First {limit} trie matches:")
            for w in trie_matches[:limit]:
                print(" ", w)

        else:
            print("Unknown or malformed command. Type 'help'.")
            continue


if __name__ == "__main__":
    main()
