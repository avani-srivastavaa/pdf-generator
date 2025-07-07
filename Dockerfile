FROM python:3.10-slim

# Set environment to non-interactive (prevents some install prompts)
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and wkhtmltopdf (with proper dependencies)
RUN apt-get update && \
    apt-get install -y \
    wget \
    xfonts-75dpi \
    xfonts-base \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    libjpeg62-turbo \
    && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb && \
    apt-get install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb && \
    rm wkhtmltox_0.12.6-1.buster_amd64.deb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose Flask app port
EXPOSE 5000

# Run the app using gunicorn, from the backend directory
CMD ["gunicorn", "--chdir", "backend", "--bind", "0.0.0.0:5000", "app:app"]
