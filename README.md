# Assignment 3.2: Container Orchestrations

As part of the third assignment of the Web Services & Cloud Based Systems course we developed a RESTful service to shorten URLs alongside an authentication service which works using a JWT schema. Both services are dockerized using docker and docker-compose. And then services are deployed in Kubernetes.

Implementation details, answer to questions, experience working with Kubernetes and the group members contribution can be found in the ```report.pdf``` document in this repository.


## How to Run

1. The login-service will be accessible in the 31000 port (http://145.100.134.64:31000). The shortener-service will be in the 32000 port (http://145.100.134.64:32000). Open an browser and access our UI:
```commandline
    http://145.100.134.64:32000/home
```

2. A [postman collection](https://www.getpostman.com/collections/ab23c363eafd7ece4121) to test the services is available. 

Tested on Python 3.8.9. Developed on Flask 2.1.1. Deployed on Kubernetes 1.23.0
