FROM python:3.10-slim

# Install system dependencies and fonts required by wkhtmltopdf
RUN apt-get update && apt-get install -y \
    build-essential \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    xfonts-75dpi \
    xfonts-base \
    wget \
    gnupg \
    fontconfig \
    && apt-get clean

# Manually install full version of wkhtmltopdf (binary .deb)
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb || true && \
    apt-get install -y -f && \
    rm -f wkhtmltox_0.12.6-1.buster_amd64.deb

# Set working directory
WORKDIR /app

# Copy all project files into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose Flask/Gunicorn port
EXPOSE 5000

# Start the Flask app using Gunicorn (from backend folder)
CMD ["gunicorn", "--chdir", "backend", "--bind", "0.0.0.0:5000", "app:app"]
