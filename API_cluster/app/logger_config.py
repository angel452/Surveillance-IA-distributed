import logging

# Definir los códigos de color
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
RESET = '\033[0m'

class ColorFormatter(logging.Formatter):
    """Un formateador de logging que añade colores a los mensajes"""
    def format(self, record):
        log_message = super().format(record)
        if record.levelno == logging.DEBUG:
            log_message = f"{CYAN}{log_message}{RESET}"
        elif record.levelno == logging.INFO:
            log_message = f"{BLUE}{log_message}{RESET}"
        elif record.levelno == logging.WARNING:
            log_message = f"{YELLOW}{log_message}{RESET}"
        elif record.levelno == logging.ERROR:
            log_message = f"{RED}{log_message}{RESET}"
        elif record.levelno == logging.CRITICAL:
            log_message = f"{RED}{log_message}{RESET}"
        return log_message

def setup_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    """Configura el logger para la aplicación"""
    
    # Crear un logger
    logger = logging.getLogger(name)
    logger.setLevel(level)  # Ajustar el nivel de log
    
    # Crear un handler para la salida estándar (consola)
    console_handler = logging.StreamHandler()
    
    # Crear y configurar el formateador con colores
    formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Añadir el handler al logger
    logger.addHandler(console_handler)
    
    return logger
