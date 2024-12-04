from app.celery_config import celery_app
from app.models import DetectedObjects
import time

@celery_app.task
def process_frame(frame_data):
    """
    Tarea Celery para procesar un frame y devolver los objetos detectados por la IA.
    """

    video_name = frame_data["video_name"]
    timestamp = frame_data["timestamp"]
    image = frame_data["image"]
    aditional_info = frame_data["additional_info"]

    time.sleep(5)

    # ---------------------------------------------------------------
    # LOGICA PARA LA IA: Simulamos que la IA detecta objetos en la imagen
    detected_objects = ["Persona", "Perro", "Gato"]

    # Retornamos los objetos detectados
    result = DetectedObjects(
        video_name = video_name,
        timestamp = timestamp,
        objects = detected_objects,
        aditional_info = aditional_info
    )
    # ---------------------------------------------------------------

    return result.dict()