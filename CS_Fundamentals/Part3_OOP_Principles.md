# Object-Oriented Programming Complete Guide

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

