from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from mcp.gmail_service import GmailClient

@login_required
def inbox_view(request):
    """Display a list of recent Gmail messages for the logged‑in user.

    Optional ``query`` GET parameter can be used to filter messages (e.g.
    ``?query=is:unread`` or ``?query=subject:Python``).
    """
    query = request.GET.get('query')
    client = GmailClient(request.user)
    messages = client.list_messages(query=query, max_results=20)
    # For each message, fetch minimal info (subject, snippet, date).
    message_details = []
    for msg in messages:
        msg_data = client.get_message(msg['id'], format='metadata')
        headers = {h['name']: h['value'] for h in msg_data.get('payload', {}).get('headers', [])}
        message_details.append({
            'id': msg['id'],
            'subject': headers.get('Subject', '(No Subject)'),
            'from': headers.get('From', ''),
            'date': headers.get('Date', ''),
            'snippet': msg_data.get('snippet', ''),
        })
    return render(request, 'gmail/inbox.html', {
        'messages': message_details,
        'query': query or ''
    })
