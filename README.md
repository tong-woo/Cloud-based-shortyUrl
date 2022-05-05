# Assignment 3.1: Containerized Shorty URL

As part of the third assignment of the Web Services & Cloud Based Systems course we developed a RESTful service to shorten URLs alongside an authentication service which works using a JWT schema. Both services are dockerized using docker and docker-compose.

Implementation details, answer to questions and the group members contribution can be found in the ```report.pdf``` document in this repository.


## How to Run

0. Make sure you have installed docker and docker-compose in your computer.

1. Clone this repository or download the source code
```commandline
    git clone https://github.com/Web-Services-and-Cloud-Based-Systems-G9/container-virtualization
```

2. Run the following command:
```commandline
    docker-compose up -d
```

3. The login-service will be accessible in the 8081 port (http://127.0.0.1:8081). The shortener-service will be in the 8080 port (http://127.0.0.1:8080). 

4. A [postman collection](https://www.getpostman.com/collections/ab23c363eafd7ece4121) to test the services is available. 

Tested on Python 3.8.9. Developed on Flask 2.1.1. 
