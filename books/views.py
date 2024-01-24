from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book, ViewBook
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
def add_books(request):
    if request.method == "GET":
        books = Book.objects.filter(user=request.user)

        total_views = ViewBook.objects.filter(book__user=request.user).count()

        return render(request, 'add_books.html', {'books': books, 'total_views': total_views})
    elif request.method == "POST":
        title = request.POST.get('title')
        file = request.FILES['file']
        
        book = Book(
            user=request.user,
            title=title,
            file=file
        )

        book.save()
        messages.add_message(request, constants.SUCCESS, 'Salvo com sucesso.')
        return redirect('/books/add_books')
    
def book(request, id):
    book = Book.objects.get(id=id)
    totals_views = ViewBook.objects.filter(book=book).count()
    unique_views = ViewBook.objects.filter(book=book).values('ip').distinct().count()
    
    view = ViewBook(
        ip=request.META['REMOTE_ADDR'],
        book=book
    )
    view.save()
    return render(request, 'book.html', {'book': book, 'totals_views': totals_views, 'unique_views': unique_views})