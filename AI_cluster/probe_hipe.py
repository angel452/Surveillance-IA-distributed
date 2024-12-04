from pyhive import hive
import sys

# Función para conectarse a Hive
def connect_to_hive(host, port, username, database):
    try:
        # Establecer la conexión
        conn = hive.Connection(host=host, port=port, username=username, database=database)
        print("Conexión exitosa a Hive.")
        return conn
    except Exception as e:
        print(f"Error al conectar con Hive: {e}")
        sys.exit(1)

# Función para ejecutar una consulta en Hive
def execute_query(cursor, query):
    try:
        # Ejecutar la consulta
        cursor.execute(query)
        # Obtener los resultados
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []

# Función para cargar datos en Hive desde un archivo en S3
def load_data_from_s3(cursor, s3_path, table_name):
    try:
        # Cargar datos desde S3 a la tabla de Hive
        cursor.execute(f"LOAD DATA INPATH '{s3_path}' INTO TABLE {table_name}")
        print(f"Datos cargados exitosamente desde {s3_path} a {table_name}.")
    except Exception as e:
        print(f"Error al cargar los datos desde S3: {e}")
    

# Función principal
def main():
    # Parámetros de conexión (cambia estos valores con los de tu entorno)
    host = "localhost"  # Cambia esta URL con la de tu clúster EMR
    port = 10000  # Puerto predeterminado de Hive
    username = "hive"  # Usuario Hive
    database = "default"  # Base de datos de Hive (puedes cambiarla si es necesario)

    # Conectar a Hive
    conn = connect_to_hive(host, port, username, database)
    cursor = conn.cursor()

    # Consulta que deseas ejecutar
    query = "SELECT * FROM objects LIMIT 10"  # Cambia "tu_tabla" por la tabla que quieras consultar

    # Ejecutar la consulta
    resultados = execute_query(cursor, query)
    
    # Imprimir los resultados de la consulta
    if resultados:
        print("Resultados de la consulta:")
        for fila in resultados:
            print(fila)
    else:
        print("No se encontraron resultados o hubo un error.")


    # Cerrar la conexión
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()