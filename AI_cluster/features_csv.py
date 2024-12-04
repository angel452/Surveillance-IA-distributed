import os
import json
import csv

def process_features_to_csv(input_folder, output_csv_file):
    """
    Procesa archivos collage_X_analysis.json dentro de cada subcarpeta para generar un archivo CSV
    con datos de características (features).

    Args:
        input_folder (str): Ruta principal donde están las carpetas con archivos JSON.
        output_csv_file (str): Archivo CSV de salida.
    """
    # Encabezados para el archivo CSV
    csv_headers = [
        "video_name", 
        "sec", 
        "object_name", 
        "description", 
        "color1", 
        "color2", 
        "size", 
        "orientation", 
        "type"
    ]

    # Lista para almacenar las filas del CSV
    csv_rows = []

    # Recorrer las carpetas y archivos
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('_analysis.json') and 'collage' in file:
                json_path = os.path.join(root, file)
                
                # Extraer video_name y segundo
                video_name = os.path.basename(root)
                sec = int(file.split('_')[1])  # Extraer segundo del nombre del archivo
                
                try:
                    # Leer el archivo JSON
                    with open(json_path, 'r') as f_json:
                        data = json.load(f_json)
                    
                    detections = data.get('detections', [])
                    
                    # Procesar cada detección
                    for detection in detections:
                        object_name = detection.get('object_name', 'unknown')
                        description = detection.get('description', 'No description')
                        features = detection.get('features', {})
                        
                        color1 = features.get('color1', 'unknown')
                        color2 = features.get('color2', 'unknown')
                        size = features.get('size', 'unknown')
                        orientation = features.get('orientation', 'unknown')
                        obj_type = features.get('type', 'unknown')
                        
                        # Agregar la fila al CSV
                        csv_rows.append([
                            video_name, 
                            sec, 
                            object_name, 
                            description, 
                            color1, 
                            color2, 
                            size, 
                            orientation, 
                            obj_type
                        ])
                except Exception as e:
                    print(f"Error procesando el archivo {json_path}: {e}")

    # Guardar los datos en un archivo CSV
    if csv_rows:
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            # Escribir los encabezados
            writer.writerow(csv_headers)
            # Escribir las filas
            writer.writerows(csv_rows)
        print(f"Archivo CSV generado correctamente en '{output_csv_file}'.")
    else:
        print("No se encontraron datos para exportar.")

# Ejemplo de uso
input_folder = 'detections'
output_csv_file = 'features_data.csv'
process_features_to_csv(input_folder, output_csv_file)
print(f"Archivo CSV generado: {output_csv_file}")
