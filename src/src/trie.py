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
    Trie (Prefix Tree) implementation for storing strings.

    Core operations:
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
        self._size = 0  # number of distinct words

    # ------------------------
    # Public API
    # ------------------------

    def insert(self, word: str) -> None:
        """
        Insert a word into the Trie.

        Time: O(m), where m is the length of the word.
        Space: O(m) in the worst case.
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
        """
        Check if a word exists in the Trie as a complete word.

        Time: O(m)
        Space: O(1)
        """
        node = self._traverse(word)
        return bool(node and node.is_end)

    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word in the Trie starts with the given prefix.

        Time: O(p)
        Space: O(1)
        """
        return self._traverse(prefix) is not None

    def get_words_with_prefix(
        self, prefix: str, limit: Optional[int] = None
    ) -> List[str]:
        """
        Return a list of words that start with the given prefix.

        Time: O(p + k * L), where:
          p = length of prefix
          k = number of results
          L = average length of the words returned
        Space: O(k * L) for results.
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
        """
        Delete a word from the Trie. Returns True if the word was deleted,
        False if the word was not present.

        Time: O(m)
        Space: O(m) recursion stack
        """

        def _delete(node: TrieNode, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False  # word not found
                node.is_end = False
                self._size -= 1
                # prune if no children
                return len(node.children) == 0

            ch = word[depth]
            child = node.children.get(ch)
            if child is None:
                return False  # word not found

            should_prune_child = _delete(child, depth + 1)
            if should_prune_child:
                del node.children[ch]
                # prune this node if it isn't terminal and has no children
                return not node.is_end and len(node.children) == 0

            return False

        if not word:
            return False

        existed = self.search(word)
        _ = _delete(self._root, 0)
        return existed

    def count_prefix(self, prefix: str) -> int:
        """
        Count how many words in the Trie start with the given prefix.

        Time: O(p + T), where T is the size of the subtree.
        Space: O(h) recursion stack.
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
        """
        Return the number of distinct words in the Trie.

        Time: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """
        Return True if the Trie contains no words.

        Time: O(1)
        """
        return self._size == 0

    # Pythonic helpers
    def __len__(self) -> int:
        return self._size

    def __contains__(self, word: str) -> bool:  # allows: `word in trie`
        return self.search(word)

    # ------------------------
    # Internal helpers
    # ------------------------

    def _traverse(self, string: str) -> Optional[TrieNode]:
        """
        Traverse the Trie according to the given string and
        return the node at the end of the path, or None if it doesn't exist.
        """
        if string == "":
            return self._root

        node = self._root
        for ch in string:
            node = node.children.get(ch)
            if node is None:
                return None
        return node
