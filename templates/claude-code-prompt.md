# Claude Code Prompt — Generate Weekly Learning Guides

> Use this file with Claude Code (or any AI coding assistant) to generate
> in-depth, standalone learning guides for Weeks 2-12.
> Week 1 is already complete — use it as the gold standard reference.

---

## How to Use

Open Claude Code in this repo and run:

```
Read the following files:
1. templates/claude-code-prompt.md (this file)
2. templates/week-guide-template.md
3. weeks/week-01/GUIDE.md (reference — this is the depth and quality to match)
4. ramish-12-week-plan.md (for the specific topics and problems for the target week)

Then generate the GUIDE.md for week-XX following the instructions below.
```

Replace `XX` with the week number (02 through 12).

---

## Generation Instructions for AI

You are generating a comprehensive, standalone learning guide for a
12-week career switch plan. The target reader is Ramish Taha, a Java/Spring Boot
backend engineer with 4 years at TCS (banking domain — BaNCS) preparing for
BFSI GCC interviews (JPMorgan, Goldman, Morgan Stanley).

### Quality Standards

1. **Standalone:** The guide must be self-contained. The reader should NOT need
   to open any external resource to understand the concepts. External links are
   supplementary, not required.

2. **Verified Code:** Every Java code snippet must be syntactically correct and
   compile-ready. Use proper package names, imports (or note them), and complete
   method signatures. No pseudocode. No "// TODO" placeholders.

3. **DSA Solutions:** Every DSA problem must have:
   - Full problem statement (1-2 sentences)
   - Approach explanation (WHY this approach, not just WHAT)
   - Complexity analysis (time + space)
   - Complete, verified Java solution with inline comments
   - Key insight (the non-obvious trick that makes it work)
   - At least one interview follow-up question with answer
   - Alternative approach if one exists with different trade-offs

4. **Spring Boot Code:** Every code snippet must include:
   - Full class definition with package
   - All necessary annotations
   - Constructor injection (not field @Autowired)
   - Proper exception handling
   - Comments explaining non-obvious lines
   - The application.yml configuration snippet where relevant

5. **Depth:** Explain HOW things work internally, not just WHAT to do.
   For example:
   - Don't just say "use @ControllerAdvice" — explain how Spring scans for it
     and how the exception resolution chain works
   - Don't just say "HashMap is O(1)" — explain the hash function, bucket
     array, collision handling, and tree-ification threshold
   - Don't just say "use Docker" — explain layers, caching, and multi-stage builds

6. **Banking Domain Connection:** Where relevant, connect concepts to banking
   systems. Examples:
   - Circuit breaker → "When the risk limits service is down, fail fast instead
     of timing out on every trade"
   - Kafka → "Market data events are published to a Kafka topic; multiple
     subscribers (trading desk, risk, compliance) consume independently"
   - Two Sum → "Given a list of trade IDs and a target transaction amount,
     find two trades that sum to the target (reconciliation use case)"

7. **Interview Q&A:** Include 10-15 interview questions per guide with detailed
   (3-5 sentence) answers. These should cover the most likely questions for
   that week's topics.

### Structure (Follow the Template)

Each guide must follow `templates/week-guide-template.md` with these sections:
1. Table of Contents
2. DSA — [Topic] (concepts, patterns, full solutions for every problem)
3. Spring Boot — [Topic] (concepts, code, annotations, interview Q&A)
4. DevOps — [Topic] (concepts, commands, step-by-step, common issues)
5. AI Integration — [Topic] (concepts, code, API reference)
6. Day-by-Day Task Mapping (from the 12-week plan)
7. Interview Q&A (10-15 questions with answers)
8. Resources (links as supplementary references)

### Week-by-Week Topics

Use ramish-12-week-plan.md for the exact topics per week. Here's a summary:

| Week | DSA | Spring Boot | DevOps | AI | System Design |
|------|-----|-------------|--------|-----|---------------|
| 2 | Sliding Window, Binary Search | Spring Security (JWT), profiles, Actuator, tests | Deploy to DO | Configurable prompts, multi-model | — |
| 3 | Trees, BST | Kafka producer/consumer, Schema Registry | K8s basics (minikube) | LangChain4j + chat memory | URL Shortener, Rate Limiter |
| 4 | Heaps | Database depth (N+1, indexing, query plans, HikariCP, transactions, Flyway) | K8s on cloud | pgvector, RAG endpoint | Web Crawler, Notification System |
| 5 | Graphs, Union Find | Spring internals (auto-config, bean lifecycle, AOP, conditional beans) | GitHub Actions CD | RAG caching, conversation history | Chat System |
| 6 | Tries, Backtracking | Concurrency (threads, locks, CompletableFuture, virtual threads) | Prometheus + Grafana | MCP server (optional) | Transaction Processing (banking!) |
| 7 | DP 1D | JVM internals (memory model, GC, classloading, diagnostics) | OWASP Top 10, JWT, OAuth2 | AI feature complete | Market Data Streaming (banking!) |
| 8 | DP 2D | Microservices patterns (CQRS, Saga, Outbox, API composition) | Multi-env CI/CD | — | Regulatory Reporting (banking!) |
| 9 | LeetCode Medium (timed) | Spring Boot + Java revision | Final production deploy | — | Risk Limits Enforcement (banking!) |
| 10 | LeetCode Hard | Core Java revision | — | — | Regulatory Reporting (depth) |
| 11 | Contest simulation | Mock interview warmups | — | — | Mock system designs |
| 12 | Final revision | Project demo prep | — | — | Final system design practice |

### Output

Write the complete guide to `weeks/week-XX/GUIDE.md`, overwriting the existing
skeleton. The guide should be 20,000-40,000 characters (Week 1 is ~73,000 chars
for reference — match or exceed that depth).

### Important Notes

- Use Java 17 syntax (records, sealed classes, pattern matching where relevant)
- Use Spring Boot 3.x (jakarta.* packages, not javax.*)
- Use PostgreSQL (not MySQL) for database examples
- Use Docker Compose version 3.9+
- For AI integration, use the OpenAI-compatible API format (works with
  Vultr, DigitalOcean, Heroku serverless inference)
- Reference the banking domain (BaNCS, RSM, Market Info, Limits) where relevant
- Include ASCII art diagrams for architecture and data structures
- Every code block must be syntactically valid — no placeholder code
