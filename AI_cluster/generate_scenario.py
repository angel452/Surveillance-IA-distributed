import os
import json

# Ruta de la carpeta detections
detections_folder = "detections"

# Archivo de salida para las queries
output_file = "insert_scenarios_queries_combined.txt"

# Lista para almacenar los valores a insertar
insert_values = []

# Procesar cada carpeta en detections
for video_folder in os.listdir(detections_folder):
    video_folder_path = os.path.join(detections_folder, video_folder)

    # Verifica si es una carpeta
    if os.path.isdir(video_folder_path):
        print(f"Procesando carpeta de video: {video_folder}")
        
        # Ruta del archivo escenario_analysis.json
        json_file_path = os.path.join(video_folder_path, "escenario_analysis.json")
        
        if os.path.exists(json_file_path):
            try:
                # Abre y carga el archivo JSON
                with open(json_file_path, "r") as json_file:
                    data = json.load(json_file)
                    
                    # Extrae los valores necesarios
                    scene = data.get("scene", {})
                    environment_type = scene.get("environment_type", "unknown")
                    description = scene.get("description", "No description available").replace("'", "''")
                    features = scene.get("features", {})
                    weather = features.get("weather", "unknown")
                    time_of_day = features.get("time_of_day", "unknown")
                    terrain = features.get("terrain", "unknown")
                    crowd_level = features.get("crowd_level", "unknown")
                    lighting = features.get("lighting", "unknown")
                    
                    # Formatea los valores para la query
                    values = (
                        f"('{video_folder}', '{environment_type}', '{description}', '{weather}', '{time_of_day}', '{terrain}', '{crowd_level}', '{lighting}')"
                    )
                    insert_values.append(values)
            except Exception as e:
                print(f"  ERROR: No se pudo procesar {json_file_path}: {e}")
        else:
            print(f"  ERROR: No se encontró escenario_analysis.json en {video_folder}")

# Generar la consulta completa
if insert_values:
    full_query = (
        "INSERT INTO scenarios (video_name, environment_type, description, weather, time_of_day, terrain, crowd_level, lighting) VALUES\n"
        + ",\n".join(insert_values) + ";"
    )
    # Escribir la consulta en el archivo de salida
    with open(output_file, "w") as f:
        f.write(full_query)
    print(f"Query generada correctamente en '{output_file}'.")
else:
    print("No se encontraron datos para insertar.")
