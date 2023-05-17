from django.db import models
from author.models import Author
from works.models import Works


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="comments")
    works = models.ManyToManyField(Works, related_name="works", blank=True)
    quantity_works = models.IntegerField(blank=True)
