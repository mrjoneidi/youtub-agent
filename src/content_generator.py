import os
import json
import google.generativeai as genai

class ContentGenerator:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Gemini API Key is required.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_content(self):
        """
        Generates a video script and metadata using Gemini.
        Returns a dictionary with title, description, keywords, and script_lines.
        """
        prompt = """
        You are a creative content creator for a YouTube channel about Fun Facts, Movies, and Entertainment.
        Create a short video script (approx 30-60 seconds) for a new video.

        The output must be a valid JSON object with the following structure:
        {
            "title": "The video title",
            "description": "A short video description for YouTube",
            "keywords": ["tag1", "tag2", "tag3"],
            "script_lines": [
                "Line 1 of the script to be spoken.",
                "Line 2...",
                "Line 3..."
            ]
        }

        Ensure the content is engaging, factual, and suitable for a general audience.
        Do not include markdown formatting like ```json or ```. Just the raw JSON string.
        """

        try:
            response = self.model.generate_content(prompt)
            # Clean up potential markdown code blocks if Gemini ignores the instruction
            text_response = response.text.strip()
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            if text_response.startswith("```"):
                text_response = text_response[3:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]

            content_data = json.loads(text_response)
            return content_data
        except Exception as e:
            print(f"Error generating content: {e}")
            return None

if __name__ == "__main__":
    # Test execution
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        generator = ContentGenerator(key)
        print(generator.generate_content())
    else:
        print("Set GEMINI_API_KEY to test.")
