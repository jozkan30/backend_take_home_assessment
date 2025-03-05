## Stock API

To get started install the following:
  - [Python 3.12](https://docs.python.org/3.12/)
  - [Poetry](https://python-poetry.org/)
  - [Make](https://www.gnu.org/software/make/)

Create Virtual Environment
- Run `poetry install` to install dependencies and create the virtual environment.

Activate Virtual Environment
- Run `poetry env activate` to output the activation command.
- Run the output command (e.g., source /path/to/activate) to activate the virtual environment.

Run Application
- Run `make run`

Once server is running use the following curl commands to hit each endpoint updating the authorization with your API Key.

Example Usage:

`/lookup`
curl -X GET -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Authorization: YOUR_API_KEY' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.32.3' 'http://127.0.0.1:8000/lookup?symbol=IBM&date=2025-02-28'

`/min`
curl -X GET -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Authorization: YOUR_API_KEY' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.32.3' 'http://127.0.0.1:8000/min?symbol=AAPL&days=5'

`/max`
curl -X GET -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Authorization: YOUR_API_KEY' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.32.3' 'http://127.0.0.1:8000/max?symbol=F&days=5'


### Discussion

  - What compromises did you make due to time constraints?

    Given the time constraints, I had to prioritize the core functionality of the project. While I implemented basic error handling, I would have liked to devote more time to developing robust testing and protection methods. With more time, I would focus on creating more elegant error handling mechanisms that provide clearer insights into error meanings and status codes for both logs and users.

  - What would you do differently if this software was meant for production use?

    Similar to question 1, I would focus on enhancing its reliability, maintainability, and security. I would add more error handling mechanisms that provide detailed error information and suggestions for resolution and reflect this in the tests. Additionally, I would restructure the repository to accommodate more complex methods, organizing it into separate directories for each route, containing dedicated services and helper functions. This would enable easier maintenance, updates, and scaling, ultimately making the software more robust and secure for production use. Finally, I would engage in a thorough code review with a colleague to ensure that the code meets our team's standards.


  - Propose how you might implement authentication, such that only authorized users may hit these endpoints.

    To implement authentication checks for endpoints, we could integrate with a third-party solution like OAuth 2.0 or HashiCorp's Vault and have middleware handle it.This involves creating an endpoint to generate a token, which is then verified on subsequent requests.Alternatively, we can leverage FastAPI's HTTP Basic Authentication. This would require us to create a User model, which we would store with the associated ID and hashed password. Then, on requests to endpoints, verify that password and grant a token.

  - How much time did you spend on this exercise?

    I spent roughly 4-5 hours on this exercise. It is important to me to not only demonstrate my commitment to producing clean code but also to delivering a strong, reliable project that is well-structured and maintainable

  - Please include any other comments about your implementation.

    In stock_api originally boilerplate you will find:
    app.py -  Creates instance of the Fast API
    route.py -  Defines routes and calls service method for that route
    service.py - Makes requests to API and does the heavy lifting. Also contains some helper functions
    client.py -  Contains integration test which can be run while server is running.

  - Please include any general feedback you have about the exercise.

  I enjoyed this exercise. It is very fair and engaging! I am grateful to participate.