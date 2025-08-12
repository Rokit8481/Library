from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Genre(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"

class Author(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    biography = models.CharField(max_length = 800, blank = True, null = True, default = "Біографія відсутня")
    photo = models.ImageField(upload_to = 'media/')
    birth_date = models.DateField(blank = False, null = False)
    death_date = models.DateField(blank = True, null = True, default = None)
    genre = models.ManyToManyField(Genre, related_name = "authors")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['birth_date']
        verbose_name = "Автор"
        verbose_name_plural = "Автори"

class Book(models.Model):
    title = models.CharField(max_length = 250, unique = True)
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name = "books")
    cover = models.ImageField(upload_to = 'media/')
    genre = models.ManyToManyField(Genre, related_name = "books")
    year_published = models.PositiveIntegerField(default = 1900)
    age_restrictions = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(3),
            MaxValueValidator(120)
        ]
    )
    isbn = models.CharField(max_length = 13, unique = True)
    available = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.title} — {self.author.first_name} {self.author.last_name}"
    
    class Meta:
        ordering = ['author']
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = 'borrows')
    email = models.EmailField(blank=False, null=False)
    birth_date = models.DateField(blank=False, null=False)
    termin = models.PositiveSmallIntegerField(
        choices = [
            (3, '3 дні'),
            (5, '5 днів'),
            (10, '10 днів'),
            (15, '15 днів'),
            (30, '30 днів'),
            (45, '45 днів'),
            (60, '60 днів'),
            (75, '75 днів'),
            (90, '90 днів')
        ],
        default = 30
        )
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.user.username} | Книга "{self.book.title}"'
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Взяття книги"
        verbose_name_plural = "Взяття книг"
