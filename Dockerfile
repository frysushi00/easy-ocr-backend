# Use an official Python base
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install system deps for building packages and image processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential git curl ffmpeg libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker caching)
COPY requirements.txt .

# Install all dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Environment defaults
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
EXPOSE 5000

# Use gunicorn to serve (wsgi:app must exist)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app", "--workers", "2", "--timeout", "120"]