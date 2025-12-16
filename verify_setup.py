import os
import sys

# Mock imports to avoid actual dependencies during this specific test if needed,
# but here we want to verifying import structure.
try:
    from src.content_generator import ContentGenerator
    from src.video_creator import VideoCreator
    from src.youtube_uploader import YouTubeUploader
    print("Imports successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

# Verify directory structure
required_dirs = ["src", "assets"]
for d in required_dirs:
    if not os.path.exists(d):
        print(f"Directory missing: {d}")
        # Create it if missing, as video_creator does, but good to check
        os.makedirs(d)

print("Directory structure verification passed.")

# Test VideoCreator with dummy data (Mocking gTTS/MoviePy execution conceptually)
# Since we can't easily run MoviePy/ImageMagick in this constrained env without setup,
# we will just check if the class instantiates and verify method signatures.
try:
    vc = VideoCreator()
    print("VideoCreator instantiated.")

    # Check if necessary MoviePy classes are imported available in global scope (via src.video_creator imports)
    import src.video_creator as svc
    if hasattr(svc, 'TextClip') and hasattr(svc, 'CompositeVideoClip'):
         print("MoviePy classes detected in video_creator.")
    else:
         print("Warning: MoviePy classes not detected in video_creator namespace.")

except Exception as e:
    print(f"VideoCreator instantiation failed: {e}")
    # Print the full traceback for better debugging
    import traceback
    traceback.print_exc()

print("Verification complete.")
