FROM python:3.12-slim

WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalacja Poetry
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# Kopiowanie zależności
COPY pyproject.toml poetry.lock* ./

# Instalacja zależności aplikacji
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Kopiowanie reszty aplikacji
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]