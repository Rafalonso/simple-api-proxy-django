# simple-api-proxy-django
Scalable simple api proxy using django-rest-framework. This tool aggregates and caches info from various API's in a single call which responds lightweightly. This is particularly useful when you need info from various sources but want to ease the network load off of devices.

## Requirements
1. Python 2.7
2. Django
3. Django-rest-framework
4. Redis
5. pycurl

## Setup
 1. Clone the repository
    `git clone https://github.com/Rafalonso/simple-api-proxy-django.git`.
 2. Create a virtual environment [recommended]
    `http://docs.python-guide.org/en/latest/dev/virtualenvs/`
 3. Install the dependencies `pip install -r requirements.txt`
 4. Run using `python manage.py runserver 0.0.0.0:8000`.
 5. Take you API for a spin! http://localhost:8000/.

## Calling the API

This api comes with a sample request with the following url structure:
  `/events-with-subscriptions/$event_id/`
To call this API you also need an admin user. Here is an example curl request.
  ` curl -u username:password http://127.0.0.1:8000/events/27b9fa174d3e8c317f585d3c86cb9d52_14768033385908/`
It will reproduce this output
`{
    "event_id": "27b9fa174d3e8c317f585d3c86cb9d52_14768033385908",
    "names": [
        "API",
        "Michel",
        "Jasper",
        "Bob",
        "Dennis",
        "Edmon",
        "Aslesha",
        "Lars"
    ],
    "title": "Drink a cup of coffee with C42 Team"
}`

In case the id is not found it will reproduce the following message:
`{
    "status code": 404,
    "message": "Event requested not found"
}`

## Running tests
In the project folder run `python manage.py test`
