"""Simple interactive-free AVL example; run: python avl-tree/examples/demo.py"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from AVLTree import AVLTree


def main():
    tree = AVLTree()
    for key in (30, 10, 40, 20):
        tree.insert(key, f"value-{key}")
    print("In order:", tree.avl_to_array())
    print("Search 20:", tree.search(20).get_value())
    print("Second-smallest:", tree.select(2).get_key())


if __name__ == "__main__":
    main()
