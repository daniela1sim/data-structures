"""AVL tree / order-statistic dictionary. Adapted from 2023 collaborative coursework.

Original implementation by Daniella Simonovsky and Noam Shtrahman.
The original repository is linked from the parent README. This cleaned version
removes scratch comments/student IDs and includes defensive empty-tree handling.
"""

class AVLNode(object):
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0
		self.bf = 0
	def get_key(self):
		return self.key
	def get_value(self):
		return self.value
	def get_left(self):
		return self.left
	def get_right(self):
		return self.right
	def get_parent(self):
		return self.parent
	def get_height(self):
		if not self.is_real_node():
			return -1
		return self.height
	def get_size(self):
		return self.size
	def set_key(self, key):
		self.key = key
		return None
	def set_value(self, value):
		self.value = value
		return None
	def set_left(self, node):
		if node is None:
			node = AVLNode(None, None)
		self.left = node
		return None
	def set_right(self, node):
		if node is None:
			node = AVLNode(None, None)
		self.right = node
		return None
	def set_parent(self, node):
		self.parent = node
		return None
	def set_height(self, h):
		if not self.is_real_node():
			self.height = -1
			return None
		self.height = h
		return None
	def set_size(self, s):
		if not self.is_real_node():
			self.size = 0
			return None
		self.size = s
		return None
	def is_real_node(self):
		return self.get_key() is not None
	def get_bf(self):
		return self.bf
	def set_bf(self):
		self.bf = self.get_left().get_height() - self.get_right().get_height()
		return None
class AVLTree(object):
	def __init__(self):
		self.root = None
	def search(self, key):
		node = self.get_root()
		if node is None or not node.is_real_node():
			return None
		while node.get_key() != key:
			if not node.get_left().is_real_node() and not node.get_right().is_real_node():
				return None
			elif node.get_key() < key:
				node = node.get_right()
			else:
				node = node.get_left()
		return node
	def insert_as_usual(self, node):
		curr = self.get_root()
		parent = None
		prev_height = 0
		if curr is None or not curr.is_real_node():
			self.set_root(node)
			node.set_left(AVLNode(None, None))
			node.set_right(AVLNode(None, None))
			node.get_left().set_parent(node)
			node.get_right().set_parent(node)
			self.reset_size(node)
			self.reset_height(node)
			return 0
		while curr.is_real_node():
			parent = curr
			if node.get_key() < curr.get_key():
				curr = curr.get_left()
			else:
				curr = curr.get_right()
		if parent is not None:
			prev_height = parent.get_height()
		if node.get_key() < parent.get_key():
			parent.set_left(node)
		else:
			parent.set_right(node)
		node.set_parent(parent)
		node.set_left(AVLNode(None, None))
		node.set_right(AVLNode(None, None))
		node.get_left().set_parent(node)
		node.get_right().set_parent(node)
		self.reset_size(node)
		self.reset_height(node)
		self.reset_height(parent)
		self.reset_size(parent)
		return parent.get_height() - prev_height
	def insert(self, key, val):
		cnt = 0
		node = AVLNode(key, val)
		delta_height = self.insert_as_usual(node)
		parent = node.get_parent()
		while parent is not None:
			parent.set_bf()
			bf = parent.get_bf()
			self.reset_size(parent)
			if 2 > bf > -2 and delta_height == 0:
				self.recursive_reset(parent)
				return cnt
			elif 2 > bf > -2 and delta_height != 0:
				cnt += 1
			else:
				if bf == -2:
					if parent.get_right().get_bf() == -1:
						parent = self.left_rotation(parent)
						cnt += 1
					else:
						parent.set_right(self.right_rotation(parent.get_right()))
						parent = self.left_rotation(parent)
						cnt += 2
				elif bf == 2:
					if parent.get_left().get_bf() == 1:
						parent = self.right_rotation(parent)
						cnt += 1
					else:
						parent.set_left(self.left_rotation(parent.get_left()))
						parent = self.right_rotation(parent)
						cnt += 2
			parent = parent.get_parent()
			if parent is None:
				break
			prev_height = parent.get_height()
			self.reset_height(parent)
			delta_height = parent.get_height() - prev_height
		return cnt
	def left_rotation(self, node):
		parent = node.get_parent()
		right = node.get_right()
		right_left = right.get_left()
		if right_left is None:
			right_left = AVLNode(None, None)
		if right.get_right() is None:
			right.set_right(AVLNode(None, None))
		right.set_left(node)
		node.set_right(right_left)
		node.set_parent(right)
		right.set_parent(parent)
		right_left.set_parent(node)
		if parent is not None:
			if parent.get_right().get_key() == node.get_key():
				parent.set_right(right)
			else:
				parent.set_left(right)
		else:
			self.set_root(right)
		self.reset_height(node)
		self.reset_height(right)
		self.reset_size(node)
		self.reset_size(right)
		node.set_bf()
		right.set_bf()
		return right
	def right_rotation(self, node):
		parent = node.get_parent()
		left = node.get_left()
		left_right = left.get_right()
		if left_right is None:
			left_right = AVLNode(None, None)
		if left.get_left() is None:
			left.set_left(AVLNode(None, None))
		left.set_right(node)
		node.set_left(left_right)
		node.set_parent(left)
		left.set_parent(parent)
		left_right.set_parent(node)
		if parent is not None:
			if parent.get_right().get_key() == node.get_key():
				parent.set_right(left)
			else:
				parent.set_left(left)
		else:
			self.set_root(left)
		self.reset_height(node)
		self.reset_height(left)
		self.reset_size(node)
		self.reset_size(left)
		node.set_bf()
		left.set_bf()
		return left
	def reset_size(self, node):
		size = node.get_left().get_size() + node.get_right().get_size() + 1
		node.set_size(size)
		return None
	def reset_height(self, node):
		height = max(node.get_left().get_height(), node.get_right().get_height()) + 1
		node.set_height(height)
		return None
	def recursive_reset(self, node):
		while node is not None:
			self.reset_height(node)
			self.reset_size(node)
			node.set_bf()
			node = node.get_parent()
	def delete(self, node):
		cnt = 0
		if self.get_root().get_size() == 1:
			self.set_root(AVLNode(None, None))
			return 1
		delta_height, parent = self.delete_like_bst(node)
		while parent is not None:
			parent.set_bf()
			self.reset_size(parent)
			if -2 < parent.get_bf() < 2 and delta_height != 0:
				cnt += 1
			elif parent.get_bf() == 2:
				if parent.get_left().get_bf() == -1:
					parent.set_left(self.left_rotation(parent.get_left()))
					parent = self.right_rotation(parent)
					cnt += 2
				else:
					parent = self.right_rotation(parent)
					cnt += 1
			elif parent.get_bf() == -2:
				if parent.get_right().get_bf() == 1:
					parent.set_right(self.right_rotation(parent.get_right()))
					parent = self.left_rotation(parent)
					cnt += 2
				else:
					parent = self.left_rotation(parent)
					cnt += 1
			self.reset_height(parent)
			parent = parent.get_parent()
			if parent is None:
				break
			prev_height = parent.get_height()
			self.reset_height(parent)
			delta_height = parent.get_height() - prev_height
		return cnt
	def delete_like_bst(self, node):
		parent = node.get_parent()
		if not node.get_left().is_real_node() and not node.get_right().is_real_node():
			if node.get_key() == parent.get_right().get_key():
				parent.set_right(AVLNode(None, None))
				parent.get_right().set_parent(parent)
			else:
				parent.set_left(AVLNode(None, None))
				parent.get_left().set_parent(parent)
		elif not node.get_right().is_real_node() and parent is None:
			self.set_root(node.get_left())
			root = self.get_root()
			root.set_parent(None)
			root.set_right(AVLNode(None, None))
			root.set_left(AVLNode(None, None))
			root.get_left().set_parent(root)
			root.get_right().set_parent(root)
			self.reset_height(root)
			self.reset_size(root)
			root.set_bf()
			return 1, None
		elif not node.get_left().is_real_node() and parent is not None:
			if node.get_key() == parent.get_right().get_key():
				parent.set_right(node.get_right())
				node.get_right().set_parent(parent)
			else:
				parent.set_left(node.get_right())
				node.get_right().set_parent(parent)
		elif not node.get_right().is_real_node() and parent is not None:
			if node == parent.get_right():
				parent.set_right(node.get_left())
				node.get_left().set_parent(parent)
			else:
				parent.set_left(node.get_left())
				node.get_left().set_parent(parent)
		else:
			near = self.successor(node)
			parent = near.get_parent()
			if parent.get_right().get_key() == near.get_key():
				parent.set_right(near.get_right())
			else:
				parent.set_left(near.get_right())
			near.get_right().set_parent(parent)
			node.set_key(near.get_key())
			node.set_value(near.get_value())
		prev_height = parent.get_height()
		self.recursive_reset(parent)
		delta = parent.get_height() - prev_height
		return delta, parent
	def successor(self, node):
		if node.get_right().is_real_node():
			res = node.get_right()
			while res.get_left().is_real_node():
				res = res.get_left()
			return res
		else:
			res = node.get_parent()
			while res is not None:
				if node != res.get_right():
					break
				node = res
				res = res.get_parent()
			return res
	def avl_to_array(self):
		def inorder_rec(node):
			if node is None or not node.is_real_node():
				return []
			return inorder_rec(node.get_left()) + [(node.get_key(), node.get_value())] + inorder_rec(node.get_right())
		return inorder_rec(self.get_root())
	def size(self):
		root = self.get_root()
		return root.get_size() if root is not None and root.is_real_node() else 0
	def split(self, node):
		leftTree = AVLTree()
		rightTree = AVLTree()
		parent = node.get_parent()
		leftTree.set_root(node.get_left())
		rightTree.set_root(node.get_right())
		while parent is not None:
			if node.get_key() == parent.get_right().get_key():
				left = AVLTree()
				left.set_root(parent.get_left())
				node = parent
				parent = parent.get_parent()
				left.get_root().set_parent(None)
				leftTree.join(left, node.get_key(), node.get_value())
			else:
				right = AVLTree()
				right.set_root(parent.get_right())
				node = parent
				parent = parent.get_parent()
				right.get_root().set_parent(None)
				rightTree.join(right, node.get_key(), node.get_value())
		return [leftTree, rightTree]
	def join(self, tree, key, val):
		node = AVLNode(key, val)
		root = self.get_root()
		self_is_shorter = True
		self_is_smaller = True
		if root is None:
			self.set_root(AVLNode(None, None))
			root = self.get_root()
		if tree.get_root() is None:
			tree.set_root(AVLNode(None, None))
		if not root.is_real_node() and not tree.get_root().is_real_node():
			self.set_root(node)
			node.set_left(AVLNode(None, None))
			node.set_right(AVLNode(None, None))
			node.get_left().set_parent(node)
			node.get_right().set_parent(node)
			self.reset_height(node)
			self.reset_size(node)
			return 1
		if not root.is_real_node():
			prev_height = tree.get_root().get_height()
			tree.insert(key, val)
			self.set_root(tree.get_root())
			return prev_height + 1
		if not tree.get_root().is_real_node():
			prev_height = root.get_height()
			self.insert(key, val)
			return prev_height + 1
		if root.get_key() > key:
			self_is_smaller = False
		if root.get_height() == tree.get_root().get_height():
			self.set_root(node)
			if self_is_smaller:
				node.set_left(root)
				root.set_parent(node)
				node.set_right(tree.get_root())
				tree.get_root().set_parent(node)
			else:
				node.set_right(root)
				root.set_parent(node)
				node.set_left(tree.get_root())
				tree.get_root().set_parent(node)
			self.reset_height(node)
			self.reset_size(node)
			node.set_bf()
			return 1
		min_height = min(root.get_height(), tree.get_root().get_height())
		res = 1 + abs(root.get_height() - tree.get_root().get_height())
		if root.get_height() > min_height:
			self_is_shorter = False
		if self_is_shorter and self_is_smaller:
			min_tree = tree.get_root()
			while min_tree.is_real_node() and min_tree.get_height() > min_height:
				min_tree = min_tree.get_left()
			parent = min_tree.get_parent()
			node.set_left(root)
			root.set_parent(node)
			node.set_right(min_tree)
			min_tree.set_parent(node)
			parent.set_left(node)
			node.set_parent(parent)
			self.set_root(tree.get_root())
			self.reset_height(node)
			self.reset_size(node)
			node.set_bf()
		if self_is_shorter and not self_is_smaller:
			max_tree = tree.get_root()
			while max_tree.is_real_node() and max_tree.get_height() > min_height:
				max_tree = max_tree.get_right()
			parent = max_tree.get_parent()
			node.set_right(root)
			root.set_parent(node)
			node.set_left(max_tree)
			max_tree.set_parent(node)
			parent.set_right(node)
			node.set_parent(parent)
			self.set_root(tree.get_root())
			self.reset_height(node)
			self.reset_size(node)
			node.set_bf()
		if not self_is_shorter and self_is_smaller:
			max_self = root
			while max_self.is_real_node() and max_self.get_height() > min_height:
				max_self = max_self.get_right()
			parent = max_self.get_parent()
			node.set_right(tree.get_root())
			tree.get_root().set_parent(node)
			node.set_left(max_self)
			max_self.set_parent(node)
			parent.set_right(node)
			node.set_parent(parent)
			self.reset_height(node)
			self.reset_size(node)
			node.set_bf()
		if not self_is_shorter and not self_is_smaller:
			min_self = root
			while min_self.is_real_node() and min_self.get_height() > min_height:
				min_self = min_self.get_left()
			parent = min_self.get_parent()
			node.set_left(tree.get_root())
			tree.get_root().set_parent(node)
			node.set_right(min_self)
			min_self.set_parent(node)
			parent.set_left(node)
			node.set_parent(parent)
			self.reset_height(node)
			self.reset_size(node)
			node.set_bf()
		while node is not None:
			node.set_bf()
			self.reset_size(node)
			self.reset_height(node)
			if node.get_bf() <= -2:
				if node.get_right().get_bf() == -1 or node.get_right().get_bf() == 0:
					node = self.left_rotation(node)
				else:
					node.set_right(self.right_rotation(node.get_right()))
					node = self.left_rotation(node)
			if node.get_bf() >= 2:
				if node.get_left().get_bf() == 1 or node.get_left().get_bf() == 0:
					node = self.right_rotation(node)
				else:
					node.set_left(self.left_rotation(node.get_left()))
					node = self.right_rotation(node)
			node = node.get_parent()
		return res
	def rank(self, node):
		if not node.get_left().is_real_node():
			r = 1
		else:
			r = node.get_left().get_size() + 1
		while node.get_parent() is not None:
			if node == node.get_parent().get_right():
				if not node.get_parent().get_left().is_real_node():
					r += 1
				else:
					r += node.get_parent().get_left().get_size() + 1
			node = node.get_parent()
		return r
	def select(self, i):
		if i < 1 or i > self.size():
			raise IndexError("rank out of range")
		root = self.get_root()
		return self.select_rec(root, i)
	def select_rec(self, node, i):
		if not node.is_real_node():
			return None
		if not node.get_left().is_real_node():
			curr_rank = 1
		else:
			curr_rank = node.get_left().get_size() + 1
		if i == curr_rank:
			return node
		elif i < curr_rank:
			return self.select_rec(node.get_left(), i)
		else:
			return self.select_rec(node.get_right(), i - curr_rank)
	def get_root(self):
		return self.root
	def set_root(self, node):
		self.root = node
		if node is not None:
			node.set_parent(None)
