from django.db import models

class LibraryBook(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    isbn = models.CharField(max_length = 13, unique = True)
    available = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.title} — {self.author}"
    
    class Meta:
        ordering = ['author']
        verbose_name = "Книга в бібліотеці"
        verbose_name_plural = "Книги в бібліотеці"