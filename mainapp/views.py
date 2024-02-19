from django.shortcuts import render
from django import forms
from django.utils import timezone

from .forms import UserPrompt, FeedbackForm
from .utils import get_movie_info_tmdb
from .models import Movie, Recommendation

from openai import OpenAI
import time
import ast
from datetime import datetime, timedelta


def main_view(request):
    client = OpenAI()   
    response = ""
    if request.method =="POST":
        start_time = datetime.now()
        prompt_form = UserPrompt(request.POST)
        if prompt_form.is_valid():
            # Checking searchbar tools settings
            assistant_id = 'asst_uLNsyXn04oFs1mxJkCdbEwVv'
            tools = []
            file_ids = []
            instructions = 'You are a movie expert. Your role is to recommend 5 (five) movies, based on the data provided by an user.Please response with python list of dictionaries named "movies" with keys: "Title", and "Plot short description".  No salutes, no explanations, no thank you, nothing other than the specified python list.'
            prompt_additional_info = " Please remember to not write any additional text in a response, provide just a list of 5 movies."

            if prompt_form.cleaned_data["gpt_4"]:
                assistant_id = 'asst_6bqZAqHpKP48jTaxrCSlbbxL' # 'asst_sKuRYRpYQWM6VigUHTnFzUhk'
                # file_id = 'file-E7IBRtoF7uImZmH9kU36urA1'
                tools = [{"type": "retrieval"}]
                file_ids = [file_id]
            if prompt_form.cleaned_data["only_watchlist"]:
                assistant_id = 'asst_sKuRYRpYQWM6VigUHTnFzUhk'
                # file_id = 'file-6J32Lw7YXCBQyIuYCA1tRAsH'
                tools = [{"type": "retrieval"}]
                file_ids = [file_id]

            elif prompt_form.cleaned_data["without_seen"]:
                assistant_id = 'asst_sKuRYRpYQWM6VigUHTnFzUhk'
                # file_id = 'file-qWa8QHBYup9GjeskZCHtvlFh'
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
                # file_id = 'file-E7IBRtoF7uImZmH9kU36urA1'
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
            time.sleep(1)
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            string_data = messages.data[0].content[0].text.value.replace("```python", "").replace("```","")
            print(string_data)
            start_index = string_data.find('[')
            end_index = string_data.rfind(']') + 1
            movies_list_str = string_data[start_index:end_index]
            response = ast.literal_eval(movies_list_str)
            recommendation = Recommendation.objects.create(prompt_text=prompt, datetime_of_prompt=datetime.now())
            for movie in response:
                movie_title = movie["Title"]
                movie_year = str(movie["Year"])
                db_movie = Movie.objects.filter(title=movie_title, year=movie_year)
                if db_movie.exists():
                    db_movie = Movie.objects.get(title=movie_title, year=movie_year)
                    poster_link = db_movie.poster_url
                    length = db_movie.length
                    movie_link = db_movie.tmdb_link
                    rating = db_movie.rating
                    full_streaming = db_movie.streaming_services
                    try:
                        streaming = full_streaming["US"]["flatrate"]
                        print(streaming)
                        streaming_services = [f"https://image.tmdb.org/t/p/original{platform['logo_path']}" for platform in streaming]
                        print(streaming_services)
                    except:
                        streaming_services = []
                    try:
                        renting = full_streaming["US"]["rent"]
                        print(renting)
                        renting_services = [f"https://image.tmdb.org/t/p/original{platform['logo_path']}" for platform in renting]
                        print(renting_services)
                    except:
                        renting_services = []
                    try:
                        buying = full_streaming["US"]["buy"]
                        print(buying)
                        buying_services = [f"https://image.tmdb.org/t/p/original{platform['logo_path']}" for platform in buying]
                        print(buying_services)
                    except:
                        buying_services = []
                else:
                    print(movie)
                    print("NOT EXISTS")
                    movie_info = get_movie_info_tmdb(movie_title, movie_year)
                    movie_link = movie_info["TMDB link"]
                    poster_link = movie_info["Poster"]
                    rating = movie_info["Rating"]
                    length = movie_info["Length"]
                    full_streaming = movie_info["Streaming"]
                    try:
                        print(f'Streaming: {full_streaming["US"]["flatrate"]}')
                        streaming_services = [f"https://image.tmdb.org/t/p/original{platform['logo_path']}" for platform in full_streaming["US"]["flatrate"]]
                        print(streaming_services)
                    except:
                        streaming_services = []
                    try:
                        print(f'Renting: {full_streaming["US"]["rent"]}')
                        renting_services = [f"https://image.tmdb.org/t/p/original{platform['logo_path']}" for platform in full_streaming["US"]["rent"]]
                        print(renting_services)
                    except:
                        renting_services = []
                    try:
                        print(f'Buying: {full_streaming["US"]["buy"]}')
                        buying_services = [f"https://image.tmdb.org/t/p/original{platform['logo_path']}" for platform in full_streaming["US"]["buy"]]
                        print(buying_services)
                    except:
                        buying_services = []                                                
                    db_movie = Movie(title=movie_title, year=movie["Year"], length=length, poster_url = poster_link, tmdb_link=movie_link, streaming_services = full_streaming, rating=rating, last_update=datetime.today().date())
                    db_movie.save()
                movie["Rating"] = rating
                movie["Poster"] = poster_link
                movie["Link"] = movie_link
                movie["Length"] = length
                movie["Streaming"] = streaming_services
                movie["Renting"] = renting_services
                movie["Buying"] = buying_services
                movie["Description"] = movie["Plot short description"]
                recommendation.recommended_movies.add(db_movie)
            processing_time = timedelta(seconds=(datetime.now() - start_time).total_seconds())
            print(type(processing_time))
            recommendation.response_time = processing_time
            recommendation.save()
            prompt_form = UserPrompt()
            return render(request, "mainapp/refactored.html", {"prompt_form":prompt_form, "prompt":prompt, "response":response, "processing_time":processing_time})
    else:
        prompt_form = UserPrompt()
        welcome_message = "Hello! MovieNeon, the intelligent movie matchmaker, is at your service. Share your prompts, and let MovieNeon craft a personalized movie playlist based on your preferences. Begin typing your prompts now!"
    return render(request, "mainapp/refactored.html", {"prompt_form":prompt_form,"welcome_message":welcome_message})

def about_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_form = form.save(commit=False)
            feedback_form.sending_time = timezone.now()
            feedback_form = form.save()
            # Here I want to display box with thanks for feedback or just redirect to succes_url
            return render(request, "about_view.html", {"form":form})
    else:
        form = FeedbackForm()
    return render(request, "about_view.html", {"form":form})

def error_404(request, exception):
    return render(request, 'error.html', status=404)

def error_500(request):
    return render(request, 'error.html', status=500)
            




