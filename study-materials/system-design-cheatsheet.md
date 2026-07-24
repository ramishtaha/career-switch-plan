# 🎯 System Design Interview Cheat Sheet

> **For:** Ramish Taha — TCS System Engineer (Spring Boot/Java, BaNCS banking systems)
> **Target:** Product companies & BFSI GCCs @ 14–18 LPA
> **Edge:** Banking domain — Transaction Processing, Regulatory Reporting, Risk/Limits Enforcement

---

## 📑 Table of Contents

1. [Interview Framework (RESHADED)](#1-interview-framework-reshaded)
2. [Core Concepts](#2-core-concepts)
3. [Communication Patterns](#3-communication-patterns)
4. [Microservices Patterns](#4-microservices-patterns)
5. [Data Stores](#5-data-stores)
6. [Scalability](#6-scalability)
7. [Reliability](#7-reliability)
8. [Banking Domain System Design](#8-banking-domain-system-design)
9. [Quick-Reference Tables](#9-quick-reference-tables)
10. [Common Interview Questions](#10-common-interview-questions)

---

## 1. Interview Framework (RESHADED)

A structured approach to answering any system design question. Spend **45 min** as:
- Requirements (5 min) → Estimation (5 min) → High-level design (15 min) → Detailed design (15 min) → Deep dives (5 min)

```
R - Requirements       E - Estimation       S - Storage
H - High-level design  A - APIs              D - Data model
D - Detailed design    E - Edge cases       D - Deep dive
```

### Step-by-Step Breakdown

| Step | What You Do | Time | Key Output |
|------|-------------|------|-----------|
| **R** Requirements | Functional + Non-functional. Ask clarifying questions. Define scope. | 5 min | Bullet list of features + constraints (latency, throughput, availability, consistency) |
| **E** Estimation | Back-of-envelope: QPS, storage, bandwidth, compute | 5 min | Numbers for read/write QPS, storage/year, peak traffic |
| **S** Storage | Pick DB type, estimate capacity, partition strategy | 3 min | DB choice + schema sketch + shard key |
| **H** High-level | Draw boxes: clients → LB → services → DB → cache → queue | 5 min | Architecture diagram (whiteboard/ASCII) |
| **A** APIs | REST/gRPC endpoints, request/response schemas | 3 min | API contracts |
| **D** Data Model | Tables/collections, indexes, relationships | 4 min | Schema with PK/FK/indexes |
| **D** Detailed | Pick 2-3 components to go deep on (cache strategy, queue partition, etc.) | 10 min | Sequence/flow diagrams |
| **E** Edge Cases | Failures, race conditions, security, scaling limits | 5 min | Failure scenarios + mitigations |
| **D** Deep Dive | Bottlenecks, SPOFs, alternatives you'd consider | 5 min | Trade-off discussion |

### Functional vs Non-Functional Requirements

| Functional (What) | Non-Functional (How well) |
|---|---|
| User can shorten a URL | Available (99.9% uptime) |
| Short URL redirects to original | Low latency (<100ms redirect) |
| Custom aliases allowed | High read QPS (100:1 read:write) |
| Analytics on clicks | Durable (URLs don't get lost) |

### Estimation Cheat Numbers

| Metric | Rule of Thumb |
|--------|--------------|
| 1 day | ~100K seconds (86,400) |
| 1 year | ~30M seconds (31.5M) |
| 1 KB | 10³ bytes |
| 1 MB | 10⁶ bytes |
| 1 GB | 10⁹ bytes |
| 1 TB | 10¹² bytes |
| 1 PB | 10¹⁵ bytes |
| 1 billion | 10⁹ |
| Daily active user → QPS | DAU / 86,400 (then × peak factor 2-3x) |
| Storage/day | (writes/day) × (record size) |

### Interview Script

> *"Let me start by clarifying requirements — both functional and non-functional. I'll break this into what the system does, and how well it needs to do it. Then I'll do rough capacity estimates, sketch a high-level architecture, define the APIs and data model, and finally deep-dive into 2-3 critical components and edge cases."*

---

## 2. Core Concepts

### 2.1 Load Balancing

**What:** Distributes incoming traffic across multiple servers to prevent overload on any single server.

```
                    ┌──────────────┐
   Clients ────────►│ Load Balancer │
                    └──────┬───────┘
           ┌──────────┬────┴────┬──────────┐
           ▼          ▼         ▼          ▼
       ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
       │Srv 1 │  │Srv 2 │  │Srv 3 │  │Srv 4 │
       └──────┘  └──────┘  └──────┘  └──────┘
```

| Algorithm | How it works | When to use |
|-----------|-------------|-------------|
| **Round Robin** | Cycles through servers in order | Equal-capacity servers, simple needs |
| **Least Connections** | Picks server with fewest active connections | Long-lived connections (WebSocket, streaming) |
| **IP Hash** | Same client IP → same server | Session affinity needed (sticky sessions) |
| **Weighted Round Robin** | Round robin weighted by server capacity | Mixed-capacity servers |
| **Consistent Hashing** | Hash ring — only K/n keys remap on add/remove | Caching layers, DB sharding |
| **Least Response Time** | Picks server with lowest latency | Latency-sensitive apps |
| **Random** | Picks a random server | Simple, surprisingly effective at scale |

**L4 vs L7 Load Balancing:**

| Layer | Operates at | Sees | Example |
|-------|-------------|------|---------|
| **L4 (Transport)** | TCP/UDP | IP + port | HAProxy, AWS NLB — fast, can't route by path/header |
| **L7 (Application)** | HTTP/HTTPS | Headers, path, cookies | Nginx, AWS ALB, Envoy — can route by URL path |

**Key Trade-offs:**
- More layers of LB = more latency + more SPOFs (mitigate with redundancy)
- L7 is smarter but slower than L4; L4 can't do content-based routing
- Stateless backends allow any LB algorithm; stateful requires stickiness

> **Interview line:** *"I'd put an L7 LB (like Nginx/ALB) at the edge for path-based routing and TLS termination, then optionally L4 internally for TCP-level distribution across service instances. For the cache tier, I'd use consistent hashing to minimize key redistribution when nodes join/leave."*

---

### 2.2 Caching Strategies

**What:** Store frequently accessed data in a faster, closer storage layer to reduce latency and DB load.

```
Request → [Cache Hit?] → Yes → Return data
                     └→ No  → Fetch from DB → Write to Cache → Return
```

| Cache Pattern | How it works | When to use |
|---------------|-------------|-------------|
| **Cache-Aside (Lazy Loading)** | App checks cache, on miss reads DB and populates cache | General purpose, read-heavy workloads |
| **Write-Through** | Write to cache then synchronously to DB | Write-heavy, data must be consistent |
| **Write-Behind (Write-Back)** | Write to cache, async flush to DB | Write-heavy, tolerate brief inconsistency |
| **Write-Around** | Write directly to DB, cache only on read | Data rarely re-read after write |

**Eviction Policies:**

| Policy | What | When |
|--------|------|------|
| **LRU** | Evict Least Recently Used | General-purpose, temporal locality |
| **LFU** | Evict Least Frequently Used | Stable popularity distribution |
| **FIFO** | Evict oldest | Simple queue, scan-heavy |
| **TTL** | Evict after time-to-live | Data with known staleness tolerance |

**Cache-Aside vs Write-Through:**

```
Cache-Aside:                    Write-Through:
  Read: Cache → DB → Cache        Write: Cache + DB (sync)
  Write: DB only                   Read: Cache (always fresh)
  Risk: Stale on write             Risk: Write latency higher
```

**Cache Invalidation Challenges:**
- **Thundering Herd:** Cache miss → all requests hit DB → repopulate cache → stampede
  - *Fix:* Request coalescing, stale-while-revalidate, cache warming
- **Cache Penetration:** Queries for non-existent keys bypass cache every time
  - *Fix:* Cache null results with short TTL, Bloom filters
- **Cache Avalanche:** Many keys expire simultaneously → mass DB hits
  - *Fix:* Randomized TTL jitter
- **Hot Key:** Single key gets disproportionate traffic
  - *Fix:* Client-side caching, multiple cache replicas for that key

**Multi-Level Caching:**
```
Client → Browser Cache (seconds) → CDN (minutes)
  → App-local Cache (L1, e.g., Caffeine, ms) → Distributed Cache (L2, e.g., Redis, sub-ms)
  → Database (ms-min)
```

> **Interview line:** *"I'd use cache-aside with Redis for the hot path, with a 5-minute TTL and LRU eviction. To handle thundering herd, I'd add a short mutex lock per key on cache miss so only one request populates the cache. For hot keys, I'd shard the key or use a local L1 cache."*

---

### 2.3 Database Scaling — Sharding, Partitioning, Replication

#### Sharding (Horizontal Partitioning)

**What:** Split a large table across multiple DB instances (shards) by a shard key.

```
              ┌─────────────────┐
   Router ───►│ Shard Key: user_id│
              └────┬───┬───┬────┘
                   ▼   ▼   ▼
            ┌──────┐┌──────┐┌──────┐
            │Shard0││Shard1││Shard2│
            │ 0-33K││33-66K││66-99K│
            └──────┘└──────┘└──────┘
```

| Sharding Strategy | How | Pros / Cons |
|---|---|---|
| **Range-based** | Split by key ranges (e.g., dates, user_id ranges) | Easy range queries; can cause hotspots |
| **Hash-based** | hash(key) % N | Even distribution; resharding is hard |
| **Directory-based** | Lookup table maps key → shard | Flexible; lookup service is SPOF |
| **Consistent hashing** | Hash ring | Minimal remap on add/remove; ±balanced |

#### Partitioning (Within a Single DB)

| Type | What | Use Case |
|------|------|----------|
| **Horizontal (Partitioning)** | Split by rows (like sharding but within one DB) | Large tables, one DB instance |
| **Vertical (Partitioning)** | Split by columns (frequent vs rarely accessed columns) | Wide tables, optimize I/O |
| **Partition by range/list/hash** | DB-level partitioning (e.g., PostgreSQL declarative partitioning) | Time-series (range on date), multi-tenant (list on tenant_id) |

#### Replication

```
              ┌──────────┐
  Writes ────►│  Master   │────(replicate)──►  ┌──────────┐
              │  (Primary) │                    │  Replica  │──► Reads
              └──────────┘                    └──────────┘
```

| Type | What | Trade-off |
|------|------|-----------|
| **Master-Slave (Single-Leader)** | One primary for writes, N replicas for reads | Read scaling; single write bottleneck |
| **Master-Master (Multi-Leader)** | Multiple nodes accept writes | Write scaling; conflict resolution needed |
| **Single-Leader (e.g., Aurora)** | One writer, automated failover | Strong consistency; failover time |
| **Multi-Region** | Geo-replicated clusters | Lower latency globally; higher cost & complexity |

**Replication Lag & Consistency:**
- **Synchronous** (Strong): Replica acknowledges before master commits → no lag, higher write latency
- **Asynchronous** (Eventual): Master commits, replica catches up → low latency, stale reads possible
- **Semi-Synchronous**: At least one replica confirms → middle ground

> **Interview line:** *"I'd shard by user_id with consistent hashing so adding shards only remaps a fraction of keys. For reads, I'd add read replicas with async replication — accepting brief staleness for analytics reads, but routing transactional reads to the primary. For a banking context, writes would go to a single primary with synchronous replication to a standby for durability."*

---

### 2.4 CAP Theorem

**What:** In a distributed system, you can guarantee at most **2 of 3**:

```
        C (Consistency)
       / \
      /   \
     /     \
    /  CAP  \
   /         \
  A ----- P
(Availability) (Partition Tolerance)
```

| Guarantee | Meaning |
|-----------|---------|
| **Consistency** | All nodes see the same data at the same time |
| **Availability** | Every request gets a non-error response (may be stale) |
| **Partition Tolerance** | System continues despite network partitions (message loss/delay) |

**Since networks can partition, the real choice is CP vs AP:**

| Choice | What you sacrifice | Examples |
|--------|--------------------|----------|
| **CP** | Availability during partition — may reject requests | HBase, MongoDB (configurable), ZooKeeper, etcd, Spanner |
| **AP** | Consistency during partition — may return stale data | Cassandra, DynamoDB, CouchDB, Eureka |
| **CA** | Only if no partition possible — single-node systems | Traditional RDBMS (single instance) |

> **Interview line:** *"CAP says during a network partition you choose consistency or availability. For a payments ledger, I'd choose CP — refusing a transaction is better than double-spending. For a product catalog or recommendation service, AP with eventual consistency is fine."*

---

### 2.5 ACID vs BASE

| Property | ACID (Strong) | BASE (Eventual) |
|----------|---------------|-----------------|
| **Atomicity** | All or nothing | Partial ok, compensated later |
| **Consistency** | Always valid state | Eventually consistent |
| **Isolation** | Concurrent = serial | Weak isolation, conflicts resolved later |
| **Durability** | Committed = permanent | Committed eventually durable |
| **Latency** | Higher | Lower |
| **Scale** | Harder (vertical, sharding) | Easier (horizontal) |
| **Best for** | Financial transactions, ledgers | Catalogs, social feeds, analytics |
| **Examples** | PostgreSQL, Oracle, MySQL (InnoDB) | Cassandra, DynamoDB, MongoDB (tunable) |

> **Interview line:** *"For the core transaction ledger I'd insist on ACID — money movement can never be partially committed. For the analytics layer aggregating that data, BASE with eventual consistency is acceptable because stale-by-a-minute dashboards don't cause harm."*

---

### 2.6 Consistency Models

| Model | Guarantees | Use Case |
|-------|-----------|----------|
| **Strong / Linearizability** | All operations appear atomically in a global order | Ledger, locks, distributed locks |
| **Sequential** | Operations preserve program order; all nodes agree on order | Multi-object transactions |
| **Causal** | Causally related ops ordered; concurrent ops can be reordered | Comment threads, collaborative editing |
| **Eventual** | If no new writes, all replicas converge | Caching, feeds, search indexes |
| **Read-Your-Writes** | Client always sees their own writes | User profile updates |
| **Monotonic Read** | Once you see a value, you won't see an older one | Activity feeds, notifications |
| **Session** | Guarantees hold within a client session | Shopping cart, user sessions |

**PACELC Extension:** Even when there's **no partition (E)**, you trade **Latency (L)** vs **Consistency (C)**.
- Cassandra: PA/EL (always available, low latency)
- Spanner: CP/EC (always consistent, may add latency)

---

## 3. Communication Patterns

### 3.1 REST vs gRPC vs GraphQL

| Aspect | REST | gRPC | GraphQL |
|--------|------|------|---------|
| **Protocol** | HTTP/1.1 or HTTP/2 | HTTP/2 + Protobuf | HTTP + JSON |
| **Payload** | JSON/text | Protobuf (binary, compact) | JSON (client-defined shape) |
| **Streaming** | No (request-response) | Yes (bi-directional) | Subscriptions (WebSocket) |
| **Browser support** | Native | Needs gRPC-Web proxy | Native |
| **Schema** | OpenAPI (optional) | .proto (required, strict) | SDL (required, strict) |
| **Performance** | Moderate | High (binary + HTTP/2 multiplexing) | Moderate |
| **Best for** | Public APIs, CRUD, simplicity | Inter-service communication, low latency | Flexible client queries, mobile/BFF |
| **Trade-offs** | Over/under-fetching | Harder debugging (binary), not browser-native | N+1 query risk, complex server |

> **Interview line:** *"For external-facing APIs I'd use REST for simplicity and tooling. For internal service-to-service calls, gRPC for its compact binary encoding and HTTP/2 multiplexing. If clients have varying data needs (mobile vs web), a GraphQL BFF layer avoids over-fetching."*

---

### 3.2 Message Queues — Kafka vs RabbitMQ

| Aspect | Kafka | RabbitMQ |
|--------|-------|----------|
| **Model** | Pull-based, log (append-only) | Push-based, queue (delete on consume) |
| **Throughput** | Millions/sec | ~50K/sec |
| **Persistence** | All messages persisted (log) | Optional (memory or disk) |
| **Ordering** | Per-partition ordering | Per-queue (single consumer) |
| **Replay** | Yes — re-read by offset | No — message removed on ack |
| **Retention** | Time/size-based (days) | Until consumed + ack'd |
| **Fan-out** | Consumer groups | Exchanges (topic/fanout/direct) |
| **Best for** | Event streaming, log aggregation, CDC, high-throughput pipelines | Task queues, RPC, low-latency messaging |
| **Trade-offs** | Higher latency, complex ops, heavy | Lower throughput, no replay, simpler |

**Kafka Architecture:**
```
Producer → [Topic: Partitions] → Consumer Group
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
      Partition0  Part1   Partition2
      [msg][msg]  [msg]    [msg][msg]
          │         │         │
       Offset    Offset    Offset
```

- **Partition** = ordered, append-only log; parallelism unit
- **Consumer Group** = each consumer reads different partitions; enables horizontal scaling
- **Offset** = consumer's position; can reset/replay
- **Replication** = each partition replicated across brokers (leader + followers)

---

### 3.3 Pub-Sub vs Point-to-Point

```
Point-to-Point (Queue):           Pub-Sub (Topic):
  Producer → [Queue] → Consumer     Producer → [Topic] ─┬→ Subscriber A
  (one consumer gets message)                          ├→ Subscriber B
                                                       └→ Subscriber C
                                            (all get a copy)
```

| Pattern | Delivery | Example | When to use |
|---------|----------|---------|-------------|
| **Point-to-Point** | Exactly one consumer processes | RabbitMQ queue, SQS | Work distribution, task queue |
| **Pub-Sub** | All subscribers receive | Kafka topic, SNS | Event notification, fan-out, audit |

> **Interview line:** *"For a notification system, I'd use Kafka topics with multiple consumer groups — the email service, SMS service, and push service each subscribe independently to the same event. If I need exactly-once task processing, I'd use RabbitMQ with manual ack or Kafka with transactional producers."*

---

### 3.4 Event Sourcing

**What:** Store all state changes as an immutable sequence of events; current state = replay of events.

```
Event 1: AccountCreated   ──┐
Event 2: MoneyDeposited($100)├──► Current State: Balance = $150
Event 3: MoneyWithdrawn($50) ─┘
```

| Aspect | Pros | Cons |
|--------|------|------|
| **Audit** | Complete history, perfect audit trail | Event schema evolution is hard |
| **Debugging** | Replay to any point in time | Storage grows (needs snapshots) |
| **Decoupling** | Producers don't know consumers | Eventual consistency |
| **Projections** | Build any view from events | Multiple read models to maintain |

**When to use:** Banking ledgers (immutable transaction log), order systems, CQRS systems
**When NOT to use:** Simple CRUD, where current state is all you need

> **Interview line:** *"For a banking transaction ledger, event sourcing is natural — every money movement is an immutable event. The current balance is a projection (snapshot) built from the event log. This gives perfect auditability and lets me build multiple projections (daily statement, real-time balance) from the same events."*

---

### 3.5 CQRS (Command Query Responsibility Segregation)

**What:** Separate write model (commands) from read model (queries).

```
                     ┌──────────────┐
   Write Request ───►│ Command Side │──(events)──► Event Store
                     └──────────────┘                │
                                                     ▼
                                              ┌──────────────┐
   Read Request ────► Read Model ◄─────────────│ Projection   │
                      (optimized)              └──────────────┘
```

| When to use | When NOT to use |
|-------------|-----------------|
| Read/write ratio is very different | Simple CRUD (overkill) |
| Complex read queries needing different shapes | Small scale, simple domain |
| Multiple views needed from same data | When immediate consistency is required |
| Event sourcing companion | When team isn't ready for complexity |

> **Interview line:** *"I'd use CQRS for a regulatory reporting system — the write side records transactions through a command handler, and separate projections build optimized read models for different report types (daily risk, monthly compliance). This decouples write throughput from read query patterns."*

---

## 4. Microservices Patterns

### 4.1 Pattern Overview

```
Client ─► API Gateway ─► [Auth Service, User Service, Payment Service, Notification Service]
              │                        │
              ▼                        ▼
         Service Discovery      Message Broker (Kafka)
         (Consul/Eureka)              │
                                      ▼
                              Async Event Handlers
```

### 4.2 API Gateway

**What:** Single entry point for all clients; handles routing, auth, rate limiting, TLS, response aggregation.

| Responsibility | Example |
|----------------|---------|
| Routing | `/api/users/*` → User Service |
| Authentication | Validate JWT, inject user context |
| Rate Limiting | 1000 req/min per client |
| TLS Termination | Decrypt HTTPS at edge |
| Response Aggregation | Combine multiple service calls into one response (BFF pattern) |
| Protocol Translation | REST in → gRPC out |

**Trade-offs:** Adds latency (one more hop), SPOF (mitigate with redundancy), can become a bottleneck.

---

### 4.3 Service Discovery

| Type | How | Examples |
|------|-----|----------|
| **Client-side** | Client queries a registry for service instances | Netflix Eureka, Consul |
| **Server-side** | A router/proxy handles discovery | Kubernetes + kube-proxy, Envoy, Linkerd |
| **DNS-based** | Service name resolves to instance IP | Kubernetes DNS, CoreDNS |

```
Client ──► Service Registry ──► Returns [10.0.1.5:8080, 10.0.1.6:8080]
                                    │
                    Client picks one (client-side) or
                    router forwards (server-side)
```

> **Interview line:** *"In Kubernetes, I'd rely on built-in service discovery via Services + DNS + kube-proxy — no external registry needed. For non-K8s, Consul for health-checked service discovery with TTL-based registration."*

---

### 4.4 Circuit Breaker

**What:** Fail fast when a downstream service is unhealthy; prevents cascading failures.

```
    ┌─────────┐
    │ CLOSED  │──(failures > threshold)──►  ┌─────────┐
    │ normal  │                             │  OPEN   │
    │ traffic │◄──(half-open test passes)──│ (reject)│
    └─────────┘                             └────┬────┘
         ▲                                       │ (after timeout)
         │                                       ▼
         └────(test call succeeds)────  ┌─────────────┐
                                        │  HALF-OPEN  │
                                        │ (1 test req)│
                                        └─────────────┘
```

| State | Behavior |
|-------|----------|
| **Closed** | Requests flow normally; failures counted |
| **Open** | Requests fail immediately (fast-fail); no calls to downstream |
| **Half-Open** | Limited test requests pass through to check recovery |

**Implementation:** Resilience4j, Hystrix (legacy), Istio (mesh-level)

> **Interview line:** *"I'd use Resilience4j circuit breakers on calls to downstream services — if the risk service fails beyond a threshold, the breaker opens and I return a cached/default risk score or a degradation response instead of cascading the failure."*

---

### 4.5 Saga Pattern

**What:** Sequence of local transactions where each step publishes an event triggering the next; failures trigger compensating transactions (rollback).

| Type | How | Trade-off |
|------|-----|-----------|
| **Choreography** | Services emit/listen to events; no central coordinator | Simple, decentralized; hard to trace flow |
| **Orchestration** | A central orchestrator commands each step | Centralized control; orchestrator is complex |

```
Transfer Money Saga (Orchestration):

1. Debit Account A ──► (success) ──► 2. Credit Account B ──► (success) ──► DONE
        │                                     │
     (fail)                               (fail)
        ▼                                     ▼
   FAIL + rollback                     3. Compensate: Re-credit Account A
```

| When to use Saga | When NOT to use |
|---|---|
| Multi-service transaction with rollback needs | When you need true ACID across services |
| Long-running business processes | When compensations are impossible (e.g., sent email) |
| Distributed systems without 2PC | Low-latency, tightly coupled operations |

> **Interview line:** *"For a fund transfer spanning two account microservices, I'd use a choreography saga — debit emits 'MoneyDebited', credit service listens and credits, if credit fails it emits 'CreditFailed' and the debit service compensates by reversing. For complex multi-step flows, I'd use an orchestrator (like Camunda or Spring Statemachine) for visibility."*

---

### 4.6 Outbox Pattern

**What:** Atomically write to DB and publish an event by using the same DB transaction.

```
   Service Transaction:
     1. INSERT INTO orders (...)      -- business data
     2. INSERT INTO outbox (event)    -- event to publish
     3. COMMIT                        -- both succeed or both fail atomically

   Relay (CDC / Poller):
     1. Read unpublished events from outbox table
     2. Publish to Kafka
     3. Mark as published
```

**Solves:** Dual-write problem — writing to DB and publishing to Kafka are not atomic; if one fails, you get inconsistency.

| Approach | How | Trade-off |
|----------|-----|-----------|
| **Polling** | Background job reads outbox table, publishes, marks sent | Simple; adds DB load + latency |
| **CDC (Debezium)** | Reads DB WAL/binlog → publishes to Kafka | Low latency; requires DB plugin |
| **Transactional Outbox** | App writes to outbox in same txn as business data | Guarantees at-least-once delivery |

> **Interview line:** *"To solve the dual-write problem between my DB and Kafka, I'd use the transactional outbox pattern — write the event to an outbox table in the same transaction as my business data, then Debezium reads the binlog and publishes to Kafka. This guarantees no events are lost even if Kafka is briefly unavailable."*

---

### 4.7 BFF (Backend for Frontend)

**What:** A service tailored to one client type; aggregates multiple backend services into one optimized response.

```
Web BFF ──► (aggregates User + Orders + Recommendations for web UI)
Mobile BFF ──► (aggregates User + Orders for mobile, less data)
```

| When to use | Trade-off |
|-------------|-----------|
| Different clients need different data shapes | Additional service to maintain |
| Reduce client-side orchestration | Potential for BFF to become a "god service" |
| Mobile needs minimal payloads | One BFF per client type (not one per endpoint) |

---

### 4.8 API Composition / Aggregation

**What:** A single service calls multiple backend services and merges results for the client.

```
API Composition:
  Order Summary Service ──► Order Service (get orders)
                          ──► Customer Service (get customer details)
                          ──► Product Service (get product info)
                          └──► Merge into OrderSummary DTO
```

**Trade-offs:** Latency = sum of downstream calls (parallelize with `CompletableFuture`); availability = weakest link; can create coupling.

> **Interview line:** *"I'd use an API composition layer (BFF) for the order summary screen — it calls Order, Customer, and Product services in parallel, merges responses, and returns one payload. I'd use circuit breakers on each downstream call and return partial data if one service is down."*

---

## 5. Data Stores

### 5.1 Relational vs NoSQL

| Feature | Relational (SQL) | NoSQL |
|---------|-------------------|-------|
| **Schema** | Fixed, enforced | Flexible / dynamic |
| **Query** | SQL, joins, ACID | Varies (key-value, document, graph, column) |
| **Scaling** | Vertical (primarily), sharding (hard) | Horizontal (built-in) |
| **Consistency** | Strong (ACID) | Eventual (tunable) |
| **Best for** | Transactions, relationships, complex queries | Flexible schema, massive scale, specific access patterns |
| **Examples** | PostgreSQL, MySQL, Oracle | MongoDB, Cassandra, DynamoDB, Redis |

### 5.2 NoSQL Categories — When to Use What

| Type | Data Model | Best For | Examples |
|------|------------|----------|----------|
| **Key-Value** | `{key: value}` | Session, cache, config | Redis, DynamoDB, Memcached |
| **Document** | JSON-like nested docs | Content management, catalogs, flexible schema | MongoDB, Couchbase |
| **Column-Family** | Wide column, sorted by row key | Time-series, high-write, sparse data | Cassandra, HBase, ScyllaDB |
| **Graph** | Nodes + edges + properties | Social networks, fraud detection, recommendations | Neo4j, ArangoDB |

**Decision Framework:**

```
Do I need ACID transactions across multiple records?
├─ YES → Relational (PostgreSQL/MySQL)
└─ NO
   └─ What's the access pattern?
      ├─ Get/Set by key only → Key-Value (Redis)
      ├─ Nested, flexible documents → Document (MongoDB)
      ├─ High-write, time-series, wide rows → Column-Family (Cassandra)
      └─ Relationship traversal → Graph (Neo4j)
```

### 5.3 Time-Series Databases

| DB | Characteristics | Best For |
|----|----------------|----------|
| **InfluxDB** | Purpose-built TS, SQL-like query, retention policies | IoT, monitoring, market data ticks |
| **TimescaleDB** | PostgreSQL extension, SQL compatible, hypertables | If you already use PostgreSQL, financial tick data |
| **Prometheus** | Pull-based metrics, dimensional labels | Infrastructure monitoring, alerting |
| **ClickHouse** | Columnar, fast aggregations, high compression | Analytics on large datasets, real-time dashboards |

> **Interview line:** *"For storing market data ticks (price, volume per instrument per millisecond), I'd use a time-series DB like TimescaleDB — it handles high write throughput and time-range queries natively. For historical analytics on years of tick data, ClickHouse for its columnar compression and aggregation speed."*

### 5.4 Vector Databases

| DB | What | Best For |
|----|------|----------|
| **Pinecone** | Managed vector search, serverless | Semantic search, RAG embeddings |
| **Milvus** | Open-source, high-scale vector search | Large-scale similarity matching |
| **pgvector** | PostgreSQL extension | If already on PostgreSQL, smaller scale |
| **Weaviate** | Vector + graph hybrid | AI apps needing object + vector search |
| **Qdrant** | Rust-based, fast, filtering | Production semantic search with metadata filters |

**Use case:** Embeddings from LLMs, similarity search, recommendation engines, fraud pattern matching.

### 5.5 Choosing a Database — Decision Table

| Requirement | Primary Choice | Alternative |
|-------------|---------------|-------------|
| Financial transactions (ACID) | PostgreSQL / Oracle | MySQL (InnoDB) |
| Session store / cache | Redis | Memcached |
| User profiles (flexible schema) | MongoDB | PostgreSQL (JSONB) |
| Time-series market data | TimescaleDB / InfluxDB | Cassandra |
| High-write event log | Kafka (not a DB, but log) | Cassandra |
| Search / full-text | Elasticsearch / OpenSearch | PostgreSQL (FTS) |
| Graph (fraud detection) | Neo4j | ArangoDB |
| Analytics / OLAP | ClickHouse / Snowflake | BigQuery |
| Global low-latency KV | DynamoDB | Cassandra |

---

## 6. Scalability

### 6.1 Horizontal vs Vertical Scaling

| Aspect | Horizontal (Scale-Out) | Vertical (Scale-Up) |
|--------|----------------------|---------------------|
| How | Add more machines | Upgrade CPU/RAM on same machine |
| Limit | Theoretically unlimited | Hardware ceiling |
| Cost | Linear-ish; cheap commodity hardware | Expensive (premium hardware) |
| Failure | Single node failure = partial | Single node failure = total |
| Complexity | Network, consistency, distribution | Simple — just upgrade |
| State | Must be stateless or externalize state | Can be stateful |

### 6.2 Stateless Services

**What:** A service stores no client state between requests; any instance can handle any request.

```
Stateless:                    Stateful:
  Request → [any instance]      Request → [specific instance holding session]
  (LB can route anywhere)       (LB must use sticky sessions)
```

**Why it matters:** Enables horizontal scaling, rolling deployments, and auto-scaling without session affinity.

**How to achieve:** Externalize state to Redis (session), DB (user data), S3 (files). The service instance holds only in-memory caches (non-authoritative).

> **Interview line:** *"I'd make all services stateless — session state goes to Redis, any persistent data to the DB. This lets me auto-scale based on CPU and do rolling deploys without draining sessions. Only the cache tier needs affinity (consistent hashing)."*

---

### 6.3 CDN (Content Delivery Network)

```
User in Mumbai ──► CDN Edge (Mumbai) ──► (cache hit) ──► Return content
                                      └─► (cache miss) ──► Origin (US) ──► Cache + Return
```

| What CDN does | Benefit |
|---------------|---------|
| Caches static content at edge locations | Lower latency for users globally |
| Terminates TLS at edge | Offloads TLS from origin |
| Shields origin from traffic spikes | DDoS mitigation |
| Serves dynamic content via edge compute | Reduce origin load |

**When to use:** Static assets (images, CSS, JS), large-file downloads, streaming media, geographically distributed users.

---

### 6.4 Read Replicas

```
                    ┌──────────┐
  All Writes ──────►│  Primary  │
                    │           │────(async replicate)──► ┌──────────┐
                    └──────────┘                          │ Replica 1 │──► Read queries
                                                          └──────────┘
                                                          ┌──────────┐
                                               ┌─────────►│ Replica 2 │──► Analytics queries
                                               │          └──────────┘
                                          (sync)               │
                                               ┌──────────┐    │
                                               │ Standby   │◄───┘ (for failover)
                                               └──────────┘
```

| Pattern | Use |
|---------|-----|
| Read-replica for analytics | Offload heavy reads from primary |
| Read-replica in different region | Lower read latency globally |
| Synchronous replica as standby | Disaster recovery / failover |

**Trade-offs:** Replication lag → stale reads; write throughput still bounded by single primary.

---

### 6.5 Scalability Summary Table

| Problem | Solution |
|---------|----------|
| Too much read load | Read replicas + caching |
| Too much write load | Sharding + partitioning |
| Too much traffic | Load balancer + auto-scaling + CDN |
| Single point of failure | Redundancy at every layer |
| Data too large for one DB | Sharding + partitioning |
| Global latency | CDN + multi-region + geo-DNS |
| Hot key / hot shard | Consistent hashing + key splitting |

---

## 7. Reliability

### 7.1 Retries

| Strategy | How | When |
|----------|-----|------|
| **Fixed delay** | Retry after N ms | Simple, non-critical |
| **Exponential backoff** | Delay doubles each retry (100ms, 200ms, 400ms...) | Network calls, external APIs |
| **Exponential backoff + jitter** | Add randomness to avoid sync retry storms | Always — production systems |
| **Retry budget** | Max retries per request + circuit breaker | Prevent retry cascades |

> **Interview line:** *"I'd use exponential backoff with jitter and a max of 3 retries, combined with a circuit breaker so retries don't pile up against an already-failing downstream. For idempotency, I'd add a request ID so retries don't cause duplicate side effects."*

---

### 7.2 Idempotency

**What:** An operation can be called multiple times with the same result as calling it once.

```
Non-idempotent: POST /transfer (called twice = two transfers)
Idempotent:     POST /transfer (called twice = one transfer, deduplicated)
```

| Technique | How |
|-----------|-----|
| **Idempotency key** | Client sends unique key; server tracks processed keys |
| **Natural idempotency** | PUT (state set), DELETE (already gone = same) |
| **Database constraint** | Unique constraint on (idempotency_key, endpoint) |
| **Token-based** | Issue a token, client submits with token, server validates + invalidates |

**Critical for:** Payment APIs, fund transfers, order creation, any retry scenario.

> **Interview line:** *"For a payment API, I'd require an idempotency key header (UUID). The server stores (key, response) in a dedup table with a unique constraint — if a retry arrives with the same key, it returns the original response instead of re-processing. This is how Stripe's idempotency works."*

---

### 7.3 Dead Letter Queue (DLQ)

```
Producer → [Main Queue] → Consumer
                         │ (fails N times)
                         ▼
                    [Dead Letter Queue] → Alert + Manual/automated reprocessing
```

**What:** Messages that fail processing after N retries are moved to a separate queue for investigation.

| When to use | How |
|-------------|-----|
| Poison messages (always fail) | Max delivery attempts → DLQ |
| Transient failures exhausted | Retry + then DLQ |
| Need manual inspection | DLQ + alerting (PagerDuty, Slack) |

---

### 7.4 Circuit Breaker (see §4.4)

### 7.5 Rate Limiting

| Algorithm | How | Trade-off |
|-----------|-----|-----------|
| **Token Bucket** | Tokens refill at rate R; each request consumes a token | Allows bursts up to bucket size |
| **Leaky Bucket** | Requests enter bucket, leak out at fixed rate | Smooths traffic, no bursts |
| **Fixed Window** | Count requests per fixed time window | Edge bursts at window boundary |
| **Sliding Window** | Rolling window count | More accurate, more memory |
| **Sliding Window Counter** | Approximation using current + previous window | Memory-efficient, good accuracy |

**Where to rate limit:**
- API Gateway (global per-client limits)
- Application level (per-user, per-resource)
- Database level (connection pool limits)

> **Interview line:** *"I'd implement rate limiting at the API Gateway using a token bucket algorithm — it allows controlled bursts while enforcing an average rate. State (token counts) lives in Redis so limits are shared across all gateway instances. For per-user limits, I'd key by user_id + API path."*

---

### 7.6 Reliability Patterns Summary

| Goal | Pattern |
|------|---------|
| Prevent cascading failures | Circuit Breaker |
| Handle transient failures | Retry + exponential backoff + jitter |
| Prevent duplicate processing | Idempotency keys |
| Handle unprocessable messages | Dead Letter Queue |
| Protect downstream from overload | Rate limiting + load shedding |
| Ensure at-least-once delivery | Outbox pattern + Kafka acks |
| Graceful degradation | Fallback (cached/default response) |
| Detect failures | Health checks + heartbeat |

---

## 8. Banking Domain System Design

> **This is your edge.** BFSI GCCs and product companies in fintech deeply value banking domain knowledge. Connect generic patterns to real banking scenarios.

### 8.1 Transaction Processing System

#### Architecture

```
                          ┌──────────────────┐
   Client (Teller/Mobile)──►  API Gateway     │
                          │  (Auth, Rate      │
                          │   Limit, TLS)     │
                          └────────┬─────────┘
                                   │
                          ┌────────▼─────────┐
                          │ Transaction       │
                          │ Orchestrator      │
                          │ (Saga Coordinator)│
                          └────────┬─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
              ┌──────────┐  ┌──────────┐  ┌──────────┐
              │ Account  │  │ Ledger    │  │ Limits   │
              │ Service  │  │ Service   │  │ Service  │
              │ (ACID)   │  │ (Event    │  │ (Check &  │
              │          │  │  Source)  │  │  Reserve) │
              └──────────┘  └──────────┘  └──────────┘
                    │              │              │
                    └──────────────┴──────────────┘
                                   │
                          ┌────────▼─────────┐
                          │  Kafka (Events)  │
                          │  - TransactionEvent│
                          │  - AuditEvent     │
                          └──────────────────┘
```

#### Key Design Decisions

| Concern | Decision | Why |
|---------|----------|-----|
| **Consistency** | ACID for account balance | Money can never be partially moved |
| **Atomicity across services** | Saga pattern (orchestrated) | Debit + Credit must both succeed or both rollback |
| **Audit trail** | Event sourcing on ledger | Immutable, replayable, regulatory requirement |
| **Idempotency** | Idempotency key on transfer API | Retries don't cause double transfers |
| **Double-entry bookkeeping** | Two ledger entries per transaction (debit + credit) | Accounting integrity |
| **Concurrency** | Optimistic locking (version) or pessimistic locks on account | Prevent concurrent modifications to same account |
| **Durability** | Synchronous replication of primary | No committed transaction is lost |

#### Double-Entry Bookkeeping Flow

```
Transfer $100 from Account A → Account B:

Ledger Entry 1:  DEBIT   Account A   $100   (balance decreases)
Ledger Entry 2:  CREDIT  Account B   $100   (balance increases)
                  ─────────────────────────────
                  Net effect: balanced (zero-sum)
```

#### Saga Flow (Orchestrated)

```
1. Orchestrator: "Begin Transfer"
2. → Account Service: Debit A $100     (reserve + hold)
3. ← Success
4. → Account Service: Credit B $100
5. ← Success
6. → Ledger Service: Record entries (debit A, credit B)
7. ← Success
8. → Post "TransactionCompleted" event to Kafka
9. Done

FAILURE AT STEP 4:
4a. → Account Service: Compensate — Re-credit A $100
4b. → Post "TransactionFailed" event
4c. Alert
```

> **Interview line:** *"I'd implement money movement as an orchestrated saga — the orchestrator debits the source, credits the destination, and records double-entry ledger entries. Each step is idempotent via idempotency keys. If credit fails, a compensating transaction reverses the debit. The ledger is event-sourced for perfect auditability — critical for regulatory compliance."*

---

### 8.2 Regulatory Reporting System

#### Architecture

```
  Transaction ──► Kafka ──► ┌─────────────────┐
  Events                   │ Normalization    │
                           │ Service          │
                           └────────┬────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              ┌──────────┐    ┌──────────┐    ┌──────────┐
              │ RBI/     │    │ FATCA/   │    │ Internal │
              │ FEMA     │    │ CRS      │    │ Risk     │
              │ Report   │    │ Report   │    │ Report   │
              │ Builder  │    │ Builder  │    │ Builder  │
              └────┬─────┘    └────┬─────┘    └────┬─────┘
                   │               │               │
                   └───────────────┴───────────────┘
                                   │
                          ┌────────▼─────────┐
                          │ Report Store     │
                          │ (S3 + Metadata DB)│
                          └────────┬────────┘
                                   │
                          ┌────────▼─────────┐
                          │ Scheduler        │
                          │ (Daily/Monthly)  │
                          └────────┬────────┘
                                   │
                          ┌────────▼─────────┐
                          │ Submission Gateway│
                          │ (SFTP/API to Reg) │
                          └──────────────────┘
```

#### Key Design Decisions

| Concern | Decision | Why |
|---------|----------|-----|
| **Data source** | Kafka events from transaction system | Decoupled, replays, no direct DB coupling |
| **Transformation** | Dedicated normalization service | Different regulators need different formats (FEMA, FATCA, CRS) |
| **Storage** | S3 for report files + PostgreSQL for metadata | Cheap, durable; DB for queryable status |
| **Scheduling** | Cron/Quartz for periodic reports | Regulators have fixed deadlines |
| **Submission** | SFTP / API gateway to regulator | Depends on regulator interface |
| **Reconciliation** | Daily reconciliation job | Ensure reports match source transactions |
| **Lineage** | Event sourcing + audit log | Prove data provenance to auditors |
| **Accuracy** | Idempotent report generation | Regenerating a report yields identical output |

#### Report Generation Pipeline

```
1. Kafka consumer reads transaction events
2. Normalization service maps to canonical model:
   {txn_id, timestamp, amount, currency, counterparty, jurisdiction, type}
3. Report builders apply regulator-specific rules:
   - RBI/FEMA: cross-border transactions, FEMA classification
   - FATCA/CRS: US persons, reportable accounts
   - STR/AML: suspicious pattern flagging
4. Report stored (S3 + metadata DB)
5. Scheduler triggers submission at deadline
6. Submission gateway sends via SFTP/API
7. Acknowledgment stored for audit
```

> **Interview line:** *"Regulatory reporting is a CQRS pattern — the write side is the transaction system; the read side is a set of projections that build regulator-specific reports. I'd consume transaction events from Kafka, normalize them, and build projections for each regulator (RBI, FATCA, CRS). Reports are stored in S3 with metadata in PostgreSQL, submitted via SFTP on schedule, with full lineage back to source events for audit."*

---

### 8.3 Risk Limits Enforcement System

#### Architecture

```
                    ┌──────────────────────┐
   Trade Request ──►│  Pre-Trade Check      │
                    │  (Synchronous)        │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  Limits Service       │
                    │  ┌─────────────────┐ │
                    │  │ Limit Hierarchy  │ │
                    │  │ Trader → Desk →  │ │
                    │  │ Product → Bank   │ │
                    │  └─────────────────┘ │
                    │  ┌─────────────────┐ │
                    │  │ Limit Engine     │ │
                    │  │ (Check & Reserve)│ │
                    │  └────────┬────────┘ │
                    └───────────┼──────────┘
                                │
                    ┌───────────▼──────────┐
                    │  Redis (Real-time    │
                    │  Utilization Cache)  │
                    └───────────┬──────────┘
                                │
                    ┌───────────▼──────────┐
                    │  PostgreSQL           │
                    │  (Limit Definitions   │
                    │   + Utilization Log)  │
                    └──────────────────────┘
                                │
                    ┌───────────▼──────────┐
                    │  Kafka (Post-Trade    │
                    │  Events → Update      │
                    │  Utilization)         │
                    └──────────────────────┘
```

#### Limit Hierarchy

```
Bank-Level Limit (e.g., max exposure: $10B)
  └─ Product-Level Limit (e.g., Equities: $3B)
       └─ Desk-Level Limit (e.g., Equity Derivatives: $500M)
            └─ Trader-Level Limit (e.g., Trader A: $50M)
```

A trade must pass ALL levels in the hierarchy.

#### Key Design Decisions

| Concern | Decision | Why |
|---------|----------|-----|
| **Pre-trade check latency** | Redis for real-time utilization; <5ms | Must check before trade executes (synchronous path) |
| **Limit definitions** | PostgreSQL (source of truth) | Durable, queryable, audit-trail |
| **Utilization updates** | Kafka post-trade events → update Redis + DB | Async; don't block trade execution |
| **Consistency** | Read-through cache with short TTL on Redis | Near-real-time utilization; refresh from DB on miss |
| **Concurrency** | Atomic reservation via Redis EVAL script or DB row lock | Prevent over-utilization under concurrent trades |
| **Breach handling** | Soft limit → alert; Hard limit → reject trade | Regulatory requirement |
| **Reconciliation** | End-of-day: Redis utilization vs DB ledger | Catch drift between real-time and authoritative |

#### Pre-Trade Check Flow

```
1. Trade request arrives (trader_id, product, notional, counterparty)
2. Limits Service determines applicable limit hierarchy:
   Trader → Desk → Product → Bank
3. For each level, check: current_utilization + new_notional ≤ limit_threshold
4. If ALL pass:
   a. Reserve utilization (atomic increment in Redis)
   b. Approve trade
   c. Post "TradeExecuted" event to Kafka
5. If ANY fail:
   a. Reject trade with reason (which limit breached)
   b. Log breach event
6. Post-trade: Kafka consumer updates PostgreSQL utilization log
```

> **Interview line:** *"Risk limit enforcement is a two-phase pattern — a synchronous pre-trade check reads real-time utilization from Redis and atomically reserves capacity, then an async post-trade event updates the authoritative utilization in PostgreSQL. Limits are hierarchical (trader → desk → product → bank), and a trade must pass all levels. I'd reconcile Redis vs DB at end-of-day to catch drift, which is exactly the kind of reconciliation auditors expect."*

---

### 8.4 Market Data Streaming System

#### Architecture

```
  Exchange Feeds ──► ┌────────────────────┐
  (FIX/FAST)        │ Ingestion Service   │
                    │ (Protocol Adapter)  │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │ Kafka (per asset     │
                    │  class partitioning) │
                    └─────────┬──────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │ Real-time │    │ Historical│    │ Analytics │
        │ Fan-out   │    │ Store     │    │ Consumer  │
        │ (WebSocket│    │ (Time-    │    │ (Risk     │
        │  /gRPC   │    │  Series DB)│   │  calc, etc)│
        │  stream)  │    │           │    │           │
        └──────────┘    └──────────┘    └──────────┘
```

#### Key Design Decisions

| Concern | Decision | Why |
|---------|----------|-----|
| **Ingestion** | Protocol adapters (FIX → internal) | Exchanges have different protocols |
| **Transport** | Kafka with per-instrument partitioning | Ordered per instrument, high throughput |
| **Real-time delivery** | WebSocket / gRPC streaming to clients | Sub-second tick delivery |
| **Historical storage** | Time-series DB (TimescaleDB / InfluxDB) | Time-range queries, high write throughput |
| **Backpressure** | Kafka consumer lag monitoring | Slow consumers don't crash producers |
| **Fan-out** | Consumer groups per subscriber type | Each downstream gets its own offset/position |
| **Deduplication** | Sequence numbers per exchange feed | Network may redeliver ticks |

> **Interview line:** *"For market data streaming, I'd use protocol adapters to normalize exchange feeds into Kafka, partitioned by instrument symbol for ordering. Real-time consumers stream via WebSocket/gRPC; historical data lands in TimescaleDB. Consumer lag metrics alert me if a downstream falls behind. This is essentially the BaNCS Market Info pattern — ingest, normalize, fan-out."*

---

### 8.5 Banking-Specific NFRs to Always Mention

| NFR | Banking Requirement |
|-----|---------------------|
| **Auditability** | Every action traceable to a user + timestamp (immutable log) |
| **Compliance** | RBI/FEMA/FATCA/AML data residency and reporting |
| **Zero data loss** | At-least-once delivery + idempotency (effectively-once) |
| **Low latency** | Pre-trade checks < 5ms; ticks < 100ms |
| **High availability** | 99.99% for trading; 99.9% for back-office |
| **Security** | Encryption at rest + in transit, PII tokenization, role-based access |
| **Reconciliation** | End-of-day batch reconciliation between systems |
| **Disaster recovery** | Active-active or active-passive with RTO/RPO targets |

---

## 9. Quick-Reference Tables

### 9.1 Pattern → When to Use

| Pattern | Trigger / When to use |
|---------|---------------------|
| **Cache-Aside** | Read-heavy, can tolerate brief staleness |
| **Write-Through** | Write-heavy, need cache freshness |
| **Sharding** | Single DB can't handle write/storage load |
| **Read Replicas** | Read-heavy, write load is manageable |
| **CQRS** | Read/write patterns differ significantly |
| **Event Sourcing** | Need audit trail, replay, temporal queries |
| **Saga** | Multi-service transactions with rollback |
| **Outbox** | Dual-write problem (DB + message queue) |
| **Circuit Breaker** | Protect against cascading failures |
| **API Gateway** | Single entry, auth, routing, aggregation |
| **BFF** | Different clients need different data shapes |
| **Consistent Hashing** | Cache/shard with minimal redistribution |
| **DLQ** | Handle unprocessable messages |
| **Rate Limiting** | Protect downstream from overload |

### 9.2 Database → Scenario

| Scenario | Database | Why |
|----------|----------|-----|
| Transaction ledger | PostgreSQL | ACID, double-entry integrity |
| Session store | Redis | Sub-ms read/write, TTL |
| Market data ticks | TimescaleDB | Time-series optimized, high write |
| Trade event log | Kafka | Append-only, replay, ordering |
| Customer profiles | MongoDB | Flexible schema |
| Fraud graph | Neo4j | Relationship traversal |
| Regulatory reports | S3 + PostgreSQL | Files in S3, metadata in DB |
| Real-time limits | Redis | Atomic ops, low latency |
| Analytics dashboards | ClickHouse | Columnar, fast aggregations |

### 9.3 Queue → Use Case

| Need | Choose |
|------|--------|
| High throughput event streaming | Kafka |
| Task queue with ack/retry | RabbitMQ |
| Managed, simple queue | SQS |
| Ordered per-partition | Kafka (partition key) |
| Exactly-once (transactional) | Kafka transactions |
| Fan-out to many consumers | Kafka (consumer groups) / SNS |
| Dead letter handling | SQS DLQ, RabbitMQ DLX |
| Delayed/scheduled messages | RabbitMQ (TTL + DLX), SQS delay |

### 9.4 Consistency → Trade-off

| Consistency Level | Latency | Availability | Use Case |
|-------------------|---------|-------------|----------|
| Strong / Linearizable | Highest | Reduced | Ledger, locks, money movement |
| Eventual | Lowest | High | Caches, feeds, search index |
| Read-Your-Writes | Medium | Medium | User-facing writes |
| Causal | Medium | Medium | Collaboration, chat |
| Session | Medium | High | Shopping cart, sessions |

---

## 10. Common Interview Questions

### Warm-Up Questions

| Question | Key Points to Hit |
|----------|-------------------|
| **Design a URL Shortener** | Base62 encoding, KV store (Cassandra/Redis), cache, redirect 301 vs 302, analytics via async events, custom aliases collision, consistent hashing for shard |
| **Design a Rate Limiter** | Token bucket, Redis for distributed state, atomic Lua scripts, client-side vs server-side, fixed vs sliding window, 429 response + Retry-After header |
| **Design a Web Crawler** | URL frontier (priority queue), DNS cache, politeness (robots.txt + rate limit), BFS, dedup (Bloom filter), storage (KV), horizontal scaling, fault tolerance |
| **Design a Notification System** | Kafka topics, consumer groups per channel (email/SMS/push), template engine, rate limit per user, retry + DLQ, preference service, idempotency |
| **Design a Chat System** | WebSocket for real-time, message ordering (per-conversation sequence), offline messages (DB), presence (Redis), group chat fan-out, push notification fallback, end-to-end encryption |

### Product Company Favorites

| Question | Key Points |
|----------|-----------|
| **Design Twitter/X** | Fan-out on write (celebrity) vs read, timeline generation, tweet sharding, CDN for media, tweet search (inverted index) |
| **Design Instagram** | Object storage for images, CDN, pre-generated thumbnails, feed generation (timeline), async image processing pipeline |
| **Design Uber** | Geo indexing (geohash/s2), driver dispatch, real-time location tracking, surge pricing, Kafka for trip events |
| **Design Netflix** | CDN (Open Connect), adaptive bitrate streaming, pre-generation of formats, A/B testing infra, chaos engineering |
| **Design a Ticket Booking System** | Concurrency (seat locking), idempotency, payment integration, seat map sharding, overbooking strategy |

### BFSI / Banking Favorites

| Question | Key Points |
|----------|-----------|
| **Design a Payment Gateway** | Idempotency, PCI-DSS, tokenization, retry/backoff, multi-PSP failover, webhook handling, reconciliation |
| **Design a Core Banking Ledger** | Double-entry bookkeeping, event sourcing, ACID, append-only, immutable, balance as projection, audit trail |
| **Design a Fraud Detection System** | Real-time stream processing (Flink), rule engine + ML model, feature store, graph DB for relationship analysis, Kafka streams |
| **Design a Regulatory Reporting System** | CQRS projections, Kafka events, normalization, report builders, SFTP submission, reconciliation, lineage |
| **Design a Risk Limits System** | Pre-trade check (Redis), hierarchical limits, atomic reservation, post-trade event updates, EOD reconciliation |
| **Design a Trading Platform** | Order matching engine, FIX protocol, market data fan-out, pre-trade risk check, order book, WebSocket streaming |

---

## Appendix: ASCII Architecture Templates

### A. Generic Microservices Architecture

```
                              Internet
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   CDN / WAF / DDoS      │
                     └───────────┬───────────┘
                                 ▼
                     ┌───────────────────────┐
                     │   API Gateway / BFF    │
                     │   (Auth, Rate Limit)   │
                     └───────────┬───────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
        ┌──────────┐      ┌──────────┐      ┌──────────┐
        │ Service A │      │ Service B │      │ Service C │
        │ (x N)     │      │ (x N)     │      │ (x N)     │
        └─────┬────┘      └─────┬────┘      └─────┬────┘
              │                 │                 │
              ▼                 ▼                 ▼
        ┌──────────┐      ┌──────────┐      ┌──────────┐
        │  Redis    │      │ PostgreSQL│      │ Kafka    │
        │  (Cache)  │      │ (Primary) │      │ (Events) │
        └──────────┘      └─────┬────┘      └──────────┘
                                │
                        ┌───────┴───────┐
                        ▼               ▼
                  ┌──────────┐    ┌──────────┐
                  │ Replica  │    │ Replica  │
                  │ (Read)   │    │ (Standby)│
                  └──────────┘    └──────────┘
```

### B. Event-Driven Architecture

```
  Service A ──(event)──► Kafka Topic ──► Service B (consumer group 1)
                                   ──► Service C (consumer group 2)
                                   ──► Service D (consumer group 3)
                                   ──► DLQ (on failure)
```

### C. CQRS + Event Sourcing

```
  Command ──► Command Handler ──► Event Store (append)
                                   │
                                   ▼
                              Event Bus (Kafka)
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
              Projection A   Projection B   Projection C
              (Balance)       (Statement)    (Risk Exposure)
              ──► Read Model   ──► Read Model  ──► Read Model
```

### D. Sharding with Consistent Hashing

```
        0°                          360°
         ┌─────────────────────────────┐
         │    Consistent Hash Ring     │
         │                             │
   NodeA │        NodeB                │
    (0-120°)    (120-240°)             │
         │                             │
         │           NodeC  │          │
         │          (240-360°)│         │
         └─────────────────────────────┘

  Key hash → position on ring → clockwise → first node
  Adding Node D splits one range — only affected keys move
```

---

## Study Checklist

- [ ] Memorize RESHADED framework + estimation cheat numbers
- [ ] Be able to draw generic microservices architecture from memory
- [ ] Practice explaining each core concept in 1-2 sentences (interview line)
- [ ] For each of the 9 practice designs, write out: requirements, est, data model, 1 deep-dive
- [ ] Connect every generic pattern to a banking example (your edge)
- [ ] Know the trade-offs for: SQL vs NoSQL, REST vs gRPC, Kafka vs RabbitMQ, CP vs AP
- [ ] Practice whiteboard diagrams in ASCII (for remote interviews)
- [ ] Review idempotency, circuit breaker, saga, outbox — these come up constantly
- [ ] Prepare 2 banking deep-dives: transaction processing + risk limits enforcement
- [ ] Have questions ready for the interviewer about their architecture

---

> **Remember:** In a system design interview, the journey matters more than the destination. Communicate your thought process, justify trade-offs, and connect to real-world (banking) examples. Your BFSI domain knowledge is a differentiator — use it.
</content>