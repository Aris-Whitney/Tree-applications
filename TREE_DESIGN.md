# TREE_DESIGN.md  
## Mini-Project 3 – Tree Applications  
### Trie (Prefix Tree) Design Document

---

## 1. Tree Selection

I selected the **Trie (Prefix Tree)** as the data structure for my project.

A Trie stores strings by mapping each character to a child node, with complete words marked at terminal nodes. Tries are ideal for prefix-based operations.

### Why I Chose the Trie
- The application I’m building is an **autocomplete tool**, which perfectly fits a Trie.
- Trie performance depends on **word length**, not on the number of words.
- Widely used in real systems: autocomplete, spell-check, word games, and prefix search.

---

## 2. Use Cases

Common use cases of Tries include:

- Autocomplete (search bars, IDEs, smartphone keyboards)
- Spell checking and suggestion engines
- Word game helpers (Scrabble, Boggle, Wordle)
- Dictionary lookup by prefix
- Contact list filtering
- Longest-prefix matching in networking

For this project, the Trie supports:
- Fast word lookup
- Autocomplete suggestions
- Prefix counting
- Word insertion and deletion

---

## 3. Properties and Performance

### 3.1 Structural Properties
- Each node contains:
  - A dictionary mapping `character → child node`
  - A boolean `is_end` flag for completing a word
- The root node represents the empty prefix
- The Trie height ≤ length of the longest word

### 3.2 Complexity Summary
Let:
- `m` = length of a word  
- `p` = length of a prefix  
- `k` = number of results returned by prefix search  
- `L'` = average length of returned words beyond the prefix  
- `T` = number of nodes under a prefix  

| Operation | Time Complexity | Space Complexity |
|----------|-----------------|------------------|
| Insert | O(m) | O(m) |
| Search | O(m) | O(1) |
| Starts With | O(p) | O(1) |
| Words With Prefix | O(p + k·L') | O(k·L') |
| Delete | O(m) | O(m) recursion |
| Count Prefix | O(p + T) | O(T) |
| Size | O(1) | O(1) |
| Is Empty | O(1) | O(1) |

### Overall Space Requirement
Worst case: **O(n · L)** for `n` words of average length `L`.

---

## 4. Interface Design

The Trie interface below defines all operations used in the application.  
Each method includes a description and time/space complexity.

### 4.1 Class Structure

```python
class Trie:
    def insert(self, word: str) -> None: ...
    def search(self, word: str) -> bool: ...
    def starts_with(self, prefix: str) -> bool: ...
    def get_words_with_prefix(self, prefix: str,
                              limit: Optional[int] = None) -> List[str]: ...
    def delete(self, word: str) -> bool: ...
    def count_prefix(self, prefix: str) -> int: ...
    def size(self) -> int: ...
    def is_empty(self) -> bool: ...
```
### 4.2 Method Specifications
insert(word: str) → None

Inserts a word into the Trie.

Time: O(m)

Space: O(m) worst case

search(word: str) → bool

Returns True if the word exists.

Time: O(m)

Space: O(1)

starts_with(prefix: str) → bool

Returns True if any word starts with the prefix.

Time: O(p)

Space: O(1)

get_words_with_prefix(prefix: str, limit: Optional[int]) → List[str]

Returns limit words (or all if limit=None) that start with the prefix.

Time: O(p + k·L')

Space: O(k·L')

delete(word: str) → bool

Deletes a word and prunes unused nodes.

Time: O(m)

Space: O(m) recursion

count_prefix(prefix: str) → int

Counts all words that begin with the prefix.

Time: O(p + T)

Space: O(T)

size() → int

Returns number of stored words.

Time: O(1)

Space: O(1)

is_empty() → bool

Returns whether the Trie contains zero words.

Time: O(1)


## 5. Implementation Notes

Each node is represented using:

- children: Dict[str, TrieNode]

- is_end: bool

A private method _traverse(string) is used to reduce repeated code.

Prefix operations use DFS to gather results.

Delete uses recursion and returns whether a subtree can be pruned.

The Trie maintains a private _size counter for O(1) size lookups.

## 6. Evolution of the Interface

The initial interface included:

insert

search

starts_with

get_words_with_prefix

delete

During application development, more methods were necessary:

size() – to support a stats command

is_empty() – for edge-case handling

count_prefix(prefix) – to report suggestion counts

These methods were added as the application requirements evolved, showing the intended iterative design process.

## 7. Summary

This design document includes:

Tree selection and justification

Real-world use cases

Trie properties and performance

Full interface with complexity

Implementation considerations

Evolution of the interface

