# Complete CS Fundamentals, Java, and Backend Engineering Mastery Guide

Audience: a C++ programmer who already knows Data Structures and Algorithms and wants deep interview-ready understanding of operating systems, DBMS, OOP, Java, concurrency, REST APIs, and backend engineering.

How to use this guide:

- Read concepts for understanding, not memorization.
- For interviews, practice explaining: "what problem does this solve?", "what are the tradeoffs?", "what happens internally?", and "what breaks at scale?"
- Compare every abstraction with what you already know in C++.
- Implement the code samples yourself and alter edge cases.

---

## Part 1: Operating Systems

### 1.1 What Is An Operating System?

An Operating System is system software that manages hardware resources and provides abstractions to user programs.

Without an OS, every program would need to know how to:

- Talk directly to disks, keyboards, screens, network cards, and memory controllers.
- Decide which program gets the CPU.
- Prevent one program from corrupting another program.
- Recover from hardware interrupts.
- Handle files, permissions, and devices.

The OS provides:

- Process abstraction: a running program with its own execution context.
- Virtual memory: each process sees a private address space.
- File abstraction: persistent byte streams and directories.
- System calls: controlled entry points into kernel services.
- Scheduling: fair and efficient CPU sharing.
- Protection: user programs cannot arbitrarily access kernel memory or other processes.

High-level view:

```text
+-------------------------------+
| User Applications             |
| browser, shell, JVM, database |
+---------------+---------------+
                |
                | system calls
                v
+---------------+---------------+
| Kernel                        |
| scheduler, memory, FS, IPC    |
+---------------+---------------+
                |
                v
+---------------+---------------+
| Hardware                      |
| CPU, RAM, disk, NIC, devices  |
+-------------------------------+
```

Interview focus:

- OS is a resource manager and abstraction provider.
- Kernels enforce isolation and provide safe access to hardware.
- Performance and correctness often conflict: caching improves speed but complicates consistency.

Common questions:

- What happens when a program reads a file?
- Why do we need system calls?
- Why can a user program not directly modify page tables?

Follow-ups:

- Difference between monolithic kernels and microkernels.
- Why Linux is considered monolithic but modular.

### 1.2 User Space Vs Kernel Space

Modern CPUs support privilege levels. User programs run in a restricted mode. The kernel runs in privileged mode.

User space:

- Runs application code.
- Cannot execute privileged CPU instructions.
- Cannot directly access device registers or arbitrary physical memory.
- Crashes usually kill only the process.

Kernel space:

- Runs OS kernel code.
- Can access hardware and memory management structures.
- A bug can crash the whole system.

Transition:

```text
User program
   |
   | read(fd, buf, n)
   v
libc wrapper
   |
   | syscall instruction / trap
   v
Kernel system call handler
   |
   | validate args, check permissions, perform operation
   v
return to user mode
```

Internal working:

1. Program calls a library function such as `read`.
2. Library places syscall number and arguments into registers.
3. CPU executes a special instruction such as `syscall`.
4. CPU switches to kernel mode and jumps to a registered kernel entry point.
5. Kernel validates user pointers and permissions.
6. Kernel performs the operation.
7. CPU returns to user mode.

Real-world example:

- A Java `FileInputStream.read()` eventually invokes native code and a kernel `read`-like syscall.

Common mistakes:

- Thinking every library call is a system call. Many are pure user-space functions.
- Thinking kernel space means a different physical memory chip. It is a privileged address region/mode.

Interview questions:

- Why is crossing user/kernel boundary expensive?
- What happens if a user process passes an invalid pointer to a syscall?

### 1.3 Programs, Processes, And Threads

Program:

- Passive executable file on disk.
- Example: `chrome.exe`, `/bin/ls`, a compiled Java class/JAR plus JVM.

Process:

- Active running instance of a program.
- Has virtual address space, open file descriptors, registers, stack, heap, permissions, environment.

Thread:

- Execution path inside a process.
- Shares process memory and resources with other threads.
- Has its own stack, registers, program counter, and thread-local state.

```text
Process
+--------------------------------------------------+
| Code | Heap | Globals | File descriptors          |
|                                                  |
| Thread A: PC, registers, stack                   |
| Thread B: PC, registers, stack                   |
| Thread C: PC, registers, stack                   |
+--------------------------------------------------+
```

C++ comparison:

- `std::thread` creates an OS thread in most implementations.
- Threads share address space, so unsynchronized shared data causes undefined behavior/data races.

Java comparison:

- `Thread` maps to platform threads in classic JVM implementations.
- Virtual threads in modern Java are lightweight JVM-managed threads scheduled over carrier OS threads.

Interview questions:

- Why are threads cheaper than processes?
- Why are processes safer than threads?
- What resources are shared between threads?

### 1.4 Process States

Typical states:

```text
             admitted
 New -----------------> Ready
                        |
                        | scheduler dispatch
                        v
                     Running
                    /   |    \
          I/O wait /    |exit \ interrupt/time slice
                  v     v      v
               Waiting Terminated Ready
                  |
                  | I/O complete
                  v
                Ready
```

States:

- New: process is being created.
- Ready: loaded and waiting for CPU.
- Running: currently executing on CPU.
- Waiting/Blocked: waiting for I/O, lock, event, child process, signal.
- Terminated: finished or killed.

Linux-specific note:

- Linux exposes states such as running, sleeping, uninterruptible sleep, stopped, zombie.
- A zombie is a terminated process whose exit status has not been collected by its parent using `wait`.

Common questions:

- Can a process go directly from waiting to running? Usually no; it becomes ready first.
- What is a zombie process?
- What is an orphan process?

### 1.5 Process Control Block

The PCB is a kernel data structure representing a process.

Contains:

- Process ID.
- Process state.
- Program counter and CPU registers.
- Scheduling priority and accounting.
- Memory management info: page tables, address space metadata.
- Open files.
- Signal handlers/masks.
- Parent/child relationships.
- Credentials and permissions.

During context switch:

```text
Save current CPU registers -> current PCB
Choose next process
Load next process registers <- next PCB
Switch page table/address space if needed
Resume execution
```

Interview questions:

- Why does the OS need a PCB?
- Which PCB fields are needed for context switching?

### 1.6 CPU Scheduling

CPU scheduling chooses which ready process/thread runs next.

Metrics:

- CPU utilization: keep CPU busy.
- Throughput: completed jobs per unit time.
- Turnaround time: finish time - arrival time.
- Waiting time: time spent in ready queue.
- Response time: first response - arrival.
- Fairness: avoid starvation.

Algorithms:

#### FCFS: First Come First Served

- Non-preemptive.
- Simple queue.
- Bad for short jobs behind long jobs.

Convoy effect:

```text
Long CPU-bound job arrives first:
[Long 100ms][Short 2ms][Short 2ms][Short 2ms]
Short jobs wait unnecessarily.
```

#### SJF: Shortest Job First

- Runs job with shortest CPU burst.
- Optimal average waiting time if burst times are known.
- Unrealistic because future CPU burst is not exactly known.
- Can starve long jobs.

#### SRTF: Shortest Remaining Time First

- Preemptive SJF.
- If a new job has shorter remaining time, preempt current job.

#### Round Robin

- Preemptive.
- Each process gets a time quantum.
- Good for time-sharing.
- Quantum too small: too many context switches.
- Quantum too large: becomes FCFS-like.

```text
Ready queue: P1 P2 P3
Quantum: 4ms
CPU: P1(4) -> P2(4) -> P3(4) -> P1(4) ...
```

#### Priority Scheduling

- Highest priority runs first.
- Can be preemptive or non-preemptive.
- Starvation solved by aging: gradually increase priority of waiting tasks.

#### Multilevel Queue

- Separate queues for classes of processes.
- Example: foreground interactive, background batch, system processes.

#### Multilevel Feedback Queue

- Processes move between queues based on behavior.
- Interactive tasks that block often may stay high priority.
- CPU-heavy tasks may move lower.

Real-world:

- Linux CFS attempts fair CPU distribution using virtual runtime.
- Production scheduling considers CPU affinity, NUMA, real-time priority, cgroups, power management.

Interview questions:

- Why is Round Robin good for interactive systems?
- What is starvation and how does aging solve it?
- What scheduler would you choose for batch jobs?

### 1.7 Context Switching

A context switch saves the state of one execution context and restores another.

Switch types:

- Process switch: may change address space/page tables.
- Thread switch in same process: same address space, cheaper.
- Mode switch: user to kernel; not always a full context switch.

Costs:

- Saving/restoring registers.
- Scheduler overhead.
- Cache/TLB pollution.
- Possible page table switch.

Common misconception:

- "Context switch is always bad." It is necessary for fairness, I/O overlap, and responsiveness. Excessive switching is bad.

Interview questions:

- Why is switching between threads cheaper than between processes?
- How can too many threads hurt performance?

### 1.8 Threads And Multithreading Models

User threads:

- Managed by user-space runtime.
- Kernel may not know each user thread.
- Fast to create/switch.
- Blocking syscall can block the whole process in many-to-one models.

Kernel threads:

- Managed by OS.
- Can run on multiple cores.
- Syscall blocking affects only that thread.
- More overhead.

Models:

```text
Many-to-One:
User T1 T2 T3 -> one kernel thread

One-to-One:
User T1 -> Kernel K1
User T2 -> Kernel K2

Many-to-Many:
Many user threads multiplexed over many kernel threads
```

Java:

- Traditional Java threads are one-to-one OS threads.
- Virtual threads are many virtual threads scheduled over fewer carrier threads.

Interview questions:

- What happens if one user thread blocks in a many-to-one model?
- Why are virtual threads useful for I/O-heavy servers?

### 1.9 Synchronization

Synchronization coordinates access to shared mutable state.

Race condition:

- Program output depends on timing/interleaving.

Example:

```java
counter++; // not atomic
```

Internally:

```text
load counter
add 1
store counter
```

Two threads can both load `5`, add, and both store `6`.

Critical section problem:

- Mutual exclusion: only one thread in critical section.
- Progress: if no one is inside, some waiting thread can enter.
- Bounded waiting: no thread waits forever.

Mutex:

- Lock with ownership.
- One thread enters, owner unlocks.

Semaphore:

- Counter controlling permits.
- Binary semaphore can act like mutex, but ownership semantics differ.
- Counting semaphore models limited resources such as DB connections.

Monitor:

- Higher-level construct combining mutual exclusion and condition variables.
- Java `synchronized` methods/blocks use intrinsic monitor locks.

Java monitor example:

```java
class BoundedBuffer<T> {
    private final Queue<T> q = new ArrayDeque<>();
    private final int capacity;

    BoundedBuffer(int capacity) {
        this.capacity = capacity;
    }

    public synchronized void put(T item) throws InterruptedException {
        while (q.size() == capacity) {
            wait();
        }
        q.add(item);
        notifyAll();
    }

    public synchronized T take() throws InterruptedException {
        while (q.isEmpty()) {
            wait();
        }
        T item = q.remove();
        notifyAll();
        return item;
    }
}
```

Why `while`, not `if`:

- Spurious wakeups.
- Another thread may consume the condition before this thread resumes.

Interview questions:

- Difference between mutex and semaphore.
- Why can `counter++` be unsafe?
- Why should condition waits use loops?

### 1.10 Deadlocks

Deadlock occurs when a set of processes/threads wait forever for each other.

Coffman conditions:

1. Mutual exclusion.
2. Hold and wait.
3. No preemption.
4. Circular wait.

Example:

```text
Thread A holds Lock 1, waits for Lock 2
Thread B holds Lock 2, waits for Lock 1
```

Handling:

- Prevention: break one Coffman condition.
- Avoidance: allocate only if system remains safe, e.g. Banker's algorithm.
- Detection and recovery: find cycles, kill/rollback.
- Practical engineering: lock ordering, timeouts, smaller critical sections.

Java lock ordering:

```java
void transfer(Account from, Account to, int amount) {
    Account first = from.id < to.id ? from : to;
    Account second = from.id < to.id ? to : from;

    synchronized (first) {
        synchronized (second) {
            from.withdraw(amount);
            to.deposit(amount);
        }
    }
}
```

Interview questions:

- List the four deadlock conditions.
- How do you prevent deadlock in money transfer?
- Difference between deadlock, livelock, starvation.

### 1.11 Memory Management

Goals:

- Allocate memory to processes.
- Protect process memory.
- Support virtual memory.
- Efficiently use RAM.
- Allow sharing when safe.

Address types:

- Logical/virtual address: generated by program.
- Physical address: actual RAM location.
- MMU translates virtual to physical.

```text
CPU virtual address -> MMU -> physical address -> RAM
                     uses page table/TLB
```

#### Paging

Virtual memory divided into fixed-size pages. Physical memory divided into frames.

```text
Virtual pages:  V0 V1 V2 V3
Page table:     V0->F5, V1->F2, V2->disk, V3->F8
Physical RAM:   F0 F1 F2 F3 F4 F5 ...
```

Benefits:

- Avoids external fragmentation.
- Supports non-contiguous allocation.
- Enables virtual memory and protection.

Costs:

- Page table memory overhead.
- Address translation overhead.
- Internal fragmentation in last page.

Page table entry may contain:

- Frame number.
- Present/valid bit.
- Protection bits.
- Dirty bit.
- Accessed/reference bit.
- Caching flags.

#### Segmentation

Memory divided into logical segments such as code, stack, heap.

Each segment has base and limit.

Pros:

- Matches programmer's logical view.
- Fine-grained protection/sharing.

Cons:

- External fragmentation.
- More complex allocation.

Modern systems often combine segmentation concepts with paging, but paging dominates general-purpose memory management.

#### Virtual Memory And Demand Paging

Virtual memory lets processes use more address space than physical RAM.

Demand paging:

- Load a page into RAM only when accessed.
- If page not present, CPU triggers page fault.
- Kernel loads page from disk or creates zero page.
- Process resumes.

Page fault flow:

```text
Access virtual page
   |
PTE present? no
   |
CPU trap to kernel
   |
valid access? no -> segmentation fault
   |
find free frame or evict victim
   |
load page from disk / zero-fill
   |
update page table and TLB
   |
restart instruction
```

#### TLB

Translation Lookaside Buffer is a CPU cache for virtual-to-physical translations.

Without TLB:

- Every memory access needs page table walk, often multiple memory reads.

With TLB:

- Most translations are cached.

TLB miss:

- Hardware or OS performs page table walk.
- Entry inserted into TLB.

Context switch concern:

- TLB entries may belong to old address space.
- OS may flush TLB or use address space identifiers.

#### Thrashing

Thrashing occurs when system spends more time paging than executing.

Causes:

- Too many active processes.
- Working sets exceed physical memory.
- Poor locality.

Symptoms:

- High disk I/O.
- Low CPU utilization.
- Severe latency.

Solutions:

- Reduce multiprogramming level.
- Add RAM.
- Improve locality.
- Tune memory limits.

Interview questions:

- What happens on a page fault?
- Difference between internal and external fragmentation.
- Why does TLB improve performance?
- What is copy-on-write?

### 1.12 File Systems

A file system organizes persistent data.

Core abstractions:

- File: named sequence of bytes plus metadata.
- Directory: mapping from names to files/directories.
- Inode: metadata structure in Unix-like systems.
- File descriptor: process-local integer handle for an open file.

Inode contains:

- File type.
- Permissions.
- Owner/group.
- Size.
- Timestamps.
- Pointers to data blocks.
- Link count.

Open file flow:

```text
path "/home/a/x.txt"
   |
parse directories
   |
find inode
   |
check permissions
   |
create open-file table entry
   |
return fd to process
```

Hard link vs soft link:

- Hard link: another directory entry pointing to same inode.
- Soft link/symlink: separate file containing target path.

Common mistakes:

- Deleting a file name does not necessarily delete data immediately if links or open file descriptors remain.
- `fsync` matters when durability is required; `write` may only update page cache.

Interview questions:

- What is an inode?
- What happens when you delete an open file?
- Difference between file descriptor and inode.

### 1.13 Disk Scheduling

Classic spinning disk scheduling minimizes seek time.

Algorithms:

- FCFS: simple but inefficient.
- SSTF: shortest seek time first; may starve far requests.
- SCAN: elevator algorithm moves in one direction then reverses.
- C-SCAN: circular scan; provides more uniform wait.
- LOOK/C-LOOK: like SCAN/C-SCAN but only go as far as last request.

Modern note:

- SSDs do not have mechanical seek, but I/O schedulers still matter for batching, fairness, and write behavior.

Interview questions:

- Why is SCAN called elevator algorithm?
- Are disk scheduling algorithms still relevant for SSDs?

### 1.14 System Calls

System calls are controlled kernel service entry points.

Categories:

- Process: `fork`, `exec`, `wait`, `exit`.
- File: `open`, `read`, `write`, `close`.
- Memory: `mmap`, `brk`.
- IPC: `pipe`, shared memory, sockets.
- Signals: `kill`, signal handling.

#### Fork, Exec, Wait

`fork`:

- Creates child process.
- Child is near-copy of parent.
- Returns child PID to parent, `0` to child.
- Usually implemented efficiently with copy-on-write pages.

`exec`:

- Replaces current process image with new program.
- PID remains same.

`wait`:

- Parent collects child exit status.
- Prevents zombie accumulation.

Shell command flow:

```text
shell
 |
 | fork()
 +--> child: exec("ls")
 |
 +--> parent: wait(child)
```

#### Signals

Signals are asynchronous notifications.

Examples:

- `SIGINT`: Ctrl+C.
- `SIGTERM`: polite termination request.
- `SIGKILL`: cannot be caught; force kill.
- `SIGCHLD`: child changed state.

Common issue:

- Signal handlers must be careful because they interrupt normal execution.

#### IPC

Inter-process communication options:

- Pipes: unidirectional byte stream, often parent-child.
- Named pipes/FIFOs: pipe with file-system name.
- Message queues: structured messages.
- Shared memory: fastest but needs synchronization.
- Sockets: local or network communication.
- Signals: lightweight notifications.

Interview questions:

- Why `fork` then `exec`?
- What is copy-on-write?
- Difference between pipe and socket.

### 1.15 Linux Process Model

Linux treats processes and threads as tasks internally.

Important ideas:

- `fork()` creates a new process.
- `clone()` can create tasks sharing selected resources.
- Threads are tasks sharing address space, file descriptors, and signal handlers.
- `/proc` exposes process information.
- `init`/`systemd` adopts orphans.
- Zombies remain until parent waits.

Linux process relationships:

```text
systemd(1)
  |
  +-- shell
        |
        +-- java process
              |
              +-- JVM threads
```

Interview questions:

- How are Linux threads represented?
- What is `/proc`?
- What is a zombie and how do you clear it?

---

## Part 2: DBMS

### 2.1 DBMS Architecture

A DBMS stores, retrieves, secures, and manages data.

Typical architecture:

```text
Client
  |
SQL parser
  |
Query optimizer
  |
Query executor
  |
Storage engine
  |
Buffer manager ---- Disk files
  |
Transaction manager / lock manager / log manager
```

Components:

- Parser: validates SQL syntax and builds parse tree.
- Optimizer: chooses execution plan.
- Executor: runs plan operators.
- Storage engine: manages pages, indexes, records.
- Buffer pool: caches disk pages in memory.
- Transaction manager: ACID, isolation.
- Log manager: write-ahead logging for recovery.

Real-world:

- PostgreSQL, MySQL/InnoDB, Oracle, SQL Server each implement these differently.

Interview questions:

- Why does a DBMS need a buffer pool if OS has page cache?
- What is query optimization?
- Why is logging needed?

### 2.2 RDBMS

Relational databases model data as relations/tables.

Terms:

- Relation: table.
- Tuple: row.
- Attribute: column.
- Schema: structure.
- Domain: allowed values.

Example:

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
```

Relational strengths:

- Declarative SQL.
- Strong consistency.
- Joins.
- Constraints.
- Mature indexing and transactions.

Common mistake:

- Treating SQL tables as spreadsheets. Tables should represent entities/relationships with constraints.

### 2.3 Keys And Constraints

Keys:

- Super key: any attribute set uniquely identifying rows.
- Candidate key: minimal super key.
- Primary key: chosen candidate key.
- Alternate key: candidate key not chosen.
- Foreign key: references primary/candidate key in another table.
- Composite key: key with multiple columns.
- Surrogate key: artificial key, e.g. auto-increment ID.
- Natural key: meaningful real-world key, e.g. email or SSN.

Constraints:

- `NOT NULL`.
- `UNIQUE`.
- `PRIMARY KEY`.
- `FOREIGN KEY`.
- `CHECK`.
- `DEFAULT`.

Example:

```sql
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('NEW', 'PAID', 'CANCELLED')),
    total_cents BIGINT NOT NULL CHECK (total_cents >= 0),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

Edge cases:

- `UNIQUE` often allows multiple `NULL`s depending on DB.
- Foreign keys can cascade, restrict, set null, or set default on delete/update.
- Composite foreign keys must match referenced columns.

Interview questions:

- Primary key vs unique key.
- Surrogate vs natural key tradeoffs.
- Why enforce constraints in DB if app validates?

### 2.4 ER Modeling

ER modeling maps real-world entities and relationships.

Entities:

- User.
- Order.
- Product.

Relationships:

- One-to-one.
- One-to-many.
- Many-to-many.

Example:

```text
User 1 ---- * Order * ---- * Product
                  |
                  v
             OrderItem
```

Many-to-many requires junction table:

```sql
CREATE TABLE order_items (
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price_cents BIGINT NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

Interview questions:

- How do you model many-to-many?
- When should a relationship become an entity?
- How do you store historical price in orders?

### 2.5 Normalization

Normalization reduces redundancy and update anomalies.

Anomalies:

- Insert anomaly: cannot insert fact without unrelated data.
- Update anomaly: same fact stored in multiple places becomes inconsistent.
- Delete anomaly: deleting one row removes unrelated fact.

#### 1NF

Rules:

- Atomic columns.
- No repeating groups.
- Rows identifiable.

Bad:

```text
student_id | phones
1          | 111,222
```

Good:

```text
student_id | phone
1          | 111
1          | 222
```

#### 2NF

Requires 1NF and no partial dependency on part of a composite key.

Bad:

```text
(student_id, course_id) -> student_name, course_name, grade
student_id -> student_name
course_id -> course_name
```

Split student and course data.

#### 3NF

Requires 2NF and no transitive dependency of non-key attributes.

Bad:

```text
employee_id -> department_id
department_id -> department_name
```

`department_name` belongs in department table.

#### BCNF

For every functional dependency `X -> Y`, `X` must be a super key.

BCNF is stricter than 3NF.

#### 4NF

Deals with independent multivalued dependencies.

Example:

- Student has multiple skills.
- Student has multiple hobbies.
- Skills and hobbies independent.

Do not store all combinations in one table.

#### 5NF

Deals with join dependencies where data can be reconstructed from smaller projections without loss.

Rare in daily interviews, but important conceptually: decompose when facts are truly independent and reconstructable.

#### Denormalization

Intentional redundancy for performance.

Examples:

- Store `order_total_cents` instead of summing items each time.
- Store comment count on post.
- Materialized views.

Tradeoffs:

- Faster reads.
- More complex writes.
- Risk of inconsistency.

Interview questions:

- Explain normalization with examples.
- Difference between 3NF and BCNF.
- When would you denormalize?

### 2.6 Transactions And ACID

Transaction:

- Logical unit of work that either fully succeeds or fails.

ACID:

- Atomicity: all or nothing.
- Consistency: preserves constraints/invariants.
- Isolation: concurrent transactions appear controlled/serializable depending on level.
- Durability: committed data survives crashes.

Bank transfer:

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

If crash after debit before credit, atomicity/recovery should undo or complete consistently.

Write-ahead logging:

- Log change before applying it to data page.
- On crash, DB replays committed changes and undoes uncommitted ones.

Interview questions:

- Which ACID property prevents partial transfer?
- How does durability work?
- Can consistency be guaranteed by DB alone?

### 2.7 Isolation Levels

Concurrency anomalies:

- Dirty read: read uncommitted data.
- Non-repeatable read: same row read twice gives different value.
- Phantom read: same predicate query returns different set of rows.
- Lost update: concurrent writes overwrite each other.
- Write skew: transactions read overlapping data and write disjoint rows, violating invariant.

Isolation levels:

```text
Read Uncommitted: dirty reads possible
Read Committed: no dirty reads
Repeatable Read: same row stable; phantom behavior DB-dependent
Serializable: equivalent to serial execution
```

Example lost update:

```text
T1 reads balance 100
T2 reads balance 100
T1 writes 90
T2 writes 80
Expected 70, actual 80
```

Fixes:

- Row locks: `SELECT ... FOR UPDATE`.
- Optimistic version column.
- Atomic update: `UPDATE accounts SET balance = balance - 10 WHERE id = ?`.
- Serializable isolation.

Interview questions:

- Dirty vs non-repeatable vs phantom read.
- Why is serializable expensive?
- What is optimistic locking?

### 2.8 Concurrency Control, Locking, 2PL, Deadlocks

Lock types:

- Shared/read lock: many readers.
- Exclusive/write lock: one writer.
- Intention locks: indicate locks lower in hierarchy.
- Row, page, table locks.
- Gap/next-key locks: protect ranges.

Two Phase Locking:

- Growing phase: acquire locks, release none.
- Shrinking phase: release locks, acquire none.
- Strict 2PL holds write locks until commit, improving recoverability.

```text
Growing:  lock A, lock B
Shrinking: unlock B, unlock A
```

Deadlock example:

```text
T1 locks row A, waits for B
T2 locks row B, waits for A
```

DB handling:

- Detect wait-for graph cycle.
- Abort one transaction.
- Return deadlock error to application.

Application rule:

- Always retry transactions that fail due to deadlock or serialization failure if operation is idempotently retryable.

Interview questions:

- What is 2PL?
- Difference between deadlock and lock wait timeout.
- How do databases detect deadlocks?

### 2.9 Indexing And B+ Trees

Index:

- Auxiliary data structure that speeds lookup at cost of storage and write overhead.

B+ tree:

- Balanced tree.
- Internal nodes store keys and child pointers.
- Leaf nodes store keys plus row references or data.
- Leaves linked for range scans.

```text
              [30 | 60]
             /    |     \
        [10 20] [40 50] [70 80 90]
          <------ linked leaves ------>
```

Why B+ trees for DBs:

- High fanout reduces height.
- Disk/page friendly.
- Efficient equality and range queries.
- Ordered traversal.

Hash index:

- Fast equality.
- Poor range queries.

Composite index:

```sql
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);
```

Useful for:

- `WHERE user_id = ?`
- `WHERE user_id = ? ORDER BY created_at`
- sometimes range on `created_at` after equality on `user_id`

Less useful for:

- `WHERE created_at = ?` without `user_id` due to leftmost prefix rule.

Covering index:

- Query can be satisfied from index alone.

Index downsides:

- Slower inserts/updates/deletes.
- More disk.
- Bad selectivity may not help.
- Too many indexes confuse/slow writes.

Interview questions:

- Why B+ tree over binary tree?
- Clustered vs non-clustered index.
- What is leftmost prefix?
- Why might DB ignore an index?

### 2.10 Query Optimization And Execution

SQL is declarative: you specify what, not how.

Optimizer chooses:

- Join order.
- Join algorithms.
- Index usage.
- Scan type.
- Predicate pushdown.
- Aggregation strategy.

Common operators:

- Sequential scan.
- Index scan.
- Nested loop join.
- Hash join.
- Merge join.
- Sort.
- Aggregate.

Join algorithms:

Nested loop:

- Good when outer small and inner indexed.

Hash join:

- Build hash table on smaller input, probe larger.
- Good for equality joins.

Merge join:

- Both inputs sorted by join key.
- Good for large sorted data.

Execution example:

```sql
SELECT u.email, COUNT(*) AS order_count
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE o.status = 'PAID'
GROUP BY u.email;
```

Logical order:

1. FROM/JOIN.
2. WHERE.
3. GROUP BY.
4. HAVING.
5. SELECT.
6. ORDER BY.
7. LIMIT.

Possible physical plan:

```text
Index scan orders(status='PAID')
  -> hash by user_id
Seq/index scan users
  -> hash join
  -> aggregate by email
```

Interview questions:

- Logical SQL order vs written order.
- How does optimizer choose index?
- Nested loop vs hash join.

### 2.11 SQL Sample Tables, Queries, Outputs

Sample schema:

```sql
CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    department_id INT,
    salary INT NOT NULL,
    hired_at DATE NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
```

Sample data:

```text
departments
id | name
1  | Engineering
2  | Sales
3  | HR

employees
id | name  | department_id | salary | hired_at
1  | Asha  | 1             | 120000 | 2022-01-10
2  | Ben   | 1             | 90000  | 2023-03-01
3  | Chen  | 2             | 80000  | 2021-07-12
4  | Diya  | NULL          | 70000  | 2024-02-20
```

Inner join:

```sql
SELECT e.name, d.name AS department
FROM employees e
JOIN departments d ON d.id = e.department_id;
```

Output:

```text
name | department
Asha | Engineering
Ben  | Engineering
Chen | Sales
```

`Diya` is excluded because `NULL` does not match.

Left join:

```sql
SELECT e.name, d.name AS department
FROM employees e
LEFT JOIN departments d ON d.id = e.department_id;
```

Output:

```text
name | department
Asha | Engineering
Ben  | Engineering
Chen | Sales
Diya | NULL
```

Aggregation:

```sql
SELECT department_id, COUNT(*) AS n, AVG(salary) AS avg_salary
FROM employees
GROUP BY department_id;
```

Output:

```text
department_id | n | avg_salary
1             | 2 | 105000
2             | 1 | 80000
NULL          | 1 | 70000
```

Window function:

```sql
SELECT
    name,
    department_id,
    salary,
    RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank
FROM employees;
```

Output:

```text
name | department_id | salary | salary_rank
Asha | 1             | 120000 | 1
Ben  | 1             | 90000  | 2
Chen | 2             | 80000  | 1
Diya | NULL          | 70000  | 1
```

Edge cases:

- `COUNT(*)` counts rows; `COUNT(column)` ignores NULL.
- `WHERE` filters before grouping; `HAVING` filters groups.
- `NULL = NULL` is unknown, not true.
- `NOT IN` with NULL can produce surprising empty results; prefer `NOT EXISTS`.

### 2.12 Views, Stored Procedures, Triggers

View:

- Saved query.
- Can simplify access and enforce security boundaries.

```sql
CREATE VIEW high_paid_employees AS
SELECT id, name, salary
FROM employees
WHERE salary >= 100000;
```

Stored procedure:

- Database-side procedural logic.
- Useful for encapsulated operations close to data.
- Can harm portability and hide business logic if overused.

Trigger:

- Runs automatically on insert/update/delete.
- Useful for audit logs and derived fields.
- Dangerous when hidden side effects surprise application developers.

Interview questions:

- View vs materialized view.
- When would you use a trigger?
- Stored procedure pros and cons.

### 2.13 Partitioning, Replication, Sharding

Partitioning:

- Split one logical table into physical parts.

Types:

- Range: by date ranges.
- List: by region/status.
- Hash: by hash of key.

Benefits:

- Partition pruning.
- Easier archival.
- Smaller indexes per partition.

Replication:

- Copies data to multiple nodes.

Types:

- Primary-replica: writes to primary, reads can go to replicas.
- Multi-primary: multiple write nodes; conflict complexity.
- Synchronous: safer, slower.
- Asynchronous: faster, replication lag possible.

Sharding:

- Horizontal partitioning across machines.

Example:

```text
user_id % 4:
0 -> shard A
1 -> shard B
2 -> shard C
3 -> shard D
```

Challenges:

- Cross-shard joins.
- Rebalancing.
- Hot shards.
- Distributed transactions.
- Global secondary indexes.

Interview questions:

- Partitioning vs sharding.
- Replication lag effects.
- How do you choose a shard key?

### 2.14 SQL Vs NoSQL And CAP

SQL:

- Strong schema.
- Relational queries and joins.
- ACID transactions.
- Good for financial/order/inventory systems.

NoSQL categories:

- Key-value: Redis, Dynamo-style systems.
- Document: MongoDB.
- Wide-column: Cassandra.
- Graph: Neo4j.

NoSQL strengths:

- Flexible schema.
- Horizontal scaling.
- Specialized access patterns.

CAP theorem:

In presence of network partition, a distributed system must choose between:

- Consistency: every read sees latest write.
- Availability: every request receives non-error response.

Partition tolerance is not optional in real distributed systems.

Important nuance:

- CAP is about behavior during partitions, not a blanket ranking of databases.
- Systems can provide tunable consistency.

Interview questions:

- Explain CAP with example.
- SQL vs NoSQL tradeoffs.
- When would you choose Cassandra over PostgreSQL?

---

## Part 3: Object-Oriented Programming

### 3.1 OOP From First Principles

OOP organizes software around objects that combine state and behavior.

Core ideas:

- Encapsulation: hide representation.
- Abstraction: expose essential interface.
- Inheritance: reuse/specialize behavior.
- Polymorphism: same interface, different implementations.

Object model:

```text
Class: blueprint
Object: runtime instance

Account class
  fields: balance, owner
  methods: deposit, withdraw

account1, account2 are objects
```

Java vs C++:

- Java objects are accessed through references and allocated on heap conceptually.
- C++ objects can live on stack, heap, static storage, or inside other objects.
- Java has garbage collection; C++ uses deterministic destructors and RAII.

### 3.2 Classes, Objects, Constructors

C++:

```cpp
class Account {
private:
    long balance;
public:
    Account(long initial) : balance(initial) {}
    void deposit(long amount) { balance += amount; }
};

Account a(100);          // stack object
auto p = new Account(5); // heap object, must delete or use smart pointer
```

Java:

```java
class Account {
    private long balance;

    Account(long initial) {
        this.balance = initial;
    }

    void deposit(long amount) {
        balance += amount;
    }
}

Account a = new Account(100); // reference to heap object
```

Constructor purpose:

- Establish class invariants.
- Initialize fields.
- Acquire resources carefully.

Common mistakes:

- Calling overridable methods from constructors.
- Leaving objects partially initialized.
- Confusing Java references with C++ pointers; Java has no pointer arithmetic.

### 3.3 Destructor Vs Garbage Collection

C++ destructor:

- Runs deterministically when object lifetime ends.
- Core of RAII.
- Releases memory, locks, file handles, sockets.

Java GC:

- Reclaims memory automatically when objects become unreachable.
- Does not deterministically release non-memory resources.
- Use `try-with-resources` for deterministic cleanup.

Java:

```java
try (FileInputStream in = new FileInputStream("data.txt")) {
    int b = in.read();
}
```

Interview point:

- GC handles memory, not resource lifetime in general.

### 3.4 Encapsulation And Abstraction

Encapsulation:

- Keep fields private.
- Validate changes through methods.

Abstraction:

- Expose what object does, not how.

Java:

```java
class BankAccount {
    private long balance;

    public void withdraw(long amount) {
        if (amount <= 0 || amount > balance) throw new IllegalArgumentException();
        balance -= amount;
    }
}
```

Bad:

```java
class BankAccount {
    public long balance; // anyone can set negative balance
}
```

Interview questions:

- Why not make all fields public?
- Difference between abstraction and encapsulation.

### 3.5 Inheritance And Polymorphism

Inheritance models an "is-a" relationship.

UML:

```text
       Shape
        ^
        |
   +----+----+
   |         |
 Circle   Rectangle
```

C++:

```cpp
class Shape {
public:
    virtual double area() const = 0;
    virtual ~Shape() = default;
};

class Circle : public Shape {
    double r;
public:
    Circle(double r) : r(r) {}
    double area() const override { return 3.14159 * r * r; }
};
```

Java:

```java
abstract class Shape {
    abstract double area();
}

class Circle extends Shape {
    private final double r;

    Circle(double r) {
        this.r = r;
    }

    @Override
    double area() {
        return Math.PI * r * r;
    }
}
```

Dynamic binding:

- Runtime object type determines overridden method.

Static binding:

- Compile-time resolution, such as overloaded methods, private methods, static methods.

Interview questions:

- Overloading vs overriding.
- Why virtual destructor in C++ base class?
- Is Java dynamic dispatch by default? Instance methods are virtual unless `final`, `private`, or `static` semantics apply.

### 3.6 Overloading Vs Overriding

Overloading:

- Same method name, different parameter list.
- Compile-time resolution.

Java:

```java
void print(int x) {}
void print(String s) {}
```

Overriding:

- Subclass provides implementation of inherited method.
- Runtime dispatch.

Java:

```java
class Animal {
    void speak() { System.out.println("sound"); }
}

class Dog extends Animal {
    @Override
    void speak() { System.out.println("bark"); }
}
```

Edge case:

```java
class Test {
    void f(Object o) { System.out.println("Object"); }
    void f(String s) { System.out.println("String"); }
}

new Test().f(null); // String, because it is more specific
```

### 3.7 Abstract Classes And Interfaces

Abstract class:

- Can hold state.
- Can define constructors.
- Can provide common implementation.
- Single inheritance in Java.

Interface:

- Contract for behavior.
- Java interfaces can have default/static/private methods, but fields are public static final constants.
- A class can implement multiple interfaces.

Java:

```java
interface Payable {
    long amountDue();
}

abstract class Employee implements Payable {
    protected final String name;

    Employee(String name) {
        this.name = name;
    }
}
```

C++:

- Pure abstract base classes often serve as interfaces.

```cpp
class Payable {
public:
    virtual long amountDue() const = 0;
    virtual ~Payable() = default;
};
```

Interview questions:

- Abstract class vs interface.
- Can Java interfaces have method implementations?
- Why does Java avoid multiple class inheritance?

### 3.8 Multiple Inheritance And Diamond Problem

C++ supports multiple inheritance.

Diamond:

```text
    A
   / \
  B   C
   \ /
    D
```

Problem:

- Does `D` contain one `A` subobject or two?
- Which inherited method/field wins?

C++ solution:

- Virtual inheritance.

Java:

- No multiple class inheritance.
- Multiple interfaces allowed.
- If default methods conflict, implementing class must override.

Java conflict:

```java
interface A { default void f() {} }
interface B { default void f() {} }

class C implements A, B {
    @Override
    public void f() {
        A.super.f();
    }
}
```

### 3.9 Composition, Association, Aggregation, Dependency

Composition:

- Strong ownership; part lifetime tied to whole.

```text
House *-- Room
```

Aggregation:

- Weak ownership; part can exist independently.

```text
Team o-- Player
```

Association:

- General relationship.

```text
Teacher -- Student
```

Dependency:

- Temporary usage.

```text
ReportService ..> EmailSender
```

Composition vs inheritance:

- Prefer composition when behavior varies independently.
- Use inheritance for true substitutability.

Interview questions:

- Is `Car extends Engine` correct? No; car has an engine.
- Explain "favor composition over inheritance."

### 3.10 SOLID Principles

Single Responsibility:

- A class should have one reason to change.

Open/Closed:

- Open for extension, closed for modification.

Liskov Substitution:

- Subtypes must be usable wherever base type is expected.
- Do not strengthen preconditions or weaken postconditions.

Interface Segregation:

- Prefer small focused interfaces.

Dependency Inversion:

- High-level modules depend on abstractions, not concrete low-level classes.

Example:

```java
interface PaymentGateway {
    void charge(long cents);
}

class CheckoutService {
    private final PaymentGateway gateway;

    CheckoutService(PaymentGateway gateway) {
        this.gateway = gateway;
    }
}
```

Common mistake:

- Treating SOLID as rules to create many tiny classes. Use them to manage change and dependencies.

### 3.11 Design Patterns

Patterns are reusable design vocabulary.

Creational:

- Factory Method: defer object creation.
- Abstract Factory: families of related objects.
- Builder: construct complex immutable objects.
- Singleton: one instance; often overused.

Structural:

- Adapter: convert interface.
- Decorator: wrap and add behavior.
- Facade: simplify subsystem.
- Proxy: control access.

Behavioral:

- Strategy: interchangeable algorithms.
- Observer: publish/subscribe.
- Command: objectify request.
- Template Method: fixed algorithm skeleton with overridable steps.

Strategy example:

```java
interface PricingStrategy {
    long price(Order order);
}

class RegularPricing implements PricingStrategy {
    public long price(Order order) { return order.subtotal(); }
}

class DiscountPricing implements PricingStrategy {
    public long price(Order order) { return order.subtotal() * 90 / 100; }
}
```

Interview questions:

- Strategy vs State.
- Factory vs Builder.
- Why is Singleton hard to test?

---

## Part 4: Java Complete Course For A C++ Developer

### 4.1 JVM, JDK, JRE, Bytecode

JDK:

- Java Development Kit.
- Compiler, tools, runtime, libraries.

JRE:

- Java Runtime Environment.
- JVM plus standard libraries needed to run Java apps.

JVM:

- Virtual machine executing bytecode.
- Provides class loading, verification, JIT, GC, memory management.

Flow:

```text
MyClass.java --javac--> MyClass.class bytecode --JVM--> machine code
```

Bytecode:

- Platform-independent instruction set.
- Verified before execution for safety.

C++ comparison:

- C++ compiles directly to native machine code for target platform.
- Java compiles to bytecode and JVM compiles/interprets at runtime.

### 4.2 Class Loading

Stages:

1. Loading: find class bytes and create class representation.
2. Linking:
   - Verification: bytecode safety.
   - Preparation: allocate static fields with default values.
   - Resolution: symbolic references to direct references.
3. Initialization: execute static initializers.

Class loaders:

- Bootstrap.
- Platform.
- Application.
- Custom loaders.

Delegation model:

```text
Application loader asks parent first
Platform loader asks parent first
Bootstrap tries core classes
```

Interview questions:

- When is a class initialized?
- Can two classes with same name be different? Yes, if loaded by different class loaders.

### 4.3 JIT Compiler

JVM execution:

- Interpreter starts quickly.
- Hot methods are compiled by JIT to native code.
- Runtime profiling enables optimizations.

Optimizations:

- Inlining.
- Escape analysis.
- Lock elimination.
- Devirtualization.
- Dead code elimination.

Tradeoff:

- JVM may start slower than native C++, but can optimize based on runtime behavior.

### 4.4 Garbage Collection, Heap, Stack, Metaspace

Memory areas:

```text
Thread stack: frames, local variables, operand stack
Heap: objects and arrays
Metaspace: class metadata
Code cache: JIT compiled code
Native memory: JVM and native libraries
```

Object lifecycle:

1. Allocation.
2. Initialization.
3. Use.
4. Becomes unreachable.
5. GC discovers unreachable object.
6. Memory reclaimed.

Generational hypothesis:

- Most objects die young.
- Young generation collection is frequent and fast.
- Long-lived objects promoted to old generation.

GC roots:

- Thread stacks.
- Static fields.
- JNI references.
- JVM internal references.

Reachability:

```text
GC roots -> reachable objects kept
unreachable objects reclaimed
```

Common mistakes:

- Memory leak is still possible in Java if reachable references are retained unnecessarily.
- `System.gc()` is only a request, not a guarantee.

### 4.5 Java Memory Model

The Java Memory Model defines visibility and ordering guarantees between threads.

Problems it addresses:

- CPU caches.
- Compiler reordering.
- Out-of-order execution.

Happens-before examples:

- Unlock happens-before subsequent lock on same monitor.
- Write to volatile happens-before subsequent read of same volatile.
- Thread start happens-before actions in started thread.
- Actions in thread happen-before another thread successfully returns from `join`.

Without happens-before:

- One thread may not see another thread's writes promptly or consistently.

### 4.6 Java Syntax Basics

Variables:

```java
int x = 10;
long y = 10L;
double d = 2.5;
boolean ok = true;
String s = "hello";
```

Primitive types:

- `byte`, `short`, `int`, `long`.
- `float`, `double`.
- `char`.
- `boolean`.

Reference types:

- Classes, interfaces, arrays, enums, records.

Operators:

- Arithmetic: `+ - * / %`.
- Relational: `< <= > >= == !=`.
- Logical: `&& || !`.
- Bitwise: `& | ^ ~ << >> >>>`.

Loops:

```java
for (int i = 0; i < 10; i++) {}
while (condition) {}
do {} while (condition);
for (String item : items) {}
```

Methods:

```java
static int add(int a, int b) {
    return a + b;
}
```

C++ comparison:

- Java has no header files, pointer arithmetic, operator overloading, stack-allocated objects, or multiple class inheritance.
- Java passes arguments by value. Object references are copied by value.

### 4.7 Java Keywords

`class`:

- Defines a reference type with fields, methods, constructors.

`interface`:

- Defines behavior contract; supports default/static/private methods.

`extends`:

- Inherits from a class or extends an interface.

`implements`:

- Class promises to implement interface methods.

`static`:

- Member belongs to class, not instance.
- Static methods are not polymorphically overridden; they are hidden.

`final`:

- Variable cannot be reassigned.
- Method cannot be overridden.
- Class cannot be subclassed.

`abstract`:

- Class cannot be instantiated or method has no body.

`this`:

- Current object reference.

`super`:

- Parent class reference for constructor/method access.

Access modifiers:

- `public`: visible everywhere.
- `private`: visible within class.
- `protected`: package plus subclasses.
- no modifier: package-private.

`package`:

- Namespace and access boundary.

`import`:

- Allows using class names without full qualification.

`synchronized`:

- Acquires monitor lock.
- Provides mutual exclusion and happens-before on unlock/lock.

`volatile`:

- Visibility and ordering for a variable.
- Does not make compound actions atomic.

`transient`:

- Field skipped by Java built-in serialization.

`native`:

- Method implemented in native code through JNI or similar.

`strictfp`:

- Historically forced strict floating-point semantics; less important in modern Java due to standardized FP behavior.

`enum`:

- Type-safe fixed set of constants.

```java
enum Status { NEW, PAID, CANCELLED }
```

`record`:

- Concise immutable data carrier.

```java
record UserDto(long id, String email) {}
```

`sealed`, `non-sealed`, `permits`:

- Restrict which classes can extend a class/interface.

```java
sealed interface Payment permits CardPayment, CashPayment {}
final class CardPayment implements Payment {}
non-sealed class CashPayment implements Payment {}
```

Interview questions:

- `final` vs immutability.
- `volatile` vs `synchronized`.
- `static` method hiding vs overriding.
- Why use records?
- Why use sealed classes?

---

## Part 5: Java Collections Framework

### 5.1 Collection Hierarchy

```text
Iterable
  |
Collection
  |-- List
  |-- Set
  |-- Queue
       |-- Deque

Map is separate:
Map
  |-- HashMap
  |-- LinkedHashMap
  |-- TreeMap
  |-- ConcurrentHashMap
```

Collection:

- Group of elements.

Map:

- Key-value associations; not a subtype of Collection.

### 5.2 List Implementations

#### ArrayList

Internal:

- Resizable array.
- Fast random access.
- Append amortized O(1).
- Insert/delete middle O(n).

Resizing:

- When capacity full, allocate larger array and copy.

Ordering:

- Preserves insertion order.

Thread safety:

- Not synchronized.

C++ comparison:

- Similar to `std::vector`, but stores object references for objects, not objects inline.

Use cases:

- Read-heavy ordered collections.
- Random access.

Common mistake:

- Removing many elements from front repeatedly is O(n) each.

#### LinkedList

Internal:

- Doubly linked list.

Complexities:

- Access by index O(n).
- Add/remove at known node O(1).
- More memory per element.

Also implements Deque.

C++ comparison:

- Similar to `std::list`, but less commonly ideal than people think.

Use cases:

- Queue/deque operations when `ArrayDeque` is not suitable.

#### Vector And Stack

Vector:

- Synchronized legacy resizable array.
- Usually avoid; prefer `ArrayList` plus external synchronization or concurrent collection.

Stack:

- Legacy LIFO extending Vector.
- Prefer `ArrayDeque`.

### 5.3 Queue, Deque, PriorityQueue

Queue:

- FIFO abstraction.

Deque:

- Double-ended queue.

`ArrayDeque`:

- Resizable circular array.
- Excellent stack/queue implementation.

`PriorityQueue`:

- Binary heap.
- Head is least element by natural ordering/comparator.
- Insert O(log n), poll O(log n), peek O(1).
- Iteration order is not sorted.

C++ comparison:

- Java `PriorityQueue` is min-heap by default.
- C++ `std::priority_queue` is max-heap by default.

### 5.4 Map Implementations

#### HashMap

Internal:

- Array of buckets.
- Hash spreads key hash.
- Bucket holds nodes; collisions handled by chaining.
- In modern Java, heavily-collided buckets can treeify into balanced trees when thresholds are met.

Basic layout:

```text
table[0] -> null
table[1] -> (k1,v1) -> (k2,v2)
table[2] -> null
```

Complexities:

- Average get/put/remove O(1).
- Worst-case improved by tree bins under conditions, but do not rely blindly.

Resizing:

- Triggered when size exceeds capacity * load factor.
- Default load factor commonly 0.75.
- Rehash/distribute entries into larger table.

Ordering:

- No guaranteed iteration order.

Thread safety:

- Not thread-safe.

Key requirement:

- If override `equals`, override `hashCode`.
- Equal objects must have same hash code.

Common mistake:

- Mutable keys. If fields used in hash change after insertion, lookup can fail.

#### LinkedHashMap

Internal:

- HashMap plus doubly linked list.

Ordering:

- Insertion order or access order.

Use case:

- LRU cache by overriding `removeEldestEntry`.

#### TreeMap

Internal:

- Red-black tree.

Complexities:

- O(log n) get/put/remove.

Ordering:

- Sorted by natural order or comparator.

C++ comparison:

- Similar role to `std::map`.

#### ConcurrentHashMap

Internal:

- Concurrent hash table with fine-grained synchronization/CAS.
- Allows concurrent reads and updates.
- Does not allow null keys/values.

Iteration:

- Weakly consistent: does not throw ConcurrentModificationException and may reflect some updates.

Use cases:

- Shared maps in concurrent applications.

### 5.5 Set Implementations

`HashSet`:

- Backed by HashMap.
- No order.
- Average O(1).

`LinkedHashSet`:

- Backed by LinkedHashMap.
- Insertion order.

`TreeSet`:

- Backed by TreeMap.
- Sorted order.
- O(log n).

Important:

- TreeSet uniqueness uses comparator/natural ordering. If comparator says two objects compare equal, set treats them as duplicates even if `equals` differs.

### 5.6 Comparable, Comparator, Iterators, Generics

Comparable:

```java
class User implements Comparable<User> {
    final int age;
    public int compareTo(User other) {
        return Integer.compare(this.age, other.age);
    }
}
```

Comparator:

```java
Comparator<User> byName = Comparator.comparing(User::name);
```

Generics:

- Compile-time type safety.
- Implemented mostly by type erasure.

```java
List<String> names = new ArrayList<>();
```

Type erasure consequence:

- Cannot create `new T[]` directly.
- Runtime usually sees raw class, not full generic parameter.

Fail-fast iterator:

- Detects structural modification and throws `ConcurrentModificationException`.
- Best-effort bug detection, not synchronization guarantee.

Fail-safe/weakly consistent:

- Concurrent collections may iterate over snapshot or weakly consistent view.

Interview questions:

- HashMap vs TreeMap vs LinkedHashMap.
- ArrayList vs LinkedList.
- Why override hashCode with equals?
- Why is PriorityQueue iteration not sorted?
- Comparable vs Comparator.

---

## Part 6: Java Multithreading And Concurrency

### 6.1 Thread Lifecycle

States:

```text
NEW -> RUNNABLE -> TERMINATED
          |
          +-> BLOCKED
          +-> WAITING
          +-> TIMED_WAITING
```

Java states:

- NEW: created, not started.
- RUNNABLE: eligible/running.
- BLOCKED: waiting to acquire monitor.
- WAITING: waiting indefinitely.
- TIMED_WAITING: waiting with timeout.
- TERMINATED: done.

### 6.2 Thread Creation

Extending Thread:

```java
class Worker extends Thread {
    public void run() {
        System.out.println("work");
    }
}
```

Runnable:

```java
Thread t = new Thread(() -> System.out.println("work"));
t.start();
```

Callable and Future:

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
Future<Integer> f = pool.submit(() -> 42);
Integer result = f.get();
pool.shutdown();
```

Prefer executor services over manually creating many threads.

### 6.3 Synchronization And Locks

Intrinsic lock:

```java
synchronized (lock) {
    // critical section
}
```

ReentrantLock:

```java
ReentrantLock lock = new ReentrantLock();
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();
}
```

Reentrant means same thread can acquire lock it already owns.

ReentrantLock advantages:

- `tryLock`.
- Interruptible lock acquisition.
- Fairness option.
- Multiple condition variables.

Common mistake:

- Forgetting `unlock` in `finally`.

### 6.4 Deadlock, Starvation, Livelock

Deadlock:

- Threads wait forever for each other.

Starvation:

- Thread cannot make progress because others keep getting resources.

Livelock:

- Threads actively respond to each other but no progress is made.

Example:

- Two people both step aside repeatedly in the same direction.

### 6.5 Volatile, Atomic Classes, Concurrent Collections

`volatile`:

- Guarantees visibility and ordering.
- Good for flags.
- Not enough for compound increments.

```java
volatile boolean running = true;
```

AtomicInteger:

```java
AtomicInteger count = new AtomicInteger();
count.incrementAndGet();
```

CAS:

- Compare current value with expected.
- If equal, atomically update.
- Retry loop if failed.

Concurrent collections:

- `ConcurrentHashMap`.
- `CopyOnWriteArrayList`.
- `BlockingQueue`.

BlockingQueue producer-consumer:

```java
BlockingQueue<String> q = new ArrayBlockingQueue<>(100);
q.put("item");
String item = q.take();
```

### 6.6 Thread Pools And Executors

Why thread pools:

- Reuse threads.
- Bound concurrency.
- Reduce creation overhead.
- Provide task queue.

Executor types:

- Fixed thread pool.
- Cached thread pool.
- Single-thread executor.
- Scheduled executor.
- ForkJoinPool.

Important warning:

- `Executors.newFixedThreadPool` uses an unbounded queue. In production, prefer explicit `ThreadPoolExecutor` with bounded queue and rejection policy.

```java
ThreadPoolExecutor pool = new ThreadPoolExecutor(
    4,
    8,
    30, TimeUnit.SECONDS,
    new ArrayBlockingQueue<>(1000),
    new ThreadPoolExecutor.CallerRunsPolicy()
);
```

### 6.7 Scheduled Executors

```java
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
scheduler.scheduleAtFixedRate(task, 0, 1, TimeUnit.SECONDS);
```

Fixed rate:

- Attempts regular period based on scheduled start time.

Fixed delay:

- Delay counted after previous run finishes.

### 6.8 ForkJoinPool And Parallel Streams

ForkJoin:

- Work-stealing pool for divide-and-conquer tasks.

```java
class SumTask extends RecursiveTask<Long> {
    private final int[] a;
    private final int l, r;

    SumTask(int[] a, int l, int r) {
        this.a = a; this.l = l; this.r = r;
    }

    protected Long compute() {
        if (r - l <= 1000) {
            long sum = 0;
            for (int i = l; i < r; i++) sum += a[i];
            return sum;
        }
        int m = (l + r) >>> 1;
        SumTask left = new SumTask(a, l, m);
        SumTask right = new SumTask(a, m, r);
        left.fork();
        long rv = right.compute();
        return left.join() + rv;
    }
}
```

Parallel streams:

- Easy data parallelism.
- Avoid blocking operations and shared mutable state.
- Uses common ForkJoinPool by default.

### 6.9 CompletableFuture

```java
CompletableFuture<String> user =
    CompletableFuture.supplyAsync(() -> fetchUser())
        .thenApply(u -> u.toUpperCase())
        .exceptionally(ex -> "fallback");
```

Composition:

- `thenApply`: transform result.
- `thenCompose`: flatten async result.
- `thenCombine`: combine independent futures.
- `allOf`: wait for many.

Common mistake:

- Blocking with `get()` too early defeats async composition.

### 6.10 Happens-Before

Examples:

```java
class Holder {
    private int value;
    private volatile boolean ready;

    void publish() {
        value = 42;
        ready = true; // volatile write
    }

    int read() {
        if (ready) {  // volatile read
            return value; // guaranteed visible
        }
        return -1;
    }
}
```

The write to `value` happens-before the volatile write to `ready`; the volatile write happens-before the read of `ready`.

Interview questions:

- `volatile` vs AtomicInteger.
- Why are thread pools preferred?
- How can deadlock happen with `Future.get()`?
- What is happens-before?
- Why is double-checked locking broken without volatile?

---

## Part 7: REST APIs And Backend Engineering Fundamentals

### 7.1 Client-Server Architecture

Client sends request; server processes and responds.

Browser-to-server lifecycle:

```text
User enters URL
  |
DNS resolves domain to IP
  |
TCP connection established
  |
TLS handshake for HTTPS
  |
HTTP request sent
  |
Server/router/controller handles request
  |
Service/business logic
  |
Database/cache calls
  |
HTTP response returned
  |
Browser renders/uses response
```

DNS:

- Resolves names to IP addresses.
- Uses caching at browser, OS, resolver, authoritative servers.

TCP:

- Reliable ordered byte stream.
- Connection setup with handshake.

HTTP:

- Application protocol over TCP/TLS.

### 7.2 HTTP Protocol

Request:

```text
GET /api/users/42 HTTP/1.1
Host: example.com
Accept: application/json
Authorization: Bearer <token>
```

Response:

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"id":42,"name":"Asha"}
```

Status codes:

- 2xx success: `200 OK`, `201 Created`, `204 No Content`.
- 3xx redirection: `301`, `302`, `304`.
- 4xx client error: `400`, `401`, `403`, `404`, `409`, `422`, `429`.
- 5xx server error: `500`, `502`, `503`, `504`.

Headers:

- Metadata such as content type, cache control, auth, cookies.

Cookies:

- Browser-managed key-value data sent to matching domains.
- Can be `HttpOnly`, `Secure`, `SameSite`.

Sessions:

- Server stores session state keyed by session ID, often in cookie.

Authentication:

- Who are you?

Authorization:

- What are you allowed to do?

### 7.3 REST APIs

REST is an architectural style.

Constraints:

- Client-server.
- Stateless.
- Cacheable.
- Uniform interface.
- Layered system.
- Code on demand optional.

Resource-oriented design:

```text
GET    /users          list users
POST   /users          create user
GET    /users/{id}     get user
PUT    /users/{id}     replace user
PATCH  /users/{id}     partially update user
DELETE /users/{id}     delete user
```

Idempotency:

- Repeating request has same effect as once.

Methods:

- GET: safe, idempotent.
- POST: not necessarily idempotent.
- PUT: idempotent replace/create at known URI.
- PATCH: may or may not be idempotent depending design.
- DELETE: idempotent in intended resource state.

Statelessness:

- Each request contains needed context.
- Server does not rely on hidden conversational state.

Common mistakes:

- Using GET for mutation.
- Putting verbs in URIs: `/createUser`.
- Returning `200` for every error.

### 7.4 API Design

Validation:

- Validate syntax and business rules.
- Return helpful errors.

DTOs:

- Data transfer objects separate API shape from domain/persistence models.

Error format:

```json
{
  "error": "VALIDATION_FAILED",
  "message": "email is invalid",
  "field": "email"
}
```

Versioning:

- URI: `/v1/users`.
- Header-based.
- Compatibility-first evolution often better than frequent versioning.

Pagination:

Offset:

```text
GET /orders?limit=20&offset=40
```

Cursor:

```text
GET /orders?limit=20&after=eyJpZCI6...
```

Cursor pagination is better for large changing datasets.

Filtering/sorting:

```text
GET /orders?status=PAID&sort=-createdAt
```

Edge cases:

- Stable sort needed for pagination.
- Validate max page size.
- Do not expose internal DB errors.

### 7.5 JSON And XML

JSON:

- Lightweight.
- Natural fit for web APIs.
- Types: object, array, string, number, boolean, null.

XML:

- Verbose.
- Supports attributes, namespaces, schemas.
- Common in older enterprise integrations.

JSON edge cases:

- Large integers may lose precision in JavaScript clients.
- Dates need consistent format, usually ISO-8601.
- Missing field vs null field can mean different things.

### 7.6 Security

Password hashing:

- Never store plaintext passwords.
- Use slow salted password hashing such as bcrypt, scrypt, or Argon2.

JWT:

- Signed token carrying claims.
- Stateless verification.
- Hard to revoke unless using short expiry or revocation list.

OAuth:

- Delegated authorization framework.
- "Allow app X to access resource Y on my behalf."

CORS:

- Browser security policy controlling cross-origin requests.
- Server sends allowed origins/methods/headers.

CSRF:

- Attack where browser sends authenticated request unintentionally.
- Defenses: SameSite cookies, CSRF tokens, avoid cookie auth for unsafe cross-origin flows.

Security basics:

- Use HTTPS.
- Validate input.
- Use parameterized SQL.
- Enforce authorization on server.
- Rate limit sensitive endpoints.
- Log security events without leaking secrets.

### 7.7 Backend Architecture

Monolith:

- One deployable application.
- Simpler development and transactions.
- Can become large and tightly coupled.

Microservices:

- Independently deployable services.
- Scale teams and components.
- Adds network failures, distributed tracing, eventual consistency, operational complexity.

Layered architecture:

```text
Controller: HTTP/request mapping
Service: business logic/use cases
Repository: persistence access
Database: storage
```

Example:

```java
class UserController {
    private final UserService service;
    UserDto getUser(long id) { return service.getUser(id); }
}

class UserService {
    private final UserRepository repo;
    UserDto getUser(long id) {
        User user = repo.findById(id).orElseThrow();
        return new UserDto(user.id(), user.email());
    }
}
```

Repository pattern:

- Hides persistence details.
- Makes service logic easier to test.

Interview questions:

- Monolith vs microservices.
- Controller vs service vs repository.
- How do you design idempotent APIs?
- How do you secure a REST API?

---

## Part 8: Medium-Level Java Implementations

These implementations are intentionally compact but complete enough for interview discussion. Production versions need more validation, tests, metrics, and failure handling.

### 8.1 Custom Dynamic Array

```java
import java.util.Arrays;

public class DynamicArray<T> {
    private Object[] data;
    private int size;

    public DynamicArray() {
        data = new Object[10];
    }

    public void add(T value) {
        ensureCapacity(size + 1);
        data[size++] = value;
    }

    public T get(int index) {
        checkIndex(index);
        return element(index);
    }

    public T set(int index, T value) {
        checkIndex(index);
        T old = element(index);
        data[index] = value;
        return old;
    }

    public T remove(int index) {
        checkIndex(index);
        T old = element(index);
        int moved = size - index - 1;
        if (moved > 0) System.arraycopy(data, index + 1, data, index, moved);
        data[--size] = null;
        return old;
    }

    public int size() {
        return size;
    }

    private void ensureCapacity(int min) {
        if (min <= data.length) return;
        int newCap = data.length + (data.length >> 1);
        if (newCap < min) newCap = min;
        data = Arrays.copyOf(data, newCap);
    }

    private void checkIndex(int index) {
        if (index < 0 || index >= size) throw new IndexOutOfBoundsException(index);
    }

    @SuppressWarnings("unchecked")
    private T element(int index) {
        return (T) data[index];
    }
}
```

Explanation:

- Uses `Object[]` because Java cannot directly create generic arrays.
- `add` is amortized O(1).
- `remove` shifts elements and nulls old slot to avoid memory leak.
- C++ `std::vector<T>` stores values inline; Java stores references for object types.

### 8.2 Custom HashMap

```java
import java.util.Objects;

public class SimpleHashMap<K, V> {
    private static class Node<K, V> {
        final K key;
        V value;
        Node<K, V> next;

        Node(K key, V value, Node<K, V> next) {
            this.key = key;
            this.value = value;
            this.next = next;
        }
    }

    private Node<K, V>[] table;
    private int size;
    private final double loadFactor;

    @SuppressWarnings("unchecked")
    public SimpleHashMap() {
        table = (Node<K, V>[]) new Node[16];
        loadFactor = 0.75;
    }

    public V put(K key, V value) {
        if ((size + 1) > table.length * loadFactor) resize();
        int i = index(key, table.length);
        for (Node<K, V> n = table[i]; n != null; n = n.next) {
            if (Objects.equals(n.key, key)) {
                V old = n.value;
                n.value = value;
                return old;
            }
        }
        table[i] = new Node<>(key, value, table[i]);
        size++;
        return null;
    }

    public V get(K key) {
        int i = index(key, table.length);
        for (Node<K, V> n = table[i]; n != null; n = n.next) {
            if (Objects.equals(n.key, key)) return n.value;
        }
        return null;
    }

    public V remove(K key) {
        int i = index(key, table.length);
        Node<K, V> prev = null;
        Node<K, V> cur = table[i];
        while (cur != null) {
            if (Objects.equals(cur.key, key)) {
                if (prev == null) table[i] = cur.next;
                else prev.next = cur.next;
                size--;
                return cur.value;
            }
            prev = cur;
            cur = cur.next;
        }
        return null;
    }

    public int size() {
        return size;
    }

    private int index(K key, int len) {
        int h = key == null ? 0 : key.hashCode();
        h ^= (h >>> 16);
        return h & (len - 1);
    }

    @SuppressWarnings("unchecked")
    private void resize() {
        Node<K, V>[] old = table;
        table = (Node<K, V>[]) new Node[old.length * 2];
        size = 0;
        for (Node<K, V> head : old) {
            for (Node<K, V> n = head; n != null; n = n.next) {
                put(n.key, n.value);
            }
        }
    }
}
```

Complexity:

- Average O(1), worst O(n) with long chains.
- Production Java HashMap has more optimizations, including tree bins.

### 8.3 Stack And Queue

Stack:

```java
public class ArrayStack<T> {
    private final DynamicArray<T> data = new DynamicArray<>();

    public void push(T value) { data.add(value); }

    public T pop() {
        if (data.size() == 0) throw new IllegalStateException("empty");
        return data.remove(data.size() - 1);
    }

    public T peek() {
        if (data.size() == 0) throw new IllegalStateException("empty");
        return data.get(data.size() - 1);
    }
}
```

Circular queue:

```java
public class CircularQueue<T> {
    private Object[] data = new Object[8];
    private int head;
    private int size;

    public void offer(T value) {
        ensureCapacity(size + 1);
        data[(head + size) % data.length] = value;
        size++;
    }

    public T poll() {
        if (size == 0) throw new IllegalStateException("empty");
        @SuppressWarnings("unchecked")
        T value = (T) data[head];
        data[head] = null;
        head = (head + 1) % data.length;
        size--;
        return value;
    }

    private void ensureCapacity(int min) {
        if (min <= data.length) return;
        Object[] next = new Object[data.length * 2];
        for (int i = 0; i < size; i++) next[i] = data[(head + i) % data.length];
        data = next;
        head = 0;
    }
}
```

### 8.4 Linked List

```java
public class SinglyLinkedList<T> {
    private static class Node<T> {
        T value;
        Node<T> next;
        Node(T value) { this.value = value; }
    }

    private Node<T> head;
    private Node<T> tail;
    private int size;

    public void addLast(T value) {
        Node<T> n = new Node<>(value);
        if (tail == null) head = tail = n;
        else {
            tail.next = n;
            tail = n;
        }
        size++;
    }

    public T removeFirst() {
        if (head == null) throw new IllegalStateException("empty");
        T value = head.value;
        head = head.next;
        if (head == null) tail = null;
        size--;
        return value;
    }

    public boolean contains(T value) {
        for (Node<T> n = head; n != null; n = n.next) {
            if (java.util.Objects.equals(n.value, value)) return true;
        }
        return false;
    }
}
```

### 8.5 LRU Cache

```java
import java.util.HashMap;
import java.util.Map;

public class LruCache<K, V> {
    private class Node {
        K key;
        V value;
        Node prev, next;
        Node(K key, V value) { this.key = key; this.value = value; }
    }

    private final int capacity;
    private final Map<K, Node> map = new HashMap<>();
    private final Node head = new Node(null, null);
    private final Node tail = new Node(null, null);

    public LruCache(int capacity) {
        if (capacity <= 0) throw new IllegalArgumentException();
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public V get(K key) {
        Node n = map.get(key);
        if (n == null) return null;
        moveToFront(n);
        return n.value;
    }

    public void put(K key, V value) {
        Node n = map.get(key);
        if (n != null) {
            n.value = value;
            moveToFront(n);
            return;
        }
        n = new Node(key, value);
        map.put(key, n);
        addAfterHead(n);
        if (map.size() > capacity) {
            Node victim = tail.prev;
            remove(victim);
            map.remove(victim.key);
        }
    }

    private void moveToFront(Node n) {
        remove(n);
        addAfterHead(n);
    }

    private void addAfterHead(Node n) {
        n.next = head.next;
        n.prev = head;
        head.next.prev = n;
        head.next = n;
    }

    private void remove(Node n) {
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }
}
```

Design:

- HashMap gives O(1) lookup.
- Doubly linked list gives O(1) recency update and eviction.

### 8.6 Trie

```java
public class Trie {
    private static class Node {
        Node[] child = new Node[26];
        boolean word;
    }

    private final Node root = new Node();

    public void insert(String s) {
        Node cur = root;
        for (char ch : s.toCharArray()) {
            int i = ch - 'a';
            if (i < 0 || i >= 26) throw new IllegalArgumentException("lowercase only");
            if (cur.child[i] == null) cur.child[i] = new Node();
            cur = cur.child[i];
        }
        cur.word = true;
    }

    public boolean search(String s) {
        Node n = find(s);
        return n != null && n.word;
    }

    public boolean startsWith(String prefix) {
        return find(prefix) != null;
    }

    private Node find(String s) {
        Node cur = root;
        for (char ch : s.toCharArray()) {
            int i = ch - 'a';
            if (i < 0 || i >= 26) return null;
            cur = cur.child[i];
            if (cur == null) return null;
        }
        return cur;
    }
}
```

Complexity:

- O(length) insert/search.
- Space can be high; use HashMap children for sparse alphabets.

### 8.7 Producer Consumer

```java
import java.util.ArrayDeque;
import java.util.Queue;

public class BlockingBuffer<T> {
    private final Queue<T> q = new ArrayDeque<>();
    private final int capacity;

    public BlockingBuffer(int capacity) {
        this.capacity = capacity;
    }

    public synchronized void put(T item) throws InterruptedException {
        while (q.size() == capacity) wait();
        q.add(item);
        notifyAll();
    }

    public synchronized T take() throws InterruptedException {
        while (q.isEmpty()) wait();
        T item = q.remove();
        notifyAll();
        return item;
    }
}
```

Production equivalent:

- Use `ArrayBlockingQueue`.

### 8.8 Simple Thread Pool

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

public class SimpleThreadPool implements AutoCloseable {
    private final Queue<Runnable> tasks = new ArrayDeque<>();
    private final List<Thread> workers = new ArrayList<>();
    private boolean shutdown;

    public SimpleThreadPool(int n) {
        for (int i = 0; i < n; i++) {
            Thread t = new Thread(this::work, "worker-" + i);
            workers.add(t);
            t.start();
        }
    }

    public synchronized void submit(Runnable task) {
        if (shutdown) throw new IllegalStateException("shutdown");
        tasks.add(task);
        notifyAll();
    }

    private void work() {
        while (true) {
            Runnable task;
            synchronized (this) {
                while (tasks.isEmpty() && !shutdown) {
                    try {
                        wait();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }
                if (tasks.isEmpty() && shutdown) return;
                task = tasks.remove();
            }
            try {
                task.run();
            } catch (RuntimeException e) {
                e.printStackTrace();
            }
        }
    }

    public synchronized void close() {
        shutdown = true;
        notifyAll();
    }
}
```

Design:

- Workers wait on queue.
- Submit enqueues and notifies.
- Shutdown allows workers to exit after queue drains.

### 8.9 Parking Lot Design

Core model:

```text
ParkingLot
  -> floors
Floor
  -> spots
Vehicle
  -> type, plate
Ticket
  -> spot, entryTime
```

Code:

```java
import java.time.Instant;
import java.util.*;

enum VehicleType { BIKE, CAR, TRUCK }

record Vehicle(String plate, VehicleType type) {}

class ParkingSpot {
    final int id;
    final VehicleType type;
    Vehicle vehicle;

    ParkingSpot(int id, VehicleType type) {
        this.id = id;
        this.type = type;
    }

    boolean canFit(Vehicle v) {
        return vehicle == null && type == v.type();
    }
}

record Ticket(String id, Vehicle vehicle, ParkingSpot spot, Instant entryTime) {}

class ParkingLot {
    private final List<ParkingSpot> spots;
    private final Map<String, Ticket> active = new HashMap<>();

    ParkingLot(List<ParkingSpot> spots) {
        this.spots = spots;
    }

    synchronized Ticket park(Vehicle v) {
        for (ParkingSpot s : spots) {
            if (s.canFit(v)) {
                s.vehicle = v;
                Ticket t = new Ticket(UUID.randomUUID().toString(), v, s, Instant.now());
                active.put(t.id(), t);
                return t;
            }
        }
        throw new IllegalStateException("full");
    }

    synchronized long leave(String ticketId) {
        Ticket t = active.remove(ticketId);
        if (t == null) throw new IllegalArgumentException("invalid ticket");
        t.spot().vehicle = null;
        long minutes = Math.max(1, java.time.Duration.between(t.entryTime(), Instant.now()).toMinutes());
        return minutes * 10;
    }
}
```

Interview extensions:

- Different spot sizes.
- Nearest spot allocation.
- Multiple gates.
- Payment states.
- Concurrency control.

### 8.10 Library Management System

Design:

```text
Book(isbn, title)
BookCopy(copyId, book, status)
Member
Loan(copy, member, dueDate)
```

Code:

```java
import java.time.LocalDate;
import java.util.*;

record Book(String isbn, String title) {}

class BookCopy {
    final String copyId;
    final Book book;
    boolean borrowed;

    BookCopy(String copyId, Book book) {
        this.copyId = copyId;
        this.book = book;
    }
}

record Member(String id, String name) {}

record Loan(String id, BookCopy copy, Member member, LocalDate dueDate) {}

class Library {
    private final Map<String, BookCopy> copies = new HashMap<>();
    private final Map<String, Loan> loans = new HashMap<>();

    void addCopy(BookCopy copy) {
        copies.put(copy.copyId, copy);
    }

    synchronized Loan borrow(String copyId, Member member) {
        BookCopy copy = copies.get(copyId);
        if (copy == null) throw new IllegalArgumentException("copy not found");
        if (copy.borrowed) throw new IllegalStateException("already borrowed");
        copy.borrowed = true;
        Loan loan = new Loan(UUID.randomUUID().toString(), copy, member, LocalDate.now().plusDays(14));
        loans.put(loan.id(), loan);
        return loan;
    }

    synchronized void returnBook(String loanId) {
        Loan loan = loans.remove(loanId);
        if (loan == null) throw new IllegalArgumentException("loan not found");
        loan.copy().borrowed = false;
    }
}
```

Extensions:

- Reservations.
- Fines.
- Search index.
- Multiple copies.
- Member borrowing limits.

### 8.11 Banking System

```java
import java.util.concurrent.atomic.AtomicLong;

class Account {
    final long id;
    private long balance;

    Account(long id, long balance) {
        if (balance < 0) throw new IllegalArgumentException();
        this.id = id;
        this.balance = balance;
    }

    long balance() {
        return balance;
    }

    void deposit(long amount) {
        if (amount <= 0) throw new IllegalArgumentException();
        balance += amount;
    }

    void withdraw(long amount) {
        if (amount <= 0 || amount > balance) throw new IllegalArgumentException();
        balance -= amount;
    }
}

class Bank {
    private final AtomicLong ids = new AtomicLong(1);

    Account open(long initial) {
        return new Account(ids.getAndIncrement(), initial);
    }

    void transfer(Account from, Account to, long amount) {
        Account first = from.id < to.id ? from : to;
        Account second = from.id < to.id ? to : from;
        synchronized (first) {
            synchronized (second) {
                from.withdraw(amount);
                to.deposit(amount);
            }
        }
    }
}
```

Design:

- Lock ordering prevents deadlock.
- Real banking needs ledger entries, idempotency keys, audit trails, transactions, and immutable money representation.

### 8.12 URL Shortener Design

Core requirements:

- Create short code for long URL.
- Redirect short code to long URL.
- Track metadata.
- Handle high read traffic.

Architecture:

```text
Client -> API -> Service -> DB
                 |
                 +-> Cache
```

Schema:

```sql
CREATE TABLE urls (
    code VARCHAR(16) PRIMARY KEY,
    long_url TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NULL
);
```

Code:

```java
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

class UrlShortener {
    private static final String ALPHABET =
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

    private final AtomicLong sequence = new AtomicLong(1);
    private final Map<String, String> store = new ConcurrentHashMap<>();

    public String shorten(String longUrl) {
        validate(longUrl);
        String code = encode(sequence.getAndIncrement());
        store.put(code, longUrl);
        return code;
    }

    public String resolve(String code) {
        String url = store.get(code);
        if (url == null) throw new NoSuchElementException("not found");
        return url;
    }

    private String encode(long n) {
        StringBuilder sb = new StringBuilder();
        while (n > 0) {
            int r = (int) (n % 62);
            sb.append(ALPHABET.charAt(r));
            n /= 62;
        }
        return sb.reverse().toString();
    }

    private void validate(String url) {
        if (url == null || !(url.startsWith("http://") || url.startsWith("https://"))) {
            throw new IllegalArgumentException("invalid URL");
        }
    }
}
```

Scaling discussion:

- Sequence generator must be distributed or coordinated.
- Cache popular codes.
- Use 301 vs 302 carefully.
- Prevent abuse and malware.
- Add custom aliases with uniqueness checks.
- Consider analytics pipeline separate from redirect path.

---

## Interview Practice Map

Use this checklist to test depth.

OS:

- Explain page fault from CPU instruction to resumed process.
- Design a bounded buffer using semaphores or monitors.
- Explain what happens when a shell runs `ls`.
- Diagnose high CPU with many context switches.

DBMS:

- Given a query, choose indexes and explain plan.
- Explain how a transaction recovers after crash.
- Model an order system normalized to 3NF.
- Explain replication lag bug in read-after-write flow.

OOP:

- Design payment processing using Strategy and Dependency Inversion.
- Explain why inheritance can violate LSP.
- Compare Java interface and C++ abstract class.

Java:

- Explain class loading and JIT.
- Explain why `HashMap` key mutation is dangerous.
- Explain `volatile` with happens-before.
- Design a thread pool and discuss shutdown.

Backend:

- Design REST API for orders with pagination and errors.
- Explain authentication vs authorization.
- Explain how browser reaches backend from URL.
- Design URL shortener and identify bottlenecks.

---

## Common High-Signal Interview Answers

Good answers usually include:

- Definition.
- Why the concept exists.
- Internal mechanism.
- Tradeoffs.
- Failure modes.
- Example.

Example answer shape for "What is an index?":

> An index is an auxiliary data structure, commonly a B+ tree, that lets the database find rows without scanning the whole table. It speeds reads and range queries but costs storage and slows writes because the index must be maintained. A composite index on `(user_id, created_at)` helps queries filtering by `user_id` and sorting/ranging by `created_at`, but usually not queries filtering only by `created_at` because of leftmost prefix behavior.

---

## Final Study Strategy

1. For each OS topic, draw the state transition or memory diagram from memory.
2. For each DB topic, write SQL and predict output before running.
3. For OOP, implement both Java and C++ versions of the same design.
4. For Java collections, implement simplified versions and list invariants.
5. For concurrency, explain visibility, atomicity, and ordering separately.
6. For backend, trace one request from browser to database and back.
7. For system design, always state assumptions, traffic, data model, APIs, bottlenecks, and failure handling.

