from django.urls import path
from . import views

urlpatterns = [
    path('new_flashcard/', views.new_flashcard, name='new_flashcard'),
    path('delete_flashcard/<int:id>', views.delete_flashcard, name='delete_flashcard'),
    path('start_challenge/', views.start_challenge, name='start_challenge'),
    path('list_challenge/', views.list_challenge, name='list_challenge'),
    path('challenge/<int:id>/', views.challenge, name='challenge'),
    path('reply_flashcard/<int:id>/', views.reply_flashcard, name='reply_flashcard')
]
