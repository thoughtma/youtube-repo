FROM python:3-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /learnstack

COPY requirements.txt /learnstack/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
