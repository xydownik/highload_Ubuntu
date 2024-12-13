# Use Python slim image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc python3-dev musl-dev \
    build-essential \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Install Cassandra dependencies
RUN pip install cassandra-driver

# Copy requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-it.sh script
COPY scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copy application code
COPY . .

# Expose ports for Gunicorn and Cassandra
EXPOSE 8000 8001 8002 8003

# Set Gunicorn as the default command
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "market.wsgi:application"]
