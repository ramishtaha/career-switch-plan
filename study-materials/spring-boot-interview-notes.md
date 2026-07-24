# Spring Boot Deep-Dive Interview Notes

> **Target:** Mid-level Java developer (3-4 yrs) targeting product companies & BFSI GCCs at 14-18 LPA
> **Author context:** Ramish Taha — TCS System Engineer, Spring Boot/Java, BaNCS banking systems
> **Assumes:** REST APIs, JPA, CRUD basics already known. This goes DEEPER.

---

## Table of Contents

1. [IoC Container Internals](#1-ioc-container-internals)
2. [Bean Lifecycle](#2-bean-lifecycle)
3. [AOP (Aspect-Oriented Programming)](#3-aop-aspect-oriented-programming)
4. [Auto-Configuration Mechanism](#4-auto-configuration-mechanism)
5. [Spring Data JPA Deep Dive](#5-spring-data-jpa-deep-dive)
6. [Transaction Management](#6-transaction-management)
7. [Spring Security](#7-spring-security)
8. [Spring Cloud / Microservices](#8-spring-cloud--microservices)
9. [Spring Boot Actuator](#9-spring-boot-actuator)
10. [Profiles & Environment Management](#10-profiles--environment-management)
11. [Spring Boot Testing](#11-spring-boot-testing)
12. [Event-Driven Architecture](#12-event-driven-architecture)
13. [Caching](#13-caching)
14. [WebSocket Support](#14-websocket-support)

---

## Legend

- **🔴 MUST KNOW** — Asked in nearly every mid/senior interview. Be able to explain + code.
- **🟡 GOOD TO KNOW** — Asked often; deep answer sets you apart.
- **🟢 NICE TO HAVE** — Differentiator for senior roles / product companies.

---

## 1. IoC Container Internals

> **🔴 MUST KNOW**

The IoC (Inversion of Control) container is the core of Spring. It manages bean instantiation, wiring, and lifecycle.

### 1.1 What is the difference between BeanFactory and ApplicationContext?

| Feature | BeanFactory | ApplicationContext |
|---|---|---|
| Loading | Lazy by default | Eager (pre-instantiates singletons) |
| Extensions | Basic container | Adds event pub/sub, i18n, resource loading, AOP |
| Use case | Lightweight / resource-constrained | Enterprise apps (almost always this) |

`ApplicationContext` **extends** `BeanFactory`. In Spring Boot, `AnnotationConfigServletWebServerApplicationContext` is the default context.

### 1.2 Explain the internal architecture of the IoC container.

The container has three key phases:

```
1. CONFIGURATION → Read annotations/XML, build BeanDefinition objects
2. INSTANTIATION  → Create bean instances from BeanDefinitions
3. WIRING        → Inject dependencies, run lifecycle callbacks
```

**BeanDefinition** is metadata about a bean (class name, scope, init/destroy methods, constructor args, property values). The `BeanDefinitionRegistry` holds them. `BeanDefinitionReader` populates them from annotations/XML.

### 1.3 How does dependency injection actually happen under the hood?

1. Container scans `@ComponentScan` packages (via `ClassPathBeanDefinitionScanner`).
2. For each candidate, it creates a `BeanDefinition`.
3. `DefaultListableBeanFactory` resolves dependencies using `getBean()` recursively.
4. Injection via setter/field (`@Autowired` uses `AutowiredAnnotationBeanPostProcessor`) or constructor.
5. Circular references handled via **early reference (3-level cache)** — see next.

### 1.4 Explain Spring's three-level cache and circular dependency resolution.

**🔴 MUST KNOW** — Very common interview question.

Spring uses three caches in `DefaultSingletonBeanRegistry`:

| Cache | Holds | Purpose |
|---|---|---|
| `singletonObjects` (L1) | Fully initialized beans | Final, ready-to-use singletons |
| `earlySingletonObjects` (L2) | Early bean references (partially initialized) | Breaks circular ref for singletons |
| `singletonFactories` (L3) | `ObjectFactory` lambdas | Produces early references when needed |

**Flow for circular dependency (A → B → A):**

```
1. createBean(A) → instantiate A (constructor done, fields not injected)
2. Put A's ObjectFactory into L3
3. Inject A's dependencies → needs B
4. createBean(B) → instantiate B
5. Put B's ObjectFactory into L3
6. Inject B's dependencies → needs A
7. getBean(A) → L1 miss, L2 miss, L3 HIT → call ObjectFactory.getObject()
   → returns early A reference → move to L2
8. B finishes injecting A → B fully initialized → L1
9. Back to A → B reference injected → A fully initialized → L1
```

**Caveat:** Constructor injection **cannot** resolve circular deps (no way to create early reference). Use `@Lazy` or refactor. Spring **throws** `BeanCurrentlyInCreationException`.

### 1.5 Difference between `@Component`, `@Service`, `@Repository`, `@Controller`?

Functionally identical (all `@Component` stereotypes). Semantics differ:
- `@Service` — business/service layer (conveys intent)
- `@Repository` — triggers exception translation (SQLException → DataAccessException)
- `@Controller` — request mapping (web layer)
- `@Component` — generic

### 1.6 What is `@Configuration` vs `@Component` for config classes?

**🔴 MUST KNOW**

`@Configuration` uses CGLIB proxying (via `ConfigurationClassPostProcessor`) to ensure bean methods return **the same singleton instance** when called multiple times. `@Component` does NOT — calling a `@Bean` method twice creates two instances.

```java
@Configuration  // CGLIB proxied — myService() called twice returns SAME bean
public class AppConfig {
    @Bean public MyService myService() { return new MyService(myRepo()); }
    @Bean public MyRepo myRepo() { return new MyRepo(); }
}
```

Add `@Configuration(proxyBeanMethods = false)` to disable proxying (Lightweight mode, faster startup, used in Spring Boot auto-config).

### 1.7 How does `@Autowired` resolve conflicts when multiple candidates exist?

Resolution order:
1. **By type** — if exactly one match, done.
2. **By field/parameter name** — matches bean name to parameter name.
3. **`@Qualifier("beanName")`** — explicit.
4. **`@Primary`** — marks a bean as preferred among candidates.
5. If still ambiguous → `NoUniqueBeanDefinitionException`.

---

## 2. Bean Lifecycle

> **🔴 MUST KNOW**

### 2.1 Describe the complete bean lifecycle.

```
┌─────────────────────────────────────────────────────────────┐
│  1. Instantiation (constructor called)                      │
│  2. Populate Properties (@Autowired, @Value)                │
│  3. BeanNameAware.setBeanName()                             │
│  4. BeanFactoryAware.setBeanFactory()                       │
│  5. ApplicationContextAware.setApplicationContext()          │
│  6. BeanPostProcessor.postProcessBeforeInitialization() ←── hooks│
│  7. @PostConstruct                                            │
│  8. InitializingBean.afterPropertiesSet()                    │
│  9. Custom init-method (@Bean(initMethod="..."))            │
│ 10. BeanPostProcessor.postProcessAfterInitialization() ←─── hooks│
│ 11. BEAN READY FOR USE                                       │
│ 12. @PreDestroy                                              │
│ 13. DisposableBean.destroy()                                 │
│ 14. Custom destroy-method (@Bean(destroyMethod="..."))      │
│ 15. Bean GC'd                                               │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 What is BeanPostProcessor and why is it powerful?

**🔴 MUST KNOW**

`BeanPostProcessor` intercepts **every** bean before and after initialization. It's the foundation of AOP, `@Autowired`, `@Async`, etc.

```java
@Component
public class MyBeanPostProcessor implements BeanPostProcessor {

    @Override
    public Object postProcessBeforeInitialization(Object bean, String name) {
        // Runs before @PostConstruct
        if (bean instanceof Auditable) ((Auditable) bean).markCreated();
        return bean;
    }

    @Override
    public Object postProcessAfterInitialization(Object bean, String name) {
        // Runs after init. THIS is where AOP wraps beans in proxies.
        return bean;
    }
}
```

**Key insight:** `AutowireCapableBeanFactory.resolveDependency` calls `postProcessBeforeInitialization`. The `postProcessAfterInitialization` phase is where `AbstractAutoProxyCreator` wraps beans in proxies (this is how `@Transactional`, AOP proxies are created).

### 2.3 Difference between `@PostConstruct`, `InitializingBean`, and `init-method`?

All achieve the same goal (post-construction init logic). Order: `@PostConstruct` → `afterPropertiesSet()` → custom `init-method`.

| Approach | Mechanism | Coupling |
|---|---|---|
| `@PostConstruct` | JSR-250 annotation | Loosely coupled (preferred) |
| `InitializingBean` | Implement interface | Tightly coupled to Spring |
| `@Bean(initMethod=...)` | XML/annotation config | Loosely coupled, config-controlled |

### 2.4 How do you run logic before bean destruction?

Three ways (reverse order of init):

```java
@PreDestroy                    // 1. Annotation (preferred)
public void cleanup() { ... }

// 2. Implement DisposableBean
@Override public void destroy() { ... }

// 3. @Bean(destroyMethod = "cleanup")
```

### 2.5 What are `@Lazy` beans and why use them?

By default, singleton beans are eagerly instantiated at startup. `@Lazy` defers creation to first access.

**Use cases:**
- Break circular dependencies
- Speed up startup time (load rarely-used beans lazily)
- Load heavyweight resources only when needed

```java
@Lazy
@Service
public class HeavyReportService { ... }  // Created on first injection
```

### 2.6 What happens if a singleton bean injects a prototype bean?

By default, the prototype is injected **once** (at singleton creation) and **never refreshed**. The singleton keeps the same prototype instance forever.

**Fix — `@Lookup`:**

```java
@Service @Scope("singleton")
public class OrderService {
    @Lookup  // Spring overrides this method via CGLIB proxy to return a fresh prototype each call
    protected PaymentProcessor getProcessor() { return null; }
}
```

### 2.7 Explain bean scopes.

| Scope | Meaning |
|---|---|
| `singleton` (default) | One instance per IoC container |
| `prototype` | New instance every `getBean()` |
| `request` | One per HTTP request (web context) |
| `session` | One per HTTP session |
| `application` | One per `ServletContext` |
| `websocket` | One per WebSocket session |

---

## 3. AOP (Aspect-Oriented Programming)

> **🔴 MUST KNOW**

### 3.1 Core AOP terminology with a concrete example

```java
@Aspect
@Component
public class LoggingAspect {

    @Pointcut("execution(* com.example.service.*.*(..))")
    public void serviceMethods() {}

    @Before("serviceMethods()")
    public void logBefore(JoinPoint jp) { ... }

    @AfterReturning(value = "serviceMethods()", returning = "result")
    public void logAfter(JoinPoint jp, Object result) { ... }
}
```

| Term | Meaning |
|---|---|
| **Aspect** | Module cross-cutting concern (the class) |
| **Join Point** | Point where advice can be applied (in Spring = method execution) |
| **Advice** | Action taken at a join point (the method) |
| **Pointcut** | Expression matching join points (`execution(...)`) |
| **Target** | The object being advised |
| **Weaving** | Linking aspect to target (runtime proxy in Spring) |
| **Proxy** | Object wrapping target to intercept calls |

### 3.2 Types of advice

| Advice | Annotation | Timing |
|---|---|---|
| Before | `@Before` | Before method |
| After returning | `@AfterReturning` | After successful return |
| After throwing | `@AfterThrowing` | After exception |
| After (finally) | `@After` | After method (regardless) |
| Around | `@Around` | Surrounds method (most powerful) |

```java
@Around("serviceMethods()")
public Object measureTime(ProceedingJoinPoint pjp) throws Throwable {
    long start = System.currentTimeMillis();
    Object result = pjp.proceed();  // proceed() executes the target method
    log.info("Took {} ms", System.currentTimeMillis() - start);
    return result;
}
```

### 3.3 JDK dynamic proxy vs CGLIB proxy — CRITICAL

**🔴 MUST KNOW**

| | JDK Dynamic Proxy | CGLIB Proxy |
|---|---|---|
| Mechanism | `java.lang.reflect.Proxy` + `InvocationHandler` | CGLIB subclassing (extends target) |
| Requirement | Target must implement ≥1 interface | Target must not be `final` |
| Default when | Target implements interfaces | Target has no interfaces |
| Performance | Slightly slower (reflection) | Faster (generated bytecode) |
| Spring Boot 2+ | Forces CGLIB (`spring.aop.proxy-target-class=true`) by default | Same |

**Force CGLIB (proxyTargetClass=true):**

```yaml
spring.aop.proxy-target-class: true  # Default in Spring Boot 2.x+
```

**Key pitfalls:**
- **Self-invocation** bypasses proxy: calling `this.someMethod()` inside the same class does **NOT** trigger advice (proxy is not involved).
- Fix: inject self-reference (`@Lazy` self), use `AopContext.currentProxy()`, or refactor.

### 3.4 Common pointcut expressions

```java
execution(public * com.example..*(..))               // all public methods in package
execution(* com.example.service.PaymentService.pay(..))  // specific method
within(com.example.service..*)                       // all beans in package
@annotation(org.springframework.transaction.annotation.Transactional)  // annotated methods
bean(accountService)                                 // specific bean
args(String, ..)                                      // first arg is String
execution(* *.save*(..)) && args(entity)              // combine + bind
```

### 3.5 What is the difference between `join()` and `args()` in pointcuts?

- `execution()` matches method signature.
- `args()` matches runtime argument **types** (runtime matching — slower, allows binding).
- `within()` matches type statically.

### 3.6 How does `@Transactional` use AOP under the hood?

**🔴 MUST KNOW**

`@Transactional` is processed by `TransactionInterceptor` (an `Around` advice). At runtime:

1. Spring creates a CGLIB/JDK proxy of the bean.
2. When `@Transactional` method is called via the proxy:
   - `TransactionInterceptor.invoke()` begins a transaction (if needed per propagation).
   - Calls target method.
   - Commit on success, rollback on `RuntimeException`/`Error`.
3. Self-invocation bypasses proxy → no transaction.

```java
@Service
public class TransferService {
    @Transactional
    public void transfer() {
        recordAudit();  // NOT transactional — self-invocation bypasses proxy!
    }
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void recordAudit() { ... }
}
```

---

## 4. Auto-Configuration Mechanism

> **🔴 MUST KNOW**

### 4.1 How does `@SpringBootApplication` work?

`@SpringBootApplication` = `@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`.

```java
@SpringBootApplication  // equivalent to:
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(basePackages = "com.example")
public class App { ... }
```

### 4.2 Explain `@EnableAutoConfiguration` in detail.

**🔴 MUST KNOW**

`@EnableAutoConfiguration` triggers `AutoConfigurationImportSelector`. This class:

1. Loads `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (Spring Boot 2.7+) or `META-INF/spring.factories` (older).
2. Reads a list of auto-configuration classes.
3. Evaluates `@Conditional*` annotations on each class to decide whether to activate.
4. Only matching beans are registered.

### 4.3 What are the `@Conditional` annotations?

| Annotation | Activates when |
|---|---|
| `@ConditionalOnClass` | Specified class is on classpath |
| `@ConditionalOnMissingBean` | No bean of type exists yet (user override hook) |
| `@ConditionalOnBean` | A bean of type exists |
| `@ConditionalOnProperty` | A config property matches |
| `@ConditionalOnWebApplication` | It's a web app |
| `@ConditionalOnNotWebApplication` | Not a web app |
| `@ConditionalOnExpression` | SpEL expression true |
| `@ConditionalOnJava` | Java version matches |

```java
@Configuration
@ConditionalOnClass(DataSource.class)
@ConditionalOnProperty(prefix = "app.cache", name = "enabled", havingValue = "true")
@EnableConfigurationProperties(CacheProperties.class)
public class CacheAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public CacheManager cacheManager(CacheProperties props) {
        return new RedisCacheManager(props);
    }
}
```

### 4.4 How to write a custom auto-configuration?

**🟡 GOOD TO KNOW**

```
my-starter/
├── pom.xml
└── src/main/resources/
    └── META-INF/
        └── spring/
            └── org.springframework.boot.autoconfigure.AutoConfiguration.imports
```

`AutoConfiguration.imports` content:
```
com.example.starter.MyFeatureAutoConfiguration
```

```java
@AutoConfiguration
@ConditionalOnClass(MyService.class)
@EnableConfigurationProperties(MyProperties.class)
public class MyFeatureAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    @ConditionalOnProperty(prefix = "my.feature", name = "enabled", matchIfMissing = true)
    public MyService myService(MyProperties props) {
        return new MyService(props.getEndpoint());
    }
}
```

Register on classpath. When application starts, Spring Boot picks it up.

### 4.5 How does `@ConditionalOnMissingBean` enable user customization?

This is the **customization hook**. Auto-config defines a default bean `@ConditionalOnMissingBean`. If the user defines their own bean of that type, Spring Boot's default is skipped.

```java
// Auto-config (default)
@Bean @ConditionalOnMissingBean
public DataSource dataSource() { return defaultHikariDS(); }

// User overrides — auto-config backs off
@Bean
public DataSource dataSource() { return customDS(); }  // takes precedence
```

### 4.6 Difference between `spring.factories` and the new imports file?

- **Pre Spring Boot 2.7:** `META-INF/spring.factories` — single file listing auto-config classes under `EnableAutoConfiguration` key.
- **Spring Boot 2.7+:** `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` — one class per line. Cleaner, faster startup, better discoverability.
- Spring Boot 3.0 removed `spring.factories` support for auto-config.

### 4.7 How to debug auto-configuration?

```bash
# Start with debug flag — prints ConditionalEvaluationReport
java -jar app.jar --debug
```

Or use Actuator:
```yaml
management.endpoints.web.exposure.include: conditions
```
GET `/actuator/conditions` shows which configs matched and why.

---

## 5. Spring Data JPA Deep Dive

> **🔴 MUST KNOW**

### 5.1 Explain the N+1 problem and how to fix it

**🔴 MUST KNOW — Asked very frequently**

**Problem:** Fetching N parent entities triggers N additional queries to fetch lazy associations (one query per parent).

```java
@Entity
public class Order {
    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderItem> items;
}

// N+1: 1 query for orders + N queries for items (each order.getItems())
List<Order> orders = orderRepo.findAll();
orders.forEach(o -> o.getItems().size());  // N queries!
```

**Solutions:**

| Approach | How | When |
|---|---|---|
| **`@EntityGraph`** | Eager-fetch specific assoc in one query | Best — declarative, per-query |
| **JOIN FETCH in JPQL** | `SELECT o FROM Order o JOIN FETCH o.items` | Per-query control |
| **FetchType.EAGER** | Always eager (anti-pattern) | Avoid — causes cartesian issues |
| **DTO projection** | Select only needed fields | When you don't need entities |

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    @EntityGraph(attributePaths = "items")  // single query with JOIN
    List<Order> findAllWithItems();
}
```

### 5.2 Fetch types — LAZY vs EAGER

**🔴 MUST KNOW**

| | LAZY (default for `@*ToMany`) | EAGER (default for `@*ToOne`) |
|---|---|---|
| Behavior | Loaded on first access | Loaded immediately |
| Queries | Separate query per access | JOIN in parent query |
| Risk | N+1, LazyInitializationException | Cartesian product, over-fetching |

**Rule of thumb:** Keep LAZY. Eagerly fetch only via `@EntityGraph` or `JOIN FETCH` when needed.

### 5.3 `@EntityGraph` vs `JOIN FETCH` vs `@Fetch`

**🟡 GOOD TO KNOW**

- `@EntityGraph` — Declarative on repository method. Creates a fetch plan. **No duplicate root rows issue** (Hibernate dedups). Best practice.
- `JOIN FETCH` — JPQL-level. Explicit. Works well but duplicates root rows in result set if not careful.
- `@Fetch(FetchMode.SUBSELECT)` — Hibernate-specific. Runs a single sub-select for all associations. Good for `@*ToMany` across multiple roots.
- `@Fetch(FetchMode.JOIN)` — Hibernate-specific eager join. Overrides LAZY.

```java
@EntityGraph(attributePaths = {"items", "customer.address"})
List<Order> findByStatus(String status);
```

### 5.4 Difference between `persist`, `merge`, and `save`?

| Operation | JPA method | Spring Data | Behavior |
|---|---|---|---|
| Persist | `em.persist()` | `save()` if new entity | Inserts. Assigns generated ID. |
| Merge | `em.merge()` | `save()` if detached entity | Copies state to managed entity, returns managed copy. Original stays detached. |
| `saveOrUpdate` | — | — | Hibernate native: insert if no ID, update if ID exists. |

```java
@Transactional
public Order update(Order detached) {
    Order managed = em.merge(detached);  // returns NEW managed instance
    // detached is still detached; only managed changes tracked
    return managed;
}
```

### 5.5 First-level vs second-level cache

**🟡 GOOD TO KNOW**

| | L1 (Session/EntityManager) | L2 (SessionFactory) |
|---|---|---|
| Scope | Per session | Across sessions |
| Default | Enabled | Disabled (need provider config) |
| Backed by | Map in session | EhCache/Caffeine/Redis |
| Entities | All entities | `@Cacheable` entities only |

```java
@Entity
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)  // L2 cache
public class Currency { ... }

// application.yml
spring.jpa.properties.hibernate.cache.use_second_level_cache: true
spring.jpa.properties.hibernate.javax.cache.provider: org.ehcache.jsr107.EhcacheCachingProvider
```

### 5.6 What is the dirty checking mechanism?

Hibernate snapshots entity state on load. On flush, it compares current state to snapshot. If changed → generates UPDATE. This is **automatic dirty checking**.

```java
@Transactional
public void rename(Long id, String name) {
    User u = repo.findById(id).get();  // snapshot stored
    u.setName(name);                   // dirty — auto-detected
    // No save() needed. Flush commits the UPDATE.
}
```

### 5.7 JPA repository proxy — how does Spring Data implement it?

Spring Data generates a **JDK dynamic proxy** (`SimpleJpaRepository` is the target) implementing your repository interface. Method execution:

| Method type | Implementation |
|---|---|
| `findById`, `save` | Delegated to `SimpleJpaRepository` (predefined) |
| Derived queries (`findByName`) | Parsed at startup, turned into JPA Criteria |
| `@Query` methods | JPQL/native parsed and prepared |
| Custom methods | Executed via repository fragment composition |

### 5.8 Common JPA pitfalls

1. **LazyInitializationException** — Accessing lazy assoc outside transaction/session. Fix: keep in `@Transactional`, use `@EntityGraph`, or OSIV.
2. **OSIV (Open Session In View)** — Spring Boot enables by default (`spring.jpa.open-in-view=true`). Keeps session open during request rendering. **Disable in production** to catch bugs early.
3. **Flush before query** — If you modify entities and then run a JPQL query, Hibernate may not auto-flush. Use `em.flush()` or `FlushModeType.AUTO`.
4. **CascadeType** — `REMOVE` can cascade-delete more than intended. Prefer explicit child management.

---

## 6. Transaction Management

> **🔴 MUST KNOW**

### 6.1 Transaction isolation levels

**🔴 MUST KNOW**

| Isolation | Dirty Read | Non-Repeatable Read | Phantom Read |
|---|---|---|---|
| READ_UNCOMMITTED | ✅ possible | ✅ possible | ✅ possible |
| READ_COMMITTED | ❌ | ✅ possible | ✅ possible |
| REPEATABLE_READ | ❌ | ❌ | ✅ possible |
| SERIALIZABLE | ❌ | ❌ | ❌ |

```java
@Transactional(isolation = Isolation.READ_COMMITTED)
public void process() { ... }
```

**Anomalies:**
- **Dirty read** — Read uncommitted data from another txn.
- **Non-repeatable read** — Same row reads different values between two reads (another txn updated).
- **Phantom read** — New rows appear between two queries (another txn inserted).
- **Lost update** — Two txns overwrite each other.

**Default (most DBs):** READ_COMMITTED. PostgreSQL default is READ_COMMITTED. MySQL/InnoDB default is REPEATABLE_READ.

### 6.2 `@Transactional` propagation behaviors

**🔴 MUST KNOW**

| Propagation | Behavior |
|---|---|
| **REQUIRED** (default) | Use current txn; create new if none exists |
| **REQUIRES_NEW** | Always suspend current, create new txn |
| **SUPPORTS** | Use current if exists; run non-transactional otherwise |
| **NOT_SUPPORTED** | Run non-transactional; suspend current if exists |
| **NEVER** | Throw if txn exists |
| **MANDATORY** | Throw if no txn exists |
| **NESTED** | Create nested txn (savepoint) within current |

```java
@Service
public class OrderService {
    @Transactional
    public void placeOrder() {
        auditLog();  // runs in same txn as placeOrder
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void auditLog() {  // ALWAYS new txn — even if outer fails
        // audit committed independently
    }
}
```

**NESTED vs REQUIRES_NEW:**
- `NESTED` — Uses a savepoint within the same physical transaction. Rollback to savepoint only.
- `REQUIRES_NEW` — Entirely separate physical transaction. Fully independent commit/rollback.

### 6.3 Rollback rules

`@Transactional` rolls back on **unchecked** exceptions (`RuntimeException`, `Error`) by default. **Checked** exceptions do **NOT** trigger rollback unless specified.

```java
@Transactional(rollbackFor = IOException.class)  // rollback on checked too
public void importFile() throws IOException { ... }

@Transactional(noRollbackFor = BusinessException.class)  // don't rollback on this unchecked
public void process() { ... }
```

### 6.4 Common `@Transactional` pitfalls

**🔴 MUST KNOW**

1. **Self-invocation** — `methodA()` calls `methodB()` on `this`, bypasses proxy, no txn on B.
2. **Non-public methods** — By default, `@Transactional` only works on public methods (proxy-based AOP).
3. **Checked exceptions don't rollback** — Common bug.
4. **Exception swallowed** — If you catch the exception inside the method, no rollback.
5. **`REQUIRES_NEW` on same bean** — Self-invocation issue again (needs separate bean or `AopContext`).

```java
@Transactional
public void batch() {
    try {
        riskyOp();
    } catch (Exception e) {
        log.error("Failed", e);
        // PROBLEM: exception swallowed, txn commits despite failure
    }
}
```

### 6.5 PlatformTransactionManager vs JtaTransactionManager

- `PlatformTransactionManager` — Interface for all txn managers.
- `DataSourceTransactionManager` — JDBC/JPA single datasource.
- `JtaTransactionManager` — Distributed (XA) transactions across multiple resources.
- `JpaTransactionManager` — JPA-specific, bridges to `EntityManager`.

Spring Boot auto-configures the appropriate one based on dependencies.

### 6.6 How to debug transaction issues?

1. Enable txn logging: `logging.level.org.springframework.orm.jpa=DEBUG`
2. Check `TransactionSynchronizationManager.isActualTransactionActive()` in code.
3. Verify propagation/isolation in annotations.
4. Verify the method is invoked via proxy (not `this.method()`).

---

## 7. Spring Security

> **🔴 MUST KNOW for BFSI roles**

### 7.1 Spring Security filter chain — how it works

**🔴 MUST KNOW**

Spring Security is implemented as a **servlet filter chain** (`FilterChainProxy`). Each request passes through a configurable list of `Filter` instances.

```
HTTP Request
  → SecurityContextHolderFilter
  → UsernamePasswordAuthenticationFilter (form login)
  → DefaultLoginPageGeneratingFilter
  → BasicAuthenticationFilter (HTTP Basic)
  → AuthorizationFilter (URL-based RBAC)
  → ExceptionTranslationFilter
  → FilterSecurityInterceptor (method-level)
  → DispatcherServlet / Controller
```

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }
}
```

### 7.2 JWT authentication flow in Spring Boot

**🔴 MUST KNOW for BFSI**

```
1. Client POST /api/auth/login with credentials
2. AuthController → AuthenticationManager.authenticate()
3. If valid → generate JWT (signed with secret/private key)
4. Return JWT to client
5. Client sends JWT in `Authorization: Bearer <token>` header on subsequent requests
6. JwtAuthenticationFilter intercepts request:
   a. Extract token from header
   b. Validate signature + expiry
   c. Load user details → set Authentication in SecurityContext
   d. Continue filter chain → request reaches controller authenticated
```

```java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws ServletException, IOException {
        String token = extractToken(req);
        if (token != null && jwtUtil.validate(token)) {
            String username = jwtUtil.getUsername(token);
            UserDetails user = userDetailsService.loadUserByUsername(username);
            UsernamePasswordAuthenticationToken auth =
                new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
            auth.setDetails(new WebAuthenticationDetailsSource().buildDetails(req));
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
        chain.doFilter(req, res);
    }
}
```

### 7.3 OAuth2 Authorization Code flow in Spring Security

**🟡 GOOD TO KNOW**

```
1. User → client app → redirect to Authorization Server (AS) login
2. User logs in at AS, grants consent
3. AS redirects back to client with an `authorization_code`
4. Client exchanges code (+ client_secret) at AS token endpoint
5. AS returns `access_token` (+ optional `refresh_token`, `id_token`)
6. Client calls resource server APIs with `Bearer access_token`
7. Resource server validates token (introspection or JWT signature)
```

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: ${GOOGLE_CLIENT_ID}
            client-secret: ${GOOGLE_CLIENT_SECRET}
            scope: openid, profile, email
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
```

```java
http.oauth2Login(Customizer.withDefaults());  // enables OAuth2 login
```

### 7.4 RBAC vs ABAC vs PBAC

| Model | Basis | Example |
|---|---|---|
| **RBAC** (Role-Based) | Role assigned to user | `hasRole('ADMIN')` |
| **ABAC** (Attribute-Based) | Attributes of user/resource/env | `@PreAuthorize("user.dept == 'FIN'")` |
| **PBAC** (Policy-Based) | Centralized policy rules (OPA/AuthZed) | External policy engine decides |

```java
// RBAC
@PreAuthorize("hasRole('ADMIN')")
public void deleteUser(Long id) { ... }

// ABAC
@PreAuthorize("#user.id == authentication.principal.id or hasRole('ADMIN')")
public User getUser(Long id, User user) { ... }
```

### 7.5 Method-level security with `@PreAuthorize` / `@PostAuthorize`

```java
@EnableMethodSecurity  // replaces @EnableGlobalMethodSecurity (Spring Security 6)
@Configuration
public class MethodSecurityConfig { }

@Service
public class AccountService {

    @PreAuthorize("hasAuthority('ACCOUNT_READ')")
    public Account getAccount(Long id) { ... }

    @PostAuthorize("returnObject.owner == authentication.name")
    public Account getOwnAccount(Long id) { ... }  // filter result after method

    @PreFilter("filterObject.owner == authentication.name")
    public List<Account> filterAccounts(List<Account> accounts) { ... }  // filter input

    @PostFilter("filterObject.owner == authentication.name")
    public List<Account> listAccounts() { ... }  // filter output
}
```

### 7.6 SecurityContext and how it's stored

- `SecurityContext` holds the `Authentication` object.
- Default storage: `ThreadLocal` via `SecurityContextHolder` (mode `MODE_THREADLOCAL`).
- For async: use `DelegatingSecurityContextRunnable` or `MODE_INHERITABLETHREADLOCAL`.
- In reactive: stored in Reactor `Context`, not `ThreadLocal`.

### 7.7 CSRF — when to disable it

- **Enable** (default) for traditional web apps with sessions and cookies.
- **Disable** for stateless REST APIs using JWT (no session, no CSRF attack vector).
- CSRF protects against attacks where a malicious site tricks an authenticated user's browser into submitting a request. If you have no session cookie, CSRF doesn't apply.

### 7.8 Password storage — best practices

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12);  // cost factor 12
}
```

- **Never store plaintext.** Use BCrypt, Argon2, or PBKDF2 (adaptive, salt built-in).
- BCrypt cost factor should be tuned so hashing takes ~250ms.
- Use `DelegatingPasswordEncoder` to support multiple algorithms (for migration).

---

## 8. Spring Cloud / Microservices

> **🟡 GOOD TO KNOW (product companies love this)**

### 8.1 Service discovery — Eureka

```
Service Registry Pattern:
1. Microservice registers itself with Eureka Server on startup
2. Sends heartbeats every 30s (default) to stay registered
3. Client (e.g., another service) queries Eureka for instance locations
4. Load balancing via Spring Cloud LoadBalancer (client-side)

Eureka Server:
@EnableEurekaServer

Eureka Client:
@EnableDiscoveryClient
eureka.client.service-url.defaultZone: http://eureka:8761/eureka/
```

**Self-preservation mode:** If Eureka sees >85% expected heartbeats missing, it stops evicting instances (assumes network partition). This prevents cascading deregistration.

### 8.2 API Gateway — Spring Cloud Gateway

**🔴 MUST KNOW (for microservices roles)**

```java
@Configuration
public class GatewayConfig {
    @Bean
    public RouteLocator routes(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("account-service", r -> r
                .path("/api/accounts/**")
                .filters(f -> f
                    .addRequestHeader("X-Gateway", "prod")
                    .retry(3)
                    .circuitBreaker(c -> c.setName("accountsCB")
                        .setFallbackUri("forward:/fallback")))
                .uri("lb://ACCOUNT-SERVICE"))
            .build();
    }
}
```

Features: routing, load balancing, rate limiting, circuit breaking, request/response modification, JWT validation, CORS.

**Gateway vs Zuul:** Zuul 2 (Netflix) is deprecated. Spring Cloud Gateway (reactive, Netty-based) is the modern standard.

### 8.3 Circuit Breaker — Resilience4j

**🟡 GOOD TO KNOW**

```java
@Configuration
public class CircuitBreakerConfig {

    @Bean
    public CircuitBreakerRegistry registry() {
        CircuitBreakerConfig config = CircuitBreakerConfig.custom()
            .failureRateThreshold(50)            // open at 50% failures
            .slowCallRateThreshold(80)           // open at 80% slow calls
            .slowCallDurationThreshold(Duration.ofSeconds(2))
            .waitDurationInOpenState(Duration.ofSeconds(30))
            .slidingWindowSize(10)               // last 10 calls
            .slidingWindowType(SlidingWindowType.COUNT_BASED)
            .permittedNumberOfCallsInHalfOpenState(3)
            .build();
        return CircuitBreakerRegistry.of(config);
    }
}

@Service
public class PaymentClient {
    @CircuitBreaker(name = "paymentCB", fallbackMethod = "fallback")
    @TimeLimiter(name = "paymentCB")
    public CompletableFuture<Payment> pay(Order order) { ... }

    public CompletableFuture<Payment> fallback(Order order, Exception e) {
        return CompletableFuture.completedFuture(Payment.pending(order));
    }
}
```

**States:** CLOSED (normal) → OPEN (failing) → HALF_OPEN (testing recovery) → CLOSED.

| State | Behavior |
|---|---|
| CLOSED | Calls pass through; metrics collected |
| OPEN | All calls fail-fast → fallback invoked immediately |
| HALF_OPEN | Limited calls allowed to test if service recovered |

### 8.4 Saga pattern for distributed transactions

**🟡 GOOD TO KNOW — BFSI / fintech relevance**

Distributed transactions across microservices where 2PC (XA) is too slow/fragile. Two flavors:

**Choreography (event-driven):**

```
Order Service ──(OrderCreated event)──→ Payment Service
Payment Service ──(PaymentCompleted)──→ Inventory Service
Inventory Service ──(InventoryReserved)──→ Shipping Service

If Payment fails → PaymentFailed event → Order Service compensates (cancel order)
```

**Orchestration (centralized):**

```
Order Saga Orchestrator:
  1. Call Payment Service (reserve)
  2. Call Inventory Service (reserve)
  3. Call Shipping Service (ship)
  If any fails → orchestrator sends compensate commands in reverse
```

```java
// Using Axon framework or custom orchestrator
@Saga
public class OrderSaga {
    @StartSaga
    @SagaEventHandler(associationProperty = "orderId")
    public void on(OrderCreated event) {
        commandGateway.send(new ReservePaymentCommand(event.orderId, event.amount));
    }

    @SagaEventHandler
    public void on(PaymentReserved event) {
        commandGateway.send(new ReserveInventoryCommand(event.orderId));
    }

    @SagaEventHandler
    public void on(PaymentFailed event) {
        commandGateway.send(new CancelOrderCommand(event.orderId));  // compensate
    }
}
```

### 8.5 Other Spring Cloud components (quick reference)

| Component | Purpose |
|---|---|
| **Config Server** | Centralized external config (git-backed) |
| **Bus** | Broadcast config changes via AMQP/Kafka |
| **OpenFeign** | Declarative REST client (like Spring Data for HTTP) |
| **Sleuth + Zipkin** | Distributed tracing (now: Micrometer Tracing) |
| **LoadBalancer** | Client-side load balancing (replaces Ribbon) |
| **Stream** | Abstraction over Kafka/RabbitMQ |
| **Consul / Zookeeper** | Alternative service registries |

```java
// OpenFeign example
@FeignClient(name = "account-service")
public interface AccountClient {
    @GetMapping("/accounts/{id}")
    Account getAccount(@PathVariable Long id);
}
// Spring generates an HTTP client proxy — no boilerplate RestTemplate
```

---

## 9. Spring Boot Actuator

> **🟡 GOOD TO KNOW**

### 9.1 What is Actuator and what does it provide?

Actuator adds production-grade operational endpoints to your app: health, metrics, info, env, threads, caches, sessions, shutdown, and more.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,env,loggers
  endpoint:
    health:
      show-details: when_authorized
    shutdown:
      enabled: true
  info:
    env:
      enabled: true
```

### 9.2 Health checks and custom health indicators

```java
@Component
public class KafkaHealthIndicator implements HealthIndicator {

    @Override
    public Health health() {
        try {
            kafkaAdmin.describeCluster();
            return Health.up()
                .withDetail("brokers", kafkaAdmin.getBrokers())
                .build();
        } catch (Exception e) {
            return Health.down(e)
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

Built-in indicators: DB, Redis, Mongo, Disk space, Elasticsearch, RabbitMQ, etc. All aggregated at `/actuator/health`. Down → HTTP 503.

### 9.3 Metrics with Micrometer

**🟡 GOOD TO KNOW**

Actuator uses **Micrometer** as its metrics facade (vendor-neutral — exports to Prometheus, Datadog, New Relic, etc.).

```java
@Service
public class OrderService {
    private final Counter ordersCreated;
    private final Timer orderProcessingTime;

    public OrderService(MeterRegistry registry) {
        this.ordersCreated = Counter.builder("orders.created")
            .tag("type", "retail")
            .register(registry);
        this.orderProcessingTime = Timer.builder("orders.processing.time")
            .register(registry);
    }

    public void process() {
        orderProcessingTime.record(() -> {
            // work
            ordersCreated.increment();
        });
    }
}
```

Metric types: Counter, Gauge, Timer, Distribution Summary (histogram), LongTaskTimer.

### 9.4 Custom actuator endpoint

```java
@Component
@Endpoint(id = "featureflags")
public class FeatureFlagEndpoint {

    @ReadOperation
    public Map<String, Boolean> getAllFlags() {
        return featureFlagService.getAllFlags();
    }

    @ReadOperation
    public Boolean getFlag(@Selector String name) {
        return featureFlagService.getFlag(name);
    }

    @WriteOperation
    public void setFlag(@Selector String name, Boolean enabled) {
        featureFlagService.setFlag(name, enabled);
    }
}
// GET /actuator/featureflags
// GET /actuator/featureflags/{name}
// POST /actuator/featureflags/{name}?enabled=true
```

### 9.5 Securing actuator endpoints

```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"              # expose all
  server:
    port: 8081                   # separate management port
    address: 127.0.0.1           # internal only
```

Combine with security: `authorizeHttpRequests(auth -> auth.requestMatchers("/actuator/**").hasRole("ADMIN"))`.

### 9.6 Common Actuator endpoints (reference)

| Endpoint | Purpose |
|---|---|
| `/actuator/health` | App health (UP/DOWN) |
| `/actuator/info` | Build info, git commit |
| `/actuator/metrics` | Micrometer metrics |
| `/actuator/env` | Environment properties |
| `/actuator/loggers` | View/change log levels at runtime |
| `/actuator/threaddump` | Thread dump |
| `/actuator/heapdump` | Heap dump (download) |
| `/actuator/beans` | All Spring beans |
| `/actuator/conditions` | Auto-config report |
| `/actuator/mappings` | All request mappings |
| `/actuator/shutdown` | Graceful shutdown (POST) |

---

## 10. Profiles & Environment Management

> **🔴 MUST KNOW**

### 10.1 What are profiles and how to use them?

Profiles allow conditional bean registration based on the active environment (dev, prod, test).

```java
@Configuration
public class DataSourceConfig {

    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        return new EmbeddedDatabaseBuilder().setType(H2).build();
    }

    @Bean
    @Profile("prod")
    public DataSource prodDataSource() {
        return HikariDataSourceBuilder.create()
            .url(dbUrl).username(dbUser).password(dbPass).build();
    }
}
```

```yaml
# application.yml (default)
spring:
  profiles:
    active: dev  # can be overridden by --spring.profiles.active=prod
```

```yaml
# application-prod.yml
server:
  port: 8080
spring:
  datasource:
    url: jdbc:postgresql://prod-db:5432/app
```

### 10.2 How does profile resolution work?

**🔴 MUST KNOW**

Property resolution order (highest to lowest):

1. Command-line args (`--spring.profiles.active=prod`)
2. `SPRING_PROFILES_ACTIVE` env var
3. Servlet config init params
4. `ServletContext` init params
5. JNDI
6. Java system properties
7. OS env variables
8. `application-{profile}.yml` outside jar
9. `application-{profile}.yml` inside jar
10. `application.yml` outside jar
11. `application.yml` inside jar
12. `@PropertySource` annotations
13. Default properties

```bash
# Externalize config
java -jar app.jar --spring.profiles.active=prod --server.port=9090
SPRING_DATASOURCE_URL=jdbc:postgresql://db java -jar app.jar
```

### 10.3 `@ConfigurationProperties` vs `@Value`

```java
@ConfigurationProperties(prefix = "app.payment")  // Type-safe binding (preferred)
@Validated
public class PaymentProperties {
    @NotBlank private String endpoint;
    @Min(1000) private int timeout = 5000;
    private RetryPolicy retry;  // nested POJO auto-bound
    // getters/setters
}
```

```java
@Value("${app.payment.endpoint}")  // Single value, no validation, no nested
private String endpoint;
```

`@ConfigurationProperties` advantages:
- Relaxed binding (kebab-case, camelCase, snake_case, UPPER_CASE all work)
- Validation (`@Validated`)
- Nested object binding
- IDE autocompletion (with `additional-spring-configuration-metadata.json`)

### 10.4 Spring Cloud Config Server (externalized config)

**🟡 GOOD TO KNOW**

```yaml
# Config server
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/org/config-repo
          searchPaths: '{application}'  # per-app folder

# Config client
spring:
  config:
    import: optional:configserver:http://config-server:8888
  cloud:
    config:
      name: payment-service
      profile: prod
```

The config server pulls config from Git and serves it via HTTP. Clients fetch on startup. `/actuator/refresh` reloads at runtime (with `@RefreshScope`).

### 10.5 `@RefreshScope` — hot-reload beans

```java
@RefreshScope
@Service
public class DynamicConfigService {
    @Value("${feature.new.ui.enabled:false}")
    private boolean newUiEnabled;  // refreshes on /actuator/refresh
}
```

When `/actuator/refresh` is POSTed, beans annotated `@RefreshScope` are destroyed and lazily recreated on next access, reading fresh config values.

---

## 11. Spring Boot Testing

> **🔴 MUST KNOW**

### 11.1 Test annotations cheat sheet

| Annotation | What it loads | Speed | Use case |
|---|---|---|---|
| `@SpringBootTest` | Full context | Slow | Integration tests |
| `@WebMvcTest` | MVC slice (controllers + filters) | Fast | Controller unit tests |
| `@DataJpaTest` | JPA slice (repos + embedded DB) | Fast | Repository tests |
| `@JsonTest` | Jackson serializers | Very fast | DTO serialization |
| `@RestClientTest` | REST client slice | Fast | `RestTemplate`/Feign tests |
| `@MockBean` | Adds Mockito mock to context | — | Replace dep in any test |
| `@SpyBean` | Spies on real bean | — | Wrap real bean, verify calls |
| `@TestConfiguration` | Test-specific config | — | Override beans in tests |

### 11.2 `@SpringBootTest` — full integration test

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@AutoConfigureTestDatabase  // H2 replaces real DB
class OrderIntegrationTest {

    @Autowired private TestRestTemplate restTemplate;
    @Autowired private OrderRepository orderRepo;

    @Test
    void createOrder_returns201() {
        ResponseEntity<Order> resp = restTemplate.postForEntity(
            "/api/orders", new OrderDTO("ITEM1", 2), Order.class);

        assertThat(resp.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(orderRepo.count()).isEqualTo(1);
    }
}
```

`@SpringBootTest` without `webEnvironment` runs with a **mock** servlet environment (no real server).

### 11.3 `@WebMvcTest` — controller slice test

**🔴 MUST KNOW**

```java
@WebMvcTest(OrderController.class)
@Import(SecurityConfig.class)  // if you need security
class OrderControllerTest {

    @Autowired private MockMvc mockMvc;
    @MockBean private OrderService orderService;  // service mocked

    @Test
    void getOrder_returnsOk() throws Exception {
        when(orderService.findById(1L)).thenReturn(new Order(1L, "ITEM1"));

        mockMvc.perform(get("/api/orders/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.item").value("ITEM1"));
    }
}
```

Only loads the controller layer. Dependencies (services) are `@MockBean`. `MockMvc` performs requests without a real HTTP server. Fast and focused.

### 11.4 `@DataJpaTest` — repository slice test

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
// Replace.NONE uses real DB; default replaces with H2
class OrderRepositoryTest {

    @Autowired private TestEntityManager entityManager;
    @Autowired private OrderRepository orderRepo;

    @Test
    void findByName_returnsOrder() {
        entityManager.persist(new Order("ITEM1"));
        entityManager.flush();

        Order found = orderRepo.findByName("ITEM1").orElseThrow();
        assertThat(found.getName()).isEqualTo("ITEM1");
    }
}
```

Rolls back after each test by default (`@Transactional` auto-applied). Uses embedded H2 by default.

### 11.5 `@MockBean` vs `@Mock` (Mockito)

| | `@MockBean` | `@Mock` |
|---|---|---|
| Source | Spring Boot | Mockito |
| Scope | Spring context (replaces bean) | Single test class |
| When | Need to mock a Spring bean in context tests | Pure unit tests, no context |

```java
// Unit test — no Spring context needed
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock private OrderRepository orderRepo;     // Mockito mock
    @InjectMocks private OrderService orderService;  // auto-injected

    @Test
    void test() {
        when(orderRepo.findById(1L)).thenReturn(Optional.of(new Order(1L)));
        // ...
    }
}

// Slice/integration test — Spring context
@WebMvcTest(OrderController.class)
class OrderControllerTest {
    @MockBean private OrderService orderService;  // replaces in context
}
```

### 11.6 Testing `@Transactional` methods

**🟡 GOOD TO KNOW**

```java
@SpringBootTest
@Transactional  // test txn — rolls back after test (default)
class TxnTest {

    @Autowired private OrderService orderService;

    @Test
    @Rollback(false)  // keep data (or use @DirtiesContext)
    void testCommit() {
        orderService.placeOrder(new OrderDTO());
    }

    @Test
    void testRollback() {
        // even if service commits, test-level @Transactional rolls back
    }
}
```

To test actual commit behavior (not rollback), use `@Commit` or separate `@Transactional(propagation = NOT_SUPPORTED)` on the test.

### 11.7 Test containers for integration tests

**🟡 GOOD TO KNOW — product companies love this**

```java
@SpringBootTest
@Testcontainers
class OrderIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Test
    void testWithRealPostgres() { ... }
}
```

Uses real PostgreSQL in Docker. No mocking. Reliable. Start once per class (static) for speed.

---

## 12. Event-Driven Architecture

> **🟡 GOOD TO KNOW**

### 12.1 `ApplicationEvent` and `@EventListener`

```java
// Event
public record OrderCreatedEvent(Long orderId, String customerEmail) {}

// Publisher
@Service
public class OrderService {
    private final ApplicationEventPublisher publisher;

    public void placeOrder(Order order) {
        // ... save order
        publisher.publishEvent(new OrderCreatedEvent(order.getId(), order.getEmail()));
    }
}

// Listener (synchronous by default)
@Component
public class EmailListener {
    @EventListener
    public void onOrderCreated(OrderCreatedEvent event) {
        emailService.sendConfirmation(event.customerEmail());
    }
}
```

### 12.2 `@TransactionalEventListener` — publish on commit

**🟡 GOOD TO KNOW**

```java
@Component
public class AuditListener {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onOrderCreated(OrderCreatedEvent event) {
        // Only fires after the transaction commits successfully
        auditService.record(event);
    }
}
```

Phases:
- `BEFORE_COMMIT` — before txn commit
- `AFTER_COMMIT` (default) — after commit
- `AFTER_ROLLBACK` — after rollback
- `AFTER_COMPLETION` — after either

**Without this, `@EventListener` fires immediately** — even if the transaction later rolls back. This causes bugs (e.g., email sent for a failed order).

### 12.3 Async events

```java
@Component
public class EmailListener {
    @Async
    @EventListener
    public void onOrderCreated(OrderCreatedEvent event) {
        // runs on a separate thread — non-blocking
        emailService.sendConfirmation(event.customerEmail());
    }
}

// Need @EnableAsync
@Configuration @EnableAsync
public class AsyncConfig {
    @Bean
    public Executor taskExecutor() {
        return new ThreadPoolTaskExecutor() {{ setCorePoolSize(5); setMaxPoolSize(10); }};
    }
}
```

### 12.4 Spring ApplicationEvent vs Kafka/RabbitMQ

| Feature | ApplicationEvent | Kafka/RabbitMQ |
|---|---|---|
| Scope | Single JVM (in-process) | Distributed |
| Persistence | None | Persistent (durable topics) |
| Reliability | Fire-and-forget | Guaranteed delivery |
| Ordering | Call order | Partition order |
| Use case | Domain events within app | Cross-service events |

**Pattern:** Use `ApplicationEvent` for internal domain events. Publish to Kafka/RabbitMQ (from `@TransactionalEventListener`) for cross-service communication.

---

## 13. Caching

> **🟡 GOOD TO KNOW**

### 13.1 `@Cacheable`, `@CacheEvict`, `@CachePut`

**🔴 MUST KNOW**

```java
@Service
public class ProductService {

    @Cacheable(value = "products", key = "#id")  // Check cache first; if miss, run method and cache result
    public Product getProduct(Long id) {
        return productRepo.findById(id).orElseThrow();  // only runs on cache miss
    }

    @CacheEvict(value = "products", key = "#product.id")  // Remove from cache
    public Product updateProduct(Product product) {
        return productRepo.save(product);
    }

    @CachePut(value = "products", key = "#product.id")  // Always run method; update cache with result
    public Product refreshProduct(Product product) {
        return productRepo.save(product);
    }

    @CacheEvict(value = "products", allEntries = true)  // Clear entire cache
    public void clearCache() { }
}
```

| Annotation | Behavior |
|---|---|
| `@Cacheable` | Cache miss → execute → store result. Hit → return cached, skip method |
| `@CacheEvict` | Remove entries (by key or all) |
| `@CachePut` | Always execute method; update cache with return |
| `@Caching` | Combine multiple cache operations |
| `@CacheConfig` | Class-level default cache config |

### 13.2 How Spring caching works under the hood

1. `CacheInterceptor` (AOP Around advice) intercepts `@Cacheable` methods.
2. Computes cache key from SpEL `key` expression (or generate via `KeyGenerator`).
3. Checks `CacheManager.getCache(name).get(key)`.
4. If hit → return cached value (method skipped).
5. If miss → proceed, cache result.
6. `@CachePut` → proceed always, then `cache.put`.
7. `@CacheEvict` → proceed, then `cache.evict`.

### 13.3 Redis integration

**🟡 GOOD TO KNOW — BFSI relevant**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

```yaml
spring:
  cache:
    type: redis
    redis:
      time-to-live: 10m     # TTL on all cache entries
      cache-nulls: false
  data:
    redis:
      host: redis-cluster
      port: 6379
      password: ${REDIS_PASSWORD}
```

```java
@Configuration
public class RedisCacheConfig {

    @Bean
    public RedisCacheManager cacheManager(RedisConnectionFactory factory) {
        RedisCacheConfiguration defaultConfig = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .serializeKeysWith(RedisSerializationContext.SerializationPair
                .fromSerializer(new StringRedisSerializer()))
            .serializeValuesWith(RedisSerializationContext.SerializationPair
                .fromSerializer(new GenericJackson2JsonRedisSerializer()))
            .disableCachingNullValues();

        // Per-cache TTL
        Map<String, RedisCacheConfiguration> perCache = Map.of(
            "products", defaultConfig.entryTtl(Duration.ofMinutes(30)),
            "users", defaultConfig.entryTtl(Duration.ofHours(1))
        );

        return RedisCacheManager.builder(factory)
            .cacheDefaults(defaultConfig)
            .withInitialCacheConfigurations(perCache)
            .transactionAware()  // cache ops participate in Spring txn
            .build();
    }
}
```

### 13.4 Cache pitfalls

1. **Caching mutable objects** — If cached object is modified, cache holds stale data. Return immutable copies or DTOs.
2. **Cache key collisions** — Default key is method params hash; use explicit `key` SpEL.
3. **N+1 with cache** — `@Cacheable` on `findById` caches one entity. `findAll` still hits DB. Consider caching at a higher level.
4. **Self-invocation** — `@Cacheable` is proxy-based. Calling cached method from same class bypasses cache.
5. **Null caching** — Cache `null` to prevent cache penetration, or disable to save memory (`cache-nulls`).
6. **Distributed cache consistency** — In cluster, evict on all nodes. Redis pub/sub or `spring.cache.cluster` mode.

### 13.5 Caffeine (in-memory) vs Redis

| | Caffeine | Redis |
|---|---|---|
| Type | Local (in-process) | Distributed |
| Speed | ~ns | ~ms (network) |
| Shared | No (per instance) | Yes |
| Size limit | JVM heap | Cluster memory |
| Eviction | LFU/LFU/W-TinyLFU | TTL/LRU |
| Use case | Single instance, low churn | Multi-instance, shared |

---

## 14. WebSocket Support

> **🟢 NICE TO HAVE**

### 14.1 WebSocket vs HTTP polling vs SSE

| Mechanism | Direction | Overhead | Use case |
|---|---|---|---|
| **HTTP Polling** | Client→Server (polls) | High (repeated requests) | Simple, compatibility |
| **Long Polling** | Client→Server (holds) | Medium | Fallback when WS blocked |
| **SSE (Server-Sent Events)** | Server→Client only | Low | One-way push (notifications, feeds) |
| **WebSocket** | Bidirectional | Low (full-duplex) | Real-time chat, trading, gaming |

### 14.2 Spring WebSocket + STOMP

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        config.enableSimpleBroker("/topic", "/queue");  // in-memory broker
        config.setApplicationDestinationPrefixes("/app");  // client→server prefix
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws").withSockJS();  // SockJS fallback for no-WS browsers
    }
}
```

```java
@Controller
public class ChatController {

    @MessageMapping("/chat.send")       // client sends to /app/chat.send
    @SendTo("/topic/messages")          // broadcast to all subscribers
    public ChatMessage send(ChatMessage message) {
        return message;
    }

    @MessageMapping("/chat.private.{userId}")
    @SendToUser("/queue/private")       // send to specific user
    public ChatMessage privateMsg(@DestinationVariable String userId, ChatMessage msg) {
        return msg;
    }
}
```

Client (JS):
```javascript
const socket = new SockJS('/ws');
const stompClient = Stomp.over(socket);
stompClient.connect({}, () => {
    stompClient.subscribe('/topic/messages', (msg) => {
        console.log(JSON.parse(msg.body));
    });
    stompClient.send('/app/chat.send', {}, JSON.stringify({text: 'Hello'}));
});
```

### 14.3 STOMP vs raw WebSocket

**🟢 NICE TO HAVE**

- **Raw WebSocket** — Just a TCP-like bidirectional byte stream. You design the protocol.
- **STOMP** — A simple text protocol on top of WebSocket (subprotocol). Adds pub/sub semantics, destinations, message types. Spring's `@MessageMapping` is built on STOMP.

Spring supports both. STOMP is preferred for pub/sub patterns (chat, broadcasts). Use raw WebSocket for custom binary protocols.

### 14.4 WebSocket security with JWT

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketSecurityConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureClientInboundChannel(ChannelRegistration registration) {
        registration.interceptors(new ChannelInterceptor() {
            @Override
            public Message<?> preSend(Message<?> message, MessageChannel channel) {
                StompHeaderAccessor accessor = MessageHeaderAccessor
                    .getAccessor(message, StompHeaderAccessor.class);
                if (StompCommand.CONNECT.equals(accessor.getCommand())) {
                    String token = accessor.getFirstNativeHeader("Authorization");
                    if (token == null || !jwtUtil.validate(token)) {
                        throw new AuthenticationException("Unauthorized") {};
                    }
                    accessor.setUser(jwtUtil.toPrincipal(token));
                }
                return message;
            }
        });
    }
}
```

### 14.5 Reactive WebSocket (WebFlux)

**🟢 NICE TO HAVE**

```java
@Configuration
@EnableWebFlux
public class ReactiveWebSocketConfig {

    @Bean
    public HandlerMapping webSocketHandlerMapping(WebSocketHandler handler) {
        Map<String, WebSocketHandler> map = new HashMap<>();
        map.put("/ws", handler);
        SimpleUrlHandlerMapping mapping = new SimpleUrlHandlerMapping();
        mapping.setOrder(-1);
        mapping.setUrlMap(map);
        return mapping;
    }

    @Bean
    public WebSocketHandler reactiveHandler() {
        return session -> {
            Flux<String> outbound = session.receive()
                .map(WebSocketMessage::getPayloadAsText)
                .map(msg -> "Echo: " + msg);
            return session.send(outbound.map(session::textMessage));
        };
    }
}
```

---

## Quick Reference: Most Asked Questions Summary

| # | Question | Category | Priority |
|---|---|---|---|
| 1 | Explain IoC and how Spring implements DI | IoC | 🔴 |
| 2 | Bean lifecycle and BeanPostProcessor | Lifecycle | 🔴 |
| 3 | Circular dependency & 3-level cache | IoC | 🔴 |
| 4 | JDK vs CGLIB proxy | AOP | 🔴 |
| 5 | AOP advice types + Around example | AOP | 🔴 |
| 6 | Self-invocation problem in `@Transactional` | Txn | 🔴 |
| 7 | Transaction propagation behaviors | Txn | 🔴 |
| 8 | N+1 problem and `@EntityGraph` | JPA | 🔴 |
| 9 | Auto-configuration mechanism | Boot | 🔴 |
| 10 | JWT flow in Spring Security | Security | 🔴 |
| 11 | Spring Security filter chain | Security | 🔴 |
| 12 | Circuit Breaker states (Resilience4j) | Cloud | 🟡 |
| 13 | Saga pattern (choreography vs orchestration) | Cloud | 🟡 |
| 14 | `@Cacheable` pitfalls | Caching | 🟡 |
| 15 | `@TransactionalEventListener` phases | Events | 🟡 |
| 16 | `@SpringBootTest` vs `@WebMvcTest` vs `@DataJpaTest` | Testing | 🔴 |

---

## Tips for BFSI / Product Company Interviews

1. **Emphasize transaction integrity** — BFSI cares about ACID, isolation levels, rollback scenarios. Be ready with isolation anomaly examples.
2. **Security is non-negotiable** — JWT, OAuth2, RBAC, password hashing, CSRF, OWASP top 10.
3. **Performance talk** — N+1, caching strategies, connection pooling (Hikari), query optimization.
4. **Microservices trade-offs** — Don't just list tools; explain why, when, and what breaks (distributed txns, eventual consistency, observability).
5. **Production readiness** — Actuator, metrics (Micrometer/Prometheus), health checks, graceful shutdown, externalized config.
6. **Testing discipline** — Slice tests, Testcontainers, `@MockBean` discipline. Product companies test well.
7. **"Tell me about a production issue"** — Prepare 2-3 real stories (LazyInitializationException, circular dependency, transaction rollback bug, cache stampede). Tie to concepts here.
8. **Don't over-engineer** — When asked design, start simple, then justify adding patterns. "It depends" is a valid answer when you explain the trade-offs.

---

*End of notes. Review one topic per day. Practice explaining aloud — interviews test articulation, not just recall.*
