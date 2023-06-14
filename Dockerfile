FROM python:3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SENTRY_DSN $SENTRY_DSN
ENV HEROKU_APP_NAME $HEROKU_APP_NAME
ENV PORT 8080

COPY . .

RUN python3 -m pip install -r requirements.txt --no-cache-dir

CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:$PORT