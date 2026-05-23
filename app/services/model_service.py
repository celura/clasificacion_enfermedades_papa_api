import json
from pathlib import Path

import numpy as np
from PIL import Image

from app.config import get_settings


class PotatoDiseaseClassifier:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.model = None

    @property
    def is_loaded(self) -> bool:
        return self.model is not None

    def load(self) -> None:
        if self.model is not None:
            return

        model_path = Path(self.settings.model_path)
        if not model_path.exists():
            raise FileNotFoundError(f"No se encontro el modelo en: {model_path}")

        import keras

        self.model = keras.models.load_model(model_path, compile=False, safe_mode=False)

    def _target_size(self) -> tuple[int, int]:
        if self.model is not None:
            input_shape = getattr(self.model, "input_shape", None)
            if isinstance(input_shape, list):
                input_shape = input_shape[0]
            if input_shape and len(input_shape) >= 4 and input_shape[1] and input_shape[2]:
                return int(input_shape[2]), int(input_shape[1])
        return self.settings.model_input_width, self.settings.model_input_height

    def preprocess(self, image: Image.Image) -> np.ndarray:
        target_size = self._target_size()
        image = image.convert("RGB").resize(target_size)
        array = np.asarray(image, dtype=np.float32) / 255.0
        return np.expand_dims(array, axis=0)

    def predict(self, image: Image.Image) -> dict:
        self.load()
        batch = self.preprocess(image)
        raw_prediction = self.model.predict(batch, verbose=0)
        probabilities = np.asarray(raw_prediction)

        if probabilities.ndim > 2:
            probabilities = probabilities.reshape(probabilities.shape[0], -1)
        probabilities = probabilities[0]

        if probabilities.size != len(self.settings.class_names):
            raise ValueError(
                "La salida del modelo no coincide con las clases configuradas: "
                f"{probabilities.size} salidas vs {len(self.settings.class_names)} clases."
            )

        probabilities = probabilities.astype(float)
        if not np.isclose(probabilities.sum(), 1.0, atol=1e-3):
            exp = np.exp(probabilities - np.max(probabilities))
            probabilities = exp / exp.sum()

        class_index = int(np.argmax(probabilities))
        class_name = self.settings.class_names[class_index]
        probability_map = {
            class_name_item: round(float(probability), 6)
            for class_name_item, probability in zip(self.settings.class_names, probabilities)
        }

        return {
            "predicted_class": class_name,
            "confidence": round(float(probabilities[class_index]), 6),
            "probabilities": probability_map,
            "probabilities_json": json.dumps(probability_map),
        }


classifier = PotatoDiseaseClassifier()
