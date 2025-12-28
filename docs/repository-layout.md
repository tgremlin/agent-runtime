# Repository Layout & Naming Suggestions
## AI Agent Execution Platform (MVP → Scalable)

This document proposes **repository naming options** and a **recommended repository layout** aligned with the PRD, MVP Run Model, and long-term architectural direction.

This repo is intended to represent the **core runtime / execution kernel** of the platform — not the marketplace, UI, or commercial packaging.

---

## 1. Recommended Repository Names

The repo name should:
- Emphasize **execution and durability**
- Avoid marketing or over‑scoping
- Age well into enterprise and on‑prem use
- Be neutral to agent type (DevOps, legal, automation, etc.)

### Tier 1 (Strongest Fits)

### `agent-runtime`
**Meaning:** The environment where agents execute and persist state  
**Why it fits:**
- Maps directly to Temporal‑backed execution
- Works well as a “core kernel” repo
- Clean language for docs and diagrams

---

### `agent-runner`
**Meaning:** The system responsible for running agents  
**Why it fits:**
- Very explicit and honest
- Matches MVP vocabulary (“Run”, “AgentRunWorkflow”)
- Reads well for worker and execution components

---

### `agent-engine`
**Meaning:** A durable execution engine for agents  
**Why it fits:**
- Signals reliability and mechanics
- Good long‑term branding for enterprise

---

### Tier 2 (Safe but Generic)

- `agent-core`
- `agent-platform`
- `run-engine`

These are acceptable but less expressive of the durability/orchestration emphasis.

---

### Names Intentionally Avoided (for MVP)

- `agent-marketplace`
- `autonomous-agents`
- `ai-platform`
- `serverless-agents`

These either over‑promise, underspecify execution, or lock architectural assumptions too early.

---

## 2. Repository Scope

This repository **owns**:
- Agent execution lifecycle
- Run orchestration
- Control + execution planes
- Infrastructure definitions (local + cloud)

This repository **does not own**:
- Customer-facing UI (future repo)
- Marketplace/catalog UX (future repo)
- SDKs (future repos)
- Marketing site

---

## 3. Proposed Repository Layout

```text
agent-runtime/
├── README.md
├── PRD.md
├── docs/
│   ├── architecture.md
│   ├── mvp-sequence-diagram.md
│   ├── run-model.md
│   └── technology-stack.md
│
├── docker/
│   ├── docker-compose.yml
│   ├── docker-compose.observability.yml
│   └── env.example
│
├── gateway/
│   └── kong.yml
│
├── auth/
│   └── keycloak/
│       ├── realm-export.json
│       └── README.md
│
├── api/
│   ├── README.md
│   ├── src/
│   ├── tests/
│   └── Dockerfile
│
├── worker/
│   ├── README.md
│   ├── src/
│   ├── activities/
│   └── Dockerfile
│
├── orchestration/
│   ├── README.md
│   ├── workflows/
│   │   └── agent_run_workflow.*
│   └── temporal/
│       └── docker-compose.override.yml
│
├── storage/
│   └── minio/
│       └── init/
│
├── infra/
│   ├── local/
│   ├── aws/
│   │   ├── ecs/
│   │   ├── ec2/
│   │   └── rds/
│   └── README.md
│
├── scripts/
│   ├── offline-pack.sh
│   ├── offline-load.sh
│   └── migrate.sh
│
└── .github/
    ├── workflows/
    └── CODEOWNERS
```

---

## 4. Folder Responsibilities

### `/api`
- Control plane
- Tenant, agent, version, and run management
- Starts Temporal workflows
- Enforces policy and quotas

### `/worker`
- Execution plane
- Temporal activities
- Tool execution, LLM calls, artifact handling

### `/orchestration`
- Temporal workflows
- Run lifecycle logic
- Retry, pause, resume, approval flows

### `/gateway`
- Kong DB‑less declarative config
- Routing, rate limiting, auth plugins

### `/auth`
- Identity provider config
- Realm definitions
- Local + cloud parity

### `/docker`
- One‑box Docker Compose MVP
- Profiles for optional services
- Minimal divergence from AWS

### `/infra`
- Cloud deployment definitions
- ECS / EC2 initially
- Future‑proofed for EKS

---

## 5. Naming Conventions Inside the Repo

### Code Concepts
- **Run** – single execution instance
- **Workflow** – durable orchestration unit
- **Activity** – execution step
- **Worker** – stateless executor

### Examples
- `AgentRunWorkflow`
- `RunStatus`
- `RunEvent`
- `RunCreated`
- `RunCompleted`

These terms should be consistent across:
- API models
- DB schema
- Workflow definitions
- UI (later)

---

## 6. Long-Term Repo Strategy

Future repos (not part of this one):

- `agent-ui`
- `agent-cli`
- `agent-sdk`
- `agent-marketplace` (eventually)
- `agent-docs` (if public OSS)

This repo remains the **execution nucleus**.

---

## 7. Recommendation Summary

If you want **clarity and longevity**:
> **Final recommendation:** `agent-runtime`

If you want **maximum explicitness**:
> **Strong alternative:** `agent-runner`

Both names:
- align with the PRD
- avoid hype
- scale into enterprise and on‑prem deployments

---

*This document is intended to guide final naming and repo setup decisions. Once a name is chosen, this structure can be committed as the initial repository scaffold.*
