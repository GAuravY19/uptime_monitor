# Use Python 3.12 Slim Image
FROM python:3.12-slim

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create Working Directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Expose FastAPI Port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
