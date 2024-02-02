from django.core.management.base import BaseCommand
import movieposters as mp
from mainapp.models import Movie
import json

class Command(BaseCommand):

    help = "Migrating movies data from database"

    def handle(self, *args, **options):

        movies = Movie.objects.all()
        movies_list = []

        for movie in movies:
            movies_list.append({"Title": movie.title, "Year": movie.year})

        file_name = "C:\\Users\\Tomasz\\Desktop\\movie_recommender\\mainapp\\static\\movie_list07012024.json"        

        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(movies_list, json_file, ensure_ascii=False, indent=2)
