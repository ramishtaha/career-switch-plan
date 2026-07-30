# ⚠️ DEPRECATED — Replaced by ramish-12-week-plan-v2.md

> This is the V1 12-week plan (July 27 start, 171 DSA target, 6 concurrent focuses).
> It has been replaced by ramish-12-week-plan-v2.md (Aug 3 start, ~100 DSA, one primary focus per week).
> Kept for reference only. Do NOT follow this plan.
> See: ramish-12-week-plan-v2.md for the current plan.

---

# V1 12-Week Plan (ARCHIVED)
## From TCS 8.29 LPA → BFSI GCC / Product Co 16-22 LPA
### Start: Monday, July 27, 2026 | Target Interview: October 2026

---

## STRATEGY OVERVIEW

**Target roles:** Backend Java Engineer at BFSI GCCs (JPMorgan, Goldman Sachs, Morgan Stanley, HSBC, Wells Fargo, Deutsche Bank, BNY Mellon, Barclays) and large product companies with Mumbai/Bangalore/Pune presence

**Your moat:** Banking domain (BaNCS — RSM, Market Info, Limits). Most engineers don't understand capital markets, risk limits, regulatory reporting. You do. This is your edge over pure-tech candidates.

**Your gaps:** DSA fluency, system design depth, Kafka hands-on, AI integration skills, interview sharpness

**Daily structure:** 4-6 hours/day (evenings + weekends). More on weekends.

| Block | Focus | Hours |
|------|-------|-------|
| DSA Practice (Java) | NeetCode 150 → LeetCode mediums/hards | 2 hrs |
| Core Java + Spring Boot | Deep concepts + project building | 1.5 hrs |
| System Design / DevOps / AI | Rotates by week | 1 hr |
| Revision + daily LeetCode | Review notes, re-solve | 0.5 hr |

**Rules:**
1. Try each DSA problem for 20 min before looking at solution
2. Track every problem: name, approach, time, needed help?
3. Push code to GitHub daily
4. No zero days — even 1 problem counts
5. Never commit API keys — always use `.env` + `.gitignore`
6. Every Sunday: weekly review — what clicked, what didn't. Adjust.

---

## THE 12 WEEKS AT A GLANCE

| Week | DSA Focus | Java/Spring | System Design | DevOps/Cloud | AI Integration | Career |
|------|-----------|------------|---------------|-------------|----------------|-------|
| 1 | Arrays, Hashing, Two Pointers, Stack, Linked List | Project setup, 2 microservices, JPA, validation | — | Docker, Docker Compose, GitHub Actions CI | First LLM API call, /ai/generate endpoint | — |
| 2 | Sliding Window, Binary Search | Spring Security, Spring Cloud Gateway, Eureka, Resilience4j | Read: Grokking Intro + Scalability basics | Deploy to DigitalOcean, Docker networking | Configurable prompts, model comparison | Resume v1 draft |
| 3 | Trees (BST, traversals) | Kafka fundamentals + integrate into project | Design: URL Shortener | Kubernetes basics (minikube) | LangChain4j integration | Resume v2 (peer review) |
| 4 | Heaps / Priority Queue | Database depth: JPA optimization, indexing, query plans | Design: Rate Limiter | Kubernetes on cloud (Vultr/DO) | Vector DB basics (pgvector) | LinkedIn optimization |
| 5 | Graphs (BFS, DFS, topological sort) | Spring Boot internals: auto-config, bean lifecycle, AOP | Design: Chat System | GitHub Actions CD pipeline | RAG endpoint (retrieve + generate) | Start applying to referrals |
| 6 | Tries, Backtracking | Concurrency deep dive: threads, locks, CompletableFuture, virtual threads | Design: Notification System | Observability: Prometheus + Grafana | MCP server basics (optional) | Mock interview 1 (pramp.com) |
| 7 | Dynamic Programming (1D) | JVM internals: memory model, GC, classloading | Design: Transaction Processing System | Security: OWASP Top 10, JWT, OAuth2 | AI project feature complete | Mock interview 2 |
| 8 | Dynamic Programming (2D) | Microservices patterns: CQRS, Saga, outbox | Design: Market Data Streaming Platform | CI/CD: multi-env (dev/staging/prod) | Project polish + documentation | Mock interview 3 |
| 9 | LeetCode Medium speed run | Spring Boot revision + common interview questions | Design: Risk Limits Enforcement Service | Deployment: final production deploy | — | Mock interview 4 + resume final |
| 10 | LeetCode Hard selected | Core Java revision: collections, concurrency, JVM | Design: Regulatory Reporting Pipeline | — | — | Start active interviews |
| 11 | LeetCode contest simulation | Mock interview warmups | System design mock practice | — | — | Active interviews |
| 12 | Final revision + weak areas | Final revision + project demo prep | Final system design practice | Project deployed + documented | AI feature documented | Active interviews + offer negotiation |

---

## WEEK 1 (Jul 27 — Aug 2): Foundations + First Microservices Project
### Theme: Get the machine running. Build the skeleton you'll grow for 12 weeks.

**DSA:** Arrays & Hashing, Two Pointers, Stack, Linked List
**Java/Spring:** Project setup, JPA, validation, 2 microservices, API Gateway, Eureka, Circuit Breaker
**DevOps:** Docker, Docker Compose, GitHub Actions CI
**AI:** First LLM API call, /ai/generate endpoint
**Career:** —

### Day 1 — Mon Jul 27
- **DSA:** Arrays & Hashing — Contains Duplicate, Two Sum (try 20 min before solution)
- **Spring Boot:** Setup JDK 17, IntelliJ Community, Maven. Create project (start.spring.io). Simple REST API (Product entity). Push to GitHub.
- **DevOps:** Install Docker. Run `docker run hello-world`. Read Docker docs overview.
- **AI:** Explore serverless inference dashboards on Vultr, DigitalOcean, and Heroku. Note available models (GLM 5.2, etc.), API endpoints, and credit balances. Save API keys in a `.env` (gitignored).

### Day 2 — Tue Jul 28
- **DSA:** Valid Anagram, Group Anagrams, Top K Frequent Elements
- **Spring Boot:** Spring Data JPA + H2 in-memory DB. CRUD for Product. Exception handling (@ControllerAdvice).
- **DevOps:** Dockerize the Spring Boot app. Write Dockerfile. Build & run image.
- **AI:** Make your first inference API call — simple cURL/HTTP POST to a GLM 5.2 endpoint. Try a basic completion prompt. Log the request/response structure.

### Day 3 — Wed Jul 29
- **DSA:** Products of Array Except Self, Longest Consecutive Sequence
- **Spring Boot:** Validation (@Valid, @NotNull). Second entity: Category (One-to-Many with Product). Test with Postman.
- **DevOps:** Docker Compose: app + PostgreSQL. Learn docker-compose.yml basics.
- **AI:** Write a Java HTTP client (RestTemplate or WebClient) that calls the inference endpoint. Add a `productDescription` field that gets generated by the LLM from product name + category.

### Day 4 — Thu Jul 30
- **DSA:** Two Pointers — Valid Palindrome, Two Sum II, 3Sum
- **Spring Boot:** Split into 2 microservices (Product Service + Category Service). Inter-service call via RestTemplate.
- **DevOps:** Docker Compose with 2 services. Understand container networking.
- **AI:** Add an `/ai/generate-description` endpoint to the Product Service. Call the inference API from within the service. Handle errors/timeouts gracefully.

### Day 5 — Fri Jul 31
- **DSA:** Two Pointers — Container With Most Water, Trapping Rain Water
- **Spring Boot:** Spring Cloud Gateway as API Gateway. Route to both services.
- **DevOps:** GitHub Actions: basic CI pipeline (build + test on push).
- **AI:** Add a simple prompt template (system prompt + user prompt). Make the AI endpoint configurable via `application.yml` (model name, temperature, max tokens).

### Day 6 — Sat Aug 1
- **DSA:** Stack — Valid Parentheses, Min Stack, Evaluate Reverse Polish Notation
- **Spring Boot:** Eureka Service Discovery. Register both services.
- **DevOps:** Provision a DigitalOcean Droplet (or Vultr VM). SSH in, install Docker, pull your images. Understand VM networking (ports, firewalls).
- **AI:** Explore a second open-weights model available on your providers (beyond GLM 5.2). Test it side-by-side. Note latency + quality differences.

### Day 7 — Sun Aug 2
- **DSA:** Linked List — Reverse Linked List, Merge Two Sorted Lists, Linked List Cycle
- **Spring Boot:** Resilience4j Circuit Breaker on inter-service call.
- **DevOps:** Deploy Docker Compose setup to DigitalOcean Droplet. Verify the app is reachable via the Droplet's public IP.
- **AI:** Deploy the AI-enabled endpoint and verify it works end-to-end on the cloud VM. Document the architecture (which provider hosts what).
- **Revision:** Weekly review — what clicked, what didn't. Adjust plan.

### End of Week 1 — You Should Have
- [ ] ~15-18 DSA problems solved (Arrays, Hashing, Two Pointers, Stack, Linked List)
- [ ] 2-microservice Spring Boot project on GitHub
- [ ] Both services Dockerized, running via Docker Compose with Postgres
- [ ] API Gateway + Eureka + Circuit Breaker
- [ ] GitHub Actions CI pipeline
- [ ] App deployed to DigitalOcean (or Vultr) Droplet
- [ ] AI endpoint calling serverless inference (GLM 5.2) integrated into the Spring Boot project
- [ ] Documented cloud architecture: which provider hosts what (DO, Vultr, Heroku)

---

## WEEK 2 (Aug 3 — Aug 9): Spring Security + Sliding Window + First Deploy
### Theme: Production-grade Spring Boot. Start resume.

**DSA:** Sliding Window, Binary Search
**Java/Spring:** Spring Security, Spring Cloud Gateway deep dive, Spring profiles, Actuator
**System Design:** Start Grokking the System Design Interview — intro + scalability basics
**DevOps:** Production deploy to DigitalOcean, Docker networking deep dive
**AI:** Configurable prompts, multi-model comparison
**Career:** Resume v1 draft

### Day 8 — Mon Aug 3
- **DSA:** Sliding Window — Best Time to Buy and Sell Stock, Longest Substring Without Repeating Characters
- **Spring Boot:** Spring Security basics — JWT authentication. Secure your API endpoints.
- **System Design:** Read Grokking Intro. Take notes on: load balancing, caching, database sharding, CAP theorem.
- **AI:** Refactor AI endpoint into a dedicated AI Service class. Add retry logic and timeout handling.
- **Career:** Resume v1 — start with a blank doc. Write down everything you did at TCS. Don't edit, just brain-dump.

### Day 9 — Tue Aug 4
- **DSA:** Sliding Window — Longest Repeating Character Replacement, Permutation in String
- **Spring Boot:** Spring Security — role-based access control. Secure admin vs user endpoints.
- **System Design:** Read: Scalability basics (vertical vs horizontal scaling, stateless vs stateful).
- **AI:** Add prompt templates: system prompt + user prompt pattern. Store templates in a config file.
- **Career:** Resume v1 — structure: Summary, Experience, Skills, Education, Certifications. Use banking domain language (see Resume section below).

### Day 10 — Wed Aug 5
- **DSA:** Sliding Window — Minimum Window Substring, Fruit Into Baskets
- **Spring Boot:** Spring Actuator — health checks, info endpoint, metrics. Add custom health indicator.
- **System Design:** Read: Load balancers (L4 vs L7, algorithms, health checks).
- **AI:** Multi-model comparison endpoint — try the same prompt against 2 models, compare output quality and latency.
- **Career:** Resume v1 — write TCS experience bullets. Frame as: "Led microservices development for regulatory reporting module in core banking platform (TCS BaNCS). Handled market data ingestion and risk limit enforcement for [X] transactions/day."

### Day 11 — Thu Aug 6
- **DSA:** Binary Search — Binary Search, Search a 2D Matrix
- **Spring Boot:** Spring profiles (dev, staging, prod). Externalize config for different environments.
- **System Design:** Read: Caching (Redis, cache-aside, write-through, eviction policies).
- **AI:** Log all AI interactions (prompt, response, latency, model). Create a simple audit table in Postgres.
- **AI:** Resume v1 — skills section: Java, Spring Boot, Microservices, Docker, PostgreSQL, Kafka (learning), REST APIs, JWT. Don't list things you can't defend in an interview.

### Day 12 — Fri Aug 7
- **DSA:** Binary Search — Koko Eating Bananas, Search in Rotated Sorted Array
- **Spring Boot:** Spring Boot Test — write unit tests and integration tests. @SpringBootTest, @MockBean, @DataJpaTest.
- **System Design:** Read: Database scaling (sharding, replication, read replicas, write-ahead logs).
- **AI:** Add rate limiting to the AI endpoint (bucket4j or Spring Security rate limiter). LLM calls are expensive.
- **Career:** Resume v1 — complete first full draft. Don't polish yet. Just get everything on paper.

### Day 13 — Sat Aug 5
- **DSA:** Binary Search — Time-Based Key-Value Store, Median of Two Sorted Arrays
- **Spring Boot:** Spring Cloud Gateway — filters, rate limiting, request logging. Understand how gateway routes work.
- **DevOps:** Deploy full stack to DigitalOcean Droplet: 2 services + Postgres + Gateway. Test with public IP.
- **AI:** Test AI endpoint on the deployed server. Verify it works end-to-end remotely.
- **Career:** Review resume v1. Does it tell your story? Does it highlight banking domain?

### Day 7 — Sun Aug 9
- **DSA:** Weekly revision — re-solve 3 problems from this week without looking at notes.
- **Spring Boot:** Refactor — clean code, remove dead code, add comments.
- **Revision:** Weekly review.
- **Career:** Share resume v1 with 2-3 trusted peers or seniors for feedback. Send it.

### End of Week 2 — You Should Have
- [ ] ~12 more DSA problems (Sliding Window, Binary Search)
- [ ] Spring Security (JWT auth), Spring Actuator, Spring Profiles, Spring Boot Test
- [ ] System design notes: scalability, load balancing, caching, DB scaling
- [ ] App deployed to DigitalOcean with security
- [ ] Resume v1 complete and sent to peers for review

---

## WEEK 3 (Aug 10 — Aug 16): Trees + Kafka + First System Design
### Theme: Add the missing distributed systems skill (Kafka) and start system design practice.

**DSA:** Trees (BST, traversals, recursion patterns)
**Java/Spring:** Kafka fundamentals + integrate into project
**System Design:** Design: URL Shortener (full walkthrough)
**DevOps:** Kubernetes basics (minikube)
**AI:** LangChain4j integration
**Career:** Resume v2 based on peer feedback

### Day 15 — Mon Aug 10
- **DSA:** Trees — Invert Binary Tree, Maximum Depth of Binary Tree, Diameter of Binary Tree
- **Spring Boot:** Kafka fundamentals — what is Kafka, partitions, consumer groups, offsets. Set up local Kafka (Docker).
- **System Design:** Design a URL Shortener — capacity estimation, encoding (base62), collision handling, caching, redirect with 301 vs 302.
- **AI:** LangChain4j — add dependency. Replace raw HTTP calls with LangChain4j's model client. Note: cleaner API.
- **Career:** Resume v2 — incorporate peer feedback. Refine banking domain bullets. Add project section.

### Day 16 — Tue Aug 11
- **DSA:** Trees — Balanced Binary Tree, Same Tree, Subtree of Another Tree
- **Spring Boot:** Kafka producer — publish events when a Product is created/updated/deleted. Product Service as producer.
- **System Design:** URL Shortener — draw the architecture diagram. Practice explaining it aloud in 10 min.
- **DevOps:** Install minikube. Deploy a simple nginx pod. Understand pods, deployments, services.
- **Career:** Resume v2 — quantify everything: "Reduced manual effort by X%", "Handled X transactions/day", "Led migration of X module".

### Day 17 — Wed Aug 12
- **DSA:** Trees — Binary Search Tree — Search, Insert, Delete
- **Spring Boot:** Kafka consumer — Category Service consumes product events. Update category counts in real-time.
- **System Design:** Read: Message queues vs pub-sub. Kafka vs RabbitMQ. When to use which.
- **DevOps:** Kubernetes — ConfigMaps, Secrets, Services (ClusterIP, NodePort, LoadBalancer). Deploy your Spring Boot app as a K8s pod.
- **Career:** Resume v2 — complete. This is the version you'll apply with (can refine later).

### Day 18 — Thu Aug 13
- **DSA:** Trees — Kth Smallest Element in BST, Validate BST
- **Spring Boot:** Kafka — consumer groups, partition rebalancing. Run 2 consumers and see how partitions are assigned.
- **System Design:** Design a Rate Limiter — token bucket, sliding window, fixed window. Distributed rate limiting with Redis.
- **AI:** LangChain4j — add a chat memory feature. Remember conversation context across requests.
- **Career:** LinkedIn optimization — headline: "Backend Engineer | Java, Spring Boot, Microservices | Banking Domain (BaNCS) | Building AI-Enhanced Financial Systems". About section: tell your story.

### Day 19 — Fri Aug 14
- **DSA:** Trees — Construct Binary Tree from Preorder and Inorder, Level Order Traversal
- **Spring Boot:** Kafka — exactly-once semantics, idempotent producer, transactional consumer. Understand the trade-offs.
- **System Design:** Rate Limiter — draw architecture. Practice explaining aloud.
- **DevOps:** Kubernetes — Deployments, ReplicaSets, rolling updates. Scale your app to 3 replicas.
- **Career:** LinkedIn — add skills, add project, set to "Open to Work" (recruiters only). Connect with 10 recruiters at BFSI GCCs.

### Day 20 — Sat Aug 15
- **DSA:** Trees — Binary Tree Right Side View, Count Good Nodes
- **Spring Boot:** Kafka — schema registry. Avro serialization. Register a Product schema. Understand schema evolution.
- **System Design:** Review both designs (URL Shortener, Rate Limiter). Can you draw and explain each in 10 minutes?
- **AI:** LangChain4j — add document loading. Load a sample regulatory document and let the LLM answer questions about it.
- **Career:** Start reaching out to referrals — friends at JPMorgan, Goldman, Morgan Stanley, HSBC. Ask for referrals.

### Day 21 — Sun Aug 16
- **DSA:** Weekly revision — re-solve 3 tree problems without notes.
- **Spring Boot:** Kafka integration review — can you explain: producer config, consumer config, consumer groups, partition assignment?
- **Revision:** Weekly review.
- **Career:** Resume v2 finalized. LinkedIn updated.

### End of Week 3 — You Should Have
- [ ] ~12 DSA problems (Trees, BST)
- [ ] Kafka producer + consumer integrated into your Spring Boot project
- [ ] 2 system designs practiced (URL Shortener, Rate Limiter)
- [ ] Kubernetes basics (minikube, pods, deployments, services)
- [ ] LangChain4j integrated with chat memory
- [ ] Resume v2 + LinkedIn optimized
- [ ] Outreach to 10+ BFSI recruiters started

---

## WEEK 4 (Aug 17 — Aug 23): Heaps + Database Depth + Kubernetes on Cloud
### Theme: Fill the database and container orchestration gaps.

**DSA:** Heaps / Priority Queue
**Java/Spring:** Database depth — JPA optimization, indexing, query plans, N+1 problem
**System Design:** Design: Rate Limiter (continued) + Design: Web Crawler
**DevOps:** Kubernetes on cloud (Vultr or DigitalOcean Kubernetes)
**AI:** Vector DB basics (pgvector)
**Career:** Continue referral outreach

### Day 22 — Mon Aug 17
- **DSA:** Heaps — Kth Largest Element in a Stream, Last Stone Weight
- **Spring Boot:** Database — N+1 query problem. Identify it in your project. Fix with JOIN FETCH or @EntityGraph.
- **System Design:** Design a Web Crawler — BFS approach, URL frontier, deduplication, politeness, distributed crawling.
- **DevOps:** Provision a managed Kubernetes cluster (Vultr Kubernetes Engine or DigitalOcean Kubernetes). Understand nodes, node pools.
- **AI:** pgvector — add pgvector extension to your Postgres. Store embeddings for product descriptions.
- **Career:** Follow up with referrals. Send a reminder to people who haven't responded.

### Day 23 — Tue Aug 18
- **DSA:** Heaps — K Closest Points to Origin, Task Scheduler
- **Spring Boot:** Database — JPA/Hibernate query plan analysis. Use `hibernate.show_sql=true`. Read EXPLAIN ANALYZE output.
- **System Design:** Web Crawler — practice explaining. Focus on scalability, dedup, rate limiting.
- **DevOps:** Deploy your 2-service app to managed Kubernetes. Create deployments, services, configmaps, secrets.
- **AI:** pgvector — create an endpoint that does semantic search: "find products similar to X" using vector similarity.
- **Career:** Connect with 10 more BFSI GCC recruiters on LinkedIn.

### Day 24 — Wed Aug 19
- **DSA:** Heaps — Merge K Sorted Lists, Find Median from Data Stream
- **Spring Boot:** Database — indexing strategies. Add indexes to your Product/Category tables. Benchmark before/after.
- **System Design:** Design a Notification System — email/SMS/push, fan-out, prioritization, rate limiting, template engine.
- **DevOps:** Kubernetes — Horizontal Pod Autoscaler. Set CPU-based autoscaling. Load test with a simple script.
- **AI:** pgvector — compare semantic search results with keyword search. Note differences.
- **Career:** Apply to 5 BFSI GCC roles through referrals.

### Day 25 — Thu Aug 20
- **Development:** Database — connection pooling (HikariCP). Understand pool sizing, leak detection, timeout config.
- **System Design:** Notification System — draw architecture. Practice explaining.
- **DevOps:** Kubernetes — rolling updates. Deploy v2 of your app with zero downtime. Understand rollout/rollback.
- **AI:** Combine LangChain4j + pgvector — build a RAG (Retrieval Augmented Generation) endpoint. User asks a question → retrieve relevant products from pgvector → pass to LLM → return answer.
- **Career:** Apply to 5 more roles. Track in a spreadsheet: company, role, date, referral, status.

### Day 26 — Fri Aug 21
- **DSA:** Heaps revision — re-solve K Closest Points, Find Median without notes.
- **Spring Boot:** Database — transaction isolation levels. READ_COMMITTED vs SERIALIZABLE. Understand dirty reads, phantom reads.
- **System Design:** Review: Web Crawler + Notification System. Can you explain both in 10 min each?
- **DevOps:** Kubernetes — namespaces, resource limits, liveness/readiness probes. Add probes to your app.
- **AI:** RAG endpoint — add metadata filtering. "Find electronics products similar to X under ₹5000".
- **Career:** Review application tracker. Any responses? Follow up.

### Day 27 — Sat Aug 22
- **DSA:** Weekly revision — 5 heap problems re-solved without notes.
- **Spring Boot:** Database — write a migration script (Flyway or Liquibase). Version your schema changes.
- **DevOps:** Full review — can you explain: Docker vs Kubernetes, when to use each, how they complement?
- **AI:** RAG endpoint — add streaming response (SSE). Stream LLM output to client as it generates.
- **Career:** Connect with 5 more recruiters. Update application tracker.

### Day 28 — Sun Aug 23
- **DSA:** Weekly revision.
- **Spring Boot:** Database depth review — can you explain: N+1 problem, indexing, query plans, connection pooling, transaction isolation?
- **Revision:** Weekly review.
- **Career:** Application tracker review.

### End of Week 4 — You Should Have
- [ ] ~10 DSA problems (Heaps)
- [ ] Database depth: N+1 fixed, indexing, query plans, connection pooling, transactions, Flyway migrations
- [ ] 2 more system designs (Web Crawler, Notification System)
- [ ] Kubernetes on cloud (managed cluster, autoscaling, rolling updates, probes)
- [ ] pgvector + RAG endpoint (semantic search + retrieval augmented generation with streaming)
- [ ] 10+ BFSI GCC applications submitted via referrals

---

## WEEK 5 (Aug 24 — Aug 30): Graphs + Spring Internals + Chat System Design
### Theme: Spring Boot under the hood. Companies will ask how auto-configuration works.

**DSA:** Graphs (BFS, DFS, topological sort)
**Java/Spring:** Spring Boot internals: auto-configuration, bean lifecycle, AOP, conditional beans
**System Design:** Design: Chat System (WhatsApp/Slack-like)
**DevOps:** GitHub Actions CD pipeline (automated deploy on merge to main)
**AI:** RAG endpoint — add caching (cache common queries)
**Career:** Continue applying + first mock interview

### Day 29 — Mon Aug 24
- **DSA:** Graphs — Number of Islands, Max Area of Island
- **Spring Boot:** Spring Boot auto-configuration — how does `@SpringBootApplication` work? Trace the boot sequence. Read spring.factories / AutoConfiguration.imports.
- **System Design:** Design a Chat System — WebSocket vs long polling, message format, delivery guarantees (at-least-once vs at-most-once), group chat vs DM.
- **DevOps:** GitHub Actions CD — auto-deploy to Kubernetes on merge to main branch. Build image → push to registry → kubectl apply.
- **AI:** RAG endpoint — cache common queries. Use Spring Cache with Redis. Same question → cached answer (no LLM call needed).
- **Career:** Apply to 5 more roles. Check referral responses.

### Day 30 — Tue Aug 25
- **DSA:** Graphs — Clone Graph, Course Schedule (topological sort)
- **Spring Boot:** Bean lifecycle — BeanFactoryPostProcessor, BeanPostProcessor, InitializingBean, @PostConstruct, @PreDestroy. Understand the full lifecycle.
- **System Design:** Chat System — message storage (Cassandra for write-heavy, time-series), read receipts, online presence.
- **DevOps:** Test the CD pipeline — make a small change, push to main, verify it auto-deploys.
- **AI:** RAG — add conversation history. Remember the last 5 questions. Use LangChain4j's chat memory.
- **Career:** Mock interview 1 — pramp.com (DSA only, 30 min). Get a baseline.

### Day 31 — Wed Aug 26
- **DSA:** Graphs — Pacific Atlantic Water Flow, Course Schedule II
- **Spring Boot:** AOP (Aspect-Oriented Programming) — @Before, @After, @Around aspects. Write a logging aspect that logs all service method calls.
- **System Design:** Chat System — draw architecture. Practice explaining in 10 min.
- **DevOps:** GitHub Actions — add Slack/Discord notification on successful deploy.
- **AI:** RAG — add fallback: if LLM is unavailable, return cached/similar results from pgvector.
- **Career:** Review mock interview 1. What went wrong? What to improve?

### Day 32 — Thu Aug 27
- **DSA:** Graphs — Number of Connected Components, Graph Valid Tree
- **Spring Boot:** Conditional beans — @ConditionalOnProperty, @ConditionalOnBean, @ConditionalOnMissingBean. Understand how Spring decides what to create.
- **System Design:** Read: WebSockets deep dive. Understand the protocol, connection lifecycle, scaling WebSockets (sticky sessions, Redis pub/sub).
- **DevOps:** Add automated tests to CI pipeline. Block merge if tests fail.
- **AI:** RAG — evaluate the AI feature. Write 10 test queries. Rate the responses. Note what's good and what needs improvement.
- **Career:** Mock interview 2 — pramp.com (DSA, 30 min). Track improvement.

### Day 33 — Fri Aug 28
- **DSA:** Graphs — Redundant Connection, Accounts Merge (Union Find)
- **Spring Boot:** Spring Boot revision — can you explain: auto-configuration, bean lifecycle, AOP, conditional beans? If not, go back and review.
- **System Design:** Chat System — final review. Can you design and explain in 15 min?
- **DevOps:** Review the full CI/CD pipeline. Can you draw it on a whiteboard and explain each step?
- **AI:** RAG endpoint polish. Add input validation, error handling, rate limiting, logging, caching.
- **Career:** Apply to 5 more roles. Follow up on pending referrals.

### Day 34 — Sat Aug 29
- **DSA:** Weekly revision — 5 graph problems re-solved.
- **Spring Boot:** Write a one-page cheat sheet: Spring Boot internals. Auto-config, bean lifecycle, AOP, conditions, profiles, actuator.
- **System Design:** Review all 4 system designs so far (URL Shortener, Rate Limiter, Web Crawler, Notification System, Chat). Can you explain any one in 10 min?
- **AI:** Document the AI architecture. Write a README for the AI feature. Architecture diagram + explanation.
- **Career:** Connect with 5 more recruiters. Update application tracker.

### Day 35 — Sun Aug 30
- **DSA:** Weekly revision.
- **Spring Boot:** Revision.
- **Revision:** Weekly review.
- **Career:** Review mock interviews 1 & 2. Identify patterns in mistakes.

### End of Week 5 — You Should Have
- [ ] ~12 DSA problems (Graphs, Union Find)
- [ ] Spring Boot internals understood (auto-config, bean lifecycle, AOP, conditional beans)
- [ ] Chat System design practiced
- [ ] Full CI/CD pipeline: push to main → test → build → deploy to Kubernetes
- [ ] RAG endpoint with caching, conversation history, fallback, streaming
- [ ] 2 mock interviews done (baseline established)
- [ ] 20+ BFSI GCC applications submitted

---

## WEEK 6 (Aug 31 — Sep 6): Tries + Concurrency + Transaction Processing Design
### Theme: Java concurrency is a core interview topic. Master it.

**DSA:** Tries, Backtracking
**Java/Spring:** Concurrency deep dive: threads, locks, CompletableFuture, virtual threads
**System Design:** Design: Transaction Processing System (banking domain!)
**DevOps:** Observability: Prometheus + Grafana
**AI:** MCP server basics (optional/stretch)
**Career:** Mock interview 3

### Day 36 — Mon Aug 31
- **DSA:** Tries — Implement Trie, Search Suggestions System
- **Spring Boot:** Concurrency — Thread creation, Runnable, Callable, Future. Thread pools (FixedThreadPool, CachedThreadPool). Understand when to use which.
- **System Design:** Design a Transaction Processing System — ACID properties, two-phase commit, idempotency, retry logic, deadletter queue.
- **System Design:** Read: Distributed transactions — Saga pattern, outbox pattern. When to use each.
- **DevOps:** Install Prometheus + Grafana (Docker). Scrape your Spring Boot Actuator metrics.
- **Career:** Mock interview 3 — pramp.com (DSA, 30 min).

### Day 378 — Tue Sep 1
- **DSA:** Tries — Design In-Memory File System, Word Search II
- **Spring Boot:** Concurrency — synchronized, volatile, ReentrantLock, ReadWriteLock. Understand the differences. When to use volatile vs synchronized.
- **System Design:** Transaction Processing — draw architecture. This is YOUR domain. Use BaNCS experience: "In BaNCS, transactions flow through..."
- **DevOps:** Grafana — create a dashboard for your app: CPU, memory, request rate, error rate.
- **Career:** Review mock interview 3. Track progress from mock 1.

### Day 38 — Wed Sep 2
- **DSA:** Backtracking — Subsets, Combination Sum
- **Spring Boot:** Concurrency — CompletableFuture. Chain async operations. Exception handling in async code.
- **System Design:** Transaction Processing — practice explaining. Focus on: idempotency, retry, deadletter queue, exactly-once processing.
- **DevOps:** Prometheus — add custom metrics to your app (counter for AI requests, gauge for active sessions).
- **Career:** Apply to 5 more roles. Focus on companies where you have referrals.

### Day 39 — Thu Sep 3
- **DSA:** Backtracking — Permutations, Word Search
- **Spring Boot:** Concurrency — Virtual Threads (Java 21). Understand Project Loom. Compare platform threads vs virtual threads. When to use each.
- **System Design:** Read: Event sourcing and CQRS. Understand the pattern. When does it apply to banking systems?
- **DevOps:** Alerting — set up a Grafana alert: if error rate > 5%, trigger an alert.
- **Career:** Reach out to 5 more people at target companies for referrals.

### Day 40 — Fri Sep 4
- **DSA:** Backtracking — N-Queens, Sudoku Solver
- **Spring Boot:** Concurrency — ExecutorService vs ForkJoinPool. Parallel streams. Understand when parallel streams help and when they hurt.
- **System Design:** Transaction Processing — final review. Can you design and explain in 15 min? Use your banking domain vocabulary.
- **DevOps:** Review observability stack. Can you explain: metrics vs logs vs traces? When to use each?
- **Career:** Mock interview 4 — pramp.com (System Design, 45 min). First system design mock.

### Day 41 — Sat Sep 5
- **Claude Cert:** If TCS gives it free and you can study during work hours → register for Claude Certified Developer - Foundations. Do the free prep courses on Partner Academy.
- **DSA:** Weekly revision — 5 problems (Tries + Backtracking) re-solved.
- **Spring Boot:** Concurrency cheat sheet — threads, locks, CompletableFuture, virtual threads, thread pools.
- **AI:** Optional stretch: Build a simple MCP server that exposes your Product data to Claude. (If too ambitious, skip — but try.)
- **Career:** Review all 4 mock interviews. What are your weak areas?

### Day 42 — Sun Sep 6
- **DSA:** Weekly revision.
- **Spring Boot:** Revision.
- **Revision:** Weekly review. You're at the halfway point. How do you feel? What needs adjustment?
- **Career:** Half-point review: How many applications? How many responses? Any interviews scheduled?

### End of Week 6 — You Should Have
- [ ] ~10 DSA problems (Tries, Backtracking)
- [ ] Java concurrency mastered (threads, locks, CompletableFuture, virtual threads)
- [ ] Transaction Processing System design practiced (banking domain framing!)
- [ ] Observability stack (Prometheus + Grafana + custom metrics + alerting)
- [ ] 4 mock interviews done (2 DSA, 1 system design, 1 mixed)
- [ ] Claude Developer cert prep started (if TCS offers free)

---

## WEEK 7 (Sep 7 — Sep 13): Dynamic Programming + JVM Internals + Market Data Design
### Theme: DP is the hardest DSA topic. Start early, practice daily.

**DSA:** Dynamic Programming (1D)
**Java/Spring:** JVM internals: memory model, GC, classloading
**System Design:** Design: Market Data Streaming Platform (banking domain!)
**DevOps:** Security: OWASP Top 10, JWT deep dive, OAuth2
**AI:** AI feature complete and documented
**Career:** Mock interview 5

### Day 43 — Mon Sep 7
- **DSA:** DP — Climbing Stairs, Min Cost Climbing Stairs, House Robber
- **Spring Boot:** JVM — Memory model: heap, stack, method area, metaspace. Draw the JVM memory diagram.
- **System Design:** Design a Market Data Streaming Platform — Kafka for ingestion, real-time processing, multiple subscribers (trading desk, risk, compliance).
- **DevOps:** Security — OWASP Top 10 overview. Which ones apply to your app? (Injection, broken auth, security misconfiguration).
- **AI:** AI feature complete. Write comprehensive README. Architecture diagram + data flow + security notes.
- **Career:** Mock interview 5 — DSA, 30 min.

### Day 44 — Tue Sep 8
- **DSA:** DP — House Robber II, Longest Palindromic Substring
- **Spring Boot:** JVM — Garbage Collection: G1GC, ZGC, Serial GC. Understand generational hypothesis. How to choose a GC for your app.
- **System Design:** Market Data Platform — draw architecture. Use your BaNCS Market Info experience: "In BaNCS, market data flows through..."
- **DevOps:** Security — JWT deep dive. How does JWT work? Signature, expiration, refresh tokens. Implement refresh token rotation.
- **Career:** Review mock interview 5. Track progress.

### Day 45 — Wed Sep 9
- **DSA:** DP — Word Break, Coin Change
- **Spring Boot:** JVM — Classloading: bootstrap classloader, platform classloader, application classloader. Understand classloader hierarchy. What is NoClassDefFoundError vs ClassNotFoundException?
- **System Design:** Market Data Platform — practice explaining. Focus on: throughput, low latency, multiple subscriber patterns, backpressure.
- **DevOps:** Security — OAuth2. Implement OAuth2 login in your app (Google or GitHub). Understand the flow.
- **Career:** Apply to 5 more roles. You should have 30+ applications by now.

### Day 46 — Thu Sep 10
- **DSA:** DP — Longest Increasing Subsequence, Best Time to Buy and Sell Stock with Cooldown
- **Spring Boot:** JVM — Memory leaks. How to detect them. Heap dump analysis. Use VisualVM or JConsole.
- **System Design:** Read: Time-series databases (InfluxDB, TimescaleDB). When to use for market data vs Kafka + Postgres.
- **DevOps:** Security — audit your app. Run OWASP ZAP against your deployed app. Fix any findings.
- **Career:** Mock interview 6 — System Design, 45 min.

### Day 47 — Fri Sep 11
- **Backend:** DP — Longest Common Subsequence, Decode Ways
- **Spring Boot:** JVM — Thread dump analysis. How to find deadlocks, thread starvation. Use jstack.
- **System Design:** Market Data Platform — final review. Can you design and explain in 15 min with banking vocabulary?
- **DevOps:** Security review — can you explain: JWT, OAuth2, OWASP Top 10, HTTPS, CORS?
- **Career:** Review mock interview 6. Are your system design answers improving?

### Day 48 — Sat Sep 12
- **DSA:** Weekly revision — 5 DP problems re-solved. DP takes repetition. Do them again.
- **Spring Boot:** JVM cheat sheet — memory model, GC, classloading, diagnostics (heap dump, thread dump, jstack, VisualVM).
- **System Design:** Review all designs so far. Can you pick any one and explain in 10-15 min?
- **AI:** Final AI feature review. Is it production-quality? Error handling, rate limiting, caching, streaming, fallback.
- **Career:** Connect with 5 more recruiters. Follow up on all pending applications.

### Day 49 — Sun Sep 13
- **DSA:** Weekly revision.
- **Spring Boot:** Revision.
- **Revision:** Weekly review.
- **Career:** Application tracker review. Any interviews scheduled?

### End of Week 7 — You Should Have
- [ ] ~10 DSA problems (DP 1D)
- [ ] JVM internals (memory model, GC, classloading, diagnostics)
- [ ] Market Data Streaming Platform design (banking domain framing!)
- [ ] Security (OWASP Top 10, JWT, OAuth2, ZAP audit)
- [ ] AI feature complete and documented
- [ ] 6 mock interviews done

---

## WEEK 8 (Sep 14 — Sep 20): DP 2D + Microservices Patterns + Regulatory Reporting Design
### Theme: Advanced microservices patterns. Design a system from your actual work experience.

**DSA:** Dynamic Programming (2D)
**Java/Spring:** Microservices patterns: CQRS, Saga, outbox, API composition
**System Design:** Design: Regulatory Reporting Pipeline (YOUR domain!)
**DevOps:** CI/CD: multi-environment pipeline (dev → staging → prod)
**AI:** —
**Career:** Mock interview 7

### Day 50 — Mon Sep 14
- **DSA:** DP 2D — Unique Paths, Longest Common Subsequence (revisit as 2D), Triangle
- **Spring Boot:** Microservices — CQRS (Command Query Responsibility Segregation). Understand the pattern. When does it apply?
- **System Design:** Design a Regulatory Reporting Pipeline — data ingestion from multiple sources, transformation, validation, report generation, submission to regulators.
- **DevOps:** CI/CD — multi-environment pipeline. Dev → Staging → Prod. Approval gates between environments.
- **Career:** Mock interview 7 — DSA, 30 min.

### Day 51 — Tue Sep 15
- **DSA:** DP 2D — Longest Palindromic Subsequence, Interleaving String
- **Spring Boot:** Microservices — Saga pattern (choreography vs orchestration). Distributed transactions across microservices. Understand the trade-offs.
- **System Design:** Regulatory Reporting — draw architecture. Use your BaNCS RSM experience: "In BaNCS RSM, regulatory data flows through..."
- **DevOps:** CI/CD — add automated security scan (Trivy or Snyk) to pipeline. Scan Docker images for vulnerabilities.
- **Career:** Review mock interview 7.

### Day 52 — Wed Sep 16
- **DSA:** DP 2D — Edit Distance, Distinct Subsequences
- **Spring Boot:** Microservices — Outbox pattern. Reliable event publishing. Why not just publish to Kafka directly? Understand the dual-write problem.
- **System Design:** Regulatory Reporting — practice explaining. Focus on: data quality, validation rules, regulatory deadlines, audit trail.
- **DevOps:** CI/CD — add automated DAST scan (OWASP ZAP) to staging deploy.
- **Career:** Apply to 5 more roles. Target: JPMorgan, Goldman, Morgan Stanley, HSBC, Barclays specifically.

### Day 53 — Thu Sep 17
- **DSA:** DP 2D — Burst Balloons, Regular Expression Matching
- **Spring Boot:** Microservices — API composition / API gateway pattern. How to aggregate data from multiple services. Backend-for-Frontend (BFF) pattern.
- **System Design:** Read: Data partitioning strategies. How to partition regulatory data by region, entity, time period.
- **DevOps:** Review CI/CD pipeline. Can you draw it and explain: build → test → security scan → deploy dev → deploy staging → approval → deploy prod?
- **CI/CD:** Review pipeline. Can you explain each step to an interviewer?
- **Career:** Mock interview 8 — System Design, 45 min.

### Day 8 — Fri Sep 18
- **DSA:** DP 2D — Stone Game, Minimum Path Sum
- **Spring Boot:** Microservices revision — can you explain: CQRS, Saga, Outbox, API composition? When to use each? What are the trade-offs?
- **System Design:** Regulatory Reporting — final review. This is your strongest design. You LIVED this system. Explain it with confidence.
- **DevOps:** Final CI/CD review.
- **Career:** Review mock interview 8. Track improvement across all 8 mocks.

### Day 55 — Sat Sep 19
- **DSA:** Weekly revision — 5 DP 2D problems re-solved. These are hard. Repetition is key.
- **Spring Boot:** Microservices cheat sheet — CQRS, Saga, Outbox, API composition, BFF. One page.
- **System Design:** Review all designs. You should have 8 designs now. Pick 3 you're most confident on. Those are your go-to in interviews.
- **DevOps:** Project final review. Is everything deployed? CI/CD working? Observability up?
- **Career:** Review all applications. Follow up on everything. Any interviews scheduled?

### Day 56 — Sun Sep 20
- OA:** Weekly revision.
- **Spring Boot:** Revision.
- **Revision:** Weekly review. 2/3 of the way through. How's your confidence?
- **Career:** Application tracker full review. Prioritize companies that have responded.

### End of Week 8 — You Should Have
- [ ] ~10 DSA problems (DP 2D)
- [ ] Microservices patterns (CQRS, Saga, Outbox, API composition)
- [ ] Regulatory Reporting Pipeline design (your domain!)
- [ ] Multi-environment CI/CD (dev → staging → prod with security scans)
- [ ] 8 mock interviews done
- [ ] Claude Developer cert exam (if scheduled and ready)

---

## WEEK 9 (Sep 21 — Sep 27): LeetCode Speed Run + Spring Revision + Risk Limits Design
### Theme: Speed up DSA. Time yourself. Interview-like conditions.

**DSA:** LeetCode Medium speed run (timed, 20 min per problem)
**Java/Spring:** Spring Boot revision + common interview questions
**System Design:** Design: Risk Limits Enforcement Service (YOUR domain!)
**DevOps:** Final production deploy + documentation
**AI:** —
**Career:** Mock interview 9 + resume final polish

### Day 57 — Mon Sep 21
- **DSA:** LeetCode Medium speed run — solve 5 mediums in 20 min each. Track which patterns you struggle with under time pressure.
- **Spring Boot:** Revision — top 20 Spring Boot interview questions. Write answers. Practice saying them aloud.
- **System Design:** Design a Risk Limits Enforcement Service — pre-trade vs post-trade limits, limit types (gross, net, exposure), real-time enforcement, limit breach handling.
- **DevOps:** Final production deploy. Everything running on Kubernetes. CI/CD working. Observability dashboards up.
- **Career:** Resume final polish. This is the version you'll apply with. Banking domain language. Project with AI feature highlighted.

### Day  Transaction Processing, Market Data, Regulatory Reporting, Risk Limits. Which 3 are your strongest? Those are your interview go-tos.
- **DevOps:** Write architecture documentation for the project. Diagram + each service + data flow + deployment topology.
- **Career:** Mock interview 9 — DSA, 30 min. Under interview-like conditions.

### Day 59 — Wed Sep 23
- **DSA:** LeetCode Medium speed run — 5 more mediums, 20 min each.
- **Spring Boot:** Revision — common Java interview questions: HashMap internals, ConcurrentHashMap, fail-fast vs fail-safe iterators, TreeMap, PriorityQueue implementation.
- **System Design:** Risk Limits — practice explaining. Use BaNCS Limits experience: "In BaNCS, limits are enforced at..."
- **DevOps:** Document the project's CI/CD pipeline. Draw it. Can you explain it to an interviewer?
- **Career:** Review mock interview 9. Almost there.

### Day 60 — Thu Sep 24
- **DSA:** LeetCode Medium speed run — 5 more mediums, 20 min each.
- **Spring Boot:** Revision — concurrency interview questions: thread pools, CompletableFuture, virtual threads, synchronized vs Lock, deadlock detection.
- **System Design:** Read: Real-time processing patterns. Stream processing (Kafka Streams, Flink). When to use stream processing vs request-response.
- **DevOps:** Project documentation final review. README, architecture diagram, API docs, deployment guide.
- **Career:** Mock interview 10 — System Design, 45 min.

### Day 61 — Fri Sep 25
- **DSA:** LeetCode Medium speed run — 5 more mediums, 20 min each.
- **Spring Boot:** Revision — Spring Security interview questions: JWT flow, OAuth2 flow, security filters, CSRF, CORS.
- **System Design:** Risk Limits — final review. Can you design and explain in 15 min with banking vocabulary?
- **DevOps:** Final project review. Everything documented and deployed.
- **Career:** Review mock interview 10. You should be seeing improvement.

### Day 62 — Sat Sep 26
- **DSA:** Weekly revision — re-solve 10 problems that gave you trouble this week. No notes.
- **Spring Boot:** Full Spring Boot cheat sheet. One page. All concepts.
- **System Design:** Review all designs. Pick your top 3. Practice explaining each in 10-15 min.
- **Career:** Connect with 5 more recruiters. Follow up on all applications.

### Day 63 — Sun Sep 27
- **DSA:** Weekly revision.
- **Spring Boot:** Revision.
- **Revision:** Weekly review. You're 75% through. Next week: start active interviews.
- **Career:** Application tracker review. Which companies have responded? Prioritize those.

### End of Week 9 — You Should Have
- [ ] 25+ LeetCode mediums solved under timed conditions (20 min each)
- [ ] Spring Boot interview cheat sheet (top 20 questions)
- [ ] Java interview cheat sheet (collections, concurrency, JVM)
- [ ] Risk Limits Enforcement Service design (your domain!)
- [ ] Project fully deployed, documented, CI/CD, observability
- [ ] Resume final version
- [ ] 10 mock interviews done

---

## WEEK 10 (Sep 28 — Oct 4): LeetCode Hard + Core Java Revision + Regulatory Pipeline Design
### Theme: Hit the hard problems. Solidify Java fundamentals. Start interviewing.

**DSA:** LeetCode Hard selected (focus on patterns that appear in BFSI interviews)
**Java/Spring:** Core Java revision: collections, concurrency, JVM, memory model
**System Design:** Design: Regulatory Reporting Pipeline (revisit with more depth)
**DevOps:** —
**AI:** —
**Career:** START ACTIVE INTERVIEWS

### Day 64 — Mon Sep 28
- **DSA:** LeetCode Hard — Median of Two Sorted Arrays, Regular Expression Matching (DP), Merge K Sorted Lists (Heap)
- **Spring Boot:** Core Java revision — Collections framework: ArrayList vs LinkedList, HashMap internals (array + linked list + red-black tree), ConcurrentHashMap, TreeMap, PriorityQueue (heap).
- **System Design:** Regulatory Reporting Pipeline — revisit. Add more depth: data lineage, reconciliation, exception handling, regulatory deadlines.
- **Career:** Start actively interviewing. Apply to 10 new roles this week. Reach out to all referrals.

### Day 65 — Tue Sep 29
- **DSA:** LeetCode Hard — Trapping Rain Water (two pointers), Sliding Window Maximum (deque/monotonic), Word Ladder (BFS)
- **Spring Boot:** Core Java revision — Concurrency: thread states, synchronized, volatile, ReentrantLock, ReadWriteLock, StampedLock, CompletableFuture, virtual threads.
- **System Design:** Regulatory Reporting — practice explaining with more depth. 15 min. Use banking vocabulary.
- **Career:** Phone screen / online assessment if scheduled. Treat it seriously.

### Day 66 — Wed Sep 30
- **DSA:** LeetCode Hard — Alien Dictionary (topological sort), Word Search II (Trie + backtracking), Reconstruct Itinerary (graph + greedy)
- **Spring Boot:** Core Java revision — JVM: memory model, GC algorithms (G1, ZGC), classloading, memory leaks, thread dumps.
- **System Design:** Read: Event-driven architecture. When to use events vs request-response. How does this apply to regulatory reporting?
- **Career:** Phone screen / online assessment if scheduled.

### Day 67 — Thu Oct 1
- **DSA:** LeetCode Hard — Minimum Window Substring (sliding window), Longest Valid Parentheses (stack), Largest Rectangle in Histogram (stack/monotonic)
- **Spring Boot:** Core Java revision — I/O: NIO, ByteByffer, channels, files. Understand blocking vs non-blocking I/O.
- **System Design:** Review all system designs. You should have 10+ designs. Pick 3 you're most confident on.
- **Career:** Phone screen / online assessment if scheduled.

### Day 68 — Fri Oct 2
- **DSA:** LeetCode Hard — N-Queens (backtracking), Sudoku Solver (backtracking), Jump Game II (greedy)
- **Spring Boot:** Core Java revision — Exceptions: checked vs unchecked, custom exceptions, try-with-resources, exception chaining.
- **System Design:** Mock system design practice — pick a random prompt. 30 min. Draw and explain.
- **Career:** Phone screen / online assessment if scheduled.

### Day 69 — Sat Oct 3
- **DSA:** Weekly revision — re-solve 5 hard problems that gave you trouble.
- **Spring Boot:** Full Core Java cheat sheet — collections, concurrency, JVM, I/O, exceptions. One page.
- **System Design:** Mock system design practice — pick another random prompt. 30 min.
- **Career:** Follow up on all interviews. Send thank-you emails.

### Day 70 — Sun Oct 4
- **DSA:** Weekly revision.
- **Spring Boot:** Revision.
- **Revision:** Weekly review.
- **Career:** Application tracker review. How many interviews in progress?

### End of Week 10 — You Should Have
- [ ] 15+ LeetCode hards solved
- [ ] Core Java fully revised (collections, concurrency, JVM, I/O, exceptions)
- [ ] Active interviews started
- [ ] 12 mock interviews done

---

## WEEK 11 (Oct 5 — Oct 11): Interview Simulation + System Design Mocks
### Theme: Full interview simulation. DSA + System Design + Core Java + Spring Boot.

**DSA:** LeetCode contest simulation (timed, contest-like conditions)
**Java/Spring:** Mock interview warmups — practice explaining concepts aloud
**System Design:** System design mock practice (timed, 45 min each)
**Career:** Active interviews

### Day 71 — Mon Oct 5
- **DSA:** LeetCode Weekly Contest simulation — 4 problems, 90 min. Real contest conditions.
- **Spring Boot:** Warmup — explain Spring Boot auto-configuration aloud (5 min). Record yourself. Listen back.
- **System Design:** Mock — design a distributed cache (Redis-like). 45 min. Draw and explain.
- **Career:** Active interviews. Phone screens, online assessments.

### Day 72 — Tue Oct 6
- **DSA:** LeetCode Biweekly Contest simulation — 4 problems, 90 min.
- **Spring Boot:** Warmup — explain JVM garbage collection aloud (5 min). Record.
- **System Design:** Mock — design a distributed message queue (Kafka-like). 45 min.
- **Career:** Active interviews.

### Day 73 — Wed Oct 7
- **DSA:** LeetCode contest problems — re-solve the ones you couldn't do in time.
- **Spring Boot:** Warmup — explain ConcurrentHashMap internals aloud (5 min). Record.
- CompletableFuture, and virtual threads. Practice whiteboarding.
- **Career:** Active interviews.

### Day 74 — Thu Oct 8
- **DSA:** LeetCode Hard speed run — 5 hards, 25 min each.
- **Spring Boot:** Warmup — explain Spring Security JWT flow aloud (5 min). Record.
- **System Design:** Mock — design a rate limiter (distributed). 45 min. Compare with your earlier version. Improved?
- **Career:** Active interviews.

### Day 75 — Fri Oct 9
- **DSA:** LeetCode Hard speed run — 5 hards, 25 min each.
- **System Design:** Mock — design a transaction processing system. 45 min. Use banking domain vocabulary.
- **Career:** Active interviews. Follow up on all pending.

### Day 76 — Sat Oct 10
- **DSA:** Weekly revision — 10 problems from this week, no notes.
- **System Design:** Mock — design a market data streaming platform. 45 min. Use banking domain vocabulary.
- **Career:** Review all active interviews. Status? Next steps?

### Day 77 — Sun Oct 11
- **DSA:** Weekly revision.
- **System Design:** Review all system design mock practice. Which designs are you most confident on?
- **Revision:** Weekly review.
- **Career:** Application tracker review. Any offers? Any final rounds coming up?

### End of Week 11 — You Should Have
- [ ] 20+ LeetCode hards solved + contest simulation
- [ ] System design mock practice (4+ full mocks)
- [ ] Active interviews in progress
- [ ] Confidence in explaining Spring Boot, Java, and system design aloud

---

## WEEK 12 (Oct 12 — Oct 18): Final Revision + Interview Excellence
### Theme: Polish everything. Be interview-ready. Every day is interview prep.

**DSA:** Final revision + weak area focus
**Java/Spring:** Final revision + project demo prep
**System Design:** Final system design practice
**Career:** Active interviews + offer negotiation prep

### Day 78 — Mon Oct 12
- **DSA:** Final revision — re-solve 10 problems across different patterns. No notes. Timed.
- **Spring Boot:** Final revision — Spring Boot cheat sheet, Core Java cheat sheet. Read through. Anything you can't explain, go back and review.
- **System Design:** Final practice — pick your strongest design. Explain it in 15 min. Record. Critique yourself.
- **Career:** Active interviews.

### Day 13 — Tue Oct 13
- **DSA:** Weak area focus — spend 2 hours on your weakest DSA pattern. Grind it.
- **Spring Boot:** Project demo prep — can you explain your project in 5 min? Architecture, tech stack, AI feature, deployment, CI/CD?
- **System Design:** Final practice — pick your second strongest design. 15 min. Record.
- **Career:** Active interviews.

### Day 80 — Wed Oct 14
- **DSA:** Weak area focus — 2 more hours on your weakest pattern.
- **Spring Boot:** Mock interview — explain your project + answer Spring Boot questions for 30 min. Record.
- **System Design:** Final practice — pick your third strongest design. 15 min. Record.
- **Career:** Active interviews. Negotiation prep — know your market value. 16-22 LPA is your range. Don't accept below 14.

### Day 81 — Thu Oct 15
- **DSA:** Mixed revision — 5 problems across different patterns. Timed.
- **Spring Boot:** Final revision — go through your cheat sheets one last time.
- **System Design:** Final practice — random prompt, 30 min. Draw and explain.
- **Career:** Active interviews. Start thinking about offer negotiation.

### Day 82 — Fri Oct 16
- **DSA:** Mixed revision — 5 more problems. Timed.
- **SpringBoot:** Final project review. Is everything clean? README updated? Architecture diagram clear?
- **System Design:** Final review of all cheat sheets and notes.
- **Career:** Active interviews. If you have an offer, start negotiation.

### Day 83 — Sat Oct 17
- **DSA:** Final DSA session — 10 problems, no notes, timed. This is your last hard practice.
- **Spring Boot:** Final project demo run-through. 5 min. Confident.
- **System Design:** Final system design run-through. 15 min. Confident.
- **Career:** Offer negotiation practice. Know your number. Know your walk-away point.

### Day 84 — Sun Oct 18
- **DSA:** Light revision. No hard grinding. Rest your brain.
- **Spring Boot:** Light revision.
- **System Design:** Light revision.
- **Career:** Plan next steps. If you have offers, evaluate. If not, continue interviewing through November.
- **Mental Health:** Take a break. You've worked hard for 12 weeks. Pray, exercise, spend time with family. You're ready.

### End of Week 12 — You Should Have
- [ ] 150+ DSA problems solved (NeetCode 150 + LeetCode Mediums/Hards)
- [ ] 10+ system designs practiced (3 banking-domain specific)
- [ ] Spring Boot project with 2 microservices, Kafka, Docker, Kubernetes, CI/CD, observability, AI integration (RAG endpoint)
- [ ] Project deployed on cloud (DigitalOcean/Vultr/Kubernetes)
- [ ] Resume + LinkedIn optimized with banking domain language
- [ ] Claude Developer cert (if TCS provided free and you completed it during work hours)
- [ ] 12+ mock interviews done
- [ ] Active interviews and potentially offers

---

## RESUME FRAMING: Banking Domain Language

### How to write your TCS experience

**Don't write:**
- "Worked on BaNCS RSM module using QPP"
- "Did low-code development on TCS BaNCS platform"

**Write:**
- "Led microservices development for Regulatory Server Module (RSM) in TCS BaNCS core banking platform, handling regulatory reporting workflows for capital markets clients"
- "Designed and implemented Market Info microservice for real-time market data ingestion and distribution across trading systems"
- "Built Limits enforcement service for pre-trade risk limit checking, including gross/net exposure limits and position limits"
- "Led development of microservices using Spring Boot, REST APIs, and QPP (Quick Process Portfolio) low-code platform for accelerated delivery"
- "Collaborated with Kafka and orchestration teams for event-driven communication between banking microservices"
- "Owned end-to-end delivery of [X] modules from requirements to production deployment for [banking client name if allowed]"
- "Reduced manual regulatory reporting effort by [X]% through automation of [specific workflow]"

### Skills section
- **Languages:** Java, SQL
- **Frameworks:** Spring Boot, Spring Security, Spring Cloud (Gateway, Eureka), Spring Data JPA
- **Microservices:** REST APIs, API Gateway, Service Discovery, Circuit Breaker (Resilience4j), Kafka (fundamentals)
- **Database:** PostgreSQL, JPA/Hibernate, query optimization, indexing
- **DevOps:** Docker, Docker Compose, Kubernetes, GitHub Actions CI/CD, Prometheus, Grafana
- **AI Integration:** LangChain4j, Spring AI, Vector Database (pgvector), RAG (Retrieval Augmented Generation), LLM API integration
- **Domain:** Capital Markets, Regulatory Reporting, Risk Limits, Market Data, Core Banking (TCS BaNCS)
- **Cloud:** DigitalOcean, Vultr, Heroku (deployment experience)
- **Certifications:** [If completed] Claude Certified Developer - Foundations (Anthropic)

---

## INTERVIEW STRATEGY

### For BFSI GCCs (JPMorgan, Goldman, Morgan Stanley, HSBC, etc.)

**Round 1: Online Assessment / Phone Screen**
- DSA: 2-3 problems, 60-90 min. Medium to hard.
- Your preparation: NeetCode 150 + LeetCode mediums/hards. You should be fluent in mediums, comfortable on hards.

**Round 2: Technical Interview (DSA + Core Java)**
- DSA: 1-2 problems, 45 min. They want to see your thought process.
- Core Java: HashMap internals, ConcurrentHashMap, thread pools, volatile vs synchronized, JVM GC, collections.
- Your preparation: Core Java cheat sheets + 150+ DSA problems.

**Round 3: System Design**
- Design a distributed system. 45-60 min. Draw architecture, explain trade-offs.
- YOUR EDGE: Use banking domain vocabulary. When they say "design a transaction processing system," you can say "I worked on this at TCS BaNCS. Here's how we did it..."
- Your preparation: 10+ system designs, 3 banking-specific.

**Round 4: Behavioral / Hiring Manager**
- Why are you leaving TCS? → "I'm looking for deeper engineering work. At TCS, my role involved significant low-code development. I want to build production Java systems with modern architecture."
- Why our company? → Research the company. Know what their GCC does in India.
- Tell me about your project. → 5 min. Architecture, tech stack, AI feature, deployment, CI/CD.

### For Large Product Companies (Amazon, Microsoft, Oracle, etc.)

Same structure but:
- DSA bar is HIGHER. Expect hard problems.
- System design is more general (not banking-specific).
- Your banking domain is less of an edge here. Compensate with stronger DSA + system design.

---

## CLOUD & AI INFRASTRUCTURE

- **DigitalOcean** — App deployment (Droplet or App Platform). Primary compute.
- **Vultr** — Database / secondary service hosting. Managed Postgres or VM. Also serverless inference.
- **Heroku ($300 credits)** — Quick PaaS deployment, staging env, or AI proxy service.
- **AI Inference** — Vultr/DO/Heroku serverless inference endpoints (GLM 5.2 + other open-weights models). Use these credits to add an AI feature to the project.
- **Kubernetes** — Vultr Kubernetes Engine or DigitalOcean Kubernetes for managed K8s.

---

## CLAUDE CERTIFICATIONS (If TCS Provides Free)

**Strategy:** Do ONLY Claude Certified Developer - Foundations ($125, but free via TCS). Skip the other 3 for now.

**When:** Study during TCS work hours only. Do NOT let it eat into your evening prep time.

**Why this one:** It teaches Claude API, MCP servers, custom tools, agent building, security — real engineering skills relevant to the AI integration premium in the job market.

**How it helps your career:**
- Differentiates you as a Java engineer who can also integrate AI/LLM capabilities
- Combined with your project's AI feature (RAG endpoint), it shows you can both understand and apply AI integration
- Put it on your resume under Certifications, not at the top
- The cert is the knowledge. The project feature is the proof. You need both.

**Timeline:** Register during Week 1. Do prep courses during work hours over Weeks 1-6. Take the exam whenever ready (Week 6-8). Don't spend more than 1 week of actual study time.

**Do NOT do:**
- Associate – Foundations (for non-technical people, not for you)
- Architect – Foundations (stretch, not worth the time right now)
- Architect – Professional (requires enterprise deployment experience you don't have)

---

## KEY RESOURCES

- **DSA:** NeetCode 150 (neetcode.io) — free. LeetCode Premium (optional, for company-specific questions).
- **Spring Boot:** Spring Academy (spring.io/academy) — free tier. Spring Boot Reference Docs.
- **System Design:** Grokking the System Design Interview (educative.io). Alex Xu's System Design Interview books. ByteByteGo.
- **Core Java:** Java Concurrency in Practice (book). Baeldung.com for specific topics.
- **Kafka:** Kafka: The Definitive Guide (book). Confluent docs.
- **Docker:** Docker docs (docs.docker.com).
- **Kubernetes:** Kubernetes docs (kubernetes.io docs). Minikube quick start.
- **AI Integration:** LangChain4j docs (docs.langchain4j.dev). Spring AI docs.
- **Mock Interviews:** pramp.com — free. InterviewBit. Practice with friends.
- **Salary Research:** levels.fyi, ambitionbox.com, 6figr.com, glassdoor.com.
- **Job Search:** LinkedIn Jobs, Naukri, Instahyre, Wellfound (for startups if you change your mind).
- **Claude Cert:** Anthropic Partner Academy (anthropic-partners.skilljar.com).

---

## TRACKING

Maintain a spreadsheet with these tabs:
1. **DSA Tracker:** Date, Problem, Pattern, Difficulty, Time, Needed Help?, Notes
2. **Application Tracker:** Company, Role, Location, Date Applied, Referral, Status, Next Step
3. **Mock Interview Tracker:** Date, Platform, Type (DSA/SD), Topic, What went well, What to improve
4. **Weekly Review:** What worked, what didn't, adjustments for next week

---

## FINAL NOTE

Ramish, you have a genuine edge that most engineers don't: **banking domain experience**. BFSI GCCs in Mumbai are actively hiring people who understand capital markets, regulatory reporting, and risk limits. JPMorgan is building a 30,000-person GCC in your city. The jobs are there.

The gap between you and those jobs is: DSA fluency, system design depth, and interview sharpness. This 12-week plan closes that gap.

The Claude cert, if TCS gives it free, is a bonus — not the main event. The main event is DSA + Spring Boot depth + system design + your banking domain story.

Do the work. Trust the process. You'll be ready by October.

— Saved to `~/ramish-12-week-plan.md`
