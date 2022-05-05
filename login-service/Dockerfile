FROM python:3.8

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8081

CMD ["python3", "./login-service/ShortyLogin.py"]


