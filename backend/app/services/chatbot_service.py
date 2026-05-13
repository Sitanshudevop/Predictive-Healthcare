"""
Chatbot service — rule-based symptom triage chatbot.
"""

import uuid
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Session storage (in-memory for dev; use Redis in production)
_sessions: dict[str, dict] = {}

GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "good morning", "good evening"]
SYMPTOM_KEYWORDS = ["symptom", "symptoms", "feeling", "pain", "ache", "hurts", "sick", "ill", "unwell"]
EMERGENCY_KEYWORDS = ["emergency", "chest pain", "difficulty breathing", "unconscious", "seizure",
                       "stroke", "heart attack", "severe bleeding", "suicidal"]

CHATBOT_RESPONSES = {
    "greeting": (
        "Hello! I'm the PHS Health Assistant. I can help you understand your symptoms and "
        "guide you to the right tools. How can I help you today?\n\n"
        "You can:\n"
        "• Describe your symptoms and I'll suggest which predictor to use\n"
        "• Ask about a specific disease\n"
        "• Ask about how to use the system\n\n"
        "⚠️ Remember: I'm an AI assistant for an academic project, not a medical professional."
    ),
    "emergency": (
        "🚨 **EMERGENCY ALERT** 🚨\n\n"
        "Based on what you've described, this sounds like it could be a medical emergency. "
        "Please:\n\n"
        "1. **Call emergency services immediately** (911 in US, 112 in EU, 108 in India)\n"
        "2. Do NOT rely on this chatbot for emergency medical decisions\n"
        "3. If someone is unconscious, check breathing and begin CPR if trained\n\n"
        "⚠️ This is an academic project and cannot provide emergency medical assistance."
    ),
    "symptom_guide": (
        "Based on your symptoms, here are some tools that might help:\n\n"
        "• **Symptom Checker** (/checker) — Enter multiple symptoms for a general disease prediction\n"
        "• **Specific Predictors** — We have specialized models for diabetes, heart disease, "
        "breast cancer, liver disease, kidney disease, and mental health\n"
        "• **Image Analysis** — Upload chest X-rays (/upload/xray) or skin images (/upload/skin)\n\n"
        "Would you like me to help you navigate to any of these tools?"
    ),
    "help": (
        "Here's how to use the Predictive Healthcare System:\n\n"
        "1. **Symptom Checker** — Select from 132 symptoms or type freely\n"
        "2. **Disease-Specific Predictors** — Enter lab values for specific conditions\n"
        "3. **Image Upload** — Upload chest X-rays or skin images for AI analysis\n"
        "4. **Dashboard** — View your prediction history and risk distribution\n"
        "5. **Results** — Each prediction includes recommendations and severity scores\n\n"
        "⚠️ All predictions are for educational purposes only. Always consult a doctor."
    ),
    "fallback": (
        "I understand you're looking for health information. Here are some ways I can help:\n\n"
        "• Tell me about your symptoms and I'll suggest the right predictor\n"
        "• Ask me about a specific disease for information from our knowledge base\n"
        "• Ask 'help' for a guide on using the system\n\n"
        "⚠️ Remember: This is an academic project, not a medical consultation."
    ),
}

DISEASE_ROUTING = {
    "diabetes": {
        "keywords": ["diabetes", "blood sugar", "glucose", "insulin", "diabetic", "sugar level"],
        "route": "/predict/diabetes",
        "message": "For diabetes assessment, I'd recommend using our **Diabetes Predictor**. "
                  "It uses the Pima Indians dataset model and needs 8 health parameters like glucose, "
                  "BMI, and age. Go to /predict/diabetes to get started."
    },
    "heart": {
        "keywords": ["heart", "cardiac", "chest pain", "cardiovascular", "blood pressure", "cholesterol"],
        "route": "/predict/heart",
        "message": "For heart disease assessment, try our **Heart Disease Predictor**. "
                  "It uses 13 clinical features from the UCI Cleveland dataset. "
                  "Navigate to /predict/heart to begin."
    },
    "breast_cancer": {
        "keywords": ["breast", "breast cancer", "lump in breast", "mammogram"],
        "route": "/predict/breast-cancer",
        "message": "For breast cancer screening, use our **Breast Cancer Predictor**. "
                  "It analyzes 30 features from the Wisconsin dataset. "
                  "Go to /predict/breast-cancer."
    },
    "liver": {
        "keywords": ["liver", "hepatitis", "jaundice", "bilirubin", "fatty liver"],
        "route": "/predict/liver",
        "message": "For liver health assessment, try our **Liver Disease Predictor**. "
                  "Navigate to /predict/liver to enter your lab values."
    },
    "kidney": {
        "keywords": ["kidney", "renal", "creatinine", "urinary", "ckd"],
        "route": "/predict/kidney",
        "message": "For kidney disease assessment, use our **Kidney Disease Predictor**. "
                  "Go to /predict/kidney to enter your clinical parameters."
    },
    "mental_health": {
        "keywords": ["mental", "depression", "anxiety", "stress", "sleep", "mood", "sad", "worried"],
        "route": "/predict/mental-health",
        "message": "For mental health screening, try our **Mental Health Risk Screener**. "
                  "It uses PHQ-9 and GAD-7 questionnaires. Navigate to /predict/mental-health."
    },
    "pneumonia": {
        "keywords": ["pneumonia", "lung", "x-ray", "xray", "chest x-ray", "respiratory"],
        "route": "/upload/xray",
        "message": "For pneumonia detection, upload a chest X-ray image to our **Pneumonia Detector**. "
                  "Go to /upload/xray to upload your image."
    },
    "skin": {
        "keywords": ["skin", "rash", "mole", "lesion", "dermatology", "melanoma", "eczema"],
        "route": "/upload/skin",
        "message": "For skin condition analysis, upload a skin image to our **Skin Disease Classifier**. "
                  "Navigate to /upload/skin."
    },
}


class ChatbotService:
    """Rule-based symptom triage chatbot."""

    def process_message(self, message: str, session_id: Optional[str] = None) -> dict:
        """Process a user message and return a response."""
        if not session_id:
            session_id = str(uuid.uuid4())

        # Initialize or get session
        if session_id not in _sessions:
            _sessions[session_id] = {"history": [], "turn": 0}

        session = _sessions[session_id]
        session["history"].append({"role": "user", "content": message})
        session["turn"] += 1

        msg_lower = message.lower().strip()

        # Check for emergency
        if any(kw in msg_lower for kw in EMERGENCY_KEYWORDS):
            reply = CHATBOT_RESPONSES["emergency"]
            suggestions = ["Call emergency services", "Visit nearest ER"]
        # Check for greeting
        elif any(kw in msg_lower for kw in GREETING_KEYWORDS) and session["turn"] <= 2:
            reply = CHATBOT_RESPONSES["greeting"]
            suggestions = ["Check my symptoms", "What can you do?", "I need help"]
        # Check for help
        elif "help" in msg_lower or "how to" in msg_lower or "what can" in msg_lower:
            reply = CHATBOT_RESPONSES["help"]
            suggestions = ["Symptom Checker", "Disease Predictors", "Image Upload"]
        # Check for specific disease routing
        else:
            routed = False
            for disease_key, info in DISEASE_ROUTING.items():
                if any(kw in msg_lower for kw in info["keywords"]):
                    reply = info["message"]
                    suggestions = [f"Go to {info['route']}", "Tell me more", "Other symptoms"]
                    routed = True
                    break

            if not routed:
                # Check for general symptom discussion
                if any(kw in msg_lower for kw in SYMPTOM_KEYWORDS):
                    reply = CHATBOT_RESPONSES["symptom_guide"]
                    suggestions = ["Use Symptom Checker", "Specific predictor", "Upload image"]
                else:
                    reply = CHATBOT_RESPONSES["fallback"]
                    suggestions = ["Check symptoms", "Help", "Disease info"]

        session["history"].append({"role": "assistant", "content": reply})

        return {
            "reply": reply,
            "session_id": session_id,
            "suggestions": suggestions,
        }


# Global service instance
chatbot_service = ChatbotService()
