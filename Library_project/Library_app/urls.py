from django.urls import path
from . import views

urlpatterns = [
    path('', views.library, name = 'library'),
    path('book/<int:pk>/', views.book_detail, name = 'book_detail'),
    path('book/<int:pk>/borrow/', views.borrow_book, name = 'borrow_book'),
    path('my_borrows/', views.my_borrows, name = 'my_borrows'),
    path('borrow/<int:pk>/edit', views.edit_borrow, name = 'edit_borrow'),
    path('borrow/<int:pk>/cancel', views.cancel_borrow, name = 'cancel_borrow'),
    path('author/<int:pk>/', views.author_detail, name = 'author_detail'),
    path('genre/<int:pk>/books', views.genre_books, name = 'genre_books'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
