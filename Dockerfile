FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# >>> penting: pastikan root project /app ada di sys.path
ENV PYTHONPATH=/app

EXPOSE 8000

# jalankan Flask dengan module path eksplisit
CMD ["flask", "--app", "web.app", "run", "--host=0.0.0.0", "--port=8000"]

