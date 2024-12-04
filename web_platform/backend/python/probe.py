from ultralytics import YOLO
import cv2
import numpy as np

# Cargar el modelo YOLOv8 en modo segmentación
modelo = YOLO('yolov8x-seg.pt')  # Cambiar a 'yolov8n-seg.pt' para modelos más ligeros

# Cargar la imagen
ruta_imagen = '/home/name/bigdata/proyecto_final/datos2.png'
imagen = cv2.imread(ruta_imagen)

# Redimensionar la imagen al tamaño esperado por YOLO (640x640 por defecto)
input_size = 640  # Asegúrate de usar el tamaño configurado en el modelo
imagen_redimensionada = cv2.resize(imagen, (input_size, input_size))

# Ejecutar detección con segmentación
resultados = modelo(imagen_redimensionada)

# Iterar sobre las detecciones
contador = 0
for resultado in resultados:
    boxes = resultado.boxes  # Coordenadas de las cajas delimitadoras
    masks = resultado.masks  # Máscaras segmentadas

    if masks is not None:  # Verificar si hay máscaras
        for mask in masks.data:
            # Convertir la máscara a formato binario
            mask_binaria = (mask.cpu().numpy() * 255).astype(np.uint8)

            # Encontrar los contornos de la máscara
            contornos, _ = cv2.findContours(mask_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Dibujar los contornos sobre la imagen redimensionada
            color_contorno = (0, 255, 0)  # Color verde para los contornos
            grosor = 2  # Grosor del contorno
            cv2.drawContours(imagen_redimensionada, contornos, -1, color_contorno, grosor)

            contador += 1

# Guardar la imagen redimensionada con los bordes pintados
ruta_salida = 'resultado_con_bordes_redimensionado.png'
cv2.imwrite(ruta_salida, imagen_redimensionada)
print(f'Imagen con bordes guardada como: {ruta_salida}')
