import sys

print(f"Received arguments: {sys.argv}")

def scan_videos(video_list):
    print("Scanning videos from backend with Python...")
    for video in video_list:
        print(f"Scanning {video}")

if __name__ == "__main__":
    videos = sys.argv[1:]
    print(f"Videos to scan: {videos}")
    scan_videos(videos)