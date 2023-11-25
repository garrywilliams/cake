# The Cake Bakery

![Cake Bakery](gateway/gateway.png)

## The Task Summary

Build and deploy a Python API for Docker (or Kubernetes)

## The Story - Part 2

The API is a massive success and goes viral. The bakery is inundated with cake traffic and there is a need to scale the API to handle the load, monitor the API to ensure it is healthy and available, and extend the capabilities of the API. 

They also need to understand how the API is being used so they can plan for the future and there are also concerns that some of the cakes submitted are not actually cakes.

### The Requirements

- [x] The API should return an OpenAPI or Swagger spec.
- [x] You should be able to list all cakes.
- [x] You should be able to add another cake.
- [x] You should be able to delete an existing cake.
- [x] All cake data should come from the API, using standard GET/POST/DELETE HTTP endpoints.

### Data model : Cake

- id: <number> (required)
- name: <string> (required, no more than 30 characters)
- comment: <string> (required, no more than 200 characters)
- imageUrl: <string> (required)
- yumFactor: <number> (required, number between 1 and 5 inclusive)


#### Example Cake

```json
{
  "id": 1,
  "name": "Lemon cheesecake",
  "comment": "A cheesecake made of lemon",
  "imageUrl": "http://www.food.com/recipelemon-cheesecake-31004",
  "yumFactor": 3
}
```

### The Acceptance Criteria

- [x] The API should be deployed to Docker or Kubernetes
- [x] The API should be downloadable and runnable after a simple git clone.
- [x] The API specification should be detailed enough to allow a hypothetical team to implement a client to consume it.
- [x] Don’t worry about authentication
- [x] A lot of modern software development is about using 3rd party packages the right way, so pick your favourites and show us you know how to use them.
- [x] Make your own choices about data persistence, server framework etc, and we’ll see if they add up.

### Architecture Decision Records

1. Start from scratch approach (as far as possible)
   - No boilerplate code
   - No pre-existing code
2. Build the API in Python using the Django framework
   - Produces a Swagger spec automatically
   - Models and associated validation is built into the framework
3. There currently isn't budget or time to rebuild the current API, so the new API will be deployed as a gateway to the current API
1. Use a Postgres database to store the cake request data
   - This is a more robust and scalable solution than the current solution
   - The database can be readied for storing Cake data
2. Docker to deploy the API
    - Simple to deploy and run and can readly be deployed to AWS, GCP, Azure, etc.
3. No authentication
    - There are no non-functional requirements for authentication
    - Removes the need for secrets management
    - Removes the need for a user management system
4. Use the [Pydantic](https://pydantic-docs.helpmanual.io/) library for data validation
    - Pydantic is a popular library for data validation in Python
5. Use the [black](https://black.readthedocs.io/en/stable/) library for code formatting
6.  Use the [flake8](https://flake8.pycqa.org/en/latest/) library for linting
7.   Use the [isort](https://pycqa.github.io/isort/) library for import sorting
8.   Not including CI/CD in this iteration
    - There are no non-functional requirements for CI/CD
    - The team **assume** that the CI/CD pipeline will be built using GitHub Actions
    - No pre-commit hooks, for example
    - No automated code formatting, linting, testing, etc.
9.  Not including a logging solution in this iteration
10. Makefile for common commands
    - `make test` - Run the unit tests
    - `make lint` - Run the linter (black and flake8)
    - `make clean` - Reset
    - `make migrations` - Run the database migrations
    - `make run` - Run the API
11. Use the [Django Rest Framework](https://www.django-rest-framework.org/) to build the API
    - The Django Rest Framework is a popular library for building APIs in Python
12. Configure for Prometheus monitoring
    - Prometheus is a popular monitoring solution
    - It is easy to deploy and configure
    - It is easy to integrate with Grafana
13. Use Celery for asynchronous tasks
    - Celery is a popular library for running asynchronous tasks
    - It is easy to deploy and configure
    - It is easy to integrate with Django
14. Use Redis as a message broker for Celery
15. Use Flower for monitoring Celery
    - Flower is a popular library for monitoring Celery
    - It is easy to deploy and configure
    - It is easy to integrate with Django
  