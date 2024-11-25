FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["/app/django.sh"]
