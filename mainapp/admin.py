from django.contrib import admin
from .models import Movie, Recommendation, Feedback

admin.site.register(Movie)
admin.site.register(Recommendation)
admin.site.register(Feedback)

# Register your models here.
