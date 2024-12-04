import cv2
import numpy as np
from ultralytics import YOLO


COLOR_NAMES = [
    ("red", (255, 0, 0)),
    ("green", (0, 255, 0)),
    ("blue", (0, 0, 255)),
    ("yellow", (255, 255, 0)),
    ("cyan", (0, 255, 255)),
    ("magenta", (255, 0, 255)),
    ("black", (0, 0, 0)),
    ("white", (255, 255, 255)),
    ("gray", (128, 128, 128)),
    ("orange", (255, 165, 0)),
    ("pink", (255, 192, 203)),
    ("purple", (128, 0, 128)),
    ("brown", (165, 42, 42)),
    ("lime", (191, 255, 0)),
    ("teal", (0, 128, 128)),
    ("olive", (128, 128, 0)),
    ("navy", (0, 0, 128)),
    ("maroon", (128, 0, 0)),
    ("gold", (255, 215, 0)),
    ("silver", (192, 192, 192))
]

def rgb_to_color_name(rgb):
    """
    Encuentra el nombre del color más cercano en la lista de colores.
    """
    min_distance = float("inf")
    closest_color = None
    for name, color_rgb in COLOR_NAMES:
        distance = np.linalg.norm(np.array(rgb) - np.array(color_rgb))  # Distancia euclidiana
        if distance < min_distance:
            min_distance = distance
            closest_color = name
    return closest_color

def get_object_color(frame, mask):
    """
    Obtiene el color dominante en la región delimitada por la máscara como un nombre de color.
    """
    object_region = cv2.bitwise_and(frame, frame, mask=mask)
    object_hsv = cv2.cvtColor(object_region, cv2.COLOR_BGR2HSV)

    # Extraer los canales H, S, y V
    h_channel = object_hsv[:, :, 0]
    s_channel = object_hsv[:, :, 1]
    v_channel = object_hsv[:, :, 2]

    # Aplicar la máscara para considerar solo los píxeles de la región del objeto
    h_values = h_channel[mask > 0]
    s_values = s_channel[mask > 0]
    v_values = v_channel[mask > 0]

    # Calcular la mediana de cada canal
    median_hue = np.median(h_values)
    median_saturation = np.median(s_values)
    median_value = np.median(v_values)

    # Convertir el color dominante a BGR
    dominant_color_bgr = cv2.cvtColor(np.uint8([[[median_hue, median_saturation, median_value]]]), cv2.COLOR_HSV2BGR)[0][0]

    # Convertir a nombre de color
    dominant_color_name = rgb_to_color_name(dominant_color_bgr)

    return dominant_color_name
def classify_depth(y, height):
    """
    Clasifica la profundidad de un objeto basado en su posición vertical (y) en la imagen.
    """
    third = height // 3
    if y < third:
        return "far"
    elif y < 2 * third:
        return "middle"
    else:
        return "near"

def create_collage(objects, collage_size=(800, 800), max_width=150, max_height=150):
    """
    Crea un collage con las imágenes de los objetos (personas y vehículos) y los coloca en una imagen blanca de 800x800.
    Los objetos se insertan de izquierda a derecha y de arriba a abajo hasta llenar el collage.
    """
    collage = np.ones((collage_size[1], collage_size[0], 3), dtype=np.uint8) * 255  # Imagen blanca de 800x800
    current_x, current_y = 10, 10  # Empieza en la esquina superior izquierda

    for obj_img in objects:
        try:
            # Verificar si la imagen es de 3 canales (RGB/BGR)
            if len(obj_img.shape) == 2:  # Si es una imagen en escala de grises
                obj_img = cv2.cvtColor(obj_img, cv2.COLOR_GRAY2BGR)

            # Redimensionar la imagen para ajustarla al collage
            object_crop_resized = cv2.resize(obj_img, (max_width, max_height), interpolation=cv2.INTER_LINEAR)

            # Verificar si hay espacio suficiente para agregar la imagen
            obj_h, obj_w = object_crop_resized.shape[:2]
            if current_x + obj_w > collage_size[0]:
                current_x = 10
                current_y += obj_h + 10  # Mover a la siguiente línea
            if current_y + obj_h > collage_size[1]:
                break  # No cabe más en la imagen

            collage[current_y:current_y + obj_h, current_x:current_x + obj_w] = object_crop_resized
            current_x += obj_w + 10  # Mover a la siguiente posición horizontal

        except Exception as e:
            print(f"Error al agregar el objeto al collage: {e}")
            continue

    return collage

def save_frame_and_detections(frame, second, output_folder):
    """
    Procesa un cuadro de video, realiza detecciones de objetos con YOLO y árboles,
    y guarda los resultados en un archivo de imagen y un archivo de texto.
    """
    original_height, original_width = frame.shape[:2]

    try:
        # Redimensionar la imagen al tamaño esperado por YOLO (640x640 por defecto)
        input_size = 640
        frame_resized = cv2.resize(frame, (input_size, input_size))

        # Cargar el modelo YOLO
        model = YOLO('yolov8x-seg.pt')  # Cambiar según el modelo disponible
        results = model(frame_resized)
    except Exception as e:
        print(f"Error al procesar el cuadro de video o cargar el modelo: {e}")
        return

    detections = []

    persons = []
    vehicles = []

    try:
        # Detección de árboles (basada en el color verde)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([20, 70, 40])
        upper_green = np.array([85, 255, 255])
        mask = cv2.inRange(frame_hsv, lower_green, upper_green)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                tree_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
                cv2.drawContours(tree_mask, [contour], -1, 255, thickness=cv2.FILLED)
                dominant_color = get_object_color(frame, tree_mask)
                x, y, w, h = cv2.boundingRect(contour)
                # Clasificar la profundidad
                depth = classify_depth(y, original_height)
                detections.append(f"tree,{x},{y},{w},{h},{dominant_color},{depth},{second}")
    except Exception as e:
        print(f"Error al detectar árboles: {e}")

    try:
        # Detección de objetos con YOLO (con segmentación)
        for result in results:
            boxes = result.boxes  # Coordenadas de las cajas delimitadoras
            masks = result.masks  # Máscaras segmentadas

            if masks is not None:
                for mask, box in zip(masks.data, boxes):
                    try:
                        # Asegurarse de que la máscara tenga el tipo correcto
                        mask_binaria = (mask.cpu().numpy() * 255).astype(np.uint8)

                        # Asegurarse de que la máscara tenga las dimensiones correctas
                        mask_resized = cv2.resize(mask_binaria, (original_width, original_height), interpolation=cv2.INTER_NEAREST)

                        # Ajustar las coordenadas del cuadro delimitador a la escala original
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        x1 = int(x1 * (original_width / input_size))
                        y1 = int(y1 * (original_height / input_size))
                        x2 = int(x2 * (original_width / input_size))
                        y2 = int(y2 * (original_height / input_size))

                        # Clasificar profundidad
                        depth = classify_depth(y1, original_height)

                        # Guardar la información del objeto sin dibujar los recuadros
                        label = result.names[int(box.cls)]
                        dominant_color = get_object_color(frame, mask_resized)  # Obtener color dominante del objeto
                        detections.append(f"{label},{x1},{y1},{x2},{y2},{dominant_color},{depth},{second}")

                        # Clasificar objetos y guardarlos en las listas correspondientes
                        if label == "person":
                            persons.append(frame[y1:y2, x1:x2])  # Recorte de la región
                        elif label in ["car", "motorbike", "bus", "bicycle"]:
                            vehicles.append(frame[y1:y2, x1:x2])  # Recorte de la región
                    except Exception as e:
                        print(f"Error al procesar una máscara: {e}")
                        continue
    except Exception as e:
        print(f"Error al detectar objetos con YOLO: {e}")

    try:
        if persons or vehicles:
            all_objects = persons + vehicles
            collage = create_collage(all_objects)

            # Guardar el collage generado
            collage_path = f"{output_folder}/collage_{second}.png"
            cv2.imwrite(collage_path, collage)
        else:
            print(f"No se detectaron personas ni vehículos en el frame {second}. No se creó collage.")
    except Exception as e:
        print(f"Error al crear el collage: {e}")

    try:
        # Guardar la imagen con las detecciones (sin los recuadros, solo con las detecciones)
        detected_frame_path = f"{output_folder}/detected_{second}.png"
        cv2.imwrite(detected_frame_path, frame)
    except Exception as e:
        print(f"Error al guardar la imagen con las detecciones: {e}")

    try:
        # Guardar las detecciones en un archivo de texto
        txt_path = f"{output_folder}/detections_{second}.txt"
        with open(txt_path, "w") as f:
            for detection in detections:
                f.write(detection + "\n")
    except Exception as e:
        print(f"Error al guardar las detecciones en archivo de texto: {e}")
