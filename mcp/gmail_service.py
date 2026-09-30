import os
from django.conf import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from datetime import timezone

class GmailClient:
    """Simple wrapper for Gmail API using a Django User's stored OAuth tokens.

    The client expects the ``User`` model to have ``google_access_token``,
    ``google_refresh_token`` and ``google_token_expiry`` fields (as defined in
    ``accounts.models.User``).
    """

    def __init__(self, user):
        self.user = user
        self.creds = self._load_credentials()
        if not self.creds or not self.creds.valid:
            raise ValueError("User does not have valid Google credentials")
        self.service = build('gmail', 'v1', credentials=self.creds)

    def _load_credentials(self):
        """Create a ``Credentials`` object from stored tokens.

        If the access token is expired and a refresh token is present, the
        ``Credentials`` object will automatically refresh when a request is made.
        """
        if not self.user.google_access_token:
            return None
        token = self.user.google_access_token
        refresh_token = getattr(self.user, 'google_refresh_token', None)
        expiry = self.user.google_token_expiry
        if expiry:
            expiry = expiry.replace(tzinfo=timezone.utc) if expiry.tzinfo is None else expiry
        creds = Credentials(
            token=token,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
            client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
            scopes=[
                'https://www.googleapis.com/auth/gmail.readonly',
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile',
                'openid',
            ],
            expiry=expiry,
        )
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                self.user.google_access_token = creds.token
                self.user.google_refresh_token = creds.refresh_token
                self.user.google_token_expiry = creds.expiry
                self.user.save()
            except Exception as e:
                raise e
        return creds

    def list_messages(self, query=None, max_results=100):
        """Return a list of message metadata matching the optional Gmail query.

        Parameters
        ----------
        query: str or ``None``
            Gmail search string (e.g. "is:unread"). If ``None`` all messages
            are returned.
        max_results: int
            Maximum number of messages to return.
        """
        result = self.service.users().messages().list(
            userId='me', q=query, maxResults=max_results
        ).execute()
        return result.get('messages', [])

    def get_message(self, message_id, format='full'):
        """Retrieve a single message by its Gmail ID.

        ``format`` can be 'full', 'metadata', 'minimal' or 'raw'.
        """
        message = self.service.users().messages().get(
            userId='me', id=message_id, format=format
        ).execute()
        return message

    def list_attachments(self, message_id):
        """Return a list of attachment IDs for a given message.

        The returned list contains dictionaries with 'filename' and 'attachmentId'.
        """
        message = self.get_message(message_id, format='full')
        parts = message.get('payload', {}).get('parts', [])
        attachments = []
        for part in parts:
            if part.get('filename') and part.get('body', {}).get('attachmentId'):
                attachments.append({
                    'filename': part['filename'],
                    'attachmentId': part['body']['attachmentId'],
                })
        return attachments
