from django.urls import path
from . import views

urlpatterns = [
    path('new_flashcard/', views.new_flashcard, name='new_flashcard'),
    path('delete_flashcard/<int:id>', views.delete_flashcard, name='delete_flashcard')
]
