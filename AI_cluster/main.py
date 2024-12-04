from src.video_processor import process_videos_in_folder

if __name__ == "__main__":
    input_folder = "/home/name/Videos"
    output_folder = "./detections"
    process_videos_in_folder(input_folder, output_folder)
