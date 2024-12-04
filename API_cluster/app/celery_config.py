# app/celery_config.py
from celery import Celery

celery_app = Celery(
    'tasks',  # Nombre de la aplicación Celery
    broker='redis://localhost:6379/0',  # Conexión al broker Redis
    backend='redis://localhost:6379/0'  # Para almacenar los resultados
)

# Configuración adicional
celery_app.conf.update(
    result_expires=3600,  # Tiempo de expiración de los resultados
)
