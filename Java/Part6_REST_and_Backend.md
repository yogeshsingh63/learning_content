# REST APIs and Backend Engineering

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

