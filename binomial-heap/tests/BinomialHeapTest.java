import BinomialHeap.BinomialHeap;
import java.util.*;

public final class BinomialHeapTest {
    private static int passed = 0;
    private static void check(boolean value, String message) { if (!value) throw new AssertionError(message); }
    private static void run(String label, Runnable check) {
        check.run(); System.out.println("PASS " + label); passed++;
    }
    private static void verify(BinomialHeap heap) {
        if (heap.size() == 0) {
            check(heap.empty(), "empty flag");
            check(heap.last == null && heap.min == null && heap.numTrees() == 0, "empty metadata");
            return;
        }
        check(heap.last != null && heap.min != null, "nonempty metadata");
        Set<BinomialHeap.HeapNode> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        Set<Integer> ranks = new HashSet<>();
        BinomialHeap.HeapNode cur = heap.last.next;
        int roots = 0;
        int min = Integer.MAX_VALUE;
        do {
            check(cur != null, "null root link");
            check(cur.parent == null, "root has parent");
            check(ranks.add(cur.rank), "duplicate root rank");
            check(cur.rank >= 0, "negative root rank");
            min = Math.min(min, cur.item.key);
            verifyTree(cur, seen);
            cur = cur.next;
            roots++;
            check(roots <= heap.size(), "root ring never terminates");
        } while(cur != heap.last.next);
        check(roots == heap.numTrees(), "root count mismatch");
        check(seen.size() == heap.size(), "reachable node count mismatch");
        check(heap.min.item.key == min, "min metadata wrong");
    }
    private static void verifyTree(BinomialHeap.HeapNode node, Set<BinomialHeap.HeapNode> seen) {
        check(seen.add(node), "duplicate or cyclic node");
        check(node.item != null && node.item.node == node, "item handle does not point at containing node");
        if (node.rank == 0) {
            check(node.child == null, "rank-zero node has child");
            return;
        }
        check(node.child != null, "positive-rank node has no child");
        BinomialHeap.HeapNode child = node.child;
        int count = 0;
        Set<Integer> ranks = new HashSet<>();
        do {
            check(child != null, "null sibling link");
            check(child.parent == node, "incorrect parent link");
            check(child.item.key >= node.item.key, "heap-order violation");
            check(ranks.add(child.rank), "duplicate child rank");
            BinomialHeap.HeapNode next = child.next;
            verifyTree(child,seen);
            child = next;
            count++;
            check(count <= node.rank, "child ring malformed");
        } while(child != node.child);
        check(count == node.rank, "rank and child count differ");
    }
    public static void main(String[] args) {
        run("empty heap", () -> verify(new BinomialHeap()));
        run("insertion and min", () -> {
            BinomialHeap h=new BinomialHeap();
            for(int x : new int[]{10,3,12,1,8,5,2,6}) { h.insert(x,"item-"+x);verify(h); }
            check(h.findMin().key==1,"minimum incorrect");
        });
        run("repeated deleteMin matches PriorityQueue", () -> {
            for (int seed=0;seed<12;seed++) {
                BinomialHeap h=new BinomialHeap();PriorityQueue<Integer> pq=new PriorityQueue<>();
                Random rand=new Random(seed);
                for(int i=0;i<45;i++){int x=1+rand.nextInt(1000);h.insert(x,"x");pq.add(x);verify(h);}
                while(!pq.isEmpty()) {check(h.findMin().key==pq.remove(),"min mismatch");h.deleteMin();verify(h);}
                check(h.empty(),"expected empty");
            }
        });
        run("meld retains keys", () -> {
            BinomialHeap a=new BinomialHeap(),b=new BinomialHeap();
            for(int x:new int[]{7,2,12,9,10})a.insert(x,"a");
            for(int x:new int[]{6,1,5,11,3,8})b.insert(x,"b");
            a.meld(b);verify(a);
            int prev=Integer.MIN_VALUE;
            while(!a.empty()){int val=a.findMin().key;check(val>=prev,"wrong order after meld");prev=val;a.deleteMin();verify(a);}
        });
        run("decreaseKey retains item handles", () -> {
            BinomialHeap h=new BinomialHeap();
            BinomialHeap.HeapItem[] items=new BinomialHeap.HeapItem[15];
            for(int i=0;i<15;i++)items[i]=h.insert(i*5+20,"item"+i);
            verify(h);
            h.decreaseKey(items[13], 70);verify(h);
            check(items[13].node.item==items[13],"decreased item handle became stale");
        });
        run("delete arbitrary item", () -> {
            BinomialHeap h=new BinomialHeap();
            BinomialHeap.HeapItem[] items=new BinomialHeap.HeapItem[20];
            for(int i=0;i<20;i++)items[i]=h.insert(10+i,"i"+i);
            h.delete(items[10]);verify(h);
            check(h.size()==19,"delete did not remove exactly one element");
            while(!h.empty()) {check(h.findMin().info.equals("i10")==false,"deleted item still present");h.deleteMin();verify(h);}
        });
        System.out.println("Passed " + passed + " Java tests");
    }
}
