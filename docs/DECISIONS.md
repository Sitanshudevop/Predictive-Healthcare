# Architectural Decision Log

> This document records key design and implementation decisions made during the development of the Predictive Healthcare System.

---

## ADR-001: Monorepo Structure

**Decision:** Use a monorepo with separate `backend/`, `frontend/`, and `ml/` directories.

**Rationale:** For an academic project, a monorepo simplifies development, CI/CD, and grading. Each layer remains independently deployable via Docker.

**Alternatives Considered:** Separate repositories per layer — rejected for complexity overhead in an academic context.

---

## ADR-002: SQLite for Development, PostgreSQL for Production

**Decision:** Default to SQLite for zero-config development; Docker Compose uses PostgreSQL.

**Rationale:** Students can run the project without installing a database server. SQLAlchemy's ORM abstraction makes switching databases a one-line config change.

---

## ADR-003: JWT Authentication with Refresh Tokens

**Decision:** Use HS256 JWTs with 15-minute access tokens and 7-day refresh tokens.

**Rationale:** Stateless auth simplifies the API. Short access tokens limit exposure if compromised. Refresh tokens avoid forcing re-login.

**Security Notes:**
- Passwords hashed with bcrypt (passlib)
- JWT secret loaded from environment variable
- Rate limiting on auth endpoints (slowapi)

---

## ADR-004: Guest Mode for Demo Access

**Decision:** Implement "Sign In as Guest" with a synthetic guest user (role: `guest`) that bypasses backend auth.

**Rationale:** Portfolio reviewers and examiners need instant access without registration. Guest state is persisted to localStorage with a sentinel token `"guest"`.

**Trade-offs:** Guest users see mock/sample data. Prediction endpoints require real auth for actual ML inference.

---

## ADR-005: 11-Model Architecture

**Decision:** Implement 11 separate ML models rather than one monolithic model.

**Rationale:**
1. Each health domain has different feature sets and data sources
2. Models can be updated independently
3. Demonstrates breadth of ML techniques (classification, regression, NLP, CNN)
4. Each model has its own training script for reproducibility

**Model Registry:** A JSON-based registry (`ml/artifacts/registry.json`) tracks model versions, enabling hot-swapping without restart.

---

## ADR-006: Synthetic Data for Mental Health and Severity Models

**Decision:** Generate synthetic training data for Mental Health Risk Screener and Severity Scorer.

**Rationale:** No suitable open-source dataset exists for these specific prediction tasks. Synthetic data with realistic distributions allows demonstrating the full pipeline.

**Mitigation:** Clearly documented in model metrics and UI ("Synthetic dataset for academic purposes only").

---

## ADR-007: Tailwind CSS with Custom Design Tokens

**Decision:** Use Tailwind CSS 3 with a custom "Midnight Glass" design system defined in `index.css`.

**Rationale:** Tailwind's utility-first approach enables rapid prototyping. Custom `@layer components` classes (`glass-card`, `glass-panel`, `badge`, `btn-primary`) create a consistent design language without CSS-in-JS overhead.

---

## ADR-008: Zustand for State Management

**Decision:** Use Zustand instead of Redux or Context API.

**Rationale:** Zustand is lightweight (~1KB), has zero boilerplate, and supports localStorage persistence out-of-the-box. Perfect for the scale of this application.

---

## ADR-009: Disease Knowledge Base as JSON

**Decision:** Store the 46-disease knowledge base as a static JSON file in `knowledge_base/diseases.json`, loaded into the DB via `seed.py` and also directly imported in the frontend.

**Rationale:** JSON is human-readable and easy to edit. Dual-loading (backend DB + frontend static import) ensures the Disease Library works even without the backend running.

---

## ADR-010: Medical Disclaimer on Every Response

**Decision:** Include a medical disclaimer in every prediction API response and prominently display it in the UI.

**Rationale:** Ethical requirement for any healthcare-adjacent application. Prevents misuse and establishes clear expectations.

---

## ADR-011: MobileNetV2 for Image Models

**Decision:** Use MobileNetV2 (transfer learning) for pneumonia X-ray and skin lesion classification.

**Rationale:** MobileNetV2 is optimized for CPU inference with minimal memory footprint (~14MB). Fine-tuning the top layers on medical imaging datasets provides good accuracy while meeting the 8GB RAM hardware constraint.

---

## ADR-012: Rule-Based Chatbot

**Decision:** Implement the floating chatbot with keyword-matching rules rather than an LLM.

**Rationale:** An LLM would require API keys or large local models, violating the size budget. Rule-based logic is deterministic, fast, and avoids hallucination risks in a medical context.

---

## ADR-013: No Real-Time Backend for Guest Mode

**Decision:** In Guest Mode, the frontend uses mock data for History, Admin metrics, and predictions rather than calling the backend.

**Rationale:** Ensures the frontend demo works independently without a running backend. Real API calls are made only for authenticated (non-guest) users.
