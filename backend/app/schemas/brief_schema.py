# backend/app/schemas/brief_schema.py

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class BriefParams(BaseModel):
    type: Literal["MARKETING", "CREATIF", "PRODUIT"] = Field(..., description="Type de brief à générer")
    secteur: str = Field(..., min_length=2, max_length=100, description="Secteur d’activité (ex: Mode, Tech, Alimentaire)")
    ton: str = Field(..., min_length=2, max_length=50, description="Ton du message (ex: Inspirant, Professionnel, Drôle)")


class BriefOut(BaseModel):
    project_name: str
    project_type: str
    client: str
    goal: str
    target_audience: str
    main_message: str
    tone: str
    constraints: Optional[str] = None
    deliverables: str
    generated_at: datetime

    class Config:
        from_attributes = True
