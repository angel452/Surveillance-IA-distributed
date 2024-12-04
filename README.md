# Reconocimiento de objetos en videovigilancia y almacenamiento en sistema distribuido

Este proyecto integra inteligencia artificial con almacenamiento distribuido para videovigilancia. Utiliza YOLO para detección de objetos y algoritmos para extraer características. Los datos se gestionan en un clúster con Hive sobre HDFS, permitiendo búsquedas eficientes de objetos similares. Incluye una plataforma web y una API REST para análisis y visualización.

## Tabla de Contenidos


1. [Características Principales](#características-principales)
2. [Requisitos Previos](#requisitos-previos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Guía de Instalación](#guía-de-instalación)
5. [Configuración](#configuración)
6. [Uso](#uso)
7. [Arquitectura](#arquitectura)
8. [Contribuciones](#contribuciones)


## Características Principales
- Detección precisa: Identificación de objetos y extracción de características clave en los videos mediante modelos de IA como YOLO.
- Almacenamiento escalable: Gestión eficiente de grandes volúmenes de datos estructurados utilizando Hive sobre HDFS en un clúster distribuido.
- Plataforma web intuitiva: Interfaz para cargar videos, analizar objetos detectados y gestionar resultados de análisis.
- Integración API: Acceso programático para consultar y gestionar datos a través de una API RESTful en el cluster.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes necesarios para cada parte del sistema:

### API (Python)
La API utiliza Python y requiere las siguientes bibliotecas y herramientas:  
- FastAPI  
- Uvicorn  
- Celery  
- Redis  
- PyHive  
- Thrift  
- Thrift-SASL  

### Inteligencia Artificial (Procesamiento de Videos)
El análisis y detección de objetos requiere las siguientes bibliotecas:  
- OpenAI (para tareas de procesamiento avanzado)  
- dotenv  
- OpenCV  
- NumPy  
- Ultralytics YOLO  

### Backend
El backend requiere:  
- Node.js  
- npm  

### Frontend
El frontend está desarrollado en React y requiere un entorno compatible con Node.js y npm.

### Infraestructura
El sistema se monta en un clúster **Amazon EMR** para proporcionar escalabilidad y procesamiento distribuido. Asegúrate de configurar un clúster adecuado con Hive y HDFS.  


## Estructura del Proyecto

El proyecto está organizado en varias carpetas principales que representan los diferentes componentes del sistema. A continuación, se proporciona una descripción general de cada carpeta clave:

### 📁 AI_cluster  
Contiene los scripts y herramientas relacionadas con el procesamiento y análisis de datos utilizando modelos de IA.  
- **Principales funciones:** generación de datos, detección de objetos con YOLO, detección de movimiento y procesamiento de videos.  
- **Archivos clave:**  
  - `main.py`: Punto de entrada para ejecutar el análisis principal.  
  - `src/`: Contiene módulos como `gpt_detector.py` y `yolo_detection.py` para tareas específicas de IA.  

### 📁 API_cluster  
Aloja la implementación de la API RESTful en Python.  
- **Principales funciones:** manejo de tareas en segundo plano (Celery), conexión a Hive, y exposición de datos procesados.  
- **Archivos clave:**  
  - `main.py`: Inicia la API con FastAPI.  
  - `tasks.py`: Gestiona tareas en segundo plano.  
  - `requirements.txt`: Lista de dependencias necesarias para el entorno.  
e
### 📁 data_cluster  
Contiene los datos de entrada y scripts para cargar y gestionar tablas en Hive.  
- **Archivos clave:**  
  - `data_sd/`: Archivos CSV con datos de características, objetos y escenarios.  
  - `deploy_hive.py`: Script para desplegar y configurar Hive.  
  - `querys.sql`: Consultas SQL predefinidas para el sistema.  

### 📁 web_platform  
Contiene la implementación de la plataforma web.  
- **Backend:** Construido con Node.js, permite cargar videos y realizar análisis mediante la API.  
  - **Archivos clave:**  
    - `app.js`: Punto de entrada para el servidor backend.  
    - `controllers/`: Lógica de control para procesar videos y gestionar resultados.  
  - **Carpetas adicionales:**  
    - `uploads/`: Almacena videos cargados por los usuarios.  
    - `detections/`: Resultados de análisis de videos, como imágenes y JSON.  
- **Frontend:** Construido con React, proporciona una interfaz para cargar videos, iniciar análisis y visualizar resultados.  
  - **Archivos clave:**  
    - `src/components/`: Componentes principales como botones, listas de videos y resultados.  
    - `App.js`: Entrada principal de la aplicación web.

    
## Guía de Instalación

### 1. Clonar el repositorio

  ``` bash
    git clone https://github.com/angel452/Surveillance-IA-distributed.git
  ```

## 2. Crear el clúster en AWS

Para comenzar, crea el clúster de Amazon EMR. Asegúrate de que el clúster esté configurado con Hive y HDFS para el almacenamiento distribuido.

### 3. Subir el código de la API y los datos al clúster

Usa el siguiente comando scp para transferir las carpetas API_cluster y data_cluster al clúster de EC2 en el nodo maestro:

  ``` bash
    scp -i "<ruta_a_tu_llave.pem>" -r API_cluster <usuario>@<dirección_ec2>:/<ruta_destino>
    scp -i "<ruta_a_tu_llave.pem>" -r data_cluster <usuario>@<dirección_ec2>:/<ruta_destino>
  ```

### 4. Configurar el entorno
Una vez que hayas subido los archivos, conéctate a tu instancia EC2 y asegúrate de que todas las dependencias necesarias estén instaladas:

- Para la API en Python, instala las dependencias utilizando pip:

    ``` bash
    pip install -r API_cluster/requirements.txt
    ```

### 5. Instanciar y crear las tablas en Hive

Para crear las tablas necesarias en Hive, entra como usuario root y ejecuta Hive desde la CLI:

1. Accede a la instancia EC2 como root:

    ``` bash
    sudo su 
    ```

2. Lanza la CLI de Hive:
    ``` bash
    hive
    ```
3. Dentro de la CLI de Hive, carga las consultas SQL para crear las tablas usando el archivo querys.sql ubicado en data_cluster o se puede colocar manualmente en el cli de hive todas las consultas:

    ``` bash
    source /home/ec2-user/data_cluster/querys.sql;
    ```

### 6. Iniciar el servidor de la API
Para iniciar el servidor de la API, usa el script `start.sh` dentro de la carpeta `API_cluster`. Si es necesario, puedes modificar el puerto en este archivo antes de ejecutarlo.

1. Navega a la carpeta `API_cluster`:
   ```bash
   cd API_cluster
   ```

2. Si necesitas cambiar el puerto en el que se ejecuta la API, edita el archivo start.sh y ajusta la configuración de puerto:

    ``` bash
    nano start.sh
    ``` 
3. Busca la línea donde se define el puerto y modifícalo según sea necesario.
    ``` bash
    ./start.sh
    ```
### 7. Levantar la Plataforma Web

1. Primero, instala las dependencias necesarias para Python, el backend y el frontend:

   - Navega a la carpeta `web_platform/backend/python` y ejecuta:
     ```bash
     cd web_platform/backend/python
     pip install -r requirements.txt
     ```

   - Luego, instala las dependencias de Node.js en el backend:
     ```bash
     cd ../
     npm install
     ```

   - Finalmente, instala las dependencias del frontend:
     ```bash
     cd ../../
     npm install
     ```

2. Para iniciar el servidor del backend, ejecuta:
   ```bash
   npm run server
   ```
3. Para iniciar el frontend, ejecuta:
   ```bash
    npm run start
   ```