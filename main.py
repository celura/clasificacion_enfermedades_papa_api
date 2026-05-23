from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.routers import diseases, predictions
from app.schemas import HealthRead
from app.seed import seed_diseases
from app.services.model_service import classifier


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_diseases(db)
    finally:
        db.close()

    try:
        classifier.load()
    except Exception as exc:
        app.state.model_load_error = str(exc)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "API para clasificar enfermedades en hojas de papa usando un modelo Keras. "
        "Clases soportadas: Early_Blight, Healthy y Late_Blight."
    ),
    lifespan=lifespan,
)

allow_origins = (
    ["*"]
    if settings.cors_origins == "*"
    else [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diseases.router, prefix="/api/v1")
app.include_router(predictions.router, prefix="/api/v1")


@app.get("/", tags=["Sistema"], summary="Bienvenida")
def root() -> dict[str, str]:
    return {
        "message": "API de clasificacion de enfermedades en hoja de papa",
        "swagger": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthRead, tags=["Sistema"], summary="Estado de la API")
def health() -> HealthRead:
    return HealthRead(
        status="ok",
        model_loaded=classifier.is_loaded,
        model_path=settings.model_path,
    )
