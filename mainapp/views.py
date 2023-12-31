from django.shortcuts import render
from django.http import JsonResponse
from .forms import UserPrompt
from openai import OpenAI
import time
import ast
import movieposters as mp
import requests
from bs4 import BeautifulSoup
from .models import Movie
from datetime import datetime
from .utils import check_platforms_for_a_movie

def main_view(request):
    print(request.headers)
    print(request.headers.get("x-requested-with"))
    client = OpenAI()   
    response = ""
    file = client.files.create(file=open("C:\\Users\\Tomasz\\Desktop\\movie_recommender\\mainapp\\static\\already_seen_movies.txt", "rb"), purpose="assistants")
    assistant = client.beta.assistants.create(name="Movie recommender", instructions='You are a movie expert. Your role is to recommend 5 (five) movies, based on the data provided by an user.Please response with python list of dictionaries named "movies" with keys: "Title", "Year", "Plot short description".  No salutes, no explanations, no thank you, nothing other than the specified python list. Also do not recommend movies attached in a file, these are already watched.', model="gpt-3.5-turbo-1106", tools=[{"type": "retrieval"}], file_ids=[file.id])
    thread = client.beta.threads.create()
    if request.method =="POST":
        start_time = time.time()
        prompt_form = UserPrompt(request.POST)
        if prompt_form.is_valid():
            prompt = prompt_form.cleaned_data['text'] + "Please remember to not write any additional text in a response, provide just a list."
            message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
            run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
            print(run)
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
            print(string_data)
            start_index = string_data.find('[')
            end_index = string_data.rfind(']') + 1
            movies_list_str = string_data[start_index:end_index]
            response = ast.literal_eval(movies_list_str)
            print(f"Before imdb data {time.time() - start_time}")
            for movie in response:
                movie_title = movie["Title"]
                db_movie = Movie.objects.filter(title=movie_title, year=movie["Year"])
                if db_movie.exists():
                    print(db_movie)
                    db_movie = Movie.objects.get(title=movie_title, year=movie["Year"])
                    poster_link = db_movie.poster_url
                    length = db_movie.length
                    movie_link = db_movie.imdb_link
                    rating = db_movie.rating
                else:
                    imdb_link_and_local_poster = mp.get_imdb_link_from_title(movie_title)
                    movie_link = imdb_link_and_local_poster[0]
                    poster_rating_length = mp.get_poster_from_imdb_link(imdb_link_and_local_poster[0])
                    poster_link = poster_rating_length[0]
                    rating = poster_rating_length[1]
                    length = poster_rating_length[2]
                    streaming_platforms = check_platforms_for_a_movie(movie_title, movie["Year"])
                    db_movie = Movie(title=movie_title, year=movie["Year"], length=length, poster_url = poster_link, imdb_link=imdb_link_and_local_poster[0], rating=rating, netflix = streaming_platforms[0], amazon_prime= streaming_platforms[1], hulu= streaming_platforms[2], disney_plus= streaming_platforms[3], hbo_max= streaming_platforms[4], apple_tv= streaming_platforms[5], peacock= streaming_platforms[6], last_update=datetime.today().date())
                    db_movie.save()
                movie["Rating"] = rating
                movie["Poster"] = poster_link
                movie["Link"] = movie_link
                movie["Length"] = length
                movie["Platforms"] = db_movie.get_streaming_platforms()
                movie["Description"] = movie["Plot short description"]
            processing_time = time.time() - start_time
            prompt_form = UserPrompt()
            if not request.headers.get("x-requested-with") == "XMLHttpRequest":
                print("NOT AJAX")
                return render(request, "mainapp/main_view.html", {"thread":thread,"prompt_form":prompt_form, "prompt":prompt, "response":response, "processing_time":processing_time})
            else:
                print("AJAX")
                return JsonResponse({"thread":thread,"prompt_form":prompt_form, "prompt":prompt, "response":response, "processing_time":processing_time})
    else:   
        prompt_form = UserPrompt()
        prompt = "No prompt yet"
    return render(request, "mainapp/main_view.html", {"prompt_form":prompt_form, "prompt":prompt, "response":response})




def find_movies(client, assistant, thread):
    prompt = "5 more, please. Please remember to not write any additional text in a response, provide just a list."
    message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
    time.sleep(0.5)
    time.sleep(1)
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    string_data = messages.data[0].content[0].text.value
    print(string_data)
    start_index = string_data.find('[')
    end_index = string_data.rfind(']') + 1
    movies_list_str = string_data[start_index:end_index]
    response = ast.literal_eval(movies_list_str)
    for movie in response:
        movie_title = movie["Title"]
        db_movie = Movie.objects.filter(title=movie_title, year=movie["Year"])
        if db_movie.exists():
            print(db_movie)
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
            db_movie = Movie(title=movie_title, year=movie["Year"], length=length, poster_url = poster_link, imdb_link=imdb_link_and_local_poster[0], rating=rating, netflix = streaming_platforms[0], amazon_prime= streaming_platforms[1], hulu= streaming_platforms[2], disney_plus= streaming_platforms[3], hbo_max= streaming_platforms[4], apple_tv= streaming_platforms[5], peacock= streaming_platforms[6], last_update=datetime.today().date())
            db_movie.save()
        movie["Rating"] = rating
        movie["Poster"] = poster_link
        movie["Link"] = movie_link
        movie["Length"] = length
        movie["Platforms"] = db_movie.get_streaming_platforms()
        movie["Description"] = movie["Plot short description"]

