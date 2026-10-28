# Provenance and changes

The implementations originate from collaborative Data Structures coursework at Tel Aviv University in 2023 by **Daniella Simonovsky and Noam Shtrahman**. The original sources, development iterations, and commit histories remain available in:

- [AVL Tree source repository](https://github.com/daniella1sim/data_stractures1), primary source file `AVLTree.py` (last update marked `final`, May 24, 2023).
- [Binomial Heap source repository](https://github.com/daniella1sim/BinomialHeap), source filename `BInomealHeap.java` (June 2023).

## Included code

- `avl-tree/AVLTree.py`: based on the final `AVLTree.py` rather than the older `final.py` or other experimental scratch files.
- `binomial-heap/src/BinomialHeap/BinomialHeap.java`: based on the original `BInomealHeap.java`; renamed for the public Java class and package.

## Portfolio edits

- Removed the original student identification numbers, repetitive coursework docstrings, debugging comments, exploratory fragments, and unused IDE files.
- Preserved core algorithms and the public course-facing method names where practical.
- Added explicit handling for empty AVL trees, corrected the virtual-child setters, and rejected out-of-range AVL selection indices.
- Fixed binomial-heap child parent-pointer resets after root deletion, the updating of `HeapItem.node` references after a `decreaseKey` swap, root-tail maintenance during certain deletions, and rank-based `setLast` comparisons.
- Added basic argument and empty-heap checks and documented consuming meld semantics.
- Added separate Python and Java automated regression tests, validation of structural invariants, and this README.

This bundle contains code snapshots, **not a history-preserving Git merge**. When publishing, retain links and named collaborator credit and verify coursework/collaboration publication rules. A public repository without a license does not automatically grant reuse rights to unrelated third parties.
