This file describes the role of endpoints, what they are used for etc.

In [FastAPI](https://fastapi.tiangolo.com/) an endpoint is a route or path that is associated with a particular function or operation in the web application. Each endpoint can handle different types of HTTP requests and is defined using Python functions decorated with FastAPI's routing decorators.

After starting the server, FastAPI automatically creates [Swagger](https://swagger.io/tools/swagger-ui/) documentation, containing more information about the endpoints. The documentation is found at `/docs/` endpoint.
