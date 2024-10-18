FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD . /app/

RUN  pip install --upgrade pip
RUN  pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "soundwave.wsgi", "--bind:0.0.0.0:8000"]