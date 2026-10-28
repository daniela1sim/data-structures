.PHONY: test test-avl test-heap clean

test: test-avl test-heap

test-avl:
	python -m unittest discover -s avl-tree/tests -v

test-heap:
	javac -d binomial-heap/build binomial-heap/src/BinomialHeap/BinomialHeap.java binomial-heap/tests/BinomialHeapTest.java
	java -cp binomial-heap/build BinomialHeapTest

clean:
	rm -rf binomial-heap/build
