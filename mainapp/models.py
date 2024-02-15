from django.db import models

FEEDBACK_CATEGORIES = (
    ("error", "Error/bug"),
    ("feedback", "Feedback"),
    ("question", "Question"),
    ("other", "Other"),
)

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
    
class Recommendation(models.Model):
    datetime_of_prompt = models.DateTimeField(null=True, blank=True)
    # User data? IP \ Geolocation \ Language Pref \ Device (mobile\pc)
    prompt_text = models.CharField(max_length=2000)
    # if_random = models.BooleanField()
    response_time = models.DurationField(null=True, blank=True) # as timedelta seconds
    recommended_movies = models.ManyToManyField(Movie, related_name='recommendations')
    # if error

class Feedback(models.Model):
    category = models.CharField(max_length = 40, choices=FEEDBACK_CATEGORIES, default='feedback')
    mail = models.CharField(max_length = 20)
    content = models.TextField()