# API de clasificacion de enfermedades en hoja de papa

Backend en Python con FastAPI para integrar el modelo `ensamble_papa_completo_compatible.keras`.

## Clases del modelo

- `Early_Blight`: tizon temprano
- `Healthy`: hoja sana
- `Late_Blight`: tizon tardio

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copia `.env.example` a `.env` y ajusta la ruta del modelo o la conexion a Postgres si cambia tu usuario, clave, host o puerto.

```bash
copy .env.example .env
```

## Base de datos Postgres

La API esta configurada para usar Postgres con esta URL:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/potato_diseases
```

Como ya tienes Postgres instalado, crea la base de datos `potato_diseases` y ajusta `DATABASE_URL` en `.env` si tu usuario, clave, host o puerto son distintos.

Ejemplo desde `psql`:

```sql
CREATE DATABASE potato_diseases;
```

## Ejecutar

```bash
uvicorn main:app --reload
```

Swagger queda disponible en:

```text
http://127.0.0.1:8000/docs
```

## Modelo Keras

El modelo original `ensamble_papa_completo.keras` trae un campo de configuracion (`quantization_config`) que puede fallar al cargar en este entorno. Por eso se genero una copia compatible:

```text
ensamble_papa_completo_compatible.keras
```

Si vuelves a exportar o reemplazar el modelo y aparece el mismo error, regenera la copia compatible:

```bash
python scripts/patch_keras_model.py
```

## Endpoints principales

- `GET /health`: estado de la API y carga del modelo.
- `GET /api/v1/diseases`: lista las enfermedades con informacion, causas, caracteristicas, tratamiento y prevencion.
- `GET /api/v1/diseases/{class_name}`: consulta una clase concreta.
- `POST /api/v1/predictions/classify`: sube una imagen y obtiene la prediccion.
- `GET /api/v1/predictions`: historial de las ultimas 100 predicciones.

## Tablas y datos iniciales

Al iniciar la API se crean las tablas en Postgres y se insertan los datos base para:

- `Early_Blight`
- `Healthy`
- `Late_Blight`

Tablas:

- `diseases`: informacion agronomica por clase.
- `predictions`: historial de predicciones, confianza y probabilidades por clase.

Tambien puedes inicializar la base manualmente:

```bash
python scripts/init_db.py
```

## Ejemplo con curl

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predictions/classify" ^
  -H "accept: application/json" ^
  -H "Content-Type: multipart/form-data" ^
  -F "file=@ruta\a\imagen.jpg"
```

## Frontend

El frontend esta en `frontend/` y usa Expo para web, Android e iOS. Para web local:

```bash
cd frontend
copy .env.example .env
npm run web
```

Para emulador Android, la app usa `http://10.0.2.2:8000` por defecto. Para un celular fisico, cambia `EXPO_PUBLIC_API_BASE_URL` en `frontend/.env` por la IP LAN de tu computador, por ejemplo:

```text
EXPO_PUBLIC_API_BASE_URL=http://192.168.1.20:8000
```

## Nota de preprocesamiento

La API intenta leer el tamano de entrada del modelo. Si no se puede inferir, redimensiona a `224x224`, convierte la imagen a RGB y normaliza los pixeles a rango `0..1`.
