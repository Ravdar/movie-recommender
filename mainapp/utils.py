import urllib.request
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import quote

# user_id = "ur68322908"

def sync_imdb_ratings_list(user_id):
    """Creates .txt file with already seen movies based on an user id"""

    url = f"https://www.imdb.com/user/{user_id}/ratings"
    headers = {'Accept-Language': 'en-US,en;q=0.9'}
    request = urllib.request.Request(url, headers=headers)

    db = []

    with urllib.request.urlopen(request) as response:
        if response.getcode() == 200:
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')

            movies = soup.find_all("h3", class_="lister-item-header")
            for movie in movies:
                title = movie.select_one('h3.lister-item-header a').text.strip()
                year = movie.select_one('h3.lister-item-header span.lister-item-year').text.strip().replace("(", "").replace(")", "")
                db.append(f"{title} {year}")

    file_name = "C:\\Users\\Tomasz\\Desktop\\movie_recommender\\mainapp\\static\\already_seen_movies.txt"

    with open(file_name, 'w', newline='', encoding='utf-8') as txt_file:
        txt_file.write("I have already seen below movies, do not recommend these:"+ '\n'+ '\n')
        for line in db:
            txt_file.write(line + '\n')
            

def sync_imdb_watchlist(user_id):
    """Creates .txt file with imdb watchlist based on an user id"""

    url = f"https://www.imdb.com/user/{user_id}/watchlist"
    headers = {'Accept-Language': 'en-US,en;q=0.9'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        movies = soup.find_all("div", class_="article")

    pattern = r'"year":\["(\d+)"\],"title":"([^"]+)"'

    # Use re.findall to extract matches
    matches = re.findall(pattern, str(movies))

    # Extracted data
    result = [match[1]+ " " +match[0] for match in matches]

    file_name = "C:\\Users\\Tomasz\\Desktop\\movie_recommender\\mainapp\\static\\watchlist.txt"

    with open(file_name, 'w', newline='', encoding='utf-8') as txt_file:
        txt_file.write("Recommend me only movies from below watchlist:"+ '\n'+ '\n')
        for line in result:
            print(line)
            txt_file.write(line + '\n')


def check_streaming(movie_title, year):
    """Returns available streaming platforms list for a particular movie"""

    selected_platforms = []
    movie_title = movie_title.replace(" ", "%20")
    movie_title = movie_title.replace("&", "%26")
    url = f"https://www.justwatch.com/us/search?q={movie_title}%20{year}"

    response = requests.get(url)

    if response.status_code==200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        first_result = soup.find("section", class_="buybox__content inline")
        if first_result:
            platforms = first_result.find_all("div", class_="buybox-row__offers")
            for platform in platforms:
                for element in platform:
                    image = element.find('img')
                    if image:
                        if type(image) != int:
                            platform_name = image.get('alt', 'No alt attribute')
                            selected_platforms.append(platform_name)
        

    return selected_platforms


def check_platforms_for_a_movie(movie_title, year):
    """Returns list fo boolean values for each streaming platform"""
    
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

    if "Apple TV" in platforms or "Apple TV Plus":
        apple_tv = True
    else:
        apple_tv = False

    if "Peacock" in platforms:
        peacock = True
    else:
        peacock = False

    return [netflix, prime_video, hulu, disney_plus, max, apple_tv, peacock]