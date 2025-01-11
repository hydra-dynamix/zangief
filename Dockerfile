FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

# Install communex from git
RUN pip install git+https://github.com/renlabs-dev/communex

# Copy requirements files
COPY validator_requirements.txt .
COPY requirements.txt .
COPY m2m_miner_requirements.txt .
COPY openai_miner_requirements.txt .
COPY translate_miner_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r validator_requirements.txt \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r m2m_miner_requirements.txt \
    && pip install --no-cache-dir -r openai_miner_requirements.txt \
    && pip install --no-cache-dir -r translate_miner_requirements.txt

# Copy the source code
COPY src/ ./src/
COPY setup.py .
COPY pyproject.toml .

# Install the package
RUN pip install -e .

# Copy environment example file
COPY .env.example .env.example

# Set environment variables
ENV PYTHONPATH=/app/src
ENV TESTNET=0
ENV VALIDATOR_CALL_TIMEOUT=20
ENV VALIDATOR_INTERVAL=10

# Run the validator
CMD ["python", "-m", "zangief.validator.validator"]
