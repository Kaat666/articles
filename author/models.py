from django.db import models
from works.models import Works
from django.contrib.auth.models import AbstractUser, Permission


class Author(AbstractUser):
    fullname = models.TextField()
    works = models.ManyToManyField(Works, related_name="works", blank=True)
    quantity_works = models.IntegerField(blank=True)
    email = models.EmailField()
    password = models.CharField(max_length=50)
