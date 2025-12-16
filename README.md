# AI Video Agent

This project is an automated AI agent that creates and posts short videos to YouTube every 12 hours. It focuses on the "fun, movies, and entertainment" niche.

## Features

-   **Content Generation**: Uses Google's Gemini AI to generate engaging topics, scripts, titles, and descriptions.
-   **Video Creation**: Automatically converts scripts to audio (TTS) and generates a video with text overlays.
-   **YouTube Upload**: Automatically uploads the generated video to a specified YouTube channel.
-   **Scheduling**: Runs on a 12-hour cycle.

## Prerequisites

1.  **Python 3.8+**
2.  **Google Gemini API Key**:
    *   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey).
3.  **YouTube Data API Credentials**:
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a project and enable the **YouTube Data API v3**.
    *   Create **OAuth 2.0 Client IDs** (Desktop App).
    *   Download the JSON file and rename it to `client_secret.json` in the project root.

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You might need to install ImageMagick for MoviePy separately if you are on Windows or if it's not automatically detected.*

## Configuration

Create a `.env` file (or set environment variables) with the following:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

Run the agent:

```bash
python src/main.py
```

The agent will attempt to generate and upload a video immediately, and then schedule the next run for 12 hours later.

## Directory Structure

-   `src/`: Source code.
-   `assets/`: Storage for generated media (can be cleared periodically).
-   `client_secret.json`: Your YouTube OAuth credentials (not included).
