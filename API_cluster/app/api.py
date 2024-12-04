from fastapi import APIRouter
from app.models import ObjectDetection, FrameCharacteristics
from app.services import start_frame_processing, get_frame_task_status
from app.logger_config import setup_logger 

# Configurar el logger con el nombre del archivo actual
logger = setup_logger(__name__)

router = APIRouter()

# Ruta para recivir caracteristicas 
@router.post("/receive_characteristics")
async def receive_frame(frame: FrameCharacteristics):
    """Recibe las características de un frame de video. Se tiene que clasificar
    segun el tipo (1,2,3)"""
    
    logger.info(f"Recibiendo video: {frame.video_name}")
    logger.info(f"Datos completos del video: {frame.dict()}")
    
    result = start_frame_processing(frame)
        
    #return {"message": "El procesamiento del frame está en marcha", "task_id": task_id}
    return result

# Ruta para consultar el estado de la tarea de procesamiento de un frame
@router.post("/task_status/{task_id}")
async def frame_status(task_id: str):
    """
    Consulta el estado de la tarea de procesamiento de un frame.
    """
    
    logger.info(f"Consultando el estado de la tarea con ID: {task_id}")
    
    status = get_frame_task_status(task_id)
    
    if status["status"] == "Error":
        logger.error(f"Tarea {task_id} no encontrada")
    else:
        logger.info(f"Estado de la tarea {task_id}: {status['status']}")
    
    return status