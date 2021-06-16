FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
RUN apt-get update
RUN apt-get install wkhtmltopdf -y
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn Foodgram.wsgi:application --bind 0:8000