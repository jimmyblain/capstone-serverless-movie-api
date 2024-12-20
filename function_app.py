import azure.functions as func
from azure.cosmos import CosmosClient
import os
import json

# Initialize CosmosDB client
# In Azure Functions, CosmosDB string is added as App Setting Environmental Variable
COSMOS_CONNECTION_STRING = os.getenv("CosmosDBConnectionString")
DATABASE_NAME = "MovieDatabase"
CONTAINER_NAME = "Movies"

client = CosmosClient.from_connection_string(COSMOS_CONNECTION_STRING)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.function_name(name="getmovies")
@app.route(route="getmovies")
def get_movies(req: func.HttpRequest) -> func.HttpResponse:
    ''' Defining endpoint that returns JSON list of all movies'''
    items = list(container.read_all_items())
    
    return func.HttpResponse(
        json.dumps(items, indent=4),
        mimetype="application/json",
        status_code=200
    )

# Function to return movies by year
@app.function_name(name="getmoviesbyyear")
@app.route(route="getmoviesbyyear/{year}")
def get_movies_by_year(req: func.HttpRequest) -> func.HttpResponse:
    '''Using provided year in API call, return list of movies from that year'''

    # Grab the year from the route 
    year = req.route_params.get("year")

    if not year:
        return func.HttpResponse(
            "Please provide a valid year in the URL, e.g., /getmoviesbyyear/2022.",
            status_code=400
        )
  
    # Read all contents of the CosmosDB into a list
    items = list(container.read_all_items())
    filtered_items = []

    # Loop through list of movies
    # Add movies of the specified year to filtered list
    for item in items:
        if item['releaseYear'] == year:
            filtered_items.append(item)

    if not filtered_items:
        return func.HttpResponse(
            f"No movies found for the year '{year}'.",
            status_code=404
        )

    return func.HttpResponse(
        json.dumps(filtered_items, indent=4),
        mimetype="application/json",
        status_code=200
    )