FROM python:3.10-slim

# Install system dependencies for wkhtmltopdf
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
    && apt-get clean

# Manually install wkhtmltopdf (since `apt-get install wkhtmltopdf` on slim image installs an incomplete version)
RUN apt-get update && \
    apt-get install -y wget gnupg fontconfig xfonts-75dpi xfonts-base libjpeg-turbo8 && \
    wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb || true && \
    apt-get install -y -f && \
    rm wkhtmltox_0.12.6-1.buster_amd64.deb


# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the Flask app with gunicorn
CMD ["gunicorn", "--chdir", "backend", "--bind", "0.0.0.0:5000", "app:app"]
