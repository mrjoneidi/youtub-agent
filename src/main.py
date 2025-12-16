import time
import schedule
import os
import sys
from datetime import datetime

# Add src to path if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.content_generator import ContentGenerator
from src.video_creator import VideoCreator
from src.youtube_uploader import YouTubeUploader

def job():
    print(f"[{datetime.now()}] Starting Job...")

    # 1. Configuration
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return

    # 2. Generate Content
    print("Generating content...")
    generator = ContentGenerator(gemini_key)
    content = generator.generate_content()

    if not content:
        print("Failed to generate content. Aborting job.")
        return

    print(f"Title: {content.get('title')}")

    # 3. Create Video
    print("Creating video...")
    creator = VideoCreator()
    video_path = creator.create_video(content, filename=f"video_{int(time.time())}.mp4")

    if not video_path:
        print("Failed to create video. Aborting job.")
        return

    print(f"Video created at: {video_path}")

    # 4. Upload to YouTube
    print("Uploading to YouTube...")
    # Note: This expects client_secret.json to be present for the first run
    uploader = YouTubeUploader()
    if uploader.youtube:
        success = uploader.upload_video(
            video_path,
            title=content.get("title", "Untitled Video"),
            description=content.get("description", "No description"),
            tags=content.get("keywords", [])
        )
        if success:
            print("Video uploaded successfully!")
        else:
            print("Video upload failed.")
    else:
        print("YouTube Uploader not initialized (check credentials). Skipping upload.")

    print(f"[{datetime.now()}] Job Finished.")

def run_scheduler():
    print("AI Agent Started. Scheduling jobs every 12 hours.")

    # Run once immediately for demonstration/initialization?
    # Or just wait. Let's run once immediately to ensure it works,
    # then schedule.
    job()

    schedule.every(12).hours.do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # If passed a flag --run-once, just run the job and exit
    if "--run-once" in sys.argv:
        job()
    else:
        run_scheduler()
