# Spring Boot — Interview Mastery Guide
### Junior Backend Engineer | NeuralMetrics-Style Prep | Interview-Ready

---

> **How to use this:** Every section has Theory → How it works internally → Code example → Interview Q&A.
> Read all sections. The Q&A at the end of each section is what interviewers actually ask.

---

# Table of Contents

1. [Spring Core: IoC, DI, Beans, Lifecycle](#part-1-spring-core-ioc-di-beans-lifecycle)
2. [Spring Boot Basics & Auto-Configuration](#part-2-spring-boot-basics--auto-configuration)
3. [REST APIs: Controllers, Validation, Exception Handling](#part-3-rest-apis-controllers-validation-exception-handling)
4. [Spring Data JPA: Hibernate, Relationships, N+1, Transactions](#part-4-spring-data-jpa-hibernate-relationships-n1-transactions)
5. [Spring Security + JWT Authentication](#part-5-spring-security--jwt-authentication)
6. [Master Interview Q&A Cheatsheet](#part-6-master-interview-qa-cheatsheet)

---

# PART 1: Spring Core — IoC, DI, Beans, Lifecycle

---

## 1.1 What is Spring and Why Does It Exist?

Before Spring, building a Java enterprise app meant using EJB (Enterprise JavaBeans) — heavy, complex, required an expensive application server, and was painful to test.

Spring's answer in 2003: **a lightweight framework that manages your objects for you**, so you can focus on business logic.

The two core ideas:
- **IoC (Inversion of Control)** — don't create your own objects; let Spring create and manage them
- **DI (Dependency Injection)** — don't look up your dependencies; let Spring hand them to you

---

## 1.2 IoC — Inversion of Control

**Without IoC (traditional approach):**
```java
public class OrderService {
    // You create your own dependency
    private PaymentService paymentService = new PaymentService();
    private EmailService emailService = new EmailService();

    public void placeOrder(Order order) {
        paymentService.charge(order);
        emailService.sendConfirmation(order);
    }
}
```

Problems:
- `OrderService` is tightly coupled to `PaymentService` — can't swap it out
- Can't test `OrderService` without a real `PaymentService`
- If `PaymentService` constructor changes, `OrderService` must change

**With IoC (Spring manages objects):**
```java
@Service
public class OrderService {
    // Spring injects this — you don't create it
    private final PaymentService paymentService;
    private final EmailService emailService;

    public OrderService(PaymentService paymentService, EmailService emailService) {
        this.paymentService = paymentService;
        this.emailService = emailService;
    }

    public void placeOrder(Order order) {
        paymentService.charge(order);
        emailService.sendConfirmation(order);
    }
}
```

Spring's IoC Container (ApplicationContext) creates ALL these objects and wires them together. You declare what you need; Spring provides it.

```
Traditional:    You           → new PaymentService() → new OrderService(paymentService)
IoC:            Spring        → creates PaymentService → creates OrderService → injects it
                                                                    ↑
                                              Control is INVERTED — Spring controls creation
```

---

## 1.3 Dependency Injection Types

### Constructor Injection (Recommended)

```java
@Service
public class OrderService {
    private final PaymentService paymentService;  // final — immutable after construction

    // Spring sees one constructor — automatically injects (no @Autowired needed in modern Spring)
    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
```

**Why constructor injection is best:**
- Dependencies are explicit and required
- `final` fields — truly immutable, thread-safe
- Easy to test (just pass mock in constructor)
- No reflection tricks needed

### Field Injection (Common but not recommended)

```java
@Service
public class OrderService {
    @Autowired
    private PaymentService paymentService;  // Spring injects via reflection
}
```

Problems: can't be `final`, harder to test, hides dependencies.

### Setter Injection (for optional dependencies)

```java
@Service
public class OrderService {
    private PaymentService paymentService;

    @Autowired(required = false)  // optional dependency
    public void setPaymentService(PaymentService ps) {
        this.paymentService = ps;
    }
}
```

---

## 1.4 What is a Bean?

A **Bean** is any object that Spring manages. Spring creates it, stores it in its container, injects it where needed, and destroys it when done.

You tell Spring what to manage using annotations:

| Annotation | Purpose | Layer |
|-----------|---------|-------|
| `@Component` | Generic Spring-managed class | Any |
| `@Service` | Business logic | Service layer |
| `@Repository` | Database access | Data layer |
| `@Controller` | HTTP request handler | Web layer |
| `@RestController` | HTTP + JSON response | Web layer |
| `@Configuration` | Java config class | Config |
| `@Bean` | Method that produces a bean | Config |

All of `@Service`, `@Repository`, `@Controller` are just `@Component` with a descriptive name — they all create beans. The distinction is for clarity and some extra behavior (`@Repository` translates SQL exceptions).

### Declaring Beans with @Bean

```java
@Configuration
public class AppConfig {

    // This method's return value becomes a Spring Bean
    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
        return mapper;
    }

    // For third-party classes you can't annotate directly
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

---

## 1.5 Bean Scopes

By default all beans are **Singleton** — Spring creates exactly one instance and reuses it everywhere.

| Scope | Meaning | Annotation |
|-------|---------|-----------|
| `singleton` | One instance for entire application (default) | `@Scope("singleton")` |
| `prototype` | New instance every time it's requested | `@Scope("prototype")` |
| `request` | One instance per HTTP request (web only) | `@RequestScope` |
| `session` | One instance per HTTP session (web only) | `@SessionScope` |

```java
@Component
@Scope("prototype")
public class ReportGenerator {
    // New instance every time this bean is injected or requested
    // Useful for stateful objects that shouldn't be shared
}
```

**Interview Trap:** Singleton beans with mutable state are a problem in multithreaded apps. Most Spring services are singletons — they must be **stateless** (no instance variables that change per request).

```java
// BAD — singleton with mutable state:
@Service
public class OrderService {
    private Order currentOrder;  // SHARED across all threads — race condition!

    public void process(Order o) {
        currentOrder = o;    // Thread 1 sets this
        // Thread 2 also sets this — Thread 1's data is gone!
    }
}

// GOOD — stateless singleton:
@Service
public class OrderService {
    public void process(Order order) {
        // order is local — safe, no shared state
        validate(order);
        save(order);
    }
}
```

---

## 1.6 Bean Lifecycle

```
Spring ApplicationContext starts
         │
         ▼
1. SCAN   — Find all @Component, @Service, @Repository, @Controller classes
         │
         ▼
2. INSTANTIATE — Call constructors to create bean instances
         │
         ▼
3. INJECT — Wire dependencies (constructor, field, or setter injection)
         │
         ▼
4. @PostConstruct — Run initialization method (optional)
         │
         ▼
5. READY — Bean is live, serving requests
         │
         ▼
6. @PreDestroy — Run cleanup method when app shuts down (optional)
         │
         ▼
7. DESTROY — Bean removed from container
```

```java
@Service
public class DatabaseConnectionPool {
    private List<Connection> pool;

    // Constructor injection
    public DatabaseConnectionPool(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    @PostConstruct
    public void init() {
        // Runs AFTER injection is complete
        // Safe to use injected dependencies here
        pool = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            pool.add(dataSource.getConnection());
        }
        System.out.println("Connection pool initialized with 10 connections");
    }

    @PreDestroy
    public void cleanup() {
        // Runs BEFORE Spring destroys this bean (on app shutdown)
        pool.forEach(Connection::close);
        System.out.println("All connections closed");
    }
}
```

---

## 1.7 ApplicationContext — The IoC Container

`ApplicationContext` is Spring's IoC container — it holds all beans and manages their lifecycle.

```java
// Spring Boot creates ApplicationContext automatically.
// But you can access it manually if needed:

@Component
public class SomeClass implements ApplicationContextAware {
    private ApplicationContext context;

    @Override
    public void setApplicationContext(ApplicationContext ctx) {
        this.context = ctx;
    }

    public void doSomething() {
        // Get any bean from the container programmatically
        PaymentService ps = context.getBean(PaymentService.class);
    }
}

// Or inject it directly:
@Service
public class DynamicLoader {
    @Autowired
    private ApplicationContext context;

    public void loadPlugin(String beanName) {
        Object bean = context.getBean(beanName);
    }
}
```

---

## Part 1 Interview Q&A

**Q: What is IoC?**
A: Inversion of Control means the framework (Spring) controls the creation and lifecycle of objects, not your code. Instead of `new MyService()`, you declare a class as a `@Component` and Spring creates and manages it.

**Q: What is Dependency Injection?**
A: DI is the mechanism for IoC. Spring identifies what dependencies a class needs (via constructor parameters, `@Autowired` fields) and automatically injects the correct objects.

**Q: What is the difference between @Component, @Service, @Repository?**
A: All three register a bean with Spring's container — functionally identical. The difference is semantic: `@Service` = business logic, `@Repository` = database layer (also translates persistence exceptions), `@Controller` = web layer. Use the right one for clarity.

**Q: What is the default bean scope in Spring?**
A: Singleton — one instance per ApplicationContext. This means Spring beans must be stateless to be thread-safe.

**Q: What is @PostConstruct?**
A: A method annotated with `@PostConstruct` runs once after Spring has fully constructed and injected the bean. Used for initialization that requires injected dependencies (which aren't available in the constructor yet for field injection).

**Q: Constructor vs field injection — which is better and why?**
A: Constructor injection is recommended. Reasons: dependencies are explicit, fields can be `final` (immutable), no reflection tricks, and the class is easier to unit test (just pass mocks to constructor).

---

# PART 2: Spring Boot Basics & Auto-Configuration

---

## 2.1 Spring vs Spring Boot

| Spring Framework | Spring Boot |
|-----------------|-------------|
| You configure everything manually (XML or Java config) | Auto-configures based on classpath |
| Must manually set up DispatcherServlet, DataSource, etc. | `@SpringBootApplication` does it all |
| No embedded server — deploy to Tomcat separately | Embedded Tomcat/Jetty included |
| Lots of boilerplate | Minimal boilerplate |

Spring Boot is **not a replacement** for Spring — it's Spring Framework + auto-configuration + embedded server + opinionated defaults.

---

## 2.2 Project Structure

```
my-app/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/neuralmetrics/app/
│   │   │       ├── MyApplication.java          ← Entry point
│   │   │       ├── controller/
│   │   │       │   └── UserController.java
│   │   │       ├── service/
│   │   │       │   └── UserService.java
│   │   │       ├── repository/
│   │   │       │   └── UserRepository.java
│   │   │       ├── model/
│   │   │       │   └── User.java               ← JPA Entity
│   │   │       ├── dto/
│   │   │       │   ├── UserRequest.java         ← Input DTO
│   │   │       │   └── UserResponse.java        ← Output DTO
│   │   │       ├── exception/
│   │   │       │   ├── GlobalExceptionHandler.java
│   │   │       │   └── UserNotFoundException.java
│   │   │       └── config/
│   │   │           └── SecurityConfig.java
│   │   └── resources/
│   │       ├── application.properties           ← Config
│   │       ├── application-dev.properties       ← Dev profile
│   │       └── application-prod.properties      ← Prod profile
│   └── test/
│       └── java/
│           └── com/neuralmetrics/app/
│               └── UserControllerTest.java
├── pom.xml                                      ← Maven config
```

**Layered Architecture:**
```
HTTP Request
    │
    ▼
Controller    (handles HTTP, validates input, calls service)
    │
    ▼
Service       (business logic, calls repository)
    │
    ▼
Repository    (database operations)
    │
    ▼
Database
```

---

## 2.3 @SpringBootApplication — What It Does

```java
@SpringBootApplication   // This one annotation does A LOT
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

`@SpringBootApplication` is a composed annotation of three things:

```java
@SpringBootConfiguration    // = @Configuration — this is a config class
@EnableAutoConfiguration    // MAGIC — auto-configure based on classpath
@ComponentScan              // scan this package + subpackages for @Component classes
public @interface SpringBootApplication { }
```

### What Happens on `SpringApplication.run()`?

```
1. Creates SpringApplication instance
2. Determines application type (Servlet/Reactive/None)
3. Loads ApplicationListeners and Initializers from META-INF/spring.factories
4. Runs: SpringApplicationRunListeners.starting()
5. Prepares Environment (loads application.properties)
6. Prints the Spring Boot banner
7. Creates ApplicationContext (AnnotationConfigServletWebServerApplicationContext)
8. Runs @EnableAutoConfiguration — scans META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
   → Loads relevant auto-configuration classes based on what's on the classpath
   → e.g., DataSourceAutoConfiguration if spring-data-jpa is on classpath
   → e.g., SecurityAutoConfiguration if spring-security is on classpath
9. ComponentScan — finds all @Component, @Service, @Repository, @Controller
10. Creates and wires all beans
11. Runs ApplicationRunner / CommandLineRunner beans
12. Starts embedded Tomcat server (default port 8080)
13. Application is READY
```

---

## 2.4 Auto-Configuration Internals

This is the "magic" that makes Spring Boot work. Here's how it works:

```
Your pom.xml:
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
         │
         ▼
This adds to classpath: Hibernate, Spring Data JPA, HikariCP, Spring JDBC
         │
         ▼
@EnableAutoConfiguration reads:
META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
         │
         ▼
Finds: DataSourceAutoConfiguration, HibernateJpaAutoConfiguration, etc.
         │
         ▼
@ConditionalOnClass(DataSource.class)    ← is DataSource on classpath? YES
@ConditionalOnMissingBean(DataSource.class)  ← did user define their own? NO
         │
         ▼
Spring Boot auto-creates DataSource bean using application.properties values:
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=postgres
spring.datasource.password=secret
```

You can always override auto-configuration by defining your own bean — `@ConditionalOnMissingBean` means "only auto-configure if the user hasn't already defined one."

---

## 2.5 application.properties vs application.yml

```properties
# application.properties style
server.port=8080
spring.datasource.url=jdbc:postgresql://localhost:5432/neuraldb
spring.datasource.username=postgres
spring.datasource.password=secret
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
logging.level.com.neuralmetrics=DEBUG
```

```yaml
# application.yml style (same config, YAML format)
server:
  port: 8080
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/neuraldb
    username: postgres
    password: secret
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
logging:
  level:
    com.neuralmetrics: DEBUG
```

### Profiles

```properties
# application-dev.properties
spring.datasource.url=jdbc:h2:mem:testdb   # in-memory for dev
spring.jpa.show-sql=true

# application-prod.properties
spring.datasource.url=jdbc:postgresql://prod-server:5432/neuraldb
spring.jpa.show-sql=false
```

```bash
# Activate profile:
java -jar app.jar --spring.profiles.active=dev
# or in application.properties:
spring.profiles.active=dev
```

---

## 2.6 Maven pom.xml for Spring Boot

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <!-- Spring Boot parent — manages ALL dependency versions for you -->
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
    </parent>

    <groupId>com.neuralmetrics</groupId>
    <artifactId>insurance-api</artifactId>
    <version>1.0.0</version>

    <dependencies>
        <!-- Web: Spring MVC + embedded Tomcat -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- JPA: Hibernate + Spring Data JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- Security: Spring Security -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>

        <!-- Validation: Bean Validation (Hibernate Validator) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- PostgreSQL driver -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- JWT -->
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>0.12.3</version>
        </dependency>

        <!-- Lombok: reduces boilerplate -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

---

## Part 2 Interview Q&A

**Q: What does @SpringBootApplication do?**
A: It combines three annotations: `@SpringBootConfiguration` (marks as config class), `@EnableAutoConfiguration` (triggers auto-configuration based on classpath), and `@ComponentScan` (scans current package and sub-packages for Spring components).

**Q: What is auto-configuration in Spring Boot?**
A: Spring Boot reads all auto-configuration classes from META-INF/spring/AutoConfiguration.imports. Each class uses `@Conditional` annotations (like `@ConditionalOnClass`) to decide whether to activate. If you add `spring-boot-starter-data-jpa`, Spring Boot sees Hibernate on the classpath and automatically creates DataSource, EntityManagerFactory, and TransactionManager beans using your `application.properties` values — you write zero configuration code.

**Q: What is a Spring Boot Starter?**
A: A convenience dependency that bundles related libraries together. `spring-boot-starter-web` includes Spring MVC, Jackson (JSON), Tomcat, and Spring core. `spring-boot-starter-data-jpa` includes Hibernate, Spring Data JPA, and HikariCP (connection pool). Instead of adding 5 separate dependencies, you add one starter.

**Q: What is the difference between application.properties and profiles?**
A: `application.properties` is the default config loaded always. Profile-specific files like `application-dev.properties` are loaded on top when that profile is active, overriding default values. This lets you use different databases, ports, and settings per environment without code changes.

---

# PART 3: REST APIs — Controllers, Validation, Exception Handling

---

## 3.1 Request Lifecycle in Spring MVC

```
HTTP Request: POST /api/users
      │
      ▼
Embedded Tomcat (port 8080) receives it
      │
      ▼
DispatcherServlet (Front Controller — all requests go here first)
      │
      ▼
HandlerMapping — finds which Controller method handles POST /api/users
      │
      ▼
HandlerAdapter — calls the method, converts JSON body to Java object
      │
      ▼
Your Controller method runs
      │
      ▼
Return value (ResponseEntity / object) → HttpMessageConverter → JSON
      │
      ▼
HTTP Response sent back
```

---

## 3.2 Building REST Controllers

```java
@RestController                    // = @Controller + @ResponseBody (auto-serialize return to JSON)
@RequestMapping("/api/users")      // base path for all methods in this class
public class UserController {

    private final UserService userService;

    // Constructor injection (no @Autowired needed — Spring detects single constructor)
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // GET /api/users
    @GetMapping
    public ResponseEntity<List<UserResponse>> getAllUsers() {
        List<UserResponse> users = userService.getAllUsers();
        return ResponseEntity.ok(users);  // 200 OK + body
    }

    // GET /api/users/42
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUserById(@PathVariable Long id) {
        UserResponse user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }

    // GET /api/users?page=0&size=10&role=ADMIN
    @GetMapping("/search")
    public ResponseEntity<List<UserResponse>> searchUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String role) {
        return ResponseEntity.ok(userService.search(page, size, role));
    }

    // POST /api/users  (body: {"name":"Alice","email":"alice@example.com"})
    @PostMapping
    public ResponseEntity<UserResponse> createUser(
            @RequestBody @Valid UserRequest request) {  // @Valid triggers validation
        UserResponse created = userService.createUser(request);
        return ResponseEntity
                .status(HttpStatus.CREATED)           // 201 Created
                .body(created);
    }

    // PUT /api/users/42  (full update)
    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable Long id,
            @RequestBody @Valid UserRequest request) {
        return ResponseEntity.ok(userService.updateUser(id, request));
    }

    // PATCH /api/users/42  (partial update)
    @PatchMapping("/{id}/status")
    public ResponseEntity<UserResponse> updateStatus(
            @PathVariable Long id,
            @RequestParam String status) {
        return ResponseEntity.ok(userService.updateStatus(id, status));
    }

    // DELETE /api/users/42
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();  // 204 No Content
    }
}
```

---

## 3.3 DTOs — Data Transfer Objects

Never expose your Entity directly in API responses. Use DTOs:

```java
// INPUT DTO — what the client sends
public class UserRequest {
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be 2-100 characters")
    private String name;

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    @Pattern(regexp = "^(?=.*[A-Z])(?=.*[0-9]).+$",
             message = "Password must contain at least one uppercase letter and one digit")
    private String password;

    @NotNull(message = "Age is required")
    @Min(value = 18, message = "Must be at least 18 years old")
    @Max(value = 120, message = "Invalid age")
    private Integer age;

    // Getters and setters (or use Lombok @Data)
}

// OUTPUT DTO — what the API returns (never expose password hash!)
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    private String role;
    private LocalDateTime createdAt;
    // NO password field!
}
```

**Why DTOs and not Entities?**
- Entities may have fields you don't want to expose (password, internal flags)
- Entities can have circular references that break JSON serialization
- API contract is independent of database schema — you can change one without breaking the other

---

## 3.4 Validation

Spring Boot uses Hibernate Validator (Bean Validation 3.0):

```java
// Common validation annotations:
@NotNull              // field must not be null
@NotBlank             // string must not be null, empty, or whitespace
@NotEmpty             // collection/string must not be null or empty
@Size(min=2, max=50)  // string/collection size range
@Min(18)              // number minimum value
@Max(100)             // number maximum value
@Email                // valid email format
@Pattern(regexp="...") // matches regex
@Past                 // date must be in the past
@Future               // date must be in the future
@Positive             // number must be > 0
@PositiveOrZero       // number must be >= 0

// Custom validation example:
@Constraint(validatedBy = PhoneValidator.class)
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidPhone {
    String message() default "Invalid phone number";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

public class PhoneValidator implements ConstraintValidator<ValidPhone, String> {
    @Override
    public boolean isValid(String phone, ConstraintValidatorContext ctx) {
        if (phone == null) return true;
        return phone.matches("^\\+?[1-9]\\d{9,14}$");
    }
}
```

Trigger validation on controller with `@Valid` or `@Validated`:

```java
@PostMapping
public ResponseEntity<UserResponse> createUser(@RequestBody @Valid UserRequest request) {
    // If validation fails, Spring throws MethodArgumentNotValidException
    // before your method body runs at all
}
```

---

## 3.5 Exception Handling — Global Handler

```java
// Custom exceptions:
public class UserNotFoundException extends RuntimeException {
    private final Long userId;

    public UserNotFoundException(Long userId) {
        super("User not found with id: " + userId);
        this.userId = userId;
    }

    public Long getUserId() { return userId; }
}

public class DuplicateEmailException extends RuntimeException {
    public DuplicateEmailException(String email) {
        super("Email already exists: " + email);
    }
}
```

```java
// Standard error response DTO:
public class ErrorResponse {
    private int status;
    private String error;
    private String message;
    private LocalDateTime timestamp;
    private Map<String, String> fieldErrors;  // for validation errors

    // Constructor, getters...
    public static ErrorResponse of(int status, String error, String message) {
        ErrorResponse r = new ErrorResponse();
        r.status = status;
        r.error = error;
        r.message = message;
        r.timestamp = LocalDateTime.now();
        return r;
    }
}
```

```java
// Global Exception Handler — catches exceptions from ALL controllers:
@RestControllerAdvice   // = @ControllerAdvice + @ResponseBody
public class GlobalExceptionHandler {

    // Handle: resource not found
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = ErrorResponse.of(
            404, "Not Found", ex.getMessage()
        );
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    // Handle: duplicate resource
    @ExceptionHandler(DuplicateEmailException.class)
    public ResponseEntity<ErrorResponse> handleDuplicate(DuplicateEmailException ex) {
        ErrorResponse error = ErrorResponse.of(
            409, "Conflict", ex.getMessage()
        );
        return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
    }

    // Handle: @Valid validation failures
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> fieldErrors = new HashMap<>();
        ex.getBindingResult()
          .getFieldErrors()
          .forEach(err -> fieldErrors.put(err.getField(), err.getDefaultMessage()));

        ErrorResponse error = ErrorResponse.of(
            400, "Validation Failed", "Request has invalid fields"
        );
        error.setFieldErrors(fieldErrors);
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }

    // Handle: illegal arguments
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErrorResponse> handleIllegalArg(IllegalArgumentException ex) {
        return ResponseEntity.badRequest()
            .body(ErrorResponse.of(400, "Bad Request", ex.getMessage()));
    }

    // Catch-all — any unhandled exception
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneral(Exception ex) {
        // Log the real error for debugging:
        log.error("Unhandled exception", ex);
        // Return generic message (don't expose internals to client):
        return ResponseEntity.internalServerError()
            .body(ErrorResponse.of(500, "Internal Server Error",
                "An unexpected error occurred"));
    }
}
```

**Validation error response example:**
```json
{
  "status": 400,
  "error": "Validation Failed",
  "message": "Request has invalid fields",
  "timestamp": "2024-01-15T10:30:00",
  "fieldErrors": {
    "email": "Invalid email format",
    "password": "Password must be at least 8 characters",
    "age": "Must be at least 18 years old"
  }
}
```

---

## 3.6 Service Layer

```java
@Service
@Transactional  // all public methods wrapped in a transaction
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional(readOnly = true)  // optimizes read-only operations
    public List<UserResponse> getAllUsers() {
        return userRepository.findAll()
                .stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public UserResponse getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException(id));  // throws if not found
        return mapToResponse(user);
    }

    public UserResponse createUser(UserRequest request) {
        // Check duplicate email
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateEmailException(request.getEmail());
        }

        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        user.setRole("USER");
        user.setCreatedAt(LocalDateTime.now());

        User saved = userRepository.save(user);
        return mapToResponse(saved);
    }

    public void deleteUser(Long id) {
        if (!userRepository.existsById(id)) {
            throw new UserNotFoundException(id);
        }
        userRepository.deleteById(id);
    }

    // Private mapping method — Entity → DTO
    private UserResponse mapToResponse(User user) {
        UserResponse response = new UserResponse();
        response.setId(user.getId());
        response.setName(user.getName());
        response.setEmail(user.getEmail());
        response.setRole(user.getRole());
        response.setCreatedAt(user.getCreatedAt());
        return response;
    }
}
```

---

## Part 3 Interview Q&A

**Q: What is the difference between @Controller and @RestController?**
A: `@Controller` marks a class as a web controller. Methods return view names (for server-side rendering with templates). `@RestController` = `@Controller` + `@ResponseBody` on every method — return values are automatically serialized to JSON/XML. For REST APIs, always use `@RestController`.

**Q: What is @PathVariable vs @RequestParam?**
A: `@PathVariable` extracts values from the URI path — `/users/{id}` → `@PathVariable Long id`. `@RequestParam` extracts values from the query string — `/users?page=0&size=10` → `@RequestParam int page`. Use path variables for resource identity, query params for filtering/pagination.

**Q: How does validation work with @Valid?**
A: `@Valid` on a `@RequestBody` parameter triggers Bean Validation before the method body executes. If any constraint is violated, Spring throws `MethodArgumentNotValidException`. You catch this in `@RestControllerAdvice` to return a proper 400 response with field-level error details.

**Q: What is @RestControllerAdvice?**
A: A global exception handler. `@ExceptionHandler` methods in this class catch exceptions thrown anywhere in any controller. Without it, every controller needs its own try-catch. With it, exception handling is centralized — one place to define how each exception type maps to an HTTP response.

**Q: What is the difference between PUT and PATCH?**
A: PUT replaces the entire resource — you send all fields, and they all get updated. PATCH partially updates — you send only the fields you want to change. PUT is idempotent (sending the same request twice gives the same result). PATCH may or may not be idempotent depending on implementation.

**Q: Why use DTOs instead of returning Entities directly?**
A: Entities may expose sensitive data (password hashes), have circular references breaking JSON serialization, or couple the API contract to the database schema. DTOs decouple what the API exposes from how data is stored — you can change either without breaking the other.

---

# PART 4: Spring Data JPA — Hibernate, Relationships, N+1, Transactions

---

## 4.1 ORM and JPA Basics

**ORM (Object-Relational Mapping):** Maps Java objects to database tables automatically. You work with Java objects; ORM generates SQL.

**JPA (Jakarta Persistence API):** The specification (interface). Defines annotations like `@Entity`, `@Table`, `@Column`.

**Hibernate:** The most popular JPA implementation. Does the actual SQL generation and execution.

**Spring Data JPA:** Adds repository abstraction on top of JPA/Hibernate. You write an interface; Spring generates the implementation.

```
Your Code → Spring Data JPA → JPA (Specification) → Hibernate (Implementation) → JDBC → Database
```

---

## 4.2 Entity Design

```java
@Entity                          // marks this as a JPA entity
@Table(name = "users",           // maps to "users" table
       uniqueConstraints = {
           @UniqueConstraint(columnNames = "email")
       })
public class User {

    @Id                          // primary key
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // auto-increment (DB generates)
    private Long id;

    @Column(name = "full_name",
            nullable = false,
            length = 100)
    private String name;

    @Column(unique = true, nullable = false)
    private String email;

    @Column(name = "password_hash", nullable = false)
    private String passwordHash;

    @Enumerated(EnumType.STRING)  // store enum as "USER"/"ADMIN" string, not 0/1
    @Column(nullable = false)
    private Role role = Role.USER;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "is_active")
    private boolean active = true;

    // Standard getters/setters (or use Lombok @Entity + @Data/@Getter/@Setter)
}

public enum Role { USER, ADMIN, MODERATOR }
```

### Generated DDL (what Spring/Hibernate creates):

```sql
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,
    full_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role        VARCHAR(50) NOT NULL DEFAULT 'USER',
    created_at  TIMESTAMP,
    is_active   BOOLEAN DEFAULT TRUE
);
```

---

## 4.3 Repositories

```java
// Just write the interface — Spring generates the implementation at startup
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // JpaRepository gives you for free:
    // save(entity), findById(id), findAll(), deleteById(id),
    // count(), existsById(id), saveAll(list), etc.

    // Derived query methods — Spring parses method names to generate SQL:
    Optional<User> findByEmail(String email);
    // SQL: SELECT * FROM users WHERE email = ?

    boolean existsByEmail(String email);
    // SQL: SELECT COUNT(*) > 0 FROM users WHERE email = ?

    List<User> findByRole(Role role);
    // SQL: SELECT * FROM users WHERE role = ?

    List<User> findByActiveTrue();
    // SQL: SELECT * FROM users WHERE is_active = true

    List<User> findByNameContainingIgnoreCase(String name);
    // SQL: SELECT * FROM users WHERE LOWER(full_name) LIKE LOWER('%name%')

    List<User> findByRoleAndActiveTrue(Role role);
    // SQL: SELECT * FROM users WHERE role = ? AND is_active = true

    List<User> findByCreatedAtBetween(LocalDateTime start, LocalDateTime end);
    // SQL: SELECT * FROM users WHERE created_at BETWEEN ? AND ?

    // Custom JPQL query (object-oriented SQL):
    @Query("SELECT u FROM User u WHERE u.email = :email AND u.active = true")
    Optional<User> findActiveByEmail(@Param("email") String email);

    // Native SQL query:
    @Query(value = "SELECT * FROM users WHERE email = :email", nativeQuery = true)
    Optional<User> findByEmailNative(@Param("email") String email);

    // Update query — needs @Modifying + @Transactional
    @Modifying
    @Transactional
    @Query("UPDATE User u SET u.active = false WHERE u.id = :id")
    int deactivateUser(@Param("id") Long id);

    // Pagination:
    Page<User> findByRole(Role role, Pageable pageable);
}
```

```java
// Using pagination in service:
@Transactional(readOnly = true)
public Page<UserResponse> getUsers(int page, int size, String sortBy) {
    Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy).ascending());
    // SQL: SELECT * FROM users ORDER BY name ASC LIMIT 10 OFFSET 0
    return userRepository.findAll(pageable).map(this::mapToResponse);
}
```

---

## 4.4 Relationships

### One-To-Many / Many-To-One (Most Common)

```
One User has Many Orders
One Order belongs to One User
```

```java
@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;

    // One user has many orders
    @OneToMany(mappedBy = "user",          // "user" = field name in Order class
               cascade = CascadeType.ALL,  // save/delete user cascades to orders
               fetch = FetchType.LAZY)     // orders NOT loaded unless accessed
    private List<Order> orders = new ArrayList<>();
}

@Entity
@Table(name = "orders")
public class Order {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Double amount;

    // Many orders belong to one user
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)  // foreign key column
    private User user;
}
```

**Generated SQL:**
```sql
CREATE TABLE orders (
    id      BIGSERIAL PRIMARY KEY,
    amount  DECIMAL(10, 2),
    user_id BIGINT NOT NULL REFERENCES users(id)  -- FK from @JoinColumn
);
```

### One-To-One

```java
@Entity
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "profile_id", referencedColumnName = "id")
    private UserProfile profile;
}

@Entity
public class UserProfile {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String bio;
    private String avatarUrl;

    @OneToOne(mappedBy = "profile")
    private User user;
}
```

### Many-To-Many

```java
@Entity
public class Student {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;

    @ManyToMany
    @JoinTable(
        name = "student_courses",             // join table name
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id")
    )
    private Set<Course> courses = new HashSet<>();
}

@Entity
public class Course {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String title;

    @ManyToMany(mappedBy = "courses")
    private Set<Student> students = new HashSet<>();
}
```

**Generated join table SQL:**
```sql
CREATE TABLE student_courses (
    student_id BIGINT REFERENCES students(id),
    course_id  BIGINT REFERENCES courses(id),
    PRIMARY KEY (student_id, course_id)
);
```

---

## 4.5 Lazy vs Eager Loading

```java
// LAZY (default for @OneToMany, @ManyToMany):
// Related entities are NOT loaded until you access them
@OneToMany(fetch = FetchType.LAZY)
private List<Order> orders;

User user = userRepository.findById(1L).get();
// SQL: SELECT * FROM users WHERE id = 1   (orders NOT loaded)

user.getOrders();  // ACCESS triggers another SQL:
// SQL: SELECT * FROM orders WHERE user_id = 1   (loaded now)

// EAGER (default for @ManyToOne, @OneToOne):
// Related entities loaded immediately with parent
@ManyToOne(fetch = FetchType.EAGER)
private User user;

Order order = orderRepository.findById(1L).get();
// SQL: SELECT o.*, u.* FROM orders o JOIN users u ON o.user_id = u.id WHERE o.id = 1
// User loaded immediately with Order
```

---

## 4.6 The N+1 Problem (Critical Interview Topic)

This is one of the most important JPA concepts for interviews.

**The problem:**
```java
// You fetch 10 users (1 query)
List<User> users = userRepository.findAll();
// SQL 1: SELECT * FROM users

// Then in a loop, you access each user's orders (1 query PER user)
for (User user : users) {
    System.out.println(user.getOrders().size());
    // SQL 2:  SELECT * FROM orders WHERE user_id = 1
    // SQL 3:  SELECT * FROM orders WHERE user_id = 2
    // SQL 4:  SELECT * FROM orders WHERE user_id = 3
    // ... 10 more queries!
}
// Total: 1 + 10 = 11 queries = N+1 problem!
```

**Solution 1: JOIN FETCH (fetch in one query)**
```java
@Query("SELECT DISTINCT u FROM User u LEFT JOIN FETCH u.orders")
List<User> findAllWithOrders();
// SQL: SELECT DISTINCT u.*, o.* FROM users u LEFT JOIN orders o ON u.id = o.user_id
// 1 query instead of N+1!
```

**Solution 2: @EntityGraph**
```java
@EntityGraph(attributePaths = {"orders"})
List<User> findAll();
// Hibernate generates a JOIN query automatically
```

**Solution 3: @BatchSize (loads in batches)**
```java
@OneToMany(fetch = FetchType.LAZY)
@BatchSize(size = 25)   // loads up to 25 users' orders in one query
private List<Order> orders;
// SQL: SELECT * FROM orders WHERE user_id IN (1,2,3,...,25)
```

---

## 4.7 Transactions

```java
@Service
@Transactional  // class-level: all public methods are transactional by default
public class BankingService {

    @Transactional  // method-level overrides class-level
    public void transfer(Long fromId, Long toId, BigDecimal amount) {
        Account from = accountRepo.findById(fromId)
            .orElseThrow(() -> new AccountNotFoundException(fromId));
        Account to = accountRepo.findById(toId)
            .orElseThrow(() -> new AccountNotFoundException(toId));

        if (from.getBalance().compareTo(amount) < 0) {
            throw new InsufficientFundsException();
        }

        from.setBalance(from.getBalance().subtract(amount));
        to.setBalance(to.getBalance().add(amount));

        accountRepo.save(from);
        accountRepo.save(to);
        // If ANY exception occurs above, BOTH saves are rolled back
        // Either both succeed or neither does — ATOMICITY
    }

    // Read-only transaction — Hibernate skips dirty checking, better performance
    @Transactional(readOnly = true)
    public AccountResponse getAccount(Long id) {
        return accountRepo.findById(id).map(this::mapToResponse)
            .orElseThrow(() -> new AccountNotFoundException(id));
    }

    // Propagation: what to do if a transaction already exists
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logAuditEntry(String action) {
        // Always runs in its own NEW transaction
        // Even if the calling transaction rolls back, this log entry is committed
        auditRepo.save(new AuditLog(action, LocalDateTime.now()));
    }
}
```

### Transaction Propagation Types

| Propagation | Behavior |
|-------------|----------|
| `REQUIRED` (default) | Join existing transaction; create new if none |
| `REQUIRES_NEW` | Always create new transaction; suspend existing |
| `SUPPORTS` | Use existing if present; run non-transactional if none |
| `MANDATORY` | Must have existing transaction; throw if none |
| `NEVER` | Must NOT be in a transaction; throw if one exists |
| `NOT_SUPPORTED` | Suspend existing transaction; run non-transactional |

### @Transactional self-invocation bug:

```java
@Service
public class UserService {

    public void processUser(Long id) {
        updateUser(id);  // CALLS INTERNAL METHOD — @Transactional IGNORED!
    }

    @Transactional  // This annotation has NO effect when called from same class!
    public void updateUser(Long id) {
        // transaction does NOT wrap this when called from processUser() above
    }
}
```

**Why:** Spring transactions use AOP proxies. The proxy wraps your class from outside. Internal method calls bypass the proxy entirely. **Fix:** Extract `updateUser` to a separate `@Service` class.

---

## Part 4 Interview Q&A

**Q: What is JPA and Hibernate?**
A: JPA (Jakarta Persistence API) is the Java specification for ORM — it defines annotations like `@Entity`, `@OneToMany` and interfaces like `EntityManager`. Hibernate is the most popular implementation of JPA — it does the actual SQL generation and execution.

**Q: What is the N+1 problem?**
A: When fetching N entities triggers N additional queries to load their associations. Example: fetching 100 orders and then accessing each order's user triggers 100 extra SELECT queries. Fix with JOIN FETCH in JPQL, `@EntityGraph`, or `@BatchSize`.

**Q: What is the difference between FetchType.LAZY and EAGER?**
A: LAZY loads associated entities only when you first access them (separate SQL query). EAGER loads them immediately with the parent (JOIN). LAZY is default for collections and preferred — it avoids loading unnecessary data. EAGER can cause performance problems by loading too much.

**Q: What does @Transactional do?**
A: Wraps a method in a database transaction. If the method completes normally, the transaction is committed. If a RuntimeException is thrown, the transaction is rolled back — all database changes are undone. Spring implements this using AOP proxies.

**Q: Why doesn't @Transactional work on self-invoked methods?**
A: Spring transactions use AOP (Aspect-Oriented Programming) proxies. The proxy intercepts external calls and wraps them in transactions. Internal method calls (this.method()) bypass the proxy completely — the transaction annotation is never seen. Solution: move the transactional method to a different Spring bean.

**Q: What is CascadeType.ALL?**
A: It means operations on the parent entity cascade to child entities. CascadeType.ALL includes PERSIST (save), MERGE (update), REMOVE (delete), REFRESH, and DETACH. If you save a User with `cascade = CascadeType.ALL` on orders, their orders are saved too. If you delete the user, their orders are deleted too.

---

# PART 5: Spring Security + JWT Authentication

---

## 5.1 Spring Security Architecture

```
HTTP Request
     │
     ▼
SecurityFilterChain (a chain of servlet filters)
     │
     ├── UsernamePasswordAuthenticationFilter (for form login)
     ├── BasicAuthenticationFilter (for Basic auth)
     ├── JwtAuthenticationFilter (YOUR custom filter)
     ├── ExceptionTranslationFilter (401/403 handling)
     └── FilterSecurityInterceptor (authorization check)
     │
     ▼
Your Controller (only reached if all filters passed)
```

Every HTTP request passes through the filter chain. Filters authenticate the request, set the security context, or reject it with 401/403.

---

## 5.2 JWT — How It Works

**JWT (JSON Web Token):** A self-contained token that carries user identity and claims. No server-side session needed.

```
JWT Structure:   header.payload.signature

Header (Base64):  {"alg":"HS256","typ":"JWT"}
Payload (Base64): {"sub":"user@example.com","role":"USER","exp":1710000000,"iat":1709996400}
Signature:        HMACSHA256(base64(header) + "." + base64(payload), SECRET_KEY)

Full token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIn0.XXXXX
```

**Auth flow:**
```
1. Client:  POST /api/auth/login  {"email":"user@ex.com","password":"pass"}
2. Server:  verify credentials → generate JWT → return token
3. Client:  store token (localStorage/cookie)
4. Client:  GET /api/orders  →  Authorization: Bearer eyJ...
5. Server:  JwtFilter intercepts → validate token → set SecurityContext → proceed
6. Controller receives authenticated request
```

---

## 5.3 Complete JWT Implementation

### Dependencies (pom.xml additions):
```xml
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.12.3</version>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.12.3</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.12.3</version>
    <scope>runtime</scope>
</dependency>
```

### Step 1: JWT Utility Service

```java
@Component
public class JwtService {

    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.expiration:86400000}")  // 24 hours in ms (default)
    private long jwtExpiration;

    // Generate token for a user
    public String generateToken(UserDetails userDetails) {
        return generateToken(new HashMap<>(), userDetails);
    }

    public String generateToken(Map<String, Object> extraClaims, UserDetails userDetails) {
        return Jwts.builder()
                .claims(extraClaims)
                .subject(userDetails.getUsername())   // email as subject
                .issuedAt(new Date(System.currentTimeMillis()))
                .expiration(new Date(System.currentTimeMillis() + jwtExpiration))
                .signWith(getSignKey())
                .compact();
    }

    // Validate token
    public boolean isTokenValid(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return username.equals(userDetails.getUsername()) && !isTokenExpired(token);
    }

    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    private boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    private Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }

    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    private Claims extractAllClaims(String token) {
        return Jwts.parser()
                .verifyWith(getSignKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    private SecretKey getSignKey() {
        byte[] keyBytes = Decoders.BASE64.decode(secretKey);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
```

### Step 2: UserDetailsService (load user from DB)

```java
@Service
public class CustomUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    public CustomUserDetailsService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new UsernameNotFoundException("User not found: " + email));

        return org.springframework.security.core.userdetails.User.builder()
                .username(user.getEmail())
                .password(user.getPasswordHash())
                .roles(user.getRole().name())  // "USER" → "ROLE_USER"
                .build();
    }
}
```

### Step 3: JWT Filter (intercepts every request)

```java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    // OncePerRequestFilter = runs exactly once per request (not re-triggered by forwards)

    private final JwtService jwtService;
    private final UserDetailsService userDetailsService;

    public JwtAuthenticationFilter(JwtService jwtService,
                                    UserDetailsService userDetailsService) {
        this.jwtService = jwtService;
        this.userDetailsService = userDetailsService;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {

        // 1. Get Authorization header
        final String authHeader = request.getHeader("Authorization");

        // 2. If no token, skip to next filter (request will fail at authorization)
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        // 3. Extract token
        final String jwt = authHeader.substring(7);  // remove "Bearer " prefix
        final String userEmail;

        try {
            userEmail = jwtService.extractUsername(jwt);
        } catch (JwtException e) {
            // Invalid token — let request proceed unauthenticated (will be rejected by security)
            filterChain.doFilter(request, response);
            return;
        }

        // 4. If token has email and user not yet authenticated
        if (userEmail != null && SecurityContextHolder.getContext().getAuthentication() == null) {

            // 5. Load user from DB
            UserDetails userDetails = userDetailsService.loadUserByUsername(userEmail);

            // 6. Validate token
            if (jwtService.isTokenValid(jwt, userDetails)) {

                // 7. Create authentication token and set in SecurityContext
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,                          // credentials (null for JWT)
                        userDetails.getAuthorities()   // roles
                    );
                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                // 8. Tell Spring Security this request is authenticated
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        // 9. Continue to next filter
        filterChain.doFilter(request, response);
    }
}
```

### Step 4: Security Configuration

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity  // enables @PreAuthorize on methods
public class SecurityConfig {

    private final JwtAuthenticationFilter jwtAuthFilter;
    private final UserDetailsService userDetailsService;

    public SecurityConfig(JwtAuthenticationFilter jwtAuthFilter,
                          UserDetailsService userDetailsService) {
        this.jwtAuthFilter = jwtAuthFilter;
        this.userDetailsService = userDetailsService;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            // Disable CSRF (not needed for stateless JWT APIs)
            .csrf(csrf -> csrf.disable())

            // Define which endpoints are public vs protected
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()       // login, register
                .requestMatchers("/api/public/**").permitAll()     // public APIs
                .requestMatchers("/actuator/health").permitAll()   // health check
                .requestMatchers("/api/admin/**").hasRole("ADMIN") // admin only
                .anyRequest().authenticated()                       // everything else needs auth
            )

            // Stateless session — no HttpSession (JWT is our session)
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )

            // Add JWT filter BEFORE UsernamePasswordAuthenticationFilter
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    // Password encoder — BCrypt hashing
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    // Authentication manager — used in login endpoint
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config)
            throws Exception {
        return config.getAuthenticationManager();
    }

    // Wire UserDetailsService + PasswordEncoder for authentication
    @Bean
    public AuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(userDetailsService);
        provider.setPasswordEncoder(passwordEncoder());
        return provider;
    }
}
```

### Step 5: Auth Controller (Login + Register)

```java
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<UserResponse> register(@RequestBody @Valid RegisterRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                             .body(authService.register(request));
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody @Valid LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }
}

// DTOs
public class LoginRequest {
    @NotBlank @Email
    private String email;
    @NotBlank
    private String password;
}

public class AuthResponse {
    private String token;
    private String type = "Bearer";
    private String email;
    private String role;
    // constructor, getters
}
```

```java
@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;

    // Constructor injection...

    public AuthResponse login(LoginRequest request) {
        // 1. Authenticate (throws BadCredentialsException if wrong)
        authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
        );

        // 2. Load user
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new UsernameNotFoundException("User not found"));

        // 3. Generate JWT
        UserDetails userDetails = userDetailsService.loadUserByUsername(user.getEmail());
        String token = jwtService.generateToken(userDetails);

        // 4. Return token
        return new AuthResponse(token, user.getEmail(), user.getRole().name());
    }

    public UserResponse register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateEmailException(request.getEmail());
        }

        User user = new User();
        user.setName(request.getName());
        user.setEmail(request.getEmail());
        user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        user.setRole(Role.USER);
        user.setCreatedAt(LocalDateTime.now());

        return mapToResponse(userRepository.save(user));
    }
}
```

### Step 6: Method-Level Security

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    // Only ADMIN can access this endpoint
    @GetMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<List<UserResponse>> getAllUsers() { ... }

    // User can access their own data OR admin can access anyone's
    @GetMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")
    public ResponseEntity<UserResponse> getUserById(@PathVariable Long id) { ... }

    // Any authenticated user
    @GetMapping("/me")
    public ResponseEntity<UserResponse> getCurrentUser(Authentication authentication) {
        String email = authentication.getName();  // from SecurityContext
        return ResponseEntity.ok(userService.getUserByEmail(email));
    }
}
```

---

## 5.4 application.properties for Security

```properties
# JWT secret (use a strong, random base64-encoded key in production)
jwt.secret=404E635266556A586E3272357538782F413F4428472B4B6250645367566B5970
jwt.expiration=86400000

# BCrypt strength (10 = default, higher = slower but more secure)
spring.security.bcrypt.strength=10
```

---

## Part 5 Interview Q&A

**Q: What is JWT and how does it work?**
A: JWT (JSON Web Token) is a stateless authentication token. It has three parts: header (algorithm), payload (user data like email, role, expiry), and signature (HMAC of header+payload using a secret key). The server generates a JWT on login and sends it to the client. The client sends it with every request. The server verifies the signature without any database lookup — that's what makes it stateless.

**Q: What is the difference between authentication and authorization?**
A: Authentication = verifying WHO you are (login with email/password). Authorization = checking WHAT you're allowed to do (do you have the ADMIN role to access this endpoint?). In Spring Security: authentication happens at login, authorization happens at every request.

**Q: How does the JWT filter work in Spring Security?**
A: It extends `OncePerRequestFilter`. For every request, it reads the `Authorization: Bearer <token>` header, extracts and validates the JWT, loads the user from the database, and sets a `UsernamePasswordAuthenticationToken` in the `SecurityContextHolder`. This tells Spring Security the request is authenticated and what roles the user has.

**Q: Why is CSRF disabled for REST APIs?**
A: CSRF attacks rely on browsers automatically including cookies in cross-origin requests. JWT tokens are sent in the `Authorization` header, not in cookies — so CSRF doesn't apply. Cookies with CSRF protection are needed for traditional form-based web apps.

**Q: What is BCrypt and why is it used for passwords?**
A: BCrypt is a password hashing algorithm specifically designed to be slow (cost factor is configurable). Unlike MD5/SHA (fast, crackable), BCrypt makes brute-force attacks prohibitively expensive. It also includes a built-in salt (random data mixed into the hash), preventing rainbow table attacks. Never store plain-text or MD5 passwords.

**Q: What is SessionCreationPolicy.STATELESS?**
A: It tells Spring Security not to create or use HTTP sessions. Each request must carry authentication information (JWT) on its own — the server keeps no session state. This is essential for scalable APIs where any server instance should be able to handle any request.

---

# PART 6: Master Interview Q&A Cheatsheet

---

## Spring Core

| Question | Key Answer Points |
|----------|------------------|
| What is Spring Boot? | Spring Framework + auto-configuration + embedded Tomcat + opinionated defaults. Reduces boilerplate. |
| IoC vs DI | IoC = framework controls object creation. DI = mechanism — Spring injects dependencies into your classes. |
| @Component vs @Bean | `@Component` on your own class — Spring detects it. `@Bean` is a method in `@Configuration` class — you write how to create it (for third-party classes). |
| Default bean scope | Singleton — one instance per ApplicationContext. Beans must be stateless. |
| @Autowired resolution | Spring first matches by type. If multiple beans of same type exist, it matches by field name. `@Qualifier("beanName")` to be explicit. |

## REST APIs

| Question | Key Answer Points |
|----------|------------------|
| HTTP status codes | 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 500 Server Error |
| Idempotent methods | GET, PUT, DELETE are idempotent. POST is not. PATCH may or may not be. |
| @RequestBody vs @RequestParam | `@RequestBody` = JSON body of POST/PUT request. `@RequestParam` = query string `?key=value`. |
| Validation failure response | Catch `MethodArgumentNotValidException` in `@RestControllerAdvice`, return 400 with field-level errors. |

## Spring Data JPA

| Question | Key Answer Points |
|----------|------------------|
| What is JPA vs Hibernate | JPA = specification (interface). Hibernate = implementation. Like JDBC is to MySQL driver. |
| @Entity @Id @GeneratedValue | @Entity = maps to table. @Id = primary key. @GeneratedValue(IDENTITY) = DB auto-increment. |
| Lazy vs Eager | LAZY = load on access (good default). EAGER = load immediately (can cause performance issues). |
| N+1 problem | Fetching N entities then N more queries for associations. Fix: JOIN FETCH, @EntityGraph. |
| @Transactional rollback | Rolls back on RuntimeException by default. For checked exceptions: `@Transactional(rollbackFor = Exception.class)`. |
| ddl-auto options | `none`=no action, `validate`=check schema, `update`=update schema, `create`=drop+create, `create-drop`=create on start, drop on stop. Never use `create`/`create-drop` in production. |

## Spring Security + JWT

| Question | Key Answer Points |
|----------|------------------|
| JWT structure | header.payload.signature — all base64 encoded. Signature prevents tampering. |
| JWT stateless | No server session — server validates signature on every request. Scales horizontally. |
| Where JWT is stored client-side | HttpOnly cookie (most secure) or localStorage (vulnerable to XSS). |
| JWT expiry | Short-lived access token (15min-1hr) + long-lived refresh token (days). |
| BCrypt | Adaptive hashing function — slow by design. Includes salt. `passwordEncoder.encode()` and `passwordEncoder.matches()`. |
| @PreAuthorize | Method-level security. `@EnableMethodSecurity` must be on config class. Supports SpEL expressions. |

---

## Common Follow-Up Questions

**Q: How would you handle pagination in your API?**
```java
// Controller:
@GetMapping
public Page<UserResponse> getUsers(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "10") int size) {
    return userService.getUsers(PageRequest.of(page, size));
}
// Response includes: content, totalElements, totalPages, pageNumber, pageSize
```

**Q: How do you prevent SQL injection in Spring?**
A: Spring Data JPA and JPQL use parameterized queries — user input is never concatenated into SQL strings. `@Query("SELECT u FROM User u WHERE u.email = :email")` with `@Param("email")` is safe. Never use string concatenation in native queries.

**Q: What is the difference between save() and saveAndFlush() in JPA?**
A: `save()` puts the entity in Hibernate's persistence context — the INSERT may be batched and sent to DB later (within the transaction). `saveAndFlush()` immediately flushes changes to the database, useful when you need the DB-generated ID or to see changes within the same transaction.

**Q: How would you add logging to your Spring Boot app?**
```java
@Service
public class UserService {
    private static final Logger log = LoggerFactory.getLogger(UserService.class);
    // Or with Lombok: @Slf4j on the class

    public UserResponse createUser(UserRequest request) {
        log.info("Creating user with email: {}", request.getEmail());
        // ...
        log.debug("User created with id: {}", saved.getId());
        return mapToResponse(saved);
    }
}
```
```properties
# application.properties
logging.level.com.neuralmetrics=DEBUG  # your package
logging.level.org.hibernate.SQL=DEBUG  # see generated SQL
logging.level.root=INFO
```

**Q: What is @Transactional readOnly = true?**
A: Hints to Spring and Hibernate that this transaction won't modify data. Hibernate skips dirty checking (comparing entity state to detect changes) — this is a performance optimization. Also allows the database to route the query to a read replica if configured.

**Q: How do you handle circular dependencies in Spring?**
A: Best: redesign to eliminate the cycle (a sign of poor design). Alternatives: use `@Lazy` on one injection point (Spring creates a proxy, injects real bean later), or use setter injection (Spring can handle circular setter injection). Constructor injection with circular dependency = startup failure — which is actually good because it exposes the design problem.

---

## Quick Definitions (Rapid-Fire Round)

| Term | One-Line Definition |
|------|---------------------|
| IoC Container | Spring's ApplicationContext — creates, wires, and manages beans |
| Bean | Any object Spring manages |
| AOP | Aspect-Oriented Programming — cross-cutting concerns (logging, transactions, security) added without modifying business code |
| DispatcherServlet | Spring MVC's front controller — all requests route through it |
| EntityManager | JPA interface for database operations (persist, find, merge, remove) |
| HikariCP | Default Spring Boot connection pool — reuses DB connections instead of creating new ones |
| @Transactional | Wraps method in a DB transaction — commits on success, rolls back on RuntimeException |
| SecurityContext | Holds the authenticated user for the current request (ThreadLocal) |
| Principal | The authenticated user object in the SecurityContext |
| Filter Chain | Series of filters each request passes through before reaching controllers |

---

*End of Spring Boot Interview Mastery Guide*
*Covers: IoC/DI/Beans → Spring Boot/AutoConfig → REST APIs/Validation/Exceptions → JPA/Hibernate/N+1 → Security/JWT*
