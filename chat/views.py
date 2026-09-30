from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import json
import os
from ai.services import generate_ai_response

@login_required
def chat_index(request):
    """The main AI Chat interface."""
    chat_history = request.session.get('chat_history', [])
    document_name = request.session.get('document_name', None)
    return render(request, 'chat/chat.html', {
        'chat_history': chat_history,
        'document_name': document_name
    })

@login_required
def send_message(request):
    """API endpoint to process a chat message and return AI response."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'error': 'Message is empty'}, status=400)
                
            # Retrieve chat history from session
            chat_history = request.session.get('chat_history', [])
            document_path = request.session.get('document_path', None)
            
            # Generate AI response
            ai_response = generate_ai_response(request.user, user_message, chat_history, document_path)
            
            # Update session history
            chat_history.append({'role': 'user', 'text': user_message})
            chat_history.append({'role': 'model', 'text': ai_response})
            request.session['chat_history'] = chat_history
            request.session.modified = True
            
            return JsonResponse({'response': ai_response})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def clear_chat(request):
    """Clears the chat history in the session."""
    if request.method == 'POST':
        request.session['chat_history'] = []
        return JsonResponse({'status': 'cleared'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def upload_document(request):
    """Handles document uploads for AI analysis."""
    if request.method == 'POST' and request.FILES.get('document'):
        document = request.FILES['document']
        
        # Simple validation
        ext = os.path.splitext(document.name)[1].lower()
        if ext not in ['.pdf', '.docx', '.xlsx', '.csv', '.txt', '.doc', '.xls']:
            return JsonResponse({'error': 'Unsupported file type'}, status=400)
            
        fs = FileSystemStorage(location='media/temp')
        filename = fs.save(document.name, document)
        filepath = fs.path(filename)
        
        request.session['document_path'] = filepath
        request.session['document_name'] = document.name
        
        return JsonResponse({'status': 'success', 'filename': document.name})
        
    return JsonResponse({'error': 'No file uploaded'}, status=400)

@login_required
def clear_document(request):
    """Clears the current document from the session."""
    if request.method == 'POST':
        filepath = request.session.get('document_path')
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass # Ignore if file couldn't be deleted
                
        if 'document_path' in request.session:
            del request.session['document_path']
        if 'document_name' in request.session:
            del request.session['document_name']
            
        return JsonResponse({'status': 'cleared'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
