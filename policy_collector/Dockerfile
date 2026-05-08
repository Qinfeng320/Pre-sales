FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create data directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "policy_collector.main:app", "--host", "0.0.0.0", "--port", "8000"]
