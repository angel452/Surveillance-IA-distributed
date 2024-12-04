import os
import json
import csv

# Ruta de la carpeta detections
detections_folder = "detections"

# Archivo de salida para el archivo CSV
output_csv_file = "scenarios_data.csv"

# Encabezados para el archivo CSV
csv_headers = [
    "video_name", 
    "environment_type", 
    "description", 
    "weather", 
    "time_of_day", 
    "terrain", 
    "crowd_level", 
    "lighting"
]

# Lista para almacenar las filas del CSV
csv_rows = []

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
                    
                    # Agregar la fila al CSV
                    csv_rows.append([
                        video_folder, 
                        environment_type, 
                        description, 
                        weather, 
                        time_of_day, 
                        terrain, 
                        crowd_level, 
                        lighting
                    ])
            except Exception as e:
                print(f"  ERROR: No se pudo procesar {json_file_path}: {e}")
        else:
            print(f"  ERROR: No se encontró escenario_analysis.json en {video_folder}")

# Guardar los datos en un archivo CSV
if csv_rows:
    with open(output_csv_file, "w", newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        # Escribir los encabezados
        writer.writerow(csv_headers)
        # Escribir las filas
        writer.writerows(csv_rows)
    print(f"Archivo CSV generado correctamente en '{output_csv_file}'.")
else:
    print("No se encontraron datos para exportar.")
