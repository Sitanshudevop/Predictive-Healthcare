---
title: Predictive Healthcare System
emoji: ⚕️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# 🏥 Predictive Healthcare System (PHS)

Live link - https://sitanshu07-predictivehealthcaresystem.hf.space/

> An academic, AI-powered health intelligence platform using 11 machine learning models for disease prediction, symptom analysis, and health recommendations.

⚠️ **MEDICAL DISCLAIMER**: This is an academic project developed for educational purposes only. It is NOT a certified medical device and should NOT be used for actual medical diagnosis, treatment, or clinical decision-making.

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [ML Models](#ml-models)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Ethics & Compliance](#ethics--compliance)
- [License](#license)

---

## ✨ Features

### Diagnostic Engine
- **NLP Symptom Parser** — Natural language symptom input with disease prediction
- **Biometric Analysis** — 6 specialized models (Diabetes, Heart, Breast Cancer, Liver, Kidney, Mental Health)
- **Image Lab** — CNN-based X-ray pneumonia detection and skin lesion classification
- **Severity Scoring** — 0–10 urgency scale with gradient boosting regression

### Platform
- **Disease Library** — 46 comprehensive disease profiles with ICD-10 codes, symptoms, treatments, and red flags
- **Prediction History** — Timeline-based log with search and model filtering
- **Admin Dashboard** — Real-time metrics grid, system resource monitoring, and model health status
- **AI Chatbot** — Floating assistant with rule-based health Q&A and navigation support
- **Guest Mode** — Full demo access without registration

### Design
- **Midnight Glass** aesthetic — Deep Slate (#020617), glassmorphism, cyan/violet accents
- Responsive layout with mobile navigation
- Smooth micro-animations and hover effects

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React + Vite Frontend                  │
│  (TypeScript, Tailwind CSS, Zustand, React Router)       │
├─────────────────────────────────────────────────────────┤
│                    FastAPI Backend                        │
│  (REST API, JWT Auth, SQLAlchemy ORM, Rate Limiting)     │
├─────────────────────────────────────────────────────────┤
│                    ML Engine Layer                        │
│  (scikit-learn, XGBoost, TensorFlow, spaCy)              │
├─────────────────────────────────────────────────────────┤
│               SQLite Database + JSON KB                   │
│  (Users, Predictions, Disease profiles)                  │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer      | Technology                                                |
|------------|-----------------------------------------------------------|
| Frontend   | React 18, TypeScript, Vite, Tailwind CSS 3, Zustand       |
| Backend    | Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic v2        |
| Auth       | JWT (python-jose), bcrypt (passlib)                       |
| ML         | scikit-learn, XGBoost, TensorFlow, spaCy, SMOTE           |
| Database   | SQLite (dev), PostgreSQL (prod-ready)                     |
| DevOps     | Docker, Docker Compose                                    |

---

## 🤖 ML Models

| # | Model               | Algorithm              | Task                          | Dataset Source       |
|---|----------------------|------------------------|-------------------------------|----------------------|
| 1 | General Disease      | VotingClassifier       | Multi-class disease prediction | Kaggle               |
| 2 | Diabetes Risk        | XGBClassifier          | Binary diabetes screening     | UCI / Kaggle         |
| 3 | Heart Disease        | RandomForest           | Binary heart disease detection | UCI                  |
| 4 | Breast Cancer        | SVM (RBF)              | Malignant/Benign classification | UCI Wisconsin       |
| 5 | Liver Disease        | GradientBoosting       | Binary liver disease detection | UCI ILPD             |
| 6 | Kidney Disease       | RandomForest           | CKD detection                 | UCI                  |
| 7 | Mental Health        | GradientBoosting       | Risk level screening          | Synthetic            |
| 8 | Severity Scorer      | GradientBoostingRegressor | 0-10 urgency score        | Synthetic            |
| 9 | Pneumonia CNN        | MobileNetV2 (transfer) | X-ray classification          | Kaggle Chest X-ray   |
| 10| Skin Lesion CNN      | MobileNetV2 (transfer) | Dermatology classification    | HAM10000             |
| 11| NLP Symptom Parser   | spaCy + rules          | Symptom extraction from text  | Rule-based           |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm 9+

### 1. Clone and setup

```bash
git clone https://github.com/your-username/predictive-healthcare-system.git
cd predictive-healthcare-system
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run backend
uvicorn app.main:app --reload --port 8000
```

### 3. Train ML models

```bash
cd ml
python train_all.py
```

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit **http://localhost:5173** and click **"Sign In as Guest"** for full demo access.

---

## 📁 Project Structure

```
predictive-healthcare-system/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # REST endpoints (auth, predict, disease, etc.)
│   │   ├── core/            # Config, security, dependencies
│   │   ├── db/              # Database session and base
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic (prediction, recommendation)
│   │   ├── ml_loader.py     # Model registry and loading
│   │   ├── main.py          # FastAPI app entry point
│   │   └── seed.py          # Database seeder
│   ├── tests/               # pytest test suite
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Route pages
│   │   ├── stores/          # Zustand state management
│   │   ├── lib/             # API client, utilities
│   │   └── data/            # Static JSON data
│   ├── Dockerfile
│   └── package.json
├── ml/
│   ├── trainers/            # 11 model training scripts
│   ├── data_loaders/        # Dataset download & generation
│   ├── artifacts/           # Trained model pickles + metrics
│   ├── datasets/            # Raw datasets
│   ├── utils.py             # Shared ML utilities
│   └── train_all.py         # Train all models script
├── knowledge_base/
│   └── diseases.json        # 46 disease profiles
├── docs/
│   ├── DECISIONS.md          # Architectural decisions
│   ├── API.md                # API documentation
│   └── ETHICS.md             # Ethics compliance
├── docker-compose.yml
└── README.md
```

---

## 📖 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Key endpoints:

| Method | Endpoint                | Description                    | Auth Required |
|--------|-------------------------|--------------------------------|:---:|
| GET    | `/api/health`            | Liveness probe                 | ✗ |
| POST   | `/api/auth/register`     | Register new user              | ✗ |
| POST   | `/api/auth/login`        | Login, returns JWT             | ✗ |
| GET    | `/api/auth/me`           | Get current user profile       | ✓ |
| POST   | `/api/predict/general`   | General disease prediction     | ✓ |
| POST   | `/api/predict/diabetes`  | Diabetes risk scoring          | ✓ |
| POST   | `/api/predict/heart`     | Heart disease detection        | ✓ |
| POST   | `/api/predict/pneumonia` | X-ray pneumonia classification | ✓ |
| GET    | `/api/disease`           | List diseases (paginated)      | ✗ |
| GET    | `/api/disease/search`    | Search diseases by name        | ✗ |
| GET    | `/api/history`           | Get prediction history         | ✓ |

See [docs/API.md](docs/API.md) for full documentation.

---

## 🧪 Testing

### Backend (pytest)
```bash
cd backend
python -m pytest tests/ -v
```

Test suite covers:
- Health/version endpoints
- Authentication flow (register, login, refresh, delete)
- Disease KB (list, search, detail)
- Prediction endpoints (auth guards, input validation, error handling)

### Frontend (Vitest)
```bash
cd frontend
npx vitest run
```

---

## 🐳 Docker Deployment

```bash
# Build and run all services
docker-compose up --build

# Access:
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API docs:  http://localhost:8000/docs
```

---

## ⚖️ Ethics & Compliance

This project follows responsible AI practices for academic healthcare applications:

- **Medical Disclaimer** — Displayed on every prediction response
- **No Real Patient Data** — Uses only publicly available datasets
- **Bias Awareness** — Known dataset limitations documented
- **GDPR-style Deletion** — Users can delete their accounts and all associated data
- **Transparency** — Model accuracy metrics and confidence scores are always shown

See [docs/ETHICS.md](docs/ETHICS.md) for the full compliance statement.

---

## 📄 License

This project is developed as an academic portfolio piece for a 2nd-year B.Tech CSE semester project. All datasets used are publicly available under their respective licenses.

---

**Built with ❤️ using FastAPI, React, and scikit-learn**
