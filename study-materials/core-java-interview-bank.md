# Core Java Interview Question Bank
## For Ramish Taha — Mid-Level Java Developer (3-4 Years Experience)
### Target: Product Companies & BFSI GCCs (JPMorgan, Goldman, Morgan Stanley, HSBC, Deutsche Bank, BNY Mellon, Barclays)

> **How to use this bank:** Questions tagged 🔴 are **must-know** — expect these in nearly every interview. Questions tagged 🟡 are **nice-to-have** — strong answers here differentiate you from other candidates. Questions tagged 🔵 are **advanced/stretch** — answer these well and you're in the top 10% of candidates.
>
> **Suggested 2-3 week revision schedule:**
> - **Days 1-4:** Collections Framework
> - **Days 5-9:** Concurrency (biggest weight in BFSI interviews)
> - **Days 10-13:** JVM Internals
> - **Days 14-15:** Exceptions & Generics
> - **Days 16-17:** Streams API & I/O
> - **Days 18-19:** OOP Concepts
> - **Days 20-21:** Full revision + timed self-quiz

---

## Table of Contents

1. [Collections Framework](#1-collections-framework)
2. [Concurrency](#2-concurrency)
3. [JVM Internals](#3-jvm-internals)
4. [Exceptions](#4-exceptions)
5. [Generics](#5-generics)
6. [Streams API](#6-streams-api)
7. [I/O — NIO & Channels](#7-io--nio--channels)
8. [OOP Concepts](#8-oop-concepts)
9. [Quick Reference Tables](#9-quick-reference-tables)

---

## 1. Collections Framework

> Collection questions are the bread-and-butter of Java interviews. BFSI GCCs love HashMap internals and ConcurrentHashMap — expect these in the first round.

### 1.1 HashMap Internals

**Q1. 🔴 How does HashMap work internally in Java?**

HashMap stores key-value pairs in an array of buckets (default initial capacity 16, load factor 0.75). When you `put(k, v)`:

1. Compute hash: `hash = key.hashCode() ^ (key.hashCode() >>> 16)` — this "spreads" high bits to lower positions to reduce collisions.
2. Compute bucket index: `index = (n - 1) & hash` (where n = array length). Using `&` instead of `%` works because array length is always a power of 2.
3. If bucket is empty → store the entry as a new Node.
4. If bucket is non-empty → traverse the linked list (or red-black tree):
   - If key matches (`key.equals(k)`) → replace the value.
   - If no match → append a new node at the end of the list.
5. After insertion, if `size > capacity * loadFactor` → resize: double capacity and rehash all entries.

```java
// Simplified internal structure
static class Node<K,V> implements Map.Entry<K,V> {
    final int hash;
    final K key;
    V value;
    Node<K,V> next;
}

// Java 8+ treeify threshold: when a bucket's linked list exceeds 8 entries
// AND the table capacity exceeds 64, the list converts to a red-black tree.
// If capacity < 64, HashMap resizes instead of treeifying.
static final int TREEIFY_THRESHOLD = 8;
static final int UNTREEIFY_THRESHOLD = 6; // converts back to linked list on resize
```

---

**Q2. 🔴 What happens when two keys have the same hashCode?**

This is a **hash collision** — it's perfectly legal and common. Both keys map to the same bucket index and are stored in the same bucket's linked list (or tree). When retrieving, HashMap:

1. Finds the bucket by `hash & (n-1)`.
2. Iterates through the bucket's entries.
3. Compares using `key.equals(k)` to find the exact match.

**Key point:** A good `hashCode()` implementation distributes keys uniformly. A poor `hashCode()` (e.g., returning a constant) forces all entries into a single bucket, degrading HashMap to O(n) for put/get instead of O(1).

```java
// Bad hashCode — all keys collide
@Override
public int hashCode() { return 1; }

// Good hashCode — uniform distribution
@Override
public int hashCode() {
    return Objects.hash(field1, field2, field3);
}
```

---

**Q3. 🔴 Why does Java 8 convert a bucket's linked list to a red-black tree? What's the threshold?**

In Java 7, a bucket with many collisions degrades to O(n) for get/put because of linear linked list traversal. Java 8 converts a bucket's linked list to a **red-black tree** (self-balancing BST) when:

- The bucket has **≥ 8 entries** (`TREEIFY_THRESHOLD = 8`).
- The **table capacity is ≥ 64**. If capacity < 64, HashMap resizes instead of treeifying (resizing is cheaper at small sizes).

A red-black tree gives O(log n) for search/insert/delete in that bucket, making the worst case O(log n) instead of O(n). When the tree shrinks below 6 entries (`UNTREEIFY_THRESHOLD`), it converts back to a linked list.

**Why 8?** The Poisson distribution with default load factor 0.75 shows probability of ≥ 8 entries in a bucket is ~0.00000006 — treeification is rare under normal conditions. It's a defense against pathological hash collisions (including deliberate hash collision attacks).

---

**Q4. 🔴 What is the difference between `equals()` and `==` in the context of HashMap keys?**

- `==` checks **reference equality** — do two references point to the same object in memory?
- `equals()` checks **value equality** — defined by the class (e.g., two String objects with the same content).

HashMap uses `equals()` to compare keys within a bucket. If you use a mutable object as a key and modify it after insertion, its `hashCode()` changes, and the key becomes **unreachable** — the entry is effectively lost (a memory leak).

```java
List<String> key = new ArrayList<>(List.of("a"));
map.put(key, "value");
key.add("b"); // hashCode changed! map.get(key) now returns null
```

---

**Q5. 🔴 Why should HashMap keys be immutable?**

If a key is mutable and modified after being inserted into the HashMap:
- Its `hashCode()` may change → the entry is now in the wrong bucket.
- `map.get(key)` will not find it → looks like a silent deletion.
- The orphaned entry remains in memory → memory leak.

Immutable keys (String, Integer, Long, UUID, records) are safe because their hashCode never changes. String is the most commonly used HashMap key because it's immutable and caches its hashCode.

---

**Q6. 🟡 What is the initial capacity and load factor of HashMap? What happens when you resize?**

| Parameter | Default | Description |
|-----------|---------|-------------|
| Initial capacity | 16 | Number of buckets (array length) |
| Load factor | 0.75 | Threshold ratio for resizing |
| Threshold | capacity × loadFactor | When `size > threshold`, resize |
| Treeify threshold | 8 | Entries per bucket to trigger treeification |

**Resize process:** Create a new array of double the size, then rehash every entry into the new array. This is O(n) — expensive. If you know the expected size, pre-size the HashMap:

```java
// If you expect ~1000 entries, use targetSize / 0.75 + 1 to avoid resizing
Map<String, String> map = new HashMap<>(1334, 0.75f);
```

---

**Q7. 🟡 How does `computeIfAbsent`, `computeIfPresent`, and `merge` work?**

These are Java 8 Map methods that make common operations atomic and concise:

```java
// computeIfAbsent: if key is absent, compute value using function
map.computeIfAbsent("key", k -> "default");

// computeIfPresent: if key is present, recompute value
map.computeIfPresent("key", (k, v) -> v + " updated");

// merge: if key absent → put value; if present → apply merge function
map.merge("key", 1, Integer::sum); // counter pattern — increments or initializes
```

**Why prefer these over put-if-absent patterns?** They're **atomic** for ConcurrentHashMap (single lock-free operation), whereas get-check-put is a race condition for concurrent maps.

---

**Q8. 🔵 What is the internal difference between HashMap and LinkedHashMap?**

HashMap maintains no insertion order. LinkedHashMap maintains a **doubly-linked list** running through all entries, preserving either **insertion order** (default) or **access order** (`new LinkedHashMap<>(16, 0.75f, true)`).

```java
// Access-order LinkedHashMap — useful for LRU cache
LinkedHashMap<K, V> lruCache = new LinkedHashMap<>(16, 0.75f, true) {
    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > 100; // evict oldest accessed entry
    }
};
```

Each entry has `before` and `after` pointers. This adds O(1) overhead per put/get but guarantees iteration order. Access-order mode makes LinkedHashMap a natural LRU cache implementation.

---

### 1.2 ConcurrentHashMap

**Q9. 🔴 How does ConcurrentHashMap work internally? (Java 7 vs Java 8)**

**Java 7 (Segment-based):** ConcurrentHashMap is divided into 16 `Segment` objects, each acting as an independent mini-HashMap with its own lock. This allows up to 16 threads to write concurrently (one per segment). Read operations are lock-free.

**Java 8+ (CAS + synchronized):** No segments. The internal array is `Node[]`. Each bucket is independently locked using `synchronized` on the first node of the bucket. Write operations use **CAS (Compare-And-Swap)** for lock-free operations on empty buckets, and `synchronized` only when there's a collision (non-empty bucket). This means:

- Empty bucket → CAS to insert (no lock).
- Non-empty bucket → synchronized on the bucket head node.
- Read operations are fully lock-free (volatile reads).

```java
// Java 8 ConcurrentHashMap put() — simplified
Node<K,V> f; int n, i;
if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
    // Bucket empty — CAS insert (no lock)
    if (casTabAt(tab, i, null, new Node<>(hash, key, value)))
        break;
} else {
    // Bucket non-empty — synchronized on bucket head
    synchronized (f) {
        // traverse list/tree, insert or update
    }
}
```

**Advantages of Java 8 approach:** Finer-grained locking (per-bucket instead of per-segment), better scalability, less memory overhead (no Segment objects).

---

**Q10. 🔴 Why is ConcurrentHashMap thread-safe but Hashtable is discouraged?**

| Feature | Hashtable | ConcurrentHashMap |
|---------|-----------|-------------------|
| Locking | Single lock for entire map | Per-bucket lock (Java 8+) |
| Read concurrency | Blocks on read (synchronized) | Lock-free reads |
| Write concurrency | Single writer at a time | Multiple concurrent writers |
| Null keys/values | Allowed | **Not allowed** (throws NPE) |
| Iterator | Fail-fast | Weakly consistent |
| Performance | Poor under contention | Excellent |

**Why no null in ConcurrentHashMap?** In a concurrent map, `get(key)` returning null is ambiguous — it could mean "key absent" or "value is null." In HashMap you can check with `containsKey()`, but in a concurrent map, the state could change between `containsKey()` and `get()` — a race condition. So nulls are banned entirely.

---

**Q11. 🔴 What is a fail-fast iterator vs a fail-safe (weakly consistent) iterator?**

- **Fail-fast** (HashMap, ArrayList): The iterator checks the `modCount` field. If the map is structurally modified (add/remove) after iterator creation, it throws `ConcurrentModificationException`. This is a best-effort detection — not guaranteed (the check is not synchronized).

- **Fail-safe / Weakly consistent** (ConcurrentHashMap, CopyOnWriteArrayList): The iterator operates on a snapshot or uses volatile reads. It does NOT throw `ConcurrentModificationException`. It may or may not reflect modifications made after the iterator was created, but it never throws.

```java
// Fail-fast — throws ConcurrentModificationException
for (String key : hashMap.keySet()) {
    hashMap.remove(key); // ❌ CME
}

// Safe removal via iterator
Iterator<String> it = hashMap.keySet().iterator();
while (it.hasNext()) {
    it.next();
    it.remove(); // ✅ safe
}

// Weakly consistent — no exception, may see some changes
for (String key : concurrentHashMap.keySet()) {
    concurrentHashMap.remove(key); // ✅ no exception
}
```

---

**Q12. 🟡 What is the difference between `putIfAbsent`, `computeIfAbsent`, and `put` in ConcurrentHashMap?**

All three are thread-safe, but differ in semantics:

```java
// put: always overwrites
chm.put("key", "value");

// putIfAbsent: only put if key is absent (atomic)
chm.putIfAbsent("key", "value");

// computeIfAbsent: compute value lazily, only if absent (atomic)
chm.computeIfAbsent("key", k -> expensiveCompute(k));
```

`computeIfAbsent` is preferred when the value computation is expensive — it only computes if the key is truly absent, and the computation is atomic (no other thread can insert between the check and the compute). `putIfAbsent` always evaluates the value argument even if the key exists — wasteful for expensive computations.

---

### 1.3 ArrayList vs LinkedList

**Q13. 🔴 What is the difference between ArrayList and LinkedList?**

| Feature | ArrayList | LinkedList |
|---------|-----------|------------|
| Internal structure | Dynamic array | Doubly-linked list |
| Random access (get) | O(1) | O(n) |
| Insert at end | O(1) amortized | O(1) |
| Insert at index | O(n) (shifts elements) | O(n) (traverse to index) |
| Remove at index | O(n) | O(n) (traverse + unlink) |
| Memory overhead | Less (array + capacity) | More (each node has prev/next pointers) |
| Cache locality | Excellent (contiguous) | Poor (scattered nodes) |
| Implements | List, RandomAccess | List, Deque, Queue |

**When to use ArrayList:** Almost always. For random access, iteration, and most use cases. The memory cache locality of the contiguous array makes it faster than LinkedList even for many "insert at end" operations.

**When to use LinkedList:** Rarely. Only when you frequently add/remove at both ends (use as Deque/Queue) and rarely need random access. In practice, `ArrayDeque` is preferred over `LinkedList` for queue/deque use cases because it's faster.

---

**Q14. 🟡 How does ArrayList grow internally?**

ArrayList uses a backing array. When capacity is exceeded:
1. A new array of size `oldCapacity + oldCapacity/2` (i.e., 1.5×) is created.
2. All elements are copied via `Arrays.copyOf()`.
3. The old array is GC'd.

```java
// Java 8+ ArrayList grow()
int newCapacity = oldCapacity + (oldCapacity >> 1); // 1.5x growth
```

**Why 1.5×?** Amortized O(1) for add. The 1.5× growth is a balance between memory waste (smaller is better) and number of resizes (larger is better). Java chose 1.5×; C++ `std::vector` also uses 1.5× (MSVC) or 2× (libstdc++).

If you know the size upfront, pre-allocate: `new ArrayList<>(10000)` to avoid resizing.

---

### 1.4 TreeMap

**Q15. 🔴 How does TreeMap work internally? Why and when would you use it?**

TreeMap is backed by a **Red-Black Tree** (self-balancing BST). Keys must be either `Comparable` or a `Comparator` must be provided. It maintains keys in **sorted order** and provides O(log n) for get, put, remove.

```java
TreeMap<String, Integer> treeMap = new TreeMap<>(); // uses natural ordering
TreeMap<String, Integer> customOrder = new TreeMap<>(Comparator.reverseOrder());
```

**Use cases:**
- You need keys in sorted order (e.g., sorted menu of trade IDs).
- You need range queries: `subMap()`, `headMap()`, `tailMap()`.
- You need `firstKey()`, `lastKey()`, `higherKey()`, `lowerKey()`.

**Trade-off vs HashMap:** TreeMap is O(log n) for all operations, HashMap is O(1). Only use TreeMap when you specifically need sorting or range queries.

```java
// Range queries — common in BFSI (e.g., trades in a date range)
NavigableMap<LocalDate, Trade> trades = new TreeMap<>();
Map<LocalDate, Trade> todayTrades = trades.subMap(today, tomorrow); // half-open range
Trade earliest = trades.firstEntry().getValue();
Trade latest = trades.lastEntry().getValue();
```

---

**Q16. 🟡 What is a Red-Black Tree and why is it used in TreeMap?**

A Red-Black Tree is a self-balancing BST that guarantees O(log n) height by enforcing these properties:
1. Every node is either red or black.
2. The root is black.
3. All leaves (NIL) are black.
4. A red node's children are both black (no two consecutive red nodes).
5. Every path from root to leaf has the same number of black nodes.

After insert/delete, the tree rebalances using rotations and color flips. This guarantees height ≤ 2·log(n+1), ensuring O(log n) operations.

**Why not AVL tree?** AVL trees are more strictly balanced (height difference ≤ 1) but require more rotations on insert/delete. Red-Black trees are less strictly balanced but require fewer rotations — better for write-heavy workloads. Java's TreeMap and HashMap (bucket trees) both use Red-Black trees.

---

### 1.5 Additional Collections Questions

**Q17. 🔴 What is the difference between `HashSet`, `LinkedHashSet`, and `TreeSet`?**

| Set | Internal | Order | Performance | Null |
|-----|----------|-------|-------------|------|
| HashSet | HashMap (value = dummy) | No order | O(1) | One null allowed |
| LinkedHashSet | LinkedHashMap | Insertion order | O(1) | One null allowed |
| TreeSet | TreeMap (Red-Black Tree) | Sorted (natural/comparator) | O(log n) | No null (comparator throws NPE) |

```java
Set<String> hashSet = new HashSet<>();     // unordered
Set<String> linkedHashSet = new LinkedHashSet<>(); // insertion order
Set<String> treeSet = new TreeSet<>();    // sorted
```

**Internally**, HashSet wraps a HashMap — `add(e)` calls `map.put(e, PRESENT)` where PRESENT is a dummy value. This is why HashSet has the same performance characteristics as HashMap.

---

**Q18. 🔴 What is the difference between `Comparable` and `Comparator`?**

```java
// Comparable — defines natural ordering inside the class itself
public class Trade implements Comparable<Trade> {
    private long timestamp;
    @Override
    public int compareTo(Trade other) {
        return Long.compare(this.timestamp, other.timestamp);
    }
}

// Comparator — defines external, custom ordering
Comparator<Trade> byValue = Comparator.comparing(Trade::getNotional);
Comparator<Trade> byValueDesc = byValue.reversed();
Comparator<Trade> byValueThenId = byValue.thenComparing(Trade::getId);
```

| | Comparable | Comparator |
|---|-----------|-----------|
| Where | Inside the class | External to the class |
| Method | `compareTo(T)` | `compare(T, T)` |
| Count | One natural ordering | Multiple custom orderings |
| Usage | `Collections.sort(list)` | `list.sort(comparator)` |

---

**Q19. 🟡 What is `CopyOnWriteArrayList` and when would you use it?**

`CopyOnWriteArrayList` creates a **full copy** of the internal array on every write (add, set, remove). Reads are lock-free and fast (direct array access with volatile read). Writes are expensive (O(n) copy).

**Use case:** **Read-heavy, write-rare** scenarios — e.g., event listener lists, configuration lists that are read frequently but modified rarely. The iterator never throws `ConcurrentModificationException` and reflects the state at the time of iterator creation (snapshot).

```java
CopyOnWriteArrayList<TradeListener> listeners = new CopyOnWriteArrayList<>();
// Read path: lock-free, fast
for (TradeListener l : listeners) { l.onTrade(trade); }
// Write path: creates a new copy — expensive but rare
listeners.add(newListener);
```

---

**Q20. 🟡 What is the difference between `Iterator` and `ListIterator`?**

| | Iterator | ListIterator |
|---|----------|--------------|
| Direction | Forward only | Forward + backward |
| Operations | next, hasNext, remove | add, set, next, previous, hasNext, hasPrevious, nextIndex, previousIndex |
| Applies to | All Collection types | Only List (ArrayList, LinkedList) |
| Can modify | remove only | add, set, remove |

```java
ListIterator<String> it = list.listIterator();
while (it.hasNext()) { it.next(); }
while (it.hasPrevious()) { it.previous(); } // bidirectional
```

---

**Q21. 🔵 What is the difference between `ArrayDeque` and `PriorityQueue`?**

- **ArrayDeque**: Resizable-array implementation of Deque. O(1) for add/remove at both ends. Does NOT allow null. Better than `Stack` (which is synchronized and slow) and `LinkedList` (which has poor cache locality).

- **PriorityQueue**: Min-heap (by default) implementation of Queue. Elements ordered by natural ordering or Comparator. O(log n) for offer/poll, O(1) for peek. Does NOT allow null.

```java
// ArrayDeque — stack usage (LIFO)
Deque<String> stack = new ArrayDeque<>();
stack.push("a"); stack.push("b");
stack.pop(); // "b"

// ArrayDeque — queue usage (FIFO)
Deque<String> queue = new ArrayDeque<>();
queue.offer("a"); queue.offer("b");
queue.poll(); // "a"

// PriorityQueue — min-heap (smallest first)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(5); minHeap.offer(1); minHeap.offer(3);
minHeap.poll(); // 1

// Max-heap
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
```

---

**Q22. 🔵 How does `PriorityQueue` work internally?**

PriorityQueue is backed by a **binary heap** stored in an array. For a min-heap at index `i`:
- Parent: `(i - 1) / 2`
- Left child: `2 * i + 1`
- Right child: `2 * i + 2`

**offer(x):** Add to end of array, then "sift up" — compare with parent, swap if smaller. O(log n).

**poll():** Take root (index 0, the minimum), move last element to root, then "sift down" — compare with smaller child, swap if needed. O(log n).

**peek():** Return root. O(1).

Not synchronized — use `PriorityBlockingQueue` for concurrent access.

---

## 2. Concurrency

> Concurrency is the most heavily tested area in BFSI GCC interviews (JPMorgan, Goldman, Morgan Stanley). Expect 3-5 concurrency questions per interview round. This is your banking domain — concurrent transaction processing, thread pools for trade matching, etc.

### 2.1 Thread Basics & Thread Pools

**Q23. 🔴 What are the different ways to create a Thread in Java?**

```java
// 1. Extend Thread
class MyThread extends Thread {
    public void run() { System.out.println("running"); }
}
new MyThread().start();

// 2. Implement Runnable (preferred — separates task from execution)
Thread t = new Thread(() -> System.out.println("running"));
t.start();

// 3. Callable + ExecutorService (returns a value)
ExecutorService es = Executors.newFixedThreadPool(4);
Future<Integer> future = es.submit(() -> 42);

// 4. CompletableFuture (Java 8+ — composable async)
CompletableFuture.supplyAsync(() -> 42)
    .thenApply(x -> x * 2)
    .thenAccept(System.out::println);

// 5. Virtual Threads (Java 21+ — lightweight)
Thread.startVirtualThread(() -> System.out.println("virtual"));
```

**Runnable vs Callable:** `Runnable.run()` returns void and cannot throw checked exceptions. `Callable.call()` returns a value and can throw checked exceptions. Use Callable when you need a return value.

---

**Q24. 🔴 What are the types of Thread Pools in Java? When do you use each?**

| Pool | Creation | Behavior | Use Case |
|------|----------|----------|----------|
| Fixed | `newFixedThreadPool(n)` | Fixed n threads, unbounded queue | Known concurrent workload, CPU-bound tasks |
| Cached | `newCachedThreadPool()` | 0 to Integer.MAX_VALUE threads, SynchronousQueue | Short-lived, many lightweight tasks |
| Single | `newSingleThreadExecutor()` | 1 thread, unbounded queue | Sequential processing, guaranteed order |
| Scheduled | `newScheduledThreadPool(n)` | n threads, delayed/periodic tasks | Cron-like tasks, timers |
| WorkStealing | `newWorkStealingPool()` | ForkJoinPool with n = CPU cores | CPU-bound parallel work (divide-and-conquer) |

```java
// CPU-bound: fixed pool sized to CPU cores
int cores = Runtime.getRuntime().availableProcessors();
ExecutorService cpuPool = Executors.newFixedThreadPool(cores);

// I/O-bound: larger pool (threads spend most time waiting)
ExecutorService ioPool = Executors.newFixedThreadPool(cores * 8);

// ⚠️ Avoid newCachedThreadPool in production — can create unlimited threads
```

**Critical:** Always size thread pools based on task type:
- **CPU-bound:** Pool size ≈ number of CPU cores (Brian Goetz formula: `N_threads = N_cpu * U_cpu * (1 + W/C)`)
- **I/O-bound:** Pool size >> CPU cores because threads spend most time blocked on I/O

---

**Q25. 🔴 Why should you avoid `Executors.newFixedThreadPool` and `newCachedThreadPool` in production?**

Both use **unbounded queues** (`LinkedBlockingQueue` with `Integer.MAX_VALUE` capacity):
- `newFixedThreadPool`: Bounded threads but **unbounded queue** → memory overflow if tasks pile up faster than processing.
- `newCachedThreadPool`: Bounded queue (SynchronousQueue) but **unbounded threads** → can create thousands of threads under load → thread exhaustion / OOM.

**Best practice:** Create `ThreadPoolExecutor` explicitly with bounded queue and rejection policy:

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    4,                              // core pool size
    8,                              // max pool size
    60L, TimeUnit.SECONDS,          // idle thread keepalive
    new ArrayBlockingQueue<>(100),  // bounded queue
    new ThreadPoolExecutor.CallerRunsPolicy() // rejection policy
);
```

---

**Q26. 🔴 What are the Rejection Policies in ThreadPoolExecutor?**

When the pool is saturated (all threads busy AND queue full), the rejection handler decides what to do:

| Policy | Behavior | When to use |
|--------|----------|-------------|
| `AbortPolicy` (default) | Throws `RejectedExecutionException` | When you want to fail loudly |
| `CallerRunsPolicy` | Runs task in the calling thread (backpressure) | When you want to slow down producers |
| `DiscardPolicy` | Silently discards the new task | When dropping is acceptable |
| `DiscardOldestPolicy` | Discards oldest queued task, then retries | When old tasks are stale |

```java
// CallerRunsPolicy is the best for backpressure — slows down the caller
new ThreadPoolExecutor(4, 8, 60, TimeUnit.SECONDS,
    new ArrayBlockingQueue<>(100),
    new ThreadPoolExecutor.CallerRunsPolicy());
```

**CallerRunsPolicy** effectively implements backpressure: when the pool is full, the producer thread runs the task itself instead of submitting, which slows down the producer and gives the pool time to catch up.

---

### 2.2 synchronized vs Lock

**Q27. 🔴 What is the difference between `synchronized` and `ReentrantLock`?**

| Feature | synchronized | ReentrantLock |
|---------|-------------|---------------|
| Release | Automatic (block exit) | Manual — must call `unlock()` in finally |
| Try-lock | No (blocks indefinitely) | `tryLock(timeout)` — non-blocking attempt |
| Fairness | Unfair only | Fair mode available (`new ReentrantLock(true)`) |
| Condition | One wait-set (`wait/notify`) | Multiple `Condition` objects |
| Interruptible | No | `lockInterruptibly()` — responds to interrupts |
| Read/Write separation | No | `ReadWriteLock`, `StampedLock` |
| Performance | Optimized by JVM (biased locking, lock coarsening) | More overhead but more flexible |

```java
// synchronized — simple, automatic release
synchronized (lock) {
    // critical section
} // lock released automatically

// ReentrantLock — flexible, manual release
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    // critical section
} finally {
    lock.unlock(); // MUST be in finally
}

// tryLock with timeout — non-blocking
if (lock.tryLock(5, TimeUnit.SECONDS)) {
    try { /* critical section */ }
    finally { lock.unlock(); }
} else {
    // timeout — do alternative work
}
```

**When to use ReentrantLock:** When you need try-lock, timeouts, fairness, multiple conditions, or interruptible locking. When none of these are needed, `synchronized` is simpler and sufficient.

---

**Q28. 🔴 What is `ReadWriteLock`? When would you use it?**

`ReadWriteLock` maintains a pair of locks: one for read and one for write. Multiple threads can hold the read lock simultaneously, but only one can hold the write lock (and no readers while writing).

```java
ReadWriteLock rwLock = new ReentrantReadWriteLock();

// Read lock — multiple concurrent readers
rwLock.readLock().lock();
try {
    return cache.get(key); // safe concurrent read
} finally {
    rwLock.readLock().unlock();
}

// Write lock — exclusive
rwLock.writeLock().lock();
try {
    cache.put(key, value);
} finally {
    rwLock.writeLock().unlock();
}
```

**Use case:** Read-heavy, write-rare caches. If 90% of operations are reads, ReadWriteLock allows them all to proceed concurrently, with write exclusivity only when needed.

**Trade-off:** The overhead of managing two locks is higher than a simple lock. If reads and writes are roughly equal, a plain `ReentrantLock` may be faster. Also, **write starvation** can occur if readers keep arriving (depending on fairness setting).

---

**Q29. 🟡 What is `StampedLock`? How does it differ from `ReadWriteLock`?**

`StampedLock` (Java 8+) adds **optimistic reading** — a read that doesn't acquire any lock at all. It returns a "stamp" (long). After reading, you validate the stamp; if no write occurred, the read was consistent. If a write occurred, you upgrade to a read lock and retry.

```java
StampedLock lock = new StampedLock();

// Optimistic read — no lock acquired
long stamp = lock.tryOptimisticRead();
double x = this.x, y = this.y;
if (!lock.validate(stamp)) {
    // Write occurred — upgrade to read lock
    stamp = lock.readLock();
    try {
        x = this.x; y = this.y;
    } finally {
        lock.unlockRead(stamp);
    }
}
return Math.sqrt(x * x + y * y);
```

**Advantages over ReadWriteLock:**
- Optimistic reads are lock-free → no contention among readers.
- Better throughput for read-heavy workloads.

**Disadvantages:**
- Not reentrant — a thread holding a read lock cannot acquire it again.
- More complex to use correctly (must handle validate failures).
- Not a drop-in replacement — use only when you understand the trade-offs.

---

### 2.3 volatile

**Q30. 🔴 What does `volatile` do? When do you use it?**

`volatile` provides two guarantees:
1. **Visibility:** When one thread writes to a volatile variable, all other threads immediately see the new value. Without volatile, threads may cache the value in CPU registers/level caches and never see the update.
2. **Happens-before ordering:** A write to a volatile variable happens-before every subsequent read of that variable. This means all writes before the volatile write are also visible to threads that read the volatile.

```java
// Flag to stop a thread — without volatile, the thread may never see the update
private volatile boolean running = true;

public void run() {
    while (running) {
        // do work
    }
}

public void stop() {
    running = false; // visible to the run() thread immediately
}
```

**What volatile does NOT do:** It does NOT make compound operations atomic. `count++` is still a race condition even if `count` is volatile, because it's read-modify-write (3 separate operations: read, add, write).

```java
// ❌ Not thread-safe even with volatile
private volatile int count = 0;
count++; // race condition — read, add, write

// ✅ Use AtomicInteger for atomic compound operations
private AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet(); // atomic
```

---

**Q31. 🟡 What is the Java Memory Model (JMM)? How does it relate to volatile?**

The JMM defines the rules for how threads interact with memory. Key concepts:

1. **Main memory vs working memory:** Each thread has a working memory (CPU cache/registers). Without synchronization, a thread may not see another thread's writes.

2. **Happens-before relationship:** Establishes ordering between operations across threads:
   - Program order rule: Actions in a thread happen in the order they appear in code.
   - Monitor lock rule: An unlock on a lock happens-before every subsequent lock on that same lock.
   - Volatile variable rule: A write to a volatile field happens-before every subsequent read of that field.
   - Thread start rule: `Thread.start()` happens-before any actions in the started thread.
   - Thread termination rule: Actions in a thread happen-before another thread detects it has terminated (`Thread.join()`).

3. **Data races:** Without happens-before, a data race occurs — the result is undefined. volatile, synchronized, and the java.util.concurrent classes all establish happens-before.

```java
// Without volatile — data race, thread may loop forever
boolean ready = false;
// Thread A
data = 42;    // (1) write to data
ready = true; // (2) without volatile, (1) may not be visible to Thread B

// Thread B
while (!ready) {} // may loop forever
print(data);     // may print 0 (default) instead of 42

// With volatile boolean ready — (1) happens-before (2) happens-before read
```

---

### 2.4 CompletableFuture

**Q32. 🔴 What is CompletableFuture? How do you chain async operations?**

`CompletableFuture` (Java 8) represents a future result that can be composed, combined, and handled without blocking. Unlike `Future.get()` which blocks, CompletableFuture allows you to attach callbacks.

```java
// Supply (async) → transform → consume
CompletableFuture.supplyAsync(() -> fetchUser(userId))     // CompletableFuture<User>
    .thenApply(user -> user.getName())                     // CompletableFuture<String>
    .thenAccept(name -> System.out.println(name))          // CompletableFuture<Void>
    .thenRun(() -> System.out.println("done"));             // CompletableFuture<Void>

// Combine two independent futures
CompletableFuture<User> userFuture = CompletableFuture.supplyAsync(() -> fetchUser(id));
CompletableFuture<Order> orderFuture = CompletableFuture.supplyAsync(() -> fetchOrder(id));

CompletableFuture<String> combined = userFuture.thenCombine(orderFuture,
    (user, order) -> user.getName() + " ordered " + order.getProduct());

// Compose — dependent async (flatMap)
CompletableFuture.supplyAsync(() -> fetchUser(id))
    .thenCompose(user -> CompletableFuture.supplyAsync(() -> fetchOrders(user))) // flatten
    .thenAccept(orders -> System.out.println(orders.size()));
```

**Key methods:**

| Method | Input | Output | Runs in |
|--------|-------|--------|---------|
| `thenApply` | Function<T,R> | CompletableFuture<R> | Same or async thread |
| `thenAccept` | Consumer<T> | CompletableFuture<Void> | Same or async thread |
| `thenRun` | Runnable | CompletableFuture<Void> | Same or async thread |
| `thenCombine` | BiFunction | CompletableFuture<R> | Both futures complete |
| `thenCompose` | Function<T, CompletableFuture<R>> | CompletableFuture<R> (flat) | Dependent async |
| `exceptionally` | Function<Throwable,T> | CompletableFuture<T> | On exception |
| `handle` | BiFunction<T,Throwable,R> | CompletableFuture<R> | Always |
| `whenComplete` | BiConsumer<T,Throwable> | CompletableFuture<T> | Always (side-effect) |

---

**Q33. 🔴 How do you handle exceptions in CompletableFuture?**

```java
CompletableFuture.supplyAsync(() -> {
    if (error) throw new RuntimeException("fetch failed");
    return "success";
})
.exceptionally(ex -> {
    log.error("Failed", ex);
    return "fallback"; // recovery value
})
.thenAccept(result -> System.out.println(result)); // "fallback" if exception, "success" otherwise

// handle — process both success and exception
.handle((result, ex) -> {
    if (ex != null) return "recovered: " + ex.getMessage();
    return result;
})

// whenComplete — side-effect without modifying result (like finally)
.whenComplete((result, ex) -> {
    if (ex != null) log.error("Failed", ex);
    else log.info("Done: " + result);
});
```

**Key difference:**
- `exceptionally` only fires on exception → provides recovery value.
- `handle` fires on both success and exception → can transform either.
- `whenComplete` fires on both → side-effect only, does NOT change the result (like a finally block).

---

**Q34. 🟡 How do you run multiple CompletableFutures in parallel and wait for all?**

```java
List<CompletableFuture<String>> futures = ids.stream()
    .map(id -> CompletableFuture.supplyAsync(() -> fetchUser(id)))
    .toList();

// Wait for ALL to complete
CompletableFuture<Void> allOf = CompletableFuture.allOf(
    futures.toArray(new CompletableFuture[0]));
allOf.join(); // blocks until all complete

// Get all results
List<String> results = futures.stream()
    .map(CompletableFuture::join)
    .toList();

// Wait for ANY (first to complete)
CompletableFuture<Object> anyOf = CompletableFuture.anyOf(
    futures.toArray(new CompletableFuture[0]));
Object firstResult = anyOf.join();
```

**allOf vs anyOf:**
- `allOf(cf...)` → `CompletableFuture<Void>` — completes when all complete (doesn't carry results; you collect them separately via `join()`).
- `anyOf(cf...)` → `CompletableFuture<Object>` — completes when any one completes (carries the first result).

---

### 2.5 Virtual Threads (Java 21)

**Q35. 🔴 What are Virtual Threads? How do they differ from Platform Threads?**

Virtual threads (Project Loom, Java 21) are lightweight threads managed by the JVM, not the OS. The JVM schedules them on a small number of "carrier" platform threads (a ForkJoinPool).

| Feature | Platform Threads | Virtual Threads |
|---------|-----------------|-----------------|
| Managed by | OS | JVM (on carrier threads) |
| Memory | ~1 MB per thread stack | ~few KB per thread |
| Count | Limited (~thousands) | Millions |
| Creation cost | Expensive (OS syscall) | Cheap (JVM object) |
| Blocking | Blocks OS thread | Unmounts from carrier, frees it for others |
| Best for | CPU-bound work | I/O-bound, blocking operations |
| Not good for | — | CPU-bound (no benefit), `synchronized` blocks (pins carrier) |

```java
// Platform thread — OS thread
Thread platformThread = new Thread(() -> doWork());
platformThread.start();

// Virtual thread — lightweight, managed by JVM
Thread virtualThread = Thread.startVirtualThread(() -> doWork());

// Virtual thread executor
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i ->
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1)); // doesn't block OS thread
            return fetchData(i);
        })
    );
} // 10,000 virtual threads, only ~CPU-count carrier threads
```

**Why this matters for BFSI:** Instead of managing complex thread pools for I/O-bound operations (calling downstream services, database queries, external APIs), you can create a virtual thread per request — simpler code, same throughput. Spring Boot 3.2+ supports virtual threads natively (`spring.threads.virtual.enabled=true`).

---

**Q36. 🟡 What is thread pinning? When does it happen with virtual threads?**

**Thread pinning** occurs when a virtual thread is "pinned" to its carrier platform thread and cannot be unmounted. The carrier thread is blocked and unavailable for other virtual threads.

**Causes of pinning:**
1. **`synchronized` blocks** — the virtual thread cannot unmount while inside a synchronized block. (Fixed in Java 24 with JEP 491 — but until then, use `ReentrantLock` instead of `synchronized` in virtual-thread-heavy code.)
2. **Native methods (JNI)** — the virtual thread cannot unmount during a native call.

```java
// ❌ Pins the carrier thread — avoid with virtual threads (pre-Java 24)
public synchronized String fetchData() {
    return blockingIoCall(); // carrier thread pinned for entire duration
}

// ✅ Use ReentrantLock instead — virtual thread can unmount during blocking
private final ReentrantLock lock = new ReentrantLock();
public String fetchData() {
    lock.lock();
    try {
        return blockingIoCall(); // carrier thread freed during blocking
    } finally {
        lock.unlock();
    }
}
```

**Detection:** Use `-Djdk.tracePinnedThreads=full` JVM flag to log when pinning occurs.

---

### 2.6 ExecutorService vs ForkJoinPool

**Q37. 🔴 What is the difference between ExecutorService and ForkJoinPool?**

| Feature | ExecutorService | ForkJoinPool |
|---------|----------------|--------------|
| Task type | Independent tasks | Divide-and-conquer (ForkJoinTask) |
| Queue | Single shared queue | Per-worker deque + work-stealing |
| Work stealing | No | Yes — idle workers steal from busy workers' deques |
| Best for | Independent I/O or CPU tasks | Recursive divide-and-conquer (parallel sorting, tree traversal) |
| Parallelism level | Configurable pool size | Typically `Runtime.availableProcessors()` |

```java
// ExecutorService — submit independent tasks
ExecutorService es = Executors.newFixedThreadPool(4);
Future<Integer> f1 = es.submit(() -> compute("a"));
Future<Integer> f2 = es.submit(() -> compute("b"));

// ForkJoinPool — recursive divide-and-conquer
class SumTask extends RecursiveTask<Long> {
    private final long[] array;
    private final int start, end;
    // ... constructor
    @Override
    protected Long compute() {
        if (end - start <= THRESHOLD) {
            return computeDirectly();
        }
        int mid = (start + end) / 2;
        SumTask left = new SumTask(array, start, mid);
        SumTask right = new SumTask(array, mid, end);
        left.fork();           // submit left asynchronously
        long rightResult = right.compute(); // compute right in current thread
        long leftResult = left.join();      // wait for left
        return leftResult + rightResult;
    }
}

ForkJoinPool pool = new ForkJoinPool();
Long sum = pool.invoke(new SumTask(array, 0, array.length));
```

**Work stealing:** Each worker has its own deque. A worker processes tasks from its own deque LIFO. When its deque is empty, it "steals" from the tail of another worker's deque (FIFO). This balances load automatically and minimizes contention.

---

**Q38. 🟡 How do parallel streams relate to ForkJoinPool?**

`list.parallelStream()` uses the **common ForkJoinPool** (shared across all parallel streams in the JVM). The parallelism level defaults to `Runtime.getRuntime().availableProcessors() - 1`.

```java
// Parallel stream — uses common ForkJoinPool
int sum = list.parallelStream().mapToInt(Integer::intValue).sum();

// ⚠️ Common pool is shared — blocking I/O in a parallel stream blocks the common pool
// and affects ALL parallel streams in the JVM
list.parallelStream().map(x -> {
    Thread.sleep(1000); // ❌ blocks common pool thread — affects other parallel streams
    return x;
}).collect(Collectors.toList());

// ✅ Custom pool for blocking operations
ForkJoinPool customPool = new ForkJoinPool(4);
customPool.submit(() ->
    list.parallelStream().map(x -> blockingIoCall(x)).toList()
).get();
```

**When parallel streams help:** Large data sets, CPU-bound operations, embarrassingly parallel (no shared state, no ordering dependency).

**When they hurt:** Small data sets (overhead > benefit), I/O-bound operations (blocking pool threads), ordered operations (reduce/collect with encounter order), shared mutable state (race conditions).

---

### 2.7 Additional Concurrency Questions

**Q39. 🔴 What is a deadlock? How do you detect and prevent it?**

Deadlock: Two or more threads are blocked forever, each waiting for a lock held by the other.

```java
// Classic deadlock
private static final Object lock1 = new Object();
private static final Object lock2 = new Object();

// Thread A: locks lock1, then waits for lock2
synchronized (lock1) {
    synchronized (lock2) { /* ... */ }
}
// Thread B: locks lock2, then waits for lock1
synchronized (lock2) {
    synchronized (lock1) { /* ... */ }
}
// Deadlock! A holds lock1 waiting for lock2; B holds lock2 waiting for lock1
```

**Detection:**
```bash
# jstack — thread dump, detects deadlocks
jstack <pid> | grep -A 20 "Found Java-level deadlock"

# Or programmatically
ThreadMXBean bean = ManagementFactory.getThreadMXBean();
long[] deadlockedThreads = bean.findDeadlockedThreads(); // monitor locks
long[] deadlockedThreads = bean.findMonitorDeadlockedThreads(); // synchronized
```

**Prevention strategies:**
1. **Lock ordering** — always acquire locks in the same global order.
2. **Lock timeout** — use `tryLock(timeout)` instead of blocking `lock()`.
3. **Avoid nested locks** — don't acquire a second lock while holding one.
4. **Use higher-level abstractions** — `java.util.concurrent` classes (ConcurrentHashMap, BlockingQueue) eliminate the need for explicit locks.

---

**Q40. 🔴 What is `AtomicInteger` and how does CAS work?**

`AtomicInteger` provides lock-free, thread-safe integer operations using **CAS (Compare-And-Swap)** — a CPU-level atomic instruction.

```java
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet(); // atomic ++
counter.getAndAdd(5);      // atomic += 5 (returns old value)
counter.compareAndSet(0, 1); // if value == 0, set to 1, return true
counter.updateAndGet(x -> x * 2); // atomic function application
```

**CAS semantics:** `compareAndSet(expected, newValue)`:
1. Read current value.
2. If current == expected → set to newValue, return true.
3. If current != expected → return false (another thread modified it).

This is done as a single atomic CPU instruction (e.g., `LOCK CMPXCHG` on x86). No lock, no blocking.

```java
// Internal implementation (simplified)
public final int incrementAndGet() {
    int current, next;
    do {
        current = get();      // volatile read
        next = current + 1;
    } while (!compareAndSet(current, next)); // retry until success
    return next;
}
```

**ABA problem:** If value goes A → B → A between two CAS attempts, CAS sees A == A and succeeds, but the state changed. Solved by `AtomicStampedReference` (adds a version stamp).

---

**Q41. 🟡 What are `CountDownLatch`, `CyclicBarrier`, and `Semaphore`?**

| Synchronizer | Purpose | Reusable? |
|-------------|---------|-----------|
| CountDownLatch | Wait for N tasks to complete | No (one-shot) |
| CyclicBarrier | N threads wait for each other at a point | Yes (resets) |
| Semaphore | Limit concurrent access to N permits | Yes (permits released) |
| Phaser | Advanced barrier with phases | Yes |

```java
// CountDownLatch — wait for N completions (one-shot)
CountDownLatch latch = new CountDownLatch(3);
for (int i = 0; i < 3; i++) {
    new Thread(() -> { doWork(); latch.countDown(); }).start();
}
latch.await(); // blocks until count reaches 0
System.out.println("All done");

// CyclicBarrier — N threads wait for each other, then proceed (reusable)
CyclicBarrier barrier = new CyclicBarrier(3, () -> System.out.println("Phase done"));
for (int i = 0; i < 3; i++) {
    new Thread(() -> {
        doPart1();
        barrier.await(); // waits for all 3 threads
        doPart2();
    }).start();
}

// Semaphore — rate limiting / resource pooling
Semaphore permits = new Semaphore(5); // max 5 concurrent
permits.acquire();
try {
    doWork(); // at most 5 threads here at once
} finally {
    permits.release();
}
```

---

**Q42. 🟡 What is `ThreadLocal`? When do you use it? What are the pitfalls?**

`ThreadLocal` provides a per-thread variable — each thread has its own isolated copy.

```java
// SimpleDateFormat is NOT thread-safe — use ThreadLocal
private static final ThreadLocal<SimpleDateFormat> dateFormat =
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

String formatted = dateFormat.get().format(new Date()); // each thread has its own instance
```

**Use cases:**
- Thread-unsafe objects (SimpleDateFormat, non-thread-safe JDBC connections).
- Per-thread context (user session, transaction ID, MDC for logging).

**Pitfalls:**
1. **Memory leaks in thread pools** — ThreadLocal values are not GC'd until the thread dies. In a thread pool, threads live forever, so ThreadLocal values accumulate. Always call `threadLocal.remove()` when done.
2. **Inherited values** — `InheritableThreadLocal` passes values to child threads, but this doesn't work with thread pools (threads are reused, not created per task).
3. **Virtual threads** — with millions of virtual threads, ThreadLocal memory usage can be huge. Java 21 introduces `ScopedValue` as a lighter alternative.

```java
// ✅ Always remove
try {
    context.set(myContext);
    doWork();
} finally {
    context.remove(); // prevent leak
}
```

---

**Q43. 🔵 What is the difference between `submit()` and `execute()` in ExecutorService?**

| | execute(Runnable) | submit(Callable/Runnable) |
|---|---|---|
| Returns | void | Future<T> |
| Exception handling | Uncaught → goes to UncaughtExceptionHandler | Captured in Future, retrieved via `Future.get()` |
| Input | Runnable only | Runnable or Callable |

```java
// execute — fire and forget, exceptions go to handler
executor.execute(() -> doWork());

// submit — returns Future, can check result/exception
Future<?> future = executor.submit(() -> doWork());
try {
    future.get(); // throws ExecutionException wrapping the original
} catch (ExecutionException e) {
    e.getCause(); // original exception
}
```

---

**Q44. 🔵 What is `BlockingQueue` and its implementations?**

`BlockingQueue` is a thread-safe queue that blocks when:
- Queue is empty and you try to `take()` (blocks until element available).
- Queue is full and you try to `put()` (blocks until space available).

| Implementation | Bounded? | Characteristics |
|---------------|----------|----------------|
| `ArrayBlockingQueue` | Yes | Array-backed, FIFO, fixed capacity |
| `LinkedBlockingQueue` | Optional | Linked nodes, FIFO, optionally bounded |
| `SynchronousQueue` | Yes (1) | Zero capacity — each put waits for a take |
| `PriorityBlockingQueue` | No | Heap-backed, ordered by priority/comparator |
| `DelayQueue` | No | Elements available after their delay expires |
| `LinkedTransferQueue` | No | Transfer-based — producer can wait for consumer |

```java
// Producer-consumer pattern
BlockingQueue<Task> queue = new ArrayBlockingQueue<>(100);

// Producer
queue.put(task); // blocks if queue full

// Consumer
Task task = queue.take(); // blocks if queue empty
```

Common in BFSI: use `BlockingQueue` for decoupling producers (trade ingestion) from consumers (trade processing) with bounded capacity for backpressure.

---

## 3. JVM Internals

> JVM internals show up in interviews as a "depth check." BFSI GCCs care about this because they run high-throughput, low-latency systems where GC tuning and memory management matter.

### 3.1 Memory Model

**Q45. 🔴 What is the JVM Memory Model? Describe the key memory areas.**

```
┌─────────────────────────────────────────────┐
│                  JVM Process                 │
│  ┌──────────────────────────────────────┐   │
│  │              Heap (Shared)            │   │
│  │  ┌──────────┬──────────┬───────────┐  │   │
│  │  │  Young   │  Old     │  Metaspace │  │   │ (Java 8+: Metaspace replaces PermGen)
│  │  │  Gen     │  Gen     │           │  │   │
│  │  │ Eden +   │ Long-    │  Class     │  │   │
│  │  │ S0 + S1  │ lived    │  metadata  │  │   │
│  │  └──────────┴──────────┴───────────┘  │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │        Thread Stacks (Per-Thread)     │   │
│  │  Stack frame: local vars, operand    │   │
│  │  stack, frame data                   │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │    Direct Memory (NIO buffers)       │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

| Area | Thread-shared? | Contents | OOM error |
|------|----------------|----------|-----------|
| Heap | Yes | Object instances, arrays | `java.lang.OutOfMemoryError: Java heap space` |
| Metaspace | Yes | Class metadata, method bytecode | `OutOfMemoryError: Metaspace` |
| Stack | No (per-thread) | Stack frames, local variables | `StackOverflowError` |
| Direct Memory | Yes | NIO ByteBuffers | `OutOfMemoryError: Direct buffer memory` |
| Code Cache | Yes | JIT-compiled native code | `OutOfMemoryError: CodeCache is full` |

**Heap generations:**
- **Young Generation (Eden + Survivor 0 + Survivor 1):** New objects. Minor GC runs frequently, is fast (stop-the-world but brief).
- **Old Generation:** Objects that survived multiple minor GCs (long-lived). Major GC runs less frequently but is slower.
- **Metaspace (Java 8+):** Replaced PermGen. Stores class metadata. Grows automatically up to system memory limit (or `-XX:MaxMetaspaceSize`).

---

**Q46. 🟡 What is the difference between Stack and Heap? When is an object allocated on the stack?**

| | Stack | Heap |
|---|-------|------|
| Size | Small (~512 KB default per thread) | Large (GBs) |
| Speed | Fast (pointer bump) | Slower (pointer bump + GC) |
| Lifetime | Method scope (auto-cleaned) | Until GC collects |
| Contents | Primitives, references | Objects, arrays |
| Shared | Per-thread | All threads |

**Escape analysis (Java 8+):** The JIT compiler can allocate objects on the stack (instead of heap) if the object does not "escape" the method — meaning it's never passed to another method or stored in a field. This eliminates the GC overhead for that object entirely.

```java
public int sum() {
    Point p = new Point(1, 2); // may be stack-allocated if escape analysis confirms
    return p.x + p.y;           // p doesn't escape this method
}
```

Escape analysis is enabled by default (`-XX:+DoEscapeAnalysis`). Stack allocation is an optimization — you don't control it directly.

---

### 3.2 Garbage Collection

**Q47. 🔴 What is the generational garbage collection hypothesis?**

The **Weak Generational Hypothesis** states:
1. **Most objects die young** (are unreachable shortly after creation) → Young GC is frequent and fast.
2. **Few references from old objects to young objects** → Minor GC doesn't need to scan the old generation.

This justifies splitting the heap into generations:
- **Minor GC:** Scans only young generation (Eden + survivors). Fast because the young gen is small and most objects are dead (copy only survivors).
- **Major GC / Full GC:** Scans entire heap (young + old). Slow because it scans everything.

**Object lifecycle:**
1. Allocated in Eden.
2. Survives minor GC → moved to Survivor 0 (S0).
3. Survives more minor GCs → moved between S0 and S1, age counter increments.
4. Age exceeds threshold (default 15, `-XX:MaxTenuringThreshold`) → promoted to Old Generation.
5. Old Generation object is collected during major GC.

---

**Q48. 🔴 Compare G1 GC and ZGC. When would you choose each?**

| Feature | G1 GC | ZGC |
|---------|-------|-----|
| Target | Throughput + predictable pauses | Ultra-low latency (< 1 ms) |
| Max pause | ~200 ms (target adjustable) | < 1 ms (sub-millisecond) |
| Heap sizes | 4 GB – 64 GB | 8 GB – 16 TB |
| Region size | 1-32 MB | Dynamic (ZPage) |
| Concurrency | Partially concurrent (mostly STW) | Fully concurrent (almost no STW) |
| Compaction | Concurrent | Concurrent |
| Generational | Yes (young/old within regions) | Yes (Java 21 — generational ZGC) |
| Default | Yes (Java 9+) | No (opt-in: `-XX:+UseZGC`) |
| Best for | General server apps, medium-large heaps | Low-latency, large-heap apps |

```bash
# G1 GC (default since Java 9)
java -XX:+UseG1GC -Xmx4g -XX:MaxGCPauseMillis=200 MyApp

# ZGC (ultra-low latency)
java -XX:+UseZGC -Xmx16g -XX:ZGenerational=true MyApp  # Java 21+ generational ZGC
```

**When to choose G1:** General-purpose server applications, heap 4-64 GB, where brief pauses (100-200ms) are acceptable. Good default for most BFSI backend services.

**When to choose ZGC:** Low-latency applications (trading systems, real-time market data), very large heaps (64GB+), where pauses must be < 1ms. BFSI trading systems often use ZGC (or Shenandoah).

---

**Q49. 🔴 How does G1 GC work internally?**

G1 (Garbage-First) divides the heap into **regions** (1-32 MB each), each labeled as Eden, Survivor, Old, or Humongous. G1 tracks the "garbage" (dead objects) in each region and collects the regions with the most garbage first (hence "Garbage-First").

```
G1 Heap Layout (region-based):
┌────┬────┬────┬────┬────┬────┬────┬────┐
│ E  │ S  │ O  │ E  │ H  │ O  │ E  │ O  │  E=Eden, S=Survivor, O=Old, H=Humongous
├────┼────┼────┼────┼────┼────┼────┼────┤
│ O  │ E  │ -  │ O  │ E  │ S  │ O  │ E  │  -=Free
└────┴────┴────┴────┴────┴────┴────┴────┘
```

**GC cycle:**
1. **Young GC (STW):** Collect Eden + Survivor regions. Copy survivors to new Survivor regions. Brief pause.
2. **Concurrent Marking:** Identifies live objects across all regions (runs concurrently with application). Determines garbage density per region.
3. **Mixed GC (STW):** Collects young regions + a selection of old regions with the most garbage ("Garbage-First"). Pauses are bounded by `MaxGCPauseMillis` target.
4. **Evacuation:** Live objects copied to empty regions (compaction). Dead regions become free.

**Key advantage:** Pause times are predictable and bounded because G1 collects a subset of regions, not the entire heap. You set `MaxGCPauseMillis=200` and G1 adjusts region collection to meet it.

**Humongous objects:** Objects > 50% of region size are allocated as "humongous" — spanning one or more contiguous regions. These are allocated directly in old gen and are a common source of GC issues.

---

**Q50. 🟡 What are the common GC-related JVM flags?**

```bash
# Heap sizing
-Xms4g                          # Initial heap (set equal to -Xmx to avoid resizing)
-Xmx4g                          # Max heap
-XX:NewRatio=2                  # Young:Old = 1:2 (Young = 1/3 of heap)
-XX:SurvivorRatio=8             # Eden:Survivor = 8:1:1

# GC selection
-XX:+UseG1GC                    # Use G1 (default in Java 9+)
-XX:+UseZGC                     # Use ZGC
-XX:+UseParallelGC              # Use Parallel (throughput-focused)

# G1 tuning
-XX:MaxGCPauseMillis=200        # Target pause time
-XX:G1HeapRegionSize=16m        # Region size

# GC logging
-Xlog:gc*:file=gc.log:time      # Java 9+ unified logging
-XX:+PrintGCDetails             # Java 8 (deprecated in 9+)

# Metaspace
-XX:MaxMetaspaceSize=512m       # Cap metaspace

# Diagnostic
-XX:+HeapDumpOnOutOfMemoryError # Auto heap dump on OOM
-XX:HeapDumpPath=/tmp/dumps     # Heap dump location
```

---

### 3.3 Classloading

**Q51. 🔴 What is the ClassLoader hierarchy in Java?**

```
Bootstrap ClassLoader (C++, loads rt.jar / java.base module)
        ↑ parent
Platform ClassLoader (loads JDK modules — extension in Java 8)
        ↑ parent
Application ClassLoader (loads your application classes, classpath)
        ↑ parent
Custom ClassLoader(s) (your own — e.g., for plugins, hot-deploy)
```

**Parent-delegation model:** When a class is requested, the classloader first asks its parent to load it. Only if the parent cannot find it does the classloader attempt to load it itself. This ensures core Java classes (`java.lang.String`) are always loaded by the Bootstrap classloader — preventing a malicious classloader from replacing them.

```java
// The hierarchy
ClassLoader appLoader = MyClass.class.getClassLoader();
ClassLoader platformLoader = appLoader.getParent();   // Platform ClassLoader
ClassLoader bootstrapLoader = platformLoader.getParent(); // Returns null — Bootstrap is native C++
```

---

**Q52. 🔴 What is the difference between `NoClassDefFoundError` and `ClassNotFoundException`?**

| | NoClassDefFoundError | ClassNotFoundException |
|---|----------------------|----------------------|
| Type | Error (unchecked) | Checked Exception |
| When | Class was available at compile time but missing at runtime | Class not found when dynamically loading |
| Cause | JAR missing from classpath, class deleted | `Class.forName()` or `loadClass()` failed |
| Example | Missing dependency at runtime | JDBC driver not in classpath |

```java
// ClassNotFoundException — checked, must handle
try {
    Class.forName("com.mysql.cj.jdbc.Driver"); // throws if not found
} catch (ClassNotFoundException e) {
    // driver not in classpath
}

// NoClassDefFoundError — error, not expected at compile time
public class App {
    public static void main(String[] args) {
        MissingClass.doSomething(); // compiled fine, but MissingClass.jar not at runtime
        // → NoClassDefFoundError at runtime
    }
}
```

**Another common confusion:** `NoClassDefFoundError` can also occur when a class fails to initialize (static initializer throws an exception). The first access throws `ExceptionInInitializerError`; subsequent accesses throw `NoClassDefFoundError`.

---

**Q53. 🟡 Can you create a custom ClassLoader? Why would you?**

```java
public class CustomClassLoader extends ClassLoader {
    private final String classDir;

    public CustomClassLoader(String classDir, ClassLoader parent) {
        super(parent);
        this.classDir = classDir;
    }

    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] classBytes = loadClassBytes(name);
        return defineClass(name, classBytes, 0, classBytes.length);
    }

    private byte[] loadClassBytes(String name) {
        String path = classDir + "/" + name.replace('.', '/') + ".class";
        // read file bytes...
        return Files.readAllBytes(Path.of(path));
    }
}
```

**Use cases:**
- **Hot deployment** — reload classes without restarting the JVM (e.g., Tomcat, JBoss).
- **Isolation** — application servers load each app with its own classloader (class isolation).
- **Encryption** — decrypt class files before loading (security).
- **Dynamic proxy / bytecode generation** — load generated classes at runtime (e.g., Spring AOP proxies).

---

### 3.4 Diagnostics: Heap Dumps, Thread Dumps, jstack

**Q54. 🔴 How do you capture and analyze a thread dump? What do you look for?**

A thread dump is a snapshot of all thread states at a given moment. It shows each thread's name, state (RUNNABLE, BLOCKED, WAITING), and stack trace.

```bash
# Capture thread dump
jstack <pid> > thread_dump.txt

# Or using jcmd (Java 8+)
jcmd <pid> Thread.print > thread_dump.txt

# Or using kill (Linux)
kill -3 <pid>  # prints to stdout / log
```

**What to look for:**
1. **Deadlocks** — `jstack` detects and reports "Found Java-level deadlock" at the top.
2. **BLOCKED threads** — threads waiting on a monitor lock (look for `- waiting to lock <0x...>`).
3. **High CPU threads** — RUNNABLE threads in tight loops (combine with `top -Hp <pid>` to find the thread using CPU, then map to jstack output via nid).
4. **Thread starvation** — many WAITING threads that never get scheduled.
5. **Connection leaks** — threads stuck in Socket read (waiting on external service).

```bash
# Find highest CPU thread
top -Hp <pid>
# Convert the thread's PID to hex
printf "%x\n" <thread_pid>
# Search in thread dump
grep "nid=0x<hex_value>" thread_dump.txt
```

---

**Q55. 🔴 How do you capture and analyze a heap dump?**

A heap dump is a snapshot of the entire heap at a point in time — all live objects, their sizes, and references.

```bash
# Capture heap dump
jcmd <pid> GC.heap_dump /tmp/heap.hprof

# Or with jmap (older)
jmap -dump:format=b,file=/tmp/heap.hprof <pid>

# Or automatically on OOM (add to JVM args)
-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/dumps/
```

**Analysis tools:**
1. **Eclipse MAT (Memory Analyzer Tool):** Best tool — automated leak suspects report, dominator tree, OQL queries.
2. **VisualVM:** GUI tool, lighter analysis.
3. **jhat (deprecated):** Command-line HTML viewer.

**Analysis steps:**
1. Open the `.hprof` file in Eclipse MAT.
2. Run the **Leak Suspects Report** — identifies the largest retained objects.
3. Check the **Dominator Tree** — sorted by retained heap size.
4. Use **Path to GC Roots** for a specific object — shows what's preventing GC.
5. Look for: large collections that grow without bound, caches without eviction, ThreadLocal values not removed, unclosed resources.

---

**Q56. 🟡 What are the key `jcmd` commands for JVM diagnostics?**

```bash
# List all JVM processes
jcmd -l

# Thread dump
jcmd <pid> Thread.print

# Heap dump
jcmd <pid> GC.heap_dump /tmp/heap.hprof

# GC info
jcmd <pid> GC.heap_info
jcmd <pid> GC.run                   # request GC

# Class histogram (top classes by instance count)
jcmd <pid> GC.class_histogram

# JVM flags (all set flags)
jcmd <pid> VM.flags

# System properties
jcmd <pid> VM.system_properties

# Native memory tracking
jcmd <pid> VM.native_memory          # requires -XX:NativeMemoryTracking=summary

# Diagnostic operations
jcmd <pid> VM.classloader_stats
jcmd <pid> ManagementAgent.start jmxremote.port=9010
```

**`jcmd` vs `jstack`/`jmap`:** `jcmd` is the modern, unified replacement for `jstack`, `jmap`, `jstat`, and `jinfo`. All these older tools still work but `jcmd` is recommended for Java 8+.

---

**Q57. 🟡 How do you diagnose high CPU usage in a Java application?**

**Step 1:** Identify the Java process
```bash
top -c        # find the JVM process with high CPU
# Note the PID, e.g., 12345
```

**Step 2:** Find the thread consuming CPU
```bash
top -Hp 12345 # -H shows threads, -p filters to process
# Note the thread TID with high CPU, e.g., 12350
```

**Step 3:** Convert TID to hex
```bash
printf "%x\n" 12350  # output: 303e
```

**Step 4:** Find the thread in jstack
```bash
jstack 12345 > dump.txt
grep "nid=0x303e" -A 30 dump.txt
# The stack trace shows exactly what that thread is doing
```

**Common causes:**
- Infinite loop or tight loop
- Excessive GC (check with `jstat -gc <pid> 1000` — if GC time is high)
- Regex catastrophic backtracking (`Pattern.compile` on pathological input)
- Thread contention (check BLOCKED threads in dump)
- Busy-wait spin loops

---

### 3.5 Additional JVM Questions

**Q58. 🔵 What is JIT compilation? What are C1 and C2 compilers?**

The JIT (Just-In-Time) compiler converts frequently executed bytecode to native machine code at runtime for faster execution.

**Tiered compilation (Java 8+):**
- **C1 (Client compiler):** Fast compilation, simple optimizations. Gets code running quickly.
- **C2 (Server compiler):** Slow compilation, aggressive optimizations (loop unrolling, inlining, escape analysis). Maximizes peak performance.

**Compilation tiers:**
1. Interpreter (no compilation) → fastest startup
2. C1 with profiling → quick optimizations + collect profile data
3. C1 with full profiling → more profiling data
4. C2 → aggressive optimizations based on profile data

```bash
# Flags
-XX:+TieredCompilation          # Enable tiered (default since Java 8)
-XX:TieredStopAtLevel=1         # C1 only (fast startup, lower peak — used by GraalVM native image)
-XX:+PrintCompilation           # Log JIT compilation events
```

**Inlining:** The most important optimization. If method A calls method B, and B is small enough, the JIT inlines B's body into A — eliminating the method call overhead entirely. Controlled by `-XX:MaxInlineSize` (default 35 bytes).

---

**Q59. 🔵 What is the String pool? How does `intern()` work?**

The String pool (string constant pool) is a special memory area in the heap (Java 7+) where String literals are stored. It enables String reuse to save memory.

```java
// Literal — goes to String pool
String s1 = "hello";
String s2 = "hello";
System.out.println(s1 == s2); // true — same pool reference

// new String — creates a new object on heap, NOT in pool
String s3 = new String("hello");
System.out.println(s1 == s3); // false — different objects

// intern() — returns pool reference, adds to pool if not present
String s4 = s3.intern();
System.out.println(s1 == s4); // true — s4 now refers to pool entry
```

**How it works:** When a String literal is encountered, the JVM checks the pool. If an equal String exists (by `equals()`), it returns that reference. Otherwise, it adds the new String to the pool.

**`intern()` on `new String`:** `s3.intern()` checks if "hello" is in the pool. If yes, returns the pool reference. If no, adds `s3` to the pool and returns it. After interning, `s1 == s4` is true.

**Caution:** Overuse of `intern()` on dynamically generated strings (e.g., parsing millions of strings from a file) can bloat the String pool and cause GC pressure. Use it for a known, small set of repeated values.

---

## 4. Exceptions

### 4.1 Checked vs Unchecked

**Q60. 🔴 What is the difference between checked and unchecked exceptions?**

| | Checked Exceptions | Unchecked Exceptions |
|---|---|---|
| Subclass of | `Exception` (not `RuntimeException`) | `RuntimeException` or `Error` |
| Compiler check | Must catch or declare (throws) | No compiler check |
| Use case | Recoverable, expected (IO, SQL, network) | Programming errors (NPE, illegal argument) |
| Examples | `IOException`, `SQLException`, `ClassNotFoundException` | `NullPointerException`, `IllegalArgumentException`, `ArrayIndexOutOfBoundsException` |

```java
// Checked — must handle
public void readFile() throws IOException { // or try-catch
    Files.readString(Path.of("file.txt"));
}

// Unchecked — no handling required
public void divide(int a, int b) {
    if (b == 0) throw new ArithmeticException("division by zero"); // unchecked
    return a / b;
}
```

**Philosophy:** Checked exceptions force the caller to handle recoverable conditions (file not found, network timeout). Unchecked exceptions signal programming bugs (null dereference, invalid argument) that should be fixed in code, not caught at runtime.

**Modern view:** Many frameworks (Spring) wrap checked exceptions in unchecked ones (`RuntimeException`) to avoid polluting method signatures. The trend is toward unchecked exceptions + centralized handling (`@ControllerAdvice`).

---

**Q61. 🟡 What is the exception hierarchy in Java?**

```
Throwable
├── Error (unchecked — don't catch)
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── VirtualMachineError
└── Exception
    ├── RuntimeException (unchecked)
    │   ├── NullPointerException
    │   ├── IllegalArgumentException
    │   ├── IllegalStateException
    │   ├── ArrayIndexOutOfBoundsException
    │   ├── ClassCastException
    │   ├── ArithmeticException
    │   └── ConcurrentModificationException
    └── [Other Exception subclasses — checked]
        ├── IOException
        │   ├── FileNotFoundException
        │   └── EOFException
        ├── SQLException
        ├── ClassNotFoundException
        └── InterruptedException
```

**Error vs Exception:**
- **Error:** JVM-level failures (OOM, stack overflow). You should NOT catch these — the application is in an unrecoverable state.
- **Exception:** Application-level failures. Checked exceptions are recoverable; RuntimeExceptions are programming bugs.

---

### 4.2 Custom Exceptions

**Q62. 🔴 How do you create a custom exception?**

```java
// Custom checked exception
public class TradeValidationException extends Exception {
    public TradeValidationException(String message) {
        super(message);
    }
    public TradeValidationException(String message, Throwable cause) {
        super(message, cause); // always chain the cause
    }
}

// Custom unchecked exception
public class InvalidTradeStateException extends RuntimeException {
    public InvalidTradeStateException(String message) {
        super(message);
    }
    public InvalidTradeStateException(String message, Throwable cause) {
        super(message, cause);
    }
}

// Usage
public Trade processTrade(Trade trade) throws TradeValidationException {
    if (trade.getNotional() <= 0) {
        throw new TradeValidationException("Notional must be positive: " + trade.getNotional());
    }
    return trade;
}
```

**Best practices:**
1. Always provide both `String message` and `(String message, Throwable cause)` constructors.
2. Prefer unchecked (extend `RuntimeException`) for domain exceptions in modern frameworks.
3. Use checked exceptions only when the caller can meaningfully recover.
4. Always chain the cause (`super(message, cause)`) when wrapping exceptions — preserves the stack trace.

---

**Q63. 🟡 What is exception chaining? Why is it important?**

Exception chaining preserves the original exception's stack trace when wrapping it in a new exception. Without it, you lose the root cause.

```java
// ❌ Bad — loses the original stack trace
try {
    tradeService.process(trade);
} catch (SQLException e) {
    throw new TradeProcessingException("Failed to process trade");
    // original SQL error info lost!
}

// ✅ Good — chains the cause
try {
    tradeService.process(trade);
} catch (SQLException e) {
    throw new TradeProcessingException("Failed to process trade", e);
    // e.getCause() returns the SQLException with full stack trace
}
```

The chained exception's stack trace shows:
```
TradeProcessingException: Failed to process trade
    at TradeService.process(TradeService.java:45)
    ...
Caused by: java.sql.SQLException: Connection refused
    at com.mysql.driver.connect(Driver.java:120)
    ...
```

The "Caused by" section is the original exception — it's preserved because you passed `e` to the constructor.

---

### 4.3 try-with-resources

**Q64. 🔴 What is try-with-resources? How does it work?**

`try-with-resources` (Java 7+) automatically closes resources that implement `AutoCloseable` (or `Closeable`). The resource is closed at the end of the try block, even if an exception is thrown — no need for a finally block.

```java
// try-with-resources
try (BufferedReader reader = Files.newBufferedReader(Path.of("file.txt"));
     FileWriter writer = new FileWriter("output.txt")) {
    String line;
    while ((line = reader.readLine()) != null) {
        writer.write(line);
    }
} catch (IOException e) {
    log.error("Failed", e);
}
// reader and writer are auto-closed here (in reverse order of declaration)

// Equivalent without try-with-resources — verbose and error-prone
BufferedReader reader = null;
FileWriter writer = null;
try {
    reader = Files.newBufferedReader(Path.of("file.txt"));
    writer = new FileWriter("output.txt");
    // ...
} catch (IOException e) {
    log.error("Failed", e);
} finally {
    if (writer != null) try { writer.close(); } catch (IOException e) { /* swallowed! */ }
    if (reader != null) try { reader.close(); } catch (IOException e) { /* swallowed! */ }
}
```

**Java 9+ improvement:** You can use effectively final variables (declared outside the try):

```java
BufferedReader reader = Files.newBufferedReader(Path.of("file.txt"));
try (reader) { // reader is effectively final
    // use reader
}
```

**Suppressed exceptions:** If both the try body and `close()` throw exceptions, the `close()` exception is added as a "suppressed" exception to the primary exception:

```java
try (Resource r = new Resource()) {
    throw new RuntimeException("try body exception");
} // close() throws "close exception"
// Result: primary = "try body exception", suppressed = "close exception"
// e.getSuppressed() → ["close exception"]
```

---

**Q65. 🟡 What is the difference between `AutoCloseable` and `Closeable`?**

| | AutoCloseable | Closeable |
|---|--------------|-----------|
| Package | `java.lang` | `java.io` |
| Since | Java 7 | Java 5 |
| `close()` throws | `Exception` (broader) | `IOException` (specific) |
| Idempotent required? | No | Yes (must be safe to call multiple times) |

`Closeable` extends `AutoCloseable`. All `Closeable` resources are `AutoCloseable`, but not vice versa. For custom resources, implement `AutoCloseable` unless you're specifically dealing with I/O streams.

---

## 5. Generics

**Q66. 🔴 What are generics in Java? Why are they used?**

Generics provide **compile-time type safety** for collections and classes. They allow you to specify the type of elements a collection holds, eliminating the need for casting and catching type errors at compile time.

```java
// Without generics (pre-Java 5) — unsafe
List list = new ArrayList();
list.add("hello");
list.add(42);          // no error — Object accepts anything
String s = (String) list.get(1); // ClassCastException at runtime!

// With generics — compile-time safety
List<String> list = new ArrayList<>();
list.add("hello");
list.add(42);          // ❌ compile error — type safety at compile time
String s = list.get(0); // no cast needed
```

**Benefits:**
1. **Type safety at compile time** — errors caught before runtime.
2. **Eliminates casts** — cleaner code.
3. **Code reuse** — write one class/method that works with any type.

**Type erasure:** Java generics are implemented via type erasure. Generic type information exists only at compile time; at runtime, `List<String>` and `List<Integer>` are both just `List`. The compiler inserts casts at call sites and checks types at insertions.

---

**Q67. 🔴 What is type erasure? What are its implications?**

Type erasure is the process by which the compiler removes all generic type information at compile time, replacing type parameters with their bounds (or `Object` if unbounded).

```java
// Source code
public class Box<T> {
    private T value;
    public T get() { return value; }
    public void set(T value) { this.value = value; }
}

// After type erasure (what the JVM sees)
public class Box {
    private Object value;
    public Object get() { return value; }
    public void set(Object value) { this.value = value; }
}
```

**Implications:**
1. You cannot do `new T()` — the type parameter doesn't exist at runtime.
2. You cannot do `instanceof List<String>` — only `instanceof List`.
3. You cannot create generic arrays: `new T[]` is not allowed.
4. Static fields cannot use the class's type parameter.
5. Overloaded methods with different type parameters clash: `void m(List<String>)` and `void m(List<Integer>)` are the same after erasure.

```java
// ❌ These don't work due to erasure
class Box<T> {
    // T item = new T();              // cannot instantiate type parameter
    // T[] array = new T[10];         // cannot create generic array
    // static T defaultValue;         // static fields can't use type params
}

// ❌ Cannot overload — erasure makes them identical
void process(List<String> list) {}
void process(List<Integer> list) {} // compile error
```

---

**Q68. 🟡 What are wildcards in generics? (`<?>`, `<? extends T>`, `<? super T>`)**

Wildcards provide flexibility in generic type parameters.

```java
// ? — unbounded wildcard (any type)
void printList(List<?> list) {
    for (Object o : list) System.out.println(o); // can read, cannot add
}

// ? extends T — upper bound (T or any subtype) — PE = Producer Extends
void processNumbers(List<? extends Number> list) {
    Number n = list.get(0); // ✅ can read (safe — it's at least a Number)
    list.add(42);           // ❌ cannot add (don't know the exact type)
}

// ? super T — lower bound (T or any supertype) — CS = Consumer Super
void addNumbers(List<? super Integer> list) {
    list.add(42);             // ✅ can add Integer (safe — it accepts Integer or supertype)
    Integer i = list.get(0);  // ❌ cannot read as Integer (might be Object)
}
```

**PECS rule (Producer Extends, Consumer Super):**
- If you **read** from the collection (it produces) → `? extends T`.
- If you **write** to the collection (it consumes) → `? super T`.
- If you both read and write → don't use wildcards; use `T`.

```java
// Classic PECS example: copy from src (producer) to dest (consumer)
public static <T> void copy(List<? super T> dest, List<? extends T> src) {
    for (T item : src) dest.add(item);
}
```

---

**Q69. 🟡 What is the difference between `List`, `List<?>`, `List<Object>`, and `List<? extends Object>`?**

| Declaration | Can add? | Can read? | Type parameter |
|-------------|----------|-----------|----------------|
| `List` (raw) | Anything | Object | No type safety |
| `List<?>` | Nothing (except null) | Object | Unknown type |
| `List<Object>` | Any object | Object | Exactly Object |
| `List<? extends Object>` | Nothing (except null) | Object | Object or subtype |

```java
// List<?> — can hold any type, but you can't add (type unknown)
List<?> unknownList = new ArrayList<String>();
unknownList.add("hello"); // ❌ compile error — could be List<Integer>
Object o = unknownList.get(0); // ✅ can read as Object

// List<Object> — can hold any object
List<Object> objectList = new ArrayList<>();
objectList.add("hello"); // ✅ String is-a Object
objectList.add(42);      // ✅ Integer is-a Object

// List<String> is NOT a subtype of List<Object>!
List<String> strings = new ArrayList<>();
List<Object> objects = strings; // ❌ compile error
// Otherwise you could do objects.add(42) — corrupting the String list
```

---

**Q70. 🔵 How do you create a generic method?**

```java
// Generic method — <T> declares the type parameter
public <T> T firstElement(List<T> list) {
    if (list.isEmpty()) return null;
    return list.get(0);
}

// Multiple type parameters
public <K, V> Map<K, V> zip(List<K> keys, List<V> values) {
    Map<K, V> map = new LinkedHashMap<>();
    for (int i = 0; i < keys.size(); i++) {
        map.put(keys.get(i), values.get(i));
    }
    return map;
}

// Bounded type parameter
public <T extends Comparable<T>> T max(List<T> list) {
    T max = list.get(0);
    for (T item : list) {
        if (item.compareTo(max) > 0) max = item;
    }
    return max;
}
```

**Key:** The `<T>` before the return type declares the type parameter. It's inferred from the arguments at the call site.

---

## 6. Streams API

> Stream API questions test whether you can write idiomatic modern Java (Java 8+). BFSI interviews often include a "write this query using streams" coding question.

**Q71. 🔴 What is the Stream API? How is it different from Collections?**

A Stream is a sequence of elements supporting sequential and parallel aggregate operations (filter, map, reduce). Streams are **not data structures** — they don't store elements.

| | Collection | Stream |
|---|-----------|--------|
| Storage | Stores elements | Does not store |
| Operations | Eager | Lazy (terminal triggers) |
| Traversal | Can traverse multiple times | Traversable once |
| Purpose | Store/access data | Compute/transform data |
| Modification | Can add/remove | Cannot modify source |

```java
List<String> names = List.of("Alice", "Bob", "Charlie", "David");

// Stream pipeline: source → intermediate ops → terminal op
List<String> filtered = names.stream()
    .filter(n -> n.length() > 3)      // intermediate (lazy)
    .map(String::toUpperCase)         // intermediate (lazy)
    .sorted()                         // intermediate (lazy)
    .toList();                        // terminal (triggers execution)
```

---

**Q72. 🔴 What are intermediate vs terminal operations? Give examples.**

**Intermediate operations** are lazy — they return a new Stream and don't execute until a terminal operation is invoked.

| Intermediate | Description |
|-------------|-------------|
| `filter(Predicate)` | Keep elements matching predicate |
| `map(Function)` | Transform each element |
| `flatMap(Function)` | Transform + flatten (one-to-many) |
| `sorted()` | Sort |
| `distinct()` | Remove duplicates |
| `limit(n)` | Take first n |
| `skip(n)` | Skip first n |
| `peek(Consumer)` | Side-effect (debug) |

**Terminal operations** trigger the pipeline and produce a result or side-effect.

| Terminal | Returns | Description |
|----------|---------|-------------|
| `collect(Collector)` | Collection | Collect to List, Set, Map |
| `toList()` | List (unmodifiable) | Java 16+ shortcut |
| `reduce(BinaryOperator)` | Optional<T> | Combine elements |
| `count()` | long | Count |
| `forEach(Consumer)` | void | Side-effect per element |
| `anyMatch(Predicate)` | boolean | True if any matches |
| `allMatch(Predicate)` | boolean | True if all match |
| `findFirst()` | Optional<T> | First element |
| `findAny()` | Optional<T> | Any element (parallel-friendly) |

```java
// Intermediate are lazy — nothing happens until terminal
Stream<String> stream = names.stream()
    .filter(n -> { System.out.println("filtering " + n); return n.length() > 3; });
// Nothing printed yet!

stream.count(); // Now filtering executes
```

---

**Q73. 🔴 What is `flatMap`? How is it different from `map`?**

`map` applies a function that returns one value per element (one-to-one). `flatMap` applies a function that returns a Stream, and flattens all the Streams into one (one-to-many → flat).

```java
List<List<Integer>> nested = List.of(List.of(1, 2), List.of(3, 4), List.of(5));

// map — preserves structure
List<List<Integer>> mapped = nested.stream()
    .map(List::size)
    .toList(); // [2, 2, 1]

// flatMap — flattens
List<Integer> flattened = nested.stream()
    .flatMap(List::stream)    // each inner list becomes a Stream, then flattened
    .toList(); // [1, 2, 3, 4, 5]

// Real-world: split sentences into words
List<String> sentences = List.of("hello world", "java streams");
List<String> words = sentences.stream()
    .flatMap(s -> Arrays.stream(s.split(" ")))
    .toList(); // ["hello", "world", "java", "streams"]
```

**Mnemonic:** `map` = one-in-one-out. `flatMap` = one-in-stream-out, then flatten all streams together.

---

**Q74. 🟡 What is `reduce`? How do you use it?**

`reduce` combines all elements into a single result using an accumulator.

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5);

// 1. reduce with identity
int sum = numbers.stream().reduce(0, Integer::sum); // 15
int product = numbers.stream().reduce(1, (a, b) -> a * b); // 120

// 2. reduce without identity — returns Optional (empty stream → empty Optional)
Optional<Integer> sumOpt = numbers.stream().reduce(Integer::sum);
// sumOpt.get() → 15; empty stream → Optional.empty()

// 3. reduce with identity, accumulator, combiner (for parallel streams)
int sumParallel = numbers.parallelStream()
    .reduce(0,                    // identity
            Integer::sum,          // accumulator (per-thread)
            Integer::sum);          // combiner (combine partial results)
```

**reduce vs collect:** `reduce` produces an immutable value (combines into one). `collect` produces a mutable container (mutates and accumulates into a collection). Use `collect` for building collections; use `reduce` for computing a single value (sum, product, max).

---

**Q75. 🟡 How do you collect a Stream into a Map?**

```java
List<Trade> trades = List.of(
    new Trade("T1", "AAPL", 100),
    new Trade("T2", "GOOG", 200),
    new Trade("T3", "AAPL", 150)
);

// Collect to Map: key=tradeId, value=trade
Map<String, Trade> byId = trades.stream()
    .collect(Collectors.toMap(Trade::getId, trade -> trade));

// key=symbol, value=notional (handles duplicates — keep existing)
Map<String, Integer> notionalBySymbol = trades.stream()
    .collect(Collectors.toMap(
        Trade::getSymbol,
        Trade::getNotional,
        Integer::sum)); // merge function — sum duplicates

// Group by symbol
Map<String, List<Trade>> bySymbol = trades.stream()
    .collect(Collectors.groupingBy(Trade::getSymbol));
// {"AAPL": [T1, T3], "GOOG": [T2]}

// Group by + downstream collector (count)
Map<String, Long> countBySymbol = trades.stream()
    .collect(Collectors.groupingBy(Trade::getSymbol, Collectors.counting()));

// Group by + sum
Map<String, Integer> totalNotionalBySymbol = trades.stream()
    .collect(Collectors.groupingBy(
        Trade::getSymbol,
        Collectors.summingInt(Trade::getNotional)));

// Partitioning (boolean key)
Map<Boolean, List<Trade>> partitioned = trades.stream()
    .collect(Collectors.partitioningBy(t -> t.getNotional() > 120));
// {true: [T2, T3], false: [T1]}
```

---

**Q76. 🟡 What are short-circuiting operations in Streams?**

Short-circuiting operations don't process the entire stream — they stop as soon as the result can be determined.

**Terminal short-circuiting:**
- `findFirst()` — stops after first element
- `findAny()` — stops after any element
- `anyMatch()` — stops when first match found
- `allMatch()` — stops when first non-match found (returns false)
- `noneMatch()` — stops when first match found (returns false)

**Intermediate short-circuiting:**
- `limit(n)` — stops after n elements
- `takeWhile(Predicate)` (Java 9+) — takes elements while predicate is true
- `dropWhile(Predicate)` (Java 9+) — drops elements while predicate is true

```java
// findFirst — short-circuits
Optional<Integer> first = Stream.of(1, 2, 3, 4, 5)
    .filter(n -> n > 2)
    .findFirst(); // processes 1, 2, 3 — stops at 3 (found), doesn't process 4, 5

// takeWhile — takes while predicate holds
List<Integer> taken = Stream.of(1, 2, 3, 4, 1, 2)
    .takeWhile(n -> n < 4)
    .toList(); // [1, 2, 3] — stops at first failure
```

---

**Q77. 🔵 What are the pitfalls of parallel streams?**

1. **Shared common ForkJoinPool** — all parallel streams share one pool. Blocking I/O in a parallel stream blocks the pool, affecting all parallel streams in the JVM.

2. **Ordering overhead** — if the stream has an encounter order (List, sorted), parallel streams must maintain it, adding overhead. Use `.unordered()` if order doesn't matter.

3. **Small datasets** — overhead of splitting, managing threads, and merging exceeds the benefit for small collections (< 10,000 elements).

4. **Mutable state** — using shared mutable state (e.g., adding to a shared ArrayList in `forEach`) causes race conditions.

5. **Side effects in lambdas** — `peek` with side effects, or modifying the source, causes unpredictable results.

```java
// ❌ Race condition — shared mutable state
List<String> results = new ArrayList<>();
list.parallelStream()
    .map(s -> transform(s))
    .forEach(results::add); // ArrayList is not thread-safe!

// ✅ Use collect instead
List<String> results = list.parallelStream()
    .map(s -> transform(s))
    .toList(); // thread-safe collection
```

---

## 7. I/O — NIO & Channels

**Q78. 🔴 What is the difference between Java I/O (java.io) and NIO (java.nio)?**

| | java.io (Stream I/O) | java.nio (Buffer/Channel I/O) |
|---|---|---|
| Orientation | Stream-oriented (byte by byte) | Buffer-oriented (block of data) |
| Blocking | Blocking (thread waits) | Non-blocking (selector) |
| Streams | One-way (InputStream or OutputStream) | Two-way (Channel can read and write) |
| Best for | Simple, sequential I/O | High-throughput, concurrent I/O |

```java
// java.io — blocking stream
try (InputStream in = new FileInputStream("file.txt")) {
    int byte = in.read(); // blocks until data available
}

// java.nio — buffer + channel
try (FileChannel channel = FileChannel.open(Path.of("file.txt"))) {
    ByteBuffer buffer = ByteBuffer.allocate(1024);
    int bytesRead = channel.read(buffer); // reads a chunk into buffer
    buffer.flip(); // prepare for reading
    while (buffer.hasRemaining()) {
        byte b = buffer.get();
    }
}
```

**NIO.2 (Java 7+)** added `Path`, `Files`, `FileSystem` — modern file API replacing `File`:

```java
// Modern (NIO.2)
List<String> lines = Files.readAllLines(Path.of("file.txt"));
String content = Files.readString(Path.of("file.txt"));
Files.writeString(Path.of("output.txt"), "content");
Files.list(Path.of("/dir")).forEach(System.out::println); // stream directory
```

---

**Q79. 🔴 What is a ByteBuffer? How does it work?**

`ByteBuffer` is a container for a fixed-size block of bytes. It has a position, limit, and capacity.

```
Capacity: total buffer size (fixed)
Limit:    first index that cannot be read/written
Position: current read/write index

  0     Position    Limit          Capacity
  |         |          |               |
  [written data | unwritten space     ]
```

**Key operations:**

```java
ByteBuffer buffer = ByteBuffer.allocate(1024);

// Write mode
buffer.put((byte) 1);
buffer.put((byte) 2);
buffer.put((byte) 3);

// flip() — switch from write to read mode
// Sets limit=position, position=0
buffer.flip();

// Read mode
while (buffer.hasRemaining()) {
    byte b = buffer.get(); // reads and advances position
}

// clear() — resets to write mode (position=0, limit=capacity)
buffer.clear();

// compact() — copies unread data to beginning, positions for more writing
buffer.compact();
```

**Direct vs Heap ByteBuffer:**
- `ByteBuffer.allocate(n)` — heap buffer (GC managed, copies to/from native memory for I/O).
- `ByteBuffer.allocateDirect(n)` — direct buffer (native memory, no copy for I/O, faster for large I/O but expensive to allocate, not GC'd normally).

Use direct buffers for large, long-lived I/O channels (e.g., NIO servers). Use heap buffers for small, short-lived buffers.

---

**Q80. 🟡 What is a Selector in NIO? How does it enable non-blocking I/O?**

A `Selector` allows a single thread to monitor multiple channels for readiness (readable, writable, connectable, acceptable). This is the foundation of non-blocking I/O servers (like Netty's event loop).

```java
Selector selector = Selector.open();
ServerSocketChannel serverChannel = ServerSocketChannel.open();
serverChannel.bind(new InetSocketAddress(8080));
serverChannel.configureBlocking(false); // non-blocking mode
serverChannel.register(selector, SelectionKey.OP_ACCEPT);

while (true) {
    selector.select(); // blocks until at least one channel is ready
    Set<SelectionKey> selectedKeys = selector.selectedKeys();
    for (SelectionKey key : selectedKeys) {
        if (key.isAcceptable()) {
            SocketChannel client = serverChannel.accept();
            client.configureBlocking(false);
            client.register(selector, SelectionKey.OP_READ);
        }
        if (key.isReadable()) {
            SocketChannel client = (SocketChannel) key.channel();
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            int bytesRead = client.read(buffer);
            // process buffer...
        }
    }
    selectedKeys.clear();
}
```

**How it works:** One thread registers multiple channels with a selector. `selector.select()` blocks until at least one channel is ready. The thread processes the ready channels, then loops. This allows a single thread to handle thousands of connections — the "reactor pattern."

**In practice:** You rarely write raw NIO selectors. Use Netty (which wraps NIO with an event loop, codecs, and pipeline) for production non-blocking I/O servers.

---

**Q81. 🟡 What is the difference between `Path` and `File`?**

`File` (java.io, Java 1.0) is the old API. `Path` (java.nio.file, Java 7+) is the modern replacement.

| | File | Path |
|---|------|------|
| Package | java.io | java.nio.file |
| Platform | Filesystem path only | Supports different filesystems (zip, jar) |
| Operations | Limited (exists, delete, list) | Rich (copy, move, walk, watch) |
| Symbolic links | Inconsistent | Proper handling |
| Streams | `listFiles()` returns array | `Files.list()` returns Stream<Path> |

```java
// Old (File)
File file = new File("dir/file.txt");
file.exists();
file.delete();
File[] files = file.listFiles();

// New (Path + Files)
Path path = Path.of("dir/file.txt");
Files.exists(path);
Files.delete(path);
try (Stream<Path> stream = Files.list(Path.of("dir"))) {
    stream.forEach(System.out::println);
}

// Walk file tree (recursive)
try (Stream<Path> walk = Files.walk(Path.of("/root"))) {
    walk.filter(Files::isRegularFile)
        .forEach(System.out::println);
}
```

---

## 8. OOP Concepts

> OOP questions at mid-level are less about definitions and more about design trade-offs. Interviewers want to see that you understand WHY, not just WHAT.

**Q82. 🔴 What is polymorphism? Explain runtime vs compile-time polymorphism.**

**Compile-time polymorphism (static binding):** Method overloading. The compiler decides which method to call based on the method signature (parameter types).

**Runtime polymorphism (dynamic binding):** Method overriding. The JVM decides at runtime which overridden method to call based on the actual object type (not the reference type).

```java
class Animal {
    // Overloaded (compile-time polymorphism)
    void makeSound() { System.out.println("generic sound"); }
    void makeSound(int volume) { System.out.println("loud: " + volume); }
}

class Dog extends Animal {
    // Overridden (runtime polymorphism)
    @Override
    void makeSound() { System.out.println("bark"); }
}

Animal a = new Dog(); // reference type: Animal, object type: Dog
a.makeSound();        // "bark" — runtime polymorphism (dynamic dispatch)
a.makeSound(5);       // compile-time — calls Animal.makeSound(int)
```

**Dynamic dispatch (how runtime polymorphism works):** The JVM looks up the actual object's class in the method table (vtable) and calls the overridden method. The reference type determines which methods are *visible*; the object type determines which implementation *executes*.

---

**Q83. 🔴 What is encapsulation? Why is it important?**

Encapsulation bundles data (fields) and behavior (methods) into a single unit (class) and restricts direct access to the fields via access modifiers (private, protected, public).

```java
public class BankAccount {
    private double balance; // private — cannot be accessed directly

    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("amount must be positive");
        balance += amount;
    }

    public void withdraw(double amount) {
        if (amount > balance) throw new IllegalStateException("insufficient funds");
        balance -= amount;
    }

    public double getBalance() { return balance; } // controlled read access
}
```

**Benefits:**
1. **Data hiding** — prevents external code from setting invalid state (negative balance).
2. **Validation** — setters can enforce invariants before modifying state.
3. **Flexibility** — you can change the internal representation (e.g., balance from double to BigDecimal) without breaking external code — only the getter/setter changes.
4. **Maintainability** — the class controls its own state, making it easier to reason about.

---

**Q84. 🔴 What is the difference between composition and inheritance? When do you use each?**

| | Inheritance (is-a) | Composition (has-a) |
|---|---|---|
| Relationship | Child IS a Parent | Container HAS a Component |
| Coupling | Tight (subclass depends on parent) | Loose (depends on interface) |
| Flexibility | Fixed at compile time | Dynamic (can swap at runtime) |
| Code reuse | Through parent class | Through delegation |
| Java support | `extends` (single class) | Field of another type |

```java
// Inheritance — "is-a"
class SavingsAccount extends BankAccount { }
// Tight coupling: SavingsAccount depends on BankAccount's implementation
// Breaks if BankAccount changes its internal behavior

// Composition — "has-a"
class Portfolio {
    private final List<BankAccount> accounts; // Portfolio HAS-A BankAccount

    public Portfolio(List<BankAccount> accounts) {
        this.accounts = new ArrayList<>(accounts);
    }
}
// Loose coupling: Portfolio depends on BankAccount interface, not implementation
// Can swap accounts at runtime, test with mocks, etc.
```

**Effective Java principle: "Favor composition over inheritance."** Inheritance breaks encapsulation — a subclass depends on its parent's implementation details, which can change. Composition allows you to delegate to an interface, making the design flexible and testable.

**When to use inheritance:** Only when there's a true "is-a" relationship AND the parent class is designed for inheritance (documented, not final, not deeply tied to implementation).

**When to use composition:** Almost always. Use interfaces for behavior contracts, composition for implementation reuse.

---

**Q85. 🟡 What is the difference between abstract classes and interfaces?**

| | Abstract Class | Interface |
|---|----------------|-----------|
| Methods | Abstract + concrete | Abstract + default + static + private (Java 8+) |
| Fields | Instance fields (mutable) | Public static final constants only |
| Constructors | Yes | No |
| Multiple inheritance | No (one class) | Yes (multiple interfaces) |
| Access modifiers | All (private, protected, public) | Public (implicitly) |
| State | Can have state | Cannot have state (no instance fields) |
| `extends` vs `implements` | `extends` (one) | `implements` (many) |

```java
// Abstract class — has state, constructors, shared code
abstract class BankProduct {
    protected double balance; // instance state

    public BankProduct(double initialBalance) { // constructor
        this.balance = initialBalance;
    }

    abstract double calculateInterest(); // must implement

    void deposit(double amount) { balance += amount; } // shared implementation
}

// Interface — pure contract + default methods (Java 8+)
interface InterestBearing {
    double calculateInterest(); // abstract

    default double compoundInterest(double rate, int years) { // default
        return Math.pow(1 + rate, years);
    }

    static double annualRate() { return 0.05; } // static
}

class FixedDeposit extends BankProduct implements InterestBearing {
    public FixedDeposit(double amount) { super(amount); }
    @Override double calculateInterest() { return balance * 0.07; }
}
```

**When to use abstract class:** When you have shared state, constructors, or substantial shared implementation across related types.

**When to use interface:** When you want to define a contract with no state, or when you need multiple inheritance of type. Default methods (Java 8+) allow some shared implementation.

---

**Q86. 🟡 What are default methods in interfaces? What problems do they solve?**

Default methods (Java 8) allow interfaces to have method implementations. They solve the problem of adding methods to existing interfaces without breaking implementing classes.

```java
interface Sortable<T> {
    boolean lessThan(T other);

    default void sort(List<T> list) { // default implementation
        list.sort((a, b) -> a.lessThan(b) ? -1 : 1);
    }
}

// Existing class doesn't need to implement sort()
class Trade implements Sortable<Trade> {
    @Override
    public boolean lessThan(Trade other) { return this.notional < other.notional; }
    // sort() is inherited from the default
}
```

**Diamond problem:** If a class implements two interfaces with the same default method, it must override the method to resolve the conflict:

```java
interface A { default void hello() { System.out.println("A"); } }
interface B { default void hello() { System.out.println("B"); } }

class C implements A, B {
    @Override
    public void hello() {
        A.super.hello(); // explicitly choose A's default
    }
}
```

---

**Q87. 🟡 What is the difference between method overloading and method overriding?**

| | Overloading | Overriding |
|---|-------------|------------|
| Where | Same class | Parent-child classes |
| Method name | Same | Same |
| Parameters | Must differ (type/count) | Must be same |
| Return type | Can differ | Same or covariant |
| Binding | Compile-time (static) | Runtime (dynamic) |
| Access modifier | No restriction | Cannot be more restrictive |
| `@Override` | Optional | Recommended |

```java
class Calculator {
    // Overloading — same name, different parameters
    int add(int a, int b) { return a + b; }
    double add(double a, double b) { return a + b; }
    int add(int a, int b, int c) { return a + b + c; }
}

class ScientificCalculator extends Calculator {
    // Overriding — same signature, different implementation
    @Override
    int add(int a, int b) {
        System.out.println("scientific add");
        return super.add(a, b);
    }
}
```

**Covariant return type:** An overriding method can return a subtype of the parent's return type:

```java
class Animal { Animal clone() { return new Animal(); } }
class Dog extends Animal { @Override Dog clone() { return new Dog(); } }
// Dog is covariant of Animal — allowed
```

---

**Q88. 🔵 What is the Liskov Substitution Principle (LSP)?**

LSP states: "Objects of a subtype should be substitutable for objects of the supertype without breaking the program's correctness." In other words, if `B` extends `A`, you should be able to use `B` anywhere `A` is expected, and the program should behave correctly.

**Violation example:**

```java
class Rectangle {
    protected int width, height;
    public void setWidth(int w) { width = w; }
    public void setHeight(int h) { height = h; }
    public int area() { return width * height; }
}

class Square extends Rectangle {
    @Override public void setWidth(int w) { width = height = w; } // breaks parent's contract
    @Override public void setHeight(int h) { width = height = h; }
}

// LSP violation — using Square where Rectangle is expected breaks logic
void resize(Rectangle r) {
    r.setWidth(5);
    r.setHeight(10);
    assert r.area() == 50; // fails for Square — area = 100!
}
```

**The lesson:** Don't inherit just for code reuse. If a subclass changes the behavior contract of the parent in a way that surprises callers, LSP is violated — prefer composition.

---

**Q89. 🔵 What is the difference between composition, aggregation, and association?**

| Relationship | Strength | Lifecycle | Example |
|-------------|----------|-----------|---------|
| Association | Weakest | Independent | Teacher uses Student (both exist independently) |
| Aggregation | Medium | Independent | Department has Teachers (teachers survive without department) |
| Composition | Strongest | Dependent | House has Rooms (rooms don't exist without house) |

```java
// Association — uses
class Teacher { void teach(Student s) { } } // uses Student temporarily

// Aggregation — has (independent lifecycle)
class Department {
    private List<Teacher> teachers; // teachers exist outside department
    public Department(List<Teacher> teachers) { this.teachers = teachers; }
}

// Composition — owns (dependent lifecycle)
class House {
    private final List<Room> rooms; // rooms are created with house, die with house
    public House() {
        this.rooms = List.of(new Room("living"), new Room("bedroom"));
    }
}
```

**Composition (UML: filled diamond):** The contained object is created and destroyed with the container. If House is destroyed, Rooms are destroyed.

**Aggregation (UML: hollow diamond):** The contained object is passed in and exists independently. If Department is destroyed, Teachers continue to exist.

---

## 9. Quick Reference Tables

### Collection Interface Hierarchy

```
Collection
├── List (ordered, allows duplicates)
│   ├── ArrayList      (array, O(1) random access)
│   ├── LinkedList     (doubly-linked, O(1) ends)
│   └── Vector         (synchronized ArrayList — legacy)
├── Set (no duplicates)
│   ├── HashSet        (HashMap backed, O(1), unordered)
│   ├── LinkedHashSet  (insertion order, O(1))
│   └── TreeSet        (Red-Black Tree, O(log n), sorted)
├── Queue (FIFO)
│   ├── PriorityQueue  (min-heap, O(log n) offer/poll)
│   ├── ArrayDeque     (resizable array, O(1) ends)
│   └── LinkedList     (also a Deque)
└── Deque (double-ended)
    ├── ArrayDeque     (preferred)
    └── LinkedList

Map (key-value, NOT a Collection)
├── HashMap            (O(1), unordered, one null key)
├── LinkedHashMap      (insertion/access order)
├── TreeMap            (Red-Black Tree, O(log n), sorted)
├── Hashtable         (synchronized, legacy — avoid)
└── ConcurrentHashMap  (thread-safe, per-bucket lock)
```

### Concurrent Collections Quick Reference

| Need | Use |
|------|-----|
| Thread-safe Map | `ConcurrentHashMap` |
| Thread-safe List (read-heavy) | `CopyOnWriteArrayList` |
| Thread-safe Set (read-heavy) | `CopyOnWriteArraySet` |
| Thread-safe Queue | `ConcurrentLinkedQueue` |
| Thread-safe Blocking Queue | `ArrayBlockingQueue`, `LinkedBlockingQueue` |
| Thread-safe Priority Queue | `PriorityBlockingQueue` |
| Thread-safe Deque | `ConcurrentLinkedDeque` |
| Thread-safe Sorted Map | `ConcurrentSkipListMap` |
| Thread-safe Sorted Set | `ConcurrentSkipListSet` |

### Thread State Diagram

```
                 start()
   NEW ──────────────────► RUNNABLE
                            │
                  ┌─────────┼─────────┐
                  │         │         │
              wait()    sleep()/    I/O complete
                  │    join()
                  ▼         │         │
              WAITING       │         │
                  │     notify()      │
                  ▼         │         │
              BLOCKED ◄─────┘         │
              (waiting for lock)       │
                  │                   │
              lock acquired            │
                  │                   │
                  ▼                   │
              RUNNABLE ◄───────────────┘
                  │
              run() returns
                  ▼
              TERMINATED
```

### JVM Tuning Cheat Sheet

| Scenario | Recommended GC | Key Flags |
|----------|---------------|----------|
| General server app (4-64 GB heap) | G1 GC (default) | `-Xms4g -Xmx4g -XX:MaxGCPauseMillis=200` |
| Low-latency trading (16+ GB heap) | ZGC | `-XX:+UseZGC -XX:ZGenerational=true` |
| High throughput, batch | Parallel GC | `-XX:+UseParallelGC -XX:ParallelGCThreads=4` |
| Small heap (< 4 GB) | Serial GC | `-XX:+UseSerialGC` |
| OOM debugging | Any | `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/dumps` |

### Common Exception Quick Reference

| Exception | Type | Cause |
|-----------|------|-------|
| `NullPointerException` | Unchecked | Dereferencing null |
| `ArrayIndexOutOfBoundsException` | Unchecked | Invalid array index |
| `ClassCastException` | Unchecked | Invalid cast |
| `IllegalArgumentException` | Unchecked | Invalid method argument |
| `IllegalStateException` | Unchecked | Object in wrong state |
| `ArithmeticException` | Unchecked | Math error (division by zero) |
| `ConcurrentModificationException` | Unchecked | Concurrent modification during iteration |
| `NumberFormatException` | Unchecked | Invalid string → number conversion |
| `IOException` | Checked | I/O failure (file, network) |
| `SQLException` | Checked | Database error |
| `ClassNotFoundException` | Checked | Class not found (dynamic loading) |
| `InterruptedException` | Checked | Thread interrupted while waiting |
| `StackOverflowError` | Error | Deep recursion (stack exhausted) |
| `OutOfMemoryError` | Error | Heap/metaspace exhausted |

---

## Study Priority Matrix

| Priority | Topic | Why |
|----------|-------|-----|
| 🔴 Week 1 | HashMap internals, ConcurrentHashMap, ArrayList vs LinkedList | Asked in nearly every interview round |
| 🔴 Week 1 | Thread pools, synchronized vs Lock, volatile | BFSI core competency |
| 🔴 Week 1 | CompletableFuture, virtual threads | Modern Java — differentiates you |
| 🔴 Week 2 | JVM memory model, G1/ZGC, classloading | Depth check — shows seniority |
| 🔴 Week 2 | try-with-resources, checked vs unchecked | Fundamental, always asked |
| 🟡 Week 2 | TreeMap, Generics wildcards, Streams collect/grouping | Shows breadth |
| 🟡 Week 2 | Deadlock detection, atomic/CAS, BlockingQueue | Concurrency depth |
| 🟡 Week 3 | NIO ByteBuffer, Selector | Less common but shows I/O depth |
| 🟡 Week 3 | Composition vs inheritance, LSP, abstract vs interface | OOP design maturity |
| 🔵 Week 3 | StampedLock, ForkJoinPool work-stealing, Escape analysis | Top 10% differentiator |
| 🔵 Week 3 | JIT C1/C2, String pool, ABA problem | Deep JVM knowledge |

---

> **Final tip:** Practice explaining answers aloud. Interviewers don't just want the right answer — they want clear communication, the ability to draw diagrams (HashMap buckets, thread states, GC generations), and to explain trade-offs (when to use X vs Y). For BFSI GCCs specifically, relate concurrency and JVM answers to banking scenarios: "In BaNCS, we use a thread pool for trade matching where..." or "For our market data service, G1 GC gave us predictable pauses..."

---

*Generated for Ramish Taha's career switch preparation. Target: BFSI GCCs and product companies, 14-18 LPA CTC. Pair with Spring Boot interview bank for full coverage.*
