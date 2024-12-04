import os
import json

def process_features(input_folder, output_file):
    """
    Procesa archivos collage_X_analysis.json dentro de cada subcarpeta para generar datos
    que se insertarán en la tabla features.

    Args:
        input_folder (str): Ruta principal donde están las carpetas con archivos JSON.
        output_file (str): Archivo de salida donde se guardarán las sentencias INSERT.
    """
    with open(output_file, 'w') as f_out:
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
                            
                            # Escribir la sentencia INSERT
                            insert_query = (
                                f"INSERT INTO features "
                                f"(video_name, sec, object_name, description, color1, color2, size, orientation, type) "
                                f"VALUES ('{video_name}', {sec}, '{object_name}', '{description}', "
                                f"'{color1}', '{color2}', '{size}', '{orientation}', '{obj_type}');\n"
                            )
                            f_out.write(insert_query)
                    except Exception as e:
                        print(f"Error procesando el archivo {json_path}: {e}")

# Ejemplo de uso
input_folder = 'detections'
output_file = 'features_insert.sql'
process_features(input_folder, output_file)
print(f"Archivo de inserciones generado: {output_file}")
