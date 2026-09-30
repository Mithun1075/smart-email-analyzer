from django.urls import path
from . import views

app_name = 'gmail'

urlpatterns = [
    path('inbox/', views.inbox_view, name='inbox'),
]
