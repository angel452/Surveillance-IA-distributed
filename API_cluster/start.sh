#!/bin/bash

# Definir códigos de color
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'  # Para resetear el color

# Función para imprimir mensajes con colores
print_info() {
    echo -e "${BLUE}$1${RESET}"
}

print_success() {
    echo -e "${GREEN}$1${RESET}"
}

print_warning() {
    echo -e "${YELLOW}$1${RESET}"
}

print_error() {
    echo -e "${RED}$1${RESET}"
}


# Iniciar el servidor FastAPI (uvicorn)
print_info "Iniciando FastAPI..."
uvicorn main:app --reload --host 0.0.0.0 --port 1234

