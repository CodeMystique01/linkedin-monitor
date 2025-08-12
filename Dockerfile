# Multi-stage build for React frontend and Python backend
FROM node:18-alpine AS frontend-build

# Set working directory for frontend
WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source
COPY frontend/ ./

# Build frontend
RUN npm run build

# Python backend stage
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome dependencies for Selenium
RUN apt-get update && apt-get install -y \
    libnss3-dev \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%.*}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Copy Python requirements
COPY requirements.txt ./
COPY backend/requirements.txt ./backend_requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r backend_requirements.txt

# Copy Python source
COPY . .

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Copy backend
COPY backend/ ./backend/

# Create necessary directories
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Environment variables
ENV PYTHONPATH=/app
ENV NODE_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/status || exit 1

# Run the backend server
CMD ["python", "backend/app.py"]
