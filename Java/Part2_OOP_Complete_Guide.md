# Part 2: Object-Oriented Programming — Complete Mastery Guide
### C++ vs Java | From First Principles | Backend SDE Interview Handbook

---

> **How to use this document:** Every concept is taught from first principles, with side-by-side C++ and Java code, real-world analogies, ASCII diagrams, and interview questions. Read linearly or jump to sections.

---

# Table of Contents

1. [What is OOP? Why Does It Exist?](#1-what-is-oop-why-does-it-exist)
2. [Classes & Objects](#2-classes--objects)
3. [Constructors & Destructors vs Garbage Collection](#3-constructors--destructors-vs-garbage-collection)
4. [Encapsulation](#4-encapsulation)
5. [Abstraction](#5-abstraction)
6. [Inheritance](#6-inheritance)
7. [Polymorphism](#7-polymorphism)
8. [Method Overloading vs Overriding](#8-method-overloading-vs-overriding)
9. [Virtual Functions & Dynamic Binding](#9-virtual-functions--dynamic-binding)
10. [Abstract Classes & Interfaces](#10-abstract-classes--interfaces)
11. [Multiple Inheritance & the Diamond Problem](#11-multiple-inheritance--the-diamond-problem)
12. [Composition vs Inheritance](#12-composition-vs-inheritance)
13. [Association, Aggregation, Composition, Dependency](#13-association-aggregation-composition-dependency)
14. [SOLID Principles](#14-solid-principles)
15. [Design Patterns](#15-design-patterns)
16. [Interview Quick Reference](#16-interview-quick-reference)

---

# 1. What is OOP? Why Does It Exist?

## The Problem OOP Solves

Before OOP, programs were written procedurally — a sequence of functions acting on global data. As programs grew large, this caused:

- **Data scattered everywhere** — any function could modify any global variable
- **No logical grouping** — data and the operations on it lived in different places
- **Hard to reuse** — copying code instead of extending it
- **Hard to maintain** — changing one function could break unrelated parts

```
Procedural World (C-style):
──────────────────────────
Global: int balance, char name[50], int accountId

deposit(int amount)     { balance += amount; }
withdraw(int amount)    { balance -= amount; }
printAccount()          { printf(name, balance); }
// Any code anywhere can corrupt 'balance' directly
```

OOP's answer: **bundle data and the functions that operate on it into a single unit called a class, and control access.**

## The Four Pillars of OOP

```
┌──────────────────────────────────────────────────────────┐
│                    OOP PILLARS                           │
│                                                          │
│  ENCAPSULATION      ABSTRACTION                          │
│  "Hide the data"    "Hide the complexity"                │
│  private fields     abstract classes / interfaces        │
│  public methods     show WHAT, not HOW                   │
│                                                          │
│  INHERITANCE        POLYMORPHISM                         │
│  "Reuse & extend"   "One interface, many forms"          │
│  extends/is-a       method overriding / dynamic dispatch │
└──────────────────────────────────────────────────────────┘
```

---

# 2. Classes & Objects

## Theory

A **class** is a blueprint — it defines what data (fields) an entity has and what operations (methods) it can perform. An **object** is a concrete instance of a class — an actual entity created from the blueprint, living in memory.

```
Class (Blueprint)           Object (Instance)
─────────────────           ─────────────────
class Car {                 Car myCar = new Car("Tesla", "Red");
  String brand;             // myCar: brand="Tesla", color="Red"
  String color;
  void drive() {...}        Car yourCar = new Car("BMW", "Black");
}                           // yourCar: brand="BMW", color="Black"
```

Each object has its own **state** (field values) but shares **behavior** (method definitions) with all instances of the class.

## C++ vs Java: Class Declaration

```cpp
// C++ — declaration in .h, definition in .cpp
// Person.h
class Person {
private:
    std::string name;
    int age;

public:
    Person(std::string name, int age);
    std::string getName() const;
    void birthday();
    ~Person();  // destructor
};

// Person.cpp
Person::Person(std::string n, int a) : name(n), age(a) {}
std::string Person::getName() const { return name; }
void Person::birthday() { age++; }
Person::~Person() { /* cleanup */ }
```

```java
// Java — everything in one .java file, no header/source split
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() { return name; }

    public void birthday() { age++; }

    @Override
    public String toString() {
        return "Person{name=" + name + ", age=" + age + "}";
    }
    // No destructor — GC handles memory
}
```

## Default Access Modifiers

| Access | C++ | Java |
|--------|-----|------|
| `public` | Accessible everywhere | Accessible everywhere |
| `private` | Accessible only within class | Accessible only within class |
| `protected` | Accessible in class + subclasses + same package | Accessible in class + subclasses + same package |
| Default (no keyword) | `private` in class, `public` in struct | **package-private** — accessible within same package |

Java's default (package-private) has no C++ equivalent — it's a package-level encapsulation boundary.

## Object Identity vs Equality

```cpp
// C++ — objects can exist on stack or heap
Person p1("Alice", 30);       // stack allocated — direct object
Person p2 = p1;               // copy — two separate objects

Person* p3 = new Person("Bob", 25);  // heap allocated — pointer
delete p3;                     // MANUAL cleanup required
```

```java
// Java — all objects on heap, variables hold references
Person p1 = new Person("Alice", 30);   // p1 is a reference to the heap object
Person p2 = p1;                        // p2 points to SAME object (not a copy!)
Person p3 = new Person("Alice", 30);   // p3 points to a DIFFERENT object

p1 == p2;          // true  (same reference / same memory address)
p1 == p3;          // false (different objects)
p1.equals(p3);     // true  (if equals() compares field values — need to override)
```

This is a critical Java vs C++ difference. In Java, `Person p2 = p1` creates an alias, not a copy. If you want a copy, you must implement it explicitly (via copy constructor pattern, `clone()`, or a factory method).

## Interview Questions

- **Q: What is the difference between a class and an object?**
  A: A class is a compile-time blueprint defining structure and behavior. An object is a runtime instance of that class, occupying memory with its own state. Class is like a house plan; objects are the actual houses built from it.

- **Q: In Java, when you do `Person p2 = p1`, does p2 get a copy of p1?**
  A: No. Both p1 and p2 point to the same object on the heap. Modifying p2.name also changes what p1.name sees, because they reference the same object. To get a separate copy, you need to explicitly copy fields or use a copy constructor pattern.

---

# 3. Constructors & Destructors vs Garbage Collection

## Constructors

Constructors initialize an object's state when it's created. They have the same name as the class and no return type.

```cpp
// C++ constructors
class Database {
    Connection* conn;
    string host;
    int port;

public:
    // Default constructor
    Database() : host("localhost"), port(5432), conn(nullptr) {}

    // Parameterized constructor
    Database(string h, int p) : host(h), port(p) {
        conn = new Connection(host, port);
    }

    // Copy constructor — C++ has this, Java doesn't (built-in)
    Database(const Database& other) : host(other.host), port(other.port) {
        conn = new Connection(host, port);  // deep copy — new connection
    }

    // Move constructor (C++11)
    Database(Database&& other) noexcept : host(move(other.host)),
                                          port(other.port),
                                          conn(other.conn) {
        other.conn = nullptr;  // transfer ownership
    }
};
```

```java
// Java constructors
public class Database {
    private Connection conn;
    private String host;
    private int port;

    // Default constructor (if no constructors written, Java provides empty one)
    public Database() {
        this("localhost", 5432);   // delegate to parameterized
    }

    // Parameterized constructor
    public Database(String host, int port) {
        this.host = host;
        this.port = port;
        this.conn = new Connection(host, port);
    }

    // No copy constructor in Java — copy by writing static factory or clone()
    // No move constructor — Java GC handles object lifetime
}
```

### Constructor Chaining with super()

```java
class Vehicle {
    String brand;
    int year;

    Vehicle(String brand, int year) {
        this.brand = brand;
        this.year = year;
    }
}

class Car extends Vehicle {
    int doors;

    Car(String brand, int year, int doors) {
        super(brand, year);   // MUST be first line — calls Vehicle constructor
        this.doors = doors;
    }

    Car(String brand) {
        this(brand, 2024, 4);  // this() delegates to above — also must be first
    }
}
```

Rules:
- `super()` or `this()` must be the **first statement** in a constructor
- If you don't write `super()`, Java inserts `super()` (no-arg) automatically — compile error if parent has no no-arg constructor

## Destructors (C++) vs GC (Java)

This is one of the most fundamental differences between C++ and Java.

### C++ Destructor — Deterministic Cleanup

```cpp
class FileHandler {
    FILE* file;
    char* buffer;

public:
    FileHandler(const char* path) {
        file = fopen(path, "r");
        buffer = new char[1024];  // allocate on heap
    }

    ~FileHandler() {
        // Called DETERMINISTICALLY when object goes out of scope or delete is called
        fclose(file);       // close file handle — OS resource
        delete[] buffer;    // free heap memory
        cout << "FileHandler destroyed" << endl;
    }
};

void process() {
    FileHandler fh("data.txt");   // constructor called
    // ... use fh ...
}   // <-- destructor called HERE, automatically, deterministically
```

The destructor runs at a **predictable, defined moment** — the moment the object is destroyed. This enables **RAII** (Resource Acquisition Is Initialization) — one of C++'s most powerful patterns.

### Java — No Destructor, GC is Non-Deterministic

```java
public class FileHandler implements AutoCloseable {
    private FileInputStream file;
    private byte[] buffer;

    public FileHandler(String path) throws IOException {
        file = new FileInputStream(path);
        buffer = new byte[1024];
    }

    // finalize() — DEPRECATED, DO NOT USE
    // Called by GC at some unknown future time, or NEVER if program exits first
    @Override
    protected void finalize() throws Throwable {
        // Unreliable — don't use for resource cleanup
    }

    // CORRECT Java approach: implement AutoCloseable
    @Override
    public void close() throws IOException {
        file.close();   // explicit cleanup
    }
}

// Use try-with-resources for automatic cleanup
void process() throws IOException {
    try (FileHandler fh = new FileHandler("data.txt")) {
        // ... use fh ...
    }   // close() called here automatically — Java's RAII equivalent
}
```

| Aspect | C++ Destructor | Java Garbage Collection |
|--------|---------------|------------------------|
| When called | Deterministically at object destruction | Non-deterministic (GC decides) |
| Can skip | Never (unless crash) | finalize() may never run |
| Resource cleanup | Natural via destructor | Must use try-with-resources / close() |
| Memory cleanup | Mandatory (you must delete) | Automatic (GC does it) |
| Pattern | RAII | AutoCloseable + try-with-resources |

## Interview Questions

- **Q: Does Java have a destructor?**
  A: No. Java had `finalize()` but it's deprecated and unreliable — the GC may never call it, and timing is non-deterministic. For resource cleanup (files, DB connections), implement `AutoCloseable` and use `try-with-resources`.

- **Q: What is RAII in C++?**
  A: Resource Acquisition Is Initialization — resources are acquired in the constructor and released in the destructor. Since destructors are called deterministically, resources are guaranteed to be released even if exceptions occur. Java's equivalent is `AutoCloseable` + `try-with-resources`.

---

# 4. Encapsulation

## Theory

Encapsulation means **bundling data (fields) with the methods that operate on that data, and restricting direct access to the data from outside the class.**

The goal: an object controls its own state. External code can only interact through a well-defined interface (public methods), not by poking at internal fields directly.

```
Without encapsulation:            With encapsulation:
─────────────────────            ───────────────────
account.balance = -1000;         account.withdraw(1000);
// No validation!                // withdraw() validates before changing
                                 // balance can NEVER be negative
```

## Implementation

```cpp
// C++
class BankAccount {
private:              // Direct access blocked from outside
    double balance;
    string owner;

public:
    BankAccount(string owner, double initial)
        : owner(owner), balance(initial) {}

    // Controlled access through methods (getters/setters)
    double getBalance() const { return balance; }
    string getOwner() const { return owner; }

    bool deposit(double amount) {
        if (amount <= 0) return false;  // validation
        balance += amount;
        return true;
    }

    bool withdraw(double amount) {
        if (amount <= 0 || amount > balance) return false;
        balance -= amount;
        return true;
    }
};
```

```java
// Java — identical concept, slightly different syntax
public class BankAccount {
    private double balance;     // hidden
    private String owner;       // hidden

    public BankAccount(String owner, double initial) {
        this.owner = owner;
        this.balance = initial;
    }

    public double getBalance() { return balance; }
    public String getOwner()   { return owner; }

    public boolean deposit(double amount) {
        if (amount <= 0) return false;
        balance += amount;
        return true;
    }

    public boolean withdraw(double amount) {
        if (amount <= 0 || amount > balance) return false;
        balance -= amount;
        return true;
    }
}
```

## Why Encapsulation Matters

**1. Validation:** The class enforces invariants. `balance` can never be negative — the class guarantees it.

**2. Flexibility to change internals:** If you store balance in cents internally instead of dollars, only the class changes — callers don't notice.

```java
// Internal change — balance now stored as long cents, not double dollars
// External API stays the same!
public double getBalance() {
    return balanceCents / 100.0;   // callers don't know how it's stored
}
```

**3. Immutability:** Make fields `final` and remove setters to create immutable objects — thread-safe by design.

```java
public final class Money {
    private final double amount;
    private final String currency;

    public Money(double amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }

    // Only getters, no setters — immutable
    public double getAmount() { return amount; }
    public String getCurrency() { return currency; }

    // Operations return NEW objects instead of mutating
    public Money add(Money other) {
        if (!currency.equals(other.currency)) throw new IllegalArgumentException();
        return new Money(amount + other.amount, currency);
    }
}
```

## Interview Questions

- **Q: What is encapsulation and why is it important?**
  A: Encapsulation bundles data and methods together and restricts external access to internal state. It's important for: maintaining invariants (no invalid states), hiding implementation details (change internals without affecting callers), and improving security and maintainability.

- **Q: What is the difference between encapsulation and data hiding?**
  A: Data hiding (private fields) is the mechanism. Encapsulation is the broader principle — it includes data hiding plus the idea that an object manages its own state through controlled public methods. Data hiding is part of encapsulation.

---

# 5. Abstraction

## Theory

Abstraction means **exposing only the relevant details to the user and hiding the underlying complexity.**

While encapsulation hides *how* data is stored, abstraction hides *how* operations are implemented. You tell users *what* something does, not *how* it does it.

```
Real World Analogy — Car:
  What you see (interface): steering wheel, pedals, gear shift
  What's hidden (implementation): engine combustion, transmission ratios,
                                   fuel injection timing, brake hydraulics

You don't need to understand the engine to drive the car.
```

## Abstraction in Code

In Java, abstraction is achieved through:
1. **Abstract classes** — partial implementation, force subclasses to complete it
2. **Interfaces** — pure contract, zero implementation (pre-Java 8)

```java
// Abstract class — defines WHAT operations exist (some HOW included)
abstract class PaymentProcessor {
    // Abstract — subclasses MUST implement (the "what")
    public abstract boolean processPayment(double amount, String account);
    public abstract boolean refund(double amount, String transactionId);

    // Concrete — shared implementation (the "how" for common behavior)
    public void logTransaction(String type, double amount) {
        System.out.println("[" + type + "] Amount: " + amount + " at " + System.currentTimeMillis());
    }

    public boolean validateAmount(double amount) {
        return amount > 0 && amount < 1_000_000;
    }
}

// Concrete implementations — each hides its own complexity
class StripeProcessor extends PaymentProcessor {
    private StripeClient client = new StripeClient();

    @Override
    public boolean processPayment(double amount, String account) {
        logTransaction("CHARGE", amount);
        // Complex Stripe API calls hidden from callers
        return client.charge(account, amount, "USD");
    }

    @Override
    public boolean refund(double amount, String transactionId) {
        return client.refund(transactionId, amount);
    }
}

class PayPalProcessor extends PaymentProcessor {
    @Override
    public boolean processPayment(double amount, String account) {
        logTransaction("PAYPAL_CHARGE", amount);
        // Complex PayPal API calls hidden
        return PayPalAPI.execute(account, amount);
    }

    @Override
    public boolean refund(double amount, String transactionId) {
        return PayPalAPI.refund(transactionId);
    }
}

// Caller only sees the abstract interface
PaymentProcessor processor = new StripeProcessor();
processor.processPayment(99.99, "user@example.com");
// Caller doesn't know or care it's Stripe internally
```

## Abstraction vs Encapsulation — The Confusion

These are often confused. Here's the clear distinction:

| | Encapsulation | Abstraction |
|--|--------------|------------|
| **Focus** | Hiding DATA (fields) | Hiding COMPLEXITY (implementation) |
| **Mechanism** | Access modifiers (private/public) | Abstract classes, interfaces |
| **Question answered** | "How is the data protected?" | "What can this object do?" |
| **Goal** | Data protection, invariants | Simplified mental model for callers |
| **Example** | `private double balance` with getter | `abstract boolean processPayment(...)` |

Both work together: encapsulation hides the *state*, abstraction hides the *behavior complexity*.

## Interview Questions

- **Q: What is the difference between abstraction and encapsulation?**
  A: Encapsulation hides internal data through access modifiers — it protects state. Abstraction hides implementation complexity behind a simple interface — it simplifies what callers need to know. Encapsulation is about *data protection*; abstraction is about *complexity management*.

---

# 6. Inheritance

## Theory

Inheritance allows a class to **reuse and extend** the structure and behavior of another class. The child class (subclass) inherits all accessible fields and methods from the parent class (superclass) and can add new ones or override existing ones.

```
                    Animal
                   /      \
                Dog        Cat
               /   \
           Puppy  GuideDog

"is-a" relationship:
  Dog is an Animal ✓
  Puppy is a Dog ✓  (and transitively, Puppy is an Animal ✓)
  Dog is a Cat ✗
```

## Single Inheritance

```cpp
// C++
class Animal {
protected:          // accessible to subclasses
    string name;
    int age;

public:
    Animal(string name, int age) : name(name), age(age) {}

    virtual void speak() {     // virtual = can be overridden
        cout << name << " makes a sound" << endl;
    }

    void breathe() {
        cout << name << " breathes" << endl;
    }
};

class Dog : public Animal {   // public inheritance
    string breed;

public:
    Dog(string name, int age, string breed)
        : Animal(name, age), breed(breed) {}   // call parent constructor

    void speak() override {    // override (C++11 keyword)
        cout << name << " barks!" << endl;
    }

    void fetch() {
        cout << name << " fetches!" << endl;
    }
};
```

```java
// Java
public class Animal {
    protected String name;    // accessible to subclasses
    protected int age;

    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void speak() {
        System.out.println(name + " makes a sound");
    }

    public void breathe() {
        System.out.println(name + " breathes");
    }
}

public class Dog extends Animal {
    private String breed;

    public Dog(String name, int age, String breed) {
        super(name, age);   // call parent constructor — MUST be first line
        this.breed = breed;
    }

    @Override
    public void speak() {
        System.out.println(name + " barks!");
    }

    public void fetch() {
        System.out.println(name + " fetches!");
    }
}
```

## Inheritance Chain

```java
class LivingThing {
    void breathe() { System.out.println("breathing..."); }
}

class Animal extends LivingThing {
    String name;
    Animal(String n) { name = n; }
    void eat() { System.out.println(name + " eats"); }
}

class Dog extends Animal {
    Dog(String n) { super(n); }
    void bark() { System.out.println(name + " barks"); }
}

class Labrador extends Dog {
    Labrador(String n) { super(n); }
    void retrieve() { System.out.println(name + " retrieves"); }
}

// Labrador inherits: breathe(), eat(), bark(), retrieve()
Labrador lab = new Labrador("Buddy");
lab.breathe();    // from LivingThing
lab.eat();        // from Animal
lab.bark();       // from Dog
lab.retrieve();   // from Labrador
```

## C++ Inheritance Types (not in Java)

C++ has three inheritance types — Java only has `public` equivalent:

```cpp
class Base { public: int x; protected: int y; private: int z; };

class PublicChild    : public Base    { };  // x=public, y=protected, z=inaccessible
class ProtectedChild : protected Base { };  // x=protected, y=protected, z=inaccessible
class PrivateChild   : private Base   { };  // x=private, y=private, z=inaccessible
```

Java always behaves like C++ `public` inheritance — subclass doesn't change the visibility of inherited members.

## Preventing Inheritance

```cpp
// C++11 — final class
class Singleton final { ... };  // cannot be subclassed

// C++11 — final method
virtual void configure() final { ... }  // cannot be overridden
```

```java
// Java
public final class String { ... }     // String cannot be subclassed

public class Parent {
    public final void configure() { ... }  // cannot be overridden
}
```

## Interview Questions

- **Q: What is the difference between `protected` and `private` in the context of inheritance?**
  A: `private` members are accessible only within the declaring class — not even subclasses can access them. `protected` members are accessible within the declaring class AND all subclasses (and same package in Java). Use `protected` when subclasses need access to internals; use `private` when you want to keep internals truly hidden even from subclasses.

- **Q: What happens if you don't call `super()` in a Java subclass constructor?**
  A: Java inserts an implicit `super()` (no-arg call). If the parent class has no no-argument constructor, this causes a compile error — you must explicitly call the appropriate `super(...)`.

---

# 7. Polymorphism

## Theory

Polymorphism means **"many forms"** — the same interface can work with objects of different types, with the correct behavior selected at runtime.

This is what makes OOP code extensible: you write code against a base type, and it works correctly with any subtype — even ones written in the future.

```
Animal animal;

animal = new Dog();  → animal.speak() prints "barks!"
animal = new Cat();  → animal.speak() prints "meows!"
animal = new Bird(); → animal.speak() prints "chirps!"

Same code (animal.speak()) — different behavior based on actual object type.
This selection of the right method at runtime = dynamic dispatch.
```

## Runtime Polymorphism (Method Overriding)

```java
class Shape {
    public double area() { return 0; }
    public void describe() {
        System.out.println("Area: " + area());   // calls overridden version!
    }
}

class Circle extends Shape {
    private double radius;
    Circle(double r) { this.radius = r; }

    @Override
    public double area() { return Math.PI * radius * radius; }
}

class Rectangle extends Shape {
    private double width, height;
    Rectangle(double w, double h) { this.width = w; this.height = h; }

    @Override
    public double area() { return width * height; }
}

class Triangle extends Shape {
    private double base, height;
    Triangle(double b, double h) { this.base = b; this.height = h; }

    @Override
    public double area() { return 0.5 * base * height; }
}

// Polymorphic code — works with any Shape subclass
List<Shape> shapes = new ArrayList<>();
shapes.add(new Circle(5));
shapes.add(new Rectangle(4, 6));
shapes.add(new Triangle(3, 8));

double totalArea = 0;
for (Shape s : shapes) {
    totalArea += s.area();    // correct method called for each type at runtime
}
System.out.println("Total area: " + totalArea);

// Adding a new shape type (Hexagon) requires ZERO changes to this code!
```

## Compile-Time vs Runtime Polymorphism

| | Compile-Time (Static) | Runtime (Dynamic) |
|--|----------------------|-------------------|
| Also called | Static binding, Early binding | Dynamic binding, Late binding, Dynamic dispatch |
| Mechanism | Method overloading | Method overriding |
| Resolved at | Compile time | Runtime |
| Based on | Parameter types (in call) | Actual object type |
| C++ | Both | Only with `virtual` |
| Java | Both | All non-static, non-final methods |

```java
class Printer {
    // COMPILE-TIME: resolved by parameter type
    void print(int x)    { System.out.println("int: " + x); }
    void print(String x) { System.out.println("String: " + x); }
    void print(double x) { System.out.println("double: " + x); }
}

Printer p = new Printer();
p.print(5);      // resolved at compile time → print(int)
p.print("hi");   // resolved at compile time → print(String)
```

## Upcasting and Downcasting

```java
// Upcasting — always safe, implicit
Animal animal = new Dog("Rex", 3, "Lab");   // Dog → Animal (upcast)
animal.speak();   // calls Dog's speak() — runtime polymorphism works

// Downcasting — explicit, may fail at runtime
Dog dog = (Dog) animal;   // Animal → Dog (downcast)
dog.fetch();              // Dog-specific method

// Safe downcast with instanceof
if (animal instanceof Dog d) {    // Java 16+ pattern matching
    d.fetch();   // safe — checked first
}

// ClassCastException if wrong:
Animal cat = new Cat("Whiskers");
Dog d = (Dog) cat;   // ClassCastException at runtime!
```

## Polymorphism in Real Systems

Polymorphism powers extensible architecture. A payment system:

```java
interface NotificationService {
    void send(String user, String message);
}

class EmailNotification implements NotificationService {
    public void send(String user, String message) {
        // send via SMTP
        System.out.println("Email to " + user + ": " + message);
    }
}

class SMSNotification implements NotificationService {
    public void send(String user, String message) {
        // send via Twilio API
        System.out.println("SMS to " + user + ": " + message);
    }
}

class PushNotification implements NotificationService {
    public void send(String user, String message) {
        // send via Firebase
        System.out.println("Push to " + user + ": " + message);
    }
}

// OrderService doesn't need to change when new notification types are added
class OrderService {
    private NotificationService notifier;  // reference to interface

    OrderService(NotificationService notifier) {  // inject dependency
        this.notifier = notifier;
    }

    void completeOrder(String user) {
        // ... order logic ...
        notifier.send(user, "Your order is complete!");   // polymorphic call
    }
}

// Usage — swap notification type without changing OrderService
OrderService emailOrders = new OrderService(new EmailNotification());
OrderService smsOrders   = new OrderService(new SMSNotification());
```

## Interview Questions

- **Q: What is the difference between compile-time and runtime polymorphism?**
  A: Compile-time polymorphism (method overloading) is resolved at compile time based on the method signature in the call. Runtime polymorphism (method overriding) is resolved at runtime based on the actual type of the object. Overloading = "which method?" at compile time. Overriding = "whose version?" at runtime.

- **Q: Can you achieve runtime polymorphism without inheritance?**
  A: Yes — through interfaces. An object can implement an interface, and polymorphism works through the interface reference, without any parent class relationship.

---

# 8. Method Overloading vs Overriding

## Overloading — Same Name, Different Signature

```java
class Calculator {
    // Same method name, different parameter lists
    int add(int a, int b)             { return a + b; }
    double add(double a, double b)    { return a + b; }
    int add(int a, int b, int c)      { return a + b + c; }
    String add(String a, String b)    { return a + b; }

    // NOT overloading — return type alone doesn't differentiate
    // int getValue()    { return 0; }
    // double getValue() { return 0.0; }  // COMPILE ERROR — ambiguous
}

Calculator calc = new Calculator();
calc.add(1, 2);         // calls int add(int, int)
calc.add(1.0, 2.0);    // calls double add(double, double)
calc.add(1, 2, 3);     // calls int add(int, int, int)
```

Overloading resolution rules (from most to least specific):
1. Exact match
2. Widening primitive conversion (int → long → float → double)
3. Autoboxing (int → Integer)
4. Varargs

## Overriding — Same Signature, Different Class

```java
class Animal {
    public void speak() { System.out.println("..."); }
    protected String describe() { return "Animal"; }
}

class Dog extends Animal {
    @Override
    public void speak() {              // same return type, same name, same params
        System.out.println("Woof!");
    }

    @Override
    protected String describe() {     // can widen access (protected → public OK)
        return "Dog";                 // can't narrow access (public → protected = ERROR)
    }
}
```

### Overriding Rules (Java)

| Rule | Detail |
|------|--------|
| Method signature | Must be identical (name + parameters) |
| Return type | Must be same OR covariant (subtype of parent's return type) |
| Access | Can widen (private → protected → public) but NOT narrow |
| Exception | Can throw fewer/narrower checked exceptions, not more/broader |
| `static` methods | Cannot be overridden (method hiding instead) |
| `final` methods | Cannot be overridden |
| `private` methods | Cannot be overridden (not inherited) |
| `@Override` | Not required but strongly recommended — catches mistakes |

### Covariant Return Types

```java
class Animal {
    public Animal create() { return new Animal(); }
}

class Dog extends Animal {
    @Override
    public Dog create() {    // Dog is subtype of Animal — covariant return, OK!
        return new Dog();
    }
}
```

## Overloading vs Overriding Summary

| Aspect | Overloading | Overriding |
|--------|-------------|------------|
| Where | Same class | Parent-child classes |
| Signature | Different | Identical |
| Return type | Can differ | Must be same or covariant |
| Resolved | Compile time | Runtime |
| Inheritance | Not needed | Required |
| Polymorphism | Compile-time | Runtime |

## Interview Questions

- **Q: Can we override a static method in Java?**
  A: No. Static methods belong to the class, not instances. "Overriding" a static method in a subclass is actually **method hiding** — the subclass has its own separate static method. The version called depends on the reference type (compile-time), not the actual object type (runtime). No dynamic dispatch.

- **Q: Can overloaded methods have the same return type?**
  A: Yes, as long as the parameter lists differ. Return type alone is not sufficient to differentiate overloaded methods — the compiler would be unable to determine which to call.

---

# 9. Virtual Functions & Dynamic Binding

## C++ Virtual Functions

In C++, methods are **not virtual by default**. You must explicitly mark them `virtual` to enable dynamic dispatch (runtime polymorphism):

```cpp
class Animal {
public:
    void speak() {           // NOT virtual — resolved at compile time
        cout << "Animal sound" << endl;
    }

    virtual void move() {    // virtual — resolved at runtime
        cout << "Animal moves" << endl;
    }
};

class Dog : public Animal {
public:
    void speak() override {  // hides parent's speak (no polymorphism without virtual)
        cout << "Dog barks" << endl;
    }

    void move() override {   // overrides — polymorphism works
        cout << "Dog runs" << endl;
    }
};

Animal* a = new Dog();

a->speak();   // "Animal sound" — NOT virtual, compile-time binding on Animal*
a->move();    // "Dog runs"    — virtual, runtime binding to actual Dog object
```

## Java: All Methods Are Virtually Dispatched

In Java, **all non-static, non-final, non-private instance methods are virtually dispatched by default.** There is no `virtual` keyword — it's the default behavior.

```java
class Animal {
    public void speak() {     // implicitly virtual
        System.out.println("Animal sound");
    }
}

class Dog extends Animal {
    @Override
    public void speak() {
        System.out.println("Dog barks");
    }
}

Animal a = new Dog();
a.speak();    // "Dog barks" — always uses runtime type, no special keyword needed
```

This is a major Java-C++ difference. Java pays the virtual dispatch cost everywhere (though JIT's devirtualization optimization often eliminates it for hot code).

## How Dynamic Dispatch Works Internally: vtable

Both C++ (for virtual functions) and Java (for all methods) use a **vtable** (virtual method table):

```
vtable for Animal:                vtable for Dog:
┌─────────────────────────┐      ┌─────────────────────────┐
│ speak → Animal::speak() │      │ speak → Dog::speak()    │  ← overridden
│ move  → Animal::move()  │      │ move  → Dog::move()     │  ← overridden
│ eat   → Animal::eat()   │      │ eat   → Animal::eat()   │  ← inherited
└─────────────────────────┘      └─────────────────────────┘

Each object contains a hidden pointer to its class's vtable:

Dog object in memory:
┌──────────────────────────┐
│ vptr → Dog's vtable      │  ← added by compiler/JVM
│ name: "Rex"              │
│ age: 3                   │
│ breed: "Lab"             │
└──────────────────────────┘

When you call a->speak():
  1. Follow a to object in memory
  2. Read vptr → Dog's vtable
  3. Look up "speak" → Dog::speak()
  4. Call it
```

## Pure Virtual Functions (C++) vs Abstract Methods (Java)

```cpp
// C++ pure virtual — forces subclasses to implement
class Shape {
public:
    virtual double area() = 0;    // = 0 makes it pure virtual
    virtual void draw() = 0;
    // Shape is now an "abstract class" — cannot be instantiated
};

class Circle : public Shape {
    double radius;
public:
    Circle(double r) : radius(r) {}
    double area() override { return 3.14159 * radius * radius; }
    void draw() override { /* draw circle */ }
};

// Shape s;              // ERROR — abstract class
Shape* s = new Circle(5);  // OK
```

```java
// Java abstract method — equivalent concept
abstract class Shape {
    public abstract double area();   // must be implemented by subclasses
    public abstract void draw();

    // Abstract class CAN have concrete methods and fields
    public void describe() {
        System.out.println("Area: " + area());
    }
}
```

## Interview Questions

- **Q: What is a vtable?**
  A: A virtual method table — a per-class array of function pointers to the actual implementations of virtual methods. Each object has a hidden pointer (vptr) to its class's vtable. When a virtual method is called, the runtime follows vptr to the vtable and calls the correct implementation. This is how dynamic dispatch is implemented.

- **Q: In Java, do you need to declare methods as virtual?**
  A: No. All instance methods in Java are effectively virtual (dynamically dispatched) by default. Only `static`, `final`, and `private` methods use static binding. C++ requires explicit `virtual` keyword.

---

# 10. Abstract Classes & Interfaces

## Abstract Classes

An abstract class is a class that **cannot be instantiated** and may contain abstract methods (no body) that subclasses must implement.

```java
abstract class DatabaseRepository {
    // Fields — abstract classes can have state
    protected String tableName;
    protected Connection connection;

    DatabaseRepository(String tableName) {
        this.tableName = tableName;
        this.connection = ConnectionPool.get();
    }

    // Abstract methods — subclasses must implement
    public abstract void save(Object entity);
    public abstract Object findById(int id);
    public abstract List<Object> findAll();

    // Concrete methods — shared implementation
    public void delete(int id) {
        String sql = "DELETE FROM " + tableName + " WHERE id = ?";
        // execute sql...
        System.out.println("Deleted id=" + id + " from " + tableName);
    }

    public int count() {
        // SELECT COUNT(*) FROM tableName
        return 0; // placeholder
    }
}

class UserRepository extends DatabaseRepository {
    UserRepository() { super("users"); }

    @Override
    public void save(Object entity) {
        User user = (User) entity;
        // INSERT INTO users...
    }

    @Override
    public Object findById(int id) {
        // SELECT * FROM users WHERE id = ?
        return new User(); // placeholder
    }

    @Override
    public List<Object> findAll() {
        return new ArrayList<>(); // placeholder
    }
}
```

## Interfaces

An interface defines a **pure contract** — what operations an implementing class must provide.

```java
// Interface — all fields implicitly public static final
//           — methods implicitly public abstract (before Java 8)
interface Serializable { }  // marker interface — no methods

interface Comparable<T> {
    int compareTo(T other);   // returns negative, 0, or positive
}

interface Printable {
    void print();
    void printPDF();

    // Default method (Java 8+) — has implementation
    default void printAll() {
        print();
        printPDF();
    }

    // Static method (Java 8+) — utility, not inherited
    static Printable noOp() {
        return new Printable() {
            public void print() {}
            public void printPDF() {}
        };
    }

    // Private method (Java 9+) — shared logic between defaults
    private void logPrint(String format) {
        System.out.println("Printing as: " + format);
    }
}
```

## Implementing Multiple Interfaces

```java
// Java's solution to multiple inheritance
class Employee implements Comparable<Employee>, Serializable, Printable {
    String name;
    double salary;

    @Override
    public int compareTo(Employee other) {
        return Double.compare(this.salary, other.salary);
    }

    @Override
    public void print() {
        System.out.println("Employee: " + name + ", Salary: " + salary);
    }

    @Override
    public void printPDF() { /* pdf generation */ }
}
```

## Abstract Class vs Interface — Deep Comparison

| Feature | Abstract Class | Interface |
|---------|---------------|-----------|
| Instantiation | Cannot | Cannot |
| Fields | Any (instance + static) | Only `public static final` |
| Constructor | Yes | No |
| Abstract methods | Yes | Yes (implicitly) |
| Concrete methods | Yes | Only `default` and `static` (Java 8+) |
| Access modifiers on methods | Any | `public` only (before Java 9) |
| Extends/Implements | `extends` one class | `implements` many interfaces |
| Multiple inheritance | No | Yes |
| State (instance variables) | Yes | No |
| When to use | Shared state + partial implementation | Pure contract / capability |

### Decision Guide

```
Need to share STATE (instance variables)?
  └── Yes → Abstract Class
  └── No  → Interface

Need constructor logic?
  └── Yes → Abstract Class
  └── No  → Interface

Implementing multiple contracts?
  └── Yes → Interfaces (can implement many)
  └── No  → Either works

Is the relationship "is-a" with implementation?
  └── Yes → Abstract Class (Animal → Dog)
  └── Capability? → Interface (Flyable, Serializable)
```

## Real-World Example: Spring Framework Pattern

```java
// Spring uses abstract classes for template pattern
abstract class JdbcTemplate {
    // Template method — defines the algorithm skeleton
    public final List<Object> query(String sql) {
        Connection conn = getConnection();    // concrete
        PreparedStatement ps = prepare(sql); // concrete
        ResultSet rs = execute(ps);          // concrete
        return mapResults(rs);               // ABSTRACT — subclass implements mapping
    }

    protected abstract List<Object> mapResults(ResultSet rs);
    private Connection getConnection() { ... }
}

// Interface for Spring repositories
interface UserRepository extends JpaRepository<User, Long> {
    // Spring generates implementation at runtime!
    List<User> findByEmail(String email);
    Optional<User> findByUsername(String username);
}
```

## Interview Questions

- **Q: When would you use an abstract class over an interface?**
  A: Use an abstract class when you need to share state (instance fields), provide constructor logic, or have some methods with implementations that subclasses should inherit. Use an interface when you're defining a capability contract that multiple unrelated classes should fulfill, or when you need multiple inheritance of type.

- **Q: Can an interface have a constructor?**
  A: No. Interfaces cannot have constructors because they cannot be instantiated. They cannot have instance state either — all fields are implicitly `public static final`.

- **Q: What is a marker interface?**
  A: An interface with no methods — used as a tag to mark a class as having some property. Examples: `Serializable`, `Cloneable`, `RandomAccess`. The JVM or frameworks check `instanceof MarkerInterface` to decide behavior.

---

# 11. Multiple Inheritance & the Diamond Problem

## C++ Multiple Inheritance

C++ allows a class to inherit from multiple classes directly:

```cpp
class Flyable {
public:
    void fly() { cout << "Flying" << endl; }
};

class Swimmable {
public:
    void swim() { cout << "Swimming" << endl; }
};

class Duck : public Flyable, public Swimmable {
    // Duck inherits both fly() and swim()
};

Duck d;
d.fly();   // OK
d.swim();  // OK
```

## The Diamond Problem

The problem occurs when two parent classes both inherit from the same grandparent:

```
        Animal
       /      \
    Dog        Robot
       \      /
       RobotDog

class Animal { void eat() {...} };
class Dog    : public Animal { };
class Robot  : public Animal { };
class RobotDog : public Dog, public Robot { };  // Diamond!

RobotDog rd;
rd.eat();  // AMBIGUOUS! Which eat()? Dog's copy or Robot's copy?
           // Both Dog and Robot have their own copy of Animal's data!
```

```
Without virtual inheritance:        With virtual inheritance:
──────────────────────────          ──────────────────────────
RobotDog                            RobotDog
├── Dog                             ├── Dog
│   └── Animal (copy 1)             │   └── Animal (shared, ONE copy)
└── Robot                           └── Robot
    └── Animal (copy 2)                 └── Animal (same shared copy)

rd.eat() → AMBIGUOUS                rd.eat() → OK (one Animal)
```

### C++ Solution: Virtual Inheritance

```cpp
class Animal { public: void eat() { cout << "eating" << endl; } };

class Dog   : virtual public Animal { };   // virtual inheritance
class Robot : virtual public Animal { };   // virtual inheritance

class RobotDog : public Dog, public Robot {
    // Now only ONE copy of Animal's members
};

RobotDog rd;
rd.eat();  // OK — unambiguous, one Animal
```

## Java's Solution: No Class Multiple Inheritance

Java sidesteps the diamond problem entirely by **disallowing multiple class inheritance**. A class can only `extend` one class. But it can `implement` multiple interfaces.

```java
// This is ILLEGAL in Java:
// class RobotDog extends Dog, Robot { }  // COMPILE ERROR

// Interfaces CAN be multiply "implemented":
interface Flyable { void fly(); }
interface Swimmable { void swim(); }

class Duck implements Flyable, Swimmable {
    public void fly()  { System.out.println("Duck flies"); }
    public void swim() { System.out.println("Duck swims"); }
}
```

### Default Method Diamond (Java 8+)

With default methods in interfaces, Java introduced a limited diamond problem:

```java
interface A { default void hello() { System.out.println("A"); } }
interface B extends A { default void hello() { System.out.println("B"); } }
interface C extends A { default void hello() { System.out.println("C"); } }

// D implements both B and C — which hello() wins?
class D implements B, C {
    // MUST override to resolve ambiguity
    @Override
    public void hello() {
        B.super.hello();   // explicitly choose B's version
        // OR C.super.hello();
    }
}
```

Resolution rules for default method conflict:
1. Class method beats interface default method
2. More specific interface (closer in hierarchy) wins
3. If still ambiguous → must override and resolve manually

## Interview Questions

- **Q: Why doesn't Java support multiple class inheritance?**
  A: To avoid the diamond problem — ambiguity when two parent classes have the same method or field, and both inherit from the same grandparent. Java uses interfaces for multiple inheritance of type/behavior while keeping single-class inheritance for implementation. Interface default methods (Java 8+) brought a limited version of the problem back, resolved by explicit override rules.

---

# 12. Composition vs Inheritance

## The Problem with Over-Inheritance

Inheritance creates tight coupling between parent and child. If the parent changes, children may break:

```java
// BAD: Using inheritance for code reuse when "is-a" doesn't hold
class Stack extends ArrayList {  // Stack IS-NOT-A ArrayList conceptually
    public void push(Object item) { add(item); }
    public Object pop() { return remove(size() - 1); }
}

// Problem: Stack inherits ArrayList's get(index), add(index, item), remove(index)
// These break the Stack's LIFO contract!
Stack s = new Stack();
s.push("a"); s.push("b");
s.add(0, "c");   // inserts at beginning! — violates Stack behavior
```

This is Java's actual historical bug — `java.util.Stack extends Vector` is considered a design mistake.

## Composition — "has-a" over "is-a"

```java
// GOOD: Stack HAS-A list (composition)
class Stack<T> {
    private ArrayList<T> elements = new ArrayList<>();  // composition

    public void push(T item) { elements.add(item); }

    public T pop() {
        if (isEmpty()) throw new EmptyStackException();
        return elements.remove(elements.size() - 1);
    }

    public T peek() {
        if (isEmpty()) throw new EmptyStackException();
        return elements.get(elements.size() - 1);
    }

    public boolean isEmpty() { return elements.isEmpty(); }
    public int size()        { return elements.size(); }

    // get(index), add(index, item) etc. are NOT exposed — Stack controls its own API
}
```

## Favor Composition Over Inheritance

The classic GoF (Gang of Four) design principle: **"Favor composition over inheritance."**

```java
// Inheritance approach — gets messy
class Logger { void log(String msg) {...} }
class DatabaseLogger extends Logger { void logToDb(String msg) {...} }
class FileLogger extends Logger { void logToFile(String msg) {...} }
class NetworkLogger extends Logger { }
// What if you need DB + File? Multiple inheritance problem!

// Composition approach — flexible
interface LogSink {
    void write(String message);
}

class DatabaseSink implements LogSink {
    public void write(String msg) { /* write to DB */ }
}

class FileSink implements LogSink {
    public void write(String msg) { /* write to file */ }
}

class Logger {
    private List<LogSink> sinks;

    Logger(LogSink... sinks) {
        this.sinks = Arrays.asList(sinks);
    }

    void log(String msg) {
        for (LogSink sink : sinks) sink.write(msg);
    }
}

// Now trivially combine any sinks at runtime!
Logger logger = new Logger(new DatabaseSink(), new FileSink());
```

## When to Use Which

| Use Inheritance | Use Composition |
|----------------|-----------------|
| True "is-a" relationship | "has-a" or "uses-a" relationship |
| Extending sealed class hierarchy | Mixing behaviors from multiple sources |
| Framework base classes (Spring's `AbstractController`) | Flexible behavior that can change at runtime |
| Adding new methods to parent API | Preventing subclass from breaking parent contract |

## Interview Questions

- **Q: What does "Favor composition over inheritance" mean?**
  A: Instead of extending a class to reuse its code (inheritance), hold a reference to it and delegate calls (composition). This gives you flexibility — you can swap implementations at runtime, combine multiple behaviors, and avoid the tight coupling and fragility that deep inheritance hierarchies create.

---

# 13. Association, Aggregation, Composition, Dependency

These define *relationships between classes* — crucial for design discussions.

## Dependency (Weakest)

Class A uses class B temporarily — typically as a method parameter or local variable:

```java
class OrderService {
    // Dependency: OrderService USES EmailService but doesn't OWN it
    void placeOrder(Order order, EmailService emailService) {
        // ... process order ...
        emailService.sendConfirmation(order);  // temporary use
    }
}
// When placeOrder() returns, the relationship is gone
```

UML: `OrderService - - -> EmailService` (dashed arrow)

## Association (Knows About)

Class A has a reference to class B as a field — they "know about" each other, but neither owns the other:

```java
class Student {
    private Teacher teacher;   // association — student knows a teacher

    Student(Teacher t) { this.teacher = t; }
    void learn() { teacher.teach(); }
}

class Teacher {
    private Student student;   // bidirectional association
}
// Both exist independently — destroying Student doesn't destroy Teacher
```

UML: `Student ——— Teacher` (solid line)

## Aggregation ("has-a", weak ownership)

Class A "has" a collection of class B, but B can exist without A:

```java
class Department {
    private List<Employee> employees;  // aggregation

    Department() { employees = new ArrayList<>(); }

    void addEmployee(Employee e) { employees.add(e); }
    void removeEmployee(Employee e) { employees.remove(e); }
}

// Employees exist independently — if Department is dissolved,
// employees still exist and can join other departments
Employee emp = new Employee("Alice");
Department hr = new Department();
hr.addEmployee(emp);

// emp can exist without any department
```

UML: `Department ◇——— Employee` (open diamond at owner end)

## Composition ("has-a", strong ownership)

Class A contains class B, and B **cannot exist without A** — A creates and destroys B:

```java
class House {
    private Room livingRoom;    // composition — Room is part of House
    private Room bedroom;

    House() {
        // House creates its rooms — rooms don't exist independently
        livingRoom = new Room("Living Room", 20);
        bedroom    = new Room("Bedroom", 15);
    }

    // When House is destroyed (GC'd), Rooms go with it
}

class Room {
    private String name;
    private double size;

    Room(String name, double size) {
        this.name = name;
        this.size = size;
    }
}

// You never do: Room r = new Room(...); house.addRoom(r);
// Room only makes sense as part of a House in this design
```

UML: `House ◆——— Room` (filled diamond at owner end)

## Visualization of All Four

```
DEPENDENCY          A - - -> B       A uses B temporarily (method param)
ASSOCIATION         A ——— B          A knows B (field reference, both independent)
AGGREGATION         A ◇——— B         A has B (B can exist without A)
COMPOSITION         A ◆——— B         A owns B (B cannot exist without A)

Strength of relationship: Dependency < Association < Aggregation < Composition
```

## Interview Questions

- **Q: What is the difference between aggregation and composition?**
  A: Both are "has-a" relationships. Aggregation is weak ownership — the contained object can exist independently (Employee can exist without Department). Composition is strong ownership — the contained object cannot exist independently and is created/destroyed by the container (Room is created by and destroyed with House).

---

# 14. SOLID Principles

SOLID is an acronym for five design principles that make software more maintainable, extensible, and robust.

## S — Single Responsibility Principle (SRP)

**"A class should have only one reason to change."**

Each class should do one thing and do it well:

```java
// VIOLATION: UserService does too many things
class UserService {
    void createUser(User user) { /* DB insert */ }
    void sendWelcomeEmail(User user) { /* email logic */ }
    void generateReport() { /* reporting logic */ }
    void validateUser(User user) { /* validation logic */ }
}
// If email logic changes → touch UserService
// If DB schema changes → touch UserService
// If report format changes → touch UserService

// CORRECT: Each class has one responsibility
class UserRepository {
    void save(User user) { /* DB insert */ }
    User findById(int id) { /* DB query */ }
}

class EmailService {
    void sendWelcome(User user) { /* email logic */ }
}

class UserValidator {
    void validate(User user) { /* validation */ }
}

class ReportGenerator {
    void generate() { /* reporting */ }
}

class UserService {
    private UserRepository repo;
    private EmailService emailService;
    private UserValidator validator;

    void createUser(User user) {
        validator.validate(user);
        repo.save(user);
        emailService.sendWelcome(user);
    }
}
```

## O — Open/Closed Principle (OCP)

**"Open for extension, closed for modification."**

Add new functionality by extending, not by editing existing code:

```java
// VIOLATION: Adding new discount types requires modifying existing code
class DiscountService {
    double calculate(String type, double price) {
        if (type.equals("seasonal")) return price * 0.1;
        if (type.equals("loyalty"))  return price * 0.15;
        if (type.equals("clearance")) return price * 0.3;
        // EVERY new type requires editing this class!
        return 0;
    }
}

// CORRECT: Extend with new classes, don't modify existing
interface DiscountStrategy {
    double apply(double price);
}

class SeasonalDiscount implements DiscountStrategy {
    public double apply(double price) { return price * 0.1; }
}

class LoyaltyDiscount implements DiscountStrategy {
    public double apply(double price) { return price * 0.15; }
}

class ClearanceDiscount implements DiscountStrategy {
    public double apply(double price) { return price * 0.3; }
}

class DiscountService {
    double calculate(DiscountStrategy strategy, double price) {
        return strategy.apply(price);   // adding new types = new class, no edits here
    }
}

// New requirement: flash sale discount → add FlashSaleDiscount class, done!
```

## L — Liskov Substitution Principle (LSP)

**"Subclasses must be substitutable for their base class without breaking correctness."**

If code works with a `Bird`, it must work with any subclass of `Bird`:

```java
// VIOLATION
class Bird {
    void fly() { System.out.println("flying"); }
}

class Penguin extends Bird {
    @Override
    void fly() {
        throw new UnsupportedOperationException("Penguins can't fly!");
    }
}

// Code using Bird breaks when given Penguin:
void makeBirdFly(Bird bird) {
    bird.fly();   // throws exception for Penguin! LSP violated
}

// CORRECT: Restructure the hierarchy
interface FlyingBird {
    void fly();
}

class Sparrow implements FlyingBird {
    public void fly() { System.out.println("Sparrow flies"); }
}

class Penguin {  // Not a FlyingBird — separate type
    void swim() { System.out.println("Penguin swims"); }
}

// Now the code is correct — only FlyingBird references can fly()
```

## I — Interface Segregation Principle (ISP)

**"Clients should not be forced to depend on interfaces they don't use."**

Fat interfaces force classes to implement methods they don't need:

```java
// VIOLATION: One big interface
interface Worker {
    void work();
    void eat();
    void sleep();
}

class Robot implements Worker {
    public void work()  { /* robot works */ }
    public void eat()   { throw new UnsupportedOperationException(); }  // robots don't eat!
    public void sleep() { throw new UnsupportedOperationException(); }  // robots don't sleep!
}

// CORRECT: Split into focused interfaces
interface Workable  { void work(); }
interface Eatable   { void eat(); }
interface Sleepable { void sleep(); }

class Human implements Workable, Eatable, Sleepable {
    public void work()  { System.out.println("Human works"); }
    public void eat()   { System.out.println("Human eats"); }
    public void sleep() { System.out.println("Human sleeps"); }
}

class Robot implements Workable {
    public void work() { System.out.println("Robot works"); }
    // No forced implementation of eat/sleep!
}
```

## D — Dependency Inversion Principle (DIP)

**"High-level modules should not depend on low-level modules. Both should depend on abstractions."**

```java
// VIOLATION: High-level OrderService depends directly on low-level MySQLDatabase
class MySQLDatabase {
    void save(Order order) { /* MySQL-specific code */ }
}

class OrderService {
    private MySQLDatabase db = new MySQLDatabase();  // hard dependency!
    // If you want to use PostgreSQL, you must edit OrderService
    // If you want to test without DB, you can't!

    void placeOrder(Order order) {
        db.save(order);
    }
}

// CORRECT: Both depend on abstraction
interface OrderRepository {
    void save(Order order);
    Order findById(int id);
}

class MySQLOrderRepository implements OrderRepository {
    public void save(Order order) { /* MySQL code */ }
    public Order findById(int id) { /* MySQL code */ return null; }
}

class InMemoryOrderRepository implements OrderRepository {  // for testing
    private Map<Integer, Order> store = new HashMap<>();
    public void save(Order order) { store.put(order.getId(), order); }
    public Order findById(int id) { return store.get(id); }
}

class OrderService {
    private OrderRepository repo;  // depends on abstraction

    OrderService(OrderRepository repo) {  // injected — can be any implementation
        this.repo = repo;
    }

    void placeOrder(Order order) {
        repo.save(order);
    }
}

// Production:
OrderService service = new OrderService(new MySQLOrderRepository());

// Testing:
OrderService service = new OrderService(new InMemoryOrderRepository());
```

This is the foundation of **Dependency Injection (DI)**, which Spring Framework is built on.

## Interview Questions

- **Q: Explain the Single Responsibility Principle with a real-world example.**
  A: A `User` class should manage user data. It should NOT also handle sending emails, generating reports, and logging. If email logic changes, why would you touch the User class? Each class should have exactly one reason to change.

- **Q: What is the Dependency Inversion Principle and how does Spring implement it?**
  A: High-level modules shouldn't depend on low-level modules — both depend on abstractions (interfaces). Spring implements this via IoC (Inversion of Control) — you define dependencies as interface types, and Spring's DI container injects the right implementation at runtime.

---

# 15. Design Patterns

Design patterns are reusable solutions to commonly occurring design problems.

## Creational Patterns

### Singleton — One Instance Only

```java
// Thread-safe Singleton using double-checked locking
public class DatabaseConnection {
    private static volatile DatabaseConnection instance;  // volatile for visibility
    private Connection connection;

    private DatabaseConnection() {
        // private constructor — prevents external instantiation
        this.connection = DriverManager.getConnection("jdbc:mysql://localhost/mydb");
    }

    public static DatabaseConnection getInstance() {
        if (instance == null) {                      // first check (no lock)
            synchronized (DatabaseConnection.class) {
                if (instance == null) {              // second check (with lock)
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }

    public Connection getConnection() { return connection; }
}

// Usage
DatabaseConnection.getInstance().getConnection();
```

**Enum Singleton (preferred in Java — simplest and thread-safe):**
```java
public enum DatabaseConnection {
    INSTANCE;

    private Connection connection;

    DatabaseConnection() {
        // initialization
    }

    public Connection getConnection() { return connection; }
}

// Usage
DatabaseConnection.INSTANCE.getConnection();
```

### Builder — Construct Complex Objects Step by Step

```java
public class HttpRequest {
    private final String url;           // required
    private final String method;        // required
    private final Map<String,String> headers;
    private final String body;
    private final int timeoutMs;
    private final boolean followRedirects;

    private HttpRequest(Builder builder) {
        this.url = builder.url;
        this.method = builder.method;
        this.headers = builder.headers;
        this.body = builder.body;
        this.timeoutMs = builder.timeoutMs;
        this.followRedirects = builder.followRedirects;
    }

    public static class Builder {
        private final String url;       // required
        private final String method;    // required
        private Map<String,String> headers = new HashMap<>();
        private String body = null;
        private int timeoutMs = 30000;
        private boolean followRedirects = true;

        public Builder(String url, String method) {
            this.url = url;
            this.method = method;
        }

        public Builder header(String key, String value) {
            headers.put(key, value);
            return this;
        }
        public Builder body(String body)               { this.body = body; return this; }
        public Builder timeout(int ms)                 { this.timeoutMs = ms; return this; }
        public Builder noRedirects()                   { this.followRedirects = false; return this; }
        public HttpRequest build()                     { return new HttpRequest(this); }
    }
}

// Usage — readable, flexible
HttpRequest request = new HttpRequest.Builder("https://api.example.com/users", "POST")
    .header("Content-Type", "application/json")
    .header("Authorization", "Bearer token123")
    .body("{\"name\": \"Alice\"}")
    .timeout(5000)
    .build();
```

### Factory Method — Delegate Object Creation to Subclasses

```java
abstract class NotificationFactory {
    // Factory method — subclasses decide which concrete type to create
    public abstract Notification createNotification();

    public void sendNotification(String message) {
        Notification n = createNotification();  // polymorphic creation
        n.send(message);
    }
}

class EmailNotificationFactory extends NotificationFactory {
    @Override
    public Notification createNotification() {
        return new EmailNotification();
    }
}

class SMSNotificationFactory extends NotificationFactory {
    @Override
    public Notification createNotification() {
        return new SMSNotification();
    }
}
```

## Structural Patterns

### Adapter — Make Incompatible Interfaces Work Together

```java
// Legacy payment processor — old interface we can't change
class LegacyPaymentSystem {
    public boolean makePayment(String accountNum, int amountInCents) {
        System.out.println("Legacy payment: " + amountInCents + " cents");
        return true;
    }
}

// Modern interface our system expects
interface PaymentProcessor {
    boolean processPayment(String account, double amountInDollars);
}

// Adapter — wraps legacy system, implements modern interface
class LegacyPaymentAdapter implements PaymentProcessor {
    private LegacyPaymentSystem legacy;

    LegacyPaymentAdapter(LegacyPaymentSystem legacy) {
        this.legacy = legacy;
    }

    @Override
    public boolean processPayment(String account, double amountInDollars) {
        int cents = (int)(amountInDollars * 100);  // convert dollars → cents
        return legacy.makePayment(account, cents);
    }
}

// Our code works with the modern interface, legacy system under the hood
PaymentProcessor processor = new LegacyPaymentAdapter(new LegacyPaymentSystem());
processor.processPayment("ACC123", 29.99);
```

### Decorator — Add Behavior Without Subclassing

```java
interface TextProcessor {
    String process(String text);
}

class PlainTextProcessor implements TextProcessor {
    public String process(String text) { return text; }
}

// Decorators wrap a TextProcessor and add behavior
class UpperCaseDecorator implements TextProcessor {
    private TextProcessor wrapped;
    UpperCaseDecorator(TextProcessor t) { this.wrapped = t; }

    public String process(String text) {
        return wrapped.process(text).toUpperCase();
    }
}

class TrimDecorator implements TextProcessor {
    private TextProcessor wrapped;
    TrimDecorator(TextProcessor t) { this.wrapped = t; }

    public String process(String text) {
        return wrapped.process(text).trim();
    }
}

class HtmlEscapeDecorator implements TextProcessor {
    private TextProcessor wrapped;
    HtmlEscapeDecorator(TextProcessor t) { this.wrapped = t; }

    public String process(String text) {
        return wrapped.process(text)
                      .replace("<", "&lt;")
                      .replace(">", "&gt;");
    }
}

// Chain decorators — mix and match at runtime
TextProcessor processor = new UpperCaseDecorator(
                              new TrimDecorator(
                                  new HtmlEscapeDecorator(
                                      new PlainTextProcessor())));

System.out.println(processor.process("  <b>hello</b>  "));
// → "&LT;B&GT;HELLO&LT;/B&GT;"
```

Java's I/O streams are all decorators: `new BufferedReader(new InputStreamReader(new FileInputStream("file.txt")))`

## Behavioral Patterns

### Observer — Publish/Subscribe

```java
interface Observer {
    void update(String event, Object data);
}

class EventBus {
    private Map<String, List<Observer>> listeners = new HashMap<>();

    public void subscribe(String event, Observer observer) {
        listeners.computeIfAbsent(event, k -> new ArrayList<>()).add(observer);
    }

    public void publish(String event, Object data) {
        List<Observer> obs = listeners.getOrDefault(event, Collections.emptyList());
        for (Observer o : obs) o.update(event, data);
    }
}

// Observers
class EmailAlerter implements Observer {
    public void update(String event, Object data) {
        System.out.println("Email alert for " + event + ": " + data);
    }
}

class DashboardUpdater implements Observer {
    public void update(String event, Object data) {
        System.out.println("Dashboard updated: " + event + " - " + data);
    }
}

// Usage
EventBus bus = new EventBus();
bus.subscribe("ORDER_PLACED", new EmailAlerter());
bus.subscribe("ORDER_PLACED", new DashboardUpdater());
bus.subscribe("PAYMENT_FAILED", new EmailAlerter());

bus.publish("ORDER_PLACED", "Order #1234");
// → Email alert for ORDER_PLACED: Order #1234
// → Dashboard updated: ORDER_PLACED - Order #1234
```

### Strategy — Swap Algorithms at Runtime

```java
interface SortStrategy {
    void sort(int[] arr);
}

class BubbleSort implements SortStrategy {
    public void sort(int[] arr) { /* bubble sort impl */ }
}

class QuickSort implements SortStrategy {
    public void sort(int[] arr) { /* quick sort impl */ }
}

class MergeSort implements SortStrategy {
    public void sort(int[] arr) { /* merge sort impl */ }
}

class Sorter {
    private SortStrategy strategy;

    Sorter(SortStrategy strategy) { this.strategy = strategy; }

    void setStrategy(SortStrategy strategy) { this.strategy = strategy; }

    void sort(int[] arr) { strategy.sort(arr); }
}

// Choose algorithm at runtime
Sorter sorter = new Sorter(new QuickSort());
sorter.sort(data);

// Switch strategy for small arrays
if (data.length < 10) sorter.setStrategy(new BubbleSort());
sorter.sort(smallData);
```

### Template Method — Define Algorithm Skeleton

```java
abstract class DataExporter {
    // Template method — algorithm structure fixed here
    public final void export(String destination) {
        List<Object> data = fetchData();      // step 1
        List<Object> cleaned = clean(data);   // step 2
        String formatted = format(cleaned);   // step 3 — abstract
        write(formatted, destination);         // step 4 — abstract
        notify(destination);                  // step 5 — concrete
    }

    protected abstract String format(List<Object> data);
    protected abstract void write(String data, String destination);

    // Common implementations
    private List<Object> fetchData() { return new ArrayList<>(); }
    private List<Object> clean(List<Object> data) { return data; }
    private void notify(String dest) { System.out.println("Exported to: " + dest); }
}

class CSVExporter extends DataExporter {
    protected String format(List<Object> data) { return "csv content"; }
    protected void write(String data, String dest) { /* write CSV file */ }
}

class JSONExporter extends DataExporter {
    protected String format(List<Object> data) { return "{ json content }"; }
    protected void write(String data, String dest) { /* write JSON file */ }
}
```

## Interview Questions

- **Q: What is the difference between Factory Method and Abstract Factory?**
  A: Factory Method defines one method for creating one type of object — subclasses decide the concrete type. Abstract Factory provides an interface for creating *families* of related objects (e.g., UI components for Windows vs macOS — WindowsFactory creates WindowsButton + WindowsDialog together).

- **Q: Explain the Builder pattern and when to use it.**
  A: Builder separates object construction from representation — useful when an object has many optional parameters or complex construction logic. Avoids telescoping constructors (constructors with 7+ parameters). Makes code readable and forces valid object state.

- **Q: What design pattern does Java's InputStream/OutputStream use?**
  A: Decorator. `new BufferedInputStream(new FileInputStream("file"))` — BufferedInputStream wraps FileInputStream, adding buffering behavior without changing the InputStream interface.

---

# 16. Interview Quick Reference

## OOP Pillars Summary

| Pillar | Definition | Java Mechanism | C++ Mechanism |
|--------|-----------|---------------|---------------|
| Encapsulation | Bundle data + methods, restrict access | `private` fields + public methods | Same |
| Abstraction | Hide complexity, expose interface | `abstract` class, `interface` | Pure virtual functions |
| Inheritance | Reuse and extend parent behavior | `extends` | `:` with access specifier |
| Polymorphism | One interface, many implementations | Method overriding (all methods) | `virtual` functions only |

## Key Java vs C++ OOP Differences

| Topic | C++ | Java |
|-------|-----|------|
| Multiple class inheritance | Allowed | Not allowed |
| Default virtual | No — must use `virtual` | Yes — all instance methods |
| Destructor | Deterministic (`~Class()`) | No deterministic destructor (use AutoCloseable) |
| Abstract class | Class with pure virtual method | `abstract` class keyword |
| Interface | Not built-in (use pure abstract class) | `interface` keyword |
| Copy constructor | Built-in, used by value semantics | No built-in — must write manually |
| `override` keyword | Optional (C++11) | `@Override` annotation (optional but recommended) |
| Object slicing | Yes — copying base loses derived data | No — references don't slice |

## SOLID in One Line Each

- **S**RP: One class, one responsibility, one reason to change
- **O**CP: Extend with new code, don't modify existing code
- **L**SP: Subclasses must be usable wherever their parent is used
- **I**SP: Many small interfaces beat one large fat interface
- **D**IP: Depend on abstractions (interfaces), not concrete classes

## Design Patterns Quick Reference

| Pattern | Category | One-line purpose |
|---------|----------|-----------------|
| Singleton | Creational | One instance globally |
| Builder | Creational | Construct complex objects step by step |
| Factory Method | Creational | Subclass decides what to create |
| Abstract Factory | Creational | Create families of related objects |
| Adapter | Structural | Make incompatible interfaces work together |
| Decorator | Structural | Add behavior at runtime without subclassing |
| Proxy | Structural | Control access to another object |
| Observer | Behavioral | Notify multiple objects on state change |
| Strategy | Behavioral | Swap algorithms at runtime |
| Template Method | Behavioral | Define algorithm skeleton, subclasses fill in steps |
| Command | Behavioral | Encapsulate requests as objects |

---

*End of Part 2: Object-Oriented Programming*
*Next: Part 3 (Java Collections Framework)*
