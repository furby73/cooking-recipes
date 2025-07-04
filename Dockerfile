FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP cooking-recipes.py
ENV FLASK_ENV development

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["sh", "-c", \
    "flask db init || true && \
    flask db migrate -m 'Initial migration' && \
    flask db upgrade && \
    flask run --host=0.0.0.0 --port=5000"]