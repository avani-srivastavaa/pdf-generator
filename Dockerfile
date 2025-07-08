FROM python:3.9-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    xfonts-75dpi \
    xfonts-base \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    libjpeg62-turbo \
    libssl1.1 \
    && wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt install -y ./wkhtmltox_0.12.6-1.buster_amd64.deb \
    && rm wkhtmltox_0.12.6-1.buster_amd64.deb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "--chdir", "backend", "--bind", "0.0.0.0:5000", "app:app"]
