from app.tasks import process_frame
from celery.result import AsyncResult
from app.models import FrameData, FrameCharacteristics
from pyhive import hive
import sys
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_hive(host, port, username, database):
    try:
        # Establecer la conexión
        conn = hive.Connection(host=host, port=port, username=username, database=database)
        logger.info("Conexión exitosa a Hive.")
        return conn
    except Exception as e:
        logger.error(f"Error al conectar con Hive: {e}")
        sys.exit(1)

def execute_query(cursor, query):
    try:
        # Ejecutar la consulta
        cursor.execute(query)
        # Obtener los resultados
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        logger.error(f"Error al ejecutar la consulta: {e}")
        return []


def start_frame_processing(frame : FrameCharacteristics):


    """Inicia la tarea Celery para procesar el frame
    task = process_frame.apply_async(args=[frame_data]) # celerity 
    return task.id  
    """
    try:
        """
        Iniciar la consulta a Hive para procesar el frame
        """
    
        # Parámetros de conexión (ajusta estos valores según tu entorno)
        host = "localhost"  # Cambia con la URL de tu clúster EMR
        port = 10000  # Puerto predeterminado de Hive
        username = "hive"  # Usuario Hive
        database = "default"  # Base de datos Hive (ajusta según tu configuración)

        # Conectar a Hive
        conn = connect_to_hive(host, port, username, database)
        cursor = conn.cursor()

        # Ejecutar la consulta en Hive. Aquí se usa la consulta desde el frame que se recibe
        #query = f"SELECT * FROM {frame.video_name} LIMIT 10"  # Modificar según sea necesario
        # Consulta en Hive que relaciona objetos, escenarios y características

        query = ''

        if frame.type == 1:
            query = f"SELECT video_name FROM scenarios WHERE environment_type = '{frame.environment_type}'"

        elif frame.type == 2:
            # Inicia la consulta básica
            query = f"SELECT video_name, sec FROM objects WHERE object_name = '{frame.object_name}'"

            # Agrega el filtro para rgb_color si está presente
            if frame.color:
                query += f" AND color = '{frame.color}'"

            # Agrega el filtro para proximity si está presente
            if frame.proximity:
                query += f" AND proximity = '{frame.proximity}'"

        elif frame.type == 3:   
            # Inicia la consulta básica (sin filtros adicionales)
            query = f"SELECT video_name, sec, COUNT(*) AS object_count FROM objects WHERE object_name = '{frame.object_name}' GROUP BY video_name, sec ORDER BY object_count DESC"
    
        logger.info(f"Ejecutando consulta: {query}")

        # Obtener los resultados de la consulta
        resultados = execute_query(cursor, query)

        if resultados:
            logger.info("Resultados de la consulta:")
            for fila in resultados:
                logger.info(fila)
        else:
            logger.info("No se encontraron resultados.")

        # Cerrar la conexión a Hive
        cursor.close()
        conn.close()

        # Formatear el resultado en JSON
        response_data = []
        

        if frame.type == 1:
            # Si `frame.type` es 1, la respuesta será solo con el `video_name`
            for row in resultados:
                response_data.append({
                    "video_name": row[0]
                })

        elif frame.type == 2:
            # Si `frame.type` es 2, se debe devolver el `video_name`, `sec`, y opcionales `rgb_color` y `proximity`
            for row in resultados:
                response_data.append({
                    "video_name": row[0],
                    "sec": row[1],
                })

        elif frame.type == 3:
            # Si `frame.type` es 3, la respuesta es el conteo de objetos por video
            for row in resultados:
                response_data.append({
                    "video_name": row[0],
                    "sec": row[1],
                    "object_count": row[2]
                })

        return response_data
    
    except Exception as e:
        logger.error(f"Error al procesar el frame: {e}")
        return {"message": "Error en el procesamiento", "error": str(e)}

def get_frame_task_status(task_id: str):
    """
    Consulta el estado de la tarea de un frame
    """

    task = AsyncResult(task_id)

    if task.state == 'PENDING':
        return {"status": "En proceso"}
    elif task.state == 'SUCCESS':
        return {"status": "Completado", "result": task.result}
    elif task.state == 'FAILURE':
        return {"status": "Fallido", "error": str(task.result)}
    return {"status": "Estado desconocido"}
    