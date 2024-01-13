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
from .utils import check_platforms_for_a_movie
from django import forms

def main_view(request):
    client = OpenAI()   
    response = ""
    if request.method =="POST":
        start_time = time.time()
        prompt_form = UserPrompt(request.POST)
        if prompt_form.is_valid():
            # Checking searchbar tools settings
            assistant_id = 'asst_uLNsyXn04oFs1mxJkCdbEwVv'
            tools = []
            file_ids = []
            instructions = 'You are a movie expert. Your role is to recommend 5 (five) movies, based on the data provided by an user.Please response with python list of dictionaries named "movies" with keys: "Title", "Year", "Plot short description".  No salutes, no explanations, no thank you, nothing other than the specified python list.'
            prompt_additional_info = " Please remember to not write any additional text in a response, provide just a list."

            if prompt_form.cleaned_data["gpt_4"]:
                assistant_id = 'asst_6bqZAqHpKP48jTaxrCSlbbxL' # 'asst_sKuRYRpYQWM6VigUHTnFzUhk'
                file_id = 'file-E7IBRtoF7uImZmH9kU36urA1'
                tools = [{"type": "retrieval"}]
                file_ids = [file_id]
            if prompt_form.cleaned_data["only_watchlist"]:
                assistant_id = 'asst_sKuRYRpYQWM6VigUHTnFzUhk'
                file_id = 'file-6J32Lw7YXCBQyIuYCA1tRAsH'
                tools = [{"type": "retrieval"}]
                file_ids = [file_id]

            elif prompt_form.cleaned_data["without_seen"]:
                assistant_id = 'asst_sKuRYRpYQWM6VigUHTnFzUhk'
                file_id = 'file-qWa8QHBYup9GjeskZCHtvlFh'
                tools = [{"type": "retrieval"}]
                file_ids = [file_id]

            # Checking streaming services
            selected_platforms = []
            for field_name, field in prompt_form.fields.items():
                if isinstance(field, forms.BooleanField) and field_name not in ['without_seen', 'only_watchlist', 'gpt_4']:
                    if prompt_form.cleaned_data[field_name]:
                        selected_platforms.append(field.label)
            selected_platforms_str = ""

            if selected_platforms == [] or len(selected_platforms) == 7:
                pass
            else:
                assistant_id = 'asst_6bqZAqHpKP48jTaxrCSlbbxL'#'asst_sKuRYRpYQWM6VigUHTnFzUhk'
                file_id = 'file-E7IBRtoF7uImZmH9kU36urA1'
                tools = [{"type": "retrieval"}]
                file_ids = [file_id]
                prompt_additional_info = f' available on of these streaming platforms: {selected_platforms} .Please remember to not write any additional text in a response, provide just a list.'


            assistant = client.beta.assistants.update(assistant_id=assistant_id, tools=tools, file_ids=file_ids, instructions=instructions)
            thread = client.beta.threads.create()
            prompt = prompt_form.cleaned_data['text'] + prompt_additional_info
            print(prompt)
            message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
            run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
            while run.status == "queued" or run.status == "in_progress":
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id,
                )
            time.sleep(0.5)
            print(f"Generated {time.time() - start_time}")
            time.sleep(1)
            print(assistant)
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            print(thread)
            print(messages)
            print(messages.data[0].content[0].text.value)
            string_data = messages.data[0].content[0].text.value.replace("```python", "").replace("```","")
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
                    print("NOT EXISTS")
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
            return render(request, "mainapp/main_view.html", {"prompt_form":prompt_form, "prompt":prompt, "response":response, "processing_time":processing_time})
    else:
        prompt_form = UserPrompt()
        welcome_message = "Hello! MovieNeon, the intelligent movie matchmaker, is at your service. Share your prompts, and let MovieNeon craft a personalized movie playlist based on your preferences. Begin typing your prompts now!"
    return render(request, "mainapp/main_view.html", {"prompt_form":prompt_form, "welcome_message":welcome_message})




