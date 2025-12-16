import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class YouTubeUploader:
    def __init__(self, client_secrets_file="client_secret.json", token_file="token.json"):
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file
        self.scopes = ["https://www.googleapis.com/auth/youtube.upload"]
        self.youtube = self.authenticate()

    def authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    creds = None

            if not creds:
                if not os.path.exists(self.client_secrets_file):
                    print(f"Client secrets file '{self.client_secrets_file}' not found. Cannot authenticate.")
                    return None

                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, self.scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        try:
            youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
            return youtube
        except Exception as e:
            print(f"Failed to build YouTube resource: {e}")
            return None

    def upload_video(self, file_path, title, description, tags, category_id="24"):
        """
        Uploads a video to YouTube.
        category_id 24 is 'Entertainment'.
        """
        if not self.youtube:
            print("YouTube service not authenticated.")
            return False

        body = {
            "snippet": {
                "title": title[:100], # Max 100 chars
                "description": description[:5000], # Max 5000 chars
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": "public", # or 'private', 'unlisted'
                "selfDeclaredMadeForKids": False
            }
        }

        try:
            media = googleapiclient.http.MediaFileUpload(file_path, chunksize=-1, resumable=True)
            request = self.youtube.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Uploaded {int(status.progress() * 100)}%")

            print(f"Upload Complete! Video ID: {response.get('id')}")
            return True

        except googleapiclient.errors.HttpError as e:
            print(f"An HTTP error occurred: {e.resp.status} {e.content}")
            return False
        except Exception as e:
            print(f"An error occurred during upload: {e}")
            return False
