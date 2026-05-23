from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Disease(Base):
    __tablename__ = "diseases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    class_name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    common_name: Mapped[str] = mapped_column(String(120))
    scientific_agent: Mapped[str | None] = mapped_column(String(180), nullable=True)
    summary: Mapped[str] = mapped_column(Text)
    causes: Mapped[str] = mapped_column(Text)
    characteristics: Mapped[str] = mapped_column(Text)
    treatment: Mapped[str] = mapped_column(Text)
    prevention: Mapped[str] = mapped_column(Text)
    recommendation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    predictions: Mapped[list["Prediction"]] = relationship(back_populates="disease")


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    predicted_class: Mapped[str] = mapped_column(String(80), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    probabilities: Mapped[str] = mapped_column(Text)
    disease_id: Mapped[int | None] = mapped_column(ForeignKey("diseases.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    disease: Mapped[Disease | None] = relationship(back_populates="predictions")
