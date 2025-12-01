from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class TrieNode:
    """A single node in the Trie."""
    children: Dict[str, "TrieNode"] = field(default_factory=dict)
    is_end: bool = False


class Trie:
    """
    Trie (Prefix Tree) implementation supporting:
      - insert(word)
      - search(word)
      - starts_with(prefix)
      - get_words_with_prefix(prefix, limit=None)
      - delete(word)
      - count_prefix(prefix)
      - size(), is_empty()
    """

    def __init__(self) -> None:
        self._root = TrieNode()
        self._size = 0  # number of stored complete words

    # ------------------------------------------------------
    # Core public API
    # ------------------------------------------------------

    def insert(self, word: str) -> None:
        """Insert a word into the Trie.
        Time: O(m)
        """
        if not word:
            return

        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]

        if not node.is_end:
            node.is_end = True
            self._size += 1

    def search(self, word: str) -> bool:
        """Return True if the word exists as a complete word.
        Time: O(m)
        """
        node = self._traverse(word)
        return bool(node and node.is_end)

    def starts_with(self, prefix: str) -> bool:
        """Return True if any stored word begins with the prefix.
        Time: O(p)
        """
        return self._traverse(prefix) is not None

    def get_words_with_prefix(
        self, prefix: str, limit: Optional[int] = None
    ) -> List[str]:
        """Return words beginning with prefix. Stops at limit if provided.
        Time: O(p + k·L')
        """
        node = self._traverse(prefix)
        if node is None:
            return []

        results: List[str] = []
        path = list(prefix)

        def dfs(n: TrieNode) -> None:
            if limit is not None and len(results) >= limit:
                return
            if n.is_end:
                results.append("".join(path))
            for ch, child in n.children.items():
                path.append(ch)
                dfs(child)
                path.pop()

        dfs(node)
        return results

    def delete(self, word: str) -> bool:
        """Delete a word. Returns True if deleted.
        Time: O(m)
        """

        def _delete(node: TrieNode, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                self._size -= 1
                # True = prune this node (no children and not end)
                return len(node.children) == 0

            ch = word[depth]
            child = node.children.get(ch)
            if child is None:
                return False

            should_prune = _delete(child, depth + 1)
            if should_prune:
                del node.children[ch]
                return (not node.is_end) and (len(node.children) == 0)

            return False

        if not word:
            return False

        existed = self.search(word)
        _delete(self._root, 0)
        return existed

    def count_prefix(self, prefix: str) -> int:
        """Count how many stored words start with the prefix.
        Time: O(p + T)
        """
        node = self._traverse(prefix)
        if node is None:
            return 0

        count = 0

        def dfs(n: TrieNode) -> None:
            nonlocal count
            if n.is_end:
                count += 1
            for child in n.children.values():
                dfs(child)

        dfs(node)
        return count

    def size(self) -> int:
        """Return number of stored words."""
        return self._size

    def is_empty(self) -> bool:
        """Return True if Trie contains no words."""
        return self._size == 0

    # Pythonic convenience
    def __len__(self) -> int:
        return self._size

    def __contains__(self, word: str) -> bool:
        return self.search(word)

    # ------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------

    def _traverse(self, string: str) -> Optional[TrieNode]:
        """Return the node at the end of string traversal."""
        node = self._root
        for ch in string:
            node = node.children.get(ch)
            if node is None:
                return None
        return node
