from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Genre, Author, Book, Borrow
from django.http import HttpRequest
from .forms import BorrowForm
from datetime import date, timedelta

def library(request):
    genres = Genre.objects.all()
    selected_genres = request.GET.getlist('genre')

    if selected_genres:
        books = Book.objects.filter(genre__id__in=selected_genres).distinct()
    else:
        books = Book.objects.all()

    return render(request, 'library/library.html', {
        'genres': genres,
        'books': books,
        'selected_genres': selected_genres
    })

def book_detail(request: HttpRequest, pk: int):
    book = get_object_or_404(Book, pk = pk)
    return render(request, 'library/book_detail.html', {
        'book': book
    })

@login_required
def borrow_book(request: HttpRequest, pk: int):
    book = get_object_or_404(Book, pk = pk)
    borrow = Borrow(user = request.user, book = book)

    if request.method == 'POST':
        form = BorrowForm(request.POST, instance=borrow)
        if form.is_valid():
            form.save()
            return redirect('my_borrows')
    else:
        form = BorrowForm(instance = borrow)
    
    return render(request, 'library/borrow_book.html', {
        'book': book,
        "form": form    
        })

def pluralize_days(n):
    n_abs = abs(n)
    if n_abs % 10 == 1 and n_abs % 100 != 11:
        return "день"
    elif 2 <= n_abs % 10 <= 4 and not (12 <= n_abs % 100 <= 14):
        return "дні"
    else:
        return "днів"

@login_required
def my_borrows(request: HttpRequest):
    borrows = Borrow.objects.filter(user=request.user)
    for borrow in borrows:
        end_date = borrow.created_at.date() + timedelta(days=borrow.termin)
        borrow.days_left = (end_date - date.today()).days
        borrow.termin_word = pluralize_days(borrow.termin)
        borrow.days_left_word = pluralize_days(borrow.days_left)
    return render(request, 'library/my_borrows.html', {
        'borrows': borrows
    })

@login_required
def edit_borrow(request: HttpRequest, pk: int):
    borrow = get_object_or_404(Borrow, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BorrowForm(request.POST, instance=borrow)
        if form.is_valid():
            updated_borrow = form.save(commit=False)

            for field in form.fields:
                if form.cleaned_data.get(field) in [None, '']:
                    setattr(updated_borrow, field, getattr(borrow, field))

            updated_borrow.save()
            return redirect('my_borrows')
    else:
        form = BorrowForm(instance=borrow)

    return render(request, 'library/edit_borrow.html', {
        'form': form,
        'borrow': borrow
    })

@login_required
def cancel_borrow(request: HttpRequest, pk: int):
    borrow = get_object_or_404(Borrow, pk=pk, user=request.user)
    if request.method == 'POST':
        borrow.delete()
        return redirect('my_borrows')
    return render(request, 'library/my_borrows.html', {'borrow': borrow})

def author_detail(request: HttpRequest, pk: int):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)

    return render(request, 'library/author_detail.html', {
        'author': author,
        'books': books
    })

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
