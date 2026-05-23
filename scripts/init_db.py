import sys
from pathlib import Path

from sqlalchemy import inspect

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from app.database import Base, SessionLocal, engine
from app.seed import seed_diseases


def main() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_diseases(db)
    finally:
        db.close()

    tables = inspect(engine).get_table_names()
    print(f"Base de datos: {engine.url.render_as_string(hide_password=True)}")
    print(f"Tablas disponibles: {', '.join(tables)}")
    print("Datos iniciales cargados correctamente.")


if __name__ == "__main__":
    main()
