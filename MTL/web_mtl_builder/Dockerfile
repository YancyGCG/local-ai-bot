# Dockerfile for MTL Document Builder
FROM python:3.11-slim

WORKDIR /app

# Install required system dependencies for LibreOffice (soffice)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-writer \
    fonts-liberation \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to utilize Docker caching
COPY web_mtl_builder/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire MTL directory
COPY . .

# Create directories for uploads and generated files if they don't exist
RUN mkdir -p uploads generated_mtls
RUN chmod 777 uploads generated_mtls

# Verify templates are available
RUN ls -la templates/

# Set environment variables
ENV PYTHONUNBUFFERED=1

EXPOSE 5555

# Use a more robust command to run the app
CMD ["python", "web_mtl_builder/app.py"]
