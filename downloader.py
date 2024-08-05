import os
from moviepy.editor import VideoFileClip
import subprocess

def download_video(video_url, start_time, end_time, output_path):
    # Download the video using yt-dlp
    video_filename = "downloaded_video.mp4"
    command = ["yt-dlp", "-f", "best", "-o", video_filename, video_url]
    subprocess.run(command, check=True)

    # Trim the video
    clip = VideoFileClip(video_filename).subclip(start_time, end_time)
    clip.write_videofile(output_path)

    # Clean up the downloaded video
    os.remove(video_filename)

# Example usage
download_video('https://www.youtube.com/watch?v=DYiKZX69a-0', start_time=1, end_time=51, output_path='trimmed_video.mp4')
