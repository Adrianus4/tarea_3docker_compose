from dataclasses import dataclass
from functools import lru_cache
from io import BytesIO

import numpy as np
from django.conf import settings
from PIL import Image, ImageOps


IMAGE_SIZE = (224, 224)


class ModelUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class PredictionResult:
    probability: float
    probability_percent: float
    risk_level: str
    risk_label: str
    risk_summary: str


def classify_risk(probability: float) -> tuple[str, str, str]:
    percent = probability * 100
    if percent < 40:
        return "bajo", "Bajo", "Resultado por debajo del umbral de alerta del MVP."
    if percent <= 70:
        return "moderado", "Moderado", "Se recomienda seguimiento clinico si hay sintomas o factores de riesgo."
    return "alto", "Alto", "Se recomienda consulta con personal de salud para evaluacion confirmatoria."


@lru_cache(maxsize=1)
def get_model():
    model_path = settings.ANEMIA_MODEL_PATH
    if not model_path.exists():
        raise ModelUnavailable(f"No se encontro el modelo en {model_path}")

    try:
        from keras.saving import load_model
    except ImportError:
        try:
            from tensorflow.keras.models import load_model
        except ImportError as exc:
            raise ModelUnavailable(
                "No se pudo importar Keras/TensorFlow. Instala las dependencias de requirements.txt."
            ) from exc

    return load_model(model_path, compile=False)


def image_to_batch(image_bytes: bytes) -> np.ndarray:
    with Image.open(BytesIO(image_bytes)) as image:
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        image = image.resize(IMAGE_SIZE)
        array = np.asarray(image, dtype=np.float32)
    return np.expand_dims(array, axis=0)


def normalize_probability(raw_prediction) -> float:
    prediction = np.asarray(raw_prediction, dtype=np.float32)
    if prediction.size == 1:
        probability = float(prediction.reshape(-1)[0])
    elif prediction.ndim >= 2 and prediction.shape[-1] == 2:
        probability = float(prediction[0, 1])
    else:
        probability = float(np.max(prediction))
    return float(np.clip(probability, 0.0, 1.0))


def predict_anemia_risk(image_bytes: bytes) -> PredictionResult:
    batch = image_to_batch(image_bytes)
    model = get_model()
    raw_prediction = model.predict(batch, verbose=0)
    probability = normalize_probability(raw_prediction)
    risk_level, risk_label, risk_summary = classify_risk(probability)
    return PredictionResult(
        probability=probability,
        probability_percent=probability * 100,
        risk_level=risk_level,
        risk_label=risk_label,
        risk_summary=risk_summary,
    )
