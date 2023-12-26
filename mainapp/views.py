from django.shortcuts import render
from .forms import UserPrompt
from openai import OpenAI
import time
import ast
import movieposters as mp
import requests
from bs4 import BeautifulSoup
from .models import Movie
from datetime import datetime

def main_view(request):
    client = OpenAI()
    response = ""
    if request.method =="POST":
        start_time = time.time()
        prompt_form = UserPrompt(request.POST)
        if prompt_form.is_valid():
            assistant = client.beta.assistants.create(name="Movie recommender", instructions='You are a movie expert. Your role is to recommend 5 movies, based on the data provided by an user. The output should be python list of dictionaries with keys: "Title", "Year", "Short description". The list should be named "movies". Do not write anything else, provide just a list.', model="gpt-3.5-turbo-1106")
            thread = client.beta.threads.create()
            prompt = prompt_form.cleaned_data["text"]
            message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
            run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
            while run.status == "queued" or run.status == "in_progress":
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id,
                )
            time.sleep(0.5)
            print(f"Generated {time.time() - start_time}")
            time.sleep(1)
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            string_data = messages.data[0].content[0].text.value
            start_index = string_data.find('[')
            end_index = string_data.rfind(']') + 1
            movies_list_str = string_data[start_index:end_index]
            response = ast.literal_eval(movies_list_str)
            print(f"Before imdb data {time.time() - start_time}")
            for movie in response:
                movie_title = movie["Title"]
                db_movie = Movie.objects.filter(title=movie_title, year=movie["Year"])
                if db_movie.exists():
                    db_movie = Movie.objects.get(title=movie_title, year=movie["Year"])
                    poster_link = db_movie.poster_url
                    length = db_movie.length
                    movie_link = db_movie.imdb_link
                    rating = db_movie.rating
                else:
                    imdb_link_and_local_poster = mp.get_imdb_link_from_title(movie_title)
                    movie_link = imdb_link_and_local_poster
                    poster_rating_length = mp.get_poster_from_imdb_link(imdb_link_and_local_poster[0])
                    poster_link = poster_rating_length[0]
                    rating = poster_rating_length[1]
                    length = poster_rating_length[2]
                    streaming_platforms = check_platforms_for_a_movie(movie_title, movie["Year"])
                    new_db_movie = Movie(title=movie_title, year=movie["Year"], length=length, poster_url = poster_link, imdb_link=imdb_link_and_local_poster[0], rating=rating, netflix = streaming_platforms[0], amazon_prime= streaming_platforms[1], hulu= streaming_platforms[2], disney_plus= streaming_platforms[3], hbo_max= streaming_platforms[4], apple_tv= streaming_platforms[5], peacock= streaming_platforms[6], last_update=datetime.today().date())
                    new_db_movie.save()
                movie["Rating"] = rating
                movie["Poster"] = poster_link
                movie["Link"] = movie_link
                movie["Length"] = length
            processing_time = time.time() - start_time
            return render(request, "mainapp/main_view.html", {"prompt_form":prompt_form, "prompt":prompt, "response":response, "processing_time":processing_time})
    else:
        prompt_form = UserPrompt()
        prompt = "No prompt yet"
    return render(request, "mainapp/main_view.html", {"prompt_form":prompt_form, "prompt":prompt, "response":response})

def check_streaming(movie_title, year):

    selected_platforms = []
    url = f"https://www.justwatch.com/us/search?q={movie_title}%20{year}"

    response = requests.get(url)

    if response.status_code==200:
        soup = BeautifulSoup(response.text, 'html.parser')

        platforms = soup.find_all("div", class_="buybox-row__offers")
        print(platforms)
        for element in platforms[0]:
            image = element.find('img')
            if image:
                if type(image) != int:
                    platform_name = image.get('alt', 'No alt attribute')
                    selected_platforms.append(platform_name)

        for element in platforms[1]:
            image = element.find('img')
            if image:
                if type(image) != int:
                    platform_name = image.get('alt', 'No alt attribute')
                    selected_platforms.append(platform_name)

        for element in platforms[2]:
            image = element.find('img')
            if image:
                if type(image) != int:
                    platform_name = image.get('alt', 'No alt attribute')
                    selected_platforms.append(platform_name)
    
    return selected_platforms

def check_platforms_for_a_movie(movie_title, year):
    
    platforms = check_streaming(movie_title, year)

    if "Netflix" in platforms:
        netflix = True
    else: 
        netflix = False

    #Amazonvideo is not subscribe model, only rent or buy
    if "Amazon Prime Video" in platforms or "Amazon Video" in platforms:
        prime_video = True
    else:
        prime_video = False

    if "Hulu" in platforms:
        hulu = True
    else:
        hulu = False

    if "Disney Plus" in platforms:
        disney_plus = True
    else:
        disney_plus = False

    if "Max" in platforms:
        max = True
    else:
        max = False

    if "Apple TV" in platforms:
        apple_tv = True
    else:
        apple_tv = False

    if "Peacock" in platforms:
        peacock = True
    else:
        peacock = False

    return [netflix, prime_video, hulu, disney_plus, max, apple_tv, peacock]


