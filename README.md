# Serverless Movie API

This project is the capstone to [Phase Two of the Learn to Cloud program](https://learntocloud.guide/phase2/#capstone-project-serverless-movies-api). The intent is to create a couple of *serverless* functions that can query a databse for information regarding movies. Additionally, the database holds a field for movie cover images, which is just a URL to this image in Azure Storage.

## Cloud Infrastructure/Services

The recommended minimum cloud infrastructure needed to complete this project is:

- NoSQL database
- Cloud Storage
- Serverless Functions

My cloud platform of choice is Microsoft Azure, so the specific set of infrastructure I chose, respecitively, is:

- **Azure CosmosDB**
  - This is the preferred NoSQL solution for Azure. The data for this project is quite simple and structured so I am sure any SQL service would have sufficed.
- **Azure Blob Storage**
  - No need for any file structure to the data stored here (cover images of movies).
- **Azure Functions**
  - Function-as-a-Service that allows us to run self-contained pieces of code. The trigger for these functions are HTTP requests.
  - Language of choice: **Python**

## Step One - Preparing the Services

I used the Azure Portal to deploy both CosmosDB and Blob Storage.

### Blob Storage

This was relatively easy to set up as its only purpose is to be a repository of images. After creation and uploading of images to the container, the most important setting is ensuring that anonymous access is enabled. This allows any and all visitors to the see the images at these links.

To enable this setting, navigate to: **Selected Storage Account -> Settings -> Configuration -> Allow Blob Anonymous Access -> Set to *Enabled***

### CosmosDB

After creating my database, I needed to submit data to be queried with my functions. I opted to create a small, JSON formatted list on my own since there wasn't much value in having a large data set for this project.

```python
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
```

The JSON file that this code outputs can be easily uploaded into CosmosDB via the portal.

## Step Two - The Functions

Using VSCode and its many Azure Extensions, namely the Azure Functions subset of tools, my IDE automatically prepared a folder environment with prepared virtual envrionment, JSON settings files, and a start to the main function program. Due to using the Python V2 Model, the functions are all contained in one main file at the root rather than spread throughout the folder structure. Let's start with the local.settings.json file:

### JSON Settings

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "CosmosDBConnectionString": "ENTER COSMOSDB CONNECTION STRING HERE"
  }
}
```

For this program, the most important line is the value assigned to "CosmosDBConnectionString". As you'll see in the function_app.py code, this variable is necessary to read the data from your chosen database. It is bad security practice to enter this string in plaintext in your code, so we store the value in the local.settings.json file and it is retrieved as an environmental variable.

> [!IMPORTANT]
> Make sure your local.settings.json is included in your .gitignore. Publishing these strings and keys to your repository defeats the purpose of obfuscation.

### Functions

As previously stated, due to the using the Python V2 Model for Azure Functions, all functions are contained within a single program. This program only has two functions:

- GetMovies(): Return a JSON list of movies in the database.
- GetMoviesByYear('year'): Pass a year value at the end of the URL, and return JSON list of only movies released from that year in the database.

```python
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
```

To test, I was able able run this program locally using the following command in the terminal (while in this directory):

```bash
func start
```

If all works, it will produce two HTTP endpoints that you can navigate to in your browser to trigger these functions. [See documentation for more information.](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python#start)

## Step Three - Deployment

Once the functions are confirmed to work locally, you can deploy them to Azure Functions. If you started this project in VSCode using the Azure Extensions, then you need only navigate to the extension, right-click the function app in the Functions section, and select **Deploy to Function App**.

You can confirm this worked properly by checking two locations in Azure Functions:

1. A copy of your folder and file structure in **Function App -> Functions -> App Files**
2. Your functions appear in the "Functions" submenu of the Overview page.

> [!IMPORTANT]
> If your functions are not appearing even though they worked fine locally, the issue is likely due to your CosmosDBConnectionString missing as an environmental variable. To resolve this, enter the same variable name and connection string from your JSON settings file within **Function App -> Settings -> Environmental Variables**. Add the values as an App Setting, NOT a Connection String, despite the name. Confusing, I know.

Once your functions appear on the Overview page, you're finished! You can test the code by navigating to the API endpoints in your browser. Your URLs will follow this pattern:
- GetMovies: https://[FUNCTION-APP-NAME].azurewebsites.net/api/getmovies
- GetMoviesByYear: https://[FUNCTION-APP-NAME].azurewebsites.net/api/getmoviesbyyear/[YEAR]
