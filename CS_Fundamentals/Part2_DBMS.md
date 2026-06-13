# Database Management Systems Complete Guide

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

