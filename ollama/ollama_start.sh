#!/bin/sh

echo "Starting the Ollama translator service..."

# Start Ollama in the background
ollama serve &

# Wait for Ollama to start
sleep 5

# Pull and run llama3 model
ollama run llama3