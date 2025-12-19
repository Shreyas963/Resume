# 1. Use stable Python version compatible with your libraries
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Install system dependencies (needed for scipy, sklearn, lxml)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first (better caching)
COPY requirements.txt .

# 5. Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy full project
COPY . .

# 7. Expose Flask port
EXPOSE 5000

# 8. Run application
CMD ["python", "run.py"]
