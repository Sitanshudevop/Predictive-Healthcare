"""
NLP service — symptom extraction from free text using spaCy.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Symptom patterns for EntityRuler
SYMPTOM_PATTERNS = [
    "headache", "fever", "cough", "cold", "fatigue", "nausea", "vomiting",
    "diarrhea", "constipation", "abdominal pain", "chest pain", "back pain",
    "joint pain", "muscle pain", "sore throat", "runny nose", "sneezing",
    "shortness of breath", "difficulty breathing", "wheezing", "dizziness",
    "lightheadedness", "fainting", "blurred vision", "rash", "itching",
    "swelling", "bruising", "bleeding", "weight loss", "weight gain",
    "loss of appetite", "increased appetite", "thirst", "frequent urination",
    "painful urination", "blood in urine", "blood in stool", "dark urine",
    "yellow skin", "jaundice", "pale skin", "night sweats", "chills",
    "numbness", "tingling", "weakness", "tremor", "seizures", "confusion",
    "memory loss", "anxiety", "depression", "insomnia", "excessive sleep",
    "mood swings", "irritability", "hallucinations", "palpitations",
    "rapid heartbeat", "slow heartbeat", "high blood pressure", "low blood pressure",
    "swollen lymph nodes", "lump", "mole changes", "hair loss", "dry skin",
    "acne", "eczema", "psoriasis", "hives", "blisters", "burns", "cuts",
    "fracture", "sprain", "strain", "stiffness", "cramps", "bloating",
    "gas", "heartburn", "acid reflux", "difficulty swallowing", "dry mouth",
    "bad breath", "tooth pain", "ear pain", "hearing loss", "tinnitus",
    "nasal congestion", "nosebleed", "eye pain", "red eyes", "watery eyes",
    "sensitivity to light", "double vision", "neck pain", "shoulder pain",
    "hip pain", "knee pain", "ankle pain", "foot pain", "hand pain",
    "wrist pain", "elbow pain", "jaw pain", "facial pain", "scalp pain",
    "chest tightness", "irregular heartbeat", "cold hands", "cold feet",
    "excessive sweating", "hot flashes", "dehydration", "dry eyes",
    "stomach pain", "lower back pain", "upper back pain", "rib pain",
    "groin pain", "pelvic pain", "menstrual cramps", "irregular periods",
    "vaginal discharge", "erectile dysfunction", "urinary incontinence",
    "blood pressure changes", "sugar cravings", "metallic taste",
    "loss of smell", "loss of taste", "brain fog", "chronic fatigue",
    "body aches", "malaise", "lethargy", "restlessness", "agitation",
    "panic attacks", "social withdrawal", "appetite changes",
    "concentration difficulty", "indecisiveness", "guilt feelings",
    "worthlessness feelings", "suicidal thoughts", "self harm thoughts",
    "paranoia", "delusions", "disorientation", "slurred speech",
    "difficulty walking", "balance problems", "coordination problems",
    "muscle wasting", "muscle twitching", "pins and needles",
    "burning sensation", "stabbing pain", "throbbing pain", "dull ache",
    "sharp pain", "radiating pain", "intermittent pain", "constant pain",
    "skin discoloration", "peeling skin", "flaky skin", "oily skin",
    "skin lesions", "skin ulcers", "wound healing delay", "scarring",
    "stretch marks", "cellulite", "varicose veins", "spider veins",
    "edema", "fluid retention", "ascites", "pleural effusion",
    "coughing blood", "vomiting blood", "rectal bleeding", "black stool",
    "clay colored stool", "mucus in stool", "oily stool", "foul smelling stool",
    "abdominal bloating", "abdominal distension", "abdominal tenderness",
    "rebound tenderness", "guarding", "rigidity", "bowel sounds changes",
    "hiccups", "belching", "flatulence", "anal itching", "hemorrhoids",
    "rectal pain", "fissure", "fistula", "prolapse",
    "skin rash", "high fever", "mild fever", "low grade fever",
    "continuous fever", "intermittent fever", "night fever",
    "morning stiffness", "evening fatigue", "post meal bloating",
    "exercise intolerance", "heat intolerance", "cold intolerance",
    # ── Colloquial / informal synonyms ──
    "tired", "exhausted", "worn out", "run down", "no energy",
    "belly ache", "tummy ache", "tummy pain", "stomach ache",
    "throwing up", "puking", "feeling sick", "queasy",
    "loose stools", "runny tummy", "upset stomach",
    "itchy", "scratching", "scratchy",
    "dizzy", "woozy", "light headed",
    "stuffy nose", "blocked nose", "bunged up",
    "shaky", "shaking", "trembling",
    "achy", "sore", "painful",
    "breathless", "cant breathe", "gasping",
    "swollen", "puffy", "inflamed",
    "hot", "feverish", "burning up",
    "cold hands and feet", "poor circulation",
    "peeing a lot", "going to the toilet a lot",
    "blurry vision", "vision problems",
    "brain fog", "foggy head", "cant concentrate",
    "skin peeling", "flaking skin",
]

NEGATION_CUES = [
    "no", "not", "never", "without", "deny", "denies", "denied",
    "absence", "absent", "negative", "none", "nor", "neither",
    "doesn't", "doesn't", "don't", "don't", "didn't", "didn't",
    "hasn't", "hasn't", "haven't", "haven't", "won't", "won't",
    "can't", "can't", "cannot", "isn't", "isn't", "aren't", "aren't",
]

DURATION_PATTERNS = [
    "days", "weeks", "months", "years", "hours", "minutes",
    "since yesterday", "since last week", "since last month",
    "for a while", "recently", "suddenly", "gradually",
    "intermittently", "constantly", "occasionally", "frequently",
]

SEVERITY_HINTS = {
    "severe": "severe", "mild": "mild", "moderate": "moderate",
    "intense": "severe", "slight": "mild", "extreme": "severe",
    "unbearable": "severe", "tolerable": "mild", "manageable": "mild",
    "excruciating": "severe", "terrible": "severe", "awful": "severe",
    "minor": "mild", "major": "severe", "significant": "moderate",
    "persistent": "moderate", "chronic": "severe", "acute": "severe",
    "sharp": "severe", "dull": "mild", "throbbing": "moderate",
}


class NLPService:
    """NLP symptom extraction service using spaCy EntityRuler."""

    def __init__(self):
        self._nlp = None
        self._initialized = False

    def _initialize(self):
        """Lazy-load spaCy model with custom EntityRuler."""
        if self._initialized:
            return

        try:
            import spacy
            self._nlp = spacy.load("en_core_web_sm")

            # Add custom EntityRuler for symptom detection
            ruler = self._nlp.add_pipe("entity_ruler", before="ner")
            patterns = []
            for symptom in SYMPTOM_PATTERNS:
                # Add exact match pattern
                patterns.append({
                    "label": "SYMPTOM",
                    "pattern": symptom,
                    "id": symptom.replace(" ", "_"),
                })
                # Add capitalized version
                patterns.append({
                    "label": "SYMPTOM",
                    "pattern": symptom.title(),
                    "id": symptom.replace(" ", "_"),
                })
            ruler.add_patterns(patterns)

            self._initialized = True
            logger.info("NLP service initialized with spaCy + EntityRuler")
        except Exception as e:
            logger.error(f"Failed to initialize NLP service: {e}")
            self._nlp = None

    def extract_symptoms(self, text: str) -> list[dict]:
        """
        Extract symptoms from free text.

        Returns list of dicts with keys: symptom, negated, duration, severity_hint
        """
        self._initialize()

        if self._nlp is None:
            # Fallback: simple keyword matching
            return self._fallback_extract(text)

        doc = self._nlp(text.lower())
        extracted = []
        seen = set()

        for ent in doc.ents:
            if ent.label_ == "SYMPTOM":
                symptom_name = ent.text.lower().replace(" ", "_")
                if symptom_name in seen:
                    continue
                seen.add(symptom_name)

                # Check for negation
                negated = self._check_negation(doc, ent)

                # Check for duration
                duration = self._extract_duration(doc, ent)

                # Check for severity
                severity = self._extract_severity(doc, ent)

                extracted.append({
                    "symptom": symptom_name,
                    "negated": negated,
                    "duration": duration,
                    "severity_hint": severity,
                })

        # Also do keyword matching for symptoms not caught by NER
        text_lower = text.lower()
        for symptom in SYMPTOM_PATTERNS:
            symptom_key = symptom.replace(" ", "_")
            if symptom_key not in seen and symptom in text_lower:
                seen.add(symptom_key)
                negated = any(f"{neg} {symptom}" in text_lower for neg in NEGATION_CUES[:10])
                extracted.append({
                    "symptom": symptom_key,
                    "negated": negated,
                    "duration": None,
                    "severity_hint": None,
                })

        return extracted

    def _check_negation(self, doc, entity) -> bool:
        """Check if entity is preceded by a negation cue within 4 tokens."""
        start = max(0, entity.start - 4)
        preceding = doc[start:entity.start]
        for token in preceding:
            if token.text.lower() in NEGATION_CUES:
                return True
        return False

    def _extract_duration(self, doc, entity) -> Optional[str]:
        """Extract duration context near the symptom mention."""
        window = 10
        start = max(0, entity.start - window)
        end = min(len(doc), entity.end + window)
        context = doc[start:end].text.lower()

        for pattern in DURATION_PATTERNS:
            if pattern in context:
                # Try to extract number + duration
                import re
                match = re.search(r"(\d+)\s*" + re.escape(pattern), context)
                if match:
                    return f"{match.group(1)} {pattern}"
                return pattern
        return None

    def _extract_severity(self, doc, entity) -> Optional[str]:
        """Extract severity hints near the symptom mention."""
        window = 5
        start = max(0, entity.start - window)
        end = min(len(doc), entity.end + window)
        context_tokens = [t.text.lower() for t in doc[start:end]]

        for token in context_tokens:
            if token in SEVERITY_HINTS:
                return SEVERITY_HINTS[token]
        return None

    def _fallback_extract(self, text: str) -> list[dict]:
        """Simple keyword matching fallback when spaCy is unavailable."""
        text_lower = text.lower()
        extracted = []
        seen = set()

        for symptom in SYMPTOM_PATTERNS:
            if symptom in text_lower:
                symptom_key = symptom.replace(" ", "_")
                if symptom_key not in seen:
                    seen.add(symptom_key)
                    negated = any(f"{neg} {symptom}" in text_lower for neg in NEGATION_CUES[:10])
                    extracted.append({
                        "symptom": symptom_key,
                        "negated": negated,
                        "duration": None,
                        "severity_hint": None,
                    })

        return extracted


# Global service instance
nlp_service = NLPService()
