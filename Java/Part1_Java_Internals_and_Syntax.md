# Part 1: Java Internals & Syntax — Complete Mastery Guide
### For C++ Developers | Backend SDE Interview Handbook

---

> **How to use this document:** Every section follows the pattern:
> Theory → Internal Working → C++ vs Java → Code Examples → Interview Questions
> Read linearly for full understanding, or jump to sections as needed.

---

# Table of Contents

1. [Java Ecosystem: JDK, JRE, JVM](#1-java-ecosystem-jdk-jre-jvm)
2. [How Java Code Runs: Compilation to Execution](#2-how-java-code-runs-compilation-to-execution)
3. [Bytecode & the Class File](#3-bytecode--the-class-file)
4. [Class Loading Subsystem](#4-class-loading-subsystem)
5. [JIT Compiler](#5-jit-compiler)
6. [JVM Memory Architecture](#6-jvm-memory-architecture)
7. [Garbage Collection](#7-garbage-collection)
8. [Object Lifecycle](#8-object-lifecycle)
9. [Java Memory Model (JMM)](#9-java-memory-model-jmm)
10. [Java Syntax: Variables & Data Types](#10-java-syntax-variables--data-types)
11. [Operators](#11-operators)
12. [Control Flow](#12-control-flow)
13. [Methods in Java](#13-methods-in-java)
14. [Classes & Objects](#14-classes--objects)
15. [Java Keywords — Deep Dive](#15-java-keywords--deep-dive)
16. [Modern Java: Records, Sealed Classes, Enums](#16-modern-java-records-sealed-classes-enums)

---

# 1. Java Ecosystem: JDK, JRE, JVM

## Theory

When you install Java, you're dealing with three nested layers:

```
+---------------------------------------------+
|                    JDK                      |  ← You install this for development
|  (Java Development Kit)                     |
|  +---------------------------------------+  |
|  |               JRE                    |  |
|  |  (Java Runtime Environment)          |  |
|  |  +-------------------------------+   |  |
|  |  |           JVM                 |   |  |
|  |  |  (Java Virtual Machine)       |   |  |
|  |  |  - Class Loader               |   |  |
|  |  |  - Execution Engine           |   |  |
|  |  |  - Runtime Data Areas         |   |  |
|  |  +-------------------------------+   |  |
|  |  + Java Standard Libraries (rt.jar)  |  |
|  +---------------------------------------+  |
|  + javac, javap, jdb, jconsole, jshell    |  |
+---------------------------------------------+
```

### JVM (Java Virtual Machine)
- An **abstract computing machine** — it's a specification, not a physical chip
- It reads bytecode (.class files) and executes them
- It is **platform-specific** (different JVM binaries for Windows, Linux, macOS)
- Provides: memory management, garbage collection, security sandbox, thread management

### JRE (Java Runtime Environment)
- JVM + standard class libraries (java.lang, java.util, java.io, etc.)
- What end users install to **run** Java programs
- Does NOT contain the compiler (javac)

### JDK (Java Development Kit)
- JRE + development tools: javac (compiler), javap (disassembler), jdb (debugger), jconsole (monitoring), jshell (REPL)
- What developers install to **write and compile** Java programs

## C++ vs Java: The Key Difference

| Aspect | C++ | Java |
|--------|-----|------|
| Compilation target | Native machine code (platform-specific .exe/.out) | Bytecode (.class, platform-neutral) |
| Runtime | OS directly executes binary | JVM interprets/JIT-compiles bytecode |
| Portability | "Compile once, run on same platform" | "Write once, run anywhere" |
| Memory management | Manual (new/delete) | Automatic (GC) |
| Platform abstraction | None — you link to OS libraries | JVM is the abstraction layer |

The JVM is what makes Java's "Write Once, Run Anywhere" (WORA) promise real. The same .class file runs identically on a Windows JVM and a Linux JVM.

## Interview Questions
- **Q: What is the difference between JDK, JRE, and JVM?**
  A: JVM executes bytecode. JRE = JVM + standard libraries (enough to run). JDK = JRE + dev tools like javac (needed to compile). On a production server, you install JRE. On your dev machine, you install JDK.

- **Q: Is the JVM platform-independent?**
  A: No — the JVM itself is platform-specific. But the bytecode it runs is platform-independent. You need the right JVM for your OS, but the .class files it runs are universal.

---

# 2. How Java Code Runs: Compilation to Execution

## The Full Pipeline

```
 YourCode.java
      |
      | javac (Java Compiler)
      ▼
 YourCode.class   ← Bytecode (not machine code, not human code)
      |
      | java command → JVM loads class
      ▼
 Class Loader Subsystem
      |
      | Loads, links, initializes class
      ▼
 Execution Engine
      |
      |── Interpreter (line by line, slow)
      |
      └── JIT Compiler (hot code → native machine code, fast)
      |
      ▼
 Native Machine Code runs on CPU
```

## Step-by-Step Walkthrough

**Step 1: Write source code**
```java
// Hello.java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

**Step 2: Compile with javac**
```bash
javac Hello.java
# Produces: Hello.class
```
The compiler checks syntax, resolves types, and generates bytecode — a set of instructions for the JVM (not for any real CPU).

**Step 3: Run with java**
```bash
java Hello
```
This launches the JVM, which loads Hello.class, verifies it, and begins execution.

**Step 4: Execution Engine decides**
- First few calls → Interpreter runs bytecode directly (slow but immediate)
- Hot methods (called often) → JIT compiles them to native code and caches it
- Result: native machine code executes at near-C++ speed

## Why This Design?

The interpreter-first, JIT-later design is deliberate:
- Startup is fast (no waiting for full compilation like AOT)
- Long-running apps (servers) eventually run as fast as compiled code
- The JIT knows *runtime* behavior (actual call frequencies) and can optimize better than a static compiler

## Interview Questions
- **Q: What is bytecode?**
  A: An intermediate representation — not machine code, not source code. It's a set of instructions for the JVM's virtual instruction set. Portable across platforms.

- **Q: What happens when you run `java Hello`?**
  A: JVM starts → Bootstrap class loader loads Hello.class → Bytecode verifier validates it → JVM finds main() → Execution engine begins interpreting → JIT compiles hot paths to native code.

---

# 3. Bytecode & the Class File

## What is Bytecode?

Bytecode is the compiled output of Java source code — a platform-neutral instruction set that the JVM understands. Think of it as an assembly language for a virtual CPU.

```java
// Source code
int a = 5;
int b = 3;
int c = a + b;
```

```
// Corresponding bytecode (from javap -c)
   0: iconst_5        // push 5 onto stack
   1: istore_1        // store in local var slot 1 (a)
   2: iconst_3        // push 3 onto stack
   3: istore_2        // store in local var slot 2 (b)
   4: iload_1         // push a onto stack
   5: iload_2         // push b onto stack
   6: iadd            // pop two ints, push sum
   7: istore_3        // store result in slot 3 (c)
```

The JVM is a **stack-based virtual machine** — most operations push and pop a single operand stack rather than using named registers.

## The Class File Structure

Every .class file has a fixed binary format:

```
ClassFile {
    magic                  u4   // 0xCAFEBABE — always
    minor_version          u2
    major_version          u2   // tells JVM which Java version compiled this
    constant_pool_count    u2
    constant_pool[]             // strings, class names, method signatures
    access_flags           u2   // public? abstract? interface? final?
    this_class             u2   // index into constant pool
    super_class            u2   // index into constant pool
    interfaces[]
    fields[]
    methods[]               // each method contains its bytecode
    attributes[]            // SourceFile, LineNumberTable, etc.
}
```

The first 4 bytes are always `0xCAFEBABE` — a magic number that identifies valid Java class files. (A playful nod to the Grateful Dead and coffeehouses of early 1990s Silicon Valley.)

## Viewing Bytecode

```bash
javap -c Hello.class        # Show bytecode
javap -verbose Hello.class  # Full detail including constant pool
```

## Interview Questions
- **Q: What is the magic number in a Java class file?**
  A: `0xCAFEBABE`. It's how the JVM quickly validates that a file is a real Java class file.

- **Q: Is bytecode executable on the CPU directly?**
  A: No. It needs the JVM to either interpret it or JIT-compile it to actual machine code.

---

# 4. Class Loading Subsystem

## Theory

Before any Java code can run, its class must be loaded into the JVM. The Class Loading Subsystem handles this in three phases:

```
Class Loading Subsystem
        |
        ├─── 1. Loading
        │         Read .class file from disk/jar/network
        │         Create Class object in heap
        │
        ├─── 2. Linking
        │         ├── Verification   (valid bytecode? safe?)
        │         ├── Preparation    (allocate static fields, set defaults)
        │         └── Resolution     (resolve symbolic references to direct refs)
        │
        └─── 3. Initialization
                  Run static initializers and static blocks
                  e.g., static { System.out.println("Class loaded!"); }
```

## The Three Class Loaders

Java uses a hierarchy of class loaders:

```
Bootstrap ClassLoader      (built into JVM, loads java.lang.*, rt.jar)
        ↑
Extension ClassLoader      (loads lib/ext/* — optional extensions)
        ↑
Application ClassLoader    (loads your app's classpath — your .class files)
        ↑
Custom ClassLoader         (you can write your own for hot-reload, plugins)
```

### Delegation Model (Parent-First)

When a class needs to be loaded:
1. Application ClassLoader asks Extension ClassLoader
2. Extension asks Bootstrap
3. Bootstrap tries to load — if it can, done
4. If not, Extension tries — if it can, done
5. If not, Application ClassLoader loads it

**Why?** Security. You can't write your own `java.lang.String` and have it loaded, because Bootstrap will always load the real one first.

```java
// You can inspect class loaders at runtime:
System.out.println(String.class.getClassLoader());       // null = Bootstrap
System.out.println(ArrayList.class.getClassLoader());    // null = Bootstrap (rt.jar)
System.out.println(MyClass.class.getClassLoader());      // sun.misc.Launcher$AppClassLoader
```

## Static Initialization Blocks

Initialization phase runs `static {}` blocks:

```java
public class Config {
    static final Map<String, String> SETTINGS;

    static {
        // This runs exactly once when the class is first loaded
        SETTINGS = new HashMap<>();
        SETTINGS.put("host", "localhost");
        SETTINGS.put("port", "8080");
        System.out.println("Config class initialized!");
    }
}
```

## Class Loading in Real Life

- **Spring Boot** uses custom class loaders to load beans dynamically
- **Hot-reload** in dev tools (like Spring DevTools) works by creating new class loaders and discarding old ones
- **Plugin systems** (like IntelliJ plugins) use isolated class loaders per plugin to prevent version conflicts

## Interview Questions
- **Q: What is the delegation model in class loading?**
  A: When loading a class, the current loader first delegates to its parent. Only if the parent fails does the child attempt to load it. This prevents user code from overriding core Java classes.

- **Q: When is a class initialized?**
  A: On first active use — when an instance is created, a static method is called, or a static field (that isn't a compile-time constant) is accessed.

- **Q: Can you write your own class loader?**
  A: Yes — extend `ClassLoader` and override `findClass()`. Used in hot-reload, OSGi plugin systems, application servers running multiple apps with conflicting library versions.

---

# 5. JIT Compiler

## Theory

JIT stands for **Just-In-Time** compilation. It's the bridge between bytecode and native performance.

### The Problem with Pure Interpretation

Interpreting bytecode instruction by instruction adds overhead on every single operation. A simple `a + b` in bytecode takes the interpreter several steps to decode and execute vs. a single `ADD` instruction in native code.

### The JIT Solution

```
Execution Count Tracking:
                                    
Method A() → called 1 time    → Interpret
Method B() → called 1 time    → Interpret
Method A() → called 1000 times → JIT COMPILE → native code cached
Method A() → called 1001 time → execute native code directly (fast!)
```

The threshold for JIT compilation (called the "hotspot threshold") is 10,000 invocations by default in HotSpot JVM.

## HotSpot JVM — Two JIT Compilers

Oracle's HotSpot JVM actually has two JIT compilers working together:

```
C1 Compiler (Client Compiler)
  - Fast compilation
  - Light optimizations
  - Low latency startup
  - Used early in a method's life

C2 Compiler (Server Compiler)
  - Slower compilation
  - Heavy optimizations (inlining, loop unrolling, escape analysis)
  - Best peak performance
  - Used for genuinely hot code
```

Modern JVMs use **Tiered Compilation** — C1 first, C2 later for the hottest code.

## Key JIT Optimizations

**1. Method Inlining**
The JIT literally copies the body of a small, frequently-called method into its caller, eliminating the call overhead:
```java
// Before inlining (your code)
int result = add(a, b);

// After JIT inlining (what actually executes)
int result = a + b;   // no method call overhead
```

**2. Loop Unrolling**
```java
// Your code
for (int i = 0; i < 4; i++) arr[i] = 0;

// JIT may generate equivalent of:
arr[0] = 0; arr[1] = 0; arr[2] = 0; arr[3] = 0;
// Eliminates loop condition check overhead
```

**3. Escape Analysis**
If the JIT determines an object never "escapes" a method (never stored in a field, never returned), it can allocate it on the **stack instead of heap** — no GC pressure.

```java
void process() {
    Point p = new Point(1, 2);  // JIT may put this on stack, not heap
    int dist = p.x + p.y;
    // p never escapes this method
}
```

**4. Dead Code Elimination**
```java
if (false) {
    expensiveOperation();  // JIT removes this entirely
}
```

## AOT vs JIT (Ahead-of-Time vs Just-in-Time)

| | JIT | AOT (GraalVM Native Image) |
|--|-----|---------------------------|
| Startup | Slow (needs warmup) | Fast (already compiled) |
| Peak perf | Very high | High but not always as high |
| Binary | JVM + bytecode | Standalone native executable |
| Use case | Long-running servers | Serverless, CLI tools, microservices |

GraalVM's Native Image is AOT for Java — used in frameworks like Quarkus and Micronaut.

## Interview Questions
- **Q: What is JIT compilation and how does it improve performance?**
  A: The JVM monitors method call frequency. When a method becomes "hot" (called many times), the JIT compiles it to native machine code and caches it. Subsequent calls execute native code directly, achieving near-C performance. Key optimizations include inlining, escape analysis, and loop unrolling.

- **Q: What is the difference between JIT and AOT?**
  A: JIT compiles at runtime based on actual usage patterns. AOT (e.g., GraalVM Native) compiles at build time to a standalone native binary. JIT wins at peak throughput; AOT wins at startup time.

---

# 6. JVM Memory Architecture

## Overview: JVM Runtime Data Areas

The JVM divides memory into distinct regions, each with a specific purpose:

```
┌────────────────────────────────────────────────────────────────────┐
│                          JVM MEMORY                                │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                      HEAP (Shared)                          │  │
│  │                                                             │  │
│  │   ┌──────────────────────┐   ┌──────────────────────────┐  │  │
│  │   │    Young Generation  │   │     Old Generation       │  │  │
│  │   │  ┌──────┬───────┐    │   │  (Tenured Space)         │  │  │
│  │   │  │ Eden │ S0 S1 │    │   │  Long-lived objects       │  │  │
│  │   │  └──────┴───────┘    │   │                          │  │  │
│  │   │  New objects here    │   │                          │  │  │
│  │   └──────────────────────┘   └──────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │               Metaspace (Non-Heap, native memory)          │   │
│  │  Class metadata, method bytecode, static variables         │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                    │
│  Per-Thread (each thread has its own):                            │
│  ┌───────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │  Stack (JVM)  │  │  Stack (JVM)     │  │  Stack (JVM)      │  │
│  │  Thread 1     │  │  Thread 2        │  │  Thread 3         │  │
│  └───────────────┘  └──────────────────┘  └───────────────────┘  │
│                                                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  PC Registers (one per thread — current bytecode instr)    │   │
│  └────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
```

---

## The Heap

The heap is the largest JVM memory area, shared across all threads. All objects and arrays live here.

### Young Generation

New objects are born in Eden space:

```
Young Generation
┌──────────────────────────────────────────────────────┐
│  Eden Space                │  Survivor 0  │ Survivor 1│
│  (new objects allocated    │  (S0)        │ (S1)      │
│   here first)              │              │           │
└──────────────────────────────────────────────────────┘
```

**Lifecycle in Young Gen:**
1. Object created → goes to Eden
2. Minor GC runs → live objects from Eden → Survivor 0 (age = 1)
3. Next Minor GC → live objects from Eden + S0 → S1 (age increases)
4. Objects alternate between S0 and S1
5. Age reaches threshold (default 15) → promoted to Old Generation

The design insight: most objects die young ("generational hypothesis"). Eden is collected very frequently and very cheaply.

### Old Generation (Tenured Space)

Long-lived objects live here. Collected less frequently but collection is more expensive (Major GC / Full GC).

Examples of objects that end up in Old Gen:
- Application-level caches
- Static collections
- Thread pools
- Session objects in web apps

### Why This Design?

The generational split is a key GC optimization. Young objects are cheap to collect (most are already dead). Old objects are expensive to scan but done rarely. This makes the common case (short-lived objects) extremely fast.

---

## The Stack (JVM Stack)

Each thread gets its own stack. Each method call pushes a **Stack Frame** onto the stack:

```
Thread Stack
│
│ ┌─────────────────────────────────┐
│ │ Frame: main()                   │
│ │  Local Variables: args, result  │
│ │  Operand Stack: [5, 3, ...]     │
│ │  Return Address                 │
│ └─────────────────────────────────┘
│         ↑ calls
│ ┌─────────────────────────────────┐
│ │ Frame: calculate()              │
│ │  Local Variables: a=5, b=3      │
│ │  Operand Stack: [5, 3]          │
│ │  Return Address → back to main  │
│ └─────────────────────────────────┘  ← current frame (top of stack)
```

Each frame contains:
- **Local Variable Array**: method parameters + local variables (primitives stored directly)
- **Operand Stack**: working area for bytecode instructions
- **Return Address**: where to return after method completes

**StackOverflowError** occurs when the stack runs out of space — almost always caused by infinite recursion.

```java
// This causes StackOverflowError
void recurse() {
    recurse();  // infinite recursion → stack fills up → crash
}
```

---

## Metaspace (Java 8+)

Before Java 8, class metadata was stored in **PermGen** (part of heap, fixed size, frequently caused `OutOfMemoryError: PermGen space`). Java 8 replaced it with **Metaspace** — stored in native OS memory, auto-grows.

Metaspace stores:
- Class structure (fields, methods, bytecode)
- Method bytecode
- Static variables
- Constant pool
- JIT-compiled code cache

```bash
# Configure Metaspace limits
-XX:MetaspaceSize=128m        # Initial size
-XX:MaxMetaspaceSize=512m     # Maximum size
```

---

## C++ vs Java Memory

| Concept | C++ | Java |
|---------|-----|------|
| Stack | Same — auto-managed per function | Same — per thread, per method call |
| Heap | Manual: `new`/`delete` | Automatic: GC manages deallocation |
| Global/Static | .data / .bss segment | Metaspace |
| Object representation | In-memory struct directly | Object reference (pointer to heap) |
| Null pointer | Undefined behavior | NullPointerException (safe failure) |

A critical difference: In C++, `int x = 5` on the stack stores the integer directly. In Java, `int x = 5` on the stack also stores directly (primitives are value types). But `Object o = new Foo()` stores a **reference** (pointer) on the stack — the actual Foo object lives on the heap.

---

## Interview Questions
- **Q: What is the difference between Heap and Stack in Java?**
  A: Stack is per-thread, stores method frames with local variables and operand stacks. Heap is shared across all threads, stores all objects. Stack is LIFO and managed automatically. Heap is managed by GC.

- **Q: What replaced PermGen in Java 8?**
  A: Metaspace. It stores class metadata in native OS memory instead of inside the JVM heap. It auto-grows, eliminating the common `OutOfMemoryError: PermGen space` issue.

- **Q: What causes StackOverflowError vs OutOfMemoryError?**
  A: StackOverflowError = stack space exhausted (infinite recursion). OutOfMemoryError = heap space exhausted (too many/too large objects, or memory leak).

---

# 7. Garbage Collection

## Theory

Java's GC automatically reclaims memory from objects that are no longer reachable. You never call `delete` — the GC does it.

**Reachability:** An object is live if there's any chain of references from a **GC Root** to it.

**GC Roots are:**
- Local variables in any thread's stack frames
- Static fields
- Active thread objects
- JNI references

```
GC Root: static field → Object A → Object B → Object C   (all live, kept)
GC Root: local var   → Object D                           (live, kept)

Object E (no path from any GC root)                       (DEAD, collected)
```

---

## GC Algorithms

### Mark and Sweep (Conceptual Foundation)

```
Phase 1 - MARK:
  Start from GC roots
  Traverse all references recursively
  Mark each reachable object

Phase 2 - SWEEP:
  Scan the entire heap
  Reclaim all unmarked objects

Problem: FRAGMENTATION — free memory scattered in small gaps
```

### Mark-Sweep-Compact

Like Mark-Sweep, but adds a compaction step that slides live objects together, eliminating fragmentation. Used in the Old Generation.

### Copying Collector

Divides heap into two spaces (From-space, To-space):
```
From-space: [A][B][dead][C][dead][dead][D]
                  ↓ copy live objects
To-space:   [A][B][C][D]                    ← compact, no fragmentation!
Then swap roles.
```
Used in Young Generation (Eden → Survivor). Very fast but requires 2x memory.

---

## Major GC Implementations in Java

### Serial GC
- Single-threaded mark-sweep-compact
- Stop-the-world pause for entire GC
- Good for single-CPU, small heap, batch apps
- `-XX:+UseSerialGC`

### Parallel GC (Throughput GC)
- Multi-threaded minor GC, multi-threaded major GC
- Still stop-the-world, but faster due to parallelism
- Good for batch processing where throughput > latency
- `-XX:+UseParallelGC` (default before Java 9)

### G1 GC (Garbage First) — Default in Java 9+
```
Heap divided into equal-sized regions (~2048 regions):

┌───┬───┬───┬───┬───┬───┬───┬───┐
│ E │ E │ O │ S │ E │ O │ O │ H │
└───┴───┴───┴───┴───┴───┴───┴───┘
E=Eden  O=Old  S=Survivor  H=Humongous (large objects)
```
- Collects regions with most garbage first ("Garbage First")
- Predictable pause times (set target: `-XX:MaxGCPauseMillis=200`)
- Good for large heaps, latency-sensitive apps
- `-XX:+UseG1GC`

### ZGC / Shenandoah (Java 15+)
- Sub-millisecond GC pauses
- Concurrent (does most work while app runs)
- Scales to multi-terabyte heaps
- Good for real-time systems, trading platforms

---

## GC Tuning Flags

```bash
-Xms512m                   # Initial heap size
-Xmx2g                     # Max heap size
-XX:+UseG1GC               # Use G1 collector
-XX:MaxGCPauseMillis=200   # Target max pause
-XX:NewRatio=3             # Old:Young ratio (3:1)
-verbose:gc                # Log GC events
-XX:+PrintGCDetails        # Detailed GC log
```

---

## Common Memory Leaks in Java

Even with GC, you can leak memory by **holding references you no longer need**:

```java
// LEAK: static cache grows forever, never cleared
static Map<String, byte[]> cache = new HashMap<>();

void process(String key, byte[] data) {
    cache.put(key, data);  // added, never removed → grows forever
}
```

```java
// LEAK: Listeners not removed
button.addActionListener(this);
// If 'this' is removed from UI but listener still referenced,
// it (and everything it references) can't be GC'd
```

```java
// FIX: Use WeakReference for caches
Map<String, WeakReference<byte[]>> cache = new WeakHashMap<>();
// GC can collect values when memory is low
```

---

## C++ vs Java: Memory Management Philosophy

| | C++ | Java |
|--|-----|------|
| Allocation | `new Foo()` on heap | `new Foo()` on heap |
| Deallocation | `delete ptr` (manual!) | GC (automatic) |
| Dangling pointer | Possible — undefined behavior | Impossible — reference model prevents it |
| Memory leak | Easy to cause, hard to find | Still possible (via holding refs) but rarer |
| Deterministic destruction | Yes — destructor runs at `delete` | No — GC runs at its own time |
| Performance | No GC pause | GC pauses (milliseconds with modern GCs) |

C++ destructors are deterministic: `~MyClass()` runs exactly when the object goes out of scope or is deleted. Java has `finalize()` but it's deprecated and unreliable — use `try-with-resources` or `Closeable` instead.

---

## Interview Questions
- **Q: How does Java's Garbage Collector work?**
  A: GC identifies live objects by tracing from GC roots (stack vars, static fields, active threads). Unreachable objects are collected. Java uses generational GC — new objects in Young Gen (fast, frequent), long-lived objects in Old Gen (slower, infrequent). Modern default is G1 GC.

- **Q: Can you have a memory leak in Java?**
  A: Yes. GC only collects unreachable objects. If you keep references to objects you no longer need (static caches, forgotten listeners, thread locals not cleared), those objects stay in memory. This is a logical leak, not a C++-style physical leak.

- **Q: What is Stop-the-World in GC?**
  A: During certain GC phases, all application threads are paused ("stopped") so the GC can safely traverse the heap without interference. Modern GCs like G1 minimize these pauses; ZGC achieves sub-millisecond pauses.

---

# 8. Object Lifecycle

## Full Lifecycle of a Java Object

```
1. Class Loading
   └── Class is loaded, linked, initialized (static blocks run)

2. Allocation
   └── `new Foo()` → JVM allocates memory in Eden space (Young Gen)
   └── Memory zeroed (all fields default to 0/null/false)

3. Initialization
   └── Constructor runs (sets fields, calls super constructors)

4. Usage
   └── Object used via references

5. Unreachable
   └── No more references to the object from GC roots

6. Garbage Collection
   └── GC identifies object as unreachable
   └── Memory reclaimed

(Optional) Finalization — DEPRECATED
   └── finalize() called before collection (unreliable, avoid)
```

## Object Header

Every Java object has a hidden header before its fields:

```
Java Object in Memory:
┌─────────────────────────────────────────────────────┐
│  Mark Word (8 bytes)                                │
│  - Hashcode                                         │
│  - GC age (4 bits)                                  │
│  - Lock state (biased lock, thin lock, fat lock)    │
│  - GC flags                                         │
├─────────────────────────────────────────────────────┤
│  Class Pointer / Klass Word (4-8 bytes)             │
│  - Pointer to class metadata (in Metaspace)         │
├─────────────────────────────────────────────────────┤
│  Array Length (4 bytes, arrays only)                │
├─────────────────────────────────────────────────────┤
│  Instance Fields (your actual data)                 │
└─────────────────────────────────────────────────────┘
```

Minimum object size in Java is **16 bytes** (12-byte header + padding to 8-byte alignment). Even `new Object()` takes 16 bytes. This overhead matters when creating millions of tiny objects.

## Creating Objects: All Ways

```java
// 1. new keyword (most common)
String s = new String("hello");

// 2. Class.newInstance() (reflection, deprecated in Java 9)
String s = String.class.newInstance();

// 3. Constructor.newInstance() (reflection, preferred)
Constructor<String> c = String.class.getConstructor(String.class);
String s = c.newInstance("hello");

// 4. Object.clone() (creates copy without constructor)
MyClass obj2 = (MyClass) obj1.clone();  // requires implementing Cloneable

// 5. Deserialization (creates object without constructor)
ObjectInputStream in = new ObjectInputStream(fileInput);
MyClass obj = (MyClass) in.readObject();

// 6. Factory methods (common in APIs)
List<String> list = List.of("a", "b", "c");
```

## Interview Questions
- **Q: What is the size of an empty Java object?**
  A: 16 bytes minimum — 12-byte object header (mark word + class pointer) plus 4 bytes of alignment padding.

- **Q: What happens when you call `new Foo()`?**
  A: JVM checks if Foo's class is loaded (loads if not). Allocates memory in Eden. Zeros all fields. Runs the constructor chain (Object → ... → Foo). Returns reference.

---

# 9. Java Memory Model (JMM)

## Theory

The Java Memory Model defines the rules for how threads interact through memory. This is critical for multithreaded correctness.

### The Problem: CPU Caches

Modern CPUs have multiple levels of cache. When Thread 1 writes a value, it may sit in Thread 1's CPU cache and never be visible to Thread 2 on a different CPU:

```
CPU 1                              CPU 2
L1 Cache: x=1 (updated)          L1 Cache: x=0 (stale!)
L2 Cache: x=0                    L2 Cache: x=0
                Main Memory: x=0
```

Thread 2 reads `x` and gets 0, even though Thread 1 wrote 1. This is a **visibility problem**.

### Happens-Before Relationship

The JMM uses the **happens-before** rule: if action A happens-before action B, then A's effects are visible to B.

Key happens-before rules:
1. **Program order**: Each action in a thread happens-before the next action in that thread
2. **Monitor lock**: `unlock(m)` happens-before `lock(m)` by any thread
3. **Volatile write**: Writing a volatile variable happens-before reading it
4. **Thread start**: `thread.start()` happens-before any action in that thread
5. **Thread join**: All actions in thread T happen-before `T.join()` returns

### The volatile Keyword and Visibility

```java
class Flag {
    volatile boolean running = true;  // forces write to main memory immediately

    void stop() {
        running = false;  // other threads see this immediately
    }

    void run() {
        while (running) {  // always reads from main memory, not cache
            doWork();
        }
    }
}
```

Without `volatile`, the JVM may keep `running` in a CPU register/cache. One thread sets it `false`, but the other thread never sees the change — infinite loop.

### Reordering Problem

The JVM and CPU may reorder instructions for performance. This can break multithreaded code:

```java
// Your code:
x = 5;
initialized = true;

// CPU/JVM may reorder to:
initialized = true;   // ← Thread 2 sees this
x = 5;                // ← But Thread 2 reads x before this!
```

`volatile` and `synchronized` both prevent problematic reorderings.

## Interview Questions
- **Q: What is the Java Memory Model?**
  A: A specification that defines how threads interact through memory — specifically, which writes by one thread are guaranteed to be visible to another thread and when.

- **Q: What does `volatile` guarantee?**
  A: Visibility (writes are immediately visible to all threads) and prevents reordering around the volatile access. It does NOT guarantee atomicity for compound operations like `i++`.

---

# 10. Java Syntax: Variables & Data Types

## Primitive Types

Java has 8 primitive types — actual values, not objects (unlike C++ where you have both):

| Type | Size | Range | Default | C++ Equivalent |
|------|------|-------|---------|----------------|
| `byte` | 1 byte | -128 to 127 | 0 | `signed char` |
| `short` | 2 bytes | -32,768 to 32,767 | 0 | `short` |
| `int` | 4 bytes | -2^31 to 2^31-1 | 0 | `int` |
| `long` | 8 bytes | -2^63 to 2^63-1 | 0L | `long long` |
| `float` | 4 bytes | IEEE 754 single | 0.0f | `float` |
| `double` | 8 bytes | IEEE 754 double | 0.0 | `double` |
| `char` | 2 bytes | 0 to 65,535 (Unicode) | '\u0000' | `char` (but unsigned 2-byte!) |
| `boolean` | 1 bit (JVM uses 4 bytes internally) | true/false | false | `bool` |

### Key Differences from C++

```java
// Java char is 2-byte Unicode, C++ char is 1-byte ASCII
char c = '字';  // Valid in Java! Unicode character

// Java has no unsigned types (except char for 0-65535)
// C++: unsigned int, unsigned long, etc. — not in Java

// Integer literal suffixes
long x = 100L;    // L for long (l also works but uppercase preferred)
float f = 3.14f;  // f for float
double d = 3.14;  // default for decimal literals

// Binary, hex, octal literals (Java 7+)
int bin = 0b1010;    // binary → 10
int hex = 0xFF;      // hex → 255
int oct = 017;       // octal → 15

// Underscore in literals (Java 7+) for readability
int million = 1_000_000;
long creditCard = 1234_5678_9012_3456L;
```

## Wrapper Classes

Every primitive has a corresponding Wrapper class (object form):

| Primitive | Wrapper | Pool Range |
|-----------|---------|------------|
| `int` | `Integer` | -128 to 127 cached |
| `long` | `Long` | -128 to 127 cached |
| `double` | `Double` | No cache |
| `boolean` | `Boolean` | true and false cached |
| `char` | `Character` | 0-127 cached |

### Autoboxing and Unboxing

Java automatically converts between primitive and wrapper:
```java
// Autoboxing: int → Integer (automatic)
Integer x = 5;          // Actually: Integer x = Integer.valueOf(5);

// Unboxing: Integer → int (automatic)
int y = x;              // Actually: int y = x.intValue();

// Danger: NullPointerException from unboxing
Integer a = null;
int b = a;              // NullPointerException! unboxing null crashes
```

### The Integer Cache Trap (Common Interview Trick!)

```java
Integer a = 127;
Integer b = 127;
System.out.println(a == b);    // TRUE  (same cached object)

Integer c = 128;
Integer d = 128;
System.out.println(c == d);    // FALSE (different objects, new allocation)

// ALWAYS use .equals() for Integer comparison:
System.out.println(c.equals(d));  // TRUE
```

Integer.valueOf() caches values from -128 to 127. Outside this range, new objects are created. `==` on objects compares references, not values.

## Variable Declaration

```java
// Local variables — must be explicitly initialized before use
int x;
// System.out.println(x);  // COMPILE ERROR: variable x might not have been initialized

// Instance variables — initialized to defaults (0, null, false)
class MyClass {
    int count;      // default 0
    String name;    // default null
    boolean flag;   // default false
}

// Final variables — must be assigned exactly once
final int MAX = 100;
// MAX = 200;  // COMPILE ERROR

// var (Java 10+ local type inference)
var list = new ArrayList<String>();   // type inferred as ArrayList<String>
var s = "hello";                      // String
// var x;  // ERROR — can't infer type without initializer
```

## String Internals

Strings are objects in Java, but they behave like value types due to immutability:

```java
String s1 = "hello";      // String literal — goes to String Pool (Metaspace)
String s2 = "hello";      // Reuses same object from pool
String s3 = new String("hello");  // New object in heap, NOT from pool

System.out.println(s1 == s2);      // TRUE  (same pool object)
System.out.println(s1 == s3);      // FALSE (different objects)
System.out.println(s1.equals(s3)); // TRUE  (same content)

// intern() — force a string into the pool
String s4 = s3.intern();
System.out.println(s1 == s4);      // TRUE (s4 is now the pooled version)
```

### String Immutability

```java
String s = "hello";
s = s + " world";  // Does NOT modify original string!
                   // Creates a new String object "hello world"
                   // Old "hello" object eligible for GC
```

For repeated string building in a loop, use **StringBuilder** (mutable, not thread-safe) or **StringBuffer** (mutable, thread-safe):

```java
// SLOW (creates N intermediate String objects)
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i;
}

// FAST (single mutable buffer)
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);
}
String result = sb.toString();
```

## Interview Questions
- **Q: What is the difference between `==` and `.equals()` in Java?**
  A: `==` compares references (memory addresses) for objects, or values for primitives. `.equals()` compares logical content. Always use `.equals()` for String and object comparison. For primitives, `==` is correct.

- **Q: Why is String immutable in Java?**
  A: Security (strings used in class loading, network connections, file paths — mutable would be exploitable), String pool efficiency (safe to share same object), and thread safety (immutable objects are inherently thread-safe). Hashcode can also be cached.

- **Q: What is autoboxing and when is it dangerous?**
  A: Auto-conversion between primitive and wrapper type. Dangerous when unboxing null (NPE), in performance-sensitive loops (creates many wrapper objects), and when using `==` on Integer objects outside -128 to 127 range.

---

# 11. Operators

## Operator Types

Most operators are identical to C++. Key differences:

```java
// Arithmetic: +, -, *, /, %
int a = 10 / 3;     // 3 (integer division, same as C++)
double b = 10.0 / 3; // 3.333...

// Bitwise: &, |, ^, ~, <<, >>, >>>
int x = -1;
System.out.println(x >> 1);   // -1 (arithmetic shift, fills with sign bit)
System.out.println(x >>> 1);  // 2147483647 (logical shift, fills with 0)
// C++ has only >> which is implementation-defined for negatives
// Java adds >>> (unsigned right shift) — always fills with 0

// Ternary
int max = (a > b) ? a : b;

// instanceof — type checking (no direct C++ equivalent cleanly)
if (obj instanceof String s) {  // Java 16+ pattern matching instanceof
    System.out.println(s.length());  // s is automatically cast
}

// String concatenation with +
String result = "Value: " + 42;  // int auto-converted to String
```

## Integer Overflow

```java
// Java silently overflows (wraps around), just like C++
int max = Integer.MAX_VALUE;  // 2147483647
System.out.println(max + 1);  // -2147483648 (wraps!)

// Safe: use Math.addExact() which throws ArithmeticException on overflow
int safe = Math.addExact(max, 1);  // throws ArithmeticException
```

---

# 12. Control Flow

## Same as C++ (mostly)

```java
// if-else
if (x > 0) { ... }
else if (x < 0) { ... }
else { ... }

// for loop
for (int i = 0; i < 10; i++) { ... }

// enhanced for (for-each) — like C++ range-based for
int[] arr = {1, 2, 3, 4, 5};
for (int n : arr) {
    System.out.println(n);
}

// while / do-while
while (condition) { ... }
do { ... } while (condition);
```

## Switch Statement / Expression

```java
// Traditional switch (same as C++)
switch (day) {
    case 1: System.out.println("Monday"); break;
    case 2: System.out.println("Tuesday"); break;
    default: System.out.println("Other");
}

// Modern switch expression (Java 14+) — no break needed, returns value
String name = switch (day) {
    case 1 -> "Monday";
    case 2 -> "Tuesday";
    case 3, 4, 5 -> "Mid-week";    // multiple cases
    default -> "Weekend";
};

// Switch with blocks and yield (Java 14+)
int result = switch (op) {
    case "add" -> a + b;
    case "multiply" -> {
        int product = a * b;
        yield product;  // yield returns value from block
    }
    default -> throw new IllegalArgumentException("Unknown: " + op);
};
```

## Exception Handling

```java
// Basic try-catch-finally
try {
    int result = 10 / 0;
} catch (ArithmeticException e) {
    System.out.println("Error: " + e.getMessage());
} catch (Exception e) {
    System.out.println("General error");
} finally {
    System.out.println("Always runs — cleanup here");
}

// Multi-catch (Java 7+)
try {
    ...
} catch (IOException | SQLException e) {
    // handles both exception types
}

// try-with-resources (Java 7+) — auto-closes resources
try (FileReader fr = new FileReader("file.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line = br.readLine();
}  // fr and br are automatically closed here, even if exception occurs
// This is the Java equivalent of C++ RAII
```

### Exception Hierarchy

```
Throwable
├── Error (don't catch — JVM-level problems)
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── VirtualMachineError
└── Exception
    ├── RuntimeException (Unchecked — no need to declare or catch)
    │   ├── NullPointerException
    │   ├── ArrayIndexOutOfBoundsException
    │   ├── ClassCastException
    │   ├── IllegalArgumentException
    │   └── ArithmeticException
    └── Checked Exceptions (MUST handle or declare with throws)
        ├── IOException
        ├── SQLException
        └── ClassNotFoundException
```

**Checked vs Unchecked:**
```java
// Checked — must handle it:
void readFile() throws IOException {  // OR use try-catch
    FileReader fr = new FileReader("file.txt");  // throws IOException
}

// Unchecked — no requirement to handle:
void divide(int a, int b) {
    int result = a / b;  // may throw ArithmeticException — no throws required
}
```

C++ has no concept of checked exceptions — all exceptions are unchecked.

## Interview Questions
- **Q: What is the difference between checked and unchecked exceptions?**
  A: Checked exceptions (IOException, SQLException) are checked at compile time — you must either handle them with try-catch or declare them with `throws`. Unchecked exceptions (RuntimeException subclasses) are not enforced at compile time. The debate: checked forces handling but creates verbose code; unchecked gives flexibility but errors may be missed.

- **Q: What is try-with-resources?**
  A: Java 7+ syntax that automatically closes resources (anything implementing `AutoCloseable`) at the end of the try block, whether or not an exception occurs. It's Java's RAII equivalent.

---

# 13. Methods in Java

## Method Signature

```java
// access_modifier return_type methodName(params) throws exceptions
public static int add(int a, int b) throws ArithmeticException {
    return a + b;
}
```

## Pass by Value (Always, in Java)

Java is **always pass-by-value**. For objects, the value passed is the **reference** (pointer), not the object itself:

```java
// Primitives: copy of value passed
void modify(int x) {
    x = 100;  // only modifies local copy
}
int n = 5;
modify(n);
System.out.println(n);  // 5 — unchanged

// Objects: copy of REFERENCE passed
void modify(StringBuilder sb) {
    sb.append(" world");  // modifies the object (both refs point to same object)
}
StringBuilder s = new StringBuilder("hello");
modify(s);
System.out.println(s);  // "hello world" — modified!

// But reassigning the reference doesn't affect the caller:
void reassign(StringBuilder sb) {
    sb = new StringBuilder("new");  // only local ref reassigned
}
StringBuilder s = new StringBuilder("hello");
reassign(s);
System.out.println(s);  // "hello" — s still points to original
```

C++ developers: Java references are like C++ pointers, not C++ references. You can't pass by reference in Java the way `void f(int& x)` does.

## Varargs

```java
// Variable arguments — internally an array
int sum(int... nums) {
    int total = 0;
    for (int n : nums) total += n;
    return total;
}

sum(1, 2, 3);           // 6
sum(1, 2, 3, 4, 5);     // 15
sum(new int[]{1, 2, 3}); // also valid
```

## Method Overloading

Same method name, different parameter list (compile-time polymorphism):

```java
void print(int x)    { System.out.println("int: " + x); }
void print(double x) { System.out.println("double: " + x); }
void print(String x) { System.out.println("String: " + x); }

print(5);       // int: 5
print(5.0);     // double: 5.0
print("hello"); // String: hello
```

Resolution happens at compile time based on argument types. Note: Return type alone doesn't make methods different.

## Recursion

```java
int factorial(int n) {
    if (n <= 1) return 1;         // base case
    return n * factorial(n - 1);  // recursive case
}
```

Java does NOT optimize tail recursion (unlike some functional languages). Deep recursion causes StackOverflowError.

---

# 14. Classes & Objects

## Class Declaration

```java
public class BankAccount {
    // ── FIELDS ──────────────────────────────────────────
    private String owner;        // instance field
    private double balance;      // instance field
    private static int count;    // class field (shared across all instances)

    // ── CONSTRUCTORS ─────────────────────────────────────
    // Default constructor (generated automatically if none written)
    public BankAccount() {
        this("Unknown", 0.0);    // delegates to parameterized constructor
    }

    // Parameterized constructor
    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;       // this disambiguates field from param
        this.balance = initialBalance;
        BankAccount.count++;      // access static field
    }

    // ── METHODS ──────────────────────────────────────────
    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Amount must be positive");
        this.balance += amount;
    }

    public double getBalance() { return balance; }
    public String getOwner()   { return owner; }
    public static int getCount() { return count; }

    // ── toString ──────────────────────────────────────────
    @Override
    public String toString() {
        return "BankAccount{owner=" + owner + ", balance=" + balance + "}";
    }
}
```

## Constructor Chaining

```java
class Employee {
    String name;
    int age;
    String department;

    Employee(String name) {
        this(name, 25);          // calls Employee(String, int)
    }

    Employee(String name, int age) {
        this(name, age, "General");  // calls Employee(String, int, String)
    }

    Employee(String name, int age, String department) {
        this.name = name;
        this.age = age;
        this.department = department;
    }
}
```

## Inheritance

```java
class Animal {
    String name;

    Animal(String name) {
        this.name = name;
    }

    void sound() {
        System.out.println("...");
    }

    void breathe() {
        System.out.println(name + " breathes air");
    }
}

class Dog extends Animal {
    String breed;

    Dog(String name, String breed) {
        super(name);        // MUST be first statement — calls parent constructor
        this.breed = breed;
    }

    @Override             // annotation verifies we're actually overriding
    void sound() {
        System.out.println(name + " barks!");
    }
}

// Usage
Animal a = new Dog("Rex", "Lab");  // polymorphism
a.sound();    // "Rex barks!" — dynamic dispatch calls Dog's version
a.breathe();  // "Rex breathes air" — inherited from Animal
```

## this and super

```java
class Parent {
    int x = 10;
    void show() { System.out.println("Parent x=" + x); }
}

class Child extends Parent {
    int x = 20;   // shadows Parent's x

    void show() {
        System.out.println("Child x=" + x);     // this.x = 20
        System.out.println("Parent x=" + super.x); // super.x = 10
        super.show();                              // calls Parent's show()
    }
}
```

## Static vs Instance

```java
class Counter {
    static int total = 0;  // ONE copy, shared by all Counter objects
    int myCount = 0;       // each Counter has its OWN myCount

    void increment() {
        myCount++;   // this instance's count
        total++;     // global count across all instances
    }

    static void reset() {
        total = 0;
        // myCount = 0;  // ERROR: can't access instance field from static method
    }
}

Counter c1 = new Counter(); c1.increment();
Counter c2 = new Counter(); c2.increment(); c2.increment();
System.out.println(Counter.total);  // 3 (all increments)
System.out.println(c1.myCount);     // 1
System.out.println(c2.myCount);     // 2
```

## @Override, @Deprecated, @SuppressWarnings

Annotations are metadata attached to code elements:

```java
@Override           // Compiler verifies parent has this method — catches typos
public String toString() { ... }

@Deprecated         // Signals old API — compiler warns users
public void oldMethod() { ... }

@SuppressWarnings("unchecked")   // Suppresses specific compiler warning
public void rawTypeMethod() { ... }
```

## Interview Questions
- **Q: Can a constructor be private?**
  A: Yes. Used in Singleton pattern (prevents external instantiation) and factory method patterns.

- **Q: What is the difference between `this()` and `super()` in constructors?**
  A: `this()` calls another constructor in the same class. `super()` calls the parent class constructor. Both must be the first statement in a constructor — you can't use both.

- **Q: Can you override static methods in Java?**
  A: No — static methods are resolved at compile time based on reference type, not at runtime based on object type. This is called **method hiding** not overriding. The `@Override` annotation will reject static methods.

---

# 15. Java Keywords — Deep Dive

## `final`

The most overloaded keyword — means different things in different contexts:

```java
// 1. final VARIABLE — cannot be reassigned
final int MAX = 100;
// MAX = 200;  // COMPILE ERROR

// 2. final FIELD — must be initialized in declaration or every constructor
class Circle {
    final double PI = 3.14159;   // compile-time constant
    final double radius;

    Circle(double r) {
        this.radius = r;  // OK — initialized in constructor
    }
}

// 3. final METHOD — cannot be overridden in subclasses
class Parent {
    final void critical() { ... }   // no subclass can change this behavior
}

// 4. final CLASS — cannot be extended (subclassed)
final class String { ... }     // String in Java is final — you can't extend it
final class Integer { ... }    // all wrapper classes are final

// 5. final PARAMETER — can't reassign the parameter variable
void process(final int x) {
    // x = 10;  // COMPILE ERROR
}
```

**C++ equivalents:**
- `final` variable → `const`
- `final` method → `final` (C++11)
- `final` class → `final` (C++11)

## `static`

```java
class MathUtils {
    // Static field — shared state, no instance needed
    static final double PI = 3.14159;

    // Static method — utility functions
    static double circleArea(double r) {
        return PI * r * r;
    }

    // Static nested class — doesn't need outer instance
    static class Vector {
        double x, y;
    }

    // Static initializer block — runs once when class loads
    static {
        System.out.println("MathUtils class loaded");
    }
}

// Usage without creating instance:
double area = MathUtils.circleArea(5.0);
```

## `abstract`

```java
// Abstract class — cannot be instantiated, may have abstract methods
abstract class Shape {
    String color;

    Shape(String color) { this.color = color; }

    // Abstract method — no body, subclasses MUST implement
    abstract double area();

    // Concrete method — subclasses inherit (can override)
    void describe() {
        System.out.println(color + " shape with area " + area());
    }
}

class Circle extends Shape {
    double radius;

    Circle(String color, double radius) {
        super(color);
        this.radius = radius;
    }

    @Override
    double area() { return Math.PI * radius * radius; }
}

// Shape s = new Shape("red");  // ERROR — can't instantiate abstract class
Shape s = new Circle("red", 5);  // OK — concrete subclass
s.describe();  // "red shape with area 78.539..."
```

## `interface`

```java
// Interface — pure contract, all methods public by default
interface Payable {
    void pay(double amount);           // abstract by default
    double getBalance();               // abstract by default

    // Default method (Java 8+) — has implementation, subclasses can override
    default String getStatus() {
        return "Balance: " + getBalance();
    }

    // Static method (Java 8+) — utility, not inherited
    static boolean isValidAmount(double amount) {
        return amount > 0;
    }

    // Constant — implicitly public static final
    int MAX_TRANSACTIONS = 1000;
}

// Implementing interface
class Wallet implements Payable {
    private double balance;

    @Override
    public void pay(double amount) {
        if (!Payable.isValidAmount(amount)) throw new IllegalArgumentException();
        balance -= amount;
    }

    @Override
    public double getBalance() { return balance; }
}

// Multiple interfaces
class SuperWallet implements Payable, Serializable, Comparable<SuperWallet> {
    ...
}
```

### Abstract Class vs Interface

| Feature | Abstract Class | Interface |
|---------|---------------|-----------|
| Instantiation | No | No |
| Fields | Yes (any type) | Only `public static final` |
| Constructor | Yes | No |
| Method types | Abstract + concrete | Abstract + default + static |
| Inheritance | `extends` (single) | `implements` (multiple) |
| Use when | Shared state/behavior | Capability contract |

## `synchronized`

```java
class SafeCounter {
    private int count = 0;

    // Synchronized method — only one thread at a time can execute this
    public synchronized void increment() {
        count++;  // count++ is actually read-modify-write (not atomic)
    }

    // Synchronized block — finer-grained control
    public void incrementBlock() {
        synchronized (this) {  // lock on 'this' object
            count++;
        }
    }

    // Static synchronized — locks on the Class object
    public static synchronized void staticMethod() { ... }
}
```

## `volatile`

```java
class Server {
    private volatile boolean running = true;   // visible across all threads

    public void stop() { running = false; }

    public void run() {
        while (running) {    // always reads fresh value from main memory
            processRequest();
        }
    }
}
```

`volatile` guarantees visibility but NOT atomicity. `count++` is still not thread-safe with volatile. Use `AtomicInteger` for atomic operations.

## `transient`

```java
class UserSession implements Serializable {
    String username;
    transient String password;    // NOT serialized — excluded from byte stream
    transient Connection dbConn;  // NOT serialized — can't serialize a DB connection

    // When deserialized, password and dbConn will be null
}
```

C++ has no direct equivalent — serialization frameworks handle exclusion differently.

## `native`

```java
public class SystemInfo {
    // Implemented in C/C++, loaded from a native library
    public native long getProcessId();

    static {
        System.loadLibrary("sysinfo");  // loads libsysinfo.so (Linux) or sysinfo.dll (Windows)
    }
}
```

This is how Java interfaces with platform-specific code via JNI (Java Native Interface). Used in low-level system code, graphics drivers, hardware interfaces.

## `this`

```java
class Builder {
    private String name;
    private int value;

    // 1. Disambiguate field vs parameter
    Builder setName(String name) {
        this.name = name;    // this.name = field, name = parameter
        return this;         // 2. Return current instance (for chaining)
    }

    Builder setValue(int value) {
        this.value = value;
        return this;
    }

    // 3. Call another constructor
    Builder() {
        this("default", 0);
    }

    Builder(String name, int value) {
        this.name = name;
        this.value = value;
    }
}

// Method chaining using 'return this'
new Builder().setName("test").setValue(42);
```

## `super`

```java
class Animal {
    String name = "Animal";
    void speak() { System.out.println("..."); }
}

class Dog extends Animal {
    String name = "Dog";    // shadows Animal's name

    void speak() {
        System.out.println(name);         // Dog
        System.out.println(super.name);   // Animal — access parent field
        super.speak();                    // calls Animal.speak()
    }

    Dog() {
        super();  // calls Animal() — implicit if you don't write it
    }
}
```

## `instanceof` (and Pattern Matching, Java 16+)

```java
// Traditional
if (obj instanceof String) {
    String s = (String) obj;   // need explicit cast
    System.out.println(s.length());
}

// Pattern matching (Java 16+) — cleaner, no cast needed
if (obj instanceof String s) {
    System.out.println(s.length());  // s is already cast
}

// With switch (Java 21)
String result = switch (obj) {
    case Integer i -> "int: " + i;
    case String s  -> "string: " + s;
    case null      -> "null";
    default        -> "other";
};
```

## `enum`

```java
// Basic enum
enum Direction { NORTH, SOUTH, EAST, WEST }

// Enum with fields and methods (much richer than C++ enum)
enum Planet {
    MERCURY(3.303e+23, 2.4397e6),
    VENUS  (4.869e+24, 6.0518e6),
    EARTH  (5.976e+24, 6.37814e6);

    private final double mass;     // each enum constant has these
    private final double radius;

    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }

    double surfaceGravity() {
        final double G = 6.67300E-11;
        return G * mass / (radius * radius);
    }
}

// Usage
Planet p = Planet.EARTH;
System.out.println(p.surfaceGravity());  // 9.802...

// Enum in switch
switch (p) {
    case EARTH  -> System.out.println("Home");
    case MARS   -> System.out.println("Red planet");
    default     -> System.out.println("Space");
}

// Enum methods
Direction.values();              // array of all values: [NORTH, SOUTH, EAST, WEST]
Direction.valueOf("NORTH");      // Direction.NORTH
Direction.NORTH.ordinal();       // 0 (index)
Direction.NORTH.name();          // "NORTH"
```

Enums in Java are full classes — they can implement interfaces, have fields, methods, and constructors. Far more powerful than C++ enums.

---

# 16. Modern Java: Records, Sealed Classes, Enums

## Records (Java 16+)

Records are immutable data carriers — like C++ structs but with auto-generated boilerplate:

```java
// Traditional way (verbose)
class Point {
    private final int x;
    private final int y;

    Point(int x, int y) { this.x = x; this.y = y; }
    int x() { return x; }
    int y() { return y; }

    @Override
    public boolean equals(Object o) { ... }

    @Override
    public int hashCode() { ... }

    @Override
    public String toString() { return "Point[x=" + x + ", y=" + y + "]"; }
}

// Record way (compact!)
record Point(int x, int y) { }

// Auto-generated:
// - Constructor: Point(int x, int y)
// - Accessors: x(), y()
// - equals(), hashCode(), toString()
// Fields are private final automatically

Point p = new Point(3, 4);
System.out.println(p.x());           // 3
System.out.println(p);               // Point[x=3, y=4]

// Compact constructor (custom validation)
record Range(int min, int max) {
    Range {   // compact constructor — params already set, this validates
        if (min > max) throw new IllegalArgumentException("min > max");
    }
}
```

Records are ideal for DTOs, value objects, API responses.

## Sealed Classes (Java 17+)

Sealed classes restrict which classes can extend them — useful for exhaustive pattern matching:

```java
sealed interface Shape permits Circle, Rectangle, Triangle { }

record Circle(double radius) implements Shape { }
record Rectangle(double width, double height) implements Shape { }
record Triangle(double base, double height) implements Shape { }

// Now the compiler knows ALL possible shapes
double area(Shape shape) {
    return switch (shape) {
        case Circle c      -> Math.PI * c.radius() * c.radius();
        case Rectangle r   -> r.width() * r.height();
        case Triangle t    -> 0.5 * t.base() * t.height();
        // No default needed — compiler knows all cases are covered!
    };
}
```

Sealed classes make illegal states unrepresentable and enable exhaustive switch.

## Text Blocks (Java 15+)

```java
// Old way — awkward escaping
String json = "{\n" +
              "  \"name\": \"Alice\",\n" +
              "  \"age\": 30\n" +
              "}";

// Text block — natural multiline string
String json = """
              {
                "name": "Alice",
                "age": 30
              }
              """;
```

---

# Interview Quick Reference

## JVM Internals

| Question | Answer |
|----------|--------|
| JDK vs JRE vs JVM | JVM=executor, JRE=JVM+libs, JDK=JRE+tools |
| What is bytecode? | Platform-neutral instructions for JVM |
| What is JIT? | Runtime compilation of hot bytecode to native code |
| Heap vs Stack | Heap=objects(shared), Stack=frames(per thread) |
| What replaced PermGen? | Metaspace (Java 8+, native memory) |
| What is GC root? | Start points for reachability: stack vars, static fields |
| What causes StackOverflow? | Infinite recursion exhausting stack space |
| What is the Integer cache? | -128 to 127 are cached; outside this range new objects |

## Key Java vs C++ Differences

| Topic | C++ | Java |
|-------|-----|------|
| Memory mgmt | Manual delete | GC |
| Pointers | Raw pointers | No raw pointers (references only) |
| Multiple inheritance | Yes (classes) | No (interfaces only) |
| unsigned types | Yes | No (except char) |
| Right shift | >> (signed behavior varies) | >> arithmetic, >>> logical |
| String type | Not built-in | First-class, immutable, pooled |
| Destructor | Yes, deterministic | finalize() deprecated, use Closeable |
| Header files | Required | No — single source file |
| Default access | private in class | package-private |
| goto | Yes (limited) | No (labels exist for break/continue) |

---

*End of Part 1: Java Internals & Syntax*
*Next: Part 2 (Object-Oriented Programming), Part 3 (Java Collections Framework)*
