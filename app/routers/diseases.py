from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Disease
from app.schemas import DiseaseCreate, DiseaseRead

router = APIRouter(prefix="/diseases", tags=["Enfermedades"])


@router.get("", response_model=list[DiseaseRead], summary="Listar enfermedades")
def list_diseases(db: Session = Depends(get_db)) -> list[Disease]:
    return db.query(Disease).order_by(Disease.id).all()


@router.get("/{class_name}", response_model=DiseaseRead, summary="Obtener enfermedad por clase")
def get_disease(class_name: str, db: Session = Depends(get_db)) -> Disease:
    disease = db.query(Disease).filter(Disease.class_name == class_name).first()
    if disease is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enfermedad no encontrada")
    return disease


@router.post("", response_model=DiseaseRead, status_code=status.HTTP_201_CREATED, summary="Crear enfermedad")
def create_disease(payload: DiseaseCreate, db: Session = Depends(get_db)) -> Disease:
    exists = db.query(Disease).filter(Disease.class_name == payload.class_name).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La clase ya existe")

    disease = Disease(**payload.model_dump())
    db.add(disease)
    db.commit()
    db.refresh(disease)
    return disease
