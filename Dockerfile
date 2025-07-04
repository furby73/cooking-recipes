FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP cooking-recipes.py
ENV FLASK_ENV production  

RUN groupadd -r webuser && useradd -r -g webuser webuser

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

RUN chown -R webuser:webuser /app
USER webuser

EXPOSE 5000

CMD ["sh", "-c", \
    "flask db init || true && \
    flask db migrate -m 'Initial migration' && \
    flask db upgrade && \
    gunicorn --config gunicorn_config.py cooking-recipes:app"]
