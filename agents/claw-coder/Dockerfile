FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy application
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Make scripts executable
RUN chmod +x *.py *.sh

# Expose ports
EXPOSE 11434

CMD ["./run_all_agents.sh"]
