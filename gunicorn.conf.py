# Gunicorn configuration
workers = 4
bind = "0.0.0.0:8080"
worker_class = "gthread"
threads = 2
timeout = 120