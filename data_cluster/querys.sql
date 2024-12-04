-- ESTRUCTURA DE ALMACENAMIENTO DE DATOS EN HIVE PARA LEVANTAR EL CLUSTER EN HIVE


-- Configurar Hive para ignorar encabezados en los archivos CSV
SET hive.exec.skip.header.line.count = 1;

-- Crear tabla 'objects'
CREATE TABLE IF NOT EXISTS objects (
    object_name STRING,      -- Tipo de objeto (por ejemplo, "umbrella", "person")
    video_name STRING,       -- Relación con el nombre del video
    x1 INT,                  -- Coordenada x1
    y1 INT,                  -- Coordenada y1
    x2 INT,                  -- Coordenada x2
    y2 INT,                  -- Coordenada y2
    color STRING,        -- Color en formato RGB
    proximity STRING,        -- Proximidad ('near', 'middle', 'far')
    sec INT                  -- Segundo exacto del video en el que aparece el objeto
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- Crear tabla 'scenarios'
CREATE TABLE IF NOT EXISTS scenarios (
    video_name STRING COMMENT 'Nombre del video o carpeta de detecciones',
    environment_type STRING COMMENT 'Tipo de entorno, por ejemplo, parking_lot, street, etc.',
    description STRING COMMENT 'Descripción del escenario',
    weather STRING COMMENT 'Condiciones climáticas, por ejemplo, sunny, cloudy, etc.',
    time_of_day STRING COMMENT 'Hora del día, por ejemplo, day, night, etc.',
    terrain STRING COMMENT 'Tipo de terreno, por ejemplo, paved, concrete, etc.',
    crowd_level STRING COMMENT 'Nivel de concurrencia, por ejemplo, low, medium, high',
    lighting STRING COMMENT 'Condición de iluminación, por ejemplo, natural, artificial'
)
COMMENT 'Tabla que almacena la información de los escenarios detectados en los videos'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- Crear tabla 'features'
CREATE TABLE IF NOT EXISTS features (
    video_name STRING COMMENT 'Nombre del video o carpeta',
    sec INT COMMENT 'Segundo del video correspondiente',
    object_name STRING COMMENT 'Nombre del objeto detectado',
    description STRING COMMENT 'Descripción del objeto',
    color1 STRING COMMENT 'Color principal del objeto',
    color2 STRING COMMENT 'Color secundario del objeto',
    size STRING COMMENT 'Tamaño del objeto (small, medium, large)',
    orientation STRING COMMENT 'Orientación del objeto (lateral, rear, etc.)',
    type STRING COMMENT 'Tipo del objeto (SUV, Sedan, etc.)'
)
COMMENT 'Tabla que almacena las características de objetos detectados en los videos'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

-- Cargar datos desde archivos locales
-- Asegúrate de que los archivos estén disponibles en las rutas especificadas

LOAD DATA LOCAL INPATH '/home/ec2-user/data_cluster/data_sd/objects_data.csv'
INTO TABLE objects;

-- Cargar datos en la tabla 'scenarios'
LOAD DATA LOCAL INPATH '/home/ec2-user/data_cluster/data_sd/scenarios_data.csv'
INTO TABLE scenarios;

-- Cargar datos en la tabla 'features'
LOAD DATA LOCAL INPATH '/home/ec2-user/data_cluster/data_sd/features_data.csv'
INTO TABLE features;

-- Verificar los datos cargados
SELECT * FROM objects LIMIT 10;
SELECT * FROM scenarios LIMIT 10;
SELECT * FROM features LIMIT 10;


SELECT video_name
FROM scenarios
WHERE environment_type = 'parking_lot'; 

----
SELECT video_name
FROM objects
WHERE object_name = 'umbrella';  -- Cambia 'umbrella' por el objeto que desees


SELECT video_name
FROM objects
WHERE object_name = 'umbrella'  -- Cambia 'umbrella' por el objeto que desees
  AND rgb_color = '(255, 255, 0)';  -- Cambia '(255, 255, 0)' por el color que desees


SELECT video_name
FROM objects
WHERE object_name = 'umbrella'  -- Cambia 'umbrella' por el objeto que desees
  AND proximity = 'near';  -- Cambia 'near' por la proximidad que desees


SELECT video_name, sec
FROM objects
WHERE object_name = 'umbrella'  -- Cambia 'umbrella' por el objeto que desees
AND rgb_color = 'gray'  -- Cambia '(255, 255, 0)' por el color que desees
AND proximity = 'near';  -- Cambia 'near' por la proximidad que desees



SELECT video_name, COUNT(*) AS object_count
FROM objects
WHERE object_name = 'umbrella'  -- Cambia 'umbrella' por el objeto que desees
GROUP BY video_name
ORDER BY object_count DESC;

drop table objects;
