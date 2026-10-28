# Data Structures — AVL Trees and Binomial Heaps

Implementations of two tree-based data structures developed during the **Data Structures** course at **Tel Aviv University** (2023). The collection demonstrates balanced search trees, meldable priority queues, order-statistic operations, and careful maintenance of structural invariants.

**Languages:** Python (AVL tree), Java (binomial heap). The implementations use the standard libraries; the tests require no additional Python or Java packages.

> **Coursework and authorship:** The original assignments were developed collaboratively by **Daniella Simonovsky and Noam Shtrahman**. This repository is a cleaned, tested portfolio presentation of that work, not a claim of sole authorship. Links to the original repositories and a change log are in [docs/ORIGINS_AND_CHANGES.md](docs/ORIGINS_AND_CHANGES.md).

## Projects at a glance

| | AVL Tree | Binomial Heap |
|---|---|---|
| Language | Python | Java |
| Role | Ordered dictionary and order statistics | Meldable minimum-priority queue |
| Structural idea | Height-balanced binary search tree | Forest of heap-ordered binomial trees |
| Notable operations | `search`, `insert`, `delete`, `split`, `join`, `rank`, `select` | `insert`, `findMin`, `deleteMin`, `decreaseKey`, `delete`, `meld` |
| Key metadata | Height, balance factor, subtree size, parent pointers | Tree rank, circular sibling/root lists, minimum pointer, item handles |

## Repository layout

```text
data-structures/
├── README.md
├── Makefile
├── .gitignore
├── avl-tree/
│   ├── AVLTree.py
│   ├── examples/
│   │   └── demo.py
│   └── tests/
│       └── test_avl.py
├── binomial-heap/
│   ├── src/
│   │   └── BinomialHeap/
│   │       └── BinomialHeap.java
│   └── tests/
│       └── BinomialHeapTest.java
└── docs/
    └── ORIGINS_AND_CHANGES.md
```

## AVL Tree (Python)

An AVL tree is a binary search tree that keeps the height difference between each node's left and right subtrees at most one. Rotations restore balance after updates. In addition to keys and values, this implementation maintains each node's **subtree size**, permitting efficient rank and select operations.

- **Insertion/deletion:** BST updates followed by AVL rebalancing, with single/double rotations.
- **Search and traversal:** Lookup by key, and sorted `(key, value)` output through `avl_to_array()`.
- **Order statistics:** `rank(node)` is one-indexed; `select(i)` retrieves the node with one-indexed rank `i`.
- **Split/join:** `split(node)` separates elements smaller and greater than the pivot; `join(other, key, value)` combines trees separated by a pivot key. These operations mutate tree structure, so avoid reusing source trees after a split/join without understanding ownership.
- **Virtual nodes:** Missing children are represented using nodes whose keys are `None`.

Run a short example from the repository root (Windows, macOS, or Linux):

```bash
python avl-tree/examples/demo.py
```

This example inserts four keys, prints the sorted `(key, value)` pairs, searches for one key, and selects the second-smallest key.

### Expected complexity (balanced AVL tree)

| Operation | Time |
|---|---|
| Search, insert, delete | `O(log n)` |
| Rank, select | `O(log n)` |
| Split, join | `O(log n)` under the standard AVL algorithms and their preconditions |
| In-order array conversion | `O(n)` |
| Size and root lookup | `O(1)` |

These are algorithmic complexity targets under the stated preconditions, not formal performance proofs for this codebase. The supplied tests validate representative behavior, including structural invariants.

## Binomial Heap (Java)

A binomial heap is a collection of binomial trees satisfying the **min-heap order**: the key in a parent node does not exceed the keys of its children. Root ranks are distinct, allowing the forest to be melded by linking trees of equal rank.

- **Priority-queue operations:** `insert(key, info)`, `findMin()`, `deleteMin()`.
- **Mutable handles:** `insert()` returns a `HeapItem` handle; `decreaseKey(handle, diff)` and `delete(handle)` operate on that item.
- **Melding:** `meld(other)` joins two heaps by consolidating equal-rank roots. Treat the second heap as **consumed** after a meld.
- **Counters:** `size()` and `numTrees()` return maintained metadata.
- **Preconditions:** Coursework uses nonnegative integer insertion keys; call `findMin`/`deleteMin` only on nonempty heaps (this version throws `NoSuchElementException` otherwise). `decreaseKey` expects a meaningful positive decrement and a live item handle.

### Expected complexity

| Operation | Time |
|---|---|
| Insert | `O(log n)` worst case (some inserts `O(1)`) |
| Find minimum, size, empty | `O(1)` |
| Delete minimum, decrease key, delete | `O(log n)` |
| Meld | `O(log(n + m))` |

### Compile and run

From the repository root (Java 8+):

```bash
javac -d binomial-heap/build \
  binomial-heap/src/BinomialHeap/BinomialHeap.java \
  binomial-heap/tests/BinomialHeapTest.java
java -cp binomial-heap/build BinomialHeapTest
```

On Windows, put the compilation command on one line and use backslashes in file paths if desired.

## Automated testing

The test suites are runnable with Python's built-in `unittest` and a standalone Java test harness (no JUnit dependency).

**Python / AVL** (Python 3.9+):

```bash
python -m unittest discover -s avl-tree/tests -v
```

Tests cover empty-tree behavior, all four AVL insertion-rotation patterns, ordered search/rank/select, randomized insertions and deletions checked against a sorted reference, split/join, and recursive invariants for parent pointers, subtree sizes, heights, balance factors and search order.

**Java / Binomial heap** (JDK 8+):

```bash
javac -d binomial-heap/build binomial-heap/src/BinomialHeap/BinomialHeap.java binomial-heap/tests/BinomialHeapTest.java
java -cp binomial-heap/build BinomialHeapTest
```

Tests cover empty-heap behavior, insertion and minimum tracking, randomized `deleteMin` results checked against Java `PriorityQueue`, melding, handle stability after `decreaseKey`, arbitrary-item deletion, and recursive invariants for heap order, parent links, root ranks, item references, and reachable-node counts.

On macOS/Linux with `make`, run all suites via:

```bash
make test
```

**Verification scope:** Passing tests are regression evidence for exercised operations, not a proof of correctness for every input or exhaustive verification of coursework edge cases.

## Design notes and limitations

- AVL nodes use explicit parent links and virtual children, reflecting the original course API rather than Python's usual dictionary interface.
- The heap's linked forest and object handles mirror the original Java coursework API, rather than wrapping Java's standard priority queue.
- This repository is a **portfolio refactoring**, with fixes identified by automated tests. It is not an untouched course submission. See the provenance file for what changed.
- Neither original repository provides a published open-source license. No new license is assigned here; publishing/relicensing and reusing third-party utilities should be agreed with collaborators and consistent with university rules.
- The ZIP package does **not** carry Git commit histories. The original repositories retain their commit histories and remain linked below.

## Original repositories

- [AVL Tree — `daniella1sim/data_stractures1`](https://github.com/daniella1sim/data_stractures1)
- [Binomial Heap — `daniella1sim/BinomialHeap`](https://github.com/daniella1sim/BinomialHeap)
