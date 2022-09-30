from django.db import models


# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    spoken_language = models.CharField(max_length=50)
    population = models.IntegerField()

    def __str__(self):
        return self.country_name


