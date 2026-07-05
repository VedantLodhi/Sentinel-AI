# 🛡️ Sentinel AI

> ### The AI Incident Response Engineer for Modern Cloud Applications

**Sentinel AI** is an AI-powered Incident Intelligence Platform that automatically detects production failures, investigates incidents using AI agents, correlates logs, metrics, deployments and documentation, identifies probable root causes, recommends fixes, and generates postmortem reports.

Instead of engineers manually spending hours debugging production systems, Sentinel AI performs the investigation in minutes.

---

# 🚀 Why Sentinel AI?

Modern software systems generate enormous amounts of telemetry.

Every production incident forces engineers to jump across multiple tools:

- Grafana
- Prometheus
- Logs
- Kubernetes
- GitHub
- Deployment History
- Documentation
- Slack

Finding the real cause often takes **30 minutes to several hours**.

**Sentinel AI changes that.**

Instead of showing more dashboards, it investigates the incident itself.

---

# 🎯 Example

### Traditional Investigation

```
Website becomes slow

↓

Open Grafana

↓

Search Logs

↓

Check Deployments

↓

Inspect Database

↓

Read Documentation

↓

Compare Previous Incidents

↓

Find Root Cause
```

Time Required:

> **30–180 Minutes**

---

### Sentinel AI Investigation

```
🚨 Incident Detected

↓

Collect Logs

↓

Analyze Metrics

↓

Inspect Deployment

↓

Search Similar Incidents

↓

AI Investigation

↓

Root Cause Identified

↓

Recommended Fix Generated
```

Time Required:

> **Under 2 Minutes**

---

# ✨ Core Features

## 🤖 AI Investigation

- Multi-Agent Incident Investigation
- AI Root Cause Analysis
- Automated Incident Timeline
- AI Generated Postmortems
- Actionable Fix Recommendations

---

## 📊 Observability

- Logs
- Metrics
- Traces
- Health Monitoring
- Correlation IDs
- Event Correlation Engine

---

## 🧠 AI Engineering

- Multi-Agent Architecture
- Retrieval-Augmented Generation (RAG)
- Long-Term Memory
- Prompt Versioning
- Context Engineering
- Tool Calling
- LLM Routing

---

## 📈 Machine Learning

- Time-Series Anomaly Detection
- Similar Incident Search
- Semantic Retrieval
- Confidence Scoring
- Recommendation Engine

---

## ☁ Cloud Native

- Docker
- PostgreSQL
- Redis
- Qdrant
- MinIO
- OpenTelemetry

---

# 🏗 System Architecture

```
                           Users
                              │
                              ▼
                    Next.js Dashboard
                              │
                              ▼
                   FastAPI API Gateway
                              │
                              ▼
                  Event Correlation Engine
                              │
         ┌─────────────────────────────────────┐
         │        AI Investigation Engine      │
         │                                     │
         │  • Detection Agent                  │
         │  • Investigation Agent              │
         │  • Root Cause Agent                 │
         │  • Solution Agent                   │
         │  • Report Agent                     │
         └─────────────────────────────────────┘
                              │
                              ▼
                  Knowledge Base (Hybrid RAG)
                              │
                              ▼
                  Local + Cloud Model Router
                              │
       Ollama • Gemma • Qwen • Llama • Gemini
```

---

# 🛠 Technology Stack

| Layer | Technologies |
|--------|--------------|
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Backend | Python 3.13, FastAPI, SQLAlchemy, AsyncIO |
| AI | LangGraph, LiteLLM, LlamaIndex, MCP |
| Local LLMs | Ollama, Gemma, Qwen, Llama |
| ML | Anomaly Detection, Semantic Search, Embeddings |
| Databases | PostgreSQL, Redis, Qdrant, MinIO |
| Observability | OpenTelemetry, Prometheus, Grafana, Loki |
| DevOps | Docker, GitHub Actions, Ruff, Black, MyPy, Pytest |

---

# 📂 Project Structure

```
Sentinel-AI/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── ai/
│   │   ├── domains/
│   │   ├── infrastructure/
│   │   ├── workers/
│   │   └── core/
│   │
│   └── tests/
│
├── docs/
├── docker-compose.yml
└── README.md
```

---

# 🗺 Development Roadmap

## ✅ Phase 1 — Foundation

- [x] Clean Architecture
- [x] Docker Infrastructure
- [x] FastAPI Backend
- [x] CI/CD Pipeline
- [x] Structured Logging
- [x] Event Bus
- [x] LLM Abstraction Layer
- [x] Health & Readiness Checks

---

## 🚧 Phase 2 — Domain Layer *(Current)*

- [ ] Database Schema
- [ ] Authentication
- [ ] Organizations
- [ ] Incident Domain
- [ ] Repository Layer
- [ ] Service Layer

---

## 🔜 Phase 3 — AI Core

- [ ] Multi-Agent Investigation
- [ ] Hybrid RAG
- [ ] Context Engineering
- [ ] Memory
- [ ] Tool Calling

---

## 🔜 Phase 4 — Intelligence

- [ ] Root Cause Analysis
- [ ] ML Anomaly Detection
- [ ] Recommendation Engine
- [ ] AI Evaluation

---

## 🔜 Phase 5 — Production

- [ ] Dashboard
- [ ] GitHub Integration
- [ ] Kubernetes Integration
- [ ] Slack Alerts
- [ ] Cloud Deployment

---

# 📈 Current Progress

| Module | Status |
|----------|--------|
| Project Architecture | ✅ Complete |
| Infrastructure | ✅ Complete |
| Backend Foundation | ✅ Complete |
| CI/CD | ✅ Complete |
| Domain Layer | 🚧 In Progress |
| AI Investigation Engine | ⏳ Planned |
| Dashboard | ⏳ Planned |
| Machine Learning | ⏳ Planned |
| Production Deployment | ⏳ Planned |

---

# 🔮 Vision

Sentinel AI is being built with a single goal:

> **Create an AI-powered Site Reliability Engineer capable of understanding production systems, reasoning over telemetry, identifying failures, and helping engineering teams resolve incidents faster.**

The long-term vision is to evolve Sentinel AI into an autonomous engineering platform that not only explains incidents but also predicts failures, recommends preventive actions, and assists teams in operating reliable cloud-native systems.

---

# 👨‍💻 Author

**Vedant Lodhi**

AI Engineering • Backend Engineering • Cloud • Distributed Systems

---

## ⭐ Support the Project

If you find this project interesting, consider giving it a **Star**.

It motivates continued development and helps others discover the project.
