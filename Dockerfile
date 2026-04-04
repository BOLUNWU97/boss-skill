FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 bossuser && \
    chown -R bossuser:bossuser /app

USER bossuser

EXPOSE 8080

CMD ["python", "-m", "http.server", "8080", "--directory", "."]
