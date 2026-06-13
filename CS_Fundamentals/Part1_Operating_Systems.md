# Operating Systems Complete Guide

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

