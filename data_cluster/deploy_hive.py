import os
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

# Función para ejecutar consultas
def execute_query(cursor, query):
    try:
        print(f"Ejecutando consulta:\n{query}")
        cursor.execute(query)
        print("Consulta ejecutada exitosamente.")
        try:
            # Intentar obtener resultados
            results = cursor.fetchall()
            return results
        except:
            # Si no hay resultados que devolver
            return []
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []

# Función para crear las tablas
def create_tables(cursor):
    table_queries = [
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
            video_name STRING,
            environment_type STRING,
            description STRING,
            weather STRING,
            time_of_day STRING,
            terrain STRING,
            crowd_level STRING,
            lighting STRING
        )
        ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        STORED AS TEXTFILE
        """,
        """
        CREATE TABLE IF NOT EXISTS features (
            video_name STRING,
            sec INT,
            object_name STRING,
            description STRING,
            color1 STRING,
            color2 STRING,
            size STRING,
            orientation STRING,
            type STRING
        )
        ROW FORMAT DELIMITED
        FIELDS TERMINATED BY ','
        STORED AS TEXTFILE
        """
    ]
    for query in table_queries:
        execute_query(cursor, query)

# Función para cargar datos en las tablas
def load_data(cursor, table_name, file_path):
    if not os.path.exists(file_path):
        print(f"El archivo {file_path} no existe. Verifica la ruta.")
        return
    query = f"LOAD DATA LOCAL INPATH '{file_path}' INTO TABLE {table_name}"
    execute_query(cursor, query)
    print(f"Datos cargados exitosamente en la tabla '{table_name}' desde '{file_path}'.")

# Función principal
def main():
    # Parámetros de conexión
    host = "localhost"
    port = 10000
    username = "hive"
    database = "default"

    # Rutas relativas de los archivos CSV
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_files = {
        "objects": os.path.join(base_dir, "data_sd", "objects_data.csv"),
        "scenarios": os.path.join(base_dir, "data_sd", "scenarios_data.csv"),
        "features": os.path.join(base_dir, "data_sd", "features_data.csv"),
    }

    # Conectar a Hive
    conn = connect_to_hive(host, port, username, database)
    cursor = conn.cursor()

    # Crear tablas
    print("Creando tablas...")
    create_tables(cursor)

    # Cargar datos en las tablas
    print("Cargando datos...")
    for table, file_path in data_files.items():
        load_data(cursor, table, file_path)

    # Consultas de prueba
    test_queries = [
        "SELECT * FROM objects LIMIT 10",
        "SELECT * FROM scenarios LIMIT 10",
        "SELECT * FROM features LIMIT 10"
    ]
    for query in test_queries:
        results = execute_query(cursor, query)
        if results:
            print(f"Resultados de la consulta ({query.strip()}):")
            for row in results:
                print(row)
        else:
            print(f"No se encontraron resultados para la consulta: {query.strip()}")

    # Cerrar conexión
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
    