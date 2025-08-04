from .models import Genre, Author, Book, Borrow
from django.contrib import admin

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Borrow)