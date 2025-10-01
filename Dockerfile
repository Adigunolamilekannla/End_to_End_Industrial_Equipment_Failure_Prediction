FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements first (better for caching layers)
COPY requirements.txt .

# Install dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the code
COPY . .

# Run app
CMD ["python", "app.py"]
