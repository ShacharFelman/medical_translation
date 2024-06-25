# ollama/Dockerfile

# Use the base Ollama image
FROM ollama/ollama:latest

# Copy the ollama_start.sh script into the container
COPY ollama_start.sh /app/ollama_start.sh

# Set the appropriate permissions
RUN chmod +x /app/ollama_start.sh

# Set the entrypoint to the script
ENTRYPOINT ["sh", "/app/ollama_start.sh"]