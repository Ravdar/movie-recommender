import tmdbsimple as tmdb
from datetime import timedelta
import requests
import json

def convert_movie_length(minutes):
    """Converts minutes into hours-minutes format (e.g 140 -> 2h20m)."""
      
    hours = minutes//60
    minutes = minutes%60

    return f"{hours}h {minutes}m"

def get_tmdb_id(title, year):
    """Returns TMDB id based on provided movie info."""
    
    slugified_title = f"{title} {str(year)}".replace("-", "").replace(" ", "-").replace(",", "").replace(":","")
    headers = {'Content-Type':'application/json',
    'trakt-api-version':'2',
    'trakt-api-key':'e257c4ec8fc660f3e17f95e5cddd8daf1f178db4cc6ef86ed76bad66d5727c3f'}
    movie = requests.get(f'https://api.trakt.tv/movies/{slugified_title}', headers=headers).json()

    return movie["ids"]["tmdb"]

def get_movie_info_tmdb(title, year):
    """Returns length, description, streaming services, tmdb link, tmdb rating and poster path for a given movie."""
    
    tmdb.API_KEY = "fc42d2861e48ecba18363aaa6fc2aaa0"
    try:
        tmdb_id = get_tmdb_id(title, year)
        movie = tmdb.Movies(tmdb_id)
    except:
        search = tmdb.Search()
        search_results = search.movie(query=title)
        movie = tmdb.Movies(search.results[0]["id"]) 
        tmdb_id = movie_detailed_info['id']      
    movie_detailed_info = movie.info()
    length_in_minutes =int(movie_detailed_info["runtime"])
    length = convert_movie_length(length_in_minutes)
    description = movie_detailed_info["overview"]
    streaming_services = movie.watch_providers()["results"]
    # imdb_id = movie_detailed_info["imdb_id"]
    # imdb_link = f"https://www.imdb.com/title/{imdb_id}/"
    tmdb_link = f"https://www.themoviedb.org/movie/{tmdb_id}"
    tmdb_rating = movie_detailed_info["vote_average"]
    poster_path = f"https://image.tmdb.org/t/p/w300_and_h450_bestv2{movie_detailed_info['poster_path']}"
  
    movie_info = {"Length":length, "Description":description, "Streaming":streaming_services, "TMDB link":tmdb_link, "Rating":tmdb_rating, "Poster":poster_path}

    return movie_info









