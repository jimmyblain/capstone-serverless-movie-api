from pathlib import Path
import json

def get_movies():
    '''Locally read file and return it back in JSON'''
    path = Path('database/database_creation.json')
    movies = path.read_text()
    data = json.loads(movies)
    return data

def get_movies_by_year(year):
    '''Locally read file and print movies from given year'''
    path = Path('database/database_creation.json')
    movies = path.read_text()
    data = json.loads(movies)

    for movie in data:
        if movie['releaseYear'] == year:
            print(movie['title'].title())

get_movies_by_year('2022')
