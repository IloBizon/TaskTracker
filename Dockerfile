FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000
RUN python manage.py makemigrations && python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000
