# ☕ Core Java Interview Question Bank — Ramish

> **Target:** Mid-level Java developer (3-4 yrs) at product companies & BFSI GCCs, 14-18 LPA
> **Context:** TCS System Engineer, Spring Boot/Java, BaNCS banking systems
> **Usage:** Review 2-3 topics per day over Weeks 7-10. Mark each section as you review.

---

## Legend
- **🔴 MUST KNOW** — Asked in nearly every mid/senior interview
- **🟡 IMPORTANT** — Asked often, be ready
- **🟢 NICE TO HAVE** — Differentiates you from other candidates

---

## Table of Contents
1. [Collections Framework](#1-collections-framework)
2. [Concurrency & Multithreading](#2-concurrency--multithreading)
3. [JVM Internals](#3-jvm-internals)
4. [Exceptions](#4-exceptions)
5. [Generics](#5-generics)
6. [Streams API](#6-streams-api)
7. [I/O (NIO, Channels)](#7-io-nio-channels)
8. [OOP Concepts](#8-oop-concepts)

---

## 1. Collections Framework

### 🔴 HashMap Internals
**Q: How does HashMap work internally in Java?**
- HashMap uses an array of buckets (table), indexed by hash
- `hashCode()` → hash → index calculation: `index = (n-1) & hash`
- If collision: entries stored as a linked list at that bucket
- Java 8+: if a bucket's linked list exceeds 8 elements (TREEIFY_THRESHOLD), it converts to a red-black tree
- When tree size drops below 6 (UNTREEIFY_THRESHOLD), it reverts to linked list
- Default capacity: 16, load factor: 0.75, resize at capacity × load factor
- Resize doubles capacity and rehashes all entries

**Q: What happens when you put a key-value pair in HashMap?**
1. Compute key's `hashCode()`
2. Apply hash function: `(h = key.hashCode()) ^ (h >>> 16)` — spreads bits to reduce collisions
3. Calculate bucket index: `(n-1) & hash`
4. If bucket empty → create new node
5. If bucket not empty → check each node:
   - If `key.equals(node.key)` → replace value
   - If not found → append to linked list (or tree)
6. After insertion, if size > threshold → resize

**Q: Why did Java 8 introduce treeification in HashMap?**
- Prevents O(n) worst-case performance from hash collisions (attacker can craft keys with same hash)
- Reduces worst case from O(n) to O(log n) for get/put/remove
- This is a security improvement too — hash collision DoS attacks

### 🔴 ConcurrentHashMap
**Q: How does ConcurrentHashMap work in Java 8+?**
- Java 7: segment-based locking (Segment[]) — 16 segments by default, each is a mini HashMap with its own lock
- Java 8+: CAS (Compare-And-Swap) + synchronized on the first node of each bucket
  - `put()`: CAS to insert into empty bucket; synchronized to update existing bucket chain
  - `get()`: no locking — volatile reads ensure visibility
- More granular locking than Java 7 — less contention
- Still thread-safe, but allows concurrent reads and limited concurrent writes

**Q: HashMap vs ConcurrentHashMap vs Hashtable?**
| Feature | HashMap | ConcurrentHashMap | Hashtable |
|---------|---------|-------------------|-----------|
| Thread-safe | No | Yes | Yes |
| Null keys | 1 allowed | Not allowed | Not allowed |
| Null values | Multiple | Not allowed | Not allowed |
| Locking | None | CAS + bucket-level | Full table |
| Performance | Fastest | Fast (concurrent) | Slow (full lock) |
| Fail-fast iterator | Yes | No (weakly consistent) | Yes |

### 🟡 ArrayList vs LinkedList
**Q: When would you use ArrayList vs LinkedList?**
| Operation | ArrayList | LinkedList |
|-----------|-----------|-----------|
| get(index) | O(1) | O(n) |
| add(e) at end | O(1) amortized | O(1) |
| add(index, e) | O(n) | O(n) (traversal) |
| remove(index) | O(n) | O(n) (traversal) |
| Memory | Less (contiguous array) | More (node objects + pointers) |
| Cache locality | Good | Poor |

**Use ArrayList almost always.** LinkedList only wins for frequent head/tail insertions and deletions — which is rare. Most "I need a linked list" cases are better served by `ArrayDeque`.

### 🟡 TreeMap
**Q: How does TreeMap work?**
- Uses a Red-Black Tree (self-balancing BST)
- Keys must be `Comparable` or a `Comparator` must be provided
- Operations (get, put, remove, containsKey): O(log n)
- Maintains sorted order — iterate in sorted key order
- Not thread-safe — use `Collections.synchronizedSortedMap()` or `ConcurrentSkipListMap` for concurrency

### 🟡 fail-fast vs fail-safe iterators
- **Fail-fast:** Throws `ConcurrentModificationException` if collection modified during iteration (HashMap, ArrayList). Uses a `modCount` field checked on each `next()`.
- **Fail-safe:** Works on a copy of the collection (CopyOnWriteArrayList), or uses weakly consistent reads (ConcurrentHashMap). No exception, but may not reflect latest modifications.

### 🔴 equals() and hashCode() contract
**Q: What's the contract between equals() and hashCode()?**
1. If `a.equals(b)` is true, then `a.hashCode() == b.hashCode()` must be true
2. If `a.equals(b)` is false, `hashCode()` may or may not be equal
3. If `hashCode(a) != hashCode(b)`, then `a.equals(b)` must be false
4. Consistency: multiple calls of hashCode() on the same object must return the same value (unless fields change)
5. If you override `equals()`, you MUST override `hashCode()`

**Consequence of violating:** HashMap/HashSet will behave incorrectly — objects that are "equal" end up in different buckets.

---

## 2. Concurrency & Multithreading

### 🔴 Thread Lifecycle
**Q: What are the states of a Thread in Java?**
1. **NEW** — created but not started (`new Thread()`)
2. **RUNNABLE** — `start()` called, executing or ready to run
3. **BLOCKED** — waiting for a monitor lock (synchronized block)
4. **WAITING** — `wait()`, `join()`, `LockSupport.park()` without timeout
5. **TIMED_WAITING** — `sleep(ms)`, `wait(ms)`, `join(ms)`, `parkNanos(ns)`
6. **TERMINATED** — run() method completed

### 🔴 synchronized vs Lock
**Q: Difference between synchronized and ReentrantLock?**
| Feature | synchronized | ReentrantLock |
|---------|--------------|---------------|
| Fairness | No | Can be fair (FIFO) |
| Try-lock | No | `tryLock()` with timeout |
| Interruptible | No | `lockInterruptibly()` |
| Condition variables | 1 (wait/notify) | Multiple `Condition` objects |
| Explicit unlock | No (auto-release) | Must call `unlock()` in finally |
| Read-write separation | No | `ReentrantReadWriteLock` |

```java
// ReentrantLock pattern
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    // critical section
} finally {
    lock.unlock(); // ALWAYS in finally
}
```

### 🔴 volatile keyword
**Q: What does volatile do?**
- Guarantees **visibility**: writes by one thread are immediately visible to other threads
- Prevents instruction reordering by the compiler/CPU (acts as a memory barrier)
- Does NOT guarantee atomicity for compound operations (e.g., `count++` is NOT thread-safe even if volatile)
- Use cases: flags (`boolean running`), single-variable reads/writes, double-checked locking pattern
- Alternative: `AtomicInteger`, `AtomicBoolean` for atomic compound operations

### 🔴 CompletableFuture
**Q: How does CompletableFuture work?**
- Asynchronous computation that can be chained, combined, and composed
- Non-blocking — uses ForkJoinPool.commonPool() by default
- Key methods:
  - `supplyAsync(Supplier)` — run async, return a value
  - `thenApply(Function)` — transform result
  - `thenCompose(Function)` — chain another async (flatMap)
  - `thenCombine(OtherFuture, BiFunction)` — combine two futures
  - `allOf(futures)` — wait for all
  - `anyOf(futures)` — wait for first
  - `exceptionally(Function)` — handle errors
  - `whenComplete(BiConsumer)` — side effects on completion

```java
CompletableFuture<String> future = CompletableFuture
    .supplyAsync(() -> fetchDataFromDB())
    .thenApply(data -> data.toUpperCase())
    .thenCompose(upper -> CompletableFuture.supplyAsync(() -> enrich(upper)))
    .exceptionally(ex -> "Fallback: " + ex.getMessage());
```

### 🔴 ExecutorService vs ForkJoinPool
**Q: Difference between ExecutorService and ForkJoinPool?**
| Feature | ExecutorService | ForkJoinPool |
|---------|----------------|--------------|
| Task model | Runnable/Callable | ForkJoinTask (RecursiveAction/RecursiveTask) |
| Work stealing | No | Yes — idle threads steal from other threads' queues |
| Best for | Independent tasks | Divide-and-conquer, recursive tasks |
| Parallelism | Fixed thread pool | Work-stealing with target parallelism |
| Default pool | ThreadPoolExecutor | ForkJoinPool.commonPool() (used by parallel streams) |

### 🟡 Virtual Threads (Java 21)
**Q: What are virtual threads and when should you use them?**
- Lightweight threads managed by JVM, not OS
- Millions of virtual threads can run on a few platform threads
- Created via `Thread.startVirtualThread(Runnable)` or `Executors.newVirtualThreadPerTaskExecutor()`
- Ideal for I/O-bound work (HTTP calls, DB queries) — not CPU-bound
- No need for thread pooling — create per task
- Pinning concern: `synchronized` blocks can pin virtual threads to platform threads (use `ReentrantLock` instead)
- Spring Boot 3.2+ supports virtual threads natively

```java
// Before (platform thread, limited by thread pool size)
ExecutorService pool = Executors.newFixedThreadPool(200);

// After (virtual threads, millions of concurrent tasks)
ExecutorService vpool = Executors.newVirtualThreadPerTaskExecutor();
```

### 🟡 Thread Pool Sizing
**Q: How do you size a thread pool?**
- CPU-bound: `threads = CPU cores + 1` (or `N * CPU utilization target * (1 + W/C)` where W = wait time, C = compute time)
- I/O-bound: `threads = CPU cores * (1 + wait_time / compute_time)` — typically much higher
- Use `Runtime.getRuntime().availableProcessors()` to detect cores
- Too many threads → context switching overhead, memory pressure
- Too few threads → underutilized CPU, longer queue times

### 🟢 Deadlock Detection and Prevention
**Q: How do you prevent deadlocks?**
1. **Lock ordering** — always acquire locks in the same order
2. **Try-lock with timeout** — `tryLock(timeout)` instead of `lock()`
3. **Avoid nested locks** — minimize lock scope
4. **Use higher-level concurrency utilities** — `CountDownLatch`, `Semaphore`, `CompletableFuture` instead of raw locks
5. **Deadlock detection:** `jstack` or `ThreadMXBean.findDeadlockedThreads()`

---

## 3. JVM Internals

### 🔴 JVM Memory Model
**Q: What are the JVM memory areas?**
| Area | Stores | Thread-shared? |
|------|--------|----------------|
| Heap | Object instances, arrays | Yes |
| Metaspace (was PermGen) | Class metadata, static fields | Yes |
| Stack | Method frames, local variables, operand stack | No (per thread) |
| PC Register | Current instruction address | No (per thread) |
| Native Method Stack | Native method calls | No (per thread) |
| Direct Memory | NIO buffers, off-heap | Yes |

### 🔴 Garbage Collection
**Q: Explain garbage collection in Java.**
- JVM identifies garbage via **reachability** — objects not reachable from GC roots are eligible for collection
- GC roots: local variables in active frames, static fields, JNI references
- Generational hypothesis: most objects die young → separate young/old generations
  - **Young Gen:** Eden + 2 Survivor spaces (S0, S1) — minor GC
  - **Old Gen:** long-lived objects — major GC (slower, full STW)

**Q: G1 GC vs ZGC — when to use which?**
| Feature | G1 GC | ZGC |
|---------|-------|-----|
| Max pause | ~200ms | <10ms (sub-millisecond in Java 21) |
| Heap size | 4GB-64GB | 8GB-16TB |
| Region-based | Yes (equal regions) | Yes (dynamic) |
| Colored pointers | No | Yes |
| Best for | General purpose, moderate heaps | Low-latency, large heaps |
| Default since | Java 9 | No (experimental → stable Java 21) |

### 🟡 Classloading
**Q: Explain Java class loading.**
- **Loading:** Find and load `.class` file into memory
- **Linking:** Verify bytecode, prepare static fields (default values), resolve references
- **Initialization:** Run static initializers and static blocks
- **Classloader hierarchy (parent delegation):**
  1. Bootstrap ClassLoader → core Java classes (java.*, javax.*)
  2. Extension/Platform ClassLoader → `java.ext.dirs` or modules
  3. Application ClassLoader → classpath, your code
  4. Custom ClassLoaders → plugin systems, app servers
- **Parent-first delegation:** child asks parent first, preventing untrusted code from replacing core classes

### 🟡 Memory Leaks in Java
**Q: How do you detect and diagnose a memory leak?**
- **Symptoms:** `OutOfMemoryError`, growing heap usage, increasing GC frequency
- **Detection:**
  1. JVM flags: `-XX:+HeapDumpOnOutOfMemoryError` generates a heap dump on OOM
  2. `jmap -dump:format=b,file=heap.hprof <pid>` — manual heap dump
  3. Analyze with VisualVM, Eclipse MAT, or JConsole
  4. Look for: large collections growing, unclosed resources, static references holding objects, ThreadLocal not cleared
- **Common causes:**
  - Static collections that never get cleared
  - Unclosed resources (InputStream, Connection)
  - `ThreadLocal` not removed after use
  - Listener/callbacks not deregistered
  - Inner class holding implicit reference to outer class

### 🟡 jstack and Thread Dumps
**Q: How would you diagnose a hung Java application?**
1. `jps` — find the Java process ID
2. `jstack <pid>` — get a thread dump
3. Look for threads in BLOCKED or WAITING state
4. Check for deadlocks: `jstack` reports "Found one Java-level deadlock"
5. `jcmd <pid> Thread.print` — alternative
6. `top -H -p <pid>` — see which threads consume CPU

---

## 4. Exceptions

### 🔴 Checked vs Unchecked Exceptions
**Q: Difference between checked and unchecked exceptions?**
| Feature | Checked | Unchecked |
|---------|---------|-----------|
| Subclass of | Exception (not RuntimeException) | RuntimeException |
| Compiler check | Must catch or declare (throws) | No compile-time check |
| Examples | IOException, SQLException, ClassNotFoundException | NullPointerException, IllegalArgumentException, ArrayIndexOutOfBoundsException |
| Philosophy | Recoverable conditions | Programming errors |
| Best practice | Catch only if you can recover | Don't catch — fix the code |

### 🟡 Custom Exceptions
```java
public class InsufficientFundsException extends RuntimeException {
    private final double amount;
    private final double balance;

    public InsufficientFundsException(double amount, double balance) {
        super(String.format("Withdrawal of %.2f exceeds balance of %.2f", amount, balance));
        this.amount = amount;
        this.balance = balance;
    }

    public double getAmount() { return amount; }
    public double getBalance() { return balance; }
}
```

### 🟡 try-with-resources
**Q: How does try-with-resources work?**
- Auto-closes resources that implement `AutoCloseable` (or `Closeable`)
- Closes in reverse order of declaration
- Suppressed exceptions attached via `addSuppressed()`
- Eliminates boilerplate finally blocks

```java
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql);
     ResultSet rs = ps.executeQuery()) {
    // use resources
} // conn, ps, rs auto-closed even on exception
```

---

## 5. Generics

### 🟡 Type Erasure
**Q: What is type erasure in Java generics?**
- Generics are a compile-time feature — type parameters are erased at runtime
- `List<String>` and `List<Integer>` are both `List` at runtime
- Compiler inserts casts at call sites
- You CANNOT do: `new T()`, `T.class`, `instanceof T`, `new T[]`
- Runtime: `List<String>.getClass() == List<Integer>.getClass()` → true

### 🟡 Bounded Type Parameters
```java
// Upper bound (covariant)
public <T extends Number> double sum(List<T> numbers) {
    return numbers.stream().mapToDouble(Number::doubleValue).sum();
}

// Wildcards
// PECS: Producer extends, Consumer super
public void process(List<? extends Number> producer, List<? super Number> consumer) {
    Number n = producer.get(0); // OK — reading
    consumer.add(n);             // OK — writing
}
```

### 🟢 Type Erasure Problems
**Q: What problems does type erasure cause?**
- Cannot create generic arrays: `new T[]` — array store check fails at runtime
- Cannot overload methods with same erasure: `void m(List<String>)` and `void m(List<Integer>)` — compile error
- Runtime type checks require Class: `if (item instanceof T)` doesn't work; use `Class<T>` parameter

---

## 6. Streams API

### 🔴 Stream Operations
**Q: Explain intermediate vs terminal operations.**
| Type | Lazy? | Examples |
|------|-------|---------|
| Intermediate | Yes | `filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, `skip`, `peek` |
| Terminal | N/A (consumes) | `collect`, `forEach`, `reduce`, `count`, `min`, `max`, `anyMatch`, `findFirst` |

- Intermediate operations are lazy — nothing executes until a terminal operation is called
- Streams can be consumed only once

```java
List<String> result = employees.stream()
    .filter(e -> e.getSalary() > 50000)
    .map(Employee::getName)
    .sorted()
    .collect(Collectors.toList());
```

### 🟡 collect(Collectors)
**Q: What Collectors do you know?**
```java
// Group by department
Map<Dept, List<Employee>> byDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDept));

// Group and count
Map<Dept, Long> countByDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDept, Collectors.counting()));

// Partition
Map<Boolean, List<Employee>> partition = employees.stream()
    .collect(Collectors.partitioningBy(e -> e.getSalary() > 50000));

// Join strings
String names = employees.stream()
    .map(Employee::getName)
    .collect(Collectors.joining(", "));

// Average salary per department
Map<Dept, Double> avgSalary = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDept, Collectors.averagingDouble(Employee::getSalary)));
```

### 🟡 Stream Parallelism
**Q: When should you use parallel streams?**
- Use for CPU-intensive operations on large datasets (>10,000 elements)
- Uses ForkJoinPool.commonPool() — shared across all parallel streams in the JVM
- Do NOT use for:
  - Small datasets (overhead > savings)
  - I/O-bound tasks (blocks common pool threads)
  - Operations with side effects or ordering requirements
  - Short-circuiting with `limit()` (performance worse)

---

## 7. I/O (NIO, Channels)

### 🟡 NIO vs IO
**Q: What's the difference between Java IO and NIO?**
| Feature | Java IO | Java NIO |
|---------|---------|----------|
| Paradigm | Stream-oriented (one byte at a time) | Buffer-oriented (block of data) |
| Blocking | Blocking (thread waits) | Supports non-blocking (Selector) |
| Channels | No | Yes (FileChannel, SocketChannel) |
| Best for | Simple, small data | High-throughput, scalable I/O |

### 🟢 ByteBuffer
**Q: How does ByteBuffer work?**
- Fixed-size buffer with position, limit, and capacity markers
- `put()` writes at position, `get()` reads at position
- `flip()` switches from write to read mode (sets limit=position, position=0)
- `clear()` resets for writing (position=0, limit=capacity)
- `compact()` moves unread data to beginning, prepares for more writes

```java
ByteBuffer buffer = ByteBuffer.allocate(1024);
buffer.put(data);
buffer.flip(); // switch to read
while (buffer.hasRemaining()) {
    byte b = buffer.get();
}
buffer.clear(); // ready for more writes
```

---

## 8. OOP Concepts

### 🔴 Polymorphism
**Q: Explain polymorphism in Java.**
- **Compile-time (static):** Method overloading — same name, different parameters. Resolved at compile time.
- **Runtime (dynamic):** Method overriding — subclass redefines parent method. Resolved at runtime via virtual method dispatch.
- JVM uses vtable (virtual method table) — each class has a table mapping method names to code addresses.
- `@Override` annotation ensures the method actually overrides (compile-time check).

### 🔴 Abstract Class vs Interface (Java 8+)
**Q: What's the difference between abstract class and interface in modern Java?**
| Feature | Abstract Class | Interface |
|---------|----------------|-----------|
| Multiple inheritance | No (single) | Yes (multiple) |
| Fields | Instance fields, any access modifier | Only `public static final` constants |
| Constructors | Yes | No |
| Methods | Any visibility | `public` (default), `private` (Java 9+), `static`, `default` (Java 8+) |
| State | Can have state | No state (except constants) |
| Use case | Share code + state | Define contract |

**When to use which:** Use interface for pure contract (behavior). Use abstract class when you have shared state or partial implementation.

### 🟡 Composition vs Inheritance
**Q: Why favor composition over inheritance?**
- Inheritance creates tight coupling — changes to parent break children
- Inheritance is static (decided at compile time) — composition can change at runtime
- Inheritance breaks encapsulation — subclass depends on parent implementation details
- Composition: `class Car { private Engine engine; }` — delegate, don't inherit
- "Is-A" → inheritance. "Has-A" → composition. But even "is-a" can often be modeled as composition.

### 🟡 Encapsulation
**Q: Why is encapsulation important?**
- Hides internal state, exposes controlled access via methods
- Prevents invalid state — invariants checked in setters
- Enables internal changes without breaking clients
- Use: `private` fields, `public` getters/setters (or no setters for immutability)

```java
public class BankAccount {
    private double balance;

    public void withdraw(double amount) {
        if (amount > balance) throw new InsufficientFundsException(amount, balance);
        if (amount <= 0) throw new IllegalArgumentException("Amount must be positive");
        this.balance -= amount;
    }
    // balance can only change through controlled methods
}
```

---

## Self-Assessment Checklist
- [ ] I can explain HashMap internals (buckets, linked list, treeification)
- [ ] I can explain ConcurrentHashMap locking (CAS + bucket-level)
- [ ] I can compare synchronized vs ReentrantLock
- [ ] I can explain volatile and when it's NOT enough
- [ ] I can write CompletableFuture chains (thenApply, thenCompose, exceptionally)
- [ ] I can explain virtual threads and when to use them
- [ ] I can explain JVM memory areas (heap, metaspace, stack)
- [ ] I can compare G1 GC vs ZGC
- [ ] I can explain classloader parent delegation
- [ ] I know how to take a heap dump and thread dump
- [ ] I can explain checked vs unchecked exceptions
- [ ] I understand type erasure and its limitations
- [ ] I can write complex stream pipelines with groupingBy
- [ ] I can explain composition vs inheritance and when to use each
