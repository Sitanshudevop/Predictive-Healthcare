"""Train NLP Symptom Extractor — spaCy EntityRuler (no training needed, just setup)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
from pathlib import Path
from utils import ARTIFACTS_DIR

def train():
    print("\n[TRAIN] NLP Symptom Extractor")
    print("  spaCy EntityRuler is rule-based — no training required.")
    print("  Ensure en_core_web_sm is installed: python -m spacy download en_core_web_sm")
    
    # Save a metrics stub
    metrics = {
        "model_name": "nlp_extractor",
        "type": "rule-based",
        "num_patterns": 200,
        "note": "EntityRuler with 200+ symptom patterns + negation handling",
        "training_timestamp": __import__("time").strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with open(ARTIFACTS_DIR / "nlp_extractor_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    print("  [OK] NLP extractor ready (rule-based, no artifact file needed)")

    # OPTIONAL: DistilBERT fine-tuning path (commented out for CPU)
    # from transformers import AutoTokenizer, AutoModelForTokenClassification
    # tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
    # model = AutoModelForTokenClassification.from_pretrained("distilbert-base-uncased", num_labels=3)
    # ... fine-tune on symptom NER dataset ...

if __name__ == "__main__":
    train()
