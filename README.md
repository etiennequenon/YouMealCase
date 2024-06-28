# YouMealCase API

This repository contains the YouMealCase API, a Django-based web application that can be run, tested, and managed using various commands through an `entrypoint.sh` script. The application is containerized using Docker, with a Dockerfile for building the image and a `docker-compose.yaml` file for orchestration, including a PostgreSQL database container.

## Table of Contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Commands](#commands)
- [Docker Configuration](#docker-configuration)
- [Bonus Case Answer](#bonus-case-answer)

## Getting Started

To get started with the YouMealCase API, you will need Docker and Docker Compose installed on your machine. Follow the instructions below to build and run the application.

Next, in the youmealcase root folder container the Dockerfile, run `docker-compose build`

## Usage

Simply run `docker-compose up` to launch the youmeal Api

## Commands

### Available Commands in `entrypoint.sh`

- **run**: Runs the YouMealCase API server. This includes database migrations and creating a superuser if the environment variables `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` are set.
- **test**: Runs the YouMealCase API unit tests.
- **manual**: Runs Django server with manual arguments provided in double quotes.

### Running Commands with Docker Compose

To pass arguments to the `entrypoint.sh` script, use the `docker-compose run` command followed by the service name and the arguments. For example:

- To run the server:
  ```bash
  docker-compose run api run

- To run the tests:
  ```bash
  docker-compose run api test

- To run a manual command:
  ```bash
  docker-compose run api manual "your_command"

## Docker Configuration

### Dockerfile

The Dockerfile is used to build the rest_api image. Make sure you have it properly configured for your Django application.

### docker-compose.yaml

The docker-compose.yaml file is used to orchestrate the containers, including the PostgreSQL database container. Ensure that this file is correctly set up to link the API container with the database container.

## How the API Works

    Recipes: A recipe is the main entity that contains a list of ingredients.
    Ingredients: Each ingredient can have multiple nutrients and associated allergen information.
    Nutrients: Nutrients are associated with ingredients and contain details like name, amount, and unit.

## API Endpoints

    Create a Recipe: Allows you to create a new recipe with its ingredients and their nutrient information.
    Read a Recipe: Fetch details of a specific recipe.
    Update a Recipe: Update an existing recipe along with its nested ingredients and nutrient information.
    Delete a Recipe: Remove a specific recipe from the database.

    Same goes for Nutrients and Ingredients ressources.

## Test the API with Curl

To test the API with curl, you need to use basic authentication with the username and password set in the Docker Compose environment variables located in docker-compose.yaml (DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD).

curl -X POST http://localhost:8000/api/recipes/ -u admin:adminpassword -H "Content-Type: application/json" -d '{
    "name": "Chicken Salad",
    "ingredients": [
        {
            "ingredient": {
                "name": "Chicken Breast",
                "nutrient_information": [
                    {
                        "name": "Protein",
                        "amount": 31,
                        "unit": "g"
                    },
                    {
                        "name": "Fat",
                        "amount": 3.6,
                        "unit": "g"
                    }
                ],
                "allergen_information": "None"
            },
            "quantity": 200
        },
        {
            "ingredient": {
                "name": "Lettuce",
                "nutrient_information": [
                    {
                        "name": "Fiber",
                        "amount": 1.2,
                        "unit": "g"
                    },
                    {
                        "name": "Vitamin C",
                        "amount": 9.2,
                        "unit": "mg"
                    }
                ],
                "allergen_information": "None"
            },
            "quantity": 100
        }
    ]
}'

### Explanation of the JSON Data

- Recipe: The top-level object represents a recipe. It has an id, name, and a list of ingredients.
- Ingredients: Each ingredient is an object that contains:
    - id: The ID of the ingredient.
    - name: The name of the ingredient.
    - nutrient_information: A list of nutrient objects, each containing:
        - id: The ID of the nutrient.
        - name: The name of the nutrient (e.g., Protein, Fat, Fiber).
        - amount: The amount of the nutrient.
        - unit: The unit of measurement for the nutrient (e.g., g, mg).
    - allergen_information: Any allergen information related to the ingredient.
    - quantity: The quantity of the ingredient used in the recipe.

## Summary

The YouMealCase API allows managing recipes with nested ingredients and nutrient information.
Use the provided JSON structure to create, read, update, and delete recipes.
Ensure to test with valid JSON payloads to verify the correct functionality of the API.

## Bonus Case Answer

### How would you handle scalability and performance for this system in a real-world scenario ?

Simply put, the REST architecture is made to scale well. Using this for a simple case as shown is a bit overkill in terms of effort.

My main concerns at this point would be to provide a real production Web server like uWSGI or Gunicorn to allow queueing of requests and avoid server saturation.
I would then probably review as the project grows the overall architecture and add abstractions to keep the business core intact and avoid depending on django models directly.

Perhaps I could also think of moving to another ORM as the Django's built-in tends to have few beautiful bugs with the PostgreSQL's implementation.