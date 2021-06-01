FROM python:3

COPY requirements.txt /chat/requirements.txt

WORKDIR /chat

RUN pip install -r requirements.txt

COPY . /chat


ENV FLASK_APP main.py

CMD flask run
