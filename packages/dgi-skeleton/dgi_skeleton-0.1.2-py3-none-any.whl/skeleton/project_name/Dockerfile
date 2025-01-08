FROM python:3.9-alpine
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc musl-dev

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY . .

EXPOSE 8000
CMD python manage.py migrate && python manage.py collectstatic --no-input && gunicorn --bind 0.0.0.0:8000 --workers=1 configs.wsgi:application
