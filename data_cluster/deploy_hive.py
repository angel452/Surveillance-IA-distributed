from pyhive import hive
import sys

# Función para conectarse a Hive
def connect_to_hive(host, port, username, database):
    try:
        conn = hive.Connection(host=host, port=port, username=username, database=database)
        print("Conexión exitosa a Hive.")
        return conn
    except Exception as e:
        print(f"Error al conectar con Hive: {e}")
        sys.exit(1)

# Función para ejecutar una consulta en Hive
def execute_query(cursor, query):
    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []

# Función para cargar datos locales en Hive
def load_data_local(cursor, local_path, table_name):
    try:
        cursor.execute(f"LOAD DATA LOCAL INPATH '{local_path}' INTO TABLE {table_name}")
        print(f"Datos cargados exitosamente desde {local_path} a {table_name}.")
    except Exception as e:
        print(f"Error al cargar los datos desde el archivo local: {e}")

# Función para crear tablas
def create_tables(cursor):
    try:
        queries = [
            """
            CREATE TABLE IF NOT EXISTS objects (
                object_name STRING,
                video_name STRING,
                x1 INT,
                y1 INT,
                x2 INT,
                y2 INT,
                color STRING,
                proximity STRING,
                sec INT
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
            """,
            """
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
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
            """,
            """
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
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
            """
        ]
        for query in queries:
            cursor.execute(query)
            print(f"Tabla creada o ya existente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

# Función principal
def main():
    # Parámetros de conexión
    host = "localhost"
    port = 10000
    username = "hive"
    database = "default"

    # Archivos locales para cargar datos
    data_files = {
        "objects": "data_sd/objects_data.csv",
        "scenarios": "data_sd/scenarios_data.csv",
        "features": "data_sd/features_data.csv"
    }

    # Conectar a Hive
    conn = connect_to_hive(host, port, username, database)
    cursor = conn.cursor()

    # Crear tablas
    print("Creando tablas...")
    create_tables(cursor)

    # Cargar datos locales en tablas
    for table, file_path in data_files.items():
        print(f"Cargando datos en la tabla '{table}' desde '{file_path}'...")
        load_data_local(cursor, file_path, table)

    # Ejecutar una consulta de prueba
    query = "SELECT * FROM objects LIMIT 10"
    print(f"Ejecutando consulta: {query}")
    resultados = execute_query(cursor, query)

    # Imprimir los resultados
    if resultados:
        print("Resultados de la consulta:")
        for fila in resultados:
            print(fila)
    else:
        print("No se encontraron resultados o hubo un error.")

    # Cerrar conexión
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
