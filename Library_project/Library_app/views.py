from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Genre, Author, Book, Borrow
from django.http import HttpRequest
from .forms import BorrowForm

def library(request: HttpRequest):
    books = Book.objects.filter(available = True)

    return render(request, 'library/library.html', {
        'books': books
    })



def book_detail(request: HttpRequest, pk: int):
    book = get_object_or_404(Book, pk = pk)
    return render(request, 'library/book_detail.html', {
        'book': book
    })

@login_required
def borrow_book(request: HttpRequest, pk: int):
    pass

@login_required
def my_borrows(request: HttpRequest):
    pass

@login_required
def edit_borrow(request: HttpRequest, pk: int):
    pass

@login_required
def cancel_borrow(request: HttpRequest, pk: int):
    pass

def author_detail(request: HttpRequest, pk: int):
    pass

def genre_books(request: HttpRequest):
    pass

def login_view(request: HttpRequest):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            login(request, form.get_user())
            return redirect('library')
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')

def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('library')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
