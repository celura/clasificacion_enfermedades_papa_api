from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DiseaseBase(BaseModel):
    class_name: str = Field(..., examples=["Early_Blight"])
    common_name: str = Field(..., examples=["Tizon temprano"])
    scientific_agent: str | None = Field(None, examples=["Alternaria solani"])
    summary: str
    causes: str
    characteristics: str
    treatment: str
    prevention: str
    recommendation: str


class DiseaseCreate(DiseaseBase):
    pass


class DiseaseRead(DiseaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class PredictionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str | None
    predicted_class: str
    confidence: float
    probabilities: dict[str, float]
    disease: DiseaseRead | None
    created_at: datetime


class HealthRead(BaseModel):
    status: str
    model_loaded: bool
    model_path: str
