FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the code
COPY . .

# Run the app
CMD ["python", "app.py"]
