# The Cake Bakery

![Cake Bakery](cake-bakery.png)

## The Task Summary

Build and deploy a Python API for Docker (or Kubernetes)

---

## The Story

### Part 1

[Quickstart - Part 1](QUICKSTART1.md)

[README - Part 1](bakery/README.md)

[The bakery wants to build an API to manage their cakes...](STORY1.md) 

This part of the story is about building a solution that fufills the requirements and acceptance criteria, taking a pragmatic interative approach and delivering a working robust solution. A number of assumptions and decisions were documented along the way and in a real-life scenario these would be discussed and agreed with the client and other stakeholders to shape the solution.

---

### Part 2

[Quickstart - Part 2](QUICKSTART2.md)

[The Cake Detector](detector/README.md)

[README - Part 2](gateway/README.md)

[The API goes viral...](STORY2.md) 

This part of the story is about working with and enhancing existing solutions. In this case we assume that the API in Part 1 was developed by a different organisation and we have been asked to enhance it. It is not always possible to implement a full rewrite within time and resource constraints, and it is important to be able to work with existing solutions and build on them.

AS part of this story we learn to understand the client's situation and requirements and then make decisions about how to proceed. We would document these decisions in Architecture Decision Records (ADRs), for example. In this case we have decided that the best approach is to build a new API and deploy it as a gateway to the existing API.

---

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
