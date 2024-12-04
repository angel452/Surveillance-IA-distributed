import os
from concurrent.futures import ThreadPoolExecutor
from .motion_detection import process_motion
from .yolo_detection import save_frame_and_detections

def process_video(video_path, output_folder):
    process_motion(video_path, output_folder)

def process_videos_in_folder(input_folder, output_folder):
    videos = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.mov'))]

    with ThreadPoolExecutor() as executor:
        executor.map(lambda video: process_video(os.path.join(input_folder, video), output_folder), videos)
