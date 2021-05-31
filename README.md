# Chat

 simple chat app! 

## Local Setup:

install anaconda: https://www.anaconda.com/products/individual
</br>
install docker https://www.docker.com/products/docker-desktop

From the project directory:
* `conda create  -n chat python=3.8`
* `cd docker`
* ` docker-compose up`
* `export FLASK_APP=main.py`

Run the SQL Migration
* `flask db init`
* `flask db upgrade`

Run the flask app:
`flask run`





