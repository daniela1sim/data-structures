package BinomialHeap;

/**
 * Min-priority queue implemented as a collection of binomial trees.
 *
 * Original collaborative Data Structures coursework by
 * Daniella Simonovsky and Noam Shtrahman (Tel Aviv University, 2023).
 * This portfolio version includes documented correctness fixes.
 *
 * Item handles returned by insert are stable across decreaseKey operations.
 * Meld destructively incorporates the second heap; do not reuse the donor.
 */

public class BinomialHeap
{
	public int size;
	public HeapNode last;
	public HeapNode min;
	public int numOfTrees;

	public BinomialHeap(int size, HeapNode last, HeapNode min, int num) {
		this.size = size;
		this.last = last;
		this.min = min;
		this.numOfTrees = num;
	}

	public BinomialHeap() {
		this.size = 0;
		this.last = null;
		this.min = null;
		this.numOfTrees = 0;
	}

	public HeapItem insert(int key, String info) 
	{    
		
		HeapNode node = new HeapNode();
		node.item = new HeapItem(node, key, info);
		node.rank = 0;

		if (this.size % 2 == 0 && this.size > 0) {
			HeapNode next = this.last.next;
			this.last.next = node;
			node.next = next;
			if (this.min.item.key > node.item.key) {
				this.min = node;
			}
			
			this.numOfTrees ++;
			this.size ++;
			
			return node.item;
		}

		node.next = node;			
		BinomialHeap heap2 = new BinomialHeap(1, node, node, 1);
		
		this.meld(heap2);
		return node.item;
	}

	public void deleteMin()
	{
		if (this.empty()) throw new java.util.NoSuchElementException("empty heap");
		if(this.size == 1) {
			this.size = 0;
			this.last = null;
			this.min = null;
			this.numOfTrees = 0;
			return;
		}

		else if(this.min.rank == 0){
			HeapNode curr = this.min.next;
			while (curr.next!= this.min) {
				curr = curr.next;
			}
			curr.next = this.min.next;
			this.last = curr;
			this.setLast();
			setMin();
			this.size --;
			this.numOfTrees --;
			return;	
		}

		HeapNode child = this.min.child;
		child.parent = null;

		if (this.numOfTrees == 1) {
			this.numOfTrees = this.min.rank;
			this.min = child;
			this.size -= 1;
			this.last = child;
			this.resetParents(child);
			this.setMin();
			return;
		}

		BinomialHeap bin2 = new BinomialHeap((int)Math.pow(2, this.min.rank)-1, child, child, this.min.rank);
		
		if(child != null) {
			resetParents(child);
			bin2.setMin();
		}

		HeapNode curr = this.min.next;
		while(curr.next != this.min) {
			curr = curr.next;
		}
		curr.next = this.min.next;
		this.last = curr;
		this.min = curr;
		this.numOfTrees -= 1;
		this.size -= (1 + bin2.size);

		this.meld(bin2);
	}

	private void resetParents(HeapNode node) {
		HeapNode curr = node;
		do {
			curr.parent = null;
			curr = curr.next;
		} while (curr != node);
	}

	public void setMin()
	{
		
		HeapNode curr = this.last.next;
		HeapNode min = this.last;
		if (min.item.key > curr.item.key) {
			min = curr;
		}

		if (this.numOfTrees == 1 && curr != this.min) {
			this.min = this.last;
		}

		while(curr != this.last) {
			if(curr.item.key < min.item.key) {
				min = curr;
			}
			curr = curr.next;
		}
		this.min = min;
	} 

	public void setLast()
	{
		HeapNode last = this.last;
		HeapNode curr = last.next;
		
		if(curr.rank > last.rank) {
			last = curr;
		}
		
		while(curr != this.last) {
			if(curr.rank > last.rank) {
				last = curr;
			}
			curr = curr.next;
		}
		this.last = last;
	}

	public HeapItem findMin()
	{
		if (this.empty()) throw new java.util.NoSuchElementException("empty heap");
		return this.min.item;
	} 

	public void decreaseKey(HeapItem item, int diff) 
	{    
		item.key -= diff;
		HeapNode node = item.node;
		
		while(node.parent != null && node.parent.item.key > node.item.key) {
			HeapItem tmp = node.item;
			node.item = node.parent.item;
			node.parent.item = tmp;
			node.item.node = node;
			node.parent.item.node = node.parent;
			
			node = node.parent;
		}
		
		this.setMin();
	}

	public void delete(HeapItem item) 
	{    
		decreaseKey(item, (item.key + 1));
		this.deleteMin();
	}

	public void meld(BinomialHeap heap2)
	{
		if (heap2 == null || heap2 == this) throw new IllegalArgumentException("invalid donor heap");

		if(this.size() == 0) {
			this.last = heap2.last;
			this.size = heap2.size;
			this.min = heap2.min;
			this.numOfTrees = heap2.numOfTrees;
			return;
		}

		if(heap2.size == 0) {
			return;
		}

		int amountTrees1 = this.maxRank();
		int amountTrees2 = heap2.maxRank();
		this.size += heap2.size;
		int totalTrees = amountTrees1 + amountTrees2;
		
		HeapNode[] bucket1 = new HeapNode[totalTrees];
		HeapNode[] bucket2 = new HeapNode[totalTrees];
		HeapNode[] bucketTotal = new HeapNode[totalTrees];
		
		HeapNode pointer1 = this.last;
		for(int i=0; i<amountTrees1; i++) {
			int tmpRank = pointer1.rank;
			bucket1[tmpRank] = pointer1;
			pointer1 = pointer1.next;
		}
		
		HeapNode pointer2 = heap2.last;
		for(int i=0; i<amountTrees2; i++) {
			int tmpRank = pointer2.rank;
			bucket2[tmpRank] = pointer2;
			pointer2 = pointer2.next;
		}

		HeapNode carry = null;
		for(int i=0; i<bucketTotal.length ;i++) {
			if (bucket1[i] != null && bucket2[i] == null && carry == null) {
				bucketTotal[i] = bucket1[i];
			}
			else if (bucket1[i] == null && bucket2[i] != null && carry == null) {
				bucketTotal[i] = bucket2[i];
			}
			else if(bucket1[i] != null && bucket2[i] != null && carry == null) {
				carry = link(bucket1[i], bucket2[i]);
			}
			else if(bucket1[i] == null && bucket2[i] != null && carry != null) {
				carry = link(bucket2[i], carry);
			}
			else if(bucket1[i] != null && bucket2[i] == null && carry != null) {
				carry = link(bucket1[i], carry);
			}
			else if(bucket1[i] != null && bucket2[i] != null && carry != null) {
				bucketTotal[i] = carry;
				carry = link(bucket1[i], bucket2[i]);
			}
			else if(bucket1[i] == null && bucket2[i] == null && carry != null) {
				bucketTotal[i] = carry;
				carry = null;
			}
		}	

		int counter = 0;
		for(int i=0; i<bucketTotal.length ;i++) {
			if(bucketTotal[i] != null) {
				counter ++;
			}
		}
		
		this.numOfTrees = counter;
		HeapNode[] cleanBucket = new HeapNode[counter];
		
		int indexer = 0;
		for(int i=0; i<bucketTotal.length ;i++) {
			if(bucketTotal[i] != null) {
				cleanBucket[indexer] = bucketTotal[i];
				indexer ++;
			}
		}

		this.last = cleanBucket[cleanBucket.length-1];
		this.last.next = cleanBucket[0];
		
		for(int i=0; i<cleanBucket.length-1; i++) {
			cleanBucket[i].next = cleanBucket[i+1];
		}

		this.setMin();
		this.setLast();
	}

	public int size()
	{
		return this.size;
	}

	public boolean empty()
	{
		return this.size == 0;
	}

	public int numTrees()
	{	
		return this.numOfTrees;
	}

	public HeapNode link(HeapNode node1, HeapNode node2) {
		HeapNode smaller;
		HeapNode bigger;

		if(node1.item.key < node2.item.key) {
			smaller = node1;
			bigger = node2;
		}
		else {
			smaller = node2;
			bigger = node1;
		}

		HeapNode childOfSmaller = smaller.child;
		smaller.child = bigger;
		bigger.parent = smaller;
		smaller.rank ++;

		if(childOfSmaller == null) {
			bigger.next = bigger;
			return smaller;
		}
		bigger.next = childOfSmaller.next;
		childOfSmaller.next = bigger;
		
		return smaller;
	}

	public int maxRank() {
		return (int)(Math.log(this.size)/Math.log(2)) + 1;
	}

	public class HeapNode{
		public HeapItem item;
		public HeapNode child;
		public HeapNode next;
		public HeapNode parent;
		public int rank;

		public HeapNode() {
			this.item = null;
			this.child = null;
			this.next = null;
			this.parent = null;
			this.rank = -1;
		}

		public HeapNode(HeapItem item, HeapNode child, HeapNode next, HeapNode parent, int rank) {
			this.item = item;
			this.child = child;
			this.next = next;
			this.parent = parent;
			this.rank = rank;
		}
	}

	public class HeapItem{
		public HeapNode node;
		public int key;
		public String info;

		public HeapItem(HeapNode node, int key, String info) {
			this.node = node;
			this.key = key;
			this.info = info;
		}
	}

}
