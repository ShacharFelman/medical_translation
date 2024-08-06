FROM python:3.9-slim

WORKDIR /app

COPY requierments.txt .
RUN pip install --no-cache-dir -r requierments.txt

COPY src/ /app/src/

CMD ["python", "src/main.py"]