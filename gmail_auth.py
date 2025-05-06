import os
import pickle
import json
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GMAIL_REDIRECT_URI")
SCOPES = [os.getenv("GMAIL_SCOPES")]

def create_credentials_json():
    credentials_data = {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uris": [REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    with open("credentials_temp.json", "w") as f:
        json.dump(credentials_data, f)

def get_gmail_service():
    creds = None

    # Save dynamic credentials from .env into a temporary file
    create_credentials_json()

    # Use token.json if already authenticated
    if os.path.exists("token.json"):
        with open("token.json", "rb") as token:
            creds = pickle.load(token)

    # If no valid creds, do the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials_temp.json", SCOPES)
            creds = flow.run_local_server(port=49904)  # Make sure 8080 is in your redirect URIs

        # Save credentials for next time
        with open("token.json", "wb") as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

if __name__ == "__main__":
    service = get_gmail_service()
    print("✅ Gmail API authenticated and ready.")
