# Serverless Movie API

This project is the capstone to [Phase Two of the Learn to Cloud program](https://learntocloud.guide/phase2/#capstone-project-serverless-movies-api). The intent is to create a couple of *serverless* functions that can query a databse for information regarding movies. Additionally, the database holds a field for movie cover images, which is just a URL to this image in Azure Storage.

## Cloud Infrastructure

The minimum cloud infrastructure needed to complete this project is:

- NoSQL database
- Cloud Storage
- Serverless Functions

My cloud platform of choice is Microsoft Azure, so the specific set of infrastructure I chose, respecitively, is:

- Azure CosmosDB
  - Reasoning: This is the preferred NoSQL solution for Azure. The data for this project is quite simple and structured so I am sure any and SQL service would have sufficed.
- Azure Blob Storage
  - No need for any file structure to the data stored here (cover images of movies).
- Azure Functions
  - Function-as-a-Service that allows us to run self-contained pieces of code. The trigger for these functions are HTTP requests.
