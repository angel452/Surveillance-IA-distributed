# Proyecto de Videovigilancia con Almacenamiento Distribuido


Este proyecto integra un sistema de videovigilancia avanzado con una arquitectura de almacenamiento distribuido basada en Hive en clúster. Incluye una plataforma web, una API REST, y el sistema de almacenamiento para gestionar y analizar datos de videos capturados. El objetivo principal es proporcionar una solución escalable y eficiente para la administración y análisis de datos de videovigilancia.

## Tabla de Contenidos

1. Descripción General
2. Características Principales
3. Requisitos Previos
4. Estructura del Proyecto
5. Guía de Instalación
6. Configuración
7. Uso\n8. Arquitectura
9. Contribuciones
10. Licencia

## Descripción General

Este sistema se diseñó para gestionar grandes volúmenes de datos de videovigilancia, incluyendo:
- Procesamiento de detección de objetos y eventos en videos.
- Almacenamiento distribuido para garantizar la escalabilidad y redundancia.
- Una plataforma web para visualizar, buscar y analizar datos.
- Una API REST que actúa como puente entre la plataforma y el almacenamiento distribuido.

## Características Principales\n
- Detección en tiempo real: Identificación de objetos y eventos relevantes en los videos.
- Almacenamiento escalable: Uso de Hive sobre HDFS en un clúster para manejar datos estructurados.
- Plataforma web interactiva: Visualización de datos de videovigilancia y análisis.
- Integración API: Gestión de datos a través de una API RESTful.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

### Backend

- Python 3.8 o superior
- OpenAI para procesamiento de lenguaje natural (si aplica)

- PyHive para conexión a Hive
- Apache Hive (en clúster)\n- Hadoop (HDFS configurado)

### Frontend\n- Node.js (16.x o superior)
- Framework React (o similar, según implementación)

### Infraestructura\n- Servidores con configuración para un clúster Hadoop.
- Navegador web actualizado para la plataforma.\n\n## Estructura del Proyecto
📁 proyecto-videovigilancia

│ 
| ├── 📁 api/ # API REST para integración de datos
│ ├── app.py # Punto de entrada de la API
│ ├── routes/ # Rutas de la API
│ ├── models/ # Modelos de datos
│ └── requirements.txt # Dependencias para la API
│ 
├── 📁 frontend/ # Plataforma web
│ ├── public/ # Archivos estáticos\n│ ├── src/ # Código fuente del frontend (React o similar)\n│ └── package.json # Configuración y dependencias del frontend\n│ \n├── 📁 hive-scripts/ # Scripts para gestión de tablas y datos en Hive\n│ ├── create_tables.hql # Definición de tablas\n│ ├── load_data.hql # Scripts para cargar datos\n│ └── queries.hql # Consultas predefinidas\n│ \n├── 📁 docs/ # Documentación adicional\n│ \n├── .env # Variables de entorno (API keys, rutas, etc.)\n├── .gitignore # Archivos a ignorar por Git\n├── README.md # Documentación principal\n└── setup.sh # Script para configurar el entorno\n\n## Guía de Instalación

### 1. Clonar el repositorio
git clone https://github.com/usuario proyecto-videovigilancia.git\ncd proyecto-videovigilancia

### 2. Configurar el backend
1. Navega a la carpeta api/:
 cd api
2. Instala las dependencias:
  pip install -r requirements.txt
3. Configura las variables de entorno en el archivo .env:\n - Crea un archivo .env en la carpeta api/ con el siguiente contenido:\n HIVE_HOST=localhost\n HIVE_PORT=10000\n HIVE_USERNAME=hive\n HIVE_DATABASE=default\n OPENAI_API_KEY=tu-clave-aqui\n - Reemplaza tu-clave-aqui con tu clave API de OpenAI.\n\n### 3. Configurar el frontend\n1. Navega a la carpeta frontend/:\n cd ../frontend\n2. Instala las dependencias:\n npm install\n\n### 4. Configurar Hive\n1. Configura el clúster de Hadoop y Hive.\n2. Ejecuta los scripts en hive-scripts/ para crear tablas y cargar datos:\n hive -f hive-scripts/create_tables.hql\n hive -f hive-scripts/load_data.hql\n\n### 5. Iniciar el sistema\n1. Inicia el backend:\n python app.py\n2. Inicia el frontend:\n npm start\n\n## Configuración\n\n- API REST: Configura la clave API y el host en .env.\n- Hive: Modifica los scripts de tablas y carga de datos según tus necesidades.\n\n## Uso\n\n1. Accede a la plataforma web en http://localhost:3000.\n2. Utiliza la API para realizar consultas programáticas:\n - GET /api/videos\n - POST /api/analyze\n3. Analiza los datos almacenados en Hive a través de la plataforma o utilizando HiveQL.\n\n## Arquitectura\n\nEl sistema está compuesto por:\n- Frontend (React): Para la interacción del usuario.\n- Backend (Python/Flask): Gestiona las solicitudes y la lógica empresarial.\n- Hive (HDFS): Almacenamiento distribuido para grandes volúmenes de datos.\n- Clúster Hadoop: Para garantizar escalabilidad y procesamiento distribuido.\n\n## Contribuciones\n\n1. Realiza un fork del repositorio.\n2. Crea una rama nueva:\n git checkout -b mi-feature\n3. Realiza los cambios y haz un commit:\n git commit -m "Descripción de los cambios"\n4. Envía tus cambios:\n git push origin mi-feature\n\n## Licencia\n\nEste proyecto está licenciado bajo la licencia MIT. Consulta el archivo LICENSE para más detalles