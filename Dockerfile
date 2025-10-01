# Dockerfile for All-in-One MTL Demo (FastAPI + Python)
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for FastAPI and DOCX
RUN pip install --no-cache-dir fastapi uvicorn python-docx pydantic

# Copy source code
COPY src/ ./src/
COPY templates/ ./templates/
COPY MTL/ ./MTL/

# Expose port
EXPOSE 8899

# Start the FastAPI server
CMD ["uvicorn", "src.web_api:app", "--host", "0.0.0.0", "--port", "8899"]
