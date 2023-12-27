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

    def get_streaming_platforms(self):
        platforms = {
            'netflix': 'https://images.justwatch.com/icon/207360008/s100/netflix.webp',
            'amazon_prime': 'https://images.justwatch.com/icon/52449861/s100/amazonprimevideo.webp',
            'disney_plus': 'https://images.justwatch.com/icon/147638351/s100/disneyplus.webp',
            'hulu': 'https://images.justwatch.com/icon/116305230/s100/hulu.webp',
            'hbo_max': 'https://images.justwatch.com/icon/285237061/s100/hbomax.webp',
            'apple_tv': 'https://images.justwatch.com/icon/190848813/s100/itunes.webp',
            'peacock': 'https://images.justwatch.com/icon/194173870/s100/peacocktv.webp',
        }
        return {key: value.format(self.id) for key, value in platforms.items() if getattr(self, key)}
