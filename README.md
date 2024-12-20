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

```
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "CosmosDBConnectionString": "ENTER COSMOSDB CONNECTION STRING HERE"
  }
}
```

For this program, the most important line here is 