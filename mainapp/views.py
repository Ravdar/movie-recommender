from django.shortcuts import render
from .forms import UserPrompt
from openai import OpenAI
import time
import ast
import movieposters as mp

def main_view(request):
    client = OpenAI()
    response = ""
    if request.method =="POST":
        start_time = time.time()
        prompt_form = UserPrompt(request.POST)
        if prompt_form.is_valid():
            assistant = client.beta.assistants.create(name="Movie recommender", instructions="You are a movie expert. Your role is to recommend 5 movies, based on the data provided by an user. The output should be python list of dictionaries with keys: 'Title', 'Year', 'Short description'. The list should be named 'movies'. Do not write anything else, provide just a list.", model="gpt-3.5-turbo-1106")
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
                imdb_link = mp.get_imdb_link_from_title(movie_title)
                poster_rating_lentgh = mp.get_poster_from_imdb_link(imdb_link)
                print(poster_rating_lentgh)
                poster_link = poster_rating_lentgh[0]
                rating = poster_rating_lentgh[1]
                length = poster_rating_lentgh[2]
                movie["Poster"] = poster_link
                movie["Link"] = imdb_link
                movie["Rating"] = rating
                movie["Length"] = length
            print(response)
            processing_time = time.time() - start_time
            return render(request, "mainapp/main_view.html", {"prompt_form":prompt_form, "prompt":prompt, "response":response, "processing_time":processing_time})
    else:
        prompt_form = UserPrompt()
        prompt = "No prompt yet"
    return render(request, "mainapp/main_view.html", {"prompt_form":prompt_form, "prompt":prompt, "response":response})

