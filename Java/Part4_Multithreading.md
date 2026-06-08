# Part 6: Java Multithreading & Concurrency — Complete Mastery Guide
### From Thread Lifecycle to CompletableFuture | JVM Internals | Backend SDE Interview Handbook

---

> **How to use this document:** Every topic follows: Theory → Internal Working → Code → Common Mistakes → Interview Questions. Read sequentially for full depth.

---

# Table of Contents

1. [Processes vs Threads](#1-processes-vs-threads)
2. [Java Thread Lifecycle](#2-java-thread-lifecycle)
3. [Creating Threads: All Four Ways](#3-creating-threads-all-four-ways)
4. [Synchronization & Intrinsic Locks](#4-synchronization--intrinsic-locks)
5. [The volatile Keyword](#5-the-volatile-keyword)
6. [Reentrant Locks & Conditions](#6-reentrant-locks--conditions)
7. [Deadlock, Starvation, Livelock](#7-deadlock-starvation-livelock)
8. [Atomic Classes](#8-atomic-classes)
9. [Thread Pools & Executors Framework](#9-thread-pools--executors-framework)
10. [Callable, Future, and CompletableFuture](#10-callable-future-and-completablefuture)
11. [Fork/Join Pool](#11-forkjoin-pool)
12. [Concurrent Collections](#12-concurrent-collections)
13. [Java Memory Model & Happens-Before](#13-java-memory-model--happens-before)
14. [Producer-Consumer Pattern](#14-producer-consumer-pattern)
15. [Common Concurrency Patterns](#15-common-concurrency-patterns)
16. [Interview Quick Reference](#16-interview-quick-reference)

---

# 1. Processes vs Threads

## Theory

A **process** is an independent program in execution — it has its own memory space (heap, stack, code, data segments), file handles, and OS resources. Processes are isolated from each other; one crashing doesn't kill another.

A **thread** is the smallest unit of execution *within* a process. Multiple threads share the same process memory (heap, code, static data) but each has its own stack and program counter.

```
Process (JVM instance)
┌──────────────────────────────────────────────────────────────┐
│                      SHARED MEMORY                          │
│   Heap: all objects, class instances                        │
│   Metaspace: class metadata, static fields                  │
│   Code: compiled bytecode / JIT native code                 │
│                                                             │
│  Thread 1          Thread 2          Thread 3              │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐          │
│  │ Stack    │      │ Stack    │      │ Stack    │          │
│  │ PC Reg   │      │ PC Reg   │      │ PC Reg   │          │
│  │ (private)│      │ (private)│      │ (private)│          │
│  └──────────┘      └──────────┘      └──────────┘          │
└──────────────────────────────────────────────────────────────┘
```

## Why Threads?

- **Concurrency:** Do multiple things at once (handle multiple HTTP requests simultaneously)
- **Parallelism:** Use multiple CPU cores for computation (parallel sort, map-reduce)
- **Responsiveness:** Keep UI thread alive while background work happens
- **Resource sharing:** Threads share memory — cheaper than inter-process communication

## Thread vs Process

| Aspect | Process | Thread |
|--------|---------|--------|
| Memory | Own private address space | Shared with other threads in process |
| Creation cost | High (fork, allocate memory) | Low (just a stack + registers) |
| Communication | IPC (pipes, sockets, shared memory) | Direct — shared heap variables |
| Crash isolation | Crash doesn't affect other processes | Crash can kill entire process |
| Context switch | Expensive (MMU TLB flush) | Cheaper (same address space) |
| Example | Two JVM instances | Multiple request handler threads in Spring |

---

# 2. Java Thread Lifecycle

## The Six States

```java
public enum Thread.State {
    NEW,           // Thread object created, start() not yet called
    RUNNABLE,      // Running or ready to run (waiting for CPU)
    BLOCKED,       // Waiting to acquire a monitor lock (synchronized block)
    WAITING,       // Waiting indefinitely (wait(), join(), park())
    TIMED_WAITING, // Waiting with timeout (sleep(), wait(ms), join(ms))
    TERMINATED     // run() method completed or threw uncaught exception
}
```

## State Transition Diagram

```
                        start()
     NEW ─────────────────────────────► RUNNABLE
                                        │    ▲
                   synchronized block   │    │ lock acquired
                   (lock unavailable)   ▼    │
                              BLOCKED ──┘
                                        │
              wait() / join() / park()  │
                                        ▼
                               WAITING ─┐
                                        │ notify() / notifyAll()
                                        │ join target finishes
                                        │ unpark()
                                        ▼
         sleep(ms) / wait(ms)   TIMED_WAITING
                                        │
                                        │ timeout expires / interrupt()
                                        ▼
                                   RUNNABLE
                                        │
                     run() completes    │
                     or exception       ▼
                                  TERMINATED
```

## Key State Transitions

```java
// NEW → RUNNABLE
Thread t = new Thread(() -> System.out.println("running"));
// t is NEW
t.start();
// t is RUNNABLE

// RUNNABLE → TIMED_WAITING
Thread.sleep(1000);  // current thread sleeps 1 second

// RUNNABLE → WAITING
Object lock = new Object();
synchronized (lock) {
    lock.wait();       // releases lock, enters WAITING
    // re-acquires lock when notified
}

// RUNNABLE → BLOCKED
synchronized (sharedObject) {  // if another thread holds this lock → BLOCKED
    // do work
}

// WAITING → RUNNABLE (via notification)
synchronized (lock) {
    lock.notify();     // wake one thread in WAITING on this object
    lock.notifyAll();  // wake all threads in WAITING on this object
}
```

## Thread Priority

```java
Thread t = new Thread(() -> { });
t.setPriority(Thread.MIN_PRIORITY);   // 1
t.setPriority(Thread.NORM_PRIORITY);  // 5 (default)
t.setPriority(Thread.MAX_PRIORITY);   // 10

// Priority is a HINT to the scheduler, not a guarantee
// OS thread schedulers may ignore it entirely
```

## Daemon Threads

```java
Thread daemon = new Thread(() -> {
    while (true) { /* background cleanup */ }
});
daemon.setDaemon(true);   // MUST be set before start()
daemon.start();

// JVM exits when ALL non-daemon threads finish
// Daemon threads are killed automatically when JVM exits
// Use for: GC, background monitoring, cleanup tasks
```

---

# 3. Creating Threads: All Four Ways

## Way 1: Extend Thread

```java
class MyThread extends Thread {
    private String taskName;

    MyThread(String taskName) {
        this.taskName = taskName;
    }

    @Override
    public void run() {
        System.out.println(taskName + " running on: " + Thread.currentThread().getName());
    }
}

// Usage:
MyThread t1 = new MyThread("Task-A");
MyThread t2 = new MyThread("Task-B");
t1.start();   // creates new OS thread and calls run()
t2.start();

// t1.run();  // WRONG — runs in current thread, no new thread created!
```

**Downside:** Java only allows single class inheritance. If your class already extends something, you can't extend Thread.

## Way 2: Implement Runnable

```java
class MyTask implements Runnable {
    private String name;

    MyTask(String name) { this.name = name; }

    @Override
    public void run() {
        System.out.println(name + " running on: " + Thread.currentThread().getName());
    }
}

// Usage:
Thread t1 = new Thread(new MyTask("Task-A"));
Thread t2 = new Thread(new MyTask("Task-B"));
t1.start();
t2.start();

// Lambda (since Runnable is a functional interface):
Thread t3 = new Thread(() -> System.out.println("Lambda task"));
t3.start();
```

**Preferred over extending Thread** — separates the task from the thread mechanism, allows reuse with ExecutorService.

## Way 3: Implement Callable (returns a result)

```java
import java.util.concurrent.*;

class ComputeTask implements Callable<Integer> {
    private int n;

    ComputeTask(int n) { this.n = n; }

    @Override
    public Integer call() throws Exception {
        // Unlike run(), call() can return a value AND throw checked exceptions
        int result = 0;
        for (int i = 1; i <= n; i++) result += i;
        return result;
    }
}

// Usage with ExecutorService:
ExecutorService executor = Executors.newSingleThreadExecutor();
Future<Integer> future = executor.submit(new ComputeTask(100));

// Do other work here while ComputeTask runs in parallel...

Integer result = future.get();   // blocks until result is ready
System.out.println("Sum = " + result);  // 5050
executor.shutdown();
```

**Key difference from Runnable:** `call()` can return a value and throw checked exceptions. `run()` returns void and can't throw checked exceptions.

## Way 4: ExecutorService + Thread Pools (Production Approach)

```java
// Never create raw threads in production — use thread pools
ExecutorService pool = Executors.newFixedThreadPool(4);

for (int i = 0; i < 10; i++) {
    final int taskId = i;
    pool.submit(() -> {
        System.out.println("Task " + taskId + " on " + Thread.currentThread().getName());
    });
}

pool.shutdown();             // no new tasks accepted
pool.awaitTermination(30, TimeUnit.SECONDS);  // wait for all tasks
```

Full details in the Executors section.

## Thread Methods Reference

```java
Thread t = new Thread(() -> { });

t.start();              // start the thread (NEW → RUNNABLE)
t.join();               // wait for t to finish (blocks current thread)
t.join(1000);           // wait at most 1 second
t.interrupt();          // set interrupt flag (doesn't kill thread — just signals)
t.isAlive();            // true if thread has started and not terminated
t.getName();            // "Thread-0" etc.
t.setName("worker-1");
Thread.currentThread(); // get reference to current running thread
Thread.sleep(500);      // sleep 500ms (throws InterruptedException)
Thread.yield();         // hint to scheduler to let other threads run
```

### Handling InterruptedException

```java
// Interruption is cooperative — you must CHECK and RESPOND to it
thread.interrupt();   // sets the interrupt flag

// In the thread's code:
void run() {
    while (!Thread.currentThread().isInterrupted()) {
        try {
            Thread.sleep(100);   // throws InterruptedException if interrupted
            doWork();
        } catch (InterruptedException e) {
            // IMPORTANT: sleep() clears the interrupt flag when it throws
            // Restore the flag so callers can detect it:
            Thread.currentThread().interrupt();
            break;   // or return — clean shutdown
        }
    }
}
```

---

# 4. Synchronization & Intrinsic Locks

## The Race Condition Problem

```java
class Counter {
    private int count = 0;

    public void increment() {
        count++;   // looks atomic but is NOT!
    }
    // count++ compiles to:
    //   1. READ  count from memory → register
    //   2. ADD   1 to register
    //   3. WRITE register back to memory
    // Two threads can interleave these steps!
}

Counter counter = new Counter();

// Thread 1: reads count=0, adds 1, prepares to write 1
// Thread 2: reads count=0 (hasn't seen Thread 1's write yet!), adds 1, writes 1
// Thread 1: writes 1
// FINAL count = 1, but we did 2 increments! LOST UPDATE
```

## synchronized keyword — Intrinsic Lock (Monitor)

Every Java object has a hidden **monitor lock** (intrinsic lock). `synchronized` acquires that lock before executing and releases it after:

```java
class SafeCounter {
    private int count = 0;

    // Synchronized METHOD — locks on 'this' object
    public synchronized void increment() {
        count++;   // now atomic — only one thread at a time
    }

    public synchronized int getCount() {
        return count;
    }

    // Synchronized BLOCK — finer-grained control
    public void incrementBlock() {
        // do non-critical work here (no lock held)
        synchronized (this) {    // lock only for critical section
            count++;
        }
        // lock released, other work here (no lock held)
    }

    // Static synchronized — locks on Class object (not instance)
    public static synchronized void staticMethod() {
        // locks Counter.class object
    }
}
```

## How Intrinsic Locks Work Internally

```
Object Monitor:
┌────────────────────────────────────────────┐
│  Owner: Thread-1 (currently holds lock)    │
│  Entry Set: [Thread-2, Thread-3]           │  ← threads competing for lock (BLOCKED)
│  Wait Set:  [Thread-4]                     │  ← threads that called wait() (WAITING)
└────────────────────────────────────────────┘

Thread-1 calls synchronized → enters monitor → becomes Owner
Thread-2 tries synchronized → lock held → joins Entry Set (BLOCKED)
Thread-1 calls wait() → releases lock → moves to Wait Set (WAITING)
Thread-3 gets lock → becomes Owner
Thread-3 calls notify() → moves Thread-4 from Wait Set → Entry Set
Thread-3 exits synchronized → releases lock
Thread-4 (or Thread-2) acquires lock → becomes Owner
```

## wait(), notify(), notifyAll()

These MUST be called from within a `synchronized` block on the same object:

```java
class MessageQueue {
    private String message = null;
    private final Object lock = new Object();

    // Called by producer thread
    public void send(String msg) throws InterruptedException {
        synchronized (lock) {
            while (message != null) {      // while — not if (guard against spurious wakeups)
                lock.wait();               // release lock, wait for consumer to take message
            }
            message = msg;
            lock.notifyAll();              // wake up consumer waiting to receive
        }
    }

    // Called by consumer thread
    public String receive() throws InterruptedException {
        synchronized (lock) {
            while (message == null) {      // wait until message available
                lock.wait();
            }
            String msg = message;
            message = null;
            lock.notifyAll();              // wake up producer waiting to send
            return msg;
        }
    }
}
```

### Why `while` not `if` for wait()?

**Spurious wakeups:** A thread can wake from `wait()` without `notify()` being called — this is allowed by the JVM spec and happens on some platforms. Using `while` re-checks the condition and waits again if it's not actually met.

```java
// WRONG:
synchronized (lock) {
    if (queue.isEmpty()) lock.wait();   // could wake up spuriously and proceed on empty queue!
    process(queue.poll());              // NullPointerException or wrong behavior
}

// CORRECT:
synchronized (lock) {
    while (queue.isEmpty()) lock.wait();  // re-check condition after every wakeup
    process(queue.poll());
}
```

## Reentrancy

Java's intrinsic locks are **reentrant** — a thread can re-acquire a lock it already holds:

```java
class ReentrantExample {
    public synchronized void outer() {
        System.out.println("outer");
        inner();   // calls synchronized inner() — same thread can re-acquire the lock
    }

    public synchronized void inner() {
        System.out.println("inner");
        // Without reentrancy: outer() holds the lock → inner() tries to acquire same lock → DEADLOCK
        // With reentrancy: same thread re-enters → works fine
    }
}
```

The JVM tracks a lock count per thread-object pair. First acquire: count=1. Re-acquire: count=2. Each `synchronized` exit decrements; lock released when count=0.

## Interview Questions

- **Q: What is a race condition?**
  A: When the outcome of a program depends on the relative timing of threads — multiple threads reading and writing shared data without synchronization, leading to inconsistent results.

- **Q: What is the difference between synchronized method and synchronized block?**
  A: Both acquire the same lock (intrinsic lock of the object). Synchronized method locks the entire method — coarser granularity. Synchronized block locks only the specified section — allows non-critical code to run without holding the lock, improving throughput.

- **Q: Why must wait()/notify() be called inside synchronized?**
  A: To prevent a race condition between the check-and-wait sequence. If you check a condition, then another thread modifies it before you call wait(), you'd wait forever (missed notification). The synchronized block ensures atomicity of the check-then-wait sequence.

---

# 5. The volatile Keyword

## What volatile Guarantees

`volatile` provides two guarantees:
1. **Visibility:** Writes to a volatile variable are immediately visible to all threads (written to main memory, not cached in CPU registers)
2. **Ordering:** Prevents reordering of instructions across the volatile access (memory barrier)

```java
class StatusFlag {
    private volatile boolean running = true;   // volatile!

    public void stop() {
        running = false;   // write goes directly to main memory
    }

    public void run() {
        while (running) {         // read always comes from main memory
            processRequest();
        }
        System.out.println("Stopped cleanly");
    }
}
```

Without `volatile`: the JIT might cache `running` in a CPU register for `run()`. The stop signal from another thread would never be seen — infinite loop.

## What volatile Does NOT Guarantee

`volatile` does NOT guarantee **atomicity** of compound operations:

```java
private volatile int count = 0;

// STILL NOT THREAD-SAFE even with volatile:
public void increment() {
    count++;   // read-modify-write: 3 steps, not atomic
}
// Thread 1: reads count=5
// Thread 2: reads count=5
// Thread 1: writes count=6
// Thread 2: writes count=6   ← LOST UPDATE
```

For atomic compound operations, use `synchronized` or `AtomicInteger`.

## volatile vs synchronized

| Aspect | volatile | synchronized |
|--------|---------|-------------|
| Visibility | Yes | Yes |
| Atomicity | No | Yes |
| Blocking | No (never blocks) | Yes (threads may block) |
| Performance | Fast | Slower (lock overhead) |
| Use for | Simple flags, status indicators | Compound operations, critical sections |

## Typical volatile Use Cases

```java
// 1. Stop flag for thread
volatile boolean running = true;

// 2. Singleton double-checked locking (REQUIRES volatile)
class Singleton {
    private static volatile Singleton instance;

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();  // volatile ensures safe publication
                }
            }
        }
        return instance;
    }
}
// Without volatile: JVM may reorder: allocate memory → update reference → initialize
// Another thread sees non-null but uninitialized object!

// 3. Progress counter (write once, read by many)
volatile int progress = 0;
```

---

# 6. Reentrant Locks & Conditions

## ReentrantLock — Explicit Lock

`java.util.concurrent.locks.ReentrantLock` provides the same semantics as `synchronized` but with more capabilities:

```java
import java.util.concurrent.locks.*;

class SafeCounter {
    private int count = 0;
    private final ReentrantLock lock = new ReentrantLock();

    public void increment() {
        lock.lock();           // acquire lock (blocks if held by another thread)
        try {
            count++;
        } finally {
            lock.unlock();     // ALWAYS in finally — ensures release even on exception
        }
    }

    public int getCount() {
        lock.lock();
        try {
            return count;
        } finally {
            lock.unlock();
        }
    }
}
```

## ReentrantLock Advantages over synchronized

```java
// 1. tryLock() — non-blocking attempt
if (lock.tryLock()) {
    try {
        // got the lock, do work
    } finally {
        lock.unlock();
    }
} else {
    // lock not available — do something else, don't block
}

// 2. tryLock with timeout
if (lock.tryLock(500, TimeUnit.MILLISECONDS)) {
    // got lock within 500ms
}

// 3. lockInterruptibly() — can be interrupted while waiting
try {
    lock.lockInterruptibly();  // throws InterruptedException if thread interrupted while waiting
} catch (InterruptedException e) {
    // handle
}

// 4. Fairness — FIFO ordering (longest-waiting thread gets lock next)
ReentrantLock fairLock = new ReentrantLock(true);  // fair mode
// Default (false) = non-fair: any waiting thread may get the lock
// Fair is slower but prevents starvation

// 5. Diagnostics
lock.isLocked();              // true if any thread holds it
lock.isHeldByCurrentThread(); // true if current thread holds it
lock.getQueueLength();        // number of threads waiting
```

## Condition Variables

`Condition` is the ReentrantLock equivalent of `wait()/notify()`:

```java
class BoundedBuffer<T> {
    private final Queue<T> buffer = new LinkedList<>();
    private final int capacity;
    private final ReentrantLock lock = new ReentrantLock();
    private final Condition notFull  = lock.newCondition();  // producers wait here
    private final Condition notEmpty = lock.newCondition();  // consumers wait here

    BoundedBuffer(int capacity) { this.capacity = capacity; }

    public void put(T item) throws InterruptedException {
        lock.lock();
        try {
            while (buffer.size() == capacity) {
                notFull.await();   // wait until not full (releases lock)
            }
            buffer.offer(item);
            notEmpty.signal();     // signal one consumer
        } finally {
            lock.unlock();
        }
    }

    public T take() throws InterruptedException {
        lock.lock();
        try {
            while (buffer.isEmpty()) {
                notEmpty.await();  // wait until not empty
            }
            T item = buffer.poll();
            notFull.signal();      // signal one producer
            return item;
        } finally {
            lock.unlock();
        }
    }
}
```

### synchronized vs ReentrantLock Comparison

| Feature | synchronized | ReentrantLock |
|---------|-------------|--------------|
| Syntax | Built-in keyword | Explicit lock/unlock |
| Reentrancy | Yes | Yes |
| tryLock (non-blocking) | No | Yes |
| Timeout | No | Yes |
| Interruptible wait | No | Yes (lockInterruptibly) |
| Fairness control | No | Yes |
| Multiple conditions | No (one per object) | Yes (multiple Conditions) |
| Performance | Good (JVM optimized) | Similar |
| Forgetting to unlock | Impossible (auto) | Easy mistake → use try-finally |

## ReadWriteLock

When reads are far more frequent than writes, `ReentrantReadWriteLock` allows concurrent reads:

```java
class CachedData {
    private final ReentrantReadWriteLock rwLock = new ReentrantReadWriteLock();
    private final Lock readLock  = rwLock.readLock();
    private final Lock writeLock = rwLock.writeLock();
    private Map<String, String> cache = new HashMap<>();

    public String get(String key) {
        readLock.lock();    // multiple readers can hold readLock simultaneously
        try {
            return cache.get(key);
        } finally {
            readLock.unlock();
        }
    }

    public void put(String key, String value) {
        writeLock.lock();   // exclusive — blocks all readers AND writers
        try {
            cache.put(key, value);
        } finally {
            writeLock.unlock();
        }
    }
}
// Read-heavy workloads: massively improved throughput
// Write operations still exclusive
```

---

# 7. Deadlock, Starvation, Livelock

## Deadlock

Deadlock occurs when two or more threads are each waiting for a lock that the other holds — circular wait:

```java
class DeadlockDemo {
    private final Object lockA = new Object();
    private final Object lockB = new Object();

    void method1() {
        synchronized (lockA) {
            System.out.println("Thread 1: holds A, waiting for B");
            synchronized (lockB) {   // waiting for B (Thread 2 holds B)
                System.out.println("Thread 1: holds A and B");
            }
        }
    }

    void method2() {
        synchronized (lockB) {
            System.out.println("Thread 2: holds B, waiting for A");
            synchronized (lockA) {   // waiting for A (Thread 1 holds A)
                System.out.println("Thread 2: holds A and B");
            }
        }
    }
}

// Thread 1 calls method1: acquires A, wants B
// Thread 2 calls method2: acquires B, wants A
// → DEADLOCK — both wait forever
```

```
Deadlock Visualization:
Thread 1 ──holds──► Lock A ◄──wants── Thread 2
Thread 1 ──wants──► Lock B ◄──holds── Thread 2
```

### Four Conditions for Deadlock (Coffman Conditions)

All four must hold for deadlock to occur:
1. **Mutual Exclusion:** Resources held exclusively (locks are mutually exclusive)
2. **Hold and Wait:** Thread holds one resource while waiting for another
3. **No Preemption:** Locks can't be forcibly taken
4. **Circular Wait:** T1 waits for T2's resource, T2 waits for T1's resource

### Deadlock Prevention Strategies

```java
// Strategy 1: Lock Ordering — always acquire locks in same order
// Thread 1 AND Thread 2 both acquire A first, then B
void method1() {
    synchronized (lockA) {
        synchronized (lockB) { doWork(); }
    }
}
void method2() {
    synchronized (lockA) {   // same order as method1!
        synchronized (lockB) { doWork(); }
    }
}

// Strategy 2: tryLock with timeout
boolean acquired = false;
try {
    if (lockA.tryLock(100, TimeUnit.MILLISECONDS)) {
        try {
            if (lockB.tryLock(100, TimeUnit.MILLISECONDS)) {
                try {
                    doWork();
                } finally { lockB.unlock(); }
            }
        } finally { lockA.unlock(); }
    }
    // If either tryLock fails — back off, retry later
} catch (InterruptedException e) { Thread.currentThread().interrupt(); }

// Strategy 3: Avoid holding multiple locks simultaneously
// Refactor design so you never need two locks at once
```

### Detecting Deadlock

```java
// Programmatic detection using ThreadMXBean:
ThreadMXBean tmxb = ManagementFactory.getThreadMXBean();
long[] deadlockedThreads = tmxb.findDeadlockedThreads();
if (deadlockedThreads != null) {
    ThreadInfo[] infos = tmxb.getThreadInfo(deadlockedThreads);
    for (ThreadInfo info : infos) {
        System.out.println(info.getThreadName() + " waiting on " + info.getLockName());
    }
}

// Also: jstack <pid> in terminal prints thread dump showing deadlocked threads
```

## Starvation

A thread never gets CPU time because higher-priority threads always run first, or a lock is always acquired by other threads first:

```java
// Example: unfair lock — same threads keep getting it
ReentrantLock fairLock = new ReentrantLock(true);  // fair mode prevents starvation
// With fair=true, longest-waiting thread gets lock next
```

## Livelock

Threads keep responding to each other's state but make no actual progress — like two people in a hallway both stepping aside in the same direction repeatedly:

```java
// Two threads: each backs off if the other is active, but they back off simultaneously
class Worker {
    boolean active = true;

    void cooperate(Worker other) throws InterruptedException {
        while (active) {
            if (other.active) {
                System.out.println(Thread.currentThread().getName() + " backing off");
                active = false;
                Thread.sleep(100);
                active = true;   // back to active... other is also active again
            }
        }
    }
}
// Solution: add randomized backoff so they don't always move simultaneously
Thread.sleep((long)(Math.random() * 100));
```

## Interview Questions

- **Q: What are the four conditions for a deadlock?**
  A: Mutual Exclusion (locks are exclusive), Hold and Wait (holding one lock while requesting another), No Preemption (can't forcibly take locks), and Circular Wait (circular dependency between threads and locks). Prevent deadlock by breaking any one of these four conditions.

- **Q: What is the difference between deadlock and livelock?**
  A: In deadlock, threads are completely blocked — no progress, no CPU usage. In livelock, threads are active and consuming CPU but making no actual forward progress — they keep responding to each other and staying in a loop.

---

# 8. Atomic Classes

Atomic classes provide **lock-free, thread-safe** operations using CPU-level Compare-And-Swap (CAS) instructions:

## How CAS Works

```
CAS(memory_location, expected_value, new_value):
  if (*memory_location == expected_value):
      *memory_location = new_value
      return SUCCESS
  else:
      return FAILURE (and retry)

This is one ATOMIC CPU instruction — no lock needed!
```

## AtomicInteger

```java
import java.util.concurrent.atomic.*;

AtomicInteger count = new AtomicInteger(0);

// Thread-safe operations:
count.get();                  // read current value
count.set(10);                // set value
count.incrementAndGet();      // ++count (returns new value)
count.getAndIncrement();      // count++ (returns old value)
count.decrementAndGet();      // --count
count.addAndGet(5);           // count += 5, returns new value
count.getAndAdd(5);           // returns old value, then adds 5

// CAS — the core operation:
count.compareAndSet(10, 20);  // if count==10, set to 20, return true; else return false

// Complex atomic update (Java 8+):
count.updateAndGet(x -> x * 2);   // atomically: count = count * 2
count.accumulateAndGet(5, Integer::sum);  // atomically: count += 5
```

## AtomicLong, AtomicBoolean, AtomicReference

```java
AtomicLong longVal = new AtomicLong(0L);
longVal.incrementAndGet();

AtomicBoolean flag = new AtomicBoolean(false);
flag.compareAndSet(false, true);  // set to true only if currently false

AtomicReference<String> ref = new AtomicReference<>("initial");
ref.compareAndSet("initial", "updated");
ref.getAndUpdate(s -> s.toUpperCase());
```

## AtomicInteger vs synchronized vs volatile

| Aspect | volatile | synchronized | AtomicInteger |
|--------|---------|-------------|--------------|
| Visibility | Yes | Yes | Yes |
| Atomicity | No | Yes | Yes |
| Blocking | No | Yes | No (CAS loop) |
| Performance | Fastest (read/write only) | Slower (lock) | Fast (CAS) |
| Use for | Simple flags | Complex critical sections | Counters, references |

## LongAdder — High-Contention Counter

When many threads update a counter simultaneously, CAS retries on `AtomicLong` cause contention. `LongAdder` uses **cell striping** — each thread updates its own cell, final sum computed when needed:

```java
LongAdder adder = new LongAdder();

// In many threads simultaneously:
adder.increment();  // no contention — each thread uses its own cell
adder.add(5);

// Get total:
long total = adder.sum();  // sums all cells

// LongAdder is preferred over AtomicLong for high-contention counting
// AtomicLong is better when you need compareAndSet semantics
```

---

# 9. Thread Pools & Executors Framework

## Why Thread Pools?

Creating a raw thread for every task is expensive:
- Thread creation: allocate stack memory (512KB–1MB per thread), JVM setup
- Context switching overhead increases with more threads
- Too many threads → thrashing, OOM

Thread pools maintain a pool of pre-created threads that pick up tasks as they arrive:

```
Thread Pool:
                 Task Queue (BlockingQueue)
Submitter  ──►  [Task1][Task2][Task3][Task4]
                         ↓ ↓ ↓
                 ┌──────────────────────────┐
                 │ Worker-1: executing Task1│
                 │ Worker-2: executing Task2│
                 │ Worker-3: idle           │
                 │ Worker-4: idle           │
                 └──────────────────────────┘
```

## ThreadPoolExecutor — The Core

All `Executors` factory methods create `ThreadPoolExecutor` underneath:

```java
ThreadPoolExecutor pool = new ThreadPoolExecutor(
    2,                           // corePoolSize: min threads always alive
    10,                          // maximumPoolSize: max threads when queue full
    60L, TimeUnit.SECONDS,       // keepAliveTime: idle threads above core die after this
    new LinkedBlockingQueue<>(100),  // workQueue: holds tasks when all threads busy
    new ThreadPoolExecutor.CallerRunsPolicy()  // rejectionPolicy: if queue AND max threads full
);
```

### Rejection Policies

```java
// AbortPolicy (default): throw RejectedExecutionException
// CallerRunsPolicy: caller thread runs the task (backpressure)
// DiscardPolicy: silently discard the task
// DiscardOldestPolicy: discard oldest queued task, retry submission
```

## Executors Factory Methods

```java
// 1. Fixed thread pool — N threads, tasks queue up if all busy
ExecutorService fixed = Executors.newFixedThreadPool(4);
// Use for: CPU-bound tasks (N = number of CPU cores)
// int cores = Runtime.getRuntime().availableProcessors();

// 2. Cached thread pool — creates threads as needed, reuses idle ones
ExecutorService cached = Executors.newCachedThreadPool();
// Threads idle for 60s are terminated
// Use for: many short-lived IO-bound tasks
// WARNING: no upper bound — can create thousands of threads under load!

// 3. Single thread executor — one thread, tasks execute sequentially
ExecutorService single = Executors.newSingleThreadExecutor();
// Use for: tasks that must run in order, serialized access to resource

// 4. Scheduled executor — run tasks with delay or periodically
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(2);
scheduled.schedule(() -> System.out.println("Delayed!"), 5, TimeUnit.SECONDS);
scheduled.scheduleAtFixedRate(() -> System.out.println("Every 1s"), 0, 1, TimeUnit.SECONDS);
scheduled.scheduleWithFixedDelay(() -> cleanup(), 0, 10, TimeUnit.SECONDS);
// scheduleAtFixedRate: starts next run at fixed interval from PREVIOUS START
// scheduleWithFixedDelay: waits fixed delay after PREVIOUS COMPLETION

// 5. Work-stealing pool (Java 8+) — ForkJoinPool with parallelism
ExecutorService workStealing = Executors.newWorkStealingPool();
// Uses ForkJoinPool internally — good for recursive/parallel tasks
```

## Submitting Tasks

```java
ExecutorService pool = Executors.newFixedThreadPool(4);

// submit(Runnable) — returns Future<?> (result is null)
Future<?> f1 = pool.submit(() -> System.out.println("runnable task"));
f1.get();   // blocks until done (returns null)

// submit(Callable) — returns Future<V>
Future<Integer> f2 = pool.submit(() -> {
    Thread.sleep(1000);
    return 42;
});
Integer result = f2.get();         // blocks until result ready
Integer result2 = f2.get(2, TimeUnit.SECONDS); // blocks at most 2s, throws TimeoutException

// execute(Runnable) — no Future returned, can't check completion
pool.execute(() -> System.out.println("fire and forget"));

// invokeAll — submit list of Callables, wait for ALL to complete
List<Callable<Integer>> tasks = List.of(
    () -> compute(1),
    () -> compute(2),
    () -> compute(3)
);
List<Future<Integer>> futures = pool.invokeAll(tasks);  // blocks until all done
for (Future<Integer> f : futures) {
    System.out.println(f.get());
}

// invokeAny — submit list, return first result, cancel rest
Integer firstResult = pool.invokeAny(tasks);  // returns first completed result
```

## Proper Shutdown

```java
pool.shutdown();       // stop accepting new tasks, let queued tasks finish
// OR:
pool.shutdownNow();    // interrupt running tasks, return unstarted tasks

// Wait for completion:
try {
    if (!pool.awaitTermination(60, TimeUnit.SECONDS)) {
        pool.shutdownNow();  // force shutdown if not done in 60s
    }
} catch (InterruptedException e) {
    pool.shutdownNow();
    Thread.currentThread().interrupt();
}
```

## Sizing Thread Pools

```
CPU-Bound Tasks (computation):
  optimal threads = number of CPU cores
  int cores = Runtime.getRuntime().availableProcessors();
  Executors.newFixedThreadPool(cores)

IO-Bound Tasks (network, disk):
  threads can be many more (while waiting on IO, CPU is free)
  optimal threads = cores × (1 + wait_time / service_time)
  e.g., if 80% of time is waiting: 4 cores × (1 + 4) = 20 threads
```

---

# 10. Callable, Future, and CompletableFuture

## Future — Basic Async Result

```java
ExecutorService pool = Executors.newFixedThreadPool(2);

Future<String> future = pool.submit(() -> {
    Thread.sleep(2000);  // simulate slow network call
    return "data from server";
});

// Do other work while future is computing...
System.out.println("Doing other work...");

// Block and get result:
try {
    String result = future.get(3, TimeUnit.SECONDS);  // wait max 3 seconds
    System.out.println("Got: " + result);
} catch (TimeoutException e) {
    future.cancel(true);  // cancel task, interrupt if running
    System.out.println("Timed out!");
} catch (ExecutionException e) {
    System.out.println("Task threw exception: " + e.getCause());
}

future.isDone();       // true if completed (normally, cancelled, or exception)
future.isCancelled();  // true if cancelled
```

## Future Limitations

Future has several problems in production code:
- `get()` blocks — no way to say "call me when done"
- Can't chain futures — "when A is done, start B"
- Can't combine — "wait for both A and B"
- Exception handling is awkward (wrapped in ExecutionException)

## CompletableFuture — Reactive Async (Java 8+)

`CompletableFuture` solves all Future's limitations with a fluent, composable API:

```java
import java.util.concurrent.CompletableFuture;

// 1. Create a CompletableFuture
CompletableFuture<String> cf = CompletableFuture.supplyAsync(() -> {
    // runs in ForkJoinPool.commonPool() by default
    return fetchDataFromServer();
});

// 2. Transform result when done (non-blocking!)
CompletableFuture<Integer> length = cf.thenApply(String::length);

// 3. Chain actions
CompletableFuture<Void> print = cf
    .thenApply(String::toUpperCase)
    .thenAccept(System.out::println);  // terminal — returns void

// 4. Chain that returns another async operation
CompletableFuture<String> chained = cf
    .thenCompose(data -> CompletableFuture.supplyAsync(() -> process(data)));

// 5. Combine two independent futures when BOTH complete
CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> "Hello");
CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> "World");
CompletableFuture<String> combined = f1.thenCombine(f2, (a, b) -> a + " " + b);
combined.get();  // "Hello World"

// 6. Wait for ALL to complete
CompletableFuture<Void> all = CompletableFuture.allOf(f1, f2);
all.join();  // blocks until both done

// 7. Take the FIRST to complete
CompletableFuture<Object> any = CompletableFuture.anyOf(f1, f2);
Object first = any.get();  // whichever finishes first

// 8. Exception handling
CompletableFuture<String> handled = cf
    .exceptionally(ex -> "default value on error")   // recover from exception
    .handle((result, ex) -> {                         // OR handle both result and exception
        if (ex != null) return "error: " + ex.getMessage();
        return result.toUpperCase();
    });

// 9. Timeout (Java 9+)
CompletableFuture<String> withTimeout = cf
    .orTimeout(2, TimeUnit.SECONDS)        // throws TimeoutException after 2s
    .completeOnTimeout("default", 2, TimeUnit.SECONDS);  // returns "default" after 2s

// 10. Custom executor
ExecutorService myPool = Executors.newFixedThreadPool(4);
CompletableFuture<String> withPool = CompletableFuture.supplyAsync(
    () -> fetchData(),
    myPool   // use custom pool instead of common ForkJoinPool
);
```

## Real-World Example: Parallel API Calls

```java
// Fetch user, orders, and inventory in PARALLEL — not sequentially
CompletableFuture<User> userFuture = CompletableFuture.supplyAsync(
    () -> userService.getUser(userId));

CompletableFuture<List<Order>> ordersFuture = CompletableFuture.supplyAsync(
    () -> orderService.getOrders(userId));

CompletableFuture<Inventory> inventoryFuture = CompletableFuture.supplyAsync(
    () -> inventoryService.getInventory());

// Wait for all three, then combine:
CompletableFuture<Dashboard> dashboard = CompletableFuture
    .allOf(userFuture, ordersFuture, inventoryFuture)
    .thenApply(v -> new Dashboard(
        userFuture.join(),
        ordersFuture.join(),
        inventoryFuture.join()
    ));

Dashboard result = dashboard.get(5, TimeUnit.SECONDS);
// Total time ≈ max(user_time, orders_time, inventory_time) instead of sum!
```

## thenApply vs thenCompose vs thenCombine

| Method | When to use | Returns |
|--------|-------------|---------|
| `thenApply(fn)` | Transform result synchronously | `CF<U>` |
| `thenCompose(fn)` | Chain to another async operation (fn returns CF) | `CF<U>` |
| `thenCombine(other, fn)` | Combine two independent futures | `CF<V>` |
| `thenAccept(fn)` | Consume result, no return | `CF<Void>` |
| `thenRun(fn)` | Run action after complete, no access to result | `CF<Void>` |

---

# 11. Fork/Join Pool

## Theory

`ForkJoinPool` is designed for **divide-and-conquer** algorithms — recursively split a problem into subtasks, compute them in parallel, combine results:

```
findSum([1..1_000_000]):
        FORK
       /    \
 [1..500K]  [500K..1M]
    FORK         FORK
   /    \       /    \
[1..250K]... [750K..]...
    JOIN         JOIN
       \    /
        JOIN → total sum
```

## Work-Stealing Algorithm

ForkJoinPool implements **work stealing** — idle threads steal tasks from busy threads' queues:

```
Thread-1 queue: [T1][T2][T3][T4]   (busy working on T1)
Thread-2 queue: []                  (idle — steals T4 from Thread-1's tail!)
Thread-3 queue: [T5]                (busy)
Thread-4 queue: []                  (steals T5's subtask)
```

This keeps all threads busy with minimal coordination.

## RecursiveTask Example

```java
import java.util.concurrent.*;

class SumTask extends RecursiveTask<Long> {
    private static final int THRESHOLD = 10_000;  // split if array bigger than this
    private final int[] array;
    private final int start, end;

    SumTask(int[] array, int start, int end) {
        this.array = array;
        this.start = start;
        this.end   = end;
    }

    @Override
    protected Long compute() {
        int length = end - start;

        if (length <= THRESHOLD) {
            // BASE CASE: small enough to compute directly
            long sum = 0;
            for (int i = start; i < end; i++) sum += array[i];
            return sum;
        }

        // RECURSIVE CASE: split and fork
        int mid = start + length / 2;

        SumTask leftTask  = new SumTask(array, start, mid);
        SumTask rightTask = new SumTask(array, mid, end);

        leftTask.fork();                 // submit leftTask to pool (async)
        long rightResult = rightTask.compute();  // compute right in current thread
        long leftResult  = leftTask.join();      // wait for left result

        return leftResult + rightResult;
    }
}

// Usage:
int[] data = new int[1_000_000];
Arrays.fill(data, 1);

ForkJoinPool pool = new ForkJoinPool();  // default parallelism = CPU cores
Long sum = pool.invoke(new SumTask(data, 0, data.length));
System.out.println("Sum: " + sum);  // 1000000

// OR use common pool (shared, no need to create):
Long sum2 = ForkJoinPool.commonPool().invoke(new SumTask(data, 0, data.length));
```

## RecursiveAction (no return value)

```java
class ArrayFiller extends RecursiveAction {
    private int[] array;
    private int start, end, value;

    // ... constructor ...

    @Override
    protected void compute() {
        if (end - start <= THRESHOLD) {
            Arrays.fill(array, start, end, value);  // base case
            return;
        }
        int mid = (start + end) / 2;
        invokeAll(
            new ArrayFiller(array, start, mid, value),
            new ArrayFiller(array, mid, end, value)
        );  // fork both, wait for both to complete
    }
}
```

## Parallel Streams (ForkJoinPool under the hood)

```java
int[] numbers = IntStream.rangeClosed(1, 1_000_000).toArray();

// Sequential:
long sum = Arrays.stream(numbers).sum();

// Parallel (uses ForkJoinPool.commonPool()):
long parallelSum = Arrays.stream(numbers).parallel().sum();

// Use parallel streams when:
// - Large datasets (>10,000 elements)
// - Stateless, associative operations
// - CPU-bound (not IO-bound)
// - Don't share mutable state
```

---

# 12. Concurrent Collections

(Covered in detail in Part 5. Summary here for completeness.)

```java
// Thread-safe Map — production default
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("key", 1);
map.computeIfAbsent("count", k -> 0);
map.merge("count", 1, Integer::sum);   // atomic increment

// Thread-safe List — for read-heavy workloads
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("item");   // copies entire array on each write — expensive!

// Blocking Queue — for producer-consumer
BlockingQueue<Task> queue = new LinkedBlockingQueue<>(100);
queue.put(task);    // blocks if full
queue.take();       // blocks if empty
queue.offer(task, 500, TimeUnit.MILLISECONDS);  // timeout version
queue.poll(500, TimeUnit.MILLISECONDS);

// Other blocking queues:
ArrayBlockingQueue<T>   // fixed-size, array-backed
PriorityBlockingQueue<T> // priority ordering
SynchronousQueue<T>     // no buffer — transfer directly from producer to consumer
DelayQueue<T>           // elements become available after delay
```

## Semaphore — Limit Concurrent Access

```java
// Allow at most 3 threads to access a resource simultaneously
Semaphore semaphore = new Semaphore(3);

void accessResource() throws InterruptedException {
    semaphore.acquire();   // decrement permit count (blocks at 0)
    try {
        useSharedResource();
    } finally {
        semaphore.release();  // increment permit count
    }
}

// Use for: connection pools, rate limiting, resource-bounded access
// Semaphore(1) acts like a mutex (binary semaphore)
```

## CountDownLatch — Wait for Multiple Events

```java
// Main thread waits until N worker threads complete initialization
CountDownLatch latch = new CountDownLatch(3);

// Worker threads:
Thread worker1 = new Thread(() -> {
    initializeService1();
    latch.countDown();  // decrement count from 3 to 2
});
Thread worker2 = new Thread(() -> {
    initializeService2();
    latch.countDown();  // 2 to 1
});
Thread worker3 = new Thread(() -> {
    initializeService3();
    latch.countDown();  // 1 to 0 → releases waiting threads
});

worker1.start(); worker2.start(); worker3.start();
latch.await();  // blocks until count reaches 0
System.out.println("All services initialized!");

// CountDownLatch is one-time use — cannot be reset
```

## CyclicBarrier — Synchronize at a Point

```java
// All threads must reach the barrier before any can proceed
CyclicBarrier barrier = new CyclicBarrier(4, () -> {
    System.out.println("All threads reached barrier — proceeding to phase 2");  // runs once all arrive
});

Runnable task = () -> {
    doPhase1Work();
    barrier.await();   // wait here until all 4 threads arrive
    doPhase2Work();
    barrier.await();   // CyclicBarrier is REUSABLE — same barrier for phase 3
    doPhase3Work();
};

// Start 4 threads — they sync at each phase boundary
for (int i = 0; i < 4; i++) new Thread(task).start();
```

| | CountDownLatch | CyclicBarrier |
|--|---------------|--------------|
| Reusable | No | Yes |
| Count direction | Down from N to 0 | Up from 0 to N |
| Who waits | await() callers | await() callers |
| Release trigger | Count reaches 0 | All parties arrived |
| Use for | Wait for events | Synchronize phases |

---

# 13. Java Memory Model & Happens-Before

## The Problem: Visibility Without Happens-Before

```java
int x = 0;
boolean ready = false;

// Thread A:
x = 42;
ready = true;

// Thread B:
if (ready) {
    System.out.println(x);  // Could print 0!
}
```

Why? Two reasons:
1. **Caching:** Thread A's writes may be in its CPU cache, not main memory
2. **Reordering:** JVM/CPU may reorder `x=42` and `ready=true` for performance

## Happens-Before Rules

The JMM defines **happens-before** as the guarantee that if A happens-before B, A's effects are visible to B.

### Complete List of Happens-Before Rules

**1. Program Order Rule:**
```java
// In a single thread, each action happens-before all subsequent actions
int a = 1;     // happens-before
int b = 2;     // happens-before
int c = a + b; // b=3 guaranteed
```

**2. Monitor Lock Rule:**
```java
// unlock happens-before lock of same monitor
synchronized (lock) { x = 42; }  // write happens-before...
// (another thread acquires same lock)
synchronized (lock) { System.out.println(x); }  // ...this read. x is 42.
```

**3. Volatile Variable Rule:**
```java
volatile int value = 0;
// Write to volatile happens-before all subsequent reads of that volatile
value = 42;               // Thread A writes
int v = value;            // Thread B reads — guaranteed to see 42
```

**4. Thread Start Rule:**
```java
x = 42;
thread.start();           // start() happens-before any action in the new thread
// new thread is guaranteed to see x = 42
```

**5. Thread Join Rule:**
```java
// All actions in thread T happen-before thread.join() returns
thread.join();
// main thread is guaranteed to see everything thread did
System.out.println(resultSetByThread);  // safe to read
```

**6. Transitivity:**
```
If A happens-before B, and B happens-before C, then A happens-before C.
```

## Safe Publication

An object is **safely published** if its initialization is visible to all threads that access it:

```java
// UNSAFE publication — no happens-before guarantee
class Unsafe {
    static Helper helper;  // not volatile, not synchronized

    static void init() {
        helper = new Helper();   // another thread may see partially constructed object!
    }
}

// SAFE publication methods:
// 1. Initialize in static initializer (class loading guarantees visibility)
static final Helper helper = new Helper();

// 2. volatile reference
static volatile Helper helper;

// 3. Synchronized access
static Helper helper;
static synchronized Helper getHelper() {
    if (helper == null) helper = new Helper();
    return helper;
}

// 4. Immutable objects — inherently thread-safe once published
final class ImmutableHelper {
    final int value;
    ImmutableHelper(int v) { this.value = v; }
}
```

---

# 14. Producer-Consumer Pattern

The producer-consumer pattern is the most fundamental concurrency pattern — producers generate data, consumers process it, separated by a queue:

## Implementation 1: BlockingQueue (Simplest & Best)

```java
class ProducerConsumerWithBlockingQueue {
    private static final BlockingQueue<Integer> queue = new LinkedBlockingQueue<>(10);

    static class Producer implements Runnable {
        @Override
        public void run() {
            try {
                for (int i = 0; i < 20; i++) {
                    queue.put(i);   // blocks if queue is full — built-in backpressure
                    System.out.println("Produced: " + i);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    static class Consumer implements Runnable {
        @Override
        public void run() {
            try {
                while (true) {
                    Integer item = queue.poll(2, TimeUnit.SECONDS);  // wait up to 2s
                    if (item == null) break;  // timeout — producer probably done
                    System.out.println("Consumed: " + item);
                    Thread.sleep(200);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread producer  = new Thread(new Producer());
        Thread consumer1 = new Thread(new Consumer());
        Thread consumer2 = new Thread(new Consumer());

        producer.start();
        consumer1.start();
        consumer2.start();

        producer.join();
        consumer1.join();
        consumer2.join();
    }
}
```

## Implementation 2: wait()/notify() (Manual, Educational)

```java
class BoundedBuffer {
    private final int[] buffer;
    private int count = 0, putIndex = 0, takeIndex = 0;

    BoundedBuffer(int capacity) {
        buffer = new int[capacity];
    }

    public synchronized void put(int item) throws InterruptedException {
        while (count == buffer.length) {
            wait();   // buffer full — wait for consumer to take
        }
        buffer[putIndex] = item;
        putIndex = (putIndex + 1) % buffer.length;  // circular buffer
        count++;
        notifyAll();  // wake up consumers waiting for data
    }

    public synchronized int take() throws InterruptedException {
        while (count == 0) {
            wait();   // buffer empty — wait for producer to put
        }
        int item = buffer[takeIndex];
        takeIndex = (takeIndex + 1) % buffer.length;
        count--;
        notifyAll();  // wake up producers waiting for space
        return item;
    }
}
```

---

# 15. Common Concurrency Patterns

## Thread-Safe Singleton

```java
// Enum Singleton — simplest and most robust
public enum AppConfig {
    INSTANCE;

    private final Map<String, String> config = new HashMap<>();

    public String get(String key) { return config.get(key); }
    public void set(String key, String value) { config.put(key, value); }
}

// Usage: AppConfig.INSTANCE.get("db.url")
```

## Thread-Local Storage

Each thread gets its own copy of the variable — no sharing, no synchronization needed:

```java
// Classic use: per-thread database connections, SimpleDateFormat (not thread-safe)
ThreadLocal<SimpleDateFormat> dateFormat = ThreadLocal.withInitial(
    () -> new SimpleDateFormat("yyyy-MM-dd")
);

// In any thread:
String formatted = dateFormat.get().format(new Date());  // thread's own formatter
// CRITICAL: Always remove when done (especially in thread pools — threads are reused!)
dateFormat.remove();

// Real-world: Spring uses ThreadLocal for request context, security context
```

## Immutable Objects — Thread Safety by Design

```java
// Immutable = no setters, all fields final, no mutable state shared
public final class Money {
    private final long amountInCents;
    private final String currency;

    public Money(long amountInCents, String currency) {
        this.amountInCents = amountInCents;
        this.currency = currency;
    }

    public Money add(Money other) {
        // Returns new object — doesn't modify 'this'
        return new Money(this.amountInCents + other.amountInCents, currency);
    }

    // Only getters, no setters
    public long getAmountInCents() { return amountInCents; }
    public String getCurrency() { return currency; }
}
// Immutable objects can be freely shared between threads — no synchronization needed
```

## Publish-Subscribe with ExecutorService

```java
class EventBus {
    private final Map<Class<?>, List<Consumer<Object>>> handlers = new ConcurrentHashMap<>();
    private final ExecutorService executor = Executors.newCachedThreadPool();

    @SuppressWarnings("unchecked")
    public <T> void subscribe(Class<T> eventType, Consumer<T> handler) {
        handlers.computeIfAbsent(eventType, k -> new CopyOnWriteArrayList<>())
                .add((Consumer<Object>) handler);
    }

    public void publish(Object event) {
        List<Consumer<Object>> subscribers = handlers.get(event.getClass());
        if (subscribers != null) {
            for (Consumer<Object> handler : subscribers) {
                executor.submit(() -> handler.accept(event));  // async delivery
            }
        }
    }
}
```

---

# 16. Interview Quick Reference

## Thread Creation Summary

| Method | Returns | Can throw? | Use when |
|--------|---------|-----------|---------|
| `extends Thread` | void | No checked | Simple, one-off |
| `implements Runnable` | void | No checked | Preferred for tasks |
| `implements Callable` | value | Yes | Need return value or checked exceptions |
| `ExecutorService.submit` | Future | Yes (in get()) | Production code |

## Concurrency Tool Cheat Sheet

| Problem | Tool |
|---------|------|
| Shared mutable state | `synchronized` or `ReentrantLock` |
| Simple flag across threads | `volatile` |
| Thread-safe counter | `AtomicInteger` / `LongAdder` |
| Thread-safe map | `ConcurrentHashMap` |
| Producer-consumer | `BlockingQueue` |
| Wait for N events | `CountDownLatch` |
| Synchronize N threads at point | `CyclicBarrier` |
| Limit resource access | `Semaphore` |
| Async result | `CompletableFuture` |
| Divide-and-conquer | `ForkJoinPool` |
| Per-thread state | `ThreadLocal` |

## Key Interview Questions

- **Q: What is the difference between `wait()` and `sleep()`?**
  A: `sleep()` pauses the current thread for a time but does NOT release any locks it holds. `wait()` releases the intrinsic lock and enters WAITING state until `notify()`/`notifyAll()` is called. `sleep()` is a Thread method; `wait()` is an Object method and must be called within `synchronized`.

- **Q: What is the difference between `notify()` and `notifyAll()`?**
  A: `notify()` wakes one arbitrary thread waiting on the object. `notifyAll()` wakes all of them — they then compete for the lock. Prefer `notifyAll()` to avoid the case where the wrong thread is woken (e.g., all waiting threads are producers, but you wake one producer when you need a consumer woken).

- **Q: What is a ThreadLocal?**
  A: A variable where each thread has its own independent copy — no sharing, no synchronization. Used for per-thread context (DB connections, security contexts, date formatters). Critical: always call `remove()` when done, especially in thread pools where threads are reused.

- **Q: Difference between `submit()` and `execute()` in ExecutorService?**
  A: `execute(Runnable)` is fire-and-forget — no way to check completion or get result. `submit(Runnable/Callable)` returns a `Future` — you can check status, get result (blocking), handle exceptions, and cancel.

- **Q: What is the difference between `ReentrantLock` and `synchronized`?**
  A: Both provide mutual exclusion and reentrancy. `ReentrantLock` adds: `tryLock()` (non-blocking), timeout, interruptible waiting, fairness mode, multiple Condition variables per lock, and monitoring/diagnostics. `synchronized` is simpler (auto-released on exit) but less flexible.

- **Q: What is CompletableFuture and why is it better than Future?**
  A: `CompletableFuture` supports non-blocking callback chains (thenApply, thenCompose), combining multiple futures (allOf, anyOf), exception handling (exceptionally, handle), and doesn't require blocking `get()` calls. Regular `Future` only provides `get()` which blocks, with no way to register callbacks.

- **Q: What causes a deadlock and how do you prevent it?**
  A: Deadlock requires all four: mutual exclusion, hold-and-wait, no preemption, circular wait. Prevent by: consistent lock ordering, using `tryLock()` with timeout, avoiding holding multiple locks, or redesigning to use single locks or lock-free structures.

---

*End of Part 6: Java Multithreading & Concurrency*
*Next: Part 7 (REST APIs & Backend Engineering)*