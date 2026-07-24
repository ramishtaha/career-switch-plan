# 🏗️ Spring Boot Microservices Project — Banking Domain

> This project grows across 12 weeks. Each week adds new capabilities.
> By Week 12, this is a production-grade, AI-enhanced microservices system you can demo in interviews.

---

## Architecture (Target — Week 8)

```
                    ┌─────────────────────┐
                    │   API Gateway       │
                    │   (Spring Cloud)    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
   ┌──────────▼──────┐ ┌───────▼───────┐ ┌──────▼────────┐
   │  Product Service │ │ Category Svc  │ │  AI Service   │
   │  (Spring Boot)   │ │ (Spring Boot) │ │ (Spring Boot) │
   └──────┬──────────┘ └───────┬───────┘ └──────┬────────┘
          │                    │                │
          │     Kafka          │                │
          └────────────────────┘                │
                │                               │
          ┌─────▼──────┐              ┌─────────▼─────────┐
          │  Postgres   │              │  pgvector (AI)    │
          │  + HikariCP │              │  + LangChain4j    │
          └────────────┘              │  + LLM API        │
                                      └───────────────────┘
```

## Tech Stack
- **Language:** Java 17
- **Framework:** Spring Boot 3.x, Spring Cloud (Gateway, Eureka)
- **Database:** PostgreSQL with pgvector
- **Messaging:** Apache Kafka
- **AI:** LangChain4j, serverless LLM inference (GLM 5.2)
- **DevOps:** Docker, Docker Compose, Kubernetes, GitHub Actions CI/CD
- **Observability:** Prometheus, Grafana, Spring Actuator
- **Security:** JWT, OAuth2, Spring Security

## AI Feature
RAG (Retrieval Augmented Generation) endpoint:
- User asks a question about products
- System retrieves relevant products from pgvector (semantic search)
- Passes context to LLM (GLM 5.2 via serverless inference)
- Returns AI-generated answer with streaming (SSE)

## Build and Run
```bash
# Docker Compose (local)
docker-compose up -d

# Kubernetes (cloud)
kubectl apply -f k8s/
```

## Week-by-Week Progress
| Week | What's Added |
|------|-------------|
| 1 | 2 microservices, REST APIs, JPA, Docker, CI, first LLM call |
| 2 | Spring Security (JWT), profiles, tests, Actuator |
| 3 | Kafka producer/consumer, Eureka, Gateway, K8s basics |
| 4 | Database optimization, K8s on cloud, pgvector, RAG endpoint |
| 5 | Spring internals (AOP, auto-config), CI/CD pipeline, RAG caching |
| 6 | Concurrency, observability (Prometheus + Grafana) |
| 7 | Security hardening (OWASP, OAuth2), AI feature complete |
| 8 | Microservices patterns (CQRS, Saga, Outbox), multi-env CI/CD |
| 9 | Final production deploy, documentation |
