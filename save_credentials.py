import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the SCOPES you need
SCOPES = ['https://www.googleapis.com/auth/gmail.send']  # Add your required scopes here

# Start the OAuth flow to get credentials
def authenticate_gmail():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    try:
        # Attempt to load existing credentials
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    except (FileNotFoundError, EOFError):
        # In case of FileNotFound or empty (EOFError), start the OAuth flow
        pass
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=49904)  # This will trigger the authentication process
        # Save the credentials for the next run
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

# Authenticate and save credentials
creds = authenticate_gmail()

print("Authentication successful and credentials saved!")
