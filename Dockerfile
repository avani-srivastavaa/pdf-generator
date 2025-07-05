FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wkhtmltopdf \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
