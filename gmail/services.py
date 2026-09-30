import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from django.conf import settings

def get_gmail_service(user):
    creds = Credentials(
        token=user.google_access_token,
        refresh_token=user.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
        client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
    )
    service = build('gmail', 'v1', credentials=creds)
    return service

import io
import PyPDF2

def _parse_parts(service, email_id, parts):
    """Helper to parse email body parts and extract text/attachments."""
    body = ""
    attachments = []
    
    if not parts:
        return body, attachments
        
    for part in parts:
        mime_type = part.get('mimeType')
        filename = part.get('filename')
        body_data = part.get('body', {}).get('data')
        attachment_id = part.get('body', {}).get('attachmentId')
        
        if filename and attachment_id:
            attachments.append(filename)
            # Extract text from PDF attachments
            if filename.lower().endswith('.pdf'):
                try:
                    att = service.users().messages().attachments().get(
                        userId='me', messageId=email_id, id=attachment_id
                    ).execute()
                    file_data = base64.urlsafe_b64decode(att['data'])
                    
                    reader = PyPDF2.PdfReader(io.BytesIO(file_data))
                    pdf_text = ""
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            pdf_text += extracted + "\n"
                            
                    if pdf_text:
                        body += f"\n\n--- Attachment: {filename} ---\n{pdf_text}\n--- End of Attachment ---\n"
                except Exception as e:
                    body += f"\n\n[Error reading attachment {filename}: {str(e)}]\n"
            # Extract text from Word attachments
            elif filename.lower().endswith(('.docx', '.doc')):
                try:
                    att = service.users().messages().attachments().get(
                        userId='me', messageId=email_id, id=attachment_id
                    ).execute()
                    file_data = base64.urlsafe_b64decode(att['data'])
                    
                    import docx
                    doc = docx.Document(io.BytesIO(file_data))
                    docx_text = "\n".join([para.text for para in doc.paragraphs])
                    
                    if docx_text:
                        body += f"\n\n--- Attachment: {filename} ---\n{docx_text}\n--- End of Attachment ---\n"
                except Exception as e:
                    body += f"\n\n[Error reading attachment {filename}: {str(e)}]\n"
            # Extract data from Excel and CSV attachments
            elif filename.lower().endswith(('.xlsx', '.xls', '.csv')):
                try:
                    att = service.users().messages().attachments().get(
                        userId='me', messageId=email_id, id=attachment_id
                    ).execute()
                    file_data = base64.urlsafe_b64decode(att['data'])
                    
                    import pandas as pd
                    if filename.lower().endswith('.csv'):
                        df = pd.read_csv(io.BytesIO(file_data))
                    else:
                        df = pd.read_excel(io.BytesIO(file_data))
                        
                    excel_text = df.to_string()
                    if excel_text:
                        body += f"\n\n--- Attachment: {filename} ---\n{excel_text}\n--- End of Attachment ---\n"
                except Exception as e:
                    body += f"\n\n[Error reading attachment {filename}: {str(e)}]\n"
        elif mime_type == 'text/plain' and body_data:
            body += base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
        elif part.get('parts'):
            sub_body, sub_atts = _parse_parts(service, email_id, part['parts'])
            body += sub_body
            attachments.extend(sub_atts)
            
    return body, attachments

def search_gmail(user, query, max_results=10):
    """Executes a search query on Gmail and returns a list of summary data."""
    service = get_gmail_service(user)
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        email_summaries = []
        for msg in messages:
            # Get full message to extract headers (Subject, From, To, Date)
            full_msg = service.users().messages().get(
                userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject', 'From', 'To', 'Date']
            ).execute()
            headers = full_msg.get('payload', {}).get('headers', [])
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            recipient = next((h['value'] for h in headers if h['name'] == 'To'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
            
            email_summaries.append({
                'id': msg['id'],
                'subject': subject,
                'sender': sender,
                'recipient': recipient,
                'date': date,
                'snippet': full_msg.get('snippet', '')
            })
            
        return email_summaries
    except Exception as e:
        return {"error": str(e)}

def count_gmail(user, query):
    """Executes a search query and returns the total count."""
    service = get_gmail_service(user)
    try:
        clean_query = query.strip().lower() if query else ""
        if not clean_query or clean_query in ['inbox', 'label:inbox', 'in:inbox']:
            inbox_info = service.users().labels().get(userId='me', id='INBOX').execute()
            return {
                "count": inbox_info.get('messagesTotal', 0),
                "unread": inbox_info.get('messagesUnread', 0)
            }
        elif clean_query == 'is:unread':
            inbox_info = service.users().labels().get(userId='me', id='INBOX').execute()
            return {"count": inbox_info.get('messagesUnread', 0)}
        
        results = service.users().messages().list(userId='me', q=query, maxResults=500).execute()
        messages = results.get('messages', [])
        estimate = results.get('resultSizeEstimate', len(messages))
        return {"count": max(len(messages), estimate)}
    except Exception as e:
        return {"error": str(e)}

def get_email_details(user, email_id):
    """Fetches the full details of a specific email."""
    service = get_gmail_service(user)
    try:
        full_msg = service.users().messages().get(userId='me', id=email_id, format='full').execute()
        payload = full_msg.get('payload', {})
        headers = payload.get('headers', [])
        
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
        
        body, attachments = _parse_parts(service, email_id, payload.get('parts', []))
        
        # If no parts, check payload body directly
        if not body and payload.get('body', {}).get('data'):
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
            
        return {
            'id': email_id,
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': body[:4000], # Truncate very long bodies to save AI context window
            'attachments': attachments
        }
    except Exception as e:
        return {"error": str(e)}
