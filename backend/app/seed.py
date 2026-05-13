"""
Database seeder — loads diseases.json into the database.

Run: python -m app.seed
"""

import json
import sys
from pathlib import Path

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models import Disease
from app.core.config import get_settings

settings = get_settings()


def seed_diseases(db):
    """Seed disease knowledge base from diseases.json."""
    kb_path = Path(__file__).resolve().parent.parent.parent / "knowledge_base" / "diseases.json"

    if not kb_path.exists():
        print(f"[WARN] diseases.json not found at {kb_path}")
        return 0

    with open(kb_path, "r", encoding="utf-8") as f:
        diseases_data = json.load(f)

    count = 0
    for entry in diseases_data:
        existing = db.query(Disease).filter(Disease.slug == entry["id"]).first()
        if existing:
            # Update existing entry
            for key, value in {
                "disease_name": entry["disease_name"],
                "icd10_code": entry.get("icd10_code"),
                "description": entry["description"],
                "common_symptoms": entry.get("common_symptoms", []),
                "rare_symptoms": entry.get("rare_symptoms", []),
                "causes": entry.get("causes", []),
                "risk_factors": entry.get("risk_factors", []),
                "complications": entry.get("complications", []),
                "prevention": entry.get("prevention", []),
                "home_remedies": entry.get("home_remedies", []),
                "otc_medications": entry.get("otc_medications", []),
                "prescription_drug_categories": entry.get("prescription_drug_categories", []),
                "recommended_specialist": entry.get("recommended_specialist"),
                "severity_level": entry.get("severity_level", "moderate"),
                "avg_recovery_time": entry.get("avg_recovery_time"),
                "when_to_see_doctor": entry.get("when_to_see_doctor"),
                "red_flag_symptoms": entry.get("red_flag_symptoms", []),
            }.items():
                setattr(existing, key, value)
        else:
            disease = Disease(
                slug=entry["id"],
                disease_name=entry["disease_name"],
                icd10_code=entry.get("icd10_code"),
                description=entry["description"],
                common_symptoms=entry.get("common_symptoms", []),
                rare_symptoms=entry.get("rare_symptoms", []),
                causes=entry.get("causes", []),
                risk_factors=entry.get("risk_factors", []),
                complications=entry.get("complications", []),
                prevention=entry.get("prevention", []),
                home_remedies=entry.get("home_remedies", []),
                otc_medications=entry.get("otc_medications", []),
                prescription_drug_categories=entry.get("prescription_drug_categories", []),
                recommended_specialist=entry.get("recommended_specialist"),
                severity_level=entry.get("severity_level", "moderate"),
                avg_recovery_time=entry.get("avg_recovery_time"),
                when_to_see_doctor=entry.get("when_to_see_doctor"),
                red_flag_symptoms=entry.get("red_flag_symptoms", []),
            )
            db.add(disease)
            count += 1

    db.commit()
    print(f"[OK] Seeded {count} new diseases ({len(diseases_data)} total in JSON)")
    return count


def main():
    """Run all seeders."""
    print("=" * 60)
    print("Predictive Healthcare System — Database Seeder")
    print("=" * 60)

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("[OK] Database tables created/verified")

    db = SessionLocal()
    try:
        seed_diseases(db)
        print("\n[DONE] Seeding complete!")
    except Exception as e:
        print(f"[ERROR] Seeding failed: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
