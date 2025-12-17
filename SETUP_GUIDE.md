# 0 to 100 Setup Guide: AI Video Agent

This guide covers every step required to get your AI Video Agent up and running, from scratch.

## Step 1: Get the Code
1.  **Clone the repository** to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

## Step 2: Set up the Environment
1.  **Install Python** (version 3.10 or higher is recommended).
2.  (Optional) **Create a Virtual Environment** to keep dependencies isolated:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Step 3: Get Google Gemini API Key (Content Generation)
1.  Go to [Google AI Studio](https://makersuite.google.com/app/apikey).
2.  Click **"Create API Key"**.
3.  Copy the key string.
4.  **Set the Environment Variable**:
    *   **Mac/Linux**:
        ```bash
        export GEMINI_API_KEY="your_copied_api_key"
        ```
    *   **Windows (cmd)**:
        ```cmd
        set GEMINI_API_KEY=your_copied_api_key
        ```
    *   **Windows (PowerShell)**:
        ```powershell
        $env:GEMINI_API_KEY="your_copied_api_key"
        ```

## Step 4: Set up YouTube Data API (Uploading)
1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  **Create a New Project** (e.g., "YouTubeAI-Agent").
3.  **Enable the API**:
    *   Search for "YouTube Data API v3" in the search bar.
    *   Click on it and click **Enable**.
4.  **Configure OAuth Consent Screen**:
    *   Go to **APIs & Services > OAuth consent screen**.
    *   Choose **External** (unless you have a Google Workspace organization).
    *   Fill in required fields (App name, support email).
    *   **Scopes**: Add `../auth/youtube.upload` scope.
    *   **Test Users**: Add the email address of the YouTube channel account you want to upload to. (IMPORTANT: While the app is in "Testing" mode, only added users can use it).
5.  **Create Credentials**:
    *   Go to **APIs & Services > Credentials**.
    *   Click **Create Credentials > OAuth client ID**.
    *   Application type: **Desktop app**.
    *   Name: "YouTube Uploader".
    *   Click **Create**.
6.  **Download JSON**:
    *   Download the JSON file for the Client ID you just created.
    *   **Rename** the file to `client_secret.json`.
    *   **Move** this file to the root folder of the project (same folder as `src` and `requirements.txt`).

## Step 5: Verify Fonts (Linux/Servers only)
*   The script uses a specific font path (`/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`) to work with the video library.
*   If you are on **Windows** or **Mac**, you may need to edit `src/video_creator.py` to point to a valid `.ttf` file on your system (e.g., `C:\Windows\Fonts\Arial.ttf`).

## Step 6: Run the Agent
1.  Start the application:
    ```bash
    python src/main.py
    ```
2.  **First Run Authentication**:
    *   The first time you run it, a browser window will open asking you to log in with your Google account.
    *   Allow the app to manage your YouTube videos.
    *   Once confirmed, the script will save a `token.json` file. Future runs won't need you to log in again.

## Step 7: Operation
*   The script will immediately generate a video and attempt to upload it.
*   It will then go into a waiting loop, checking every minute, and will run again 12 hours after the previous run.
*   Check the terminal output for progress logs ("Generating content...", "Creating video...", "Uploading...").
