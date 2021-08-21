from django.db import models
from django.db.models.base import Model


class Website(models.Model):
    name = models.CharField(max_length=20)
    home = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    Website = models.ForeignKey(Website, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.URLField(blank=True)
    price = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return "%s %s" % (self.website__name, self.title)
