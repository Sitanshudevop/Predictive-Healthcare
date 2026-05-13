"""
Disease SQLAlchemy model — stores disease knowledge base entries.
"""

from sqlalchemy import Column, Integer, String, Text, JSON

from app.db.base import Base


class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    disease_name = Column(String(255), nullable=False, index=True)
    icd10_code = Column(String(20), nullable=True)
    description = Column(Text, nullable=False)
    common_symptoms = Column(JSON, nullable=False, default=list)
    rare_symptoms = Column(JSON, nullable=False, default=list)
    causes = Column(JSON, nullable=False, default=list)
    risk_factors = Column(JSON, nullable=False, default=list)
    complications = Column(JSON, nullable=False, default=list)
    prevention = Column(JSON, nullable=False, default=list)
    home_remedies = Column(JSON, nullable=False, default=list)
    otc_medications = Column(JSON, nullable=False, default=list)
    prescription_drug_categories = Column(JSON, nullable=False, default=list)
    recommended_specialist = Column(String(255), nullable=True)
    severity_level = Column(String(50), nullable=False, default="moderate")
    avg_recovery_time = Column(String(100), nullable=True)
    when_to_see_doctor = Column(Text, nullable=True)
    red_flag_symptoms = Column(JSON, nullable=False, default=list)
