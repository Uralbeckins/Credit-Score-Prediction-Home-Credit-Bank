FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install supervisor to run multiple processes in one container
RUN apt-get update \
    && apt-get install -y --no-install-recommends supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (requirements.txt is at project root)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy project files (paths are relative to build context)
COPY api /app/api
COPY app /app/app
COPY models /app/models

# Supervisor config and optional start script (located in docker/)
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000 8501

# Run supervisord in foreground
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
