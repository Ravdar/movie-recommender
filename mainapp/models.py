from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=500)
    year = models.CharField(max_length=10)
    length = models.CharField(max_length=100)
    poster_url = models.CharField(max_length=500)
    imdb_link = models.CharField(max_length=500)
    rating = models.CharField(max_length = 5)
    last_update = models.DateField(null=True, blank=True)

    netflix = models.BooleanField(default=False)
    amazon_prime = models.BooleanField(default=False)
    disney_plus = models.BooleanField(default=False)
    hulu = models.BooleanField(default=False)
    hbo_max = models.BooleanField(default=False)
    apple_tv = models.BooleanField(default=False)
    peacock = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " "+ self.year


# Create your models here.
