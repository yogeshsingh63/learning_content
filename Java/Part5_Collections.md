# Part 5: Java Collections Framework — Complete Mastery Guide
### Internals, Complexity, Thread Safety, C++ STL Comparisons | Backend SDE Interview Handbook

---

> **How to use this document:** Every collection is covered with internal implementation, time/space complexity, real-world use cases, pitfalls, and interview questions. Read all sections for full depth.

---

# Table of Contents

1. [Collections Framework Overview](#1-collections-framework-overview)
2. [Iterable, Collection, and the Hierarchy](#2-iterable-collection-and-the-hierarchy)
3. [ArrayList — Dynamic Array](#3-arraylist--dynamic-array)
4. [LinkedList — Doubly Linked List](#4-linkedlist--doubly-linked-list)
5. [Vector & Stack (Legacy)](#5-vector--stack-legacy)
6. [Queue & Deque](#6-queue--deque)
7. [PriorityQueue — Heap-Based Queue](#7-priorityqueue--heap-based-queue)
8. [HashMap — Hash Table](#8-hashmap--hash-table)
9. [LinkedHashMap — Insertion-Ordered Map](#9-linkedhashmap--insertion-ordered-map)
10. [TreeMap — Red-Black Tree Map](#10-treemap--red-black-tree-map)
11. [HashSet, LinkedHashSet, TreeSet](#11-hashset-linkedhashset-treeset)
12. [ConcurrentHashMap & Thread-Safe Collections](#12-concurrenthashmap--thread-safe-collections)
13. [Comparable & Comparator](#13-comparable--comparator)
14. [Iterators — Fail-Fast vs Fail-Safe](#14-iterators--fail-fast-vs-fail-safe)
15. [Generics in Collections](#15-generics-in-collections)
16. [Collections Utility Class](#16-collections-utility-class)
17. [C++ STL vs Java Collections](#17-c-stl-vs-java-collections)
18. [Interview Quick Reference](#18-interview-quick-reference)

---

# 1. Collections Framework Overview

## What is the Collections Framework?

The Java Collections Framework is a unified architecture for storing and manipulating groups of objects. It provides:
- **Interfaces** — abstract data types (List, Set, Queue, Map)
- **Implementations** — concrete classes (ArrayList, HashMap, TreeSet)
- **Algorithms** — static methods in `Collections` and `Arrays` utilities

## The Full Hierarchy

```
java.lang.Iterable<E>
    └── java.util.Collection<E>
            ├── List<E>
            │     ├── ArrayList<E>
            │     ├── LinkedList<E>
            │     ├── Vector<E>
            │     │     └── Stack<E>
            │     └── CopyOnWriteArrayList<E>
            │
            ├── Set<E>
            │     ├── HashSet<E>
            │     │     └── LinkedHashSet<E>
            │     ├── TreeSet<E>         (implements SortedSet, NavigableSet)
            │     └── CopyOnWriteArraySet<E>
            │
            └── Queue<E>
                  ├── LinkedList<E>      (also implements List!)
                  ├── PriorityQueue<E>
                  ├── ArrayDeque<E>      (also implements Deque)
                  └── Deque<E>
                        ├── ArrayDeque<E>
                        └── LinkedList<E>

java.util.Map<K,V>   (NOT in Collection hierarchy)
    ├── HashMap<K,V>
    │     └── LinkedHashMap<K,V>
    ├── TreeMap<K,V>          (implements SortedMap, NavigableMap)
    ├── Hashtable<K,V>        (legacy, synchronized)
    │     └── Properties
    └── ConcurrentHashMap<K,V>
```

## Interface Responsibilities

| Interface | Allows Duplicates | Ordered | Indexed | Sorted |
|-----------|------------------|---------|---------|--------|
| `List` | Yes | Yes (insertion) | Yes | No |
| `Set` | No | Depends | No | TreeSet only |
| `Queue` | Yes | Yes (FIFO/priority) | No | PriorityQueue only |
| `Map` (keys) | No | Depends | No | TreeMap only |

---

# 2. Iterable, Collection, and the Hierarchy

## Iterable<E>

The root of all collections. Implementing this interface enables `for-each` loop syntax:

```java
public interface Iterable<E> {
    Iterator<E> iterator();   // must provide an Iterator
}

// Any class implementing Iterable can be used in for-each:
class Range implements Iterable<Integer> {
    private int start, end;
    Range(int s, int e) { start = s; end = e; }

    @Override
    public Iterator<Integer> iterator() {
        return new Iterator<>() {
            int current = start;
            public boolean hasNext() { return current < end; }
            public Integer next()    { return current++; }
        };
    }
}

// Now usable in for-each:
for (int n : new Range(1, 6)) {
    System.out.print(n + " ");  // 1 2 3 4 5
}
```

## Collection<E>

Extends Iterable. Adds core operations shared by all collections:

```java
public interface Collection<E> extends Iterable<E> {
    int size();
    boolean isEmpty();
    boolean contains(Object o);
    boolean add(E e);
    boolean remove(Object o);
    boolean containsAll(Collection<?> c);
    boolean addAll(Collection<? extends E> c);
    boolean removeAll(Collection<?> c);
    boolean retainAll(Collection<?> c);  // intersection
    void clear();
    Object[] toArray();
    <T> T[] toArray(T[] a);
    default Stream<E> stream() { ... }
    default Stream<E> parallelStream() { ... }
}
```

## List<E>

Extends Collection. Adds positional access and ordered iteration:

```java
public interface List<E> extends Collection<E> {
    E get(int index);
    E set(int index, E element);
    void add(int index, E element);
    E remove(int index);
    int indexOf(Object o);
    int lastIndexOf(Object o);
    List<E> subList(int fromIndex, int toIndex);
    ListIterator<E> listIterator();
}
```

---

# 3. ArrayList — Dynamic Array

## Internal Implementation

`ArrayList` is backed by a plain Java array (`Object[]`). When capacity is exceeded, it grows.

```
Initial state (capacity=10):
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │   ← backing array
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
  ↑   ↑   ↑   ↑
 [A] [B] [C] [D]  size=4, capacity=10

After adding 7 more elements (size=10=capacity):
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ A │ B │ C │...│...│...│...│...│...│ K │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
                                           ← FULL!

Adding one more triggers resize:
  newCapacity = oldCapacity + (oldCapacity >> 1)  = 10 + 5 = 15
  Arrays.copyOf(array, 15) → new array of 15 slots
  old array eligible for GC
```

### Source Code (Simplified)

```java
public class ArrayList<E> {
    private static final int DEFAULT_CAPACITY = 10;
    private Object[] elementData;
    private int size;

    public ArrayList() {
        this.elementData = new Object[DEFAULT_CAPACITY];
        this.size = 0;
    }

    public boolean add(E e) {
        ensureCapacity(size + 1);
        elementData[size++] = e;
        return true;
    }

    private void ensureCapacity(int minCapacity) {
        if (minCapacity > elementData.length) {
            int newCapacity = elementData.length + (elementData.length >> 1); // ×1.5
            if (newCapacity < minCapacity) newCapacity = minCapacity;
            elementData = Arrays.copyOf(elementData, newCapacity);  // O(n) copy!
        }
    }

    @SuppressWarnings("unchecked")
    public E get(int index) {
        if (index >= size) throw new IndexOutOfBoundsException();
        return (E) elementData[index];    // O(1) random access
    }

    public void add(int index, E element) {
        ensureCapacity(size + 1);
        // Shift elements right — O(n)
        System.arraycopy(elementData, index, elementData, index + 1, size - index);
        elementData[index] = element;
        size++;
    }

    public E remove(int index) {
        E old = get(index);
        int numMoved = size - index - 1;
        if (numMoved > 0)
            System.arraycopy(elementData, index + 1, elementData, index, numMoved);
        elementData[--size] = null;  // null out for GC
        return old;
    }
}
```

## Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `get(i)` | **O(1)** | Direct array access by index |
| `add(e)` (end) | **O(1)** amortized | O(n) when resize happens |
| `add(i, e)` (middle) | **O(n)** | Must shift elements right |
| `remove(i)` (middle) | **O(n)** | Must shift elements left |
| `remove(object)` | **O(n)** | Linear search + shift |
| `contains(o)` | **O(n)** | Linear scan |
| `size()` | **O(1)** | Stored as field |

## Space Complexity

O(n) for n elements, but capacity may be up to 1.5× the actual size after a resize. You can call `trimToSize()` to reclaim unused capacity.

## Usage

```java
List<String> list = new ArrayList<>();  // always program to interface
list.add("apple");
list.add("banana");
list.add(0, "cherry");    // insert at index 0

list.get(0);              // "cherry" — O(1)
list.size();              // 3
list.contains("banana");  // true — O(n)
list.remove("banana");    // remove by value — O(n)
list.remove(0);           // remove by index — O(n) shift

// Bulk operations
list.addAll(Arrays.asList("d", "e", "f"));
list.removeIf(s -> s.startsWith("d"));  // Java 8+

// Iteration
for (String s : list) { System.out.println(s); }
list.forEach(System.out::println);     // Java 8+

// Convert to array
String[] arr = list.toArray(new String[0]);

// Sort
Collections.sort(list);
list.sort(Comparator.naturalOrder());
list.sort(String::compareTo);
```

## Pre-sizing for Performance

```java
// If you know approximate size upfront:
List<Integer> numbers = new ArrayList<>(10_000);  // preallocate, avoids resizes
for (int i = 0; i < 10_000; i++) numbers.add(i);
```

## When to Use ArrayList

- **General-purpose** list — the default choice
- **Frequent random access** by index
- **Frequent add/remove at end**
- **Infrequent insert/delete in middle**

## C++ Equivalent

`std::vector<T>` — nearly identical: dynamic array, O(1) access, amortized O(1) append, grows by ~2× (Java grows by 1.5×).

---

# 4. LinkedList — Doubly Linked List

## Internal Implementation

```
LinkedList backing structure:
                                       head                tail
                                         ↓                   ↓
null ← [prev|"A"|next] ↔ [prev|"B"|next] ↔ [prev|"C"|next] → null
             Node               Node               Node

Each Node:
┌──────────────────────────┐
│  Node<E> prev            │
│  E       item            │
│  Node<E> next            │
└──────────────────────────┘
```

Java's `LinkedList` is a **doubly-linked list** that also implements `Deque` — it can be used as a list, queue, stack, or deque.

```java
// Simplified internal node
private static class Node<E> {
    E item;
    Node<E> next;
    Node<E> prev;

    Node(Node<E> prev, E element, Node<E> next) {
        this.item = element;
        this.next = next;
        this.prev = prev;
    }
}
```

## Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `get(i)` | **O(n)** | Must traverse from head or tail |
| `add(e)` (end) | **O(1)** | Direct tail access |
| `add(e)` (front) | **O(1)** | Direct head access |
| `add(i, e)` | **O(n)** | Traverse to position, then O(1) insert |
| `remove(head/tail)` | **O(1)** | Direct head/tail access |
| `remove(i)` | **O(n)** | Traverse first |
| `contains(o)` | **O(n)** | Linear scan |

## Usage as List, Queue, and Deque

```java
LinkedList<String> list = new LinkedList<>();

// As List:
list.add("B");
list.add(0, "A");         // add at front
list.add("C");
list.get(1);              // "B" — O(n)!

// As Queue (FIFO):
list.offer("X");           // add to tail
list.poll();               // remove from head
list.peek();               // look at head without removing

// As Deque (double-ended queue):
list.addFirst("start");
list.addLast("end");
list.removeFirst();
list.removeLast();
list.peekFirst();
list.peekLast();

// As Stack (LIFO):
list.push("top");   // = addFirst
list.pop();         // = removeFirst
```

## ArrayList vs LinkedList — The Real Tradeoff

This is one of the most common interview topics:

| Operation | ArrayList | LinkedList |
|-----------|-----------|------------|
| Random access `get(i)` | **O(1)** ← winner | O(n) |
| Insert/delete at **end** | O(1) amortized | O(1) |
| Insert/delete at **front** | O(n) | **O(1)** ← winner |
| Insert/delete at **middle** | O(n) | O(n) (traverse + O(1) link) |
| Memory per element | Less (array slot) | More (two pointers + object wrapper) |
| Cache performance | Better (contiguous) | Worse (pointer chasing) |
| Iterator traversal | Slightly faster (cache) | Slightly slower |

**In practice, ArrayList almost always wins:**
- CPUs are very fast at array operations due to cache locality
- LinkedList's pointer chasing is cache-unfriendly (each node may be far apart in memory)
- The overhead of `Node` objects (3 fields per element) makes LinkedList memory-heavy

**Use LinkedList when:**
- Frequent insertions/deletions at the head specifically
- Using it as a Queue/Deque (not as a random-access List)

## C++ Equivalent

`std::list<T>` — doubly-linked list, same O complexities. C++ also has `std::forward_list<T>` (singly-linked, not in Java).

---

# 5. Vector & Stack (Legacy)

## Vector — Synchronized ArrayList

`Vector` is like `ArrayList` but **all methods are synchronized** — thread-safe but slow due to locking overhead. It also grows by **doubling** (2×) vs ArrayList's 1.5×.

```java
Vector<String> v = new Vector<>();
v.add("a");
v.add("b");

// Every method acquires a lock — expensive in single-threaded code
// Use ArrayList for single-threaded, CopyOnWriteArrayList or Collections.synchronizedList for multithreaded
```

**Verdict:** Legacy class — avoid in new code. Use `ArrayList` (not thread-safe) or `CopyOnWriteArrayList` (thread-safe, good for read-heavy workloads).

## Stack — LIFO Stack (Legacy)

`Stack extends Vector` — a fundamental design mistake. It exposes `get(index)`, `add(index, element)` etc. which violate LIFO semantics.

```java
// Legacy Stack:
Stack<Integer> stack = new Stack<>();
stack.push(1);
stack.push(2);
stack.pop();    // 2
stack.peek();   // 1
stack.add(0, 99);  // WRONG — breaks LIFO! but allowed because extends Vector

// Modern replacement — use ArrayDeque as a stack:
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1);
stack.push(2);
stack.pop();    // 2
stack.peek();   // 1
// No broken methods exposed!
```

**C++ equivalent:** `std::stack<T>` (adapter over `std::deque` by default) — properly encapsulated.

---

# 6. Queue & Deque

## Queue Interface

```java
public interface Queue<E> extends Collection<E> {
    boolean offer(E e);   // add to tail (returns false if full, no exception)
    E poll();             // remove from head (returns null if empty, no exception)
    E peek();             // look at head (returns null if empty, no exception)

    // Throwing variants:
    boolean add(E e);     // throws IllegalStateException if full
    E remove();           // throws NoSuchElementException if empty
    E element();          // throws NoSuchElementException if empty
}
```

Always prefer `offer/poll/peek` over `add/remove/element` — they handle edge cases gracefully.

## Deque Interface (Double-Ended Queue)

```java
public interface Deque<E> extends Queue<E> {
    void addFirst(E e);  void addLast(E e);
    E    removeFirst();  E    removeLast();
    E    peekFirst();    E    peekLast();
    void push(E e);      // = addFirst
    E    pop();          // = removeFirst
    // Also has offer/poll variants for both ends
}
```

## ArrayDeque — The Best General-Purpose Queue/Stack

`ArrayDeque` is backed by a **circular array** — much more efficient than `LinkedList` for queue/stack operations:

```
Circular array (capacity 8):
index:  0    1    2    3    4    5    6    7
       [  ] [ A] [ B] [ C] [ D] [  ] [  ] [  ]
              ↑                   ↑
            head                 tail

Adding to front: moves head pointer left (wraps around)
Adding to rear:  moves tail pointer right (wraps around)
Both O(1) without moving any elements!
```

```java
// ArrayDeque as Queue (FIFO):
Queue<String> queue = new ArrayDeque<>();
queue.offer("first");
queue.offer("second");
queue.offer("third");
queue.poll();   // "first" — removes from head
queue.peek();   // "second" — looks at head

// ArrayDeque as Stack (LIFO):
Deque<String> stack = new ArrayDeque<>();
stack.push("first");
stack.push("second");
stack.pop();    // "second" — removes from front
stack.peek();   // "first"

// ArrayDeque as Deque:
Deque<String> deque = new ArrayDeque<>();
deque.addFirst("front");
deque.addLast("back");
deque.removeFirst();
deque.removeLast();
```

**ArrayDeque vs LinkedList for Queue:**
- ArrayDeque is **faster** (no node allocation, better cache locality)
- ArrayDeque uses less memory (no Node wrapper objects)
- Use ArrayDeque as your default Queue/Deque/Stack

**C++ equivalent:** `std::deque<T>` (double-ended queue, but uses segmented arrays, not a single circular array).

---

# 7. PriorityQueue — Heap-Based Queue

## Internal Implementation

`PriorityQueue` is backed by a **min-heap** (binary heap in an array). The smallest element is always at the head.

```
Min-Heap storing: 1, 3, 5, 7, 8, 9, 12

Array representation:
Index:  0    1    2    3    4    5    6
       [ 1] [ 3] [ 5] [ 7] [ 8] [ 9] [12]

Tree visualization:
            1            ← minimum is always at root
          /   \
         3     5
        / \   / \
       7   8 9  12

Parent of i: (i-1)/2
Left child of i: 2*i+1
Right child of i: 2*i+2
```

### Heap Operations

**Insert (offer):** Add to end, bubble up (sift up):
```
Add 2: [1,3,5,7,8,9,12,2] → 2 at index 7, parent=(7-1)/2=3 → arr[3]=7 > 2, swap
       [1,3,5,2,8,9,12,7] → 2 at index 3, parent=(3-1)/2=1 → arr[1]=3 > 2, swap
       [1,2,5,3,8,9,12,7] → 2 at index 1, parent=0 → arr[0]=1 < 2, stop
```

**Remove min (poll):** Remove root, move last element to root, sift down:
```
Remove 1: Move 7 to root: [7,2,5,3,8,9,12]
         Sift down: 7 > min(2,5)=2, swap with 2: [2,7,5,3,8,9,12]
                    7 > min(3,8)=3, swap with 3: [2,3,5,7,8,9,12]
                    7 is leaf → done
```

## Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `offer(e)` | **O(log n)** | Insert + sift up |
| `poll()` | **O(log n)** | Remove min + sift down |
| `peek()` | **O(1)** | Root is always min |
| `contains(o)` | **O(n)** | No index structure |
| `remove(o)` | **O(n)** | Find O(n) + remove O(log n) |
| Build from collection | **O(n)** | Heapify is O(n) |

## Usage

```java
// Default: min-heap (natural ordering)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(5);
minHeap.offer(1);
minHeap.offer(3);
minHeap.poll();  // 1 (minimum)
minHeap.poll();  // 3
minHeap.poll();  // 5

// Max-heap with reverse order comparator
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
maxHeap.offer(5); maxHeap.offer(1); maxHeap.offer(3);
maxHeap.poll();  // 5 (maximum)

// Custom objects
PriorityQueue<Task> taskQueue = new PriorityQueue<>(
    Comparator.comparingInt(Task::getPriority)
);
taskQueue.offer(new Task("Low priority", 3));
taskQueue.offer(new Task("High priority", 1));
taskQueue.poll();  // Task with priority=1 (lowest number = highest priority)

// Iteration does NOT guarantee sorted order!
// poll() does, but for-each does not
for (Integer i : minHeap) {
    System.out.println(i);  // NOT necessarily sorted!
}
```

## Important: Iteration is NOT Sorted

```java
PriorityQueue<Integer> pq = new PriorityQueue<>(Arrays.asList(5,1,3,2,4));

// WRONG assumption:
for (int i : pq) System.out.print(i + " ");  // might print: 1 2 3 5 4 (heap order, not sorted)

// CORRECT way to drain in order:
while (!pq.isEmpty()) System.out.print(pq.poll() + " ");  // 1 2 3 4 5
```

**C++ equivalent:** `std::priority_queue<T>` — max-heap by default (Java is min-heap by default — opposite!).

---

# 8. HashMap — Hash Table

## Internal Implementation (Java 8+)

`HashMap` uses an **array of buckets**, where each bucket is either:
- A singly-linked list (for ≤8 entries in the bucket)
- A **Red-Black Tree** (for >8 entries — Java 8+ optimization, reduces worst case from O(n) to O(log n))

```
HashMap (capacity=16, initial):

Backing array: table[]
 ┌──────────────────────────────────────────────────────────┐
 │ [0] null                                                 │
 │ [1] → Node("alice"→30) → null                           │
 │ [2] null                                                 │
 │ [3] → Node("bob"→25) → Node("charlie"→35) → null        │  ← collision: chain
 │ [4] null                                                 │
 │ ...                                                      │
 │ [15] → Node("zara"→28) → null                           │
 └──────────────────────────────────────────────────────────┘

Each Node:
┌─────────────────────────────────────┐
│  int    hash   (cached hashCode)    │
│  K      key                         │
│  V      value                       │
│  Node   next   (linked list chain)  │
└─────────────────────────────────────┘
```

### How put(key, value) Works

```java
// Step-by-step internals:
map.put("alice", 30);

// 1. Compute hash:
int hash = hash("alice");  // spread bits to reduce clustering
// Java's hash: h = key.hashCode(); return h ^ (h >>> 16);

// 2. Find bucket index:
int index = hash & (capacity - 1);  // fast modulo using bitwise AND (capacity always power of 2)

// 3. Check bucket:
//    - Empty → create new Node, place it
//    - Non-empty → check each node:
//        key == existing.key || key.equals(existing.key) → update value
//        No match → append to chain (or tree if chain length > 8)

// 4. Check load factor:
if (++size > capacity * loadFactor) {  // loadFactor=0.75 by default
    resize();  // double capacity, rehash all entries — O(n)
}
```

### Load Factor and Resizing

```
Default capacity: 16
Default load factor: 0.75

Resize threshold: 16 × 0.75 = 12

When 12 entries are added → resize to 32
When 24 entries are added → resize to 64
...

Lower load factor = fewer collisions, more memory usage
Higher load factor = more collisions, less memory usage
0.75 is the empirical sweet spot (balanced)
```

### Java 8 Treeification

When a single bucket's chain exceeds **TREEIFY_THRESHOLD = 8** entries, the chain is converted to a Red-Black Tree:
- Lookup in chain: O(n) → becomes O(log n) in tree
- This prevents denial-of-service attacks where an attacker crafts inputs that all hash to the same bucket

## Time Complexity

| Operation | Average | Worst Case | Notes |
|-----------|---------|-----------|-------|
| `put(k,v)` | **O(1)** | O(log n) (treeified bucket) | Amortized including resize |
| `get(k)` | **O(1)** | O(log n) | Hash lookup + equals check |
| `remove(k)` | **O(1)** | O(log n) | |
| `containsKey(k)` | **O(1)** | O(log n) | |
| `containsValue(v)` | **O(n)** | O(n) | Must scan all buckets |

## Usage

```java
Map<String, Integer> scores = new HashMap<>();

// Put
scores.put("Alice", 95);
scores.put("Bob", 87);
scores.put("Alice", 98);    // updates Alice's score (key already exists)

// Get
scores.get("Alice");        // 98
scores.get("Charlie");      // null (key not present)
scores.getOrDefault("Charlie", 0);  // 0 — safer

// Check
scores.containsKey("Bob");       // true
scores.containsValue(98);        // true (O(n)!)

// Remove
scores.remove("Bob");            // removes entry, returns 87
scores.remove("Alice", 95);      // conditional remove — only if value matches

// Modern API (Java 8+)
scores.putIfAbsent("Dave", 100);           // only puts if key not present
scores.computeIfAbsent("Eve", k -> 80);   // compute and put if absent
scores.merge("Alice", 5, Integer::sum);    // Alice's score += 5

// Iterate
for (Map.Entry<String, Integer> e : scores.entrySet()) {
    System.out.println(e.getKey() + " → " + e.getValue());
}

scores.forEach((k, v) -> System.out.println(k + " → " + v));  // Java 8+

// Keys, values, entries as collections
Set<String> keys       = scores.keySet();
Collection<Integer> vals = scores.values();
Set<Map.Entry<String,Integer>> entries = scores.entrySet();
```

## Key Requirements: hashCode() and equals()

`HashMap` requires that keys properly implement `hashCode()` and `equals()`:

```java
// Contract:
// 1. If a.equals(b), then a.hashCode() == b.hashCode()   (MUST)
// 2. If a.hashCode() == b.hashCode(), a.equals(b) MAY OR MAY NOT be true (collision)

class Point {
    int x, y;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Point)) return false;
        Point p = (Point) o;
        return x == p.x && y == p.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);  // uses both fields — good distribution
    }
}

// Now Point works correctly as HashMap key:
Map<Point, String> map = new HashMap<>();
map.put(new Point(1, 2), "origin offset");
map.get(new Point(1, 2));  // returns "origin offset" — equals() finds it
```

**Common bug:** Using mutable objects as keys. If you put an object as a key, then mutate it (changing its hashCode), you'll never find it again:

```java
List<Integer> key = new ArrayList<>(Arrays.asList(1, 2, 3));
map.put(key, "value");
key.add(4);                  // MUTATED the key!
map.get(key);                // null — hashCode changed, wrong bucket
```

**Rule: HashMap keys should be immutable (String, Integer, enums are all immutable).**

## null Handling

```java
Map<String, Integer> map = new HashMap<>();
map.put(null, 42);          // null KEY is allowed (stored in bucket 0)
map.put("key", null);       // null VALUE is allowed
map.get(null);              // 42
```

## C++ Equivalent

`std::unordered_map<K,V>` — hash map, average O(1), similar structure. C++ uses separate chaining or open addressing depending on implementation.

---

# 9. LinkedHashMap — Insertion-Ordered Map

## Internal Implementation

`LinkedHashMap extends HashMap` and adds a **doubly-linked list** threading through all entries in insertion order (or access order):

```
LinkedHashMap (insertion order):

HashMap buckets: (same as HashMap)
┌────────────────────────────────────────┐
│ bucket[1] → Entry(alice,30)            │
│ bucket[3] → Entry(bob,25)             │
└────────────────────────────────────────┘

PLUS doubly-linked list:
HEAD ↔ Entry(alice,30) ↔ Entry(bob,25) ↔ Entry(charlie,35) ↔ TAIL
         (inserted first)                  (inserted last)
```

Each entry has extra `before` and `after` pointers:
```java
static class Entry<K,V> extends HashMap.Node<K,V> {
    Entry<K,V> before, after;  // extra links for doubly-linked list
}
```

## Access-Ordered LinkedHashMap — LRU Cache!

```java
// accessOrder=true → most-recently accessed is moved to tail
Map<Integer, String> lruCache = new LinkedHashMap<>(16, 0.75f, true) {
    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, String> eldest) {
        return size() > 100;  // evict oldest when cache exceeds 100 entries
    }
};

lruCache.put(1, "one");
lruCache.put(2, "two");
lruCache.put(3, "three");
lruCache.get(1);   // access 1 → moves to tail (most recently used)
// Order now: [2, 3, 1]
// If capacity exceeded, entry at HEAD (2) is evicted first
```

This is the canonical Java LRU Cache implementation using LinkedHashMap!

## Time Complexity

Same as HashMap for all operations (O(1) average), with slightly higher constant due to maintaining the linked list. Iteration is O(n) in insertion/access order.

## Usage

```java
Map<String, Integer> linked = new LinkedHashMap<>();
linked.put("banana", 2);
linked.put("apple", 1);
linked.put("cherry", 3);

// Iteration is always in insertion order:
for (String key : linked.keySet()) {
    System.out.println(key);  // banana, apple, cherry (insertion order preserved)
}
// HashMap would give unpredictable order
```

**When to use:**
- Need predictable iteration order (insertion order)
- Implementing LRU cache
- Need both O(1) lookup AND ordered iteration

---

# 10. TreeMap — Red-Black Tree Map

## Internal Implementation

`TreeMap` is backed by a **Red-Black Tree** — a self-balancing BST where all keys are kept in sorted order.

```
TreeMap containing: {"bob":25, "alice":30, "charlie":35, "dave":28}

Red-Black Tree (sorted by key):
              bob(B)
             /      \
         alice(R)  charlie(B)
                      /
                   dave(R)

B=Black, R=Red
Keys always in sorted order (alice < bob < charlie < dave)
```

## Time Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| `put(k,v)` | **O(log n)** | BST insert + rebalance |
| `get(k)` | **O(log n)** | BST search |
| `remove(k)` | **O(log n)** | BST delete + rebalance |
| `firstKey()` | **O(log n)** | Leftmost node |
| `lastKey()` | **O(log n)** | Rightmost node |
| Iteration | **O(n)** | In-order traversal = sorted |

TreeMap is slower than HashMap for basic operations but provides **sorted order** and powerful **navigation methods**.

## Usage — NavigableMap API

```java
TreeMap<String, Integer> treeMap = new TreeMap<>();
treeMap.put("charlie", 3);
treeMap.put("alice", 1);
treeMap.put("bob", 2);
treeMap.put("dave", 4);

// Sorted access:
treeMap.firstKey();          // "alice"
treeMap.lastKey();           // "dave"

// Range queries:
treeMap.headMap("charlie");  // {alice→1, bob→2} (strictly less than "charlie")
treeMap.tailMap("bob");      // {bob→2, charlie→3, dave→4} (>= "bob")
treeMap.subMap("alice", "charlie");  // {alice→1, bob→2}

// Floor/ceiling (closest key):
treeMap.floorKey("cat");    // "charlie" — largest key ≤ "cat"
treeMap.ceilingKey("cat");  // "charlie" — smallest key ≥ "cat"
treeMap.lowerKey("charlie"); // "bob" — strictly less than "charlie"
treeMap.higherKey("bob");    // "charlie" — strictly greater than "bob"

// Reverse view:
treeMap.descendingMap().forEach((k,v) -> System.out.println(k));  // dave,charlie,bob,alice
```

**When to use TreeMap:**
- Keys must be in sorted order
- Need range queries (all keys between X and Y)
- Need floor/ceiling operations
- When ordering matters more than raw speed

**C++ equivalent:** `std::map<K,V>` — Red-Black Tree internally, same O(log n) operations.

---

# 11. HashSet, LinkedHashSet, TreeSet

Sets store **unique elements only** — no duplicates.

## HashSet

Backed by a `HashMap<E, PRESENT>` (values are all a dummy `PRESENT` object):

```java
// Internally:
private transient HashMap<E, Object> map;
private static final Object PRESENT = new Object();  // dummy value

public boolean add(E e) {
    return map.put(e, PRESENT) == null;  // returns true if new element
}
```

```java
Set<String> set = new HashSet<>();
set.add("apple");
set.add("banana");
set.add("apple");    // duplicate — ignored, set unchanged
set.size();          // 2

set.contains("banana");  // true — O(1)
set.remove("apple");     // O(1)

// No guaranteed order in iteration
for (String s : set) System.out.println(s);  // unpredictable order
```

**Complexities:** O(1) add/remove/contains average (same as HashMap). O(n) space.

## LinkedHashSet

Backed by `LinkedHashMap` — maintains **insertion order**:

```java
Set<String> linked = new LinkedHashSet<>();
linked.add("banana");
linked.add("apple");
linked.add("cherry");

for (String s : linked) System.out.println(s);  // banana, apple, cherry (insertion order)
```

## TreeSet

Backed by `TreeMap` — elements stored in **sorted order**:

```java
TreeSet<Integer> treeSet = new TreeSet<>();
treeSet.add(5); treeSet.add(1); treeSet.add(3); treeSet.add(2); treeSet.add(4);

// Always sorted:
System.out.println(treeSet);  // [1, 2, 3, 4, 5]

treeSet.first();         // 1
treeSet.last();          // 5
treeSet.headSet(3);      // [1, 2] — strictly less than 3
treeSet.tailSet(3);      // [3, 4, 5] — >= 3
treeSet.subSet(2, 4);    // [2, 3] — [2, 4)
treeSet.floor(3);        // 3 — largest ≤ 3
treeSet.ceiling(3);      // 3 — smallest ≥ 3
treeSet.lower(3);        // 2 — strictly less than 3
treeSet.higher(3);       // 4 — strictly greater than 3
```

**Complexities:** O(log n) add/remove/contains (same as TreeMap).

## Set Comparison

| Feature | HashSet | LinkedHashSet | TreeSet |
|---------|---------|--------------|---------|
| Order | None | Insertion | Sorted |
| add/remove/contains | O(1) avg | O(1) avg | O(log n) |
| Backed by | HashMap | LinkedHashMap | TreeMap |
| null allowed | Yes (one) | Yes (one) | No (NullPointerException) |
| Custom ordering | Via Comparator? | No | Via Comparator ✓ |

**C++ equivalents:**
- `HashSet` → `std::unordered_set<T>`
- `TreeSet` → `std::set<T>` (Red-Black Tree, sorted)

---

# 12. ConcurrentHashMap & Thread-Safe Collections

## The Problem with HashMap in Multithreading

```java
// NOT thread-safe — two threads calling put() simultaneously:
Map<String, Integer> map = new HashMap<>();

// Thread 1: map.put("a", 1)
// Thread 2: map.put("b", 2)
// Result: possible data corruption, infinite loops, lost updates
// HashMap has no internal synchronization
```

## Option 1: Collections.synchronizedMap (Coarse Lock)

```java
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());

// Every operation acquires a single lock on the entire map
// Only one thread can read OR write at any time — very contended
syncMap.put("key", 1);    // lock → put → unlock
syncMap.get("key");       // lock → get → unlock

// Compound operations still need external sync:
synchronized (syncMap) {
    if (!syncMap.containsKey("key")) {
        syncMap.put("key", 1);
    }
}
```

## Option 2: ConcurrentHashMap (Fine-Grained Locking)

`ConcurrentHashMap` is the production-grade thread-safe map — much more scalable than `synchronizedMap`.

### Java 7: Segment-Based Locking
Divided into 16 segments (by default). Each segment is an independent lock. Up to 16 threads can write concurrently — one per segment.

### Java 8+: CAS + Synchronized Buckets
```
No lock for reading — reads are wait-free
CAS (Compare-And-Swap) for first node insertion in empty bucket
synchronized on bucket's first node for writes to non-empty bucket
```

```java
ConcurrentHashMap<String, Integer> cmap = new ConcurrentHashMap<>();

// Thread-safe put/get/remove — no external sync needed
cmap.put("key", 1);
cmap.get("key");
cmap.remove("key");

// Atomic compound operations:
cmap.putIfAbsent("key", 1);              // atomic check-then-put
cmap.computeIfAbsent("key", k -> 0);     // atomic compute if absent
cmap.compute("key", (k, v) -> v == null ? 1 : v + 1);  // atomic update
cmap.merge("count", 1, Integer::sum);    // atomic merge

// ConcurrentHashMap does NOT allow null keys or null values
// cmap.put(null, 1);      // NullPointerException
// cmap.put("key", null);  // NullPointerException
```

### HashMap vs ConcurrentHashMap

| Feature | HashMap | ConcurrentHashMap |
|---------|---------|------------------|
| Thread safety | No | Yes |
| null keys | Yes (1) | No |
| null values | Yes | No |
| Read performance | Fast (no lock) | Fast (no lock for reads) |
| Write performance | Fast (no lock) | Fast (per-bucket lock) |
| Use case | Single-threaded | Multi-threaded |

## Other Thread-Safe Collections

```java
// Thread-safe List — good for read-heavy (writes copy the entire array)
List<String> cowList = new CopyOnWriteArrayList<>();

// Thread-safe Set
Set<String> cowSet = new CopyOnWriteArraySet<>();

// Thread-safe Queue (blocking — threads wait for elements)
BlockingQueue<Task> queue = new LinkedBlockingQueue<>(100);  // capacity 100
queue.put(task);    // blocks if full
queue.take();       // blocks if empty

// Non-blocking concurrent queue (lock-free)
Queue<String> clQueue = new ConcurrentLinkedQueue<>();

// Thread-safe NavigableMap
NavigableMap<String, Integer> cSkipMap = new ConcurrentSkipListMap<>();
```

---

# 13. Comparable & Comparator

## Comparable — Natural Ordering

`Comparable<T>` defines the **natural ordering** of a class. Implement it when your objects have an obvious, single natural sort order:

```java
class Student implements Comparable<Student> {
    String name;
    double gpa;

    Student(String name, double gpa) {
        this.name = name;
        this.gpa = gpa;
    }

    @Override
    public int compareTo(Student other) {
        // Return: negative if this < other
        //          0       if this == other
        //          positive if this > other
        return Double.compare(this.gpa, other.gpa);  // sort by GPA ascending
    }
}

List<Student> students = new ArrayList<>();
students.add(new Student("Alice", 3.8));
students.add(new Student("Bob", 3.5));
students.add(new Student("Charlie", 3.9));

Collections.sort(students);  // uses compareTo()
// Result: Bob(3.5), Alice(3.8), Charlie(3.9)
```

## Comparator — Custom Ordering

`Comparator<T>` defines an **external, flexible ordering** — doesn't need to modify the class:

```java
// Comparator by name
Comparator<Student> byName = Comparator.comparing(Student::getName);

// Comparator by GPA descending
Comparator<Student> byGpaDesc = Comparator.comparingDouble(Student::getGpa).reversed();

// Chained: by GPA desc, then by name asc for ties
Comparator<Student> complex = Comparator
    .comparingDouble(Student::getGpa).reversed()
    .thenComparing(Student::getName);

students.sort(byName);
students.sort(byGpaDesc);
students.sort(complex);

// Anonymous comparator (old style):
students.sort(new Comparator<Student>() {
    @Override
    public int compare(Student a, Student b) {
        return a.getName().compareTo(b.getName());
    }
});

// Lambda (modern style):
students.sort((a, b) -> a.getName().compareTo(b.getName()));

// Method reference:
students.sort(Comparator.comparing(Student::getName));
```

## Comparable vs Comparator

| Aspect | Comparable | Comparator |
|--------|-----------|------------|
| Location | Inside the class | External to the class |
| Method | `compareTo(T other)` | `compare(T o1, T o2)` |
| Ordering defined | Once (natural) | Many different orderings |
| Modifies class | Yes | No |
| Used when | Class has one obvious ordering | Multiple orderings needed, or can't modify class |

## Common Implementations

```java
// Comparing primitives:
Comparator.comparingInt(obj -> obj.age)
Comparator.comparingDouble(obj -> obj.price)
Comparator.comparingLong(obj -> obj.id)

// String comparison:
Comparator.comparing(String::toLowerCase)  // case-insensitive

// Null-safe:
Comparator.nullsFirst(Comparator.naturalOrder())
Comparator.nullsLast(Comparator.comparingInt(obj -> obj.priority))

// Reversed:
Comparator.reverseOrder()
Comparator.comparing(obj -> obj.name, Comparator.reverseOrder())
```

---

# 14. Iterators — Fail-Fast vs Fail-Safe

## Iterator Pattern

```java
public interface Iterator<E> {
    boolean hasNext();   // is there a next element?
    E next();            // get next element and advance
    void remove();       // remove last element returned by next() (optional)
}

// Using iterator explicitly:
List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    String s = it.next();
    if (s.equals("b")) {
        it.remove();   // safe removal during iteration!
    }
}
// list is now ["a", "c"]
```

## Fail-Fast Iterators

Iterators for `ArrayList`, `HashMap`, `HashSet`, `LinkedList` (most java.util collections) are **fail-fast**.

They maintain a `modCount` (modification count) on the collection. When an iterator is created, it captures the current `modCount`. On each `next()` call, it checks:

```java
final void checkForComodification() {
    if (modCount != expectedModCount)
        throw new ConcurrentModificationException();
}
```

```java
List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
Iterator<String> it = list.iterator();

list.add("d");             // modifies list while iterator exists

it.next();                 // ConcurrentModificationException!
// modCount changed since iterator was created
```

**Why?** Fail-fast detects bugs immediately. Structural modification during iteration leads to undefined behavior — better to throw an exception than silently produce wrong results.

**Correct removal during iteration:**
```java
// Option 1: Iterator.remove()
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    if (it.next().startsWith("a")) it.remove();  // safe!
}

// Option 2: removeIf (Java 8+, cleaner)
list.removeIf(s -> s.startsWith("a"));

// Option 3: collect then remove (for complex cases)
List<String> toRemove = list.stream()
    .filter(s -> s.startsWith("a"))
    .collect(Collectors.toList());
list.removeAll(toRemove);
```

## Fail-Safe Iterators

Iterators for **concurrent collections** (`CopyOnWriteArrayList`, `ConcurrentHashMap`) are **fail-safe** — they operate on a snapshot of the data and don't throw `ConcurrentModificationException`:

```java
List<String> cowList = new CopyOnWriteArrayList<>(Arrays.asList("a", "b", "c"));
Iterator<String> it = cowList.iterator();

cowList.add("d");   // modifies list while iterator exists — NO exception!

while (it.hasNext()) {
    System.out.println(it.next());  // prints a, b, c (snapshot, not d)
}
```

`CopyOnWriteArrayList` creates a **fresh copy** of the backing array on every write. The iterator uses the old copy — so it never sees the modification, and no exception is thrown. The tradeoff: writes are expensive (copy entire array), reads are very fast and never blocked.

| | Fail-Fast | Fail-Safe |
|--|-----------|-----------|
| Examples | ArrayList, HashMap, HashSet | CopyOnWriteArrayList, ConcurrentHashMap |
| ConcurrentModificationException | Yes | No |
| Operates on | Original collection | Snapshot |
| Memory | Less | More (snapshot copy) |
| Consistent view | No guarantee in concurrent | May miss recent updates |

---

# 15. Generics in Collections

## Why Generics?

Before generics (Java 1.4):
```java
List list = new ArrayList();  // raw type — no type safety
list.add("hello");
list.add(42);               // accidentally mixed types — no compile error!

String s = (String) list.get(0);  // explicit cast needed
String s2 = (String) list.get(1); // ClassCastException at RUNTIME — surprise!
```

With generics (Java 5+):
```java
List<String> list = new ArrayList<>();  // type-safe
list.add("hello");
// list.add(42);  // COMPILE ERROR — caught at compile time!

String s = list.get(0);  // no cast needed — compiler knows it's a String
```

## Type Erasure

Java generics use **type erasure** — generic type information exists only at compile time and is erased at runtime. The JVM sees raw types:

```java
// What you write:
List<String> strings = new ArrayList<>();
List<Integer> integers = new ArrayList<>();

// What the JVM sees at runtime (after erasure):
List strings = new ArrayList();
List integers = new ArrayList();

// Therefore:
strings.getClass() == integers.getClass();  // true! Both are ArrayList at runtime
strings instanceof List<String>;             // COMPILE ERROR — can't check generic at runtime
strings instanceof List;                     // OK
```

Why erasure? Backward compatibility with pre-generics Java code.

## Wildcards

```java
// ? extends T — upper bounded wildcard (producer — read from)
// Can hold List<Integer>, List<Double>, List<Number> (any subtype of Number)
void printNumbers(List<? extends Number> list) {
    for (Number n : list) System.out.println(n);  // read as Number — safe
    // list.add(1);  // COMPILE ERROR — can't add, don't know exact type
}

// ? super T — lower bounded wildcard (consumer — write to)
// Can hold List<Integer>, List<Number>, List<Object>
void addNumbers(List<? super Integer> list) {
    list.add(1);   // safe — Integer is subtype of bound
    list.add(2);
    // Integer n = list.get(0);  // COMPILE ERROR — can only read as Object
}

// Unbounded wildcard — ? (unknown type)
void printList(List<?> list) {
    for (Object o : list) System.out.println(o);  // read as Object only
}
```

**PECS: Producer Extends, Consumer Super**
- If a collection **produces** elements you read → `? extends T`
- If a collection **consumes** elements you write → `? super T`

```java
// Copying elements from source to destination:
static <T> void copy(List<? super T> dest, List<? extends T> src) {
    for (T element : src) {   // src produces T elements
        dest.add(element);    // dest consumes T elements
    }
}
```

---

# 16. Collections Utility Class

`java.util.Collections` provides static utility methods:

```java
List<Integer> nums = new ArrayList<>(Arrays.asList(3, 1, 4, 1, 5, 9, 2, 6));

// Sorting
Collections.sort(nums);                              // natural order: [1,1,2,3,4,5,6,9]
Collections.sort(nums, Comparator.reverseOrder());  // reverse: [9,6,5,4,3,2,1,1]

// Min/Max
Collections.min(nums);  // 1
Collections.max(nums);  // 9

// Binary search (list MUST be sorted first!)
Collections.binarySearch(nums, 5);  // returns index of 5

// Shuffle
Collections.shuffle(nums);  // random order
Collections.shuffle(nums, new Random(42));  // seeded for reproducibility

// Reverse
Collections.reverse(nums);

// Fill and copy
Collections.fill(nums, 0);  // set all elements to 0
List<Integer> dest = new ArrayList<>(Arrays.asList(0, 0, 0));
Collections.copy(dest, src);

// Frequency
Collections.frequency(nums, 1);  // count occurrences of 1

// Unmodifiable views (NOT the same as immutable — backed by original):
List<Integer> readOnly = Collections.unmodifiableList(nums);
// readOnly.add(1);  // UnsupportedOperationException

// Singleton collections (one element, immutable):
List<String> single = Collections.singletonList("only");
Set<String> singleSet = Collections.singleton("only");
Map<String, Integer> singleMap = Collections.singletonMap("key", 1);

// Empty immutable collections (use these instead of null):
List<String> empty = Collections.emptyList();
Map<String, Integer> emptyMap = Collections.emptyMap();

// Synchronized wrappers:
List<String> syncList = Collections.synchronizedList(new ArrayList<>());
```

## Modern Alternatives (Java 9+)

```java
// Immutable collections (truly immutable, not just unmodifiable views):
List<String> immutable  = List.of("a", "b", "c");
Set<Integer> immutableSet = Set.of(1, 2, 3);
Map<String, Integer> immutableMap = Map.of("a", 1, "b", 2);

// Map with more than 10 entries:
Map<String, Integer> bigMap = Map.ofEntries(
    Map.entry("a", 1),
    Map.entry("b", 2),
    // ... up to any number
);
```

---

# 17. C++ STL vs Java Collections

## Direct Equivalents

| Java | C++ STL | Structure |
|------|---------|-----------|
| `ArrayList<T>` | `std::vector<T>` | Dynamic array |
| `LinkedList<T>` | `std::list<T>` | Doubly-linked list |
| `ArrayDeque<T>` | `std::deque<T>` | Double-ended queue |
| `PriorityQueue<T>` | `std::priority_queue<T>` | Binary heap |
| `HashMap<K,V>` | `std::unordered_map<K,V>` | Hash table |
| `TreeMap<K,V>` | `std::map<K,V>` | Red-Black Tree |
| `HashSet<T>` | `std::unordered_set<T>` | Hash table |
| `TreeSet<T>` | `std::set<T>` | Red-Black Tree |
| `Stack<T>` | `std::stack<T>` | Adapter (default over deque) |

## Key Differences

| Aspect | Java | C++ |
|--------|------|-----|
| Default map | HashMap (unordered) | std::map (ordered/TreeMap) |
| Priority queue default | Min-heap | Max-heap |
| Null handling | Most allow null | std::map allows null keys |
| Iterator invalidation | ConcurrentModificationException | Undefined behavior |
| Generics/Templates | Type erasure (runtime raw) | Full template instantiation |
| Thread safety | Must use concurrent versions | Must use locks manually |
| String as key | Works perfectly (immutable) | Works (copies stored) |
| Copying collections | Assignment = shared reference | Assignment = value copy |

## Code Comparison

```cpp
// C++
#include <vector>
#include <unordered_map>
#include <algorithm>

std::vector<int> vec = {3, 1, 4, 1, 5};
std::sort(vec.begin(), vec.end());
vec.push_back(9);
int x = vec[0];          // direct index access

std::unordered_map<std::string, int> map;
map["alice"] = 30;
map["bob"]   = 25;
if (map.count("alice")) { ... }   // check existence
for (auto& [k, v] : map) { ... } // structured binding iteration
```

```java
// Java
import java.util.*;

List<Integer> list = new ArrayList<>(Arrays.asList(3, 1, 4, 1, 5));
Collections.sort(list);
list.add(9);
int x = list.get(0);     // method call (no operator overloading)

Map<String, Integer> map = new HashMap<>();
map.put("alice", 30);
map.put("bob", 25);
if (map.containsKey("alice")) { ... }
for (Map.Entry<String, Integer> e : map.entrySet()) { ... }
map.forEach((k, v) -> { ... });  // Java 8+
```

---

# 18. Interview Quick Reference

## Which Collection to Choose

```
Need a list?
├── Random access by index? → ArrayList
├── Frequent insert/delete at front? → ArrayDeque (as Deque)
└── Queue/Stack operations? → ArrayDeque

Need unique elements (Set)?
├── No ordering needed? → HashSet (fastest)
├── Insertion order needed? → LinkedHashSet
└── Sorted order needed? → TreeSet

Need key-value mapping (Map)?
├── No ordering needed? → HashMap (fastest)
├── Insertion order needed? → LinkedHashMap
├── Sorted by key? → TreeMap
└── Thread-safe? → ConcurrentHashMap

Need priority ordering? → PriorityQueue (min-heap)
Need LRU cache? → LinkedHashMap with accessOrder=true
Need thread-safe list? → CopyOnWriteArrayList (read-heavy)
                         Collections.synchronizedList (write-heavy)
```

## Complexity Cheat Sheet

| Collection | get/contains | add/put | remove | Ordered |
|------------|-------------|---------|--------|---------|
| ArrayList | O(1) index, O(n) value | O(1) amortized end | O(n) | Insertion |
| LinkedList | O(n) | O(1) ends | O(n) find, O(1) linked | Insertion |
| ArrayDeque | O(n) | O(1) both ends | O(1) ends | Insertion |
| PriorityQueue | O(1) min | O(log n) | O(log n) | Priority |
| HashMap | O(1) avg | O(1) avg | O(1) avg | None |
| LinkedHashMap | O(1) avg | O(1) avg | O(1) avg | Insertion/Access |
| TreeMap | O(log n) | O(log n) | O(log n) | Sorted |
| HashSet | O(1) avg | O(1) avg | O(1) avg | None |
| TreeSet | O(log n) | O(log n) | O(log n) | Sorted |

## Key Interview Questions

- **Q: How does HashMap handle collisions?**
  A: Separate chaining with linked lists. Java 8+ converts chains longer than 8 into Red-Black Trees (O(n) → O(log n) worst case).

- **Q: What is the difference between HashMap and Hashtable?**
  A: Hashtable is legacy, synchronized (all methods), doesn't allow null keys/values. HashMap is not synchronized, allows one null key and multiple null values. Use ConcurrentHashMap for thread-safe modern alternative.

- **Q: Why should HashMap keys be immutable?**
  A: If a key's hashCode changes after insertion, the HashMap looks in the wrong bucket and can't find the entry — effectively a memory leak. String, Integer, and enums are safe as keys because they're immutable.

- **Q: What is the initial capacity and load factor of HashMap?**
  A: Default initial capacity is 16, load factor is 0.75. Resize (double capacity, rehash all entries) triggers when `size > capacity × loadFactor` = 12 for default settings.

- **Q: When does ArrayList grow, and by how much?**
  A: When the array is full. New capacity = oldCapacity + (oldCapacity >> 1) = 1.5× the old capacity. A new array is allocated and all elements are copied — O(n) for the resize itself, O(1) amortized per add.

- **Q: What is ConcurrentModificationException?**
  A: Thrown by fail-fast iterators when the underlying collection is structurally modified (elements added/removed) while iterating. Fix: use `iterator.remove()`, `removeIf()`, or use a concurrent collection.

- **Q: Difference between Iterator and ListIterator?**
  A: `Iterator` works on all Collections (forward only). `ListIterator` works only on Lists and supports bidirectional traversal (`hasPrevious()`, `previous()`), index access, and element replacement during iteration.

---

*End of Part 5: Java Collections Framework*
*Next: Part 6 (Java Multithreading & Concurrency)*