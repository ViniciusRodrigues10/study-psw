from django.shortcuts import render, redirect
from .models import Category, Flashcard
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
def new_flashcard(request): 
    if not request.user.is_authenticated:
        return redirect('/users/connect')
    
    if request.method == "GET":
        category = Category.objects.all()
        flashcards = Flashcard.objects.filter(user=request.user)

        category_filter = request.GET.get('category')
        difficulty_filter = request.GET.get('difficulty')

        if category_filter:
            flashcards = flashcards.filter(category__id=category_filter)

        if difficulty_filter:
            flashcards = flashcards.filter(difficulty=difficulty_filter)

        return render(request, 'new_flashcard.html', {'category': category, 'difficulties': Flashcard.DIFFICULTY_CHOICES, 'flashcards': flashcards})
    
    elif request.method == "POST":
        question = request.POST.get('question')
        response = request.POST.get('response')
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')

        if len(question.strip()) == 0 or len(response.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                'Preencha os campos de pergunta e resposta',
            )
            return redirect('/flashcard/new_flashcard')
        
        flashcard = Flashcard(
            user=request.user,
            question=question,
            response=response,
            category_id=category,
            difficulty=difficulty,
        )

        flashcard.save()

        messages.add_message(request, constants.SUCCESS, 'Flashcard criado com sucesso')

        return redirect('/flashcard/new_flashcard')