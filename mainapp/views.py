from django.shortcuts import render
from django.utils import timezone
from django.conf import settings

from .forms import UserPrompt, FeedbackForm
from .utils import get_movie_info_tmdb
from .models import Movie, Recommendation

from openai import OpenAI
import time
import ast
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


def main_view(request):
    """Handles the form submission for movie recommendations, processes API interactions, and updates the UI based on user requests."""

    # Initialize the OpenAI client with the API key from settings
    api_key = settings.OPENAI_API_KEY
    client = OpenAI(api_key=api_key)
    
    response = ""
    
    # Handle POST requests, typically when a user submits a form
    if request.method == "POST":
        start_time = datetime.now()
        
        # Initialize the form with POST data
        prompt_form = UserPrompt(request.POST)
        
        # Check if the form is valid
        if prompt_form.is_valid():
            # Retrieve necessary settings for the assistant
            assistant_id = settings.ASSISTANT_ID
            tools = []
            instructions = settings.INSTRUCTIONS
            prompt_additional_info = settings.PROMPT_ADDITIONAL_INFO
            
            # Update the assistant with the necessary configuration
            assistant = client.beta.assistants.update(assistant_id=assistant_id, tools=tools, instructions=instructions)
            
            # Create a new thread for conversation
            thread = client.beta.threads.create()
            
            # Combine form data with additional information and send as a message
            prompt = prompt_form.cleaned_data['text'] + prompt_additional_info
            message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
            
            # Execute the assistant run and wait for it to finish
            run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
            while run.status == "queued" or run.status == "in_progress":
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                time.sleep(1.5)  # Delay to prevent rapid polling
            
            # Retrieve the response message from the thread
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            string_data = messages.data[0].content[0].text.value.replace("```python", "").replace("```", "")
            
            # Parse the message content to extract a list of movies
            start_index = string_data.find('[')
            end_index = string_data.rfind(']') + 1
            movies_list_str = string_data[start_index:end_index]
            response = ast.literal_eval(movies_list_str)
            
            # Create a record of the recommendation request
            recommendation = Recommendation.objects.create(prompt_text=prompt, datetime_of_prompt=datetime.now())
            
            # Process each movie in the response
            for movie in response:
                movie_title = movie["Title"]
                movie_year = str(movie["Year"])
                
                # Check for existing movie in the database
                db_movie = Movie.objects.filter(title=movie_title, year=movie_year)
                if db_movie.exists():
                    db_movie = Movie.objects.get(title=movie_title, year=movie_year)
                    
                    # Extract additional details if the movie exists
                    poster_link = db_movie.poster_url
                    length = db_movie.length
                    movie_link = db_movie.tmdb_link
                    rating = db_movie.rating
                    full_streaming = db_movie.streaming_services
                else:
                    # Fetch movie info from external source if not found in DB
                    movie_info = get_movie_info_tmdb(movie_title, movie_year)
                    movie_link = movie_info["TMDB link"]
                    poster_link = movie_info["Poster"]
                    rating = movie_info["Rating"]
                    length = movie_info["Length"]
                    full_streaming = movie_info["Streaming"]
                    
                    # Create a new movie record and save it to the database
                    db_movie = Movie(title=movie_title, year=movie["Year"], length=length, poster_url=poster_link, tmdb_link=movie_link, streaming_services=full_streaming, rating=rating, last_update=datetime.today().date())
                    db_movie.save()
                
                # Update movie object with additional details for the front-end
                movie["Rating"] = rating
                movie["Poster"] = poster_link
                movie["Link"] = movie_link
                movie["Length"] = length
                movie["Streaming"] = get_streaming_services(full_streaming.get("PL", {}).get("flatrate", []))
                movie["Renting"] = get_streaming_services(full_streaming.get("PL", {}).get("rent", []))
                movie["Buying"] = get_streaming_services(full_streaming.get("PL", {}).get("buy", []))
                movie["Description"] = movie.get("Plot short description", "")
                
                # Add movie to the recommendation
                recommendation.recommended_movies.add(db_movie)
            
            # Calculate and store the processing time of the recommendation
            processing_time = timedelta(seconds=(datetime.now() - start_time).total_seconds())
            recommendation.response_time = processing_time
            recommendation.save()
            
            # Reset the form for the next request
            prompt_form = UserPrompt()
            
            # Render the response template with the recommendation results
            return render(request, "mainapp/main_view.html", {"prompt_form": prompt_form, "prompt": prompt, "response": response, "processing_time": processing_time})
    
    else:
        # Handle GET requests by initializing an empty form and welcome message
        prompt_form = UserPrompt()
        welcome_message = "Hello! movvie, the intelligent movie matchmaker, is at your service. Share your prompts, and let movvie craft a personalized movie playlist based on your preferences. Begin typing your prompts now!"
    
    # Render the initial form and welcome message for GET requests
    return render(request, "mainapp/main_view.html", {"prompt_form": prompt_form, "welcome_message": welcome_message})

def about_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_form = form.save(commit=False)
            feedback_form.sending_time = timezone.now()
            feedback_form = form.save()
            form=FeedbackForm()
            return render(request, "mainapp/about_view.html", {"form":form, "submit_succes":True})
    else:
        form = FeedbackForm()
    return render(request, "mainapp/about_view.html", {"form":form})


def get_streaming_services(streaming_data):
    try:
        return [
            f"https://image.tmdb.org/t/p/original{platform['logo_path']}"
            for platform in streaming_data
        ]
    except KeyError:
        return []
            

def error_404(request, exception):
    return render(request, 'error.html', status=404)

def error_500(request):
    return render(request, 'error.html', status=500)





