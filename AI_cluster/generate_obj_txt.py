import os
import re

# Ruta de la carpeta detections
detections_folder = "detections"

# Archivo de salida para las queries
output_file = "insert_queries.txt"

# Expresión regular para extraer los campos (incluido rgb_color con comas internas)
line_pattern = re.compile(r"([a-zA-Z\s]+),(\d+),(\d+),(\d+),(\d+),\((\d+,\s*\d+,\s*\d+)\),(\w+),(\d+)")

# Abre el archivo para escribir las queries
with open(output_file, "w") as f:
    # Recorre las carpetas dentro de detections
    for video_folder in os.listdir(detections_folder):
        video_folder_path = os.path.join(detections_folder, video_folder)

        # Verifica si es una carpeta
        if os.path.isdir(video_folder_path):
            print(f"Procesando carpeta de video: {video_folder}")
            
            # Recorre los archivos dentro de la carpeta de video
            for txt_file in os.listdir(video_folder_path):
                if txt_file.endswith(".txt"):
                    txt_file_path = os.path.join(video_folder_path, txt_file)
                    print(f"  Procesando archivo: {txt_file}")
                    
                    # Abre el archivo .txt y procesa cada línea
                    with open(txt_file_path, "r") as file:
                        for line in file:
                            line = line.strip()
                            
                            # Intenta hacer match con la expresión regular
                            match = line_pattern.match(line)
                            
                            if match:
                                object_name = match.group(1).strip()
                                x1 = match.group(2).strip()
                                y1 = match.group(3).strip()
                                x2 = match.group(4).strip()
                                y2 = match.group(5).strip()
                                rgb_color = match.group(6).strip()  # rgb_color con las comas internas
                                proximity = match.group(7).strip()
                                sec = match.group(8).strip()

                                # Crea la query de inserción
                                query = f"INSERT INTO objects (object_name, x1, y1, x2, y2, rgb_color, proximity, sec) " \
                                        f"VALUES ('{object_name}', {x1}, {y1}, {x2}, {y2}, '{rgb_color}', '{proximity}', {sec});"
                                
                                # Escribe la query en el archivo de salida
                                f.write(query + "\n")
                            else:
                                print(f"  ERROR: Línea no válida en {txt_file}: {line}")

print("Proceso completado. Las queries han sido generadas en 'insert_queries.txt'.")
