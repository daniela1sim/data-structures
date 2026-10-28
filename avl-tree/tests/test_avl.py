"""Regression tests for the original AVL algorithms and subtree metadata."""
import importlib.util
import random
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / 'AVLTree.py'
spec = importlib.util.spec_from_file_location('course_avl', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
AVLTree = module.AVLTree


def assert_valid(tree):
    root = tree.get_root()
    def visit(node, parent, lo=None, hi=None):
        if node is None or not node.is_real_node():
            return 0, -1
        assert node.get_parent() is parent, f'wrong parent of {node.get_key()}'
        key = node.get_key()
        assert (lo is None or lo < key) and (hi is None or key < hi), 'BST-order violation'
        assert node.get_left() is not None and node.get_right() is not None, 'missing virtual child'
        n_left, h_left = visit(node.get_left(), node, lo, key)
        n_right, h_right = visit(node.get_right(), node, key, hi)
        assert abs(h_left - h_right) <= 1, f'unbalanced node {key}'
        assert node.get_bf() == h_left-h_right, f'stale balance factor at {key}'
        assert node.get_size() == n_left + n_right + 1, f'wrong subtree size at {key}'
        assert node.get_height() == max(h_left, h_right) + 1, f'wrong height at {key}'
        return n_left + n_right + 1, max(h_left, h_right) + 1
    n, _ = visit(root, None)
    assert tree.size() == n
    return n


class AVLTests(unittest.TestCase):
    def test_empty(self):
        t = AVLTree()
        self.assertIsNone(t.search(3))
        self.assertEqual(t.size(), 0)
        self.assertEqual(t.avl_to_array(), [])
        with self.assertRaises(IndexError): t.select(1)

    def test_single_rotations_and_double_rotations(self):
        for keys in ([1, 2, 3], [3, 2, 1], [3, 1, 2], [1, 3, 2]):
            with self.subTest(keys=keys):
                t = AVLTree()
                for k in keys:
                    t.insert(k, str(k))
                    assert_valid(t)
                self.assertEqual(t.get_root().get_key(), 2)
                self.assertEqual([x for x, _ in t.avl_to_array()], [1, 2, 3])

    def test_rank_select_and_search(self):
        t = AVLTree()
        keys = [40, 10, 30, 20, 50, 60, 5]
        for k in keys: t.insert(k, f'v{k}')
        assert_valid(t)
        for rank, k in enumerate(sorted(keys), 1):
            self.assertEqual(t.search(k).get_value(), f'v{k}')
            self.assertEqual(t.rank(t.search(k)), rank)
            self.assertEqual(t.select(rank).get_key(), k)
        self.assertIsNone(t.search(999))
        for i in (0, len(keys)+1):
            with self.assertRaises(IndexError): t.select(i)

    def test_randomized_insert_delete_against_sorted_reference(self):
        for seed in range(12):
            rng = random.Random(seed)
            keys = rng.sample(range(1, 600), 55)
            t = AVLTree()
            live = set()
            for k in keys:
                t.insert(k, k)
                live.add(k)
                self.assertEqual(assert_valid(t), len(live))
                self.assertEqual([x for x, _ in t.avl_to_array()], sorted(live))
            for k in rng.sample(keys, len(keys)):
                t.delete(t.search(k))
                live.remove(k)
                assert_valid(t)
                self.assertEqual([x for x, _ in t.avl_to_array()], sorted(live))

    def test_split(self):
        for n in range(3, 32):
            for pivot in (0, n//2, n-1):
                t = AVLTree()
                for k in random.Random(n*97+pivot).sample(range(n), n): t.insert(k, k)
                left, right = t.split(t.search(pivot))
                assert_valid(left)
                assert_valid(right)
                self.assertEqual([k for k, _ in left.avl_to_array()], list(range(pivot)))
                self.assertEqual([k for k, _ in right.avl_to_array()], list(range(pivot+1,n)))

    def test_join(self):
        for n1, n2 in [(1, 1), (2, 15), (25, 3), (10, 10), (1, 20)]:
            a, b = AVLTree(), AVLTree()
            for k in range(n1): a.insert(k, k)
            for k in range(n1+1, n1+1+n2): b.insert(k,k)
            a.join(b, n1, n1)
            assert_valid(a)
            self.assertEqual([k for k,_ in a.avl_to_array()], list(range(n1+n2+1)))

if __name__ == '__main__':
    unittest.main()
