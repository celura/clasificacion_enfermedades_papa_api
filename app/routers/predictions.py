import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Disease, Prediction
from app.schemas import PredictionRead
from app.services.model_service import classifier

router = APIRouter(prefix="/predictions", tags=["Predicciones"])


def prediction_to_schema(prediction: Prediction) -> PredictionRead:
    return PredictionRead(
        id=prediction.id,
        filename=prediction.filename,
        predicted_class=prediction.predicted_class,
        confidence=prediction.confidence,
        probabilities=json.loads(prediction.probabilities),
        disease=prediction.disease,
        created_at=prediction.created_at,
    )


@router.post("/classify", response_model=PredictionRead, summary="Clasificar enfermedad en hoja de papa")
def classify_potato_leaf(
    file: UploadFile = File(..., description="Imagen de una hoja de papa en formato jpg, png o webp."),
    db: Session = Depends(get_db),
) -> PredictionRead:
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo debe ser una imagen")

    try:
        image = Image.open(file.file)
        result = classifier.predict(image)
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Imagen no valida") from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No fue posible clasificar la imagen: {exc}",
        ) from exc

    disease = db.query(Disease).filter(Disease.class_name == result["predicted_class"]).first()
    prediction = Prediction(
        filename=file.filename,
        predicted_class=result["predicted_class"],
        confidence=result["confidence"],
        probabilities=result["probabilities_json"],
        disease_id=disease.id if disease else None,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction_to_schema(prediction)


@router.get("", response_model=list[PredictionRead], summary="Historial de predicciones")
def list_predictions(db: Session = Depends(get_db)) -> list[PredictionRead]:
    predictions = db.query(Prediction).order_by(Prediction.id.desc()).limit(100).all()
    return [prediction_to_schema(prediction) for prediction in predictions]
