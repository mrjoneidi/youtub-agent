import os
from gtts import gTTS
from moviepy import *
import textwrap

class VideoCreator:
    def __init__(self, output_dir="assets"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def create_video(self, content_data, filename="output_video.mp4"):
        """
        Creates a video from the content data.
        content_data: dict with 'script_lines'
        """
        script_lines = content_data.get("script_lines", [])
        if not script_lines:
            print("No script lines found.")
            return None

        clips = []
        audio_files = []

        # Define some basic colors/styles
        bg_color = (20, 20, 40) # Dark Blue
        text_color = 'white'
        fontsize = 70
        font = 'Arial-Bold' # Assuming ImageMagick can find this, otherwise standard font
        size = (1080, 1920) # YouTube Shorts format (9:16)

        try:
            for i, line in enumerate(script_lines):
                # 1. Generate Audio
                audio_path = os.path.join(self.output_dir, f"segment_{i}.mp3")
                tts = gTTS(text=line, lang='en')
                tts.save(audio_path)
                audio_files.append(audio_path)

                # 2. Create Audio Clip
                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration

                # 3. Create Text Clip (Visual)
                # Wrap text
                wrapped_text = "\n".join(textwrap.wrap(line, width=20))

                # Create a solid background
                color_clip = ColorClip(size=size, color=bg_color).with_duration(duration)

                # Create Text
                # MoviePy v2 compatibility:
                # 1. font must be a path to a file (Pillow requirement).
                # 2. font_size instead of fontsize.
                # 3. method='caption' requires size.

                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
                if not os.path.exists(font_path):
                    # Fallback or let MoviePy/Pillow handle default if None
                    font_path = None
                    print("Warning: Specific font not found, using default.")

                txt_clip = TextClip(
                    text=wrapped_text,
                    font_size=fontsize,
                    color=text_color,
                    font=font_path,
                    size=(size[0]-100, None),
                    method='caption'
                )
                txt_clip = txt_clip.with_position('center').with_duration(duration)

                # Composite
                video_clip = CompositeVideoClip([color_clip, txt_clip])
                video_clip = video_clip.with_audio(audio_clip)

                clips.append(video_clip)

            # Concatenate all clips
            final_clip = concatenate_videoclips(clips)

            output_path = os.path.join(self.output_dir, filename)
            final_clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')

            # Cleanup temporary audio
            for audio_f in audio_files:
                try:
                    os.remove(audio_f)
                except:
                    pass

            return output_path

        except Exception as e:
            print(f"Error creating video: {e}")
            # Cleanup on failure
            for audio_f in audio_files:
                try:
                    os.remove(audio_f)
                except:
                    pass
            return None

if __name__ == "__main__":
    # Test stub
    dummy_data = {
        "script_lines": ["Hello world.", "This is a test video generator.", "It uses simple text overlays."]
    }
    creator = VideoCreator()
    # We won't run it here to avoid ImageMagick dependency issues in this environment immediately
    # print("Video creator initialized.")
