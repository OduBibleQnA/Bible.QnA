import os
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    'https://www.googleapis.com/auth/youtube.readonly',  # Add this!
    "openid",
]

def get_youtube_flow():
    redirect_uri = os.environ.get('GOOGLE_OAUTH_REDIRECT_URI_DEV') if settings.DEBUG else \
                   os.environ.get('GOOGLE_OAUTH_REDIRECT_URI_PROD')
    
    return Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri],
            }
        },
        scopes=[
            
        ],
        redirect_uri=redirect_uri,
    )

def get_credentials_from_session(session):
    if "google_credentials" not in session:
        return None
    return Credentials(**session["google_credentials"])

def store_credentials_in_session(session, creds):
    session["google_credentials"] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }
