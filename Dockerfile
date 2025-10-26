# Use an official Python base
FROM python:3.10-slim

# set workdir
WORKDIR /app

# Install system deps for building packages and image processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential git curl ffmpeg libglib2.0-0 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker caching)
COPY requirements.txt .

# Install CPU-only PyTorch wheels (explicit index) then requirements
# NOTE: adjust torch version if you want a specific version
RUN pip install --no-cache-dir torch==2.0.1+cpu torchvision==0.15.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html \
 && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Environment defaults
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
EXPOSE 5000

# Use gunicorn to serve (wsgi:app must exist)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app", "--workers", "2", "--timeout", "120"]
