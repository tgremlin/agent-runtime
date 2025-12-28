# Proposed Technology Stack (MVP → Scalable, Local + AWS, Minimal Divergence)

This stack is aligned to the **MVP Run Model** and PRD direction: **durable agent runs**, **portable deployments** (Docker Compose locally + AWS cloud), and **offline-capable** operation.

> **Selection criteria (“best in class” for this PRD):**
> - Works offline / self-hosted
> - Proven in production at scale
> - Strong ecosystem + docs
> - Clear role boundaries (edge/auth/orchestration/execution/observability)
> - Minimizes divergence between local and cloud

---

## 1) Edge / Single Endpoint

### ✅ Recommended: Kong Gateway (DB-less mode)
- **Why (Justification):**
  - API gateway purpose-built for microservices: routing, auth integration, rate limiting, request/response policies.
  - **DB-less declarative config** is ideal for portability: config-as-code works the same locally and in AWS, and is simple to ship offline.
- **Docs:**
  - DB-less mode: https://developer.konghq.com/gateway/db-less-mode/
  - Declarative config: https://docs.konghq.com/gateway/latest/admin-api/declarative-configuration/
- **Alternative:** Traefik Proxy
  - **Why:** very easy service discovery with Docker/ECS/K8s; lighter-weight edge proxy, great for MVP.
  - Docs: https://doc.traefik.io/traefik/

---

## 2) Identity Provider (OIDC) — “Cognito replacement”

### ✅ Recommended: Keycloak
- **Why (Justification):**
  - Enterprise-grade OIDC/SAML IdP; works offline; widely adopted in self-hosted environments.
  - Fits PRD need for tenant-aware auth + roles/groups, and keeps local/cloud behavior consistent.
- **Docs:**
  - Containers: https://www.keycloak.org/server/containers
  - Docker getting started: https://www.keycloak.org/getting-started/getting-started-docker
- **Alternative:** ORY Kratos + Hydra (or Zitadel)
  - **Why:** Ory gives composable identity components; Zitadel offers modern IAM features.
  - Docs:
    - ORY: https://www.ory.sh/docs/
    - Zitadel: https://zitadel.com/docs/

---

## 3) Durable Orchestration / Run Engine (core to the PRD)

### ✅ Recommended: Temporal
- **Why (Justification):**
  - Provides durable workflows for agent runs: retries/backoff, long-running runs, pause/resume, timers, idempotency patterns, and strong observability.
  - Critical for “run survives restart” success criteria and for scaling beyond “queue + cron + DB rows”.
- **Docs:**
  - Self-hosted deployment (Docker Compose): https://docs.temporal.io/self-hosted-guide/deployment
  - Temporal docker-compose repo: https://github.com/temporalio/docker-compose
  - Web UI: https://docs.temporal.io/web-ui
- **Alternative:** Apache Airflow
  - **Why:** excellent for scheduled ETL-style DAGs; less ideal for interactive, long-lived agent runs, but workable for some early automation patterns.
  - Docs: https://airflow.apache.org/docs/

---

## 4) System of Record Database

### ✅ Recommended: PostgreSQL
- **Why (Justification):**
  - Stable, ubiquitous relational store; ideal for tenants, agents, versions, runs, run_events, billing counters, audit logs.
  - Minimizes divergence: run Postgres locally, use RDS Postgres in AWS later with same SQL and schema.
- **Docs:** https://www.postgresql.org/docs/
- **Alternative:** MySQL
  - **Why:** also solid; fewer native extensions commonly used for vector search; still viable.
  - Docs: https://dev.mysql.com/doc/

---

## 5) Cache / Ephemeral State / Rate Limit Counters

### ✅ Recommended: Redis
- **Why (Justification):**
  - Simple, fast cache + ephemeral coordination (locks, counters).
  - Useful for rate limiting, short-lived queues, and transient state that you don’t want in Postgres.
- **Docs:** https://redis.io/docs/latest/
- **Alternative:** Valkey
  - **Why:** open-source fork with similar API; useful if you want an explicitly permissive redis-compatible path.
  - Docs: https://valkey.io/

> **Security note:** Redis has had high-severity CVEs historically; deploy it private-only, enforce auth/ACLs, and keep versions patched.

---

## 6) Object Storage (Artifacts, uploads, large outputs)

### ✅ Recommended: MinIO (S3-compatible)
- **Why (Justification):**
  - S3-compatible API keeps your app portable: local = MinIO, cloud = MinIO or AWS S3 later.
  - Great for run artifacts (files, PDFs, images), and for large inputs/outputs that shouldn’t live in Postgres.
- **Docs (Compose example):**
  - Docker-compose example: https://github.com/minio/minio/blob/master/docs/orchestration/docker-compose/docker-compose.yaml
- **Alternative:** AWS S3 (cloud) / Ceph (on-prem)
  - **Why:** S3 is the AWS native option; Ceph is common in on-prem clusters.
  - Docs:
    - AWS S3: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html
    - Ceph: https://docs.ceph.com/

---

## 7) Vector Search (RAG / memory) — optional for MVP but aligned with roadmap

### ✅ Recommended (MVP-friendly): pgvector (inside Postgres)
- **Why (Justification):**
  - Keeps infra simple: store embeddings in the same DB as the rest of the platform.
  - Great for early RAG/memory without running another database.
- **Docs:** https://github.com/pgvector/pgvector
- **Alternative (dedicated vector DB):** Qdrant
  - **Why:** strong filtering/payload support, high performance, clean operational model as a dedicated service.
  - Docs: https://qdrant.tech/documentation/

---

## 8) Local Model Serving (offline LLM calls)

### ✅ Recommended (scale-oriented): vLLM
- **Why (Justification):**
  - High-throughput serving engine for LLMs; good path for GPU-backed deployments.
  - Supports production-style serving patterns and scaling as you add more agents/tenants.
- **Docs:** https://docs.vllm.ai/
- **Alternative (super easy local dev):** Ollama
  - **Why:** best “time-to-first-local-model”; great for MVP demos and small installs.
  - Docs: https://docs.ollama.com/

---

## 9) Observability (Logs, Metrics, Traces)

### ✅ Recommended: OpenTelemetry Collector
- **Why (Justification):**
  - Vendor-agnostic telemetry pipeline; avoids lock-in; works offline.
  - Standardizes trace/metric/log emission from API + workers.
- **Docs:** https://opentelemetry.io/docs/collector/
- **Alternative:** Grafana Alloy (OTel distro) or Fluent Bit (logs-focused)
  - Docs:
    - Grafana Alloy: https://grafana.com/docs/alloy/latest/
    - Fluent Bit: https://docs.fluentbit.io/

### ✅ Recommended: Prometheus (metrics)
- **Why (Justification):**
  - De facto OSS standard for metrics; pairs well with Grafana.
- **Docs:** https://prometheus.io/docs/introduction/overview/
- **Alternative:** Grafana Mimir (scalable metrics backend)
  - Docs: https://grafana.com/docs/mimir/latest/

### ✅ Recommended: Grafana (dashboards + alerting)
- **Why (Justification):**
  - Best-in-class OSS visualization; standard dashboards for Prometheus/Loki/Tempo.
- **Docs:** https://grafana.com/docs/
- **Alternative:** Kibana (if you go Elastic stack)
  - Docs: https://www.elastic.co/guide/en/kibana/current/index.html

### ✅ Recommended: Loki (logs)
- **Why (Justification):**
  - Purpose-built for multi-tenant log aggregation; cost-effective label-index approach; integrates tightly with Grafana.
- **Docs:** https://grafana.com/docs/loki/latest/
- **Alternative:** OpenSearch (logs + search)
  - Docs: https://opensearch.org/docs/latest/

> **Traces (optional):** Grafana Tempo (native fit with Grafana stack)  
> Docs: https://grafana.com/docs/tempo/latest/

---

## 10) Secrets Management (optional for MVP, important for enterprise)

### ✅ Recommended: HashiCorp Vault
- **Why (Justification):**
  - Strong secrets lifecycle (rotation, audit logs, dynamic creds); widely used for on-prem/offline security requirements.
- **Docs:** https://developer.hashicorp.com/vault/docs
- **Alternative:** External Secrets + SOPS (GitOps-friendly) or AWS Secrets Manager (cloud)
  - Docs:
    - SOPS: https://github.com/getsops/sops
    - AWS Secrets Manager: https://docs.aws.amazon.com/secretsmanager/

---

## 11) Container Image Distribution for Offline / Airgapped (optional for MVP)

### ✅ Recommended: Harbor (OCI registry)
- **Why (Justification):**
  - A local registry makes offline installs repeatable and supports image retention, RBAC, and policy controls.
  - Useful when you start shipping on-prem bundles to customers.
- **Docs:** https://goharbor.io/docs/
- **Alternative:** Docker Registry (distribution) (lightweight)
  - Docs: https://distribution.github.io/distribution/

> MVP shortcut: you can start with **docker save/load tarballs** and add Harbor when you formalize “offline installers”.

---

## 12) Deployment & Portability Strategy (minimal divergence)

### ✅ Local MVP: Docker Compose
- **Why (Justification):**
  - Lowest friction for a one-box, offline-capable install.
  - Great for dev/proof-of-concept while keeping service boundaries intact.
- **Docs:** https://docs.docker.com/compose/

### ✅ AWS initial: ECS on EC2 (or ECS/Fargate)
- **Why (Justification):**
  - Closest mental model to Compose; good stepping stone before Kubernetes.
  - Lets you keep the same containers, env vars, and service boundaries.
- **Docs:** https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html
- **Alternative:** EKS (Kubernetes)
  - **Why:** strongest long-term scaling/ops story if you’re already Kubernetes-centric.
  - Docs: https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html

---

## 13) Infrastructure as Code (recommended)

### ✅ Recommended: OpenTofu (Terraform-compatible)
- **Why (Justification):**
  - Keeps infra reproducible across AWS and on-prem-like environments.
  - Very similar workflow to Terraform; good for long-term maintainability.
- **Docs:** https://opentofu.org/docs/
- **Alternative:** Terraform
  - Docs: https://developer.hashicorp.com/terraform/docs

---

# MVP “Core vs Optional” summary

## Core (MVP-required)
- Kong (edge)
- Keycloak (OIDC)
- Temporal (durable runs)
- Postgres (system of record)
- Redis (cache/ephemeral)
- MinIO (artifacts)
- API + Worker services

## Optional in MVP (recommended soon after)
- OpenTelemetry Collector
- Prometheus + Grafana + Loki
- pgvector (or Qdrant)
- vLLM/Ollama (depending on hardware)
- Vault
- Harbor

---

## Practical note for “minimal divergence”
To keep local/cloud nearly identical, define a strict environment variable contract (example):
- `OIDC_ISSUER`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`
- `DATABASE_URL`
- `REDIS_URL`
- `TEMPORAL_ADDRESS`
- `S3_ENDPOINT`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`
- `PUBLIC_BASE_URL`

Then:
- Local = Compose fills these in.
- AWS = ECS task defs (or Helm values) fill the same keys.

Your code should never branch on “am I local or cloud?” — only on env vars.

