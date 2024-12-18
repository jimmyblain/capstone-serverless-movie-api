# This file exists purely to create the JSON file that I will load in CosmosDB
from pathlib import Path
import json


movie_data = [
    {
        "id":"1",
        "title":"the batman",
        "releaseYear":"2022",
        "genre":"thriller",
        "coverUrl":""
    },

   {
        "id":"2",
        "title":"avatar: the way of the water",
        "releaseYear":"2022",
        "genre":"sci-fi",
        "coverUrl":""
    },


   {
        "id":"3",
        "title":"casablanca",
        "releaseYear":"1942",
        "genre":"romance",
        "coverUrl":""
    },

   {
        "id":"4",
        "title":"good will hunting",
        "releaseYear":"1997",
        "genre":"drama",
        "coverUrl":""
    },


]

path = Path('database/database_creation.json')
database = json.dumps(movie_data)
path.write_text(database)