# Base image
FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /learnstack_app

COPY . /learnstack_app

RUN apt-get update && pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]