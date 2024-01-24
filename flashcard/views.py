from django.shortcuts import render, redirect
from .models import Category, Flashcard, Challenge, FlashcardChallenge
from django.http import HttpResponse, Http404
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
    
def delete_flashcard(request, id):
    flashcard = Flashcard.objects.get(id=id)
    flashcard.delete()
    messages.add_message(
        request, constants.SUCCESS, 'Flashcard deletado com sucesso!'
    )
    return redirect('/flashcard/new_flashcard/')

def start_challenge(request):
    if request.method == "GET":
        category = Category.objects.all()
        return render(request, 'start_challenge.html', {'category': category, 'difficulty': Flashcard.DIFFICULTY_CHOICES})
    
    elif request.method == 'POST':
        title = request.POST.get('title')
        categories = request.POST.getlist('category')
        difficulty = request.POST.get('difficulty')
        qty_questions = request.POST.get('qty_questions')

        challenge = Challenge(
            user=request.user,
            title=title,
            quantity_questions=qty_questions,
            difficulty=difficulty
        )

        challenge.save()

        challenge.category.add(*categories)

        flashcard = (
            Flashcard.objects.filter(user=request.user)
            .filter(difficulty=difficulty)
            .filter(category_id__in=categories)
            .order_by('?')
        )

        if flashcard.count() <  int(qty_questions):
            # Tratar mandar menssagem de erro
            return redirect('/flashcard/start_challenge/')

        flashcard = flashcard[:int(qty_questions)]
        
        for f in flashcard:
            flashcard_challenge = FlashcardChallenge(
                flashcard=f
            )
            flashcard_challenge.save()
            challenge.flashcards.add(flashcard_challenge)
        
        challenge.save()

        return redirect('/flashcard/list_challenge')
def list_challenge(request):
    challenges = Challenge.objects.filter(user=request.user)
    #TODO: develop status
    #TODO: develop filter
    return render(request, 'list_challenge.html',{'challenges': challenges})

def challenge(request, id):
    challenge = Challenge.objects.get(id=id)

    if not challenge.user == request.user:
        raise Http404
    
    if request.method == "GET":
        right = challenge.flashcards.filter(answered=True).filter(right=True).count()
        errors = challenge.flashcards.filter(answered=True).filter(right=False).count()
        missing = challenge.flashcards.filter(answered=False).count()
        return render(request, 'challenge.html', {'challenge': challenge, 'right': right, 'errors': errors, 'missing': missing})

def reply_flashcard(request, id):
    flashcard_challenge = FlashcardChallenge.objects.get(id=id)
    right = request.GET.get('right')
    challenge_id = request.GET.get('challenge_id')

    if not flashcard_challenge.flashcard.user == request.user:
        raise Http404()

    flashcard_challenge.answered = True

    flashcard_challenge.right = True if right == "1" else False
    flashcard_challenge.save()

    return redirect(f'/flashcard/challenge/{challenge_id}')

def report(request, id):
    challenge = Challenge.objects.get(id=id)

    hits = challenge.flashcards.filter(right=True).count()
    errors = challenge.flashcards.filter(right=False).count()
    
    data = [hits, errors]

    return render(request, 'report.html', {'challenge': challenge, 'data': data})