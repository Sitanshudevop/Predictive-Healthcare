# Stage 1: Build Frontend
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build Backend & Serve
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies needed for some ML libraries
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy the entire backend source code
COPY backend/ /app/backend/

# Copy the ML models and Knowledge base (required by the backend)
COPY ml/artifacts/ /app/ml/artifacts/
COPY knowledge_base/ /app/knowledge_base/

# Copy built frontend from Stage 1 into the backend container
COPY --from=frontend-builder /app/frontend/dist /app/backend/frontend_dist

# Create data directory for SQLite and ensure it's writable
RUN mkdir -p /app/backend/data && chmod -R 777 /app/backend/data

# Set environment variables for FastAPI and Hugging Face Spaces
ENV HOST=0.0.0.0
ENV PORT=7860
ENV DATABASE_URL=sqlite:////app/backend/data/phs.db
ENV FRONTEND_DIST_DIR=/app/backend/frontend_dist

# Change working directory to backend
WORKDIR /app/backend

# Expose the specific port Hugging Face Spaces looks for
EXPOSE 7860

# Run FastAPI with uvicorn on the correct port
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
