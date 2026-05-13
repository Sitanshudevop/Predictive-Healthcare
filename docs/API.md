# API Documentation

> Predictive Healthcare System — RESTful API Reference

**Base URL:** `http://localhost:8000/api`

**Authentication:** Bearer JWT tokens. Include `Authorization: Bearer <token>` header for protected endpoints.

---

## Health & System

### `GET /api/health`
Liveness probe.

**Response:**
```json
{ "status": "healthy", "service": "Predictive Healthcare System" }
```

### `GET /api/version`
Application version and model status.

**Response:**
```json
{
  "version": "1.0.0",
  "name": "Predictive Healthcare System",
  "models_loaded": 3,
  "models_registered": 11
}
```

---

## Authentication

### `POST /api/auth/register`
Register a new user account.

**Body:**
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "SecurePass123"
}
```

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true
}
```

### `POST /api/auth/login`
Authenticate and receive JWT tokens.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### `POST /api/auth/refresh`
Refresh an expired access token.

**Body:**
```json
{ "refresh_token": "eyJ..." }
```

### `GET /api/auth/me` 🔒
Get current user profile.

### `DELETE /api/auth/me` 🔒
GDPR-style account deletion. Removes user and all associated prediction history.

---

## Predictions

All prediction endpoints require authentication (🔒).

### `POST /api/predict/general` 🔒
Predict disease from symptom list.

**Body:**
```json
{ "symptoms": ["headache", "fever", "cough", "fatigue"] }
```

**Response:**
```json
{
  "prediction": "Influenza",
  "confidence": 0.87,
  "top_k": [
    { "disease": "Influenza", "probability": 0.87 },
    { "disease": "Common Cold", "probability": 0.09 }
  ],
  "severity_score": 5.0,
  "recommendation": { ... },
  "disclaimer": "⚠️ MEDICAL DISCLAIMER: ...",
  "model_name": "general_disease_v1"
}
```

### `POST /api/predict/diabetes` 🔒
**Body:**
```json
{
  "pregnancies": 2, "glucose": 140, "blood_pressure": 80,
  "skin_thickness": 25, "insulin": 100, "bmi": 28.5,
  "diabetes_pedigree": 0.6, "age": 35
}
```

### `POST /api/predict/heart` 🔒
**Body:**
```json
{
  "age": 55, "sex": 1, "cp": 2, "trestbps": 130,
  "chol": 250, "fbs": 0, "restecg": 0, "thalach": 150,
  "exang": 0, "oldpeak": 1.5, "slope": 1, "ca": 0, "thal": 2
}
```

### `POST /api/predict/breast-cancer` 🔒
**Body:**
```json
{ "features": [17.99, 10.38, 122.8, 1001, ...] }
```
Accepts the 30 Wisconsin Breast Cancer features as a flat array.

### `POST /api/predict/liver` 🔒
### `POST /api/predict/kidney` 🔒
### `POST /api/predict/mental-health` 🔒

**Mental Health Body:**
```json
{
  "phq9_score": 12, "gad7_score": 8, "stress_level": 6,
  "sleep_hours": 5.5, "exercise_days_per_week": 2,
  "social_support_score": 4, "age": 28
}
```

### `POST /api/predict/severity` 🔒
Score symptom severity on a 0-10 scale.

**Body:**
```json
{ "symptoms": ["chest pain", "shortness of breath"] }
```

**Response:**
```json
{
  "severity_score": 7.8,
  "urgency_level": "high",
  "disclaimer": "⚠️ ..."
}
```

### `POST /api/predict/pneumonia` 🔒
Upload chest X-ray image for pneumonia detection.

**Content-Type:** `multipart/form-data`  
**Field:** `file` (JPEG/PNG, max 5MB)

### `POST /api/predict/skin` 🔒
Upload skin image for lesion classification.

**Content-Type:** `multipart/form-data`  
**Field:** `file` (JPEG/PNG, max 5MB)

---

## Disease Knowledge Base

### `GET /api/disease`
List diseases with pagination.

**Query Params:** `page` (default 1), `page_size` (default 20, max 100)

### `GET /api/disease/search?q=<query>`
Search diseases by name. Min query length: 2.

### `GET /api/disease/{slug_or_id}`
Get full disease profile by slug or numeric ID.

---

## Prediction History

### `GET /api/history` 🔒
Get current user's prediction history.

**Query Params:** `page`, `page_size`

### `GET /api/history/{id}` 🔒
Get a single prediction history entry.

---

## Admin

### `GET /api/admin/stats` 🔒👑
System statistics (admin only).

### `GET /api/admin/models` 🔒👑
Model performance analytics.

---

## Chatbot

### `POST /api/chatbot/message`
Send a message and receive a rule-based response.

**Body:**
```json
{ "message": "What models do you use?" }
```

---

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error description",
  "disclaimer": "⚠️ MEDICAL DISCLAIMER: ..."
}
```

| Status | Meaning                        |
|--------|-------------------------------|
| 400    | Bad request / invalid input    |
| 401    | Unauthorized (missing/invalid token) |
| 403    | Forbidden (insufficient role)  |
| 404    | Resource not found             |
| 409    | Conflict (duplicate email)     |
| 413    | File too large                 |
| 422    | Validation error               |
| 429    | Rate limit exceeded            |
| 503    | ML model not loaded            |
