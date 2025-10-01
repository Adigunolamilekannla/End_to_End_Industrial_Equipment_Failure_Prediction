# Build stage
FROM python:3.10.14-slim-bullseye AS builder

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install build dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --user -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Runtime stage
FROM python:3.10.14-slim-bullseye

# Set working directory
WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local

# Ensure Python path for the user
ENV PATH=/root/.local/bin:$PATH

# Copy the rest of the code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Run the app
CMD ["python", "app.py"]