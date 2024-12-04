import os
import re
import csv

# Ruta de la carpeta detections
detections_folder = "detections"

# Archivo de salida para el archivo CSV
output_csv_file = "objects_data.csv"

# Encabezados para el archivo CSV (orden según la tabla)
csv_headers = [
    "object_name", 
    "video_name", 
    "x1", 
    "y1", 
    "x2", 
    "y2", 
    "rgb_color", 
    "proximity", 
    "sec"
]

# Expresión regular para extraer los campos (incluido rgb_color con comas internas)
line_pattern = re.compile(r"([a-zA-Z\s]+),(\d+),(\d+),(\d+),(\d+),\((\d+,\s*\d+,\s*\d+)\),(\w+),(\d+)")

# Lista para almacenar las filas del CSV
csv_rows = []

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
                            x1 = int(match.group(2).strip())
                            y1 = int(match.group(3).strip())
                            x2 = int(match.group(4).strip())
                            y2 = int(match.group(5).strip())
                            rgb_color = match.group(6).strip()  # rgb_color con las comas internas
                            proximity = match.group(7).strip()
                            sec = int(match.group(8).strip())

                            # Agrega la fila al CSV en el orden definido en la tabla
                            csv_rows.append([
                                object_name, 
                                video_folder,  # Nombre del video
                                x1, 
                                y1, 
                                x2, 
                                y2, 
                                rgb_color, 
                                proximity, 
                                sec
                            ])
                        else:
                            print(f"  ERROR: Línea no válida en {txt_file}: {line}")

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
