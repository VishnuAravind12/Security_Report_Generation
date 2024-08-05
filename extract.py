import cv2
import os

def extract_frames_at_intervals(video_path, output_folder, interval=5):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get frames per second
    frame_interval = int(fps * interval)  # Calculate frame interval

    frame_id = 0
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{count:05d}.jpg")
            cv2.imwrite(frame_filename, frame)
            count += 1
        frame_id += 1

    cap.release()
    print(f"Extracted {count} frames to {output_folder}")

# Example usage
extract_frames_at_intervals('trimmed_video.mp4', 'frames', interval=5)
