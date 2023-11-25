# The Cake Bakery

![Cake Bakery](bakery/cake.png)

## The Task Summary

Build and deploy a Python API for Docker (or Kubernetes)

## The Story - Part 1

The bakery wants to build an API to manage their cakes. They want to be able to list all cakes, add a new cake, delete an existing cake and get a cake by id.

There is an urgency to get this API built and deployed as soon as possible. The bakery has a lot of cakes to bake and they need to be able to manage them. A third party is engaged to build the API.

The bakery is so happy with the idea of an API that they want to share it with the world. They want to be able to share the API with other bakeries so that they can manage their cakes too.

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
2. Build the API in Python using the FastAPI framework
   - Produces a Swagger spec automatically
   - Models and associated validation is built into the framework
3. Use a SQLite database to store the cake data
   - There are no non-functional requirements for expected use of the API, and the team **assume** there will be a low number of cake submissions
4. Docker to deploy the API
    - Simple to deploy and run and can readly be deployed to AWS, GCP, Azure, etc.
5. No authentication
    - There are no non-functional requirements for authentication
    - Removes the need for secrets management
    - Removes the need for a user management system
6. Use the [Pydantic](https://pydantic-docs.helpmanual.io/) library for data validation
    - Pydantic is built into the FastAPI framework
    - Pydantic is a popular library for data validation in Python
7. Use the [SQLAlchemy](https://www.sqlalchemy.org/) library for database access
8. Use the [Alembic](https://alembic.sqlalchemy.org/en/latest/) library for database migrations
    - Alembic is built into the FastAPI framework
    - Alembic is a popular library for database migrations in Python
9. Use the [pytest](https://docs.pytest.org/en/stable/) library for unit testing
10. Use the [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) library for code coverage
11. Use the [black](https://black.readthedocs.io/en/stable/) library for code formatting
12. Use the [flake8](https://flake8.pycqa.org/en/latest/) library for linting
13. Use the [isort](https://pycqa.github.io/isort/) library for import sorting
14. Not including CI/CD in this iteration
    - There are no non-functional requirements for CI/CD
    - The team **assume** that the CI/CD pipeline will be built using GitHub Actions
    - No pre-commit hooks, for example
    - No automated code formatting, linting, testing, etc.
15. Not including a logging solution in this iteration
16. Makefile for common commands
    - `make test` - Run the unit tests
    - `make lint` - Run the linter (black and flake8)
    - `make clean` - Reset
    - `make migrations` - Run the database migrations
    - `make run` - Run the API
