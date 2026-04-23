# ABA Technology Stack

This file defines the target implementation stack for Agentic Business Analytics (ABA).

## 1. Orchestration Layer

- LangGraph for stage-based control flow, branching, retries, checkpoints, and loop-back
- Python-based orchestrator runtime for shared state and node execution

## 2. Agent & Model Layer

- LLMs accessed through a provider-agnostic adapter
- Structured prompt and runtime layer for schema-bound agent inputs and outputs
- JSON-schema or equivalent structured response contracts for agent outputs

## 3. Backend / API Layer

- FastAPI for service endpoints and orchestration APIs
- Pydantic for request, response, and state schema validation
- Uvicorn or equivalent ASGI server for runtime hosting

## 4. Execution Layer

- Sandboxed execution for SQL, Python, and SAS
- Container-based job isolation for analytical workloads
- Worker processes or job runners for asynchronous execution and retries
- Structured execution requests and normalized result payloads

## 5. Data Layer

- PostgreSQL for operational metadata, run state, governance records, and relational storage
- Object storage for artifacts, logs, result bundles, and replay assets
- Vector store when retrieval or reusable memory requires similarity search, preferably pgvector or equivalent

## 6. Context & Memory Layer

- Versioned context pack storage in relational and object storage
- Retrieval layer over metadata, artifacts, and optional vector index
- Run memory scoped to a single execution and reusable memory for approved cross-run reuse

## 7. Observability & Logging

- Structured JSON logging
- OpenTelemetry for traces and correlated events
- Prometheus for metrics collection
- Grafana or equivalent for metrics visualization and alerting
- Centralized log aggregation for run, agent, execution, and governance events

## 8. Governance & Validation

- Schema validation through Pydantic and contract checks
- Policy enforcement through a rule engine or equivalent policy layer
- Validation checkpoints at each stage before progression
- Structured decision logging for approvals, blocks, retries, and escalations

## 9. Frontend / UI

- React with TypeScript for the analyst workspace
- Vite for frontend tooling and local development
- Structured workspace UI for stage progression, context visibility, evidence review, and human-in-the-loop actions

## 10. Dev & Deployment

- Python 3.12 for backend and orchestration services
- Node.js 20+ for frontend development
- Docker for local isolation and reproducible builds
- Docker Compose for local multi-service development
- Containerized deployment with Kubernetes as the enterprise target
- CI-driven testing for backend, frontend, and integration validation
