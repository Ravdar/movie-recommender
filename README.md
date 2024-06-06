# ![movvie-tv2](https://github.com/Ravdar/movie-recommender/assets/97836782/9eb62a3e-d007-4964-88ba-81c2098c6d67)  movvie - AI movie recommender





movvie is web application developed using Django and integrated with the OpenAI API, that delivers personalized movie recommendations. Upon receiving a user's prompt, it suggests five curated films. Additionally, the application features a function to generate random movie selections. Each recommendation includes the movie’s poster, title, production year, TMDB rating, duration, streaming availability, and a concise description, utilizing data from TMDB and JustWatch APIs.


[movvie Intro.webm](https://github.com/Ravdar/movie-recommender/assets/97836782/7e1efca9-b55b-4566-a18a-17e2939035f2)



For a more detailed video with my commentary, click [here.](https://www.youtube.com/watch?v=iPoaw0x15Wo)

# Features

movvie offers following features:

### 1. Tailored movie recommendation
Upon receiving a user's prompt, it suggests five selected films
### 2. Movie basic info
For each recommendation there is basic information such as:
* poster
* title
* year of production
* rating
* length
* short description
### 3. Watch providers info
App will also show available watch providers for each movie, informing about streaming, buying and renting options
### 4. Drawing of recommendation
After clicking dice button, application will suggest five random movies
### 5. Feedback
There is feedback form on a website, where users can give their feedback about page, report a bug or question.

# Techstack

* Django
* OpenAI API
* TMDB API
* django models
* django forms

# Screenshots
![movvie-homepage](https://github.com/Ravdar/movie-recommender/assets/97836782/2264e4c2-d050-4dca-a079-2723e47a6c01)
![movvie-results](https://github.com/Ravdar/movie-recommender/assets/97836782/43752a78-751d-47d6-b712-35648f8cd136)
![movvie-atch-providers](https://github.com/Ravdar/movie-recommender/assets/97836782/fb0dea28-7671-4732-905f-e3c0922d44a9)
![movvie-about-page](https://github.com/Ravdar/movie-recommender/assets/97836782/f894ef98-2b14-46da-87a4-e158d9ae43db)
![movvie-loading-screen](https://github.com/Ravdar/movie-recommender/assets/97836782/df6af2f4-1c06-4953-97db-e28c6b50fa89)


# Installation
1. Clone the repository:
```git clone https://github.com/Ravdar/movie-recommender```
2. Install the required libraries:
```pip install -r requirements.txt```
3. Run the application:
```python main.py```
4. Access the app in your web browser via your local server
