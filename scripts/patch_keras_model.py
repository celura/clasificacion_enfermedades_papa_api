import json
import sys
import zipfile
from pathlib import Path


UNSUPPORTED_NULL_KEYS = {"quantization_config"}


def clean_config(value):
    if isinstance(value, dict):
        return {
            key: clean_config(item)
            for key, item in value.items()
            if not (key in UNSUPPORTED_NULL_KEYS and item is None)
        }
    if isinstance(value, list):
        return [clean_config(item) for item in value]
    return value


def patch_model(source: Path, target: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"No existe el modelo: {source}")
    if source.resolve() == target.resolve():
        raise ValueError("Usa un archivo de salida distinto para no sobrescribir el modelo original.")

    with zipfile.ZipFile(source, "r") as input_zip, zipfile.ZipFile(target, "w") as output_zip:
        for item in input_zip.infolist():
            data = input_zip.read(item.filename)
            if item.filename == "config.json":
                config = json.loads(data.decode("utf-8"))
                data = json.dumps(clean_config(config), separators=(",", ":")).encode("utf-8")
            output_zip.writestr(item, data)


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("ensamble_papa_completo.keras")
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("ensamble_papa_completo_compatible.keras")
    patch_model(source, target)
    print(f"Modelo compatible creado: {target}")


if __name__ == "__main__":
    main()
