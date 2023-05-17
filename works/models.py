from django.db import models


class Works(models.Model):
    name = models.CharField(max_length=100)
    author = models.TextField()
    type = models.TextField()
    date_release = models.DateField()
    file = models.FileField()
    quantity_char = models.IntegerField()
