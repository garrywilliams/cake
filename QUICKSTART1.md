
# Quickstart

![quickstart](quickstart1.png)

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Clone the repo

```bash
git clone 
cd cake-bakery
```

## API - Part 1

The first iteration of the API is built using Python and the FastAPI framework. The API is deployed using Docker.

```bash
docker compose up -d cake
```

### View the API Docs and interact with the API

The API is available at [localhost:8080](http://localhost:8080/docs) and the swagger docs allow you to interact with the API directly.

[OpenAPI/Swagger Docs](http://localhost:8080/docs)

The following endpoints are available:

- GET /cakes
- GET /cakes/{id}
- POST /cakes
- DELETE /cakes/{id}

### Stop the API

```bash
docker compose down
```
