import sys
from src.video_processor import process_videos_in_folder

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: scanner.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    print(f"Scanning videos in folder: {input_folder}")
    print(f"Results will be saved in folder: {output_folder}")
    
    try:
        process_videos_in_folder(input_folder, output_folder)
        print("Video scanning completed successfully.")
    except Exception as e:
        print(f"Error during video scanning: {e}")
        sys.exit(1)
