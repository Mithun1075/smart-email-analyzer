from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_index, name='index'),
    path('api/send_message/', views.send_message, name='send_message'),
    path('api/clear_chat/', views.clear_chat, name='clear_chat'),
    path('api/upload_document/', views.upload_document, name='upload_document'),
    path('api/clear_document/', views.clear_document, name='clear_document'),
]
