import cv2
import numpy as np
import os
import glob
from .gpt_detector import detect_scene, detect_objects  # Importar funciones del archivo gpt_detector.py
from .yolo_detection import save_frame_and_detections

def process_motion(video_path, output_folder):
    capture = cv2.VideoCapture(video_path)
    prev_frame = None
    motion_per_second = []
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0
    elapsed_seconds = 0
    registered_peaks = []

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    video_folder = os.path.join(output_folder, video_name)

    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    # Procesar detección de movimiento
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        diff = cv2.absdiff(prev_frame, gray)
        _, thresh = cv2.threshold(diff, 80, 255, cv2.THRESH_BINARY)
        motion = np.sum(thresh)

        if frame_count % fps == 0:
            elapsed_seconds += 1
            motion_per_second.append(motion)

            if motion > np.mean(motion_per_second) and (not registered_peaks or (elapsed_seconds - registered_peaks[-1] >= 10)):
                registered_peaks.append(elapsed_seconds)
                save_frame_and_detections(frame, elapsed_seconds, video_folder)

        prev_frame = gray

    # Guardar el frame central como "escenario"
    center_frame_index = total_frames // 2
    center_second = center_frame_index // fps  # Calcula el segundo correspondiente al frame central
    capture.set(cv2.CAP_PROP_POS_FRAMES, center_frame_index)
    ret, scenario_frame = capture.read()
    if ret:
        escenario_path = os.path.join(video_folder, "escenario.jpg")
        cv2.imwrite(escenario_path, scenario_frame)  # Guardar el frame directamente como JPG

    # Lógica original para guardar "middle" si no hay picos
    if not registered_peaks:
        center_frame_index = total_frames // 2
        capture.set(cv2.CAP_PROP_POS_FRAMES, center_frame_index)
        ret, center_frame = capture.read()
        if ret:
            save_frame_and_detections(center_frame, center_second, video_folder)  # Usa el segundo central como etiqueta

    capture.release()

    # Analizar el escenario
    escenario_path = os.path.join(video_folder, "escenario.jpg")
    if os.path.exists(escenario_path):
        print("Analizando escenario...")
        scene_analysis = detect_scene(escenario_path)
        with open(os.path.join(video_folder, "escenario_analysis.json"), "w") as f:
            f.write(scene_analysis)
        print("Análisis del escenario guardado.")

    # Analizar collages
    collage_files = glob.glob(os.path.join(video_folder, "collage_*.png"))
    for collage_path in collage_files:
        print(f"Analizando collage: {collage_path}...")
        object_analysis = detect_objects(collage_path)
        collage_name = os.path.splitext(os.path.basename(collage_path))[0]
        with open(os.path.join(video_folder, f"{collage_name}_analysis.json"), "w") as f:
            f.write(object_analysis)
        print(f"Análisis del collage {collage_name} guardado.")
