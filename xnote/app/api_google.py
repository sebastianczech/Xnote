import os.path
import socket

from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .models import Token


# User https://developers.google.com/docs/api/quickstart/python
def api_google_credential():
    credential = None

    # read token from database and save to file
    token_db = Token.objects.get(id=1)
    with open(settings.GOOGLE_OAUTH2_TOKEN_FILE, 'w') as token_file:
        token_file.write(token_db.token)

    # create credentials from file
    if os.path.exists(settings.GOOGLE_OAUTH2_TOKEN_FILE):
        print("Google API read existing token")
        credential = Credentials.from_authorized_user_file(
                settings.GOOGLE_OAUTH2_TOKEN_FILE,
                settings.GOOGLE_OAUTH2_SCOPES)

    # check credentials
    if not credential or not credential.valid:
        if credential and credential.expired and credential.refresh_token:
            # refresh token
            print("Google API is not valid, need refresh")
            credential.refresh(Request())
            print("Google API token refreshed")
        else:
            # run local server to get token
            print("Google API get client secretes")
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
                settings.GOOGLE_OAUTH2_SCOPES)

            print("Google API run local server on " + socket.gethostname())
            credential = flow.run_local_server(host=settings.GOOGLE_OAUTH2_LOCAL_SERVER,
                port=settings.GOOGLE_OAUTH2_LOCAL_SERVER_PORT,
                authorization_prompt_message='Please visit this URL: {url}',
                success_message='The auth flow is complete; you may close this window.',
                open_browser=True)
            print("Google API new token received")

        # save refreshed or new credential to file and database
        with open(settings.GOOGLE_OAUTH2_TOKEN_FILE, 'w') as token_file:
            print("Google API write token to file")
            token_file.write(credential.to_json())

            print("Google API write token to database")
            Token.objects.filter(id=1).update(token=credential.to_json())

    # print(str(credential.to_json()))
    return credential
