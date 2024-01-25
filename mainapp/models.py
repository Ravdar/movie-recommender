from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=500)
    year = models.CharField(max_length=10)
    length = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)
    poster_url = models.CharField(max_length=500)
    tmdb_link = models.CharField(max_length=500)
    rating = models.CharField(max_length = 5)
    streaming_services = models.CharField(max_length=10000)
    last_update = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title + " "+ self.year
